# Structured Memory Implementation Guide

## Overview

This document contains the detailed implementation specifications for transforming the MCP Server into a structured data storage and loop integrity system. This complements the architectural overview in MCP_MEMORY_ARCHITECTURE.md with concrete implementation details.

## Implementation Plan: 3 Week MVP

### Week 1: Document Models
**Goal**: Create document models with markdown parsing/building capabilities

#### Document Model Creation
- [x] Create `TechnicalSpec` model in services/utils/models.py
- [x] Add fields based on phase_spec_template.md structure:
  - [x] name, objectives, scope, dependencies, deliverables
  - [x] architecture, technology_stack, functional_requirements
  - [x] non_functional_requirements, development_plan, testing_strategy
  - [x] research_requirements, success_criteria, integration_context
- [x] Implement `parse_markdown()` method following InitialSpec pattern
- [x] Implement `build_markdown()` method for phase_spec_template.md format
- [x] Create placeholder `StrategicPlan` model for /plan workflow
- [x] Create placeholder `BuildPlan` model for /build workflow

#### Testing
- [x] Unit tests for TechnicalSpec markdown parsing/building
- [x] Test with actual phase_spec_template.md content
- [x] Validate round-trip: markdown → model → markdown

**Success Criteria**: TechnicalSpec can accurately parse and build phase_spec_template.md format

### Week 2: Structured Feedback Models
**Goal**: Create structured feedback system for quality tracking

#### CriticFeedback Model Enhancement
- [x] Extend existing `CriticFeedback` model for document-specific feedback
- [x] Add fields for FSDD scoring (0-10 scale across 12 criteria)
- [x] Create feedback aggregation methods
- [x] Implement feedback history tracking

#### Quality Integration
- [x] Integrate feedback models with document models
- [x] Create quality scoring utilities for TechnicalSpec
- [x] Implement FSDD rubric validation
- [x] Add quality gate threshold checking

#### Testing
- [x] Unit tests for enhanced CriticFeedback model
- [x] Test quality scoring integration
- [x] Validate FSDD rubric calculations

**Success Criteria**: Structured feedback system tracks quality scores for all document types

### Week 3: Comprehensive MCP Integration
**Goal**: Integrate ALL document models and structured feedback with complete MCP workflow coverage

#### Universal Feedback Tools (All Workflows)
- [ ] Create `store_critic_feedback` MCP tool - works with ANY loop type
- [ ] Create `get_feedback_history` MCP tool - retrieves structured feedback for ANY loop
- [ ] Update existing `loop_tools.py` to use structured CriticFeedback instead of string feedback
- [ ] Integrate FSDD scoring with all existing loop decision logic

#### Document-Specific MCP Tools (Complete CRUD)
- [ ] Create `project_plan_tools.py` - Full CRUD for ProjectPlan model (/plan workflow)
- [ ] Create `feature_requirements_tools.py` - Full CRUD for FeatureRequirements model (/feature-requirements workflow)
- [ ] Create `roadmap_tools.py` enhancement - Add Roadmap model support (/plan-roadmap workflow)
- [ ] Create `spec_tools.py` - Full CRUD for TechnicalSpec model (/spec workflow)
- [ ] Create `build_plan_tools.py` - Full CRUD for BuildPlan model (/build workflow)

#### Enhanced Loop Integration (All 5 Workflows)
- [ ] Update loop decision logic to use structured feedback across ALL loop types
- [ ] Integrate quality gate thresholds with FSDD scoring for ALL workflows
- [ ] Ensure backward compatibility with existing sophisticated loop management
- [ ] Test all 5 workflows: /plan, /feature-requirements, /plan-roadmap, /spec, /build

#### Comprehensive Workflow Coverage
- [ ] Test ProjectPlan workflow with structured feedback and quality gates
- [ ] Test FeatureRequirements workflow with critic feedback integration
- [ ] Test Roadmap workflow with enhanced document model support
- [ ] Test TechnicalSpec workflow with complete FSDD integration
- [ ] Test BuildPlan workflow with structured feedback and decision logic
- [ ] Validate cross-workflow state management and feedback consistency

