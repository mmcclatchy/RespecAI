# Structured Memory Implementation Guide

## Overview

This document contains the detailed implementation specifications for transforming the MCP Server into a structured data storage and loop integrity system. This complements the architectural overview in MCP_MEMORY_ARCHITECTURE.md with concrete implementation details.

## Implementation Plan: 3 Week MVP

### Week 1: Document Models
**Goal**: Create document models with markdown parsing/building capabilities

#### Document Model Creation
- [ ] Create `TechnicalSpec` model in services/utils/models.py
- [ ] Add fields based on phase_spec_template.md structure:
  - [ ] name, objectives, scope, dependencies, deliverables
  - [ ] architecture, technology_stack, functional_requirements
  - [ ] non_functional_requirements, development_plan, testing_strategy
  - [ ] research_requirements, success_criteria, integration_context
- [ ] Implement `parse_markdown()` method following InitialSpec pattern
- [ ] Implement `build_markdown()` method for phase_spec_template.md format
- [ ] Create placeholder `StrategicPlan` model for /plan workflow
- [ ] Create placeholder `BuildPlan` model for /build workflow

#### Testing
- [ ] Unit tests for TechnicalSpec markdown parsing/building
- [ ] Test with actual phase_spec_template.md content
- [ ] Validate round-trip: markdown → model → markdown

**Success Criteria**: TechnicalSpec can accurately parse and build phase_spec_template.md format

### Week 2: Structured Feedback Models
**Goal**: Create structured feedback system for quality tracking

#### CriticFeedback Model Enhancement
- [ ] Extend existing `CriticFeedback` model for document-specific feedback
- [ ] Add fields for FSDD scoring (0-10 scale across 12 criteria)
- [ ] Create feedback aggregation methods
- [ ] Implement feedback history tracking

#### Quality Integration
- [ ] Integrate feedback models with document models
- [ ] Create quality scoring utilities for TechnicalSpec
- [ ] Implement FSDD rubric validation
- [ ] Add quality gate threshold checking

#### Testing
- [ ] Unit tests for enhanced CriticFeedback model
- [ ] Test quality scoring integration
- [ ] Validate FSDD rubric calculations

**Success Criteria**: Structured feedback system tracks quality scores for all document types

### Week 3: MCP Integration
**Goal**: Integrate document models with existing MCP workflow

#### MCP Tool Updates
- [ ] Update spec tools to use TechnicalSpec model
- [ ] Modify loop decision logic for structured feedback
- [ ] Integrate with existing LoopState management
- [ ] Update roadmap tools for document model compatibility

#### Workflow Integration
- [ ] Test `/spec` command with TechnicalSpec model
- [ ] Validate structured feedback in loops
- [ ] Test end-to-end workflow scenarios
- [ ] Verify quality gate integration

#### Documentation
- [ ] Update MCP tool documentation
- [ ] Create usage examples
- [ ] Document model relationships

**Success Criteria**: All workflows use structured models with quality tracking

## Post-MVP: Future Expansion

### Additional Document Models (Future Phases)

1. **StrategicPlan Model** - For `/plan` workflow
2. **BuildPlan Model** - For `/build` workflow

Each expansion follows the same pattern:
1. **Model Creation**: Define document-specific model with parse_markdown/build_markdown methods
2. **Feedback Integration**: Extend CriticFeedback for new document type
3. **MCP Integration**: Update tools for new workflow
4. **Testing**: Validate end-to-end workflow

## Template Integration

### Current Template Structure

The MVP focuses on the existing `phase_spec_template.md` template structure:

```markdown
# Technical Specification: {PHASE_NAME}

## Overview
**Objectives**: `${PHASE_OBJECTIVES}`
**Scope**: `${PHASE_SCOPE}`
**Dependencies**: `${PHASE_DEPENDENCIES}`

## Deliverables
`${PHASE_DELIVERABLES}`

## System Design
### Architecture
`${TECHNICAL_FOCUS_AREAS}`

### Technology Stack
<!-- /spec completes: Languages, frameworks, libraries, and tools -->

## Implementation
### Functional Requirements
### Non-Functional Requirements
### Development Plan
### Testing Strategy

## Research Requirements
`${RESEARCH_REQUIREMENTS}`

## Success Criteria
`${SUCCESS_CRITERIA}`

## Integration
`${INTEGRATION_CONTEXT}`
```

