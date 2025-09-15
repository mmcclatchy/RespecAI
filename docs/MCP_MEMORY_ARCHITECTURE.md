# MCP Memory Architecture

## Executive Summary

The MCP Server will evolve from a simple tool coordinator into a **structured data storage and loop integrity system** that maintains workflow state, tracks quality progression, and provides reliable state management across all five refinement loops of the Spec-Driven Development workflow.

**Key Principle**: The MCP Server handles data storage and loop management only. All analysis, decision-making, and cross-loop coordination happens within Claude Code itself.

### Vision
Transform the MCP Server into a **structured data storage system** that:
- Stores workflow artifacts as structured Pydantic models instead of markdown documents
- Enables incremental updates at the component level without full document regeneration
- Tracks comprehensive critic feedback and quality progression across all loops
- Maintains platform-agnostic data that can generate markdown for any target (Linear/GitHub/local files)

### Key Problems Being Solved

1. **Markdown Parsing Variability**: Claude's markdown interpretation can vary between sessions, causing inconsistent state reconstruction
2. **Document Handling Overhead**: Passing full markdown documents between agents creates unnecessary token usage and parsing complexity
3. **State Reconstruction Errors**: Rebuilding state from markdown is error-prone and loses metadata
4. **Limited Progress Tracking**: Current system lacks granular feedback tracking and quality progression metrics
5. **Platform Coupling**: Markdown-first approach makes platform switching difficult

### Benefits of Structured Data Architecture

- **State Memory Foundation**: MCP Server provides reliable memory bank, eliminating Claude Code's need to reconstruct workflow context from markdown parsing
- **Reduced Cognitive Load**: Structured data access removes LLM burden of markdown interpretation and state reconstruction across sessions
- **Consistency Guarantee**: Pydantic validation ensures data integrity and eliminates parsing errors that create workflow inconsistencies
- **Context Preservation**: Maintains complete workflow history, feedback progression, and quality metrics without information loss
- **Platform Flexibility**: Generate platform-specific outputs on-demand from canonical structured data
- **Workflow Reliability**: Dependable state management enables consistent loop progression and decision-making

## Current Implementation Analysis

### What Already Exists (Sophisticated Loop Management)
- **FastMCP Server**: Production-ready MCP server with middleware, error handling, and logging
- **Advanced Loop Management**: Sophisticated loop state tracking with configurable thresholds
- **Smart Decision Logic**: Automatic stagnation detection, score history tracking, and iteration management
- **Flexible State Storage**: InMemoryStateManager with queue-based history management (max 10 items)
- **Roadmap & Spec Management**: Full CRUD operations for roadmaps and specifications
- **Template System**: Dynamic command and agent generation based on platform selection
- **Quality Thresholds**: Per-loop-type configurable thresholds and improvement detection

### Current Model Architecture
```python
# EXISTING: LoopState (already sophisticated)
class LoopState:
    id: str
    loop_type: LoopType  # PLAN, ROADMAP, SPEC, BUILD_PLAN, BUILD_CODE, ANALYST
    status: LoopStatus   # INITIALIZED, IN_PROGRESS, COMPLETED, USER_INPUT, REFINE
    current_score: int   # 0-100 scoring already implemented
    score_history: list[int]  # Automatic history tracking
    iteration: int       # Iteration management
    created_at: str
    # + sophisticated decision logic with stagnation detection

# EXISTING: InitialSpec (markdown-based but functional)
class InitialSpec:
    name: str
    objectives: str
    scope: str
    dependencies: str
    deliverables: str
    architecture: str
    # + markdown parsing and generation methods
```

### What Works Exceptionally Well
- **Sophisticated Loop Decision Logic**: Automatic threshold checking, stagnation detection, max iterations
- **Configurable Quality Gates**: Per-loop-type thresholds via settings (plan_threshold, spec_threshold, etc.)
- **Score History Tracking**: Automatic improvement calculation and trend analysis
- **State Management**: Clean separation between loop state and roadmap/spec storage
- **Error Handling**: Comprehensive error mapping and validation
- **Template System**: Platform-agnostic command and agent generation

