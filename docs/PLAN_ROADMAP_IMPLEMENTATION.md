# Plan-Roadmap Workflow Implementation Guide

## Executive Summary

This document outlines the implementation strategy for the `/plan-roadmap` command workflow, addressing critical gaps identified in the current codebase and establishing an optimal architecture for roadmap generation with parallel spec creation.

### Current State Analysis

**✅ COMPLETED:**
- ✅ All agent template files created (`plan-roadmap`, `roadmap-critic`, `create-spec`)
- ✅ Agent behavioral instructions properly separated into agent files
- ✅ Spec scaffolding logic implemented in dedicated `create-spec` agent
- ✅ Quality threshold references properly isolated to MCP Server
- ✅ Three specialized agents following established patterns
- ✅ Command template structure created
- ✅ Parallel spec creation workflow designed in `create-spec` agent
- ✅ Header hierarchy standardized for better parseability

**❌ CRITICAL ARCHITECTURAL ISSUES BLOCKING FUNCTIONALITY:**

#### **Missing Dual Tool Architecture**
- **No Platform Abstraction**: Agent templates hardcode tool names instead of using platform-injected parameters
- **No State vs Persistence Separation**: Templates don't distinguish between MCP Specter state management and platform persistence
- **Missing PlatformService Integration**: No mechanism to inject platform-specific tools (Markdown: `Read`/`Write`, Linear: `mcp__linear__*`, GitHub: `mcp__github__*`)

#### **Required Dual Tool Pattern Missing**
```python
# CURRENT (BROKEN)
def generate_plan_roadmap_template() -> str:
    return """tools: ["Read", "Grep", "get_project_plan_markdown"]"""

# REQUIRED ARCHITECTURE
def generate_plan_roadmap_template(
    get_roadmap_state: str,      # mcp__specter__get_roadmap
    store_roadmap_state: str,    # mcp__specter__store_roadmap
    get_project_plan: str,       # Read | mcp__linear__get_issue | mcp__github__get_project
    store_roadmap_external: str, # Write | mcp__linear__create_issue | mcp__github__create_project
) -> str:
```

#### **Platform Decoupling Benefits Missing**
- **Markdown Platform**: Should use `Read`/`Write` for file operations
- **Linear Platform**: Should use `mcp__linear__*` tools for issue management
- **GitHub Platform**: Should use `mcp__github__*` tools for project management
- **MCP Specter**: Should use `mcp__specter__*` tools for internal state management

#### **Complete System Non-Functionality**
- Agent templates cannot adapt to different platforms
- No separation between internal state and external persistence
- PlatformService cannot inject appropriate tools
- Users cannot choose between Markdown/Linear/GitHub platforms

**REMAINING FOR FULL FUNCTIONALITY:**
- Fix tool name references in all command templates
- Integrate command templates with actual MCP tool names
- Test end-to-end workflow functionality
- Minor template refinements based on usage experience

## Agent Architecture

### 1. plan-roadmap Agent

**File:** `services/templates/agents/plan_roadmap.py` ✅ **COMPLETED**

**Responsibility:** Transform strategic plans into phased implementation roadmaps

**Specifications:**
- **Model:** Sonnet (for consistency and complex phase analysis)
- **Tools:** Read, Grep, Glob (read-only for plan analysis)
- **Pattern:** Follow `plan_analyst.py` structure with imperative instructions

**Input Format:**
```markdown
Strategic Plan: [Complete strategic plan from /plan command]
Structured Objectives: [Business objectives analysis from plan-analyst]
Phasing Preferences: [Optional user guidance like "2-week sprints"]

Create implementation roadmap with discrete phases.
Each phase should be implementable in 2-4 weeks.
```

**Output Format:**
```markdown
# Implementation Roadmap: [Project Name]

## Overview
[Phasing strategy and implementation approach]

## Phase Summary
- Total Phases: [3-7 phases]
- Estimated Duration: [total timeline]
- Critical Path: [key dependencies]

## Phase 1: [Foundation/Core Infrastructure]
**Duration:** 2-3 weeks
**Priority:** Critical
**Dependencies:** None

### Scope
[Clear description of included functionality]

### Deliverables
- [Specific, measurable deliverable]
- [Specific, measurable deliverable]

### Technical Focus
- [Key technical area for /spec command]
- [Key technical area for /spec command]

### Success Criteria
- [Measurable outcome]
- [Measurable outcome]

### Spec Context
**Focus Areas:** [Technical domains for /spec command]
**Key Decisions:** [Architecture choices needed]
**Research Needs:** [Technologies to investigate]
**Integration Points:** [External systems or APIs]

[Additional phases following same structure]

## Risk Mitigation
[Cross-phase risks and mitigation strategies]

## Integration Strategy
[How phases connect and build upon each other]
```

