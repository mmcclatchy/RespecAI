# /plan-roadmap Command Specification

## Overview
The `/plan-roadmap` command transforms strategic plans into phased implementation roadmaps. It orchestrates the decomposition of high-level business objectives into discrete, spec-ready implementation phases through quality-driven refinement.

## Command Metadata

**Name**: `/plan-roadmap`  
**Type**: Implementation planning orchestrator  
**Phase**: Strategic Planning → Implementation Roadmap (Bridge to Technical Specification)  
**Model**: Claude Sonnet (default)

## Invocation

### Who Invokes It
- **Primary**: End user via Claude Code CLI
- **Context**: After successful completion of `/plan` command
- **Prerequisites**: Completed strategic plan document with structured objectives

### Trigger Format
```text
/plan-roadmap [optional: phasing-preferences]
```

### Parameters
- **phasing-preferences**: Optional user guidance on phase boundaries (e.g., "2-week sprints", "MVP in 3 months")

## Workflow Position

```text
Strategic Plan → /plan-roadmap → [plan-decomposer ↔ roadmap-critic loop] → Implementation Roadmap
                                           ↓                                          ↓
                                   Phase Breakdown                          Quality Assessment
                                           ↓                                          ↓
                                   Dependency Mapping                      Refinement Decision
                                           ↓
                                    Ready for /spec calls (per phase)
```

### Position in End-to-End Flow
1. **Bridge Phase**: Connects strategic planning to technical specification
2. **Precedes**: Multiple `/spec` command invocations (one per phase)
3. **Dependencies**: Requires completed strategic plan and objectives analysis
4. **Output Used By**: `/spec` command for phase-specific technical specifications

## Primary Responsibilities

### Core Tasks

1. **Strategic Plan Context Gathering**
   - Access completed strategic plan from `/plan` command output
   - Retrieve structured objectives from plan-analyst processing
   - Capture optional user phasing preferences
   - Establish baseline for roadmap generation

2. **Implementation Decomposition Orchestration**
   - Initialize MCP refinement loop for roadmap generation
   - Launch `plan-decomposer` agent for phase breakdown
   - Manage iterative roadmap development process
   - Coordinate phase scoping and dependency mapping

3. **Quality Assessment Loop Management**
   - Invoke `roadmap-critic` agent for roadmap evaluation
   - Process quality scores and feedback through MCP Server
   - Handle refinement decisions (refine/complete/user_input)
   - Monitor iteration count and improvement trends

4. **Refinement Cycle Coordination**
   - Route critic feedback to plan-decomposer for improvements
   - Maintain roadmap context across iterations
   - Manage stagnation detection and user escalation
   - Ensure MCP Server completion criteria before finishing

5. **Final Roadmap Preparation**
   - Validate completed roadmap structure and content
   - Prepare phase-specific contexts for downstream `/spec` calls
   - Document implementation sequence and dependencies
   - Ensure smooth handoff to technical specification phase

## Orchestration Pattern

### Agent Coordination Flow
```text
Main Agent (via /plan-roadmap)
    │
    ├── 1. Initialize Roadmap MCP Loop
    │   └── mcp_tool: initialize_refinement_loop(loop_type='roadmap')
    │
    ├── 2. Strategic Plan Context Gathering
    │   ├── Access strategic plan from /plan output
    │   ├── Retrieve structured objectives from plan-analyst
    │   └── Capture phasing preferences from user
    │
    ├── 3. Roadmap Generation Loop
    │   ├── Task: plan-decomposer (phase breakdown)
    │   ├── Task: roadmap-critic (quality assessment → score)
    │   └── mcp_tool: decide_loop_next_action(roadmap_loop_id, score)
    │
    ├── 4. Handle Loop Decision
    │   ├── IF "refine" → Pass feedback to plan-decomposer
    │   ├── IF "complete" → Proceed to final preparation
    │   └── IF "user_input" → Request phasing clarification
    │
    └── 5. Final Roadmap Preparation
        └── Ready for multiple /spec command invocations
```

