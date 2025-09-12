# /plan Command Specification

## Overview
The `/plan` command initiates the strategic planning phase of the Spec-Driven Workflow system. It orchestrates a conversational requirements gathering process between the user and specialized agents to produce a comprehensive strategic plan document.

## Command Metadata

**Name**: `/plan`  
**Type**: User-invoked workflow command  
**Phase**: Strategic Planning (Phase 1 of 4)  
**Model**: Claude Sonnet (default)  

## Invocation

### Who Invokes It
- **Primary**: End user via Claude Code CLI
- **Context**: At the beginning of any new project or feature development
- **Prerequisites**: None - this is the entry point to the workflow

### Trigger Format
```text
/plan [initial_prompt (optional)]
```

### Parameters
- **initial_prompt**: Optional initial prompt for the plan-generator agent

## Workflow Position

```text
[USER] → /plan → [plan-generator ↔ plan-critic loop] → Strategic Plan Document
                           ↓
                    [plan-analyst extraction]
                           ↓
                    [analyst-critic ↔ plan-analyst validation loop]
                           ↓
                    Ready for /spec command
```

### Position in End-to-End Flow
1. **First Phase**: Initial entry point for all development workflows
2. **Precedes**: Technical specification (`/spec`) phase
3. **Dependencies**: None - can be invoked independently
4. **Output Used By**: `/spec` command and `spec-architect` agent

## Primary Responsibilities

### Core Tasks
1. **Initiate Conversational Discovery**
   - Launch `plan-generator` agent for requirements gathering
   - Maintain natural conversation flow with user
   - Progressively refine understanding through dialogue

2. **Coordinate Quality Assessment Loop**
   - Initialize MCP refinement loop for plan phase
   - Pass conversation outputs to `plan-critic` for FSDD evaluation
   - Manage loop state through MCP Server decisions

3. **Orchestrate Refinement Cycles**
   - Receive MCP Server decisions (refine/complete/user_input)
   - Route feedback to `plan-generator` for improvements
   - Monitor iteration count and quality scores

4. **Extract and Validate Business Objectives**
   - Invoke `plan-analyst` agent after plan loop completion
   - Transform conversational plan into structured objectives
   - Initialize validation loop with `analyst-critic` for quality assessment
   - Manage refinement cycles between analyst and critic until validated

5. **Handle Loop Termination**
   - Recognize completion signals from MCP Server for both loops
   - Manage user escalation when stagnation detected
   - Ensure graceful completion regardless of exit reason

## Orchestration Pattern

### Agent Coordination Flow
```text
Main Agent (via /plan)
    │
    ├── 1. Initialize Plan MCP Loop
    │   └── mcp_tool: initialize_refinement_loop(loop_type='plan')
    │
    ├── 2. Plan Generation Loop
    │   ├── Task: plan-generator (requirements gathering)
    │   ├── Task: plan-critic (quality assessment → score)
    │   └── mcp_tool: decide_loop_next_action(plan_loop_id, score)
    │
    ├── 3. Handle Plan Loop Decision
    │   ├── IF "refine" → Pass feedback to plan-generator
    │   ├── IF "complete" → Proceed to objective extraction
    │   └── IF "user_input" → Request clarification
    │
    ├── 4. Initialize Analyst MCP Loop
    │   └── mcp_tool: initialize_refinement_loop(loop_type='analyst')
    │
    ├── 5. Objective Extraction and Validation Loop
    │   ├── Task: plan-analyst (extract objectives from plan)
    │   ├── Task: analyst-critic (validate extraction → score)
    │   └── mcp_tool: decide_loop_next_action(analyst_loop_id, score)
    │
    └── 6. Handle Validation Loop Decision
        ├── IF "refine" → Pass feedback to plan-analyst for re-extraction
        ├── IF "complete" → Ready for /spec command
        └── IF "user_input" → Request objective clarification
```

### Data Flow Between Agents
**Plan Generation Phase:**
- **plan-generator → Main Agent**: Conversational plan document (markdown)
- **Main Agent → plan-critic**: Plan document for assessment
- **plan-critic → Main Agent**: Quality score (0-100) and feedback
- **Main Agent → MCP Server**: Score for plan loop decision logic
- **MCP Server → Main Agent**: Next action decision (refine/complete/user_input)

**Objective Validation Phase:**
- **Main Agent → plan-analyst**: Completed strategic plan for extraction
- **plan-analyst → Main Agent**: Business objectives analysis (markdown)
- **Main Agent → analyst-critic**: Objectives analysis for validation
- **analyst-critic → Main Agent**: Validation score (0-100) and feedback
- **Main Agent → MCP Server**: Score for analyst loop decision logic
- **MCP Server → Main Agent**: Next action decision (refine/complete/user_input)

## Quality Gates

