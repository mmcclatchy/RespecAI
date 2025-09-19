# /spec Command Specification

## Overview
The `/spec` command transforms strategic plans into detailed technical specifications. It orchestrates technical architecture design, research integration, and platform-specific specification creation through a quality-driven refinement loop.

## Command Metadata

**Name**: `/spec`  
**Type**: User-invoked workflow command  
**Phase**: Technical Specification (Phase 2 of 4)  
**Model**: Claude Sonnet (default)  

## Invocation

### Who Invokes It
- **Primary**: End user via Claude Code CLI
- **Context**: After successful completion of `/plan` command
- **Prerequisites**: Completed strategic plan document

### Trigger Format
```text
/spec [optional: specific technical area focus]
```

## Workflow Position

```text
Strategic Plan → /spec → [spec-architect ↔ spec-critic loop] → Technical Specification
                              ↓
                    Research identification
                              ↓
                    Platform-specific storage
                              ↓
                    Ready for /build command
```

### Position in End-to-End Flow
1. **Second Phase**: Follows strategic planning phase
2. **Precedes**: Implementation planning (`/build`) phase
3. **Dependencies**: Requires completed strategic plan
4. **Output Used By**: `/build` command and `build-planner` agent

## Primary Responsibilities

### Core Tasks
1. **Initialize Technical Design Process**
   - Retrieve strategic plan from previous phase
   - Launch `spec-architect` agent for technical architecture
   - Initialize MCP refinement loop for spec phase

2. **Coordinate Architecture Development**
   - Guide `spec-architect` through technical design decisions
   - Integrate existing documentation from archive
   - Identify external research requirements

3. **Manage Quality Assessment Loop**
   - Pass specifications to `spec-critic` for evaluation
   - Handle MCP Server refinement decisions
   - Iterate until quality threshold achieved

4. **Research Integration Management**
   - Catalog existing documentation paths
   - Identify gaps requiring external research
   - Create Research Requirements section in specification

5. **Platform-Specific Storage**
   - Determine active platform (Linear/GitHub/Markdown)
   - Use platform-appropriate tools for specification storage
   - Maintain platform-agnostic content structure

## Orchestration Pattern

### Agent Coordination Flow
```text
Main Agent (via /spec)
    │
    ├── 1. Initialize MCP Loop
    │   └── mcp_tool: initialize_refinement_loop(loop_type='spec')
    │
    ├── 2. Retrieve Strategic Plan
    │   └── mcp_tool: get_project_plan_markdown(plan_loop_id) or access user input
    │
    ├── 3. Technical Design Loop
    │   ├── Task: spec-architect (architecture + research identification → markdown)
    │   ├── mcp_tool: store_technical_spec(spec_loop_id, technical_spec_markdown)
    │   ├── Task: spec-critic (quality assessment → CriticFeedback)
    │   ├── mcp_tool: store_critic_feedback(critic_feedback_markdown)
    │   └── mcp_tool: decide_loop_next_action(spec_loop_id, quality_score)
    │
    ├── 4. Handle Loop Decision
    │   ├── IF "refine" → Pass structured feedback to spec-architect
    │   ├── IF "complete" → Finalize TechnicalSpec model and proceed
    │   └── IF "user_input" → Request technical clarification with feedback context
    │
    └── 5. Store Specification & Prepare for Build
        ├── mcp_tool: get_technical_spec_markdown(spec_loop_id)
        └── TechnicalSpec ready for /build command
```

### Data Flow Between Components
- **Main Agent → MCP Server**: `get_project_plan_markdown(plan_loop_id)` - Retrieve strategic plan
- **Main Agent → spec-architect**: Strategic plan + technical context
- **spec-architect → Main Agent**: Technical specification with research needs (markdown)
- **Main Agent → MCP Server**: `store_technical_spec(spec_loop_id, technical_spec_markdown)` - Create TechnicalSpec model
- **Main Agent → spec-critic**: TechnicalSpec for FSDD assessment
- **spec-critic → Main Agent**: Structured CriticFeedback (markdown format)
- **Main Agent → MCP Server**: `store_critic_feedback(feedback_markdown)` - Store feedback model
- **Main Agent → MCP Server**: `decide_loop_next_action(spec_loop_id, quality_score)` - Decision logic
- **MCP Server → Main Agent**: Next action (refine/complete/user_input) with loop state
- **Main Agent → MCP Server**: `get_technical_spec_markdown(spec_loop_id)` - Final retrieval for /build

## Quality Gates

### Success Criteria
- **Quality Threshold**: 85% (configurable via `FSDD_LOOP_SPEC_THRESHOLD`)
- **Maximum Iterations**: 5 (configurable via `FSDD_LOOP_SPEC_MAX_ITERATIONS`)
- **Improvement Threshold**: 5 points minimum between iterations