### Current Limitations (Areas for Enhancement)
- **Feedback Storage**: Critic feedback stored as simple strings rather than structured data
- **FSDD Integration**: No structured 12-point FSDD scoring framework
- **Quality Metrics**: Missing detailed rubric-based assessment
- **Feedback Consistency**: No mechanism for critics to reference previous feedback

## Architectural Goals

### 1. Eliminate Markdown Parsing Inconsistencies
- Store all workflow artifacts as structured Pydantic models
- Use type-safe field access instead of regex parsing
- Validate all data on input with clear error messages
- Maintain single source of truth in structured format

### 2. Enable Reliable State Management
- Consistent state storage and retrieval across loops
- Simple session-based state isolation
- Clear state transitions with validation

### 3. Track Quality Progression
- Standardized `CriticFeedback` model across all loops
- FSDD 12-point quality framework scoring
- Basic iteration progression tracking
- Simple stagnation detection

### 4. Maintain Platform Agnosticism
- Core data models independent of output format
- On-demand markdown generation for any platform
- Platform-specific metadata storage
- Template-based output generation

## MVP Scope: Single Loop Proof of Concept

### Initial Focus: Loop 3 (Technical Specification)
**Why This Loop:**
- Well-defined input/output structure
- Clear quality assessment criteria
- Existing FSDD framework integration
- Representative complexity for other loops
- Platform integration already working

### MVP Components
1. **Core Models**: `TechnicalSpec`, `CriticFeedback`, `LoopSession`
2. **Basic Storage**: In-memory store with simple CRUD operations
3. **MCP Integration**: Update existing spec tools to use structured models
4. **Quality Tracking**: Basic FSDD scoring and iteration management
5. **Platform Generation**: Markdown output generation from structured data

### Success Criteria for MVP
- Zero markdown parsing errors for technical specifications
- Successful round-trip: structured data → platform markdown → validation
- Basic quality progression tracking with stagnation detection
- Seamless integration with existing `/spec` command workflow

## Future Loop Integration
Once MVP proves successful with Loop 3, expand to other loops in this order:
1. **Loop 2** (Roadmap): Similar structure, clear deliverables
2. **Loop 4** (Build Planning): Well-defined steps and dependencies
3. **Loop 1** (Strategic Planning): More complex with conversational context
4. **Loop 5** (Code Implementation): Most complex with TDD cycle tracking

## Core Concepts

### Session-Based Loop Management
Each refinement loop operates within a simple session that tracks:
- Unique session identifier
- Loop type (using `LoopType` enum)
- Current iteration count
- Quality score progression
- Basic status (using `LoopStatus` enum)

## Proposed Model Enhancements (Building on Existing Foundation)

### Current Enums (Already Implemented)
```python
# CURRENT: LoopType enum (from services/utils/enums.py)
class LoopType(Enum):
    PLAN = 'plan'
    ROADMAP = 'roadmap'
    SPEC = 'spec'
    BUILD_PLAN = 'build_plan'
    BUILD_CODE = 'build_code'
    ANALYST = 'analyst'
    # Each has configurable threshold, improvement_threshold, max_iterations

# CURRENT: LoopStatus enum (from services/utils/enums.py)
class LoopStatus(Enum):
    INITIALIZED = 'initialized'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    USER_INPUT = 'user_input'
    REFINE = 'refine'
```

### New Enums (To Be Added)
```python
# PROPOSED: FSDD Criteria for structured feedback
class FSSDCriteria(str, Enum):
    CLARITY = "clarity"
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    FEASIBILITY = "feasibility"
    TESTABILITY = "testability"
    MAINTAINABILITY = "maintainability"
    SCALABILITY = "scalability"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USABILITY = "usability"
    DOCUMENTATION = "documentation"
    INTEGRATION = "integration"

# PROPOSED: Critic Agent identification
class CriticAgent(str, Enum):
    PLAN_CRITIC = "plan-critic"
    ANALYST_CRITIC = "analyst-critic"
    ROADMAP_CRITIC = "roadmap-critic"
    SPEC_CRITIC = "spec-critic"
    BUILD_CRITIC = "build-critic"
    BUILD_REVIEWER = "build-reviewer"
```

