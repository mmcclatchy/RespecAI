#!/bin/bash
set -e

# Specter Installation Script
# Installs Specter workflow system to a target project
# Supports both local execution and remote curl-based installation

# GitHub repository details
GITHUB_RAW_URL="https://raw.githubusercontent.com/mmcclatchy/specter/main"
SETUP_COMMAND_PATH=".claude/commands/specter-setup.md"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

print_debug() {
    echo -e "${BLUE}DEBUG: $1${NC}"
}

# Detect if running via curl (remote) or direct execution (local)
detect_execution_mode() {
    if [ -n "$BASH_SOURCE" ] && [ -f "$BASH_SOURCE" ]; then
        echo "local"
    else
        echo "remote"
    fi
}

# Show usage information
show_usage() {
    echo ""
    echo "Specter Installation Script"
    echo ""
    echo "Usage:"
    echo "  Remote install:  curl -fsSL https://raw.githubusercontent.com/mmcclatchy/specter/main/scripts/install-specter.sh | bash"
    echo "  With platform:   curl -fsSL https://raw.githubusercontent.com/mmcclatchy/specter/main/scripts/install-specter.sh | bash -s -- linear"
    echo "  With options:    curl -fsSL https://raw.githubusercontent.com/mmcclatchy/specter/main/scripts/install-specter.sh | bash -s -- --platform github --path ~/project"
    echo ""
    echo "  Local install:   ./scripts/install-specter.sh"
    echo "  With platform:   ./scripts/install-specter.sh linear"
    echo "  With options:    ./scripts/install-specter.sh --platform linear --path ~/project"
    echo ""
    echo "Arguments:"
    echo "  --platform       Platform choice: linear, github, or markdown (default: markdown)"
    echo "  --path           Target directory (default: current directory)"
    echo "  First arg        If no flags, treated as platform name"
    echo ""
    echo "Examples:"
    echo "  bash -s -- linear                    # Install to current dir with Linear"
    echo "  bash -s -- --platform github         # Install to current dir with GitHub"
    echo "  bash -s -- --path ~/app --platform linear  # Install to specific path"
    echo ""
}

# Parse arguments (supports both positional and flag-based)
parse_arguments() {
    TARGET_DIR="$(pwd)"
    PLATFORM="markdown"

    # If first argument doesn't start with --, treat it as platform
    if [ $# -eq 1 ] && [[ ! "$1" =~ ^-- ]]; then
        PLATFORM="$1"
        return
    fi

    # Parse flag-based arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --platform)
                PLATFORM="$2"
                shift 2
                ;;
            --path)
                TARGET_DIR="$2"
                shift 2
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown argument: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Parse arguments
parse_arguments "$@"

# Detect execution mode
EXECUTION_MODE=$(detect_execution_mode)

# Validate platform
if [[ ! "$PLATFORM" =~ ^(linear|github|markdown)$ ]]; then
    print_error "Invalid platform: $PLATFORM"
    echo "Platform must be one of: linear, github, markdown"
    exit 1
fi

# Convert to absolute path
TARGET_DIR=$(cd "$TARGET_DIR" && pwd)

print_info "Specter Installation"
print_info "Execution mode: $EXECUTION_MODE"
print_info "Target directory: $TARGET_DIR"
print_info "Platform: $PLATFORM"
echo ""

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    print_error "Target directory does not exist: $TARGET_DIR"
    exit 1
fi

# Create directory structure
print_info "Creating directory structure..."
mkdir -p "$TARGET_DIR/.claude/commands"
mkdir -p "$TARGET_DIR/.claude/agents"
mkdir -p "$TARGET_DIR/.specter/config"
print_success "Directory structure created"

# Install setup command (method depends on execution mode)
print_info "Installing setup command..."

if [ "$EXECUTION_MODE" = "local" ]; then
    # Local execution: copy from repository
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    SPECTER_ROOT="$(dirname "$SCRIPT_DIR")"

    if [ ! -f "$SPECTER_ROOT/$SETUP_COMMAND_PATH" ]; then
        print_error "Could not find setup command at: $SPECTER_ROOT/$SETUP_COMMAND_PATH"
        print_error "This script must be run from the Specter repository"
        exit 1
    fi

    cp "$SPECTER_ROOT/$SETUP_COMMAND_PATH" "$TARGET_DIR/.claude/commands/"
    print_success "Setup command installed (local copy)"
else
    # Remote execution: fetch from GitHub
    SETUP_COMMAND_URL="$GITHUB_RAW_URL/$SETUP_COMMAND_PATH"

    if command -v curl &> /dev/null; then
        curl -fsSL "$SETUP_COMMAND_URL" -o "$TARGET_DIR/.claude/commands/specter-setup.md"
    elif command -v wget &> /dev/null; then
        wget -qO "$TARGET_DIR/.claude/commands/specter-setup.md" "$SETUP_COMMAND_URL"
    else
        print_error "Neither curl nor wget is available"
        print_error "Please install curl or wget to use remote installation"
        exit 1
    fi

    if [ ! -f "$TARGET_DIR/.claude/commands/specter-setup.md" ]; then
        print_error "Failed to download setup command from GitHub"
        print_error "URL: $SETUP_COMMAND_URL"
        exit 1
    fi

    print_success "Setup command installed (downloaded from GitHub)"
fi

# Create initial platform config
print_info "Creating platform configuration..."
cat > "$TARGET_DIR/.specter/config/platform.json" <<EOF
{
  "platform": "$PLATFORM",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")",
  "version": "1.0",
  "bootstrap": true
}
EOF
print_success "Platform configuration created"

# Success message
echo ""
print_success "Specter bootstrap complete!"
echo ""
echo "Next steps:"
echo "  1. Open target project in Claude Code: cd $TARGET_DIR"
echo "  2. Run setup command: /specter-setup $PLATFORM"
echo ""
echo "This will generate all workflow templates for the $PLATFORM platform."
echo ""
echo "To check MCP server availability: /mcp list"