#### Quality Gate Integration (Universal)
- [ ] FSDD scoring integrated with ALL 5 document types
- [ ] Quality thresholds working across ALL loop types
- [ ] Stagnation detection enhanced with structured feedback for ALL workflows
- [ ] Critic feedback consistency across iterations for ALL document types

#### Documentation & Standards
- [ ] Update MCP tool documentation for ALL 5 workflows
- [ ] Create comprehensive usage examples for each document type
- [ ] Document structured feedback model relationships
- [ ] Ensure all code follows TDD methodology and coding standards

**Success Criteria**: All workflows use structured models with quality tracking

## Post-MVP: Future Expansion

### Additional Document Models (Future Phases)

1. **ProjectPlan Model** - For `/plan` workflow
2. **FeatureRequirements Model** - For `/feature-requirements` workflow
3. **Roadmap Model** - For `/plan-roadmap` workflow
4. **BuildPlan Model** - For `/build` workflow

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

#### Week 1: Complete Template & Model Creation (TDD + Standards Compliance)
**Goal**: Create ALL templates and models for the complete workflow with full parsing/building

##### ProjectPlan Template & Model
- [x] **RED**: Write failing tests for `ProjectPlan` markdown parsing/building
- [x] **GREEN**: Create `project_plan_template.md` and `ProjectPlan` model
- [x] **REFACTOR**: Ensure full typing, no unnecessary docstrings, coding standards

##### FeatureRequirements Template & Model
- [x] **RED**: Write failing tests for `FeatureRequirements` markdown parsing/building
- [x] **GREEN**: Create `feature_requirements_template.md` and `FeatureRequirements` model
- [x] **REFACTOR**: Apply SOLID principles, resolve all mypy/ruff errors

##### Roadmap Template & Model
- [x] **RED**: Write failing tests for `Roadmap` markdown parsing/building
- [x] **GREEN**: Create `roadmap_template.md` and `Roadmap` model
- [x] **REFACTOR**: Ensure round-trip parsing accuracy

##### Enhanced Spec Template & Model
- [x] **RED**: Write failing tests for enhanced `TechnicalSpec`
- [x] **GREEN**: Update existing `phase_spec_template.md` and `TechnicalSpec` model
- [x] **REFACTOR**: Ensure character-for-character round-trip accuracy

##### BuildPlan Template & Model
- [x] **RED**: Write failing tests for `BuildPlan` markdown parsing/building
- [x] **GREEN**: Create `build_plan_template.md` and `BuildPlan` model
- [x] **REFACTOR**: Final standards compliance validation

**Success Criteria**: All document types can parse markdown → model → markdown with identical output ✅ **COMPLETED**

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

#### Week 3: Comprehensive MCP Integration (TDD + Standards Compliance)

##### Universal Feedback Tools (All Workflows)
- [ ] **RED**: Write failing tests for `FeedbackTools` class with `store_critic_feedback` method
- [ ] **GREEN**: Create services/mcp/feedback_tools.py with universal feedback storage
- [ ] **REFACTOR**: Full typing, SOLID principles, error handling for all loop types
- [ ] **RED**: Write failing tests for `get_feedback_history` method in FeedbackTools
- [ ] **GREEN**: Implement feedback retrieval working with ANY loop type
- [ ] **REFACTOR**: Resolve all mypy/ruff errors, consistent response formats

##### Document-Specific MCP Tools (Complete CRUD Coverage)
- [ ] **RED**: Write failing tests for `ProjectPlanTools` - full CRUD operations
- [ ] **GREEN**: Create services/mcp/project_plan_tools.py with ProjectPlan model integration
- [ ] **REFACTOR**: Consistent error handling, full typing, standards compliance
- [ ] **RED**: Write failing tests for `FeatureRequirementsTools` - full CRUD operations
- [ ] **GREEN**: Create services/mcp/feature_requirements_tools.py with FeatureRequirements model
- [ ] **REFACTOR**: SOLID principles, no unnecessary docstrings
- [ ] **RED**: Write failing tests for enhanced `RoadmapTools` - add Roadmap model support
- [ ] **GREEN**: Update services/mcp/roadmap_tools.py to support both RoadMap and Roadmap models
- [ ] **REFACTOR**: Backward compatibility, clean separation of concerns
- [ ] **RED**: Write failing tests for `SpecTools` - TechnicalSpec model integration
- [ ] **GREEN**: Create services/mcp/spec_tools.py with TechnicalSpec model support
- [ ] **REFACTOR**: Full typing, async/await for I/O, error handling
- [ ] **RED**: Write failing tests for `BuildPlanTools` - full CRUD operations
- [ ] **GREEN**: Create services/mcp/build_plan_tools.py with BuildPlan model integration
- [ ] **REFACTOR**: Standards compliance, consistent API patterns