### Document Model Architecture

#### Three Document Types Required

**1. TechnicalSpec Model (for /spec workflow)**
Based on phase_spec_template.md structure with fields for complete technical specifications:
```python
# PROPOSED: TechnicalSpec (for /spec workflow)
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

    # Following InitialSpec pattern
    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        """Parse phase_spec_template.md format into structured fields"""

    def build_markdown(self) -> str:
        """Generate markdown in phase_spec_template.md format"""
```

**2. StrategicPlan Model (for /plan workflow)**
```python
# PROPOSED: StrategicPlan (for /plan workflow)
class StrategicPlan(BaseModel):
    # Fields TBD based on actual /plan workflow requirements
    # Following InitialSpec pattern with parse_markdown() and build_markdown()
```

**3. BuildPlan Model (for /build workflow)**
```python
# PROPOSED: BuildPlan (for /build workflow)
class BuildPlan(BaseModel):
    # Fields TBD based on actual /build workflow requirements
    # Following InitialSpec pattern with parse_markdown() and build_markdown()
```

#### New: CriticFeedback Model (Adding Structured Feedback)
```python
# PROPOSED: CriticFeedback (new model for structured feedback)
class CriticFeedback(BaseModel):
    session_id: str  # Links to LoopState.id
    critic_agent: CriticAgent
    iteration: int
    quality_score: int  # 0-100 (calculated from fsdd_scores average * 10)
    overall_assessment: str
    improvements: list[str]
    fsdd_scores: dict[FSSDCriteria, int]  # Each criterion scored 0-10
    timestamp: datetime

    # Integration with existing LoopState
    def calculate_overall_score(self) -> int:
        """Calculate 0-100 score from FSDD criteria scores"""
        if not self.fsdd_scores:
            return 0
        avg_score = sum(self.fsdd_scores.values()) / len(self.fsdd_scores)
        return int(avg_score * 10)  # Convert 0-10 to 0-100
```

#### FSDD Scoring Approach
**Individual Criteria**: Each of the 12 FSDD criteria is scored 0-10 using rubric descriptors:
- **0-2**: Critical issues, major gaps
- **3-4**: Significant problems, needs substantial work
- **5-6**: Adequate with notable issues
- **7-8**: Good quality with minor improvements needed
- **9-10**: Excellent, meets or exceeds expectations

**Overall Score**: Calculated as `(sum of all fsdd_scores) / 12 * 10` for familiar 0-100 percentage format.

**LLM Evaluation**: Critics use prompt engineering with clear rubric descriptors for each criterion, providing "good enough" consistency for practical workflow management.

#### LoopState Enhancement (Building on Existing Model)
```python
# CURRENT: LoopState (services/utils/models.py) - Already Sophisticated!
class LoopState(BaseModel):
    id: str
    loop_type: LoopType
    status: LoopStatus
    current_score: int  # 0-100 scoring
    score_history: list[int]  # Already tracks history!
    iteration: int  # Already manages iterations!
    created_at: str

    # EXISTING: Advanced decision logic with stagnation detection
    def decide_next_loop_action(self) -> MCPResponse:
        # Already implements threshold checking and stagnation detection!

    def _detect_stagnation(self) -> bool:
        # Already implements sophisticated stagnation detection!

# PROPOSED: LoopState Enhancement (add feedback storage)
class EnhancedLoopState(LoopState):
    # New field for structured feedback
    feedback_history: list[CriticFeedback] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.now)

    def add_feedback(self, feedback: CriticFeedback) -> None:
        """Add structured feedback and update score"""
        self.feedback_history.append(feedback)
        self.add_score(feedback.quality_score)  # Use existing score tracking
        self.updated_at = datetime.now()

    def get_recent_feedback(self, count: int = 5) -> list[CriticFeedback]:
        """Get recent feedback for context (leverages existing sophistication)"""
        return self.feedback_history[-count:] if self.feedback_history else []
```

### Quality History and Feedback Storage Value

