# MCP Server Refactoring & Model Integration Implementation Plan

## Overview

This document outlines the refactoring of the MCP server architecture to improve maintainability, leverage the completed model standardization improvements, and create a scalable tool organization pattern.

**Current Problem**: The `services/mcp/server.py` file contains 400+ lines with 20+ MCP tools in a single file, mixing server setup concerns with tool implementations.

**Solution**: Restructure into modular tool organization with proper separation of concerns while integrating the newly standardized model architecture.

## Current State Analysis

### Existing Architecture Issues

**server.py Problems:**
- 400+ lines violating single responsibility principle
- Mixed concerns: server setup + tool implementations
- Difficult to maintain and test individual tool categories
- All MCP tool decorators defined in one massive file
- Hard to scale as new tool categories are added

**Hybrid Architecture Issues:**
- Tool logic already separated into classes (`FeedbackTools`, `ProjectPlanTools`)
- Tool logic already separated into modules (`loop_tools`, `roadmap_tools`)
- But MCP decorators still centralized in `server.py`
- Creates confusion about where tools are actually defined

### Model Standardization Integration Opportunities

**Completed Model Work to Leverage:**
- All models now use hierarchical headers consistently
- Unnecessary metadata fields removed across all models
- Type safety improved with consistent `tuple[str, ...]` usage
- MCPModel base class provides shared parsing utilities
- Roadmap model now uses `list[InitialSpec]` instead of `list[str]`

**Integration Needed:**
- Update tools to work with standardized model structures
- Remove references to obsolete fields (creation_date, last_updated, etc.)
- Leverage new type safety improvements
- Ensure proper integration with MCPModel base class

## Proposed Architecture

### New Directory Structure

```text
services/mcp/
├── server.py                  # Server setup and tool registration only
└── tools/
    ├── __init__.py           # Tool registration utilities
    ├── loop_tools.py         # Loop management MCP tools
    ├── feedback_tools.py     # Feedback management MCP tools
    ├── project_plan_tools.py # Project plan MCP tools
    ├── roadmap_tools.py      # Roadmap management MCP tools
    └── spec_tools.py         # Future: Spec workflow tools
```

### Tool Module Pattern

Each tool module follows this simple pattern:

```python
# services/mcp/tools/example_tools.py
from fastmcp import FastMCP
from services.models.mcp_response import MCPResponse

def register_example_tools(mcp: FastMCP) -> None:
    """Register example MCP tools with the server."""

    @mcp.tool()
    async def example_tool(param: str) -> MCPResponse:
        """Tool description for MCP agent consumption."""
        # Tool implementation here
        result = process_tool_logic(param)
        return MCPResponse(status="success", data=result)
```

### Registration Pattern

**services/mcp/tools/\_\_init\_\_.py:**
```python
def register_all_tools(mcp: FastMCP) -> None:
    """Register all MCP tools with the server."""
    from .loop_tools import register_loop_tools
    from .feedback_tools import register_feedback_tools
    from .project_plan_tools import register_project_plan_tools
    from .roadmap_tools import register_roadmap_tools

    register_loop_tools(mcp)
    register_feedback_tools(mcp)
    register_project_plan_tools(mcp)
    register_roadmap_tools(mcp)
```

**Updated services/mcp/server.py:**
```python
from fastmcp import FastMCP

def create_mcp_server() -> FastMCP:
    mcp = FastMCP("Spec-Driven Development MCP Server")

    # Register all tools
    from .tools import register_all_tools
    register_all_tools(mcp)

    return mcp
```

## Implementation Phases

### Phase 1: Directory Structure & Registration Pattern

**Objectives:**
- Create new directory structure
- Implement tool registration pattern
- Create base infrastructure

**Tasks:**
1. Create `services/mcp/tools/` directory
2. Implement `tools/__init__.py` with registration utilities
3. Create tool module structure

**Success Criteria:**
- New directories exist with proper `__init__.py` files
- Registration pattern defined and testable
- Clean separation of concerns achieved

### Phase 2: Tool Module Migration

**Objectives:**
- Move each tool category to dedicated module
- Integrate model standardization improvements
- Create clean modular architecture

**Tasks:**

#### 2.1 Loop Tools Migration
- Create `services/mcp/tools/loop_tools.py`
- Move 8 loop management tools from `server.py`
- Implement `register_loop_tools()` function
- Test all loop tools function identically