### Success Criteria
**Plan Generation Phase:**
- **Quality Threshold**: 85% (configurable via `FSDD_LOOP_PLAN_THRESHOLD`)
- **Maximum Iterations**: 5 (configurable via `FSDD_LOOP_PLAN_MAX_ITERATIONS`)
- **Improvement Threshold**: 5 points minimum between iterations

**Objective Validation Phase:**
- **Quality Threshold**: 85% (configurable via `FSDD_LOOP_ANALYST_THRESHOLD`)
- **Maximum Iterations**: 3 (configurable via `FSDD_LOOP_ANALYST_MAX_ITERATIONS`)
- **Improvement Threshold**: 8 points minimum between iterations

### FSDD Assessment Points
**Plan-Critic Assessment** (12 criteria):
1. **Clarity** - Requirements clearly stated
2. **Completeness** - All aspects covered
3. **Consistency** - No contradictions
4. **Feasibility** - Technically achievable
5. **Testability** - Verifiable outcomes
6. **Maintainability** - Long-term sustainability
7. **Scalability** - Growth accommodation
8. **Security** - Risk mitigation addressed
9. **Performance** - Efficiency requirements
10. **Usability** - User experience quality
11. **Documentation** - Knowledge preservation plans
12. **Integration** - System compatibility

**Analyst-Critic Assessment** (12 dimensions):
1. **Semantic Accuracy** - Extracted objectives match source plan intent
2. **Completeness** - All stated objectives captured without omissions
3. **Quantification Quality** - Success metrics properly measured and targeted
4. **Stakeholder Mapping** - Accurate identification and needs assessment
5. **Priority Accuracy** - Correct must-have vs nice-to-have classification
6. **Dependency Mapping** - Accurate relationship identification
7. **Constraint Documentation** - Complete technical and business limitations
8. **Risk Assessment** - Appropriate risk identification and mitigation
9. **Timeline Alignment** - Realistic phasing and milestone definition
10. **Assumption Clarity** - Explicit documentation of key assumptions
11. **Success Criteria** - Measurable acceptance criteria definition
12. **Implementation Readiness** - Sufficient detail for technical specification

### Stagnation Detection
- **Trigger**: Less than 5 points improvement over 2 consecutive iterations
- **Action**: MCP Server returns "user_input" status
- **User Prompt**: "The plan refinement has stagnated. Please provide additional clarification or direction."

## Input/Output Specifications

### Input Requirements
- **User Context**: Natural language business requirements
- **Format**: Conversational text input
- **Scope**: Can range from high-level vision to detailed specifications

### Output Specifications
- **Primary Output**: Strategic plan document (markdown format)
- **Structure**:
  ```markdown
  # Strategic Plan: [Project Name]
  
  ## Executive Summary
  [High-level overview]
  
  ## Business Objectives
  - [Objective 1]
  - [Objective 2]
  
  ## Functional Requirements
  [Detailed requirements]
  
  ## Technical Constraints
  [Identified limitations]
  
  ## Success Criteria
  [Measurable outcomes]
  
  ## Risk Considerations
  [Potential challenges]
  ```

## Error Handling

### Common Failure Scenarios

1. **MCP Server Connection Failure**
   - **Error**: "Failed to initialize refinement loop"
   - **Recovery**: Retry connection, fallback to direct agent invocation
   - **User Message**: "MCP Server connection issue. Retrying..."

2. **Agent Invocation Failure**
   - **Error**: "Failed to invoke plan-generator/critic"
   - **Recovery**: Retry agent, provide detailed error to user
   - **User Message**: "Agent temporarily unavailable. Details: [error]"

3. **Stagnation Without Progress**
   - **Error**: Loop stuck at low quality scores
   - **Recovery**: Escalate to user with specific guidance request
   - **User Message**: "Plan quality is not improving. Please provide more specific requirements for: [weak areas]"

4. **Timeout/Max Iterations**
   - **Error**: Reached iteration limit without quality threshold
   - **Recovery**: Present best available plan with quality warnings
   - **User Message**: "Maximum refinements reached. Current plan quality: [score]%. Proceed with caution or refine manually."

### Error Response Format
```json
{
  "error_type": "loop_stagnation|agent_failure|mcp_error|timeout",
  "error_message": "Detailed error description",
  "recovery_action": "Specific recovery steps",
  "user_guidance": "Clear instructions for user",
  "partial_output": "Any salvageable work"
}
```

## Platform-Specific Behavior

### Platform-Agnostic Design
The `/plan` command operates identically across all platforms (Linear, GitHub, Markdown) as it produces platform-independent strategic plans. Platform-specific behavior only emerges in the `/spec` phase.

## Example Usage

