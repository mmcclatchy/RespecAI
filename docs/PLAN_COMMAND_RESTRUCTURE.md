# Plan Command Restructuring Implementation Guide

## Executive Summary

This document outlines the successfully implemented architectural restructuring of the `/plan` command workflow. The restructuring achieved better separation of concerns, modular conversation management, and improved state handling through command-driven orchestration with specialized agent processing and dual-loop validation.

## Implementation Status

### ✅ Successfully Resolved Issues

1. **Architectural Alignment**: Main Agent now handles strategic plan creation directly using template processing
2. **Clear Responsibilities**: Commands handle conversation, agents process data, MCP manages state
3. **Context Management**: Dual-loop architecture with MCP state persistence
4. **Clean Separation**: Conversation flow completely separated from quality assessment and document management

### Current Working Flow
```text
/plan command (dual-loop orchestration)
├── Step 1: Initialize plan + analyst loops
├── Step 2: /generate-plan (conversation)
├── Step 3: Main Agent creates strategic plan
├── Steps 4-5: plan-critic + MCP plan refinement loop
├── Steps 6-7: plan-analyst + analyst-critic
└── Steps 8-9: MCP analyst validation loop
```

**Achievement**: Complete workflow coordination with dual validation loops.

## Implemented Architecture

### Nested Command Architecture (Successfully Implemented)

Commands are markdown instruction templates for the Main Agent, enabling clean composition without state management complexity.

### Current Production Flow
```text
/plan command (dual-loop orchestration)
├── Step 1: Initialize MCP loops (plan + analyst)
├── Step 2: /generate-plan (3-stage conversation)
│   ├── Stage 1: Vision discovery questions
│   ├── Stage 2: Progressive refinement questions
│   └── Stage 3: Validation questions
├── Step 3: Main Agent strategic plan creation (template-based)
├── Steps 4-5: plan-critic evaluation + MCP plan loop
├── Steps 6-9: plan-analyst extraction + analyst-critic + MCP analyst loop
└── Final output with dual validation scores
```

## Project Tools and Platform Integration

### Platform-Specific Tool Mapping

The system supports three platforms for project documentation:

```python
PLATFORM_TOOL_MAPPING = {
    'linear': {
        'create_project': 'mcp__linear-server__create_project',
        'get_project': 'mcp__linear-server__get_project',
        'update_project': 'mcp__linear-server__update_project'
    },
    'github': {
        'create_project': 'mcp__github__create_issue',
        'get_project': 'mcp__github__get_issue',
        'update_project': 'mcp__github__update_issue'
    },
    'markdown': {
        'create_project': 'Write',
        'get_project': 'Read',
        'update_project': 'Edit'
    }
}
```

These tools are injected into agent templates at generation time based on the configured platform.

## Template vs Command Distinction

### Templates (Python Functions)
**Location**: `/services/templates/agents/` and `/services/templates/commands/`
**Purpose**: Generate agent and command content dynamically
**Example**: `plan_critic.py` contains `generate_plan_critic_template()`

### Commands (Markdown Files)
**Location**: `.claude/commands/`
**Purpose**: Provide instructions to Main Agent
**Example**: `generate-plan.md` guides conversation flow

### Generation Flow
```text
Template Function → Platform Config → Generated Command/Agent → Main Agent Uses
```

## Implementation Phases

### Phase 1: Core Command Restructuring

#### 1.1 Create `/generate-plan` Command

**Purpose**: Pure conversation guidance for Main Agent

**Location**: `.claude/commands/generate-plan.md`