### TechnicalSpec Model Fields

The model fields directly map to template variables:
- `name` → `{PHASE_NAME}`
- `objectives` → `${PHASE_OBJECTIVES}`
- `scope` → `${PHASE_SCOPE}`
- `dependencies` → `${PHASE_DEPENDENCIES}`
- `deliverables` → `${PHASE_DELIVERABLES}`
- `architecture` → `${TECHNICAL_FOCUS_AREAS}` + completed architecture content
- `technology_stack` → Technology Stack section content
- `functional_requirements` → Functional Requirements section content
- `non_functional_requirements` → Non-Functional Requirements section content
- `development_plan` → Development Plan section content
- `testing_strategy` → Testing Strategy section content
- `research_requirements` → `${RESEARCH_REQUIREMENTS}` + completed research content
- `success_criteria` → `${SUCCESS_CRITERIA}` + completed success content
- `integration_context` → `${INTEGRATION_CONTEXT}` + completed integration content

## MVP Enhancement Philosophy

### Additive Enhancement Approach

- **Keep what works**: The existing loop management is sophisticated and proven
- **Add what's missing**: Structured feedback and FSDD integration
- **Maintain compatibility**: All existing tools and workflows continue to function
- **Evolutionary approach**: Enhance gradually rather than revolutionary replacement

### Implementation Details

#### Week 1: Document Models (TDD + Standards Compliance)
- [ ] **RED**: Write failing tests for `TechnicalSpec` model markdown parsing
- [ ] **GREEN**: Create minimal `TechnicalSpec` model in services/models/spec.py (following InitialSpec pattern)
- [ ] **REFACTOR**: Ensure full typing (`str | None` syntax), no unnecessary docstrings, imports at top
- [ ] **RED**: Write failing tests for `build_markdown()` method
- [ ] **GREEN**: Implement `build_markdown()` for phase_spec_template.md format
- [ ] **REFACTOR**: Apply SOLID principles, resolve all mypy/ruff errors
- [ ] **RED**: Write failing tests for `StrategicPlan` and `BuildPlan` placeholder models
- [ ] **GREEN**: Create minimal placeholder models in services/models/
- [ ] **REFACTOR**: Ensure all tests pass, no warnings, coding standards compliance

#### Week 2: Structured Feedback (TDD + Standards Compliance)
- [ ] **RED**: Write failing tests for `FSSDCriteria` and `CriticAgent` enums
- [ ] **GREEN**: Add enums to services/utils/enums.py (no docstrings, clear naming)
- [ ] **REFACTOR**: Ensure enum compliance with typing standards
- [ ] **RED**: Write failing tests for `CriticFeedback` model with FSDD scoring
- [ ] **GREEN**: Create `CriticFeedback` model in services/models/feedback.py
- [ ] **REFACTOR**: Full typing, no unnecessary docstrings, SOLID compliance
- [ ] **RED**: Write failing tests for LoopState enhancement with feedback_history
- [ ] **GREEN**: Enhance existing LoopState without breaking sophistication
- [ ] **REFACTOR**: Resolve all mypy/ruff errors, maintain existing decision logic integrity

#### Week 3: MCP Integration (TDD + Standards Compliance)
- [ ] **RED**: Write failing tests for `store_critic_feedback` MCP tool
- [ ] **GREEN**: Add MCP tool to services/mcp/loop_tools.py (minimal implementation)
- [ ] **REFACTOR**: Full typing, async/await for I/O, no unnecessary docstrings
- [ ] **RED**: Write failing tests for `get_feedback_history` MCP tool
- [ ] **GREEN**: Implement feedback retrieval with existing LoopState integration
- [ ] **REFACTOR**: SOLID principles, resolve all mypy/ruff errors
- [ ] **RED**: Write failing integration tests for complete `/spec` workflow
- [ ] **GREEN**: Update critic templates, integrate FSDD scoring with existing thresholds
- [ ] **REFACTOR**: All tests pass, no warnings, backward compatibility verified

## File Structure Implementation

### MVP Project Structure