### FSDD Assessment Points
The spec-critic evaluates technical specifications against:
1. **Technical Completeness** - All components specified
2. **Architecture Clarity** - Design decisions documented
3. **Integration Points** - External systems identified
4. **Data Models** - Structure and relationships defined
5. **Security Design** - Security considerations addressed
6. **Performance Targets** - Metrics and benchmarks specified
7. **Scalability Plan** - Growth patterns considered
8. **Testing Strategy** - Validation approach defined
9. **Deployment Architecture** - Infrastructure specified
10. **Monitoring Plan** - Observability defined
11. **Documentation Requirements** - Knowledge capture planned
12. **Technology Stack** - Tools and frameworks justified

## Research Integration

### Research Identification Process
```text
spec-architect performs:
1. Archive Scanning
   - Execute: research-advisor-archive-scan.sh
   - Search: ~/.claude/best-practices/*.md
   - Catalog: Relevant existing documents

2. Gap Analysis
   - Compare: Required knowledge vs available
   - Identify: Missing technical guidance
   - Document: External research needs

3. Research Requirements Section
   - Format: Structured list in specification
   - Content: Mix of Read paths and research prompts
```

### Research Requirements Format
```markdown
## Research Requirements

### Existing Documentation
- Read: ~/.claude/best-practices/react-hooks-patterns.md
- Read: ~/.claude/best-practices/postgresql-optimization.md

### External Research Needed
- Synthesize: Best practices for integrating React with GraphQL in 2025
- Synthesize: PostgreSQL connection pooling strategies for microservices
```

## Platform-Specific Behavior

### Platform Detection
```python
# Main Agent determines active platform
platform = get_active_platform()  # Returns: 'linear' | 'github' | 'markdown'
```

### Linear Platform
- **Storage Tool**: `mcp__linear-server__create_issue`
- **Specification Location**: Linear issue with detailed description
- **Research Section**: Added as structured comment
- **Labels**: Technical specification, architecture
- **Assignee**: Technical lead (if configured)

### GitHub Platform  
- **Storage Tool**: `mcp__github__create_issue`
- **Specification Location**: GitHub issue with technical details
- **Research Section**: Included in issue body
- **Labels**: specification, technical-design
- **Milestone**: Current sprint/release

### Markdown Platform
- **Storage Tool**: `Write`
- **Specification Location**: `docs/specs/[timestamp]-[project].md`
- **Research Section**: Embedded in document
- **Version Control**: Git-tracked changes
- **Cross-references**: Links to strategic plan

## Structured Data Models

### TechnicalSpec Model
The `/spec` command creates and stores structured TechnicalSpec models:
```python
class TechnicalSpec(MCPModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    phase_name: str = 'Unnamed Specification'
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
    spec_status: SpecStatus = SpecStatus.DRAFT
```

### CriticFeedback Model
Quality assessments stored as structured feedback:
```python
class CriticFeedback(MCPModel):
    loop_id: str
    critic_agent: CriticAgent.SPEC_CRITIC
    iteration: int
    overall_score: int  # 0-100
    assessment_summary: str
    detailed_feedback: str
    key_issues: list[str]
    recommendations: list[str]
    timestamp: datetime
```

## Input/Output Specifications

### Input Requirements
- **Strategic Plan**: ProjectPlan model from `/plan` phase via `get_project_plan_markdown()`
- **Technical Focus**: Optional area of emphasis
- **Format**: TechnicalSpec markdown structure

### Output Specifications
- **Primary Output**: TechnicalSpec model stored in MCP Server + technical specification markdown
- **Structured Storage**: TechnicalSpec with validated fields for `/build` consumption
- **Markdown Format**:
  ```markdown
  # Technical Specification: [Phase Name]

  ## Overview
  ### Objectives / Scope / Dependencies / Deliverables

  ## System Design
  ### Architecture / Technology Stack

  ## Implementation
  ### Functional Requirements / Non-Functional Requirements
  ### Development Plan / Testing Strategy

  ## Additional Details
  ### Research Requirements / Success Criteria / Integration Context

  ## Metadata
  ### Status
  ```

## Error Handling

### Common Failure Scenarios

1. **Missing Strategic Plan**
   - **Error**: "No strategic plan found"
   - **Recovery**: Request plan location or invoke `/plan`
   - **User Message**: "Please provide the strategic plan or run /plan first"

2. **Platform Detection Failure**
   - **Error**: "Cannot determine active platform"
   - **Recovery**: Fallback to Markdown, prompt for `/spec-setup`
   - **User Message**: "Platform not configured. Using Markdown. Run /spec-setup to configure."

3. **Research Archive Unavailable**
   - **Error**: "Cannot access best-practices archive"
   - **Recovery**: Continue without archive, note in research section
   - **User Message**: "Archive unavailable. External research will cover all topics."