### Typical Invocation
```text
User: /plan

Main Agent: I'll help you create a strategic plan for your project. Let me gather your requirements through a conversational process.

[Invokes plan-generator agent]

plan-generator: Hello! I'm here to help you develop a comprehensive strategic plan. Let's start by understanding your vision. What problem are you trying to solve or what opportunity are you pursuing?

User: I want to build a customer feedback analysis system that uses AI to categorize and prioritize support tickets.

plan-generator: Excellent! An AI-powered customer feedback system. Let me understand more:
1. What volume of tickets are you handling?
2. What categories do you need?
3. How should prioritization work?

[Conversation continues...]

[Main Agent invokes plan-critic for quality assessment]
[Score: 72% - needs more detail on integration requirements]

[Main Agent receives "refine" decision from MCP Server]

plan-generator: Let me clarify a few more points about system integration...

[Refinement continues until quality threshold met]

[Final score: 87% - Main Agent receives "complete" decision]

Main Agent: Strategic plan completed successfully! Quality score: 87%. Now extracting business objectives...

[Main Agent invokes plan-analyst for objective extraction]

plan-analyst: Analyzing strategic plan and extracting structured business objectives...

[Main Agent invokes analyst-critic for validation]
analyst-critic: Validating objective extraction... Score: 79% - needs improved quantification of success metrics

[Main Agent receives "refine" decision from MCP Server for analyst loop]

[Refinement cycle continues...]

[Final validation score: 88% - Main Agent receives "complete" decision]

Main Agent: Business objectives extracted and validated successfully! Validation score: 88%. The objectives are now ready for technical specification development. Use /spec to proceed.
```

## Implementation Notes

### Key Considerations for Claude Code

1. **Conversation State Management**
   - Main Agent must preserve conversation context between refinement cycles
   - Pass complete conversation history to plan-generator on each iteration
   - Include critic feedback as context for improvements

2. **Natural Flow Preservation**
   - Avoid disrupting conversation with technical quality assessments
   - Present critic feedback naturally within dialogue
   - Maintain user engagement throughout process

3. **Score Transparency**
   - Optionally show quality scores to user for awareness
   - Always show final score upon completion
   - Explain score components if requested

4. **Graceful Degradation**
   - If MCP Server unavailable, continue with direct agent coordination
   - If critic unavailable, proceed with generator output only
   - Always provide best available output even if quality gates not met

5. **Context Efficiency**
   - Summarize long conversations before passing to critic
   - Focus on most recent refinements in feedback loops
   - Prune redundant information in later iterations

## Dependencies and Integration Points

### Required Components
- **MCP Server**: Loop state management and decision logic
- **plan-generator agent**: Conversational requirements gathering
- **plan-critic agent**: Quality assessment and feedback
- **plan-analyst agent**: Business objective extraction
- **analyst-critic agent**: Objective validation and quality assessment

### MCP Tools Used
**Plan Generation Phase:**
- `initialize_refinement_loop(loop_type='plan')`
- `decide_loop_next_action(plan_loop_id, current_score)`
- `get_loop_status(plan_loop_id)` (optional for monitoring)

**Objective Validation Phase:**
- `initialize_refinement_loop(loop_type='analyst')`
- `decide_loop_next_action(analyst_loop_id, current_score)`
- `get_previous_objective_feedback(analyst_loop_id)`
- `store_current_objective_feedback(analyst_loop_id, feedback)`
- `get_loop_status(analyst_loop_id)` (optional for monitoring)

### Environment Variables
**Plan Generation:**
- `FSDD_LOOP_PLAN_THRESHOLD`: Quality threshold (default: 85)
- `FSDD_LOOP_PLAN_MAX_ITERATIONS`: Maximum iterations (default: 5)

**Objective Validation:**
- `FSDD_LOOP_ANALYST_THRESHOLD`: Quality threshold (default: 85)
- `FSDD_LOOP_ANALYST_MAX_ITERATIONS`: Maximum iterations (default: 3)

## Success Metrics

### Quantitative Metrics
- **Quality Score**: Target ≥85%
- **Iterations to Complete**: Target ≤3
- **User Escalations**: Target <20% of invocations
- **Completion Rate**: Target >95%

### Qualitative Metrics
- **User Satisfaction**: Natural conversation flow maintained
- **Output Completeness**: All business objectives captured
- **Clarity**: Requirements unambiguous and actionable
- **Actionability**: Ready for technical specification without gaps

## Related Documentation
- **Next Phase**: [`/spec` Command Specification](spec.md)
- **Primary Agent**: [`plan-generator` Agent Specification](../agents/plan-generator.md)
- **Quality Agent**: [`plan-critic` Agent Specification](../agents/plan-critic.md)
- **Extraction Agent**: [`plan-analyst` Agent Specification](../agents/plan-analyst.md)
- **Validation Agent**: [`analyst-critic` Agent Specification](../agents/analyst-critic.md)
- **MCP Tools**: [MCP Tools Specification](../MCP_TOOLS_SPECIFICATION.md)