**Key Tasks:**
1. Parse strategic plan completely for implementable units
2. Break requirements into 3-7 implementation phases (2-4 weeks each)
3. Establish clear phase sequencing and dependencies
4. Define scope boundaries and technical focus areas per phase
5. Prepare spec-ready context for each phase

### 2. roadmap-critic Agent

**File:** `services/templates/agents/roadmap_critic.py` ✅ **COMPLETED**

**Responsibility:** Assess roadmap quality against FSDD criteria

**Specifications:**
- **Model:** Sonnet (for consistent scoring and nuanced evaluation)
- **Tools:** None (pure assessment agent)
- **Pattern:** Follow `analyst_critic.py` structure with CriticFeedback output

**Input Format:**
```markdown
Evaluate this implementation roadmap for quality and completeness.

Implementation Roadmap:
[Complete roadmap from plan-roadmap agent]

Focus on:
- Phase scoping and boundaries
- Dependency management
- Implementation readiness
- Balance and feasibility
```

**Output Format:**
```markdown
# Critic Feedback: ROADMAP-CRITIC

## Assessment Summary
- **Loop ID:** [loop_id from context]
- **Iteration:** [current iteration number]
- **Overall Score:** [calculated score 0-100]
- **Assessment Summary:** [Brief quality assessment]

## Analysis
[Detailed validation analysis including:]
- Phase scoping assessment (size, boundaries, value delivery)
- Dependency validation (sequencing, prerequisites, integration)
- Implementation readiness (spec context, technical focus, research needs)
- Balance evaluation (complexity distribution, timeline feasibility)

## Issues and Recommendations

### Key Issues
- [Specific roadmap problem 1 with context reference]
- [Phase sizing issue 2 with suggested resolution]
- [Dependency problem 3 with sequencing guidance]

### Recommendations
- [Specific improvement action 1 with implementation guidance]
- [Concrete enhancement 2 addressing identified gaps]
- [Refinement suggestion 3 for better implementation readiness]

## Metadata
- **Critic:** ROADMAP-CRITIC
- **Timestamp:** [current ISO timestamp]
- **Status:** completed
```

**Assessment Criteria (12-point FSDD framework):**
1. Phase Scoping - Appropriate size and boundaries
2. Dependency Management - Clear sequencing without circular dependencies
3. Scope Clarity - Specific deliverables and explicit boundaries
4. Implementation Readiness - Sufficient detail for /spec command
5. Resource Balance - Realistic complexity distribution
6. Risk Distribution - Appropriate mitigation strategies
7. Timeline Feasibility - Realistic duration estimates
8. Success Criteria - Clear, measurable outcomes
9. Specification Planning - Adequate preparation for /spec calls
10. Integration Strategy - How phases connect and build
11. Quality Assurance - Testing and validation approach
12. Performance Targets - Measurable performance criteria

**Scoring Guidelines:**
- **90-100:** Exceptional - Ready for immediate implementation
- **80-89:** Good - Minor improvements needed
- **70-79:** Acceptable - Functional but needs enhancement
- **60-69:** Poor - Major gaps requiring revision
- **0-59:** Inadequate - Fundamental issues needing rework

### 3. create-spec Agent

**File:** `services/templates/agents/create_spec.py` ✅ **COMPLETED**

**Responsibility:** Create individual InitialSpec objects from roadmap phases

**Specifications:**
- **Model:** Sonnet (for specification quality)
- **Tools:** MCP tools for roadmap retrieval and spec storage
- **Pattern:** New agent for parallel spec creation

**Input Format:**
```markdown
Create InitialSpec for project phase.

Project ID: [project_identifier]
Spec Name: [phase_name_from_roadmap]
Phase Context: [extracted phase information including scope, deliverables, technical focus]

Use roadmap context to create properly scaffolded InitialSpec.
```