```text
spec-driven-development/
├── services/
│   ├── models/                            # Simple model organization
│   │   ├── __init__.py
│   │   ├── base.py                        # BaseModel, core enums, shared types
│   │   ├── spec.py                        # TechnicalSpec model (MVP focus)
│   │   ├── feedback.py                    # CriticFeedback model
│   │   └── session.py                     # LoopSession model
│   ├── stores/
│   │   ├── __init__.py
│   │   ├── interfaces.py                  # Store interfaces
│   │   └── memory.py                      # In-memory implementations
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── spec_tools.py                  # Updated spec tools
│   └── utils/
│       ├── __init__.py
│       ├── errors.py
│       └── markdown.py                    # Markdown generation utilities
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_stores.py
│   │   └── test_spec_tools.py
│   └── integration/
│       └── test_spec_workflow.py
└── docs/
    ├── MCP_MEMORY_ARCHITECTURE.md         # This document
    ├── MCP_MEMORY_FUTURE_FEATURES.md      # Deferred features
    └── migration/
        └── MVP_MIGRATION_GUIDE.md
```

### Future Expansion Structure
As additional loops are added, the structure will grow:
```text
services/models/
├── base.py              # Core enums and shared types
├── plan.py              # Loop 1 models
├── roadmap.py           # Loop 2 models
├── spec.py              # Loop 3 models (MVP)
├── build.py             # Loop 4 models
└── code.py              # Loop 5 models
```

**Note**: All models import enums from `base.py` to ensure type safety and consistency across loops.

### MVP Organization Principles

1. **Single File per Concept**: Each model type gets its own file
2. **Flat Structure**: Avoid deep directory nesting for initial implementation
3. **Clear Dependencies**: Base models used by all others
4. **Simple Expansion**: Easy to add new loop models as single files

### Service Layer Separation

1. **Models**: Pure Pydantic data structures with validation
2. **Stores**: Simple in-memory data persistence
3. **MCP Tools**: Protocol adaptation layer only
4. **Utils**: Minimal cross-cutting concerns (errors, markdown generation)

## Coding Standards Compliance

### Mandatory Requirements (Per CLAUDE.md)

**Every implementation step must follow:**

1. **No Unnecessary Documentation**
   - No docstrings for obvious getters, simple CRUD operations
   - Docstrings ONLY for MCP tools (external agent interfaces) and complex algorithms
   - No obvious comments on variable declarations or simple operations

2. **Full Typing Standards**
   - Every parameter and return value typed
   - Use `str | None` syntax (never `Optional[str]`)
   - All imports at file top (no inline imports)

3. **Code Quality Gates**
   - All tests pass without warnings
   - Zero mypy errors
   - Zero ruff errors
   - Max 3 levels of nesting
   - No global variables (except UPPER_CASE constants)

4. **TDD Methodology**
   - **RED**: Write failing test first
   - **GREEN**: Minimal implementation to pass test
   - **REFACTOR**: Apply standards, SOLID principles, resolve all linting errors

### Implementation Validation

Each week concludes with mandatory validation:
- [ ] `uv run mypy services/` passes with no errors
- [ ] `uv run ruff check services/` passes with no errors
- [ ] `uv run pytest tests/` passes with no warnings
- [ ] Manual code review for unnecessary docstrings/comments
- [ ] SOLID principles applied (Single Responsibility, Open/Closed, etc.)

### Example Model Structure

```python
# services/models/spec.py
from datetime import datetime
from pydantic import BaseModel, Field

class TechnicalSpec(BaseModel):
    name: str
    objectives: str
    scope: str
    dependencies: str
    deliverables: str
    architecture: str
    technology_stack: str
    functional_requirements: str
    non_functional_requirements: str
    development_plan: str
    testing_strategy: str
    research_requirements: str
    success_criteria: str
    integration_context: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> "TechnicalSpec":
        """Parse phase_spec_template.md format into structured fields.

        Implements complex regex parsing logic for variable extraction
        from markdown template format.
        """
        # Complex implementation warranting docstring

    def build_markdown(self) -> str:
        # Simple template substitution - no docstring needed
        return template.substitute(self.model_dump())
```

## Anti-patterns & Implementation Gotchas

### 1. Model Design Anti-patterns