#### 2.2 Feedback Tools Migration
- Create `services/mcp/tools/feedback_tools.py`
- Move 2 feedback management tools from `server.py`
- Update to leverage MCPModel base class improvements
- Remove references to obsolete model fields
- Implement `register_feedback_tools()` function

#### 2.3 Project Plan Tools Migration
- Create `services/mcp/tools/project_plan_tools.py`
- Move 4 project plan tools from `server.py`
- Update to work with simplified ProjectPlan model (no version, creation_date, etc.)
- Implement `register_project_plan_tools()` function

#### 2.4 Roadmap Tools Migration
- Create `services/mcp/tools/roadmap_tools.py`
- Move 6 roadmap management tools from `server.py`
- **Critical Update**: Integrate with `list[InitialSpec]` instead of `list[str]`
- Update to work with cleaned-up Roadmap model
- Implement `register_roadmap_tools()` function

**Success Criteria:**
- Each tool category in dedicated module
- All tools maintain identical interfaces in new modules
- Model standardization improvements integrated
- All tools pass existing integration tests

### Phase 3: Server Simplification

**Objectives:**
- Simplify `server.py` to focus only on server setup
- Implement clean tool registration
- Remove all tool decorators from server.py

**Tasks:**
1. Update `server.py` to use registration pattern
2. Remove all MCP tool decorators from `server.py`
3. Clean up server.py to focus only on setup and registration
4. Test server startup and tool availability

**Refactoring Strategy:**
```python
# Current approach (server.py - 400+ lines)
@mcp.tool()
async def store_critic_feedback(loop_id: str, feedback_markdown: str) -> MCPResponse:
    feedback = CriticFeedback.parse_markdown(feedback_markdown)
    feedback_tools = FeedbackTools(state_manager)
    return feedback_tools.store_critic_feedback(feedback)

# New approach (tools/feedback_tools.py - focused module)
def register_feedback_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    async def store_critic_feedback(loop_id: str, feedback_markdown: str) -> MCPResponse:
        from services.tools.feedback_tools import FeedbackTools
        feedback = CriticFeedback.parse_markdown(feedback_markdown)
        feedback_tools = FeedbackTools(state_manager)
        return feedback_tools.store_critic_feedback(feedback)
```

### Phase 4: Model Integration & Type Safety

**Objectives:**
- Integrate model standardization improvements
- Improve type safety

**Tasks:**

#### 4.1 Model Integration Updates
- Update all tools to work with hierarchical header models
- Remove all references to obsolete fields:
  - `creation_date`, `last_updated`, `spec_owner` (InitialSpec)
  - `creation_date`, `last_updated`, `build_owner` (BuildPlan)
  - `creation_date`, `last_updated`, `feature_owner` (FeatureRequirements)
  - `version`, `creation_date`, `last_updated` (ProjectPlan)
- Update roadmap tools for `list[InitialSpec]` handling
- Leverage MCPModel base class parsing utilities

#### 4.2 Type Safety Improvements
- Update all tool signatures to use new model types
- Leverage consistent `tuple[str, ...]` usage for header paths
- Add type hints for all tool parameters and returns
- Ensure mypy compliance across all tool modules

### Phase 5: Testing & Documentation

**Objectives:**
- Comprehensive testing of new architecture
- Performance validation
- Documentation updates

**Tasks:**

#### 5.1 Tool Testing
- Create tests for each tool module (`tests/unit/mcp/tools/`)
- Test tool registration functionality
- Test integration with standardized models
- Validate error handling and edge cases

#### 5.2 Integration Testing
- Test server startup and tool registration
- Verify all tools function correctly with new architecture
- Test tool discovery and invocation by MCP clients
- Performance testing to ensure no regressions

#### 5.3 Documentation
- Update existing MCP tool documentation
- Document new tool organization pattern
- Create migration guide for future tool additions
- Update development setup instructions

## Model Integration Specifications

### Updated Tool Behaviors

#### Roadmap Tools Updates
**Critical Change**: Roadmap model now uses `list[InitialSpec]` instead of `list[str]`

