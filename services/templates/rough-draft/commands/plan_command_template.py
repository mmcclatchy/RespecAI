def generate_plan_command_template() -> str:
    return """---
allowed-tools: 
  - Task(plan-generator)
  - Task(plan-critic)
  - Task(plan-analyst)
  - Bash(~/.claude/scripts/detect-packages.sh)
argument-hint: [phase-name] [starting-prompt]
description: Create strategic plans through natural language conversational discovery with understanding validation checkpoints
---

# Enhanced Conversational Strategic Planning Command

Create strategic plans through natural language conversations that progress from broad vision to detailed specifications, with understanding validation checkpoints to ensure user satisfaction.

## Your Task

Create strategic plan through conversational discovery for phase: $ARGUMENTS

## Implementation Flow

### 1. Initialize Conversational Planning
- Read strategic plan template: @docs/templates/STRATEGIC_PLAN_CREATION_TEMPLATE.md
- Execute `~/.claude/scripts/detect-packages.sh` for technology context
- Set conversation parameters:
  - conversation_round = 0
  - completeness_threshold = 0.85
  - max_conversation_rounds = 5
  - understanding_validated = false

### 2. Conversational Discovery Loop

**While** understanding_validated == false AND conversation_round < 5:

#### Step A: Natural Language Planning Discussion (plan-generator)
- Launch plan-generator via Task tool
- Input: Current conversation state + understanding gaps + technology context + user's previous responses
- Conduct natural discussion based on conversation round:
  - **Round 1-2**: Broad vision exploration ("Tell me about your overall goal for this phase...")
  - **Round 3-4**: Progressive refinement ("I'm curious about how you see [specific aspect] working...")
  - **Round 5**: Gap completion ("Let's clarify the remaining areas...")
- **Key Feature**: Present understanding validation checkpoints when sufficient foundation exists
- Capture user responses and build shared understanding organically
- No mechanical questioning - use active listening and natural follow-ups

#### Step B: Conversation Quality Assessment (plan-critic)
- Launch plan-critic via Task tool
- Input: Complete conversation history + current understanding coverage + user engagement indicators
- Evaluate conversation progress:
  - Understanding completeness across FSDD dimensions (business, technical, boundaries, quality)
  - User engagement quality and natural conversation flow
  - Readiness for understanding validation checkpoint or plan finalization
  - Coverage gaps requiring continued natural discussion
- Generate completeness score and conversation continuation guidance

## Conversational Approach Benefits

### User Experience Enhancement
- **Natural Discovery**: Start with user's vision in their own words
- **No Overwhelming Questions**: Avoid presenting 19 questions upfront
- **Understanding Checkpoints**: Validate comprehension before proceeding
- **Adaptive Flow**: Conversation adjusts to what user knows vs doesn't know

### Quality Assurance
- **Complete FSDD Compliance**: All 12 quality gates achieved through organic discussion
- **User Validation**: Explicit confirmation prevents misunderstandings
- **Technology Integration**: Natural exploration of current stack + new technologies
- **Backward Compatibility**: Generates same strategic plan format for downstream commands

## Example Conversation Flow

### Opening (Natural Discovery)
```text
Assistant: I'd love to understand your vision for this phase. What's the main problem you're trying to solve, or what capability do you want to build?

User: I want to create some kind of workflow service that can handle complex research tasks automatically.

Assistant: That's really interesting - what would success look like to you if you had this working perfectly?

User: I'd save hours of research time and get more comprehensive results than I could manually.
```

### Understanding Validation Checkpoint
```text
Assistant: Based on our conversation, here's my understanding of what you want to build:

# Current Understanding

## Main Objective
Create an intelligent workflow service that automates complex research tasks to save time and improve comprehensiveness.

## Technical Approach  
Build a service that can handle multi-step research processes automatically, reducing manual effort while increasing result quality.

## Key Success Criteria
- Significant time savings (hours of research time)
- More comprehensive results than manual research
- Automated handling of complex research workflows

## Technology Context
[Current stack from detect-packages.sh would be shown here]

---

Does this capture your vision? What should I refine or expand on?

User: Yes, that's exactly it! I'd also like it to integrate with our existing Neo4j knowledge graph.
```

### Progressive Refinement
```text
Assistant: Perfect! That integration context is really helpful. I'm curious about how you see the workflow coordination working - are you thinking about orchestrating multiple research agents, or more like a single intelligent agent that can handle different types of research?

User: I want to orchestrate multiple specialized research agents through something like LangGraph, where each agent has specific expertise.
```

### Final Understanding Validation
```text
Assistant: Excellent! Now I have a complete picture. Let me validate my final understanding:

You want to build a LangGraph-based workflow service that:
- Orchestrates multiple specialized research agents
- Integrates with your existing Neo4j knowledge graph
- Automates complex, multi-step research processes
- Delivers more comprehensive results than manual research
- Saves significant time (hours per research task)

This would be Phase 2 of your system, building on the Neo4j foundation from Phase 1. Does this capture everything?

User: Perfect! That's exactly what I want to build.
```

## Error Handling

### Command-Level Error Recovery
- **Missing Template**: If template file not found, explain dependency and provide guidance to create template
- **Technology Detection Failure**: Fallback to manual technology specification with user prompts
- **Agent Communication Issues**: Retry logic for plan-generator and plan-critic coordination
- **User Disengagement**: If user provides short answers, adjust conversation style to re-engage

### Conversation Flow Errors  
- **Understanding Validation Failure**: If user corrects understanding significantly, restart discovery with corrected context
- **Conversation Stagnation**: If quality doesn't improve after 2 rounds, present current understanding and offer to proceed
- **Agent Coordination Failure**: Fallback to direct prompting if conversational agents fail
- **Template Variable Population**: Validate all required variables captured before plan generation

## Success Criteria

### Conversational Quality Achievement
- User provides rich, detailed responses showing engagement
- Natural flow from broad vision to specific requirements
- 85%+ understanding coverage across FSDD dimensions through organic discussion
- User validates understanding checkpoints positively
- No mechanical question-answer feel

### FSDD Compliance Through Conversation
- All 12 FSDD quality gates achieved through natural discussion
- User-validated understanding of business objectives, constraints, and success criteria
- Technology stack naturally explored and documented
- Complete strategic plan generation with FSDD validation

### Integration Success
- Same strategic plan format generated for downstream `/spec` command compatibility
- Technology detection and user selection process preserved
- Existing plan-analyst integration maintained for final plan generation
- Backward compatibility with existing workflow commands
"""
