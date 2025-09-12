def generate_plan_command_template() -> str:
    return """---
allowed-tools: 
  - Task(plan-generator)
  - Task(plan-critic)
  - Task(plan-analyst)
  - Bash(~/.claude/scripts/detect-packages.sh)
argument-hint: [plan-name] [starting-prompt]
description: Create strategic plans through natural language conversational discovery with understanding validation checkpoints
---

# /plan Command Template

## Command Overview
Orchestrate strategic planning phase through conversational requirements gathering with quality-driven refinement loops.

## Usage
```text
/plan [plan-name] [starting-prompt]
```

## Command Implementation

### Variable Management
**Throughout the command execution, maintain these variables:**

- **LOOP_ID**: String returned from MCP `initialize_refinement_loop` - store and use for all MCP calls
- **CONVERSATION_CONTEXT**: Accumulated conversation text - starts with `$ARGUMENTS` or default prompt
- **PREVIOUS_FEEDBACK**: String from critic feedback - starts empty, updates after each critic assessment
- **CURRENT_PLAN**: Latest plan-generator output - updated after each plan-generator invocation
- **QUALITY_SCORE**: Integer from critic (0-100) - extracted from critic response
- **CRITIC_FEEDBACK**: String with improvement suggestions - extracted from critic response
- **LOOP_STATUS**: String from MCP decision - values: "refine", "user_input", "completed"

**Variable Update Pattern:**
- After plan-generator: Update `CURRENT_PLAN`
- After plan-critic: Update `QUALITY_SCORE` and `CRITIC_FEEDBACK`
- After MCP decision: Update `LOOP_STATUS`
- Before next iteration: Update `CONVERSATION_CONTEXT` and `PREVIOUS_FEEDBACK`

**Variable Interpolation:**
When you see `${variable_name}` in prompts or templates, replace it with the actual content of that variable:
- `${CONVERSATION_CONTEXT}` → Replace with the full text stored in CONVERSATION_CONTEXT
- `${PREVIOUS_FEEDBACK}` → Replace with the text stored in PREVIOUS_FEEDBACK
- `${CURRENT_PLAN}` → Replace with the text stored in CURRENT_PLAN
- `${QUALITY_SCORE}` → Replace with the number stored in QUALITY_SCORE
- `${CRITIC_FEEDBACK}` → Replace with the text stored in CRITIC_FEEDBACK
- `${LOOP_ID}` → Replace with the string stored in LOOP_ID
- `${STRUCTURED_OBJECTIVES}` → Replace with the text stored in STRUCTURED_OBJECTIVES
- `${LOOP_STATUS}` → Replace with the string stored in LOOP_STATUS

### Phase 1: Initialize Planning Loop

**Initialize the MCP refinement loop for strategic planning:**

Use the MCP tool `initialize_refinement_loop` from the MCP Server at `services/mcp/server.py`:
- Call `initialize_refinement_loop(loop_type='plan')`
- Store the returned `LOOP_ID` for tracking throughout the refinement process
- Note the quality threshold: 85% (configurable via FSDD_LOOP_PLAN_THRESHOLD)
- Note the maximum iterations: 5 (configurable via FSDD_LOOP_PLAN_MAX_ITERATIONS)
- Set improvement threshold: 5 points minimum between iterations

**Set initial context:**
- Use `$ARGUMENTS` as initial conversation context
- If no arguments provided, start with: "I need help creating a strategic plan for my project"
- Set PREVIOUS_FEEDBACK as empty string

### Phase 2: Orchestrate Refinement Loop

**Continue the refinement loop until the MCP Server signals completion:**

Repeat the following steps until the MCP Server returns "completed" status:

#### Step 2.1: Invoke plan-generator Agent

**Gather requirements through natural conversation:**

Invoke the plan-generator agent with this context:

```text
Context: ${CONVERSATION_CONTEXT}
Previous Feedback: ${PREVIOUS_FEEDBACK}
```

**Capture and validate the plan-generator output:**
1. **Store the complete response as CURRENT_PLAN**
2. **Validate the output:**
   - Verify the response is not empty
   - Ensure it contains conversational content (not just system messages)
   - Check that it addresses the conversation context
   - If output is invalid, retry the plan-generator with the same context

#### Step 2.2: Quality Assessment

Invoke the plan-critic agent with this context:

```text
Strategic Plan:
${CURRENT_PLAN}
```

**Parse the plan-critic response:**
1. **Extract QUALITY_SCORE:**
   - Look for line starting with "SCORE: "
   - Extract the number after "SCORE: " (should be 0-100)
   - Store as QUALITY_SCORE variable
2. **Extract CRITIC_FEEDBACK:**
   - Look for line starting with "FEEDBACK: "
   - Extract all text after "FEEDBACK: "
   - Store as CRITIC_FEEDBACK variable
3. **Validate extraction:**
   - Verify QUALITY_SCORE is an integer between 0-100
   - Verify CRITIC_FEEDBACK is not empty
   - If parsing fails, retry the plan-critic with the same context

#### Step 2.3: MCP Decision Logic

**Call the MCP Server for next action decision:**

Use the MCP tool `decide_loop_next_action` from the MCP Server at `services/mcp/server.py`:
- Call `decide_loop_next_action(LOOP_ID=LOOP_ID, current_score=QUALITY_SCORE)`
- The MCP Server will analyze the score, track improvement trends, and detect stagnation
- Store the returned status from the MCP response
- Display the quality score and decision to the user

#### Step 2.4: Handle Loop Decision

**Process the MCP Server decision:**

**If status is "refine":**
- Set PREVIOUS_FEEDBACK = CRITIC_FEEDBACK
- Update CONVERSATION_CONTEXT by appending: "\\n\\nRefinement needed: " + CRITIC_FEEDBACK
- Continue to the next iteration of the loop (return to Step 2.1)

**If status is "user_input":**
- The MCP Server has detected stagnation in the refinement process
- Present the current quality score and areas needing clarification to the user
- Request specific user input with this message:

```text
The strategic planning process needs your input to proceed.

Current quality score: ${QUALITY_SCORE}%
Areas needing clarification:
${CRITIC_FEEDBACK}

Please provide additional details or adjust requirements for these areas.
```

- Wait for user response
- Update CONVERSATION_CONTEXT by appending: "\\n\\nUser clarification: " + user_response
- Set PREVIOUS_FEEDBACK = "Incorporate user's clarification into the plan"
- Continue the refinement loop (return to Step 2.1)

**If status is "completed":**
- Display completion message with final quality score
- Exit the refinement loop and proceed to Phase 3

### Phase 3: Extract Business Objectives

After loop completion, invoke the plan-analyst agent with this context:

```text
Strategic Plan:
${CURRENT_PLAN}
```

**Capture and validate the plan-analyst output:**
1. **Store the response as STRUCTURED_OBJECTIVES**
2. **Validate the structured output:**
   - Verify the response is not empty
   - Ensure it contains structured content
   - Check that it addresses the strategic plan
   - If output is invalid, retry the plan-analyst with the same context

### Phase 4: Prepare Final Output

Format the complete strategic plan:

```markdown
# Strategic Plan Output

## Plan Quality
- Final Score: ${QUALITY_SCORE}%
- Completion Status: ${LOOP_STATUS}
- Quality Threshold Met: [Yes/No based on QUALITY_SCORE >= 85]

## Strategic Plan Document
${CURRENT_PLAN}

## Structured Objectives
${STRUCTURED_OBJECTIVES}

## Next Steps
1. Review the strategic plan for accuracy
2. Proceed with technical specification using: /spec
3. The structured objectives will feed directly into spec-architect

## Metadata
- Loop ID: ${LOOP_ID}
- Timestamp: [current date/time]
```

**Final validation before presenting to user:**
1. **Verify all required variables are populated:**
   - QUALITY_SCORE is a valid integer (0-100)
   - CURRENT_PLAN contains substantial content
   - STRUCTURED_OBJECTIVES contains all required sections
   - LOOP_STATUS is "completed"
2. **Quality check:**
   - If QUALITY_SCORE < 85, include a note about threshold not met
   - Ensure the plan addresses the original user context
   - Verify structured objectives align with the strategic plan

## Error Handling

### MCP Connection Failure
**If the MCP Server connection is interrupted at any point:**
- Immediately stop all refinement loop progress
- Display error message: "❌ MCP Server connection lost. Refinement loop state cannot be maintained."
- Inform user: "Please reestablish the MCP Server connection and restart the /plan command."
- Do not attempt to continue without the MCP Server
- Exit the command gracefully

### Agent Invocation Failure
**If an agent fails to respond or returns an error:**
- Display error message: "❌ Agent [agent-name] failed: [error details]"
- Display recovery message: "💡 Attempting recovery..."
- Retry the agent invocation with a simplified prompt
- If retry fails, provide manual guidance to the user
- Continue with any partial output if available

### Stagnation Without Progress
**The MCP Server automatically handles stagnation detection:**
- When quality scores improve less than 5 points over 2 iterations
- The MCP Server will return "user_input" status
- Follow the user_input handling process in Step 2.4
- The user clarification process will break the stagnation

### Maximum Iterations Reached
**The MCP Server automatically handles iteration limits:**
- When the maximum iteration count is reached (default: 5)
- Assess the current quality score for completion decision
- **If QUALITY_SCORE is 70 or higher:**
  - Display: "✓ Proceeding with current plan (acceptable quality)"
  - Continue to Phase 3
- **If QUALITY_SCORE is below 70:**
  - Display: "⚠️ Manual refinement recommended before proceeding"
  - Ask user whether to proceed or restart

## Configuration

### Environment Variables
**The following environment variables control the planning loop behavior:**

- **FSDD_LOOP_PLAN_THRESHOLD**: Quality threshold for completion (default: 85)
- **FSDD_LOOP_PLAN_MAX_ITERATIONS**: Maximum refinement iterations (default: 5)

**Stagnation detection parameters (handled by MCP Server):**
- **IMPROVEMENT_THRESHOLD**: Minimum points improvement required (default: 5)
- **STAGNATION_WINDOW**: Iterations to check for stagnation (default: 2)

### Success Criteria
- Quality score ≥ 85% achieved
- Clear business objectives extracted
- All stakeholders identified
- Measurable success metrics defined
- Ready for technical specification phase

## Implementation Notes

### Context Management
**Standard Context Handling:**
- Preserve full conversation history between iterations
- Focus critic on most recent refinements
- Maintain chronological order of user interactions

**Large Context Management (when CONVERSATION_CONTEXT exceeds 4000 characters):**
1. **Identify content to summarize:**
   - Keep the original user context (first interaction) intact
   - Keep the most recent 2 iterations in full detail
   - Summarize middle iterations while preserving key requirements
2. **Summarization approach:**
   - Extract key business objectives and requirements from older content
   - Note important stakeholder mentions and constraints
   - Preserve any specific metrics or success criteria mentioned
   - Include note: "[Earlier conversation summarized - key requirements preserved]"
3. **Update CONVERSATION_CONTEXT:**
   - Start with original user context
   - Add summarized middle content
   - Append recent iterations in full
   - Ensure total length stays under 4000 characters

### Natural Flow Preservation
- Hide quality scores during conversation
- Integrate feedback naturally into dialogue
- Maintain user engagement throughout
- Only show scores at completion or when requested

### Performance Optimization
- Cache agent responses for retry scenarios
- Batch related clarification requests
- Limit context size to avoid token overflow
- Use incremental refinement for efficiency

## Integration Points

### Required MCP Tools
- `initialize_refinement_loop(loop_type='plan')`
- `decide_loop_next_action(LOOP_ID, current_score)`
- `get_LOOP_STATUS(LOOP_ID)` [optional for monitoring]

### Agent Dependencies
- **plan-generator**: Conversational requirements gathering
- **plan-critic**: FSDD quality assessment
- **plan-analyst**: Business objective extraction

### Output Consumers
- **/spec command**: Uses structured objectives
- **spec-architect agent**: Consumes business requirements
- **Documentation systems**: Archives strategic plans

## Detailed Error Recovery Procedures

### Agent-Specific Recovery Strategies

**plan-generator failure recovery:**
1. **First retry:** Retry the plan-generator with the same context
2. **If retry fails:** Manual guidance:
   - Ask user to directly describe their project goals
   - Provide template questions for user to answer
   - Accept user responses as CURRENT_PLAN for critic assessment

**plan-critic failure recovery:**
1. **First retry:** Retry the plan-critic with the same context
2. **If retry fails:** Manual assessment:
   - Ask user to rate their own plan satisfaction (1-10)
   - Convert to 0-100 scale (multiply by 10)
   - Use user feedback as CRITIC_FEEDBACK

**plan-analyst failure recovery:**
1. **First retry:** Retry the plan-analyst with the same context
2. **If retry fails:** Use CURRENT_PLAN as STRUCTURED_OBJECTIVES
"""
