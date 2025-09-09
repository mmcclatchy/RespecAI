def generate_spec_manager_command() -> str:
    return """---
argument-hint: [platform]
description: Configure spec management platform for this project (linear|markdown|github)
---

# Spec Manager Configuration Command

Set the spec management platform for the current project.

## Your Task

Configure spec management for platform: $ARGUMENTS

## Available Platforms

### linear
- **Tools**: Linear MCP Server integration
- **Requirements**: Linear workspace access, mcp__linear-server configured
- **Best For**: Team workflows, structured issue tracking

### markdown
- **Tools**: Claude Code native file operations (Write, Edit, Read)
- **Requirements**: None (uses local files)
- **Best For**: Solo development, documentation-focused workflows

### github
- **Tools**: GitHub CLI via Bash commands
- **Requirements**: `gh` CLI installed and authenticated
- **Best For**: Open source projects, GitHub-native workflows

## Implementation

Create or update `.claude/spec-config.json` in project root:

```json
{
  "spec_manager": "$ARGUMENTS",
  "configured_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "project_name": "$(basename $(pwd))"
}
```

## Validation

After configuration:
1. ✅ Config file created at `.claude/spec-config.json`
2. ✅ Platform set to: $ARGUMENTS
3. ✅ Ready for agent creation with: `render_agent_dynamic(agent_name='spec-architect', spec_manager_type='$ARGUMENTS')`

## Usage Examples

```bash
/spec-manager linear     # Use Linear for team workflows
/spec-manager markdown   # Use markdown files for solo dev
/spec-manager github     # Use GitHub Issues for open source
```

The selected platform will be used by default for all dynamic agent creation in this project.
"""
