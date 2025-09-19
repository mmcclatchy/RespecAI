# /plan Command Specification

## Overview
The `/plan` command orchestrates the strategic planning workflow through conversational requirements gathering and dual-loop quality assessment. It transforms natural language business requirements into validated strategic plans through human-in-the-loop conversation followed by automated quality refinement.

## Command Metadata

**Name**: `/plan`
**Type**: Conversational workflow orchestrator
**Phase**: Strategic Planning (Phase 1 of 4)
**Model**: Claude Sonnet (default)

## Invocation

### Who Invokes It
- **Primary**: End user via Claude Code CLI
- **Context**: At the beginning of any new project or feature development
- **Prerequisites**: None - this is the entry point to the workflow

### Trigger Format
```text
/plan [plan-name] [starting-prompt]
```

### Parameters
- **plan-name**: Optional identifier for the planning session
- **starting-prompt**: Optional initial context for conversation

## Workflow Position

```text
User starts → /plan → [/plan-conversation] → Strategic Plan → [plan-critic ↔ refinement loop]
                 ↓                                               ↓
        Conversational Discovery                        Quality Assessment
                 ↓                                               ↓
        Structured Context                              [plan-analyst ↔ analyst-critic loop]
                                                                 ↓
                                              Ready for /plan-roadmap command
```

### Position in End-to-End Flow
1. **First Phase**: Initial entry point for all development workflows
2. **Precedes**: Implementation roadmap (`/plan-roadmap`) phase
3. **Dependencies**: None - can be invoked independently
4. **Output Used By**: `/plan-roadmap` command and roadmap generation agents

## Primary Responsibilities

### Core Tasks

1. **Conversational Requirements Orchestration**
   - Invoke `/plan-conversation` command for user dialogue
   - Manage conversation flow and completion validation
   - Process structured conversation context into strategic plan

2. **Strategic Plan Generation**
   - Transform conversation context into comprehensive strategic plan document
   - Apply strategic plan template with business context integration
   - Handle variable interpolation and context management

3. **Quality Assessment Loop Management (PLAN Loop)**
   - Initialize MCP refinement loop for plan validation
   - Coordinate plan-critic evaluations with FSDD framework
   - Manage refinement iterations with natural checkpoint reporting
   - Handle stagnation detection and user escalation

4. **Objective Extraction and Validation (ANALYST Loop)**
   - Initialize separate MCP loop for objective validation
   - Coordinate plan-analyst extraction from strategic plan
   - Manage analyst-critic validation with quality assessment
   - Ensure business objectives are properly structured

5. **Progress Visibility and User Interaction**
   - Provide real-time quality scores and iteration progress
   - Present clear user options at max iterations and stagnation points
   - Handle error recovery and graceful degradation

## Orchestration Pattern

### Complete Workflow Orchestration
```text
Main Agent (via /plan)
    │
    ├── 1. Conversational Requirements Gathering
    │   ├── Command: /plan-conversation (3-stage dialogue)
    │   ├── Process: Structured JSON context collection
    │   ├── User Control: User drives conversation pacing and completion
    │   └── State: mcp_tool: store_conversation_context(context_json)
    │
    ├── 2. Strategic Plan Generation
    │   ├── Transform: Conversation context → strategic plan document
    │   ├── Template: Apply strategic plan structure with business context
    │   └── Storage: mcp_tool: store_project_plan(project_plan_markdown)
    │
    ├── 3. Quality Assessment and User Decision
    │   ├── Task: plan-critic (FSDD evaluation → quality feedback)
    │   ├── Storage: mcp_tool: store_critic_feedback(critic_feedback_markdown)
    │   ├── Present: Show quality score and feedback to user
    │   └── User Choice: Continue conversation | Refine plan | Accept plan
    │
    ├── 4. Handle User Decision
    │   ├── IF "continue conversation" → Return to /plan-conversation with context
    │   ├── IF "refine plan" → Generate new plan version with feedback
    │   └── IF "accept plan" → Proceed to analyst validation
    │
    ├── 5. Initialize Analyst MCP Loop (Automated Sub-Phase)
    │   └── mcp_tool: initialize_refinement_loop(loop_type='analyst')
    │
    ├── 6. Objective Extraction and Validation Loop
    │   ├── Task: plan-analyst (extract objectives → structured analysis)
    │   ├── Task: analyst-critic (validate extraction → CriticFeedback)
    │   ├── mcp_tool: store_critic_feedback(analyst_feedback_markdown)
    │   └── mcp_tool: decide_loop_next_action(analyst_loop_id, analyst_score)
    │
    ├── 7. Handle Analyst Loop Decision
    │   ├── IF "refine" → Improve objective extraction with feedback
    │   ├── IF "complete" → Finalize ProjectPlan model
    │   └── IF "user_input" → Request objective clarification
    │
    └── 8. Final Output and Handoff
        ├── Final Storage: mcp_tool: store_project_plan(project_plan_markdown)
        └── ProjectPlan ready for /plan-roadmap command
```