#### L Mixing Loop Concerns
```python
# WRONG: Single model trying to handle multiple loops
class UniversalState:
    plan_data: dict
    spec_data: dict
    build_data: dict
    code_data: dict
```

#### Separate Models per Loop
```python
# RIGHT: Dedicated models for each loop
class PlanningLoopSession: ...
class SpecificationLoopSession: ...
class BuildPlanningLoopSession: ...
class CodeImplementationLoopSession: ...
```

### 2. Storage Anti-patterns

#### L Storing Rendered Content
```python
# WRONG: Storing markdown in database
def store_spec(self, spec_markdown: str):
    self.db["spec"] = spec_markdown
```

#### Store Structured Data
```python
# RIGHT: Store structured model, generate markdown on demand
def store_spec(self, spec: EnhancedInitialSpec):
    self.specs[spec.name] = spec

def get_spec_markdown(self, name: str) -> str:
    return self.specs[name].to_markdown()
```

### 3. Platform Coupling Anti-patterns

#### L Platform-Specific Logic in Models
```python
# WRONG: Model knows about platforms
class BuildPlan:
    def create_linear_ticket(self): ...
    def create_github_issue(self): ...
```

#### Platform-Agnostic Models
```python
# RIGHT: Model is pure data, platform logic elsewhere
class BuildPlan:
    def to_markdown(self) -> str: ...
    # Platform adapters handle platform-specific logic
```

### 4. State Management Anti-patterns

#### L Global State Mutation
```python
# WRONG: Direct global state modification
global_state.current_loop.score = 95
```

#### Immutable Updates
```python
# RIGHT: Create new state with updates
new_session = session.with_feedback(feedback)
state_manager.update_session(new_session)
```

### 5. Feedback Tracking Anti-patterns

#### L Unstructured Feedback Storage
```python
# WRONG: Feedback as raw strings
feedback_list.append(f"Score: {score}, Comments: {comments}")
```

#### Structured Feedback Models
```python
# RIGHT: Type-safe feedback with validation
feedback = CriticFeedback(
    critic_agent=CriticAgent.PLAN_CRITIC,
    quality_score=score,
    improvement_suggestions=suggestions
)
```

### 6. Testing Blind Spots

#### Common Testing Gaps to Avoid
1. **Round-trip Validation**: Test markdown → model → markdown consistency
2. **Concurrent Access**: Test parallel loop execution
3. **Platform Conversion**: Test all platform output formats
4. **Stagnation Detection**: Test edge cases in quality progression
5. **Session Lifecycle**: Test session creation, update, completion
6. **Feedback Integration**: Test all critic feedback paths

### 7. Performance Pitfalls

#### L Loading Everything
```python
# WRONG: Load all sessions into memory
def get_all_sessions(self):
    return self.load_entire_database()
```

#### Lazy Loading
```python
# RIGHT: Load only what's needed
def get_active_session(self, session_id: str):
    return self.load_session(session_id)
```

### 8. Error Handling Mistakes

#### L Silent Failures
```python
# WRONG: Swallow exceptions
try:
    update_component(component)
except:
    pass
```

#### Explicit Error Handling
```python
# RIGHT: Handle specific errors with context
try:
    update_component(component)
except ComponentNotFoundError as e:
    raise UpdateError(f"Cannot update {component.name}: {e}")
```

## Success Criteria

The MVP will be considered successful when:

1. **TechnicalSpec Model**: Successfully parse and build phase_spec_template.md format (100% field mapping accuracy)
2. **FSDD Integration**: CriticFeedback model with 12-point scoring (0-10 → 0-100) implemented and tested
3. **LoopState Enhancement**: Feedback history integrated with existing decision logic without breaking current thresholds
4. **MCP Integration**: `/spec` command uses structured models seamlessly with existing workflow
5. **Round-trip Validation**: Markdown → model → markdown produces identical content (character-for-character match)
6. **Quality Tracking**: FSDD scores tracked and improving across iterations (scores increase or maintain 7+ consistently)
7. **Code Quality**: Zero mypy errors, zero ruff errors, all tests pass without warnings
8. **Standards Compliance**: No unnecessary docstrings/comments, full typing, TDD methodology followed

This implementation guide provides the concrete steps needed to enhance the MCP Server with structured feedback capabilities for the Spec-Driven Development workflow.
