# Specter Workflow System

AI-powered specification-driven development workflow for Claude Code.

## Installation

Specter supports multiple installation methods depending on your setup.

### Remote Installation (Recommended)

Install directly from GitHub using curl:

```bash
# Install with default platform (markdown)
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash

# Install with specific platform
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash -s -- linear

# Install to specific directory with platform
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash -s -- --platform github --path ~/my-project
```

### Local Installation

If you have the Specter repository cloned:

```bash
# Install from current directory (default: markdown)
./scripts/install-specter.sh

# Install with specific platform
./scripts/install-specter.sh linear

# Install to specific directory
./scripts/install-specter.sh --platform linear --path ~/my-project
```

### Installation Options

- `--platform`: Choose platform type
  - `linear` - Linear issue tracking integration
  - `github` - GitHub issues integration
  - `markdown` - Local markdown files (default)
- `--path`: Target directory (default: current directory)

### Containerized Installation

> **Note**: Docker/container-based installation support is planned for future releases.

## After Installation

1. Open your project in Claude Code:
   ```bash
   cd /path/to/your/project
   claude
   ```

2. Complete setup by running the setup command:
   ```bash
   /specter-setup [platform]
   ```

3. Verify MCP server availability:
   ```bash
   /mcp list
   ```

## Available Commands

After setup, you'll have access to:

- `/specter-plan` - Create strategic project plans
- `/specter-spec` - Convert plans to detailed specifications
- `/specter-build` - Implement specifications with code
- `/specter-roadmap` - Generate multi-phase project roadmaps

## Platform Support

- **Linear**: Full integration with Linear's issue tracking, projects, and comments
- **GitHub**: GitHub Issues integration with labels and milestones
- **Markdown**: Local file-based workflow using structured markdown files

## Requirements

- Claude Code CLI
- Bash shell (for installation script)
- Git (optional, for version control)
- Platform-specific requirements:
  - Linear: Linear MCP server configured
  - GitHub: GitHub MCP server configured
  - Markdown: No additional requirements