##### Enhanced Loop Integration (All 5 Workflows)
- [ ] **RED**: Write failing tests for enhanced `LoopTools` with structured feedback
- [ ] **GREEN**: Update services/mcp/loop_tools.py to use CriticFeedback instead of strings
- [ ] **REFACTOR**: Maintain existing sophisticated decision logic, add feedback integration
- [ ] **RED**: Write failing integration tests for ALL 5 workflows with structured feedback
- [ ] **GREEN**: Integrate FSDD scoring with quality gates across all loop types
- [ ] **REFACTOR**: All tests pass, no warnings, complete backward compatibility verified

##### Comprehensive Testing & Validation
- [ ] **RED**: Write failing end-to-end tests for complete workflows: /plan, /feature-requirements, /plan-roadmap, /spec, /build
- [ ] **GREEN**: Ensure all document models work seamlessly with their respective MCP tools
- [ ] **REFACTOR**: Performance optimization, error message consistency, documentation updates

## File Structure Implementation

### Current Project Structure (Week 1 Complete)

```text
spec-driven-development/
├── services/
│   ├── models/                            # Complete document models
│   │   ├── __init__.py
│   │   ├── project_plan.py                # ProjectPlan model (35 fields)
│   │   ├── feature_requirements.py        # FeatureRequirements model (22 fields)
│   │   ├── roadmap.py                     # Roadmap model (40+ fields)
│   │   ├── spec.py                        # TechnicalSpec model (20 fields)
│   │   └── build_plan.py                  # BuildPlan model (21 fields)
│   ├── templates/                         # All document templates
│   │   ├── agents/
│   │   ├── commands/
│   │   ├── documents/
│   │   │   ├── build_plan_template.md
│   │   │   ├── feature_requirements_template.md
│   │   │   ├── project_plan_template.md
│   │   │   ├── roadmap_template.md
│   │   │   └── spec_template.md
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
│   │   ├── models/
│   │   │   ├── test_project_plan.py
│   │   │   ├── test_feature_requirements.py
│   │   │   ├── test_roadmap.py
│   │   │   ├── test_spec.py
│   │   │   └── test_build_plan.py
│   │   ├── test_stores.py
│   │   └── test_spec_tools.py
│   └── integration/
│       └── test_spec_workflow.py
└── docs/
    ├── MCP_MEMORY_ARCHITECTURE.md          # MCP Memory Architecture
    ├── STRUCTURED_MEMORY_IMPLEMENTATION.md # This document
    ├── ARCHITECTURE.md                     # System architecture
    └── ARCHITECTURE_ANALYSIS.md            # Workflow analysis
```