### Data Flow Between Agents
**Roadmap Generation Phase:**
- **Main Agent → plan-decomposer**: Strategic plan + objectives + preferences
- **plan-decomposer → Main Agent**: Implementation roadmap (markdown)
- **Main Agent → roadmap-critic**: Roadmap document for assessment
- **roadmap-critic → Main Agent**: Quality score (0-100) and feedback
- **Main Agent → MCP Server**: Score for roadmap loop decision logic
- **MCP Server → Main Agent**: Next action decision (refine/complete/user_input)

## Input/Output Specifications

### Input Requirements
- **Strategic Plan**: Complete strategic plan document from `/plan` command
- **Structured Objectives**: Business objectives analysis from plan-analyst processing
- **Phasing Preferences**: Optional user guidance on phase structure and timing

### Output Specifications
- **Primary Output**: Implementation roadmap document (markdown format)
- **Structure**:
  ```markdown
  # Implementation Roadmap: [Project Name]
  
  ## Overview
  [Phasing strategy and implementation approach]
  
  ## Phase Summary  
  [Total phases, duration, critical path]
  
  ## Phase 1: [Foundation/Core]
  - Duration, Priority, Dependencies
  - Scope, Deliverables, Technical Focus
  - Success Criteria, Spec Context
  
  ## Phase 2: [Core Features]
  [Same structure as Phase 1]
  
  ## Risk Mitigation
  [Cross-phase risks and strategies]
  
  ## Integration Strategy
  [How phases connect and build upon each other]
  ```

## Quality Assessment Process

### MCP Server Integration
The command coordinates with MCP Server for quality-driven refinement:

1. **Score Submission**: Pass roadmap-critic scores to MCP Server
2. **Decision Handling**: Process MCP Server responses:
   - **"refine"**: Continue improvement cycle with critic feedback
   - **"complete"**: Accept current roadmap and proceed
   - **"user_input"**: Request additional user guidance
3. **Loop Management**: MCP Server manages iteration counts and improvement tracking

### Assessment Criteria
The roadmap-critic evaluates roadmaps against these areas:
1. **Phase Scoping** - Each phase delivers user value within reasonable timeframe
2. **Dependency Management** - Clear sequencing and prerequisites without circular dependencies
3. **Scope Clarity** - Specific deliverables and explicit boundaries per phase
4. **Implementation Readiness** - Sufficient detail and context for `/spec` command processing
5. **Resource Balance** - Realistic complexity distribution across phases
6. **Risk Distribution** - Critical items appropriately phased with mitigation strategies
7. **Timeline Feasibility** - Realistic duration estimates and milestone definitions
8. **Success Criteria** - Clear, measurable outcomes for each phase

## Output Structure

### Implementation Roadmap Format

```markdown
# Implementation Roadmap: [Project Name]

## Overview
[Summary of phasing strategy and approach]

## Phase Summary
- **Total Phases**: [Number]
- **Estimated Duration**: [Overall timeline]
- **Critical Path**: [Key dependencies]

## Phase 1: [Foundation/Core/Name]
**Duration**: [Timeframe]
**Priority**: Critical/High/Medium
**Dependencies**: None

### Scope
[Clear description of what this phase includes]

### Deliverables
- [Specific feature or capability]
- [Specific feature or capability]
- [Specific feature or capability]

### Technical Focus
[Key technical areas for spec development]

### Success Criteria
- [Measurable outcome]
- [Measurable outcome]

### Spec Context
[Information needed for /spec command]
- Focus Areas: [Technical domains]
- Key Decisions: [Architecture choices needed]
- Research Needs: [Knowledge gaps to address]

## Phase 2: [Name]
**Duration**: [Timeframe]
**Priority**: High/Medium
**Dependencies**: Phase 1 completion

### Scope
[Clear description]

### Deliverables
[Feature list]

### Technical Focus
[Key areas]

### Success Criteria
[Measurable outcomes]

### Spec Context
[/spec guidance]

[Additional phases following same structure]

## Risk Mitigation
[Cross-phase risks and mitigation strategies]

## Integration Points
[How phases connect and dependencies between them]
```

## Agent Coordination

### plan-decomposer Agent
- **Input**: Strategic plan + structured objectives
- **Output**: Multi-phase implementation roadmap
- **Focus**: Breaking down requirements into implementable chunks

### roadmap-critic Agent
- **Input**: Implementation roadmap
- **Output**: Quality score + improvement feedback
- **Focus**: Validating phase scoping and dependencies

