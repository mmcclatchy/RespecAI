"""
Spec-setup command template generator.

This module generates the /spec-setup command template for interactive
project configuration with MCP server validation.
"""


def generate_spec_setup_command_template() -> str:
    """Generate spec-setup command template with MCP server validation.

    Returns:
        str: Complete spec-setup command template with YAML frontmatter
    """
    return """---
allowed-tools:
  - setup_project_workflow
  - detect_installation_status
  - configure_project_spec_manager
  - render_command_dynamic
  - render_agent_dynamic
argument-hint: [platform-choice]
description: Interactive project setup and configuration
---

# /spec-setup Command

Interactive project setup with MCP server validation and platform configuration.

## Your Task

Configure the spec-driven workflow system with MCP Server Validation and platform-specific authentication.

## MCP Server Validation

### Phase 1: Platform Status Detection

Check authentication status for each supported platform:

#### Linear Platform
- Verify `mcp__linear-server__*` tools availability
- Test API authentication with workspace access
- **Status Indicators**: ✅ Ready | ❌ Setup Required

#### GitHub Platform  
- Check `mcp__github__*` tools availability
- Test GitHub CLI authentication (`gh auth status`)
- **Status Indicators**: ✅ Ready | ❌ Setup Required

#### Markdown Platform
- Verify basic file system tools (Write, Read, Edit)
- No authentication required
- **Status Indicators**: ✅ Ready (Always Available)

### Phase 2: Interactive Platform Selection

Display platform options with real-time status:

```
🔧 Spec-Driven Workflow Setup
=====================================

Platform Options:
✅ Linear    (MCP Server: Installed & Authenticated)
❌ GitHub    (MCP Server: Not found - Install required)  
✅ Markdown  (MCP Server: Ready - No auth needed)

Select platform: [linear/github/markdown]
```

### Phase 3: Missing Setup Guidance

For unavailable platforms, provide specific installation instructions:

**Linear Missing**: Direct to Linear MCP Server installation guide
**GitHub Missing**: Direct to GitHub MCP Server + GitHub CLI setup  
**Markdown**: Always available (no setup required)

### Phase 4: Authentication Check

#### Status Check

Once platform is selected, validate MCP server connectivity:

```
Checking Linear MCP Server...
✅ MCP Server: Installed
✅ Authentication: Valid  
✅ Workspace Access: Confirmed
✅ API Permissions: Read/Write

Proceeding with Linear platform setup...
```

## Project Configuration

After successful MCP server validation:

1. **Generate Commands**: Create all 7 platform-specific commands
   - `/plan` (static, already exists)
   - `/spec` (platform-specific tools)
   - `/build` (platform-specific implementation)
   - `/refine-spec` (specification refinement)
   - `/refine-build` (implementation refinement)
   - `/validate` (quality validation)
   - `/spec-manager` (platform utilities)

2. **Create Agents**: Generate all 7 platform-specific agents
   - `spec-architect` (technical design)
   - `build-planner` (implementation planning)
   - `build-coder` (code execution)
   - `build-verifier` (quality validation)
   - `plan-analyst` (business requirements)
   - `plan-conversation-analyst` (natural language planning)
   - `plan-conversation-critic` (conversation assessment)

3. **Configure Quality**: Set FSDD compliance thresholds (0.85 minimum)

4. **Validate Setup**: Test end-to-end tool resolution

## Success Criteria

- ✅ MCP Server validated and authenticated
- ✅ Platform configured and operational
- ✅ Commands generated with correct tools
- ✅ Agents created with platform integration
- ✅ Quality gates configured
- ✅ End-to-end workflow tested

## Error Handling

### MCP Server Not Found
- Display specific installation instructions
- Provide official MCP server installation URLs
- Guide user through authentication process

### Authentication Failed
- Check API credentials and permissions
- Verify workspace/repository access
- Provide troubleshooting steps

### Platform Unavailable
- Suggest alternative platforms
- Show availability status for all options
- Guide user to working configuration

## Next Steps

After successful setup:

1. **Create Strategic Plan**: `/plan [project-name]`
2. **Generate Technical Spec**: `/spec [project-name] [issue-name]`
3. **Build Implementation**: `/build [spec-id]`
4. **Quality Validation**: All steps include FSDD validation

---

*Generated spec-setup command with MCP server validation*
*Supports Linear, GitHub, and Markdown platforms*
*Interactive mode with real-time authentication checking*"""