**Output Format:**
```markdown
InitialSpec Created Successfully:
- **Project:** [project_id]
- **Phase:** [spec_name]
- **Status:** [creation_status]
- **Context:** [spec_preparation_details]
```

**Key Tasks:**
1. Retrieve roadmap via MCP Server using project_id
2. Extract phase-specific context for the specified spec_name
3. Create InitialSpec model with proper scaffolding using phase context
4. Store InitialSpec via MCP Server tools
5. Confirm successful creation and readiness for /spec command

**Parallel Execution Design:**
- Multiple create-spec agents run concurrently
- Each handles one phase from the roadmap
- Command coordinates execution and collects results
- Enables faster overall workflow completion

## Command Template Status ✅ **COMPLETED**

### Current Implementation in `plan_roadmap_command.py`

**✅ COMPLETED:**
- ✅ Agent behavioral instructions moved to agent files
- ✅ Orchestration-focused command structure
- ✅ Spec scaffolding logic delegated to `create-spec` agent
- ✅ Quality threshold references properly isolated to MCP Server
- ✅ Clear separation of coordination and implementation concerns
- ✅ Parallel spec creation coordination implemented

### Current Structure (283 lines - Functional and Complete)

**✅ Implemented Structure:**
- ✅ YAML frontmatter with allowed tools
- ✅ Workflow orchestration steps
- ✅ MCP tool integration patterns
- ✅ Platform-specific tool injection
- ✅ Comprehensive error handling for component failures
- ✅ Parallel spec creation coordination

**✅ Successfully Removed:**
- ✅ Agent behavioral instructions → Moved to agent files
- ✅ Quality threshold logic → MCP Server responsibility
- ✅ Spec scaffolding workflow → Delegated to create-spec agent

**Current Template Structure:**
```markdown
---
allowed-tools:
  - Task(plan-roadmap)
  - Task(roadmap-critic)
  - Task(create-spec)
  - {get_project_plan_tool}
  - {create_roadmap_tool}
  - {get_roadmap_tool}
  - mcp__loop_state__initialize_refinement_loop
  - mcp__loop_state__decide_loop_next_action
  - mcp__loop_state__get_loop_status
argument-hint: [project-name] [optional: phasing-preferences]
description: Transform strategic plans into phased implementation roadmaps
---

# /plan-roadmap Command: Implementation Roadmap Orchestration

## Workflow Steps

### 1. Strategic Plan Retrieval
[Orchestration for retrieving completed strategic plan]

### 2. Roadmap Generation Loop
[Coordination of plan-roadmap → roadmap-critic → MCP decision cycle]

### 3. MCP Decision Handling
[Response patterns for refine/complete/user_input actions]

### 4. Parallel Spec Creation
[Coordination of multiple create-spec agents]

### 5. Final Integration
[Result aggregation and completion reporting]

## Error Handling
[Graceful degradation patterns for component failures]
```

## Parallel Spec Creation Workflow

### Architecture Design

**Sequential Processing (Current):**
```text
Roadmap Generation → Complete → Create All Specs Sequentially
```

**Parallel Processing (New):**
```text
Roadmap Generation → Complete → [create-spec₁ || create-spec₂ || create-spec₃ ...]
```

### Implementation Pattern

**After Roadmap Completion:**
1. Extract phase list from completed roadmap
2. Launch create-spec agent for each phase in parallel
3. Coordinate execution and collect results
4. Report final status with roadmap + all specs created

**Coordination Logic:**
```text
For each phase in completed_roadmap:
  Task(
    agent="create-spec",
    prompt=f"""
    Project ID: {project_id}
    Spec Name: {phase.name}
    Phase Context: {phase.context}
    """
  )

Aggregate results and report completion status.
```

### Benefits

**Performance:** Faster overall workflow (N specs created concurrently)
**Scalability:** Handles roadmaps with many phases efficiently
**Reliability:** Isolated failures don't block other spec creation
**Maintainability:** Clear separation of roadmap vs spec creation concerns

## Testing Strategy

### Realistic Testing Approach

Based on our discussion about LLM testing limitations, we focus on deterministic components only.

### Testable Components

**1. Template Generation Functions**
```python
def test_plan_roadmap_template_generation():
    template = generate_plan_roadmap_template(
        get_project_plan_tool="mcp__linear__get_issue",
        create_roadmap_tool="mcp__linear__create_issue"
    )
    assert "mcp__linear__get_issue" in template
    assert "Task(plan-roadmap)" in template
    assert "Task(roadmap-critic)" in template
```