### Future Expansion Structure
As additional loops are added, the structure will grow:
```text
services/models/
├── base.py                  # Core enums and shared types
├── project_plan.py          # Loop 1 models
├── feature_requirements.py  # Loop 2 models
├── roadmap.py              # Loop 3 models
├── spec.py                 # Loop 4 models (MVP)
└── build_plan.py           # Loop 5 models
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

## Coding Standards Compliance (Per CLAUDE.md)

### **MANDATORY REQUIREMENTS - These override ALL other guidelines**

#### **Critical Requirements**
- **No test logic in production** - Keep test code completely separate
- **Minimal comments** - Code should be self-documenting through clear naming and structure
- **Docstrings ONLY for**:
  - Public API interfaces exposed to other services
  - MCP tools that will be called by external agents
  - Complex algorithms where the "why" isn't obvious from the code
  - **NOT for**: Obvious getters, simple CRUD operations, basic parameter mapping
- **Comments ONLY for**:
  - Non-obvious business logic or algorithms
  - Complex mathematical operations
  - Regulatory/compliance requirements
  - **NEVER for**: Variable declarations, simple function calls, obvious operations
- **No global variables** (except `UPPER_CASE` constants)
- **Minimal nesting** - Max 3 levels deep
- **No inline imports** - All imports at file top (except circular dependency resolution)
- **Languages**: Python only

#### **Python Standards**
- **Virtual environment**: Use `uv` for all Python operations
- **Imports**: Absolute imports at file top
- **Async/await**: Required for all I/O operations
- **Full typing**: Every parameter and return value typed
- **Type syntax**: `str | None` (never `Optional[str]`)
- **Models**: Use Pydantic v2
- **Architecture**: Service layer separate from endpoints
- **Testing**: pytest + pytest-mock only

#### **Quality Gates**
- All endpoints delegate to services
- All functions fully typed
- No business logic in routes
- Tests cover service layer

### **TDD Methodology - Modified for External Packages**

**Standard TDD Cycle:**
1. **RED**: Write failing test first
2. **GREEN**: Minimal implementation to pass test
3. **REFACTOR**: Apply standards, SOLID principles, resolve all linting errors

**Exception for External Packages:**
- **Skip sole testing of Pydantic models** - Trust they work out-of-the-box
- **Test business logic integration** - Test how our code uses Pydantic
- **Test complex parsing/building logic** - Our custom regex and template logic needs testing

### **Weekly Validation Requirements**

Each week concludes with mandatory validation:
- [ ] `uv run mypy services/` passes with no errors
- [ ] `uv run ruff check services/` passes with no errors
- [ ] `uv run pytest tests/` passes with no warnings
- [ ] Manual code review for unnecessary docstrings/comments
- [ ] SOLID principles applied (Single Responsibility, Open/Closed, etc.)
- [ ] No mock/placeholder code in production

### **Enforcement**

**MANDATORY COMPLIANCE**: These rules override all global guidelines and defaults.

**Immediate Correction Required**: Any violation must be fixed before proceeding with other work.

**No Exceptions Without Authorization**: These standards apply to ALL code - services, tests, utilities, scripts.

### **Self-Review Checklist**
- [ ] No obvious docstrings or comments
- [ ] All imports at top of file
- [ ] No inline imports
- [ ] Functions/variables have clear, self-documenting names
- [ ] Complex logic (and only complex logic) is documented
- [ ] No mock/placeholder production code

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

The comprehensive structured memory system will be considered successful when:

### Week 1: Document Models ✅ **COMPLETED**
1. **All Document Models**: ProjectPlan, FeatureRequirements, Roadmap, TechnicalSpec, BuildPlan parse/build templates (100% accuracy)
2. **Round-trip Validation**: ALL document types: markdown → model → markdown produces identical content
3. **Template Integration**: All 5 document templates working with their respective models

### Week 2: Structured Feedback ✅ **COMPLETED**
1. **FSDD Integration**: CriticFeedback model with 12-point scoring (0-10 → 0-100) implemented and tested
2. **LoopState Enhancement**: Feedback history integrated with existing decision logic without breaking sophistication
3. **Quality Framework**: FSDD scoring system working across all document types

### Week 3: Comprehensive MCP Integration
1. **Universal Feedback Tools**: `store_critic_feedback` and `get_feedback_history` work with ALL 5 loop types
2. **Complete Document CRUD**: MCP tools for ALL 5 document types (ProjectPlan, FeatureRequirements, Roadmap, TechnicalSpec, BuildPlan)
3. **Enhanced Loop Integration**: ALL 5 workflows (/plan, /feature-requirements, /plan-roadmap, /spec, /build) use structured feedback
4. **Quality Gate Integration**: FSDD scoring integrated with loop decision logic across ALL workflow types
5. **Backward Compatibility**: Existing sophisticated loop management preserved and enhanced
6. **Cross-Workflow Validation**: All document types work seamlessly with structured feedback and quality gates

### Technical Excellence Standards
1. **Code Quality**: Zero mypy errors, zero ruff errors, all tests pass without warnings across ALL implementations
2. **Standards Compliance**: No unnecessary docstrings/comments, full typing, TDD methodology followed throughout
3. **Performance**: Efficient state management across all 5 document types and feedback systems
4. **Error Handling**: Consistent, informative error messages across all MCP tools and workflows

This implementation guide provides the concrete steps needed to enhance the MCP Server with structured feedback capabilities for the Spec-Driven Development workflow.
