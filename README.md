# Specter Workflow System

AI-powered specification-driven development workflow for Claude Code.

## What is Specter?

Specter is a **meta MCP server** that generates platform-specific workflow automation tools for AI-driven development. It creates custom Claude Code commands and agents tailored to your project management platform (Linear, GitHub, or local Markdown files).

### Key Features

- **Platform abstraction** - Work with Linear, GitHub, or Markdown seamlessly
- **Quality-driven workflows** - Automated refinement loops with critic agents
- **Strategic to implementation** - Plan → Roadmap → Spec → Build
- **Type-safe integration** - Platform-specific tools properly configured

## Quick Start

### 1. Installation

**Remote installation (recommended):**
```bash
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash -s -- linear
```

**Local installation:**
```bash
./scripts/install-specter.sh --platform linear --path ~/my-project
```

**Bootstrap via Claude Code:**
```text
Install the Specter bootstrap files for this project
```

### 2. Project Setup

```bash
cd /path/to/your/project
claude
```

```text
/specter-setup linear
```

### 3. Start Using

```text
/specter-plan          # Create strategic plan
/specter-roadmap       # Break down into phases
/specter-spec          # Design specifications
/specter-build         # Implement features
```

## Platform Options

| Platform | Best For | Integration | Real-time |
|----------|----------|-------------|-----------|
| **Linear** | Teams using Linear | Full API | ✅ |
| **GitHub** | Open source projects | Full API | ❌ |
| **Markdown** | Solo developers | Local files | ❌ |

## Documentation

### Getting Started
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage documentation
  - Installation methods
  - Platform selection guide
  - Command reference
  - Workflow examples
  - Best practices
  - Troubleshooting

### Architecture & Development
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and implementation
  - Platform orchestrator (11-file system)
  - Template engine and strategy pattern
  - MCP tools (32 tools across 8 modules)
  - Document models and parsing
  - Deployment architecture

- **[Architecture Analysis](docs/ARCHITECTURE_ANALYSIS.md)** - Technical deep dive
  - Implementation quality assessment
  - Component analysis
  - Design pattern evaluation
  - Type safety framework
  - Testing and validation
  - Extensibility guide

- **[Architectural Realignment](docs/ARCHITECTURAL_REALIGNMENT.md)** - Development history
  - Implementation sessions
  - Technical decisions
  - Refactoring achievements
  - Production readiness status

## Requirements

### For All Users
- **Claude Code CLI** installed and configured
- **Platform MCP Server** (Linear or GitHub) if using external platforms

### For Local Installation
- **uv** (Python version and package manager)
- **Python 3.12+**
- **Unix-like OS** (Linux, macOS, Windows Subsystem for Linux)

### For Containerized Deployments
- **Docker** (Linux)
- **Docker Desktop** (macOS, Windows, Windows Subsystem for Linux)

## Workflow Overview

```text
1. Strategic Planning
   /specter-plan
   → Conversational requirements gathering
   → Creates strategic plan with business objectives
   → Quality validation with plan-critic

2. Phase Breakdown
   /specter-roadmap
   → Breaks plan into implementation phases
   → Creates initial specs for each phase
   → Quality refinement with roadmap-critic

3. Technical Design
   /specter-spec [spec-name]
   → Detailed technical specifications
   → Architecture and implementation approach
   → Quality refinement with spec-critic

4. Implementation
   /specter-build [spec-name]
   → Implementation planning
   → Code generation
   → Quality review with build-critic and build-reviewer
```

## Available Commands

- **`/specter-setup [platform]`** - Setup project with platform-specific tools
- **`/specter-plan [project-name]`** - Create strategic project plans
- **`/specter-roadmap [project-name]`** - Generate multi-phase implementation roadmaps
- **`/specter-spec [spec-name]`** - Convert plans to detailed specifications
- **`/specter-build [spec-name]`** - Implement specifications with code

## Contributing

This is a production-ready system with enterprise-grade architecture. Contributions are welcome!

### Areas for Contribution
- Additional platform integrations (Jira, GitLab, Azure DevOps)
- Advanced analytics and reporting
- Cross-platform spec migration tools
- Documentation improvements
- Bug fixes and optimizations

## License

[Add License Information]

## Support

- **Issues**: [GitHub Issues](https://github.com/mmcclatchy/spec-driven-development/issues)
- **Documentation**: See [docs/](docs/) directory
- **User Guide**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)

## Project Status

🚧 **In Development** - Core platform system complete (516 tests passing), agent templates and end-to-end workflows still in progress

### Completed
- ✅ Platform orchestrator (11-file system)
- ✅ MCP tools (32 tools across 8 modules)
- ✅ Document models with markdown parsing
- ✅ Template generation system
- ✅ Installation and setup workflows
- ✅ Unit and integration tests

### In Progress
- 🚧 Agent template completion (some agents not yet implemented)
- 🚧 End-to-end workflow testing
- 🚧 Platform integration validation
- 🚧 User acceptance testing
