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

4. **Extract Business Objectives**
   - Invoke `plan-analyst` agent after loop completion
   - Transform conversational plan into structured objectives
   - Prepare output for technical specification phase

5. **Handle Loop Termination**
   - Recognize completion signals from MCP Server
   - Manage user escalation when stagnation detected
   - Ensure graceful completion regardless of exit reason

## Orchestration Pattern

### Agent Coordination Flow
```text
Main Agent (via /plan)
    │
    ├── 1. Initialize MCP Loop
    │   └── mcp_tool: initialize_refinement_loop(loop_type='plan')
    │
    ├── 2. Start Conversation Loop
    │   ├── Task: plan-generator (requirements gathering)
    │   ├── Task: plan-critic (quality assessment → score)
    │   └── mcp_tool: decide_loop_next_action(loop_id, score)
    │
    ├── 3. Handle Loop Decision
    │   ├── IF "refine" → Pass feedback to plan-generator
    │   ├── IF "complete" → Exit loop successfully
    │   └── IF "user_input" → Request clarification
    │
    └── 4. Extract Objectives
        └── Task: plan-analyst (final structuring)
```

### Data Flow Between Agents
- **plan-generator → Main Agent**: Conversational plan document (markdown)
- **Main Agent → plan-critic**: Plan document for assessment
- **plan-critic → Main Agent**: Quality score (0-100) and feedback
- **Main Agent → MCP Server**: Score for decision logic
- **MCP Server → Main Agent**: Next action decision
- **Main Agent → plan-analyst**: Completed plan for extraction

## Quality Gates

### Success Criteria
- **Quality Threshold**: 85% (configurable via `FSDD_LOOP_PLAN_THRESHOLD`)
- **Maximum Iterations**: 5 (configurable via `FSDD_LOOP_PLAN_MAX_ITERATIONS`)
- **Improvement Threshold**: 5 points minimum between iterations

### FSDD Assessment Points
The plan-critic evaluates against 12 criteria:
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

Main Agent: Strategic plan completed successfully! Quality score: 87%. The plan is now ready for technical specification development. Use /spec to proceed.
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

### MCP Tools Used
- `initialize_refinement_loop(loop_type='plan')`
- `decide_loop_next_action(loop_id, current_score)`
- `get_loop_status(loop_id)` (optional for monitoring)

### Environment Variables
- `FSDD_LOOP_PLAN_THRESHOLD`: Quality threshold (default: 85)
- `FSDD_LOOP_PLAN_MAX_ITERATIONS`: Maximum iterations (default: 5)

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
- **MCP Tools**: [MCP Tools Specification](../MCP_TOOLS_SPECIFICATION.md)