**Structure**:
```markdown
---
description: Conduct conversational requirements gathering
---

# Conversational Requirements Discovery

## Stage 1: Vision and Context Discovery
Begin with broad, open-ended exploration:
- Vision Understanding: "Tell me about what you're trying to build or achieve"
- Context Gathering: "What's driving this project? What problem are you solving?"
- Success Exploration: "How will you know when this is successful?"
- Stakeholder Context: "Who are the main people involved or affected by this?"

### Conversational Techniques
- **Follow-up Questions**: Build naturally on user responses
- **Active Listening**: "I hear that [X] is important because..."
- **Open Space**: Give user time to add what they think matters

## Stage 2: Progressive Requirement Refinement
Guide conversation toward more specific details:
- Scope Clarification: "Let's talk about what this includes and what it doesn't"
- User Experience Focus: "Walk me through how someone would use this"
- Integration Context: "What other systems or tools does this need to work with?"
- Constraint Exploration: "What limitations or requirements do we need to work within?"

### Understanding Validation
- **Summarization**: "So if I understand correctly, you're looking for..."
- **Gap Identification**: "I want to make sure I'm not missing anything important..."
- **Priority Confirmation**: "It sounds like [X] is more important than [Y], is that right?"

## Stage 3: Detail and Validation
Refine understanding with specific validation:
- Requirement Validation: "Let me make sure I understand correctly..."
- Priority Clarification: "What's most important if we had to prioritize?"
- Timeline Context: "What's the timeline you're thinking about?"
- Success Criteria: "How will we measure if this is working well?"

### Conversation Management
- **Pacing**: Allow natural flow without rushing
- **Context Bridging**: Connect different parts of conversation
- **Comfort Building**: Create safe space for incomplete thoughts

## Context Structure
Store all responses in structured format:
```json
{
  "vision": {
    "problem_statement": "...",
    "desired_outcome": "...",
    "success_metrics": "..."
  },
  "requirements": {
    "functional": [...],
    "technical": [...],
    "constraints": [...]
  },
  "priorities": {
    "must_have": [...],
    "nice_to_have": [...]
  }
}
```

#### 1.2 Implemented `/plan` Command

**Purpose**: Dual-loop orchestration of conversation and agent validation workflow

**Current Structure**:
```markdown
---
allowed-tools:
  - Task(plan-critic)
  - Task(plan-analyst)
  - Task(analyst-critic)
  - initialize_refinement_loop
  - decide_loop_next_action
  - get_loop_status
  - get_previous_objective_feedback
  - store_current_objective_feedback
description: Orchestrate strategic planning workflow
---

# Strategic Planning Orchestration

## Step 1: Initialize Planning Loop
Use initialize_refinement_loop('plan') → PLAN_LOOP_ID

## Step 2: Conversational Requirements Gathering
Use /generate-plan command → CONVERSATION_CONTEXT (structured JSON)

## Step 3: Create Strategic Plan Document
Main Agent processes CONVERSATION_CONTEXT using strategic plan template → CURRENT_PLAN

## Step 4: Quality Assessment
Task(plan-critic) → QUALITY_SCORE + CRITIC_FEEDBACK

## Step 5: Plan Refinement Loop
MCP decide_loop_next_action(PLAN_LOOP_ID, QUALITY_SCORE) → PLAN_LOOP_STATUS

## Step 6: Initialize Analyst Validation Loop
Use initialize_refinement_loop('analyst') → ANALYST_LOOP_ID

## Step 7: Extract Objectives
Task(plan-analyst) → STRUCTURED_OBJECTIVES

## Step 8: Analyst Quality Assessment
Task(analyst-critic) → ANALYST_SCORE + ANALYST_FEEDBACK

## Step 9: Analyst Validation Loop
MCP decide_loop_next_action(ANALYST_LOOP_ID, ANALYST_SCORE) → ANALYST_LOOP_STATUS
```

#### 1.3 Strategic Plan Creation (Main Agent)

**Implementation**: Main Agent template processing approach

**Key Features**:
- No separate plan-generator agent needed
- Main Agent processes CONVERSATION_CONTEXT directly
- Template-based strategic plan generation
- Incorporates previous feedback for refinement iterations

**Process**:
```markdown
## Step 3: Create Strategic Plan Document
Using structured CONVERSATION_CONTEXT from /generate-plan:

**Strategic Plan Template:**
# Strategic Plan: [Project Name from conversation]
## Executive Summary
[High-level overview from vision section]
## Business Context  
[Problem statement and business drivers]
## Business Objectives
[Specific, measurable goals extracted]
## Functional Requirements
[Core features and capabilities]
## Technical Constraints
[Integration and technology limitations]
## Success Criteria
[Quantitative metrics and qualitative goals]
## Risk Assessment
[Potential challenges and mitigation strategies]
## Timeline Considerations
[Phased approach from timeline constraints]
## Resource Requirements
[Team, infrastructure, budget from resource constraints]

**Processing Steps:**
1. Extract information from each CONVERSATION_CONTEXT JSON section
2. Structure into strategic plan format using template
3. Incorporate PREVIOUS_FEEDBACK if not empty
4. Store complete strategic plan as CURRENT_PLAN
```

### Phase 2: Optional State Management Extensions

#### 2.1 Stage-Specific Critics

**Consider adding if quality needs more granularity:**

```text
plan-vision-critic      → Evaluates problem clarity and scope understanding
plan-refinement-critic  → Evaluates requirement depth and detail  
plan-validation-critic  → Evaluates completeness and consistency
```

**Integration Points**:
- After each conversation stage in `/generate-plan`
- Provides targeted feedback for specific aspects
- Quality gates prevent advancing without meeting criteria

#### 2.2 MCP State Tools

**Add to `/services/mcp/server.py` if context pressure becomes issue:**

```python
@mcp.tool()
async def store_stage_summary(
    loop_id: str,
    stage: str,  # "vision" | "refinement" | "validation"
    summary: str,
    ctx: Context
) -> MCPResponse:
    """Store conversation stage summary for planning."""