### Data Flow Between Components
**Human-Driven Conversation Phase:**
- **Main Agent → /plan-conversation**: Initial context + conversation orchestration
- **/plan-conversation → Main Agent**: Structured JSON context with requirements
- **Main Agent → Strategic Plan**: Template application and document generation
- **Main Agent → plan-critic**: Strategic plan for FSDD assessment
- **plan-critic → Main Agent**: Quality score (0-100) and structured feedback
- **Main Agent → User**: Quality feedback presentation with clear options
- **User → Main Agent**: Decision to continue, refine, or accept plan
- **Main Agent → MCP Server**: Context and plan storage for memory preservation

**Automated Analyst Validation Phase:**
- **Main Agent → plan-analyst**: Completed strategic plan for objective extraction
- **plan-analyst → Main Agent**: Structured business objectives analysis
- **Main Agent → analyst-critic**: Objectives for validation assessment
- **MCP Server → Main Agent**: Loop decisions (refine/complete/user_input) with iteration state

## Natural Checkpoint Strategy

### Conversation Phase Checkpoints
```text
/plan-conversation execution:
├── Stage 1: Vision Discovery → Progress: "Vision and context gathered"
├── Stage 2: Requirements Refinement → Progress: "Requirements and constraints defined"
├── Stage 3: Validation → Progress: "Understanding validated, conversation complete"
└── Handoff: Structured context ready for plan generation
```

### Human-Driven Quality Assessment Checkpoints
```text
Plan Generation and User Review:
├── Strategic Plan Created → Present to user with quality assessment
├── User Decision Point → Clear options presented:
│   ├── "Continue conversation" → Return to /plan-conversation with context
│   ├── "Refine plan" → Generate new version with specific feedback
│   └── "Accept plan" → Proceed to analyst validation
├── Quality Feedback → Show plan-critic assessment results:
│   → "Strategic plan quality: 78%
│      Key strengths: [business context, stakeholder clarity]
│      Areas needing work: [success metrics, risk assessment]"
└── User Controls Iteration → No automated loops, user drives refinement
```

### Analyst Validation Loop Checkpoints
```text
ANALYST Loop (max 3 iterations, threshold varies by configuration):
├── Iteration 1-3: plan-analyst ↔ analyst-critic validation cycles
├── Natural Checkpoint: If max iterations reached
│   → "Objective extraction quality: 81% after 3 iterations
│      Objectives identified: [summary of extracted objectives]
│      Validation issues: [specific clarity or completeness gaps]
│      Options: Continue 2 more iterations | Accept objectives | Clarify objectives"
└── Success: Objectives validated → ProjectPlan complete
```

## Quality Gates

### Success Criteria
**Plan Generation Phase:**
- **Quality Assessment**: plan-critic provides FSDD evaluation and feedback
- **User Decision**: User controls whether to continue conversation, refine plan, or accept
- **No Automated Thresholds**: Quality score informs user decision, doesn't drive automation

**Objective Validation Phase:**
- **Quality Threshold**: Configurable via `FSDD_LOOP_ANALYST_THRESHOLD` (MCP-managed)
- **Maximum Iterations**: Configurable via `FSDD_LOOP_ANALYST_MAX_ITERATIONS` (MCP-managed)
- **Improvement Threshold**: 8 points minimum between iterations

### FSDD Assessment Points
**Plan-Critic Assessment** (12-point FSDD framework):
1. **Clarity** - Requirements clearly stated and unambiguous
2. **Completeness** - All aspects of project scope addressed
3. **Consistency** - No contradictions in requirements or objectives
4. **Feasibility** - Realistic objectives within stated constraints
5. **Testability** - Measurable outcomes and success criteria defined
6. **Maintainability** - Long-term sustainability considerations
7. **Scalability** - Growth accommodation and expansion capabilities
8. **Security** - Risk mitigation strategies documented
9. **Performance** - Efficiency requirements and performance targets
10. **Usability** - User experience quality and interaction patterns
11. **Documentation** - Knowledge preservation and organization
12. **Integration** - System compatibility requirements addressed

**Analyst-Critic Assessment** (Business objective validation):
1. **Semantic Accuracy** - Extracted objectives match strategic plan intent
2. **Completeness** - All stated objectives captured without omissions
3. **Quantification Quality** - Success metrics properly measured
4. **Stakeholder Mapping** - Accurate identification and needs assessment
5. **Priority Accuracy** - Correct must-have vs nice-to-have classification
6. **Dependency Mapping** - Accurate relationship identification
7. **Constraint Documentation** - Complete limitation capture
8. **Risk Assessment** - Appropriate identification and mitigation
9. **Timeline Alignment** - Realistic phasing and milestones
10. **Assumption Clarity** - Explicit documentation of key assumptions
11. **Success Criteria** - Measurable acceptance criteria definition
12. **Implementation Readiness** - Sufficient detail for technical roadmap