```python
# Before (list[str])
def list_specs(project_id: str) -> list[str]:
    roadmap = state_manager.get_roadmap(project_id)
    return roadmap.specs  # Returns list of strings

# After (list[InitialSpec] with name extraction)
def list_specs(project_id: str) -> list[str]:
    roadmap = state_manager.get_roadmap(project_id)
    return [spec.phase_name for spec in roadmap.specs]  # Extract names from InitialSpec objects
```

#### Model Field Updates
Remove all references to obsolete fields across all tools:

**InitialSpec Tools:**
- Remove: `creation_date`, `last_updated`, `spec_owner`
- Keep: `id`, `phase_name`, `objectives`, `scope`, `dependencies`, `deliverables`, `spec_status`

**BuildPlan Tools:**
- Remove: `creation_date`, `last_updated`, `build_owner`
- Keep: All technical fields (no metadata fields)

**FeatureRequirements Tools:**
- Remove: `creation_date`, `last_updated`, `feature_owner`
- Keep: All functional requirement fields

**ProjectPlan Tools:**
- Remove: `version`, `creation_date`, `last_updated`
- Keep: All project planning fields

## Benefits Analysis

### Maintainability Improvements
- **Focused Files**: Each tool module handles single responsibility
- **Clear Organization**: Tools grouped by functional area
- **Easier Testing**: Individual tool modules can be tested in isolation
- **Simpler Debugging**: Issues isolated to specific tool categories

### Scalability Improvements
- **Easy Tool Addition**: New tool categories follow established pattern
- **Independent Development**: Teams can work on different tool modules
- **Modular Deployment**: Could support selective tool deployment in future
### Model Integration Benefits
- **Type Safety**: Leverages improved model type consistency
- **Simplified Parsing**: Uses MCPModel base class utilities
- **Cleaner Data**: No obsolete fields to handle or ignore
- **Better Performance**: Hierarchical parsing more efficient than regex

### Developer Experience
- **Clear Structure**: Easy to find and modify specific tools
- **Consistent Patterns**: All tool modules follow same registration pattern
- **Better IDE Support**: Smaller files with better auto-completion
- **Easier Code Review**: Changes isolated to relevant tool modules

## Risk Analysis & Mitigation

### Technical Risks

**Risk**: Tool registration failures during server startup
**Mitigation**:
- Comprehensive testing of registration pattern
- Graceful error handling in registration functions
- Validation that all tools register successfully

**Risk**: Breaking changes to MCP tool interfaces
**Mitigation**:
- Maintain identical tool signatures during migration
- Comprehensive integration testing with MCP clients
- Rollback plan to revert to single-file approach

**Risk**: Performance degradation from module loading
**Mitigation**:
- Benchmark server startup time before/after
- Use lazy loading if needed
- Monitor tool invocation performance

### Integration Risks

**Risk**: Model integration introduces bugs
**Mitigation**:
- Thorough testing with new model structures
- Validation of all field removals
- Test roadmap tools with `list[InitialSpec]` thoroughly

**Risk**: Missing obsolete field references
**Mitigation**:
- Systematic grep for removed field names
- Update all error messages and documentation
- Comprehensive test coverage

## Success Criteria

### Functional Requirements
- ✅ All existing MCP tools maintain identical interfaces
- ✅ Server startup time remains < 2 seconds
- ✅ All tool categories properly separated into modules
- ✅ Model standardization improvements fully integrated
- ✅ No references to obsolete model fields

### Quality Requirements
- ✅ Zero mypy errors across all tool modules
- ✅ Zero ruff check errors
- ✅ 100% test coverage for new tool modules
- ✅ All existing integration tests pass
- ✅ No performance regressions

### Architecture Requirements
- ✅ Clear separation of concerns between tool categories
- ✅ Scalable pattern for adding new tool types
- ✅ Consistent tool registration approach
- ✅ Proper integration with MCPModel base class
- ✅ Clean server.py focused only on setup

## Implementation Timeline

### Week 1: Foundation & Planning
- Days 1-2: Directory structure and registration pattern
- Days 3-4: Loop tools and feedback tools migration
- Day 5: Testing and validation

### Week 2: Core Tool Migration
- Days 1-2: Project plan tools and roadmap tools migration
- Days 3-4: Model integration updates and testing
- Day 5: Server simplification and integration testing

This refactoring will create a more maintainable, scalable, and properly integrated MCP server architecture while leveraging the model standardization improvements.
