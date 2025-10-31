# Multi-Project Architecture Design

**Status**: 🚧 In Development
**Target Release**: Version 1.1
**Last Updated**: 2025-10-31

## Overview

This document outlines the architecture for supporting multiple projects with a single Specter MCP Server instance. It defines how projects maintain isolation while sharing a common server process.

## Executive Summary

**Goal**: Enable one Specter MCP Server to serve multiple projects simultaneously with complete isolation of configurations, state, and workflows.

**Approach**: Single global MCP server with explicit project context passing and file-based persistence in per-project directories.

**Key Principles**:
- **Explicit over implicit**: Project context passed explicitly to all tools
- **Local over global**: Configuration and state stored in project directories
- **Isolation by design**: No shared state between projects
- **Git-friendly**: All project data can be version controlled

---

## Architecture Decisions

### Decision 1: Single Global MCP Server

**Choice**: One Specter MCP server instance serves all projects

**Rationale**:
- **Resource efficient**: Single Python process vs N processes for N projects
- **Simpler configuration**: One MCP server entry in `~/.claude/config.json`
- **Easier maintenance**: Updates apply to all projects simultaneously
- **Sufficient isolation**: Project context passed explicitly provides adequate separation

**Trade-offs**:
- Must pass project path explicitly to all tools (more verbose)
- Shared process means shared memory (requires careful state scoping)
- Cannot use `Path.cwd()` for auto-detection

**Alternative Considered**: Per-project MCP server instances
- **Rejected because**: Resource overhead, complex configuration management, unnecessary for isolation needs

### Decision 2: Explicit Project Context

**Choice**: Commands detect working directory and pass `project_path` parameter to all MCP tools

**Implementation**:
```markdown
## Command Template Pattern
1. Detect project context: PROJECT_PATH=$(pwd)
2. Pass to all tools: mcp__specter__create_plan:
                       project_path: $PROJECT_PATH
                       plan_markdown: $CONTENT
```

**Rationale**:
- **Reliability**: No ambiguity about which project is active
- **Debuggability**: Project path visible in all tool calls
- **Compatibility**: Works with single global MCP server architecture
- **No side effects**: No environment variable dependencies

**Trade-offs**:
- Every tool signature requires project_path parameter
- Command templates must include project path detection
- More verbose than auto-detection

**Alternative Considered**: Environment variables
- **Rejected because**: Side-effect-based, harder to debug, fragile across tool boundaries

### Decision 3: Per-Project Local Configuration

**Choice**: Store configuration in `<project>/.specter/config/` instead of `~/.specter/projects/`

**Structure**:
```text
project/
└── .specter/
    └── config/
        └── platform.json
```

**Rationale**:
- **Git-trackable**: Configuration travels with project
- **Self-contained**: Project directories include all needed config
- **No global coupling**: Deleting project directory removes all traces
- **Platform flexibility**: Each project can use different platform (Linear/GitHub/Markdown)

**Trade-offs**:
- Config not centrally accessible
- Each project must be set up individually

**Alternative Considered**: Global configuration at `~/.specter/projects/`
- **Rejected because**: Creates global state, not git-trackable, harder to manage multiple projects

### Decision 4: File-Based State Persistence

**Choice**: Persist workflow state to `<project>/.specter/state/` files

**Structure**:
```text
project/
└── .specter/
    └── state/
        ├── plans/
        │   └── {project_name}.json
        ├── specs/
        │   └── {spec_name}.json
        └── loops/
            └── {loop_id}.json
```

**Rationale**:
- **Survives restarts**: State persists across MCP server restarts
- **Git-trackable**: Workflow state can be version controlled if desired
- **Natural isolation**: Each project has its own state directory
- **Debuggable**: State files can be inspected directly

**Trade-offs**:
- File I/O overhead vs in-memory performance
- Need state cleanup mechanisms
- Potential for stale state files

**Alternative Considered**: In-memory only (current implementation)
- **Rejected because**: State lost on restart, no historical tracking, memory growth over time

---

## Project Isolation Strategy

### Configuration Isolation

**Loading Pattern**:
```python
def load_project_config(project_path: str) -> ProjectConfig:
    config_file = Path(project_path) / '.specter' / 'config' / 'platform.json'
    if not config_file.exists():
        raise ProjectNotSetupError(f"No Specter config found at {project_path}")
    return ProjectConfig.model_validate_json(config_file.read_text())
```

**Guarantees**:
- ✅ Each project loads its own platform configuration
- ✅ Projects can use different platforms simultaneously
- ✅ Config changes in Project A don't affect Project B
- ✅ No global configuration directory dependencies

### State Isolation

**Storage Pattern**:
```python
def save_project_plan(project_path: str, plan: ProjectPlan) -> None:
    state_dir = Path(project_path) / '.specter' / 'state' / 'plans'
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / f'{plan.project_name}.json'
    state_file.write_text(plan.model_dump_json(indent=2))

def load_project_plan(project_path: str, project_name: str) -> ProjectPlan:
    state_file = Path(project_path) / '.specter' / 'state' / 'plans' / f'{project_name}.json'
    return ProjectPlan.model_validate_json(state_file.read_text())
```

**Guarantees**:
- ✅ State stored in project-local directories
- ✅ No shared in-memory state between projects
- ✅ State persists across MCP server restarts
- ✅ Deleting project removes all state

### Workflow Isolation

**Platform-Specific Isolation**:

**Linear Platform**:
- Issues created in user's Linear workspace
- Naturally isolated by Linear workspace boundaries
- Each project's issues tagged with project name
- No cross-project contamination possible

**GitHub Platform**:
- Issues created in specific repository
- Naturally isolated by repository boundaries
- Each project maps to one GitHub repo
- No cross-project contamination possible

**Markdown Platform**:
- Files stored in `.specter/projects/<project-name>/specter-specs/`
- Project name in path ensures isolation
- Each project writes to its own subdirectory
- Risk: Must ensure project names are unique and validated

---

## Code Changes Required

### Phase 1: Tool Signature Updates

**Files to Update**: All files in `services/mcp/tools/` (~8 modules, ~32 tools)

**Example Change**:
```python
# BEFORE
async def create_project_plan(
    project_plan_markdown: str,
    ctx: Context
) -> MCPResponse:
    # Load from global state
    orchestrator = PlatformOrchestrator.create_with_default_config()
    ...

# AFTER
async def create_project_plan(
    project_path: str,  # NEW: Explicit project context
    project_plan_markdown: str,
    ctx: Context
) -> MCPResponse:
    # Load from project-local config
    orchestrator = PlatformOrchestrator.create_for_project(project_path)
    ...
```

**Affected Tool Modules**:
- `project_plan_tools.py` - All plan operations
- `spec_tools.py` - All spec operations
- `build_tools.py` - All build operations
- `loop_tools.py` - All refinement loop operations
- `feedback_tools.py` - All feedback operations
- `specter_setup_tools.py` - Already has project_path ✅
- Platform-specific tools - Verify they receive project context

### Phase 2: Command Template Updates

**Files to Update**: All files in `services/templates/commands/` (~5 commands)

**Pattern to Add**:
```python
# Add to template generation
def generate_plan_command(platform: PlatformType) -> str:
    template = f"""
# Specter Plan Command

## Initialize Context
- Detect project directory: PROJECT_PATH=$(pwd)
- Validate project setup: Check .specter/config/platform.json exists

## Step 1: Create Strategic Plan
Use MCP tool to create plan:

mcp__specter__create_project_plan:
  project_path: $PROJECT_PATH  # Pass explicit context
  project_plan_markdown: $PLAN_CONTENT
"""
    return template
```

**Affected Commands**:
- `plan_command.py`
- `plan_roadmap_command.py`
- `spec_command.py`
- `build_command.py`
- `plan_conversation_command.py`

### Phase 3: Configuration Management Updates

**File**: `services/platform/config_manager.py`

**Changes Required**:
```python
class ConfigManager:
    def __init__(self, project_path: str) -> None:
        # NEW: Use project-local config directory
        self.config_dir = Path(project_path) / '.specter' / 'config'
        self.config_file = self.config_dir / 'platform.json'

    def load_config(self) -> ProjectConfig:
        # Load from project directory, not global
        if not self.config_file.exists():
            raise ProjectNotSetupError(
                f"Project not set up. Run /specter-setup in {self.config_dir.parent.parent}"
            )
        return ProjectConfig.model_validate_json(self.config_file.read_text())

    def save_config(self, config: ProjectConfig) -> None:
        # Save to project directory
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(config.model_dump_json(indent=2))
```

**File**: `services/platform/platform_orchestrator.py`

**Changes Required**:
```python
class PlatformOrchestrator:
    # REMOVE this method
    @classmethod
    def create_with_default_config(cls) -> 'PlatformOrchestrator':
        # This creates global config - no longer supported
        pass

    # ADD this method
    @classmethod
    def create_for_project(cls, project_path: str) -> 'PlatformOrchestrator':
        """Create orchestrator for specific project.

        Args:
            project_path: Absolute path to project directory

        Returns:
            PlatformOrchestrator configured for the project

        Raises:
            ProjectNotSetupError: If project not set up with /specter-setup
        """
        config_manager = ConfigManager(project_path)
        config = config_manager.load_config()
        return cls(config, project_path)
```

### Phase 4: State Management Updates

**New File**: `services/state/file_state_manager.py`

**Implementation**:
```python
from pathlib import Path
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class FileStateManager(Generic[T]):
    """Manages file-based state persistence for project workflows."""

    def __init__(self, project_path: str, state_type: str):
        """Initialize state manager.

        Args:
            project_path: Absolute path to project directory
            state_type: State category (plans, specs, loops)
        """
        self.state_dir = Path(project_path) / '.specter' / 'state' / state_type
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, data: T) -> None:
        """Save state to file."""
        state_file = self.state_dir / f'{name}.json'
        state_file.write_text(data.model_dump_json(indent=2))

    def load(self, name: str, model: type[T]) -> T | None:
        """Load state from file."""
        state_file = self.state_dir / f'{name}.json'
        if not state_file.exists():
            return None
        return model.model_validate_json(state_file.read_text())

    def list(self) -> list[str]:
        """List all state files."""
        return [f.stem for f in self.state_dir.glob('*.json')]

    def delete(self, name: str) -> bool:
        """Delete state file."""
        state_file = self.state_dir / f'{name}.json'
        if state_file.exists():
            state_file.unlink()
            return True
        return False
```

**Update Existing Tools**:
```python
# In project_plan_tools.py
class ProjectPlanTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state
        # REMOVE: self._project_plans: dict[str, ProjectPlan] = {}
        # State now persisted to files, not in-memory

    def store_project_plan(
        self,
        project_path: str,  # NEW parameter
        project_plan: ProjectPlan
    ) -> MCPResponse:
        # Save to project-local state
        state_manager = FileStateManager[ProjectPlan](project_path, 'plans')
        state_manager.save(project_plan.project_name, project_plan)
        return MCPResponse(success=True, message="Plan stored successfully")

    def get_project_plan_data(
        self,
        project_path: str,  # NEW parameter
        project_name: str
    ) -> ProjectPlan | None:
        # Load from project-local state
        state_manager = FileStateManager[ProjectPlan](project_path, 'plans')
        return state_manager.load(project_name, ProjectPlan)
```

---

## Installation & Setup Flow

### One-Time: MCP Server Installation

**User performs once, globally**:

```bash
# 1. Clone Specter repository
cd ~/coding/projects
git clone git@github.com:mmcclatchy/specter.git
cd specter

# 2. Install dependencies
uv sync

# 3. Configure MCP server in Claude Code
# Edit ~/.claude/config.json:
{
  "mcpServers": {
    "specter": {
      "command": "uv",
      "args": ["run", "spec-driven-workflow-server"],
      "cwd": "/absolute/path/to/specter"
    }
  }
}

# 4. Verify
claude
/mcp list  # Should show "specter" with 32 tools
```

### Per-Project: Project Setup

**User performs for each project**:

```bash
# 1. Navigate to project
cd /path/to/my-project

# 2. Run installer (optional - just creates setup command)
~/coding/projects/specter/scripts/install-specter.sh

# 3. Setup project with Claude Code
claude

# In Claude Code:
/specter-setup markdown  # or linear, github

# This creates:
# - .claude/commands/specter-*.md
# - .claude/agents/*.md
# - .specter/config/platform.json
# - .specter/state/ (created on first workflow)
```

### Workflow Usage

**User works on any project**:

```bash
# Switch to Project A
cd /path/to/project-a
claude

# Commands automatically use Project A's config
/specter-plan my-feature
# Creates plan in .specter/state/plans/my-feature.json

# Switch to Project B
cd /path/to/project-b
claude

# Commands automatically use Project B's config
/specter-plan another-feature
# Creates plan in .specter/state/plans/another-feature.json
# No interference with Project A
```

---

## Testing Strategy

### Unit Tests

**Test File**: `tests/unit/test_multi_project_isolation.py`

**Test Cases**:
```python
def test_config_loads_from_project_directory():
    """Config manager loads from project-local .specter/config/"""

def test_state_saves_to_project_directory():
    """State manager saves to project-local .specter/state/"""

def test_projects_use_different_platforms():
    """Project A can use Linear while Project B uses Markdown"""

def test_project_path_required_in_tools():
    """All MCP tools require project_path parameter"""
```

### Integration Tests

**Test File**: `tests/integration/test_multi_project_workflows.py`

**Test Scenarios**:
```python
@pytest.fixture
def setup_two_projects(tmp_path):
    """Create two test projects with different platforms"""
    project_a = tmp_path / 'project-a'
    project_b = tmp_path / 'project-b'
    # Setup both projects
    return project_a, project_b

def test_concurrent_plan_creation(setup_two_projects):
    """Create plans in both projects simultaneously"""
    project_a, project_b = setup_two_projects

    # Create plan in project A
    plan_a = create_project_plan(str(project_a), "Plan A content")

    # Create plan in project B
    plan_b = create_project_plan(str(project_b), "Plan B content")

    # Verify isolation
    assert get_project_plan(str(project_a), "Plan A") is not None
    assert get_project_plan(str(project_b), "Plan B") is not None
    assert get_project_plan(str(project_a), "Plan B") is None  # Not cross-contaminated

def test_different_platforms_simultaneously(setup_two_projects):
    """Project A uses Linear, Project B uses Markdown"""

def test_state_persists_across_restarts(setup_two_projects):
    """State files persist when MCP server restarts"""
```

### End-to-End Tests

**Test File**: `tests/e2e/test_multi_project_production.py`

**Test Workflows**:
```python
def test_full_workflow_project_a():
    """Complete workflow: plan → roadmap → spec → build in Project A"""

def test_full_workflow_project_b():
    """Complete workflow in Project B with different platform"""

def test_switch_between_projects():
    """Start workflow in A, switch to B, return to A"""
```

---

## Migration Path

### For Existing Single-Project Users

**Current Setup** (before multi-project):
- Config at `~/.specter/projects/<sanitized-path>/platform.json`
- In-memory state only
- Works with single project

**Migration Steps**:

1. **Backup existing config** (optional):
   ```bash
   cp -r ~/.specter ~/specter-backup
   ```

2. **Run /specter-setup again**:
   ```bash
   cd /path/to/existing-project
   claude
   /specter-setup <your-platform>
   ```
   This creates `.specter/config/platform.json` in project directory

3. **State will be empty** (expected):
   - Old in-memory state is lost (was temporary anyway)
   - New workflows will use file-based persistence
   - Previous plans/specs on Linear/GitHub/Markdown still accessible via platform

4. **Delete old global config** (optional cleanup):
   ```bash
   rm -rf ~/.specter
   ```

### For New Users

No migration needed - follow standard installation flow in USER_GUIDE.md

---

## Known Limitations & Future Improvements

### Current Limitations

1. **State not migrated**: Existing in-memory state lost on migration (by design - was temporary)
2. **No state cleanup**: Old state files not automatically removed
3. **Project name conflicts**: Two projects with same name could conflict if not careful
4. **No cross-project workflows**: Can't reference specs from Project A in Project B

### Future Enhancements

**Version 1.2: State Management**
- Automatic state cleanup for completed workflows
- State archival for historical tracking
- State compression for large projects

**Version 1.3: Cross-Project Features**
- Reference specs from other projects
- Shared template libraries across projects
- Multi-project roadmaps

**Version 1.4: Advanced Isolation**
- Project name validation and uniqueness checks
- Config version tracking and auto-migration
- State backup and restore utilities

---

## Security Considerations

### Path Validation

**Risk**: Malicious project_path could access files outside project

