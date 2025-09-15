def generate_plan_roadmap_command_template(
    get_project_plan_tool: str,
    update_project_plan_tool: str,
    create_spec_tool: str,
    get_spec_tool: str,
    update_spec_tool: str,
) -> str:
    return f"""---
allowed-tools:
  - Task(plan-roadmap)
  - Task(roadmap-critic)
  - {get_project_plan_tool}
  - {update_project_plan_tool}
  - {create_spec_tool}
  - {get_spec_tool}
  - {update_spec_tool}
  - mcp__loop_state__initialize_refinement_loop
  - mcp__loop_state__decide_loop_next_action
  - mcp__loop_state__get_loop_status
argument-hint: [project-plan-name] [optional: phasing-preferences]
description: Transform strategic plans into phased implementation roadmaps through quality-driven refinement
---

# /plan-roadmap Command: Implementation Roadmap Orchestration

## Overview
Orchestrate the transformation of strategic plans into discrete, implementable phase roadmaps. Bridge strategic planning to technical specification through quality-driven decomposition and refinement.

## Primary Responsibilities

### 1. Strategic Plan Context Gathering
- Access completed strategic plan from /plan command output
- Retrieve structured objectives from plan-analyst processing
- Capture optional user phasing preferences
- Establish baseline context for roadmap generation

### 2. Implementation Decomposition Orchestration
- Initialize MCP refinement loop for roadmap generation
- Launch plan-roadmap agent for phase breakdown
- Manage iterative roadmap development process
- Coordinate phase scoping and dependency mapping

### 3. Quality Assessment Loop Management
- Invoke roadmap-critic agent for roadmap evaluation
- Process quality scores and feedback through MCP Server
- Handle refinement decisions (refine/complete/user_input)
- Monitor iteration progress and improvement trends

### 4. Final Roadmap Preparation
- Validate completed roadmap structure and content
- Prepare phase-specific contexts for downstream /spec calls
- Document implementation sequence and dependencies
- Ensure smooth handoff to technical specification phase

### 5. Spec Scaffolding Orchestration
- Create initial scaffolded specs for each implementation phase
- Apply phase-specific context to spec templates
- Use platform-appropriate tools for spec creation
- Link specs to roadmap for /spec command discovery

## Orchestration Pattern

```text
Main Agent (via /plan-roadmap)
    │
    ├── 1. Initialize Roadmap MCP Loop
    │   └── mcp__loop_state__initialize_refinement_loop(loop_type='roadmap')
    │
    ├── 2. Strategic Plan Context Gathering
    │   ├── Read strategic plan from /plan output
    │   ├── Extract structured objectives from plan-analyst
    │   └── Capture phasing preferences from user input
    │
    ├── 3. Roadmap Generation Loop
    │   ├── Task: plan-roadmap (phase breakdown)
    │   ├── Task: roadmap-critic (quality assessment → score)
    │   └── mcp__loop_state__decide_loop_next_action(roadmap_loop_id, score)
    │
    ├── 4. Handle Loop Decision
    │   ├── IF "refine" → Pass feedback to plan-roadmap
    │   ├── IF "complete" → Proceed to final preparation
    │   └── IF "user_input" → Request phasing clarification
    │
    ├── 5. Final Roadmap Preparation
    │   └── Validate roadmap and prepare phase contexts
    │
    └── 6. Spec Scaffolding
        └── Create initial specs for each phase → Ready for /spec completion
```

## Implementation Instructions

### Step 1: Strategic Plan Context Gathering

Initialize roadmap generation workflow:

```
# Gather strategic plan context
PHASING_PREFERENCES = [User provided phasing preferences or empty]
STRATEGIC_PLAN_CONTENT = Read: [Locate and read strategic plan document from /plan output]
STRUCTURED_OBJECTIVES = [Extract plan-analyst objectives from strategic plan sections]

# Establish context variables
PROJECT_NAME = [Extract from strategic plan title]
BUSINESS_OBJECTIVES = [Extract from strategic plan Business Objectives section]
SUCCESS_CRITERIA = [Extract from strategic plan Success Criteria section]
TIMELINE_CONSTRAINTS = [Extract from PHASING_PREFERENCES and strategic plan]
```

### Step 2: Initialize Roadmap Generation Loop

Set up MCP-managed quality refinement loop:

```
# Initialize roadmap refinement loop
ROADMAP_LOOP_ID = mcp__loop_state__initialize_refinement_loop:
  loop_type: "roadmap"

# Prepare roadmap input context
ROADMAP_CONTEXT = Combine:
  Strategic Plan: ${{STRATEGIC_PLAN_CONTENT}}
  Structured Objectives: ${{STRUCTURED_OBJECTIVES}}
  Phasing Preferences: ${{PHASING_PREFERENCES}}
  Project Name: ${{PROJECT_NAME}}
```

### Step 3: Phase Breakdown Generation

Invoke plan-roadmap for roadmap creation:

```
# Generate initial roadmap
Invoke plan-roadmap agent with this input:
${{ROADMAP_CONTEXT}}

Expected Output Format:
- Implementation roadmap in markdown format
- 3-7 discrete implementation phases
- Phase dependencies and sequencing
- Deliverables and success criteria per phase
- Technical focus areas for /spec preparation

# Capture roadmap output
CURRENT_ROADMAP = [plan-roadmap output: complete implementation roadmap]
```

### Step 4: Roadmap Quality Assessment

Evaluate roadmap quality through roadmap-critic:

```
# Assess roadmap quality
Invoke roadmap-critic agent with this input:
${{CURRENT_ROADMAP}}

Expected Output Format:
- Overall Quality Score: [0-100 numerical value]
- Priority Improvements: [List of specific actionable suggestions]
- Strengths: [List of well-executed areas to preserve]

# Extract assessment results
ROADMAP_QUALITY_SCORE = [roadmap-critic output: Overall Quality Score (0-100)]
ROADMAP_IMPROVEMENT_FEEDBACK = [roadmap-critic output: Priority Improvements and suggestions]
ROADMAP_STRENGTHS = [roadmap-critic output: Strengths to preserve]
```

### Step 5: MCP Loop Decision Processing

Submit quality score for MCP decision:

```
# Submit score to MCP Server for decision
ROADMAP_DECISION = mcp__loop_state__decide_loop_next_action:
  loop_id: ${{ROADMAP_LOOP_ID}}
  current_score: ${{ROADMAP_QUALITY_SCORE}}

# Handle MCP Server decisions
IF ROADMAP_DECISION == "complete":
  → Proceed to Step 6: Final Roadmap Preparation

IF ROADMAP_DECISION == "refine":
  → Return to Step 3 with refined context:
  
  Invoke plan-roadmap agent with this input:
  
  Previous Roadmap: ${{CURRENT_ROADMAP}}
  Quality Feedback: ${{ROADMAP_IMPROVEMENT_FEEDBACK}}
  Preserve Strengths: ${{ROADMAP_STRENGTHS}}
  Iteration: [increment counter]
  
  Expected Output Format: Refined implementation roadmap addressing feedback

IF ROADMAP_DECISION == "user_input":
  → Escalate roadmap stagnation:
  
  Present to user:
  "Roadmap development has reached quality plateau at ${{ROADMAP_QUALITY_SCORE}}%.
  Key gaps identified: [Priority Improvements list]
  
  Please provide guidance on:
  1. [Specific phasing approach preferences]
  2. [Timeline or scope adjustments needed]
  3. [Accept current roadmap quality: yes/no]"
```

### Step 6: Final Roadmap Preparation

Complete roadmap generation and prepare for /spec handoff:

```
# Validate final roadmap structure
FINAL_ROADMAP_VALIDATION = Verify:
- All phases have clear scope and deliverables
- Dependencies properly sequenced
- Technical focus areas identified for each phase
- Success criteria measurable and specific
- Integration points documented

# Prepare phase contexts for /spec commands
PHASE_CONTEXTS = Extract from CURRENT_ROADMAP:
  For each phase:
    - Phase name and scope
    - Technical focus areas
    - Key architectural decisions needed
    - Research requirements
    - Success criteria and deliverables

# Store roadmap completion status
ROADMAP_COMPLETION_STATUS = Generate:
  - Quality score: ${{ROADMAP_QUALITY_SCORE}}%
  - Total phases: [X] phases
  - Timeline: [Y] timeline
  - Phase contexts prepared for spec scaffolding
```

### Step 7: Spec Scaffolding

Create initial scaffolded specs for each implementation phase:

```
# Load spec template for scaffolding
PHASE_SPEC_TEMPLATE = Read: services/templates/specs/phase_spec_template.md

# Create scaffolded spec for each phase
For each phase in PHASE_CONTEXTS:

  # Extract phase information
  PHASE_NAME = [phase.name]
  PHASE_OBJECTIVES = [phase.objectives]
  PHASE_SCOPE = [phase.scope]
  PHASE_DELIVERABLES = [phase.deliverables]
  PHASE_DEPENDENCIES = [phase.dependencies]
  TECHNICAL_FOCUS_AREAS = [phase.technical_focus]
  SUCCESS_CRITERIA = [phase.success_criteria]
  INTEGRATION_CONTEXT = [phase.integration_points]
  RESEARCH_REQUIREMENTS = [phase.research_needs]
  
  # Generate scaffolded spec content
  SCAFFOLDED_SPEC_CONTENT = Apply PHASE_SPEC_TEMPLATE with:
    - PHASE_NAME: ${{PHASE_NAME}}
    - PHASE_OBJECTIVES: ${{PHASE_OBJECTIVES}}
    - PHASE_SCOPE: ${{PHASE_SCOPE}}
    - PHASE_DELIVERABLES: ${{PHASE_DELIVERABLES}}
    - PHASE_DEPENDENCIES: ${{PHASE_DEPENDENCIES}}
    - TECHNICAL_FOCUS_AREAS: ${{TECHNICAL_FOCUS_AREAS}}
    - SUCCESS_CRITERIA: ${{SUCCESS_CRITERIA}}
    - INTEGRATION_CONTEXT: ${{INTEGRATION_CONTEXT}}
    - RESEARCH_REQUIREMENTS: ${{RESEARCH_REQUIREMENTS}}
    - CREATION_DATE: [current date]
    - PHASE_NUMBER: [phase index]
    - TOTAL_PHASES: [total phase count]
    - PROJECT_NAME: ${{PROJECT_NAME}}
  
  # Create scaffolded spec using platform tool
  SPEC_CREATION_RESULT = {create_spec_tool}:
    identifier: "${{PROJECT_NAME}}-Phase-${{PHASE_NUMBER}}-${{PHASE_NAME}}"
    title: "Technical Specification: ${{PHASE_NAME}}"
    content: ${{SCAFFOLDED_SPEC_CONTENT}}
    status: "Specification In Progress"
    phase: ${{PHASE_NUMBER}}
    roadmap_reference: ${{PROJECT_NAME}} Implementation Roadmap

# Present completion with spec scaffolding results
FINAL_COMPLETION_MESSAGE = Generate:
  "Implementation roadmap completed successfully! 
  Quality score: ${{ROADMAP_QUALITY_SCORE}}%. 
  
  Roadmap Summary:
  - [X] phases over [Y] timeline
  - Each phase delivers measurable user value
  - Clear dependencies and sequencing defined
  
  Spec Scaffolding Complete:
  - [X] initial technical specifications created
  - Each spec provides structure and guidance for /spec completion
  - Specs ready for detailed technical development
  
  Next Steps:
  1. Use '/spec [phase-name]' to complete individual phase specifications
  2. Begin with Phase 1: [first-phase-name]
  3. Each completed spec enables targeted implementation planning"
```

## Error Handling

### Standardized Error Response Format
All error scenarios return structured responses:

```json
{
        'error_type': "plan_not_found|invalid_plan_format|agent_failure|mcp_loop_failure|spec_scaffolding_failure|stagnation_detected",
  "error_message": "Detailed error description",
  "recovery_action": "Specific recovery steps taken",
  "user_guidance": "Clear instructions for user",
  "partial_output": "Any salvageable roadmap work"
}
```

### Error Scenario Implementations

#### 1. Strategic Plan Not Found
```
IF no strategic plan available:
  ERROR_RESPONSE = {
        'error_type': "plan_not_found",
    "error_message": "No strategic plan found. /plan command must be completed first.",
    "recovery_action": "Prompting user to run /plan command",
    "user_guidance": "Please run '/plan [project-name]' to create strategic plan first",
    "partial_output": "No roadmap generated"
  }
  → Request /plan command completion before proceeding
```

#### 2. Invalid Plan Format
```
IF strategic plan format unrecognizable:
  ERROR_RESPONSE = {
        'error_type': "invalid_plan_format",
    "error_message": "Strategic plan format not recognized or incomplete",
    "recovery_action": "Attempting to parse available sections",
    "user_guidance": "Strategic plan may be incomplete. Proceeding with available information.",
    "partial_output": "Partial roadmap based on available plan sections"
  }
  → Continue with available information, note limitations in roadmap
```

#### 3. Agent Failures
```
IF plan-roadmap fails:
  ERROR_RESPONSE = {
        'error_type': "agent_failure",
    "error_message": "Phase breakdown generation failed",
    "recovery_action": "Creating basic 3-phase roadmap fallback",
    "user_guidance": "Using simplified roadmap structure. Manual refinement recommended.",
    "partial_output": "Basic 3-phase roadmap: Foundation → Core Features → Enhancement"
  }
  → Provide fallback 3-phase structure with manual review recommendation

IF roadmap-critic fails:
  ERROR_RESPONSE = {
        'error_type': "agent_failure", 
    "error_message": "Roadmap quality assessment failed",
    "recovery_action": "Continuing without quality loop",
    "user_guidance": "Roadmap generated without quality validation. Manual review recommended.",
    "partial_output": "Unvalidated roadmap from plan-roadmap"
  }
  → Present best-effort roadmap with manual review warning
```

#### 4. MCP Loop Failures
```
IF loop initialization fails:
  ERROR_RESPONSE = {
        'error_type': "mcp_loop_failure",
    "error_message": "MCP refinement loop initialization failed",
    "recovery_action": "Proceeding with single-pass roadmap generation",
    "user_guidance": "Quality refinement unavailable. Single-pass roadmap generated.",
    "partial_output": "Single-iteration roadmap without quality refinement"
  }
  → Generate roadmap without refinement cycles, note quality limitations
```

#### 5. Spec Scaffolding Failures
```
IF spec template loading or scaffolding fails:
  ERROR_RESPONSE = {
        'error_type': "spec_scaffolding_failure",
    "error_message": "Spec scaffolding creation failed for [X] of [Y] phases",
    "recovery_action": "Roadmap completed without initial spec scaffolding",
    "user_guidance": "Roadmap available. Create specs manually or use /spec command directly.",
    "partial_output": "Completed roadmap with [successful count] specs scaffolded"
  }
  → Present completed roadmap with spec scaffolding limitations noted

IF platform spec creation tool fails:
  ERROR_RESPONSE = {
        'error_type': "spec_scaffolding_failure", 
    "error_message": "Platform spec creation tool unavailable or failed",
    "recovery_action": "Roadmap completed with phase contexts prepared for manual spec creation",
    "user_guidance": "Use alternative spec creation method or contact platform administrator.",
    "partial_output": "Roadmap with phase contexts ready for spec development"
  }
  → Present roadmap with alternative spec creation guidance
```

## Expected Output Specifications

### Implementation Roadmap Structure
```markdown
# Implementation Roadmap: [Project Name]

## Overview
[Phasing strategy and implementation approach]

## Phase Summary
- **Total Phases**: [3-7 phases]
- **Estimated Duration**: [Overall timeline]
- **Critical Path**: [Key dependencies]

## Phase 1: [Foundation/Core Infrastructure]
**Duration**: [2-4 weeks]
**Priority**: Critical
**Dependencies**: None

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
**Focus Areas**: [Technical domains for /spec command]
**Key Decisions**: [Architecture choices needed]
**Research Needs**: [Knowledge gaps to address]
**Integration Points**: [External systems or APIs]

[Additional phases following same structure]

## Risk Mitigation
[Cross-phase risks and mitigation strategies]

## Integration Strategy
[How phases connect and build upon each other]
```

## Context Preservation Strategy

Maintain conversation flow while processing complex roadmap workflow:
- Complete conversation history passed to each agent invocation
- Technical assessments and loop decisions hidden from user interaction  
- Natural dialogue flow preserved despite multi-agent coordination
- Context summarization to manage size constraints across refinement cycles

## Success Metrics

### Quantitative Targets
- **Roadmap Quality Score**: Target determined by MCP Server thresholds
- **Phase Count**: 3-7 phases optimal for implementation readiness
- **Completion Rate**: >95% successful roadmap generation
- **Spec Scaffolding Success**: >90% phases with successful initial specs
- **User Escalation Rate**: <20% requiring manual intervention

### Qualitative Indicators
- **Implementation Readiness**: Each phase provides sufficient context for /spec completion
- **Spec Scaffolding Quality**: Initial specs provide clear structure and guidance
- **Value Delivery**: Each phase delivers measurable user value
- **Dependency Clarity**: Phase sequencing logical and well-documented
- **Scope Balance**: Realistic complexity distribution across phases

## Integration Notes

### With /plan Command
- Consumes strategic plan output as primary input
- Uses structured objectives from plan-analyst processing
- Maintains business context and success criteria from planning phase

### With /spec Command  
- Creates initial scaffolded specs with phase-specific context
- Provides structured templates for targeted technical specification completion
- Enables incremental development through phased specifications
- Supports multiple /spec cycles per roadmap (one per phase)
- Pre-populates research requirements and technical focus areas

### With /build Command
- Enables phased implementation approach through roadmap structure
- Supports iterative delivery model with clear phase boundaries
- Facilitates progress tracking across implementation phases

The implementation roadmap and scaffolded specifications are ready for technical development. All phases have clear scope, dependencies, and initial spec scaffolding to guide /spec completion.
"""