## Structured Data Models

### ProjectPlan Model
The `/plan` command creates and stores structured ProjectPlan models:
```python
class ProjectPlan(MCPModel):
    project_name: str
    project_vision: str
    project_mission: str
    project_timeline: str
    project_budget: str
    primary_objectives: str
    success_metrics: str
    # ... 35+ additional structured fields
    project_status: ProjectStatus = ProjectStatus.DRAFT
```

### CriticFeedback Model
Quality assessments stored as structured feedback:
```python
class CriticFeedback(MCPModel):
    loop_id: str
    critic_agent: CriticAgent  # PLAN_CRITIC, ANALYST_CRITIC
    iteration: int
    overall_score: int  # 0-100 with validation
    assessment_summary: str
    detailed_feedback: str
    key_issues: list[str]
    recommendations: list[str]
    timestamp: datetime
```

## Input/Output Specifications

### Input Requirements
- **User Context**: Natural language business requirements through conversation
- **Format**: Interactive dialogue through `/plan-conversation` command
- **Scope**: Can range from high-level vision to detailed business constraints

### Output Specifications
- **Primary Output**: ProjectPlan model stored in MCP Server + strategic plan markdown
- **Structured Storage**: ProjectPlan with 35+ validated fields for downstream processing
- **Conversation Archive**: Complete conversation context preserved in structured format
- **Quality History**: CriticFeedback models for both plan and analyst validation loops

## Error Handling

### Common Failure Scenarios

1. **Conversation Completion Failure**
   - **Error**: `/plan-conversation` returns incomplete or invalid context
   - **Recovery**: Retry conversation with simplified prompts, continue with available context
   - **User Message**: "Conversation incomplete. Proceeding with available context. Some refinement may be needed."

2. **Strategic Plan Generation Failure**
   - **Error**: Cannot transform conversation context into strategic plan
   - **Recovery**: Use template-based plan generation with placeholder content
   - **User Message**: "Plan generation had issues. Created basic template for refinement."

3. **MCP Server Connection Failure**
   - **Error**: Cannot initialize refinement loops or store feedback
   - **Recovery**: Use local loop management with fallback decision logic
   - **User Message**: "MCP loop management unavailable. Using local workflow management."

4. **Quality Assessment Stagnation**
   - **Error**: Plan quality not improving after max iterations
   - **Recovery**: Present current state with specific user guidance options
   - **User Message**: "Plan quality: [score]% after [iterations] iterations. Areas needing clarification: [specific gaps]"

5. **Agent Invocation Failure**
   - **Error**: plan-critic or plan-analyst agents fail to respond
   - **Recovery**: Retry once, then continue with manual quality assessment prompts
   - **User Message**: "Quality assessment unavailable. Manual review recommended for: [areas]"

## Example Usage

### Complete Workflow Example
```text
User: /plan customer-feedback-system

Main Agent: I'll help you create a strategic plan for your customer feedback system. Let me start with conversational requirements gathering.

[Invokes /plan-conversation command]

/plan-conversation: Hello! Let's explore your customer feedback system project. What's the main problem you're trying to solve with this system?

User: We're getting overwhelmed with support tickets and can't prioritize them effectively. We need AI to help categorize and route tickets.

/plan-conversation: That makes sense - automation for ticket triage. Tell me more about your current process and what you envision...

[3-stage conversation continues until completion criteria met]

/plan-conversation: Perfect! I have comprehensive context covering your vision, requirements, and constraints. Let me structure this for strategic planning.

Main Agent: Conversation complete! Creating strategic plan from your requirements...

[Generates strategic plan from structured conversation context]

Strategic Plan Created: "AI-Powered Customer Feedback Triage System"
- Vision: Automated ticket classification and intelligent routing
- Key Requirements: Real-time processing, integration with existing CRM
- Success Metrics: 80% reduction in manual triage time

Evaluating plan quality...

[Invokes plan-critic]

plan-critic: Assessing strategic plan against FSDD framework...
- Clarity: 85/100 - Requirements well articulated
- Completeness: 78/100 - Missing detailed integration requirements
- Feasibility: 82/100 - Realistic timeline and scope
Overall Score: 81%

Main Agent: Plan quality assessment: 81%

**Quality Summary:**
- Clarity: 85/100 - Requirements well articulated
- Completeness: 78/100 - Missing detailed integration requirements
- Feasibility: 82/100 - Realistic timeline and scope

**Your options:**
1. **Continue conversation** - Add more detail about integration requirements
2. **Refine plan** - Generate improved version addressing completeness gaps
3. **Accept plan** - Proceed with current plan to objective extraction

User: Accept plan - let's proceed with objective extraction

Main Agent: Proceeding to automated objective extraction and validation...

[Invokes plan-analyst for objective extraction]

plan-analyst: Extracting business objectives from strategic plan...
- Primary: Reduce manual ticket processing by 80%
- Secondary: Improve customer response time by 50%
- Success metrics: Processing time, customer satisfaction scores

[Invokes analyst-critic for validation]

analyst-critic: Validating objective extraction...
- Semantic accuracy: 88/100 - Objectives align with plan intent
- Quantification: 85/100 - Clear metrics defined
Overall Score: 87%

Main Agent: Strategic planning complete!

## Final Results
- **Plan Quality**: 81% (User-accepted after quality review)
- **Objective Validation**: 87% (Automated extraction and validation complete)
- **Conversation Archive**: 3-stage requirements gathering preserved with user decisions
- **Ready for**: /plan-roadmap to create implementation phases

## Next Steps
Use `/plan-roadmap` to break this strategic plan into implementable phases.
```