**2. MCP Tool Functions**
```python
def test_roadmap_creation():
    roadmap_markdown = load_test_roadmap()
    result = create_roadmap("test_project", roadmap_markdown)
    assert result.project_name == "test_project"
    assert len(result.specs) > 0
```

**3. Data Model Validation**
```python
def test_roadmap_model_parsing():
    roadmap = Roadmap.parse_markdown(valid_roadmap_markdown)
    assert roadmap.spec_count == len(roadmap.specs)
    assert roadmap.project_name is not None
```

**4. Static Template Analysis**
```python
def test_template_yaml_structure():
    template = generate_plan_roadmap_template()
    yaml_content = extract_yaml_frontmatter(template)
    assert "allowed-tools" in yaml_content
    assert "description" in yaml_content
```

### Non-Testable Components

**LLM Behavior:** Agent instruction following and response quality
**Response Consistency:** Output variation across identical inputs
**Quality Assessment:** Roadmap-critic scoring accuracy
**Refinement Effectiveness:** Improvement patterns across iterations

**Alternative Validation:**
- Manual testing with real workflows
- Iterative refinement based on observed behavior
- Clear specifications over automated verification
- User feedback and usage observation

### Test Structure

**Directory:** `tests/`
**Files:**
- `test_template_generation.py` - Template function validation
- `test_mcp_tools.py` - MCP tool function testing
- `test_data_models.py` - Pydantic model validation
- `test_static_analysis.py` - Template structure verification

## Key Architectural Principles

### 1. Threshold Isolation
**Principle:** Only MCP Server knows and uses quality thresholds

**Implementation:**
- Agents never reference specific scores or percentages
- Commands respond to actions (refine/complete/user_input) not scores
- MCP Server handles all decision logic based on configured thresholds
- Templates contain no hardcoded quality requirements

### 2. Action-Based Command Responses
**Principle:** Commands handle MCP actions, not evaluation logic

**Pattern:**
```markdown
MCP_DECISION = decide_loop_next_action(loop_id, quality_score)

IF MCP_DECISION == "refine":
  → Pass feedback to plan-roadmap for improvements
IF MCP_DECISION == "complete":
  → Proceed to parallel spec creation
IF MCP_DECISION == "user_input":
  → Request additional user guidance
```

### 3. Single Responsibility Agents
**Principle:** Each agent handles exactly one specialized function

**Boundaries:**
- **plan-roadmap:** Phase breakdown only
- **roadmap-critic:** Quality assessment only
- **create-spec:** Individual spec creation only
- **Command:** Orchestration coordination only

### 4. Platform Agnostic Design
**Principle:** Maintain tool injection for future platform support

**Implementation:**
- Templates accept abstract tool names as parameters
- Platform-specific tools injected at generation time
- Content remains platform-independent
- Support for Linear/GitHub/Markdown planned

### 5. Parallel Execution Capability
**Principle:** Enable concurrent processing where possible

**Design:**
- Spec creation runs in parallel after roadmap completion
- Multiple create-spec agents execute simultaneously
- Command coordinates parallel execution and result aggregation
- Improved performance for multi-phase roadmaps

### 6. Greenfield Optimization
**Principle:** Optimize for best architecture without legacy constraints

**Approach:**
- No backwards compatibility requirements
- Clean separation of concerns
- Modern patterns and practices
- Architecture optimized for maintainability and performance

## Implementation Checklist

### Phase 1: Create Agent Files ❌ **MISSING DUAL TOOL ARCHITECTURE**
- [x] `services/templates/agents/plan_roadmap.py` (250 lines)
  - [x] Follows established pattern with imperative task instructions
  - [x] Structured roadmap output format with comprehensive phase breakdown
  - [x] Multiple decomposition patterns (Foundation First, Vertical Slice, MVP Progressive)
  - [ ] **BROKEN**: Hardcoded tools (`Read`, `Grep`, `Glob`) instead of platform-injected parameters
  - [ ] **BROKEN**: Missing dual tool architecture (no state management vs platform persistence separation)
  - [ ] **BROKEN**: No action-based parameter design (`get_project_plan`, `store_roadmap_state`, etc.)
  - [ ] **BROKEN**: Function takes no parameters for platform tool injection
