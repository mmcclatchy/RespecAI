#!/bin/bash

# Fast package detection script - no LLM needed!
# Returns JSON of detected packages and versions
# Usage: detect-packages.sh [project_directory]

set -euo pipefail

# Change to project directory if provided
if [[ $# -gt 0 ]]; then
    cd "$1"
fi

START_TIME=$(date +%s)
TEMP_DIR=$(mktemp -d)
PACKAGES_FILE="$TEMP_DIR/packages.json"
DEPENDENCIES_FILE="$TEMP_DIR/dependencies.json"
VERSIONS_FILE="$TEMP_DIR/versions.json"
FILES_FILE="$TEMP_DIR/files.json"
MANAGERS_FILE="$TEMP_DIR/managers.json"

echo '{}' > "$PACKAGES_FILE"
echo '{}' > "$DEPENDENCIES_FILE"
echo '{}' > "$VERSIONS_FILE"
echo '[]' > "$FILES_FILE"
echo '[]' > "$MANAGERS_FILE"

# Helper functions
add_package() {
    local name="$1"
    local version="$2"
    jq --arg name "$name" --arg version "$version" '. + {($name): $version}' "$PACKAGES_FILE" > "$PACKAGES_FILE.tmp" && mv "$PACKAGES_FILE.tmp" "$PACKAGES_FILE"
}

add_explicit_dependency() {
    local name="$1"
    local version="$2"
    jq --arg name "$name" --arg version "$version" '. + {($name): $version}' "$DEPENDENCIES_FILE" > "$DEPENDENCIES_FILE.tmp" && mv "$DEPENDENCIES_FILE.tmp" "$DEPENDENCIES_FILE"
}

add_version() {
    local name="$1"
    local version="$2"
    jq --arg name "$name" --arg version "$version" '. + {($name): $version}' "$VERSIONS_FILE" > "$VERSIONS_FILE.tmp" && mv "$VERSIONS_FILE.tmp" "$VERSIONS_FILE"
}

add_file() {
    local file="$1"
    jq --arg file "$file" '. + [$file]' "$FILES_FILE" > "$FILES_FILE.tmp" && mv "$FILES_FILE.tmp" "$FILES_FILE"
}

add_manager() {
    local manager="$1"
    if [[ $(jq --arg manager "$manager" 'index($manager)' "$MANAGERS_FILE") == "null" ]]; then
        jq --arg manager "$manager" '. + [$manager]' "$MANAGERS_FILE" > "$MANAGERS_FILE.tmp" && mv "$MANAGERS_FILE.tmp" "$MANAGERS_FILE"
    fi
}

# JavaScript/Node.js - Parse both package.json and lockfiles
if [[ -f "package.json" ]]; then
    add_file "package.json"
    add_manager "npm"
    
    # Extract explicit dependencies from package.json
    if command -v jq >/dev/null 2>&1; then
        jq -r '.dependencies // {} | to_entries[] | "\(.key) \(.value)"' package.json 2>/dev/null | while read -r name version; do
            add_explicit_dependency "$name" "$version"
        done
        jq -r '.devDependencies // {} | to_entries[] | "\(.key) \(.value)"' package.json 2>/dev/null | while read -r name version; do
            add_explicit_dependency "$name" "$version"
        done
    fi
fi

# Extract exact versions from lockfiles
if [[ -f "package-lock.json" ]]; then
    add_file "package-lock.json"
    
    # Extract exact versions from lockfile
    if command -v jq >/dev/null 2>&1; then
        # Parse packages from npm lockfile v2/v3 format
        jq -r '.packages // {} | to_entries[] | select(.key != "") | "\(.key | ltrimstr("node_modules/")) \(.value.version // "")"' package-lock.json 2>/dev/null | while read -r name version; do
            if [[ -n "$version" && "$version" != "null" ]]; then
                add_version "$name" "$version"
            fi
        done
        
        # Fallback to dependencies format for older lockfiles
        if [[ $(jq -r '.dependencies // {} | length' package-lock.json 2>/dev/null) -gt 0 ]]; then
            jq -r '.dependencies // {} | to_entries[] | "\(.key) \(.value.version // "")"' package-lock.json 2>/dev/null | while read -r name version; do
                if [[ -n "$version" && "$version" != "null" ]]; then
                    add_version "$name" "$version"
                fi
            done
        fi
    fi
elif [[ -f "yarn.lock" ]]; then
    add_file "yarn.lock"
    add_manager "yarn"
    
    # Parse yarn.lock format: package@version:
    awk '
    /^[^[:space:]].*@.*:/ {
        # Extract package name and version from yarn.lock entry
        gsub(/@.*:/, "")  # Remove @version: part to get package name
        package = $1
        # Remove quotes if present
        gsub(/["'"'"']/, "", package)
    }
    /^[[:space:]]+version[[:space:]]+".*"/ {
        # Extract version
        gsub(/^[[:space:]]+version[[:space:]]+["'"'"']/, "")
        gsub(/["'"'"'].*$/, "")
        if (package != "") {
            print package " " $1
            package = ""
        }
    }
    ' yarn.lock 2>/dev/null | while read -r name version; do
        if [[ -n "$name" && -n "$version" ]]; then
            add_version "$name" "$version"
        fi
    done
elif [[ -f "pnpm-lock.yaml" ]]; then
    add_file "pnpm-lock.yaml"
    add_manager "pnpm"
    
    # Parse pnpm-lock.yaml dependencies
    if command -v yq >/dev/null 2>&1; then
        # Extract from dependencies and devDependencies
        yq eval '.dependencies // {} | to_entries[] | .key + " " + .value' pnpm-lock.yaml 2>/dev/null | while read -r name version; do
            # Clean up version (remove registry info)
            version=$(echo "$version" | sed 's/@.*$//' | sed 's/^[^0-9]*//')
            if [[ -n "$version" ]]; then
                add_version "$name" "$version"
            fi
        done
        yq eval '.devDependencies // {} | to_entries[] | .key + " " + .value' pnpm-lock.yaml 2>/dev/null | while read -r name version; do
            version=$(echo "$version" | sed 's/@.*$//' | sed 's/^[^0-9]*//')
            if [[ -n "$version" ]]; then
                add_version "$name" "$version"
            fi
        done
    fi
fi

# requirements.txt (pip)
if [[ -f "requirements.txt" ]]; then
    add_file "requirements.txt"
    add_manager "pip"
    
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// }" ]] && continue
        
        # Extract package==version or package>=version etc
        if [[ "$line" =~ ^([a-zA-Z0-9_.-]+)[=~\>\<]+([0-9][^[:space:]]*).*$ ]]; then
            add_explicit_dependency "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
        fi
    done < requirements.txt
fi

# Python - Parse both pyproject.toml and lockfiles
if [[ -f "pyproject.toml" ]]; then
    add_file "pyproject.toml"
    add_manager "uv"
    
    # Parse dependencies and dependency-groups (explicit dependencies)
    if command -v uv >/dev/null 2>&1; then
        uv run python -c "
import sys
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        sys.exit(0)

try:
    with open('pyproject.toml', 'rb') as f:
        data = tomllib.load(f)
    
    # Get project dependencies
    deps = data.get('project', {}).get('dependencies', [])
    for dep in deps:
        if isinstance(dep, str):
            # Parse 'package>=1.0.0' format
            for sep in ['>=', '==', '~=', '>', '<', '!=']:
                if sep in dep:
                    name, version = dep.split(sep, 1)
                    print(f'{name.strip()} {version.strip()}')
                    break
            else:
                # No version specified
                print(f'{dep.strip()} *')
    
    # Get dependency-groups
    groups = data.get('dependency-groups', {})
    for group_name, group_deps in groups.items():
        for dep in group_deps:
            if isinstance(dep, str):
                for sep in ['>=', '==', '~=', '>', '<', '!=']:
                    if sep in dep:
                        name, version = dep.split(sep, 1)
                        print(f'{name.strip()} {version.strip()}')
                        break
                else:
                    print(f'{dep.strip()} *')
except:
    pass
" 2>/dev/null | while read -r name version; do
            add_explicit_dependency "$name" "$version"
        done
    fi
fi

# Extract exact versions from uv.lock
if [[ -f "uv.lock" ]]; then
    add_file "uv.lock"
    
    # Parse uv.lock for exact package versions
    if command -v uv >/dev/null 2>&1; then
        uv run python -c "
import sys
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        sys.exit(0)

try:
    with open('uv.lock', 'rb') as f:
        data = tomllib.load(f)
    
    # Extract packages from [[package]] entries
    packages = data.get('package', [])
    for pkg in packages:
        if isinstance(pkg, dict) and 'name' in pkg and 'version' in pkg:
            name = pkg['name'].strip()
            version = pkg['version'].strip()
            print(f'{name} {version}')
except:
    pass
" 2>/dev/null | while read -r name version; do
            add_version "$name" "$version"
        done
    fi
fi

# Rust - Parse both Cargo.toml and Cargo.lock
if [[ -f "Cargo.toml" ]]; then
    add_file "Cargo.toml"
    add_manager "cargo"
    
    # Extract explicit dependencies from Cargo.toml
    sed -n '/^\[dependencies\]/,/^\[/p' Cargo.toml | grep -E '^[a-zA-Z]' | while IFS= read -r line; do
        if [[ "$line" =~ ^([a-zA-Z0-9_-]+)[[:space:]]*=[[:space:]]*[\"\']*([0-9][^\"\']*).*$ ]]; then
            add_explicit_dependency "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
        fi
    done
fi

# Extract exact versions from Cargo.lock
if [[ -f "Cargo.lock" ]]; then
    add_file "Cargo.lock"
    
    # Parse Cargo.lock for exact package versions
    awk '
    /^\[\[package\]\]/ {
        in_package = 1
        name = ""
        version = ""
    }
    in_package && /^name = / {
        gsub(/^name = ["'"'"']/, "")
        gsub(/["'"'"'].*$/, "")
        name = $0
    }
    in_package && /^version = / {
        gsub(/^version = ["'"'"']/, "")
        gsub(/["'"'"'].*$/, "")
        version = $0
    }
    /^$/ {
        if (in_package && name != "" && version != "") {
            print name " " version
        }
        in_package = 0
        name = ""
        version = ""
    }
    ' Cargo.lock 2>/dev/null | while read -r name version; do
        if [[ -n "$name" && -n "$version" ]]; then
            add_version "$name" "$version"
        fi
    done
fi

# Go - Parse both go.mod and go.sum
if [[ -f "go.mod" ]]; then
    add_file "go.mod"
    add_manager "go"
    
    # Extract explicit dependencies from go.mod
    grep -E '^[[:space:]]*[a-zA-Z]' go.mod | while read -r line; do
        if [[ "$line" =~ ^[[:space:]]*([a-zA-Z0-9./_-]+)[[:space:]]+v([0-9][^[:space:]]*).*$ ]]; then
            add_explicit_dependency "${BASH_REMATCH[1]}" "v${BASH_REMATCH[2]}"
        fi
    done
fi

# Extract exact versions from go.sum
if [[ -f "go.sum" ]]; then
    add_file "go.sum"
    
    # Parse go.sum for exact package versions (take first occurrence of each package)
    awk '
    {
        # Extract package and version from go.sum format: module version hash
        if ($2 ~ /^v[0-9]/ && !seen[$1]) {
            print $1 " " $2
            seen[$1] = 1
        }
    }
    ' go.sum 2>/dev/null | while read -r name version; do
        if [[ -n "$name" && -n "$version" ]]; then
            add_version "$name" "$version"
        fi
    done
fi


END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))

# Combine explicit dependencies with exact versions from lockfiles
DEPENDENCIES=$(cat "$DEPENDENCIES_FILE")
VERSIONS=$(cat "$VERSIONS_FILE")

# Create final packages by combining explicit deps with exact versions
COMBINED_PACKAGES=$(echo '{}' | jq --argjson deps "$DEPENDENCIES" --argjson versions "$VERSIONS" '
    reduce ($deps | to_entries[]) as $item ({};
        . + {
            ($item.key): (
                if $versions | has($item.key)
                then $versions[$item.key]
                else $item.value
                end
            )
        }
    )
')

# Fallback to old behavior if no explicit dependencies found
if [[ "$COMBINED_PACKAGES" == "{}" ]]; then
    COMBINED_PACKAGES=$(cat "$PACKAGES_FILE")
fi

DETECTED_FILES=$(cat "$FILES_FILE")
MANAGERS=$(cat "$MANAGERS_FILE")

RESULT=$(jq -n \
    --argjson packages "$COMBINED_PACKAGES" \
    --argjson detected_files "$DETECTED_FILES" \
    --argjson package_managers "$MANAGERS" \
    --argjson execution_time_ms "$EXECUTION_TIME" \
    '{
        detected_files: $detected_files,
        packages: $packages,
        package_managers: $package_managers,
        execution_time_ms: $execution_time_ms
    }')

# Cleanup temp dir
rm -rf "$TEMP_DIR"

echo "$RESULT"