# Specter Setup Process Improvements

This document outlines all changes required to make Specter installation as easy and complete as possible, and to implement full multi-project support.

## Status: Phase 1 Complete, Phase 2+ In Progress

**Phase 1 (Documentation) - ✅ COMPLETE**:
- ✅ Created MULTI_PROJECT_DESIGN.md with comprehensive architecture
- ✅ Updated USER_GUIDE.md with MCP configuration and multi-project status
- ✅ Updated README.md with Python version fix and MCP setup instructions

**Phase 2+ (Code Implementation) - 🚧 IN PROGRESS**:
- See code changes section below for detailed implementation requirements

---

## Documentation Updates (Phase 1) - ✅ COMPLETE

### README.md - ✅ Done

- ✅ Fixed Python version inconsistency (3.12+ → 3.13+)
- ✅ Added comprehensive MCP Server Configuration section
- ✅ Added private repository warning for curl installation
- ✅ Added multi-project support status section
- ✅ Reorganized Quick Start into two clear parts (MCP setup + Project setup)

### USER_GUIDE.md - ✅ Done

- ✅ Added Multi-Project Support section with current capabilities and limitations
- ✅ Documented that full isolation is in development (v1.1)
- ✅ Added link to MULTI_PROJECT_DESIGN.md for architecture details
- ✅ Kept existing comprehensive installation instructions (they were already correct)

### MULTI_PROJECT_DESIGN.md - ✅ Created

- ✅ Comprehensive architecture documentation
- ✅ Design decisions and rationale
- ✅ Project isolation strategy
- ✅ Detailed code changes required
- ✅ Testing strategy
- ✅ Migration path for existing users

---

## Code Implementation Changes (Phase 2+) - 🚧 TODO

**For complete architecture details, see [MULTI_PROJECT_DESIGN.md](MULTI_PROJECT_DESIGN.md).**

This section provides a quick reference checklist for implementation tasks.

### Phase 2: Core MCP Tool Updates (~3 days)

**Objective**: Add explicit `project_path` parameter to all MCP tools

**Files to Update** (~8 modules, ~32 tools):
- [ ] `services/mcp/tools/project_plan_tools.py`
- [ ] `services/mcp/tools/spec_tools.py`
- [ ] `services/mcp/tools/build_tools.py`
- [ ] `services/mcp/tools/loop_tools.py`
- [ ] `services/mcp/tools/feedback_tools.py`
- [ ] All other tool modules

**Implementation Pattern**:
```python
# Before
async def create_project_plan(
    project_plan_markdown: str,
    ctx: Context
) -> MCPResponse:
    orchestrator = PlatformOrchestrator.create_with_default_config()
    ...

# After
async def create_project_plan(
    project_path: str,  # NEW: Explicit project context
    project_plan_markdown: str,
    ctx: Context
) -> MCPResponse:
    orchestrator = PlatformOrchestrator.create_for_project(project_path)
    ...
```

**Details**: See MULTI_PROJECT_DESIGN.md "Phase 1: Tool Signature Updates"

---

### Phase 3: Command Template Updates (~1 day)

**Objective**: Update command templates to detect and pass project_path

**Files to Update** (~5 commands):
- [ ] `services/templates/commands/plan_command.py`
- [ ] `services/templates/commands/plan_roadmap_command.py`
- [ ] `services/templates/commands/spec_command.py`
- [ ] `services/templates/commands/build_command.py`
- [ ] `services/templates/commands/plan_conversation_command.py`

**Implementation Pattern**:
```markdown
# Add to each command template
## Initialize Context
- Detect project directory: PROJECT_PATH=$(pwd)
- Validate project setup exists

## Call MCP Tools
mcp__specter__create_project_plan:
  project_path: $PROJECT_PATH  # Pass explicit context
  plan_markdown: $CONTENT
```

**Details**: See MULTI_PROJECT_DESIGN.md "Phase 2: Command Template Updates"

---

### Phase 4: Configuration Management Updates (~1 day)

**Objective**: Move config from global `~/.specter/projects/` to per-project `.specter/config/`

**Files to Update**:
- [ ] `services/platform/config_manager.py` - Load from project directory
- [ ] `services/platform/platform_orchestrator.py` - Remove global config method, add project-scoped method

**Key Changes**:

`config_manager.py`:
```python
# NEW: Use project-local config
def __init__(self, project_path: str) -> None:
    self.config_dir = Path(project_path) / '.specter' / 'config'
    self.config_file = self.config_dir / 'platform.json'
```

`platform_orchestrator.py`:
```python
# REMOVE
@classmethod
def create_with_default_config(cls) -> 'PlatformOrchestrator':
    ...

# ADD
@classmethod
def create_for_project(cls, project_path: str) -> 'PlatformOrchestrator':
    config_manager = ConfigManager(project_path)
    return cls(config_manager.load_config(), project_path)
```

**Details**: See MULTI_PROJECT_DESIGN.md "Phase 3: Configuration Management Updates"

---

### Phase 5: File-Based State Persistence (~2 days)

**Objective**: Implement persistent state storage in `.specter/state/`

**New File**:
- [ ] `services/state/file_state_manager.py` - Generic file-based state manager

**Files to Update**:
- [ ] `services/mcp/tools/project_plan_tools.py` - Replace in-memory storage with file-based
- [ ] `services/mcp/tools/spec_tools.py` - Replace in-memory storage with file-based
- [ ] `services/mcp/tools/loop_tools.py` - Replace in-memory storage with file-based
- [ ] All other tools with state management

**State Directory Structure**:
```text
project/.specter/state/
├── plans/
│   └── {project_name}.json
├── specs/
│   └── {spec_name}.json
└── loops/
    └── {loop_id}.json
```

**Implementation Pattern**:
```python
# New FileStateManager
class FileStateManager(Generic[T]):
    def __init__(self, project_path: str, state_type: str):
        self.state_dir = Path(project_path) / '.specter' / 'state' / state_type

    def save(self, name: str, data: T) -> None:
        state_file = self.state_dir / f'{name}.json'
        state_file.write_text(data.model_dump_json(indent=2))

    def load(self, name: str, model: type[T]) -> T | None:
        state_file = self.state_dir / f'{name}.json'
        if state_file.exists():
            return model.model_validate_json(state_file.read_text())
        return None
```

**Details**: See MULTI_PROJECT_DESIGN.md "Phase 4: State Management Updates"

---

### Phase 6: Testing (~2-3 days)

**Unit Tests**:
- [ ] Test project_path validation
- [ ] Test config loading from project directory
- [ ] Test state persistence to project directory
- [ ] Test state scoping by project_path

**Integration Tests**:
- [ ] Test two projects with different platforms
- [ ] Test concurrent usage of multiple projects
- [ ] Test state isolation between projects
- [ ] Test config isolation between projects

**E2E Tests**:
- [ ] Full workflow in Project A (plan → spec → build)
- [ ] Full workflow in Project B with different platform
- [ ] Verify no cross-contamination
- [ ] Test switching between projects mid-workflow

**Test Files to Create/Update**:
- [ ] `tests/unit/test_multi_project_isolation.py`
- [ ] `tests/integration/test_multi_project_workflows.py`
- [ ] `tests/e2e/test_multi_project_production.py`

**Details**: See MULTI_PROJECT_DESIGN.md "Testing Strategy"

---

### Phase 7: Final Documentation Updates (~1 day)

**After code implementation is complete**:

- [ ] Update USER_GUIDE.md - Remove "in development" status
- [ ] Add "Working with Multiple Projects" comprehensive section to USER_GUIDE.md
- [ ] Update README.md - Mark multi-project support as complete
- [ ] Update ARCHITECTURE.md - Document multi-project architecture
- [ ] Create migration guide for existing single-project users

---

## Implementation Timeline

**Estimated Total**: 10-12 days

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 2: Tool Updates | 3 days | None |
| Phase 3: Command Templates | 1 day | Phase 2 complete |
| Phase 4: Config Management | 1 day | Phase 2 complete |
| Phase 5: State Persistence | 2 days | Phase 4 complete |
| Phase 6: Testing | 2-3 days | Phases 2-5 complete |
| Phase 7: Documentation | 1 day | Phase 6 complete |

---

## Success Criteria

Multi-project support will be complete when:

- ✅ Two projects can use Specter simultaneously without interference
- ✅ Each project has isolated config in `.specter/config/`
- ✅ State persists in project-local `.specter/state/`
- ✅ Different projects can use different platforms
- ✅ All 516+ tests pass with multi-project scenarios
- ✅ Documentation fully describes setup and usage
- ✅ No global state conflicts between projects

---

## Additional Improvements (Lower Priority)

These can be done alongside or after multi-project implementation:

### install-specter.sh Improvements

**Medium Priority**:
- [ ] Remove duplicate platform configuration (let /specter-setup handle it entirely)
- [ ] Add uv availability check with helpful error message
- [ ] Add Python version validation (3.13+)

### New Files to Create

**Medium Priority**:
- [ ] `.claude/config.example.json` - Template for MCP configuration
- [ ] `docs/INSTALLATION_CHECKLIST.md` - Step-by-step verification checklist

### pyproject.toml Updates

**Low Priority**:
- [ ] Update project description (currently says "Add your description here")
- [ ] Add entry point documentation comment

### Documentation Cross-References

**Low Priority**:
- [ ] Add links between README.md, USER_GUIDE.md, ARCHITECTURE.md
- [ ] Ensure consistent terminology across all docs
- [ ] Add table of contents to longer documents

---

## Reference Documents

- **[MULTI_PROJECT_DESIGN.md](MULTI_PROJECT_DESIGN.md)** - Complete architecture and implementation details
- **[USER_GUIDE.md](USER_GUIDE.md)** - User-facing installation and usage documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and technical architecture
- **[README.md](../README.md)** - Project overview and quick start

---

## Next Steps

1. ✅ Review Phase 1 documentation changes (COMPLETE)
2. Begin Phase 2: Update MCP tool signatures
3. Create feature branch for multi-project implementation
4. Implement phases 2-5 systematically
5. Run comprehensive testing (Phase 6)
6. Update documentation (Phase 7)
7. Create PR for review
8. Release as v1.1

---

**Document Status**: Complete - Ready for Implementation
**Last Updated**: 2025-10-31
**Version**: 2.0 (reflects Phase 1 completion)