#### Feedback Consistency Benefits
Storing previous `CriticFeedback` provides significant value:
- **Consistency Across Iterations**: Critics can reference previous feedback to avoid contradictory suggestions
- **Building Context**: New feedback can build upon previous suggestions rather than starting fresh
- **Progress Tracking**: Quality history shows improvement trends and detects stagnation
- **Debugging Support**: Historical feedback helps identify recurring issues or patterns

#### Storage Strategy
- **Recent Feedback**: Store feedback from recent iterations for context (e.g., last 5 iterations)
- **Queue Management**: Use queue-based cleanup to prevent unbounded storage growth
- **Context Window**: Critics receive previous feedback as context for consistency
- **Score Progression**: `quality_history` tracks numerical progression for stagnation detection

### Critic Feedback Integration

#### Standardized Feedback Model
```text
CriticFeedback:
- critic_agent: Enum identifying the critic
- iteration_number: Current iteration count
- quality_score: 0-100 (calculated from fsdd_scores average * 10)
- overall_assessment: Summary evaluation
- improvement_suggestions: List of specific improvements
- fsdd_scores: Individual criteria scores (each 0-10 with rubric descriptors)
- timestamp: When feedback was provided
```

#### FSDD Quality Framework
12-point criteria evaluated by all critics:
- Clarity, Completeness, Consistency
- Feasibility, Testability, Maintainability
- Scalability, Security, Performance
- Usability, Documentation, Integration

## Implementation Strategy: Evolution Not Revolution

### Current Foundation is Strong
The existing implementation already provides sophisticated loop management that exceeds many of the original architectural goals:
- ✅ **Advanced Loop Decision Logic**: Configurable thresholds, stagnation detection, iteration management
- ✅ **Score History Tracking**: Automatic improvement calculation and trend analysis
- ✅ **Flexible State Management**: Clean separation and queue-based history
- ✅ **Production-Ready MCP Server**: FastMCP with middleware, error handling, logging
- ✅ **Complete CRUD Operations**: Full roadmap and specification management

### MVP Enhancement Strategy

#### Document Models + Structured Feedback Integration
Build essential document models and structured feedback on top of the existing sophisticated LoopState system.

**Implementation Details**: See [STRUCTURED_MEMORY_IMPLEMENTATION.md](STRUCTURED_MEMORY_IMPLEMENTATION.md) for specific enhancement specifications and backward compatibility requirements.

## Template Integration

The structured memory system will integrate with the existing template system to generate platform-specific outputs from structured data. Templates remain the bridge between structured models and platform-specific formats (Linear/GitHub/Markdown).

**Implementation Details**: See [STRUCTURED_MEMORY_IMPLEMENTATION.md](STRUCTURED_MEMORY_IMPLEMENTATION.md) for complete 3-week implementation plan, model specifications, and integration requirements.

## Success Metrics

The structured memory architecture will be validated against these key outcomes:

- **Consistency**: Eliminate markdown parsing errors and state reconstruction issues
- **Performance**: Reduce token usage and processing overhead for state management
- **Reliability**: Ensure accurate state persistence and retrieval across sessions
- **Quality Tracking**: Provide comprehensive audit trail for workflow decisions
- **Platform Support**: Enable seamless generation for all supported platforms
- **Migration**: Maintain backwards compatibility throughout transition

## Conclusion

This architecture enhances an already sophisticated MCP Server system with structured feedback capabilities. The existing implementation provides advanced loop management that exceeds many initial architectural goals, including configurable quality thresholds, automatic stagnation detection, and comprehensive score tracking.

**Key Insight**: Rather than rebuilding a sophisticated system, this architecture focuses on the missing piece - structured FSDD feedback integration. The current LoopState model already provides excellent foundation with advanced decision logic, score history tracking, and flexible state management.

**Value Proposition**: By building on the existing sophisticated foundation and adding structured feedback capabilities, we achieve the benefits of both proven loop management and comprehensive quality tracking. The evolutionary approach ensures no disruption to current workflows while enabling enhanced critic feedback and FSDD integration.

**Next Steps**: Begin enhancement implementation following the evolutionary specifications in [STRUCTURED_MEMORY_IMPLEMENTATION.md](STRUCTURED_MEMORY_IMPLEMENTATION.md), focusing on additive improvements that preserve existing sophistication.