- [x] `services/templates/agents/roadmap_critic.py` (244 lines)
  - [x] Follows assessment pattern with structured evaluation
  - [x] No tool permissions (pure assessment agent) ✅
  - [x] CriticFeedback output format
  - [x] 5-dimension assessment criteria with weighted scoring
- [x] `services/templates/agents/create_spec.py` (253 lines)
  - [x] Template structure for roadmap retrieval and spec storage
  - [x] InitialSpec creation logic with proper scaffolding
  - [x] Parallel execution design for concurrent spec creation
  - [x] Comprehensive error handling for multiple failure modes
  - [ ] **BROKEN**: Hardcoded tools instead of platform-injected parameters
  - [ ] **BROKEN**: Missing dual tool architecture (MCP Specter state + Platform persistence)
  - [ ] **BROKEN**: No distinction between `get_roadmap_state` vs `get_roadmap_external`
  - [ ] **BROKEN**: Function takes no parameters for platform abstraction

### Phase 2: Refactor Command Template ❌ **TEMPLATE EXISTS BUT NON-FUNCTIONAL**
- [x] `services/templates/commands/plan_roadmap_command.py` (283 lines)
  - [x] Agent behavioral instructions moved to respective agent files
  - [x] Spec scaffolding logic delegated to create-spec agent
  - [x] Quality threshold references properly isolated to MCP Server
  - [x] Pure orchestration focus maintained
  - [x] Platform tool injection functionality designed
  - [x] Parallel spec creation coordination designed
  - [x] Comprehensive error handling and graceful degradation designed
  - [ ] **BROKEN**: References `mcp__specter__*` tools that don't exist
  - [ ] **BROKEN**: Cannot execute due to tool name mismatches

### Phase 3: Integration Verification ❌ **CRITICAL FAILURES**
- [ ] **BROKEN**: MCP tool alignment with `roadmap_tools.py` - wrong tool names in templates
- [ ] **BROKEN**: Loop state management integration - templates reference `mcp__specter__*` prefix that doesn't exist
- [ ] **BROKEN**: Platform-specific tool injection non-functional
- [x] Error handling and graceful degradation designed (but cannot execute due to tool issues)
- [ ] **BROKEN**: Parallel execution coordination cannot function due to tool mismatches

### Phase 4: Testing Setup
- [x] Template generation functions exist but reference wrong tools
- [x] MCP tool functions implemented and functional (but with different names than templates expect)
- [x] Data model validation implemented via Pydantic models
- [ ] Static template structure validation - would reveal tool naming issues
- [ ] Integration testing - would fail due to tool name mismatches
- [ ] Comprehensive test suite implementation

## Success Criteria

### Functional Requirements
- [ ] **BROKEN**: `/plan-roadmap` command cannot execute due to tool name mismatches
- [ ] **BROKEN**: Refinement loop cannot function - references non-existent `mcp__specter__*` tools
- [ ] **BROKEN**: Parallel spec creation coordination cannot execute
- [ ] **BROKEN**: InitialSpec creation workflow cannot execute
- [x] Graceful handling of component failures designed (but cannot be tested)

### Quality Requirements
- [x] Command template maintains orchestration focus (283 lines)
- [x] Clear separation between agents and command responsibilities
- [x] No quality thresholds referenced outside MCP Server
- [x] Comprehensive error handling and recovery patterns designed
- [x] Platform-agnostic design maintained
- [ ] **CRITICAL**: Templates reference non-existent tools, breaking all functionality

### Performance Requirements
- [ ] **BROKEN**: Parallel spec creation coordination cannot execute
- [ ] **BROKEN**: Refinement loops cannot function due to tool name mismatches
- [ ] **BROKEN**: MCP Server decision logic integration broken
- [x] Resource usage optimized through proper agent separation (design level)

## Future Enhancements

### Platform Expansion
- Complete platform tool injection implementation
- GitHub and Markdown platform support
- Platform-specific optimizations

### Workflow Integration
- Integration with `/spec` command for phase-specific specifications
- Connection to `/build` command for phased implementation
- Cross-workflow state management

### Quality Improvements
- Enhanced FSDD assessment criteria
- Machine learning insights for roadmap optimization
- User feedback integration for continuous improvement

---

*This implementation guide serves as the authoritative reference for the plan-roadmap workflow development. Update this document as architectural decisions evolve and new requirements emerge.*