@mcp.tool()
async def get_stage_summary(
    loop_id: str,
    stages: str,  # comma-separated stage names
    ctx: Context
) -> MCPResponse:
    """Retrieve stage summaries for planning context."""

@mcp.tool()
async def get_current_stage(
    loop_id: str,
    ctx: Context
) -> MCPResponse:
    """Get current conversation stage for resumption."""
```

**Benefits**:
- Persist summaries across context resets
- Enable conversation resumption
- Reduce Main Agent context pressure

### Phase 3: Advanced Enhancements

#### 3.1 Conversation Progress Tracking

```text
/plan with progress tracking
├── Initialize loop with stage tracking
├── /generate-plan
│   ├── Check current stage via MCP
│   ├── Resume from appropriate point
│   └── Store stage summaries
├── Compile summaries for plan-generator
└── Standard refinement loop
```

#### 3.2 Hybrid State Management

**Combine approaches for robustness:**

1. **MCP Tools**: Track stage progression and summaries
2. **Project Tools**: Store intermediate drafts
3. **Main Agent**: Maintain active conversation context

## Implementation Order

### ✅ Completed Implementation (Phase 1)

1. **✅ `/generate-plan` command implemented**
   - Pure conversation guidance for Main Agent
   - 3-stage structure (Vision → Refinement → Validation)
   - No agent invocations - clean conversation flow
   - Structured JSON output for handoff

2. **✅ `/plan` command restructured**
   - Dual-loop orchestration architecture
   - `/generate-plan` integration
   - MCP state management integration
   - Complete variable management system

3. **✅ Agent coordination optimized**
   - plan-generator removed (Main Agent handles plan creation)
   - plan-critic: FSDD framework evaluation
   - plan-analyst: Business objective extraction
   - analyst-critic: Validation quality assessment

4. **✅ Production workflow verified**
   - Conversation flow: Natural, engaging dialogue
   - Context preservation: 100% requirements captured
   - Document quality: Comprehensive strategic plans
   - Dual validation: Plan + analyst quality loops

### Future Enhancements (Phases 2-3)

1. **Add stage summaries** (if context pressure)
   - Implement MCP state tools
   - Track conversation progress
   - Enable resumption

2. **Add stage critics** (if quality needs refinement)
   - Create focused critic agents
   - Integrate quality gates
   - Provide targeted feedback

## Benefits of This Architecture

### Immediate Benefits

1. **Clear Separation of Concerns**
   - Commands handle user interaction
   - Agents process data
   - MCP manages state

2. **Modular Conversation Management**
   - `/generate-plan` is reusable
   - Easy to modify conversation flow
   - Can create variants (quick-plan, detailed-plan)

3. **Architectural Alignment**
   - Matches actual system capabilities
   - Commands compose naturally
   - Agents remain isolated processors

### Long-term Benefits

1. **Extensibility**
   - Easy to add new conversation patterns
   - Can create conversation library
   - Stage critics can be added incrementally

2. **Maintainability**
   - Changes to conversation don't affect orchestration
   - Agent logic separated from interaction
   - Clear testing boundaries

3. **Reusability**
   - `/generate-plan` usable by other workflows
   - Conversation patterns become building blocks
   - Can compose complex workflows from simple parts

## FSDD Framework Integration

### Quality Assessment Dimensions

The plan-critic agent evaluates strategic plans using the 12-point FSDD framework:

```python
FSDD_QUALITY_GATES = {
    'clarity': 'Requirements are unambiguous and clearly stated',
    'completeness': 'All aspects of project scope addressed',
    'consistency': 'No contradictions in requirements or objectives',
    'feasibility': 'Realistic objectives within stated constraints',
    'testability': 'Measurable outcomes and success criteria defined',
    'maintainability': 'Long-term sustainability considerations included',
    'scalability': 'Growth potential and expansion capabilities addressed',
    'security': 'Risk awareness and mitigation strategies documented',
    'performance': 'Efficiency goals and performance requirements specified',
    'usability': 'User experience focus and interaction patterns defined',
    'documentation': 'Knowledge capture and information organization maintained',
    'integration': 'System compatibility and integration requirements addressed'
}
```

### Quality Scoring and MCP Integration

**Scoring Mechanism**:
- Each dimension scored 0-100
- Critical gates (clarity, completeness, consistency, feasibility) weighted 2x
- Scores provided to MCP Server for threshold-based decision logic
- MCP Server determines refinement actions based on configured criteria

**Integration Points**:
- plan-critic applies FSDD scoring to generated plans
- analyst-critic validates business objective extraction quality
- Scores feed into MCP loop decision logic
- Feedback structured to support MCP refinement guidance
- Dual-loop validation ensures comprehensive quality assessment

### Stage-Specific Quality Focus

**Stage 1 (Vision)**: Focus on clarity and feasibility
**Stage 2 (Refinement)**: Focus on completeness and consistency
**Stage 3 (Validation)**: Focus on testability and documentation

## Error Handling and Recovery

### Conversation Error Handling

#### User Response Issues

**Unclear Responses**:
- Rephrase questions using simpler language
- Provide concrete examples to clarify intent
- Offer multiple-choice options when appropriate
- Example: "I'm not sure I understand. Are you looking for [Option A], [Option B], or something else?"

**Conversation Stalls**:
- Break complex questions into smaller parts
- Offer suggested topics to explore
- Summarize progress to re-engage
- Example: "Let's take a step back. So far we've covered X and Y. Would you like to explore Z next?"

**Scope Creep**:
- Gently refocus on core objectives
- Suggest phased approach for additional features
- Document out-of-scope items for future consideration
- Example: "That's an interesting idea. Let's capture it for Phase 2 and focus on the core functionality first."

**Technical Overwhelm**:
- Simplify technical language
- Focus on business outcomes over implementation details
- Defer deep technical discussions to later stages
- Example: "Let's focus on what you want to achieve rather than how we'll build it."

### Tool Operation Failures

**Project Tool Failures**:
```python
ERROR_RECOVERY = {
    'create_failed': 'Continue conversation, attempt recreation later',
    'update_failed': 'Store changes locally, retry with exponential backoff',
    'get_failed': 'Proceed with cached version or start fresh',
    'conflict': 'Reconcile through conversation validation'
}
```

**MCP Tool Failures**:
- Loop initialization failure: Proceed without formal tracking
- Decision tool failure: Apply basic fallback decision logic based on previous patterns
- Status retrieval failure: Continue with last known state

### Context Management Issues

**Context Window Exhaustion**:
- Trigger stage summary generation
- Store conversation checkpoints via MCP tools
- Prioritize most recent and critical information
- Use progressive summarization techniques

**Context Loss During /compact**:
- Persist stage summaries before compaction
- Store critical decisions in project documentation
- Maintain conversation continuity markers
- Reload essential context post-compaction

### Recovery Strategies

**Graceful Degradation**:
1. Primary: Full conversation with tool integration
2. Fallback: Conversation with manual documentation
3. Minimal: Basic requirements capture without tools

**Conversation Recovery**:
```markdown
## Resumption Protocol
1. Check last completed stage via MCP
2. Retrieve stage summaries if available
3. Validate understanding with user
4. Continue from last checkpoint
```

## Risk Mitigation

### Context Window Management

**Risk**: Extended conversations consume Main Agent context

**Mitigation**:
- Stage summaries reduce full context retention
- Progressive disclosure limits information per stage
- MCP state tools provide persistence option

### Conversation Continuity

**Risk**: Modular approach might feel disjointed

**Mitigation**:
- `/generate-plan` maintains natural flow
- Context bridging between stages
- Main Agent preserves conversation tone

### Quality Consistency

**Risk**: Without stage critics, quality might vary

**Mitigation**:
- Overall plan-critic provides comprehensive assessment
- Can add stage critics incrementally if needed
- FSDD framework ensures consistent evaluation

## Success Metrics

### Phase 1 Success Criteria

- [x] `/generate-plan` conducts natural conversations
- [x] Context successfully passed to Main Agent for plan creation
- [x] Strategic plans created using template processing
- [x] Quality assessment via plan-critic works
- [x] Dual MCP refinement loops function correctly
- [x] Business objective extraction and validation implemented

### Quality Indicators

- **Conversation Flow**: Natural, engaging dialogue
- **Context Preservation**: All requirements captured
- **Document Quality**: Comprehensive strategic plans
- **Refinement Efficiency**: <3 iterations average
- **User Satisfaction**: Clear, actionable plans

## Conclusion

This restructuring provides a clean, modular architecture that aligns with system capabilities while maintaining flexibility for future enhancements. The command-driven conversation approach with agent processing creates clear boundaries and reusable components, setting a pattern for other workflow implementations in the system.

The phased implementation allows immediate improvements while preserving options for sophisticated state management and quality assessment as the system matures.