## Implementation Notes

### Key Considerations for Claude Code

1. **Conversation Integration**
   - Seamless handoff between `/plan` orchestration and `/plan-conversation` dialogue
   - Preserve conversation context throughout workflow
   - Handle conversation completion validation and error recovery

2. **Variable State Management**
   - Track conversation context, strategic plan, quality scores throughout human-driven process
   - Handle variable interpolation and context preservation
   - Manage state corruption recovery and fallback patterns with MCP state management

3. **Progress Transparency**
   - Show conversation stage completion and plan generation progress
   - Display quality scores with clear user decision options
   - Present actionable choices at each quality assessment checkpoint

4. **Natural User Experience**
   - Maintain conversational flow during requirements gathering
   - Provide clear guidance when user decisions are needed
   - Balance human control with automated objective validation

5. **Error Resilience**
   - Graceful degradation when conversation or assessment fails
   - Recovery patterns for MCP server connectivity issues
   - Clear user communication about workflow status and options

## Dependencies and Integration Points

### Required Components
- **MCP Server**: Dual loop state management and decision logic
- **/plan-conversation command**: Interactive requirements gathering
- **plan-critic agent**: FSDD quality assessment and feedback
- **plan-analyst agent**: Business objective extraction
- **analyst-critic agent**: Objective validation and quality assessment

### MCP Tools Used
**Plan Generation Workflow:**
- `store_project_plan(project_plan_markdown)` - Store ProjectPlan model
- `store_conversation_context(context_json)` - Store conversation state during dialogue
- `store_critic_feedback(feedback_markdown)` - Store plan-critic assessment results
- `get_project_plan_markdown()` - Retrieve stored strategic plan for downstream phases

**Objective Validation Workflow:**
- `initialize_refinement_loop(loop_type='analyst')` - Create analyst validation loop
- `get_project_plan_markdown(plan_loop_id)` - Retrieve stored strategic plan
- `store_current_objective_feedback(analyst_loop_id, feedback)` - Store objective analysis
- `get_previous_objective_feedback(analyst_loop_id)` - Context retrieval for refinement
- `decide_loop_next_action(analyst_loop_id, current_score)` - Validation decision engine

### Environment Variables
**Plan Generation:**
- No automated thresholds - human-driven decisions

**Objective Validation:**
- `FSDD_LOOP_ANALYST_THRESHOLD`: Quality threshold (MCP-managed)
- `FSDD_LOOP_ANALYST_MAX_ITERATIONS`: Maximum iterations (MCP-managed)

## Success Metrics

### Quantitative Metrics
- **Plan Quality Score**: Target threshold-dependent (MCP-configured)
- **Objective Validation Score**: Target threshold-dependent (MCP-configured)
- **Conversation Completion Rate**: Target >95%
- **User Escalations**: Target <20% of invocations

### Qualitative Metrics
- **User Satisfaction**: Natural conversation flow maintained throughout
- **Output Completeness**: All business objectives captured and validated
- **Clarity**: Requirements unambiguous and actionable for technical roadmap
- **Implementation Readiness**: Sufficient detail for `/plan-roadmap` without gaps

## Related Documentation
- **Next Phase**: [`/plan-roadmap` Command Specification](plan-roadmap.md)
- **Conversation Command**: [`/plan-conversation` Command Specification](plan-conversation.md)
- **Quality Agent**: [`plan-critic` Agent Specification](../agents/plan-critic.md)
- **Analysis Agent**: [`plan-analyst` Agent Specification](../agents/plan-analyst.md)
- **Validation Agent**: [`analyst-critic` Agent Specification](../agents/analyst-critic.md)