**Mitigation**:
```python
def validate_project_path(project_path: str) -> None:
    """Validate project path is safe."""
    path = Path(project_path).resolve()

    # Must be absolute
    if not path.is_absolute():
        raise ValueError("Project path must be absolute")

    # Must exist
    if not path.exists():
        raise ValueError("Project path must exist")

    # Must be a directory
    if not path.is_dir():
        raise ValueError("Project path must be a directory")

    # Must not be system directories
    system_dirs = ['/etc', '/sys', '/proc', '/dev', '/var']
    if any(str(path).startswith(d) for d in system_dirs):
        raise ValueError("Cannot use system directories as project path")
```

### File System Isolation

**Risk**: Path traversal in project names

**Mitigation**:
```python
def sanitize_project_name(name: str) -> str:
    """Sanitize project name for file system safety."""
    # Remove path separators
    safe_name = name.replace('/', '_').replace('\\', '_')
    # Remove dangerous characters
    safe_name = re.sub(r'[^\w\-_]', '_', safe_name)
    # Limit length
    return safe_name[:100]
```

### Configuration Validation

**Risk**: Malicious platform.json could execute code

**Mitigation**:
- Use Pydantic models for strict validation
- No eval() or exec() on config contents
- Only allow known platform types: linear, github, markdown

---

## Performance Considerations

### File I/O Overhead

**Impact**: Reading/writing state files on every operation

**Optimization Strategies**:
1. **Caching**: Cache loaded state in memory for duration of command execution
2. **Lazy loading**: Only load state files when actually needed
3. **Batch operations**: Write state once at end of multi-step workflows
4. **Async I/O**: Use `aiofiles` for non-blocking file operations

### Memory Management

**Impact**: Single server process shared across projects

**Monitoring**:
- Track memory usage per project context
- Log memory pressure warnings
- Implement state eviction if needed

**Best Practices**:
- Don't load all project state at startup
- Clean up state objects after command completion
- Use generators for large list operations

---

## Appendix: Architecture Diagrams

### Single MCP Server with Multiple Projects

```text
┌─────────────────────────────────────────┐
│      Claude Code (User Interface)       │
│                                         │
│  Working Dir: /path/to/project-a        │
│  Commands: /specter-plan, /specter-spec │
└────────────────┬────────────────────────┘
                 │
                 │ MCP Protocol
                 │
┌────────────────▼────────────────────────┐
│      Specter MCP Server (Single)        │
│      Location: ~/coding/projects/       │
│                specter/                 │
│                                         │
│  Receives: project_path parameter       │
│  Routes to: Project-specific handler    │
└────────────────┬────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
┌────────▼─────┐  ┌─────▼────────┐
│  Project A   │  │  Project B   │
│              │  │              │
│  .specter/   │  │  .specter/   │
│  ├─config/   │  │  ├─config/   │
│  └─state/    │  │  └─state/    │
└──────────────┘  └──────────────┘
```

### State Isolation Flow

```text
User in Project A           Specter MCP Server              Project A Filesystem
─────────────────           ──────────────────              ────────────────────

/specter-plan ──────────────> create_project_plan()
                              project_path="/path/a"
                              │
                              ├─ Load config from
                              │  /path/a/.specter/config/  ◄─── platform.json
                              │
                              ├─ Create plan
                              │
                              └─ Save state to
                                 /path/a/.specter/state/   ───► plan.json


User in Project B           Specter MCP Server              Project B Filesystem
─────────────────           ──────────────────              ────────────────────

/specter-plan ──────────────> create_project_plan()
                              project_path="/path/b"
                              │
                              ├─ Load config from
                              │  /path/b/.specter/config/  ◄─── platform.json
                              │
                              ├─ Create plan (isolated)
                              │
                              └─ Save state to
                                 /path/b/.specter/state/   ───► plan.json
```

---

## Summary

This multi-project architecture provides:

✅ **Single global MCP server** - Efficient resource usage
✅ **Explicit project context** - Clear, debuggable tool calls
✅ **Local configuration** - Git-trackable, self-contained projects
✅ **File-based persistence** - State survives restarts
✅ **Complete isolation** - No cross-project interference
✅ **Platform flexibility** - Each project can use different platform

**Implementation Status**: 🚧 In Development
**Target Completion**: Q4 2025
**Current USER_GUIDE.md Status**: Updated with clarifications and status notes

---

**Document Version**: 1.0
**Author**: Specter Development Team
**Review Status**: Ready for Implementation