4. **Quality Threshold Not Met**
   - **Error**: "Specification quality below threshold after max iterations"
   - **Recovery**: Present specification with quality warnings
   - **User Message**: "Specification quality: [score]%. Key gaps: [areas]. Proceed with caution."

5. **Platform Storage Failure**
   - **Error**: "Failed to store specification in [platform]"
   - **Recovery**: Save to local Markdown as backup
   - **User Message**: "Platform storage failed. Saved locally to: [path]"

## Example Usage

### Typical Invocation
```text
User: /spec

Main Agent: I'll transform your strategic plan into a detailed technical specification. Let me retrieve the plan and begin the architecture design process.

[Retrieves strategic plan]
[Invokes spec-architect agent]

spec-architect: Analyzing the strategic plan for the AI-powered customer feedback system. Let me design the technical architecture.

[Searches archive for relevant patterns]
Found: ~/.claude/best-practices/ml-pipeline-patterns.md
Found: ~/.claude/best-practices/event-driven-architecture.md

Designing architecture with:
- Microservices for scalability
- Event-driven processing for real-time analysis
- ML pipeline for classification

[Creates technical specification]

[Main Agent invokes spec-critic]
[Score: 78% - needs more detail on data models]

[Refinement cycle continues]

spec-architect: Adding detailed data models and entity relationships...

[Final score: 88%]

Main Agent: Technical specification completed! 
- Quality score: 88%
- Platform: Linear
- Issue created: SPEC-1234
- Research requirements documented

The specification is ready for implementation planning. Use /build to proceed.
```

### With Technical Focus
```text
User: /spec focus on API design and integration patterns

Main Agent: I'll create a technical specification with special emphasis on API design and integration patterns.

[Process continues with focused attention on specified areas]
```

## Implementation Notes

### Key Considerations for Claude Code

1. **Archive Integration**
   - Execute shell scripts for archive scanning
   - Parse results to identify relevant documents
   - Maintain list of found documentation paths

2. **Research Documentation**
   - Clearly separate existing docs from needed research
   - Use consistent format for research prompts
   - Include year (2025) in research prompts for current practices

3. **Platform Abstraction**
   - Use platform-agnostic content structure
   - Apply platform-specific formatting only at storage time
   - Maintain ability to export/convert between platforms

4. **Quality Feedback Integration**
   - Present critic feedback constructively
   - Focus refinements on lowest-scoring areas
   - Preserve strong sections during iterations

5. **Context Management**
   - Summarize strategic plan for efficiency
   - Focus on technical decisions in later iterations
   - Prune redundant research requirements

## Dependencies and Integration Points

### Required Components
- **MCP Server**: Loop state management and decision logic
- **spec-architect agent**: Technical design and research identification
- **spec-critic agent**: Quality assessment and feedback
- **Platform tools**: Linear/GitHub/Markdown storage

### MCP Tools Used
**Technical Specification Workflow:**
- `initialize_refinement_loop(loop_type='spec')` - Create specification refinement loop
- `get_project_plan_markdown(plan_loop_id)` - Retrieve strategic plan from /plan phase
- `store_technical_spec(spec_loop_id, technical_spec_markdown)` - Store TechnicalSpec model
- `store_critic_feedback(feedback_markdown)` - Store structured CriticFeedback
- `decide_loop_next_action(spec_loop_id, current_score)` - Loop decision engine
- `get_technical_spec_markdown(spec_loop_id)` - Retrieve final specification for /build
- `get_loop_status(spec_loop_id)` - Monitor loop state (optional)
- `get_feedback_history(spec_loop_id, count)` - Retrieve recent feedback for context
- `list_technical_specs(count)` - List existing specifications

### Shell Scripts
- `~/.claude/scripts/research-advisor-archive-scan.sh`

### Environment Variables
- `FSDD_LOOP_SPEC_THRESHOLD`: Quality threshold (default: 85)
- `FSDD_LOOP_SPEC_MAX_ITERATIONS`: Maximum iterations (default: 5)

## Success Metrics

### Quantitative Metrics
- **Quality Score**: Target ≥85%
- **Iterations to Complete**: Target ≤3
- **Archive Hit Rate**: Target >60% of research needs
- **Platform Storage Success**: Target >99%

### Qualitative Metrics
- **Technical Completeness**: All architectural decisions documented
- **Research Coverage**: All knowledge gaps identified
- **Implementation Ready**: Sufficient detail for development
- **Platform Integration**: Seamless storage and retrieval

## Related Documentation
- **Previous Phase**: [`/plan` Command Specification](plan.md)
- **Next Phase**: [`/build` Command Specification](build.md)
- **Primary Agent**: [`spec-architect` Agent Specification](../agents/spec-architect.md)
- **Quality Agent**: [`spec-critic` Agent Specification](../agents/spec-critic.md)
- **Platform Setup**: [`/spec-setup` Command Specification](spec-setup.md)