## Error Handling

### Missing Strategic Plan
```text
IF no strategic plan available:
  Display: "No strategic plan found. Please run /plan command first."
  Suggest: "/plan [project-name] to create strategic plan"
  Exit gracefully
```

### Invalid Plan Format
```text
IF strategic plan format unrecognizable:
  Attempt: Parse available sections
  Continue: With partial information
  Note: Document limitations in roadmap
```

### Agent Failures
```text
IF plan-decomposer fails:
  Retry: Once with simplified input
  Fallback: Create basic 3-phase roadmap
  Document: Limitations in output

IF roadmap-critic fails:
  Continue: Without quality loop
  Note: "Manual review recommended"
  Provide: Best-effort roadmap
```

### MCP Loop Failures
```text
IF loop initialization fails:
  Continue: Single-pass roadmap generation
  Skip: Refinement cycles
  Note: Quality assessment unavailable
```

## Example Usage

### Typical Invocation
```text
User: /plan-roadmap

Main Agent: I'll transform your strategic plan into a phased implementation roadmap. Let me analyze the plan and break it down into manageable phases.

[Invokes plan-decomposer agent]

plan-decomposer: Analyzing strategic plan for AI-powered feedback system. Creating 4-phase roadmap based on dependencies and value delivery...

[Main Agent invokes roadmap-critic for quality assessment]
[Score: 73% - needs better phase scoping and risk distribution]

[Main Agent receives "refine" decision from MCP Server]

[Refinement continues until MCP Server signals completion]

[Final score: 87% - Main Agent receives "complete" decision]

Main Agent: Implementation roadmap completed successfully! Quality score: 87%. The roadmap defines 4 phases over 12 weeks, with each phase delivering user value. You can now use /spec for individual phase specifications.
```

### With Phasing Preferences
```text
User: /plan-roadmap "prefer 2-week sprints, MVP by month 3"

Main Agent: Creating roadmap with 2-week sprint phases targeting MVP delivery in 3 months...
```

### Required Components
- **MCP Server**: Loop state management and decision logic
- **plan-decomposer agent**: Phase breakdown and roadmap generation
- **roadmap-critic agent**: Quality assessment and feedback

### MCP Tools Used
**Roadmap Generation Phase:**
- `initialize_refinement_loop(loop_type='roadmap')`
- `decide_loop_next_action(roadmap_loop_id, current_score)`
- `get_loop_status(roadmap_loop_id)` (optional for monitoring)

## MCP Server Response Handling

### Decision Processing
The command handles three MCP Server responses:

1. **refine**:
   - Pass critic feedback to plan-decomposer for improvements
   - Continue refinement cycle with updated roadmap
   - Maintain context across iterations

2. **complete**:
   - Accept current roadmap as final
   - Prepare phase-specific contexts for downstream `/spec` calls  
   - Present completed roadmap to user

3. **user_input**:
   - Request additional user guidance on phasing preferences
   - Incorporate user feedback into next refinement cycle
   - Continue with enhanced requirements

## Integration Notes

### With /plan Command
- Consumes strategic plan output
- Uses structured objectives from plan-analyst
- Maintains context from planning phase

### With /spec Command
- Provides phase-specific context for targeted specification
- Enables incremental development through phased specs
- Supports multiple `/spec` cycles per roadmap

### With /build Command  
- Enables phased implementation approach
- Supports iterative delivery model
- Facilitates progress tracking across phases

## Platform-Specific Behavior

### Platform-Agnostic Design
The `/plan-roadmap` command operates identically across all platforms (Linear, GitHub, Markdown) as it produces platform-independent roadmaps. Platform-specific behavior only emerges in subsequent `/spec` and `/build` phases.

## Related Documentation
- **Previous Phase**: [`/plan` Command Specification](plan.md)
- **Primary Agent**: [`plan-decomposer` Agent Specification](../agents/plan-decomposer.md)
- **Quality Agent**: [`roadmap-critic` Agent Specification](../agents/roadmap-critic.md)
- **Next Phase**: [`/spec` Command Specification](spec.md)
- **MCP Tools**: [MCP Tools Specification](../MCP_TOOLS_SPECIFICATION.md)
