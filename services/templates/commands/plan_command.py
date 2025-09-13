def generate_plan_command_template() -> str:
    return """---
allowed-tools:
  - Task(plan-critic)
  - Task(plan-analyst)
  - Task(analyst-critic)
  - initialize_refinement_loop
  - decide_loop_next_action
  - get_loop_status
  - get_previous_objective_feedback
  - store_current_objective_feedback
argument-hint: [plan-name] [starting-prompt]
description: Orchestrate strategic planning workflow
---

# Strategic Planning Orchestration

## Variable Management
**Throughout the command execution, maintain these variables:**

- **PLAN_LOOP_ID**: String returned from MCP `initialize_refinement_loop('plan')` - store and use for plan loop MCP calls
- **ANALYST_LOOP_ID**: String returned from MCP `initialize_refinement_loop('analyst')` - store and use for analyst loop MCP calls
- **CONVERSATION_CONTEXT**: Accumulated conversation text - starts with `$ARGUMENTS` or default prompt
- **PREVIOUS_FEEDBACK**: String from critic feedback - starts empty, updates after each critic assessment
- **CURRENT_PLAN**: Strategic plan document created from conversation context
- **QUALITY_SCORE**: Integer from plan-critic (0-100) - extracted from critic response
- **CRITIC_FEEDBACK**: String with improvement suggestions - extracted from critic response
- **PLAN_LOOP_STATUS**: String from MCP decision - values: "refine", "user_input", "completed"
- **STRUCTURED_OBJECTIVES**: Business objectives analysis from plan-analyst
- **ANALYST_SCORE**: Integer from analyst-critic (0-100) - extracted from analyst-critic response
- **ANALYST_FEEDBACK**: String with validation suggestions - extracted from analyst-critic response
- **ANALYST_LOOP_STATUS**: String from MCP decision - values: "refine", "user_input", "completed"

**Variable Update Pattern:**
- After strategic plan creation: Update `CURRENT_PLAN`
- After plan-critic: Update `QUALITY_SCORE` and `CRITIC_FEEDBACK`
- After plan MCP decision: Update `PLAN_LOOP_STATUS`
- After plan-analyst: Update `STRUCTURED_OBJECTIVES`
- After analyst-critic: Update `ANALYST_SCORE` and `ANALYST_FEEDBACK`
- After analyst MCP decision: Update `ANALYST_LOOP_STATUS`
- Before next iteration: Update `CONVERSATION_CONTEXT` and `PREVIOUS_FEEDBACK`

**Variable Interpolation:**
When you see `${variable_name}` in prompts or templates, replace it with the actual content of that variable:
- `${CONVERSATION_CONTEXT}` → Replace with the full text stored in CONVERSATION_CONTEXT
- `${PREVIOUS_FEEDBACK}` → Replace with the text stored in PREVIOUS_FEEDBACK
- `${CURRENT_PLAN}` → Replace with the text stored in CURRENT_PLAN
- `${QUALITY_SCORE}` → Replace with the number stored in QUALITY_SCORE
- `${CRITIC_FEEDBACK}` → Replace with the text stored in CRITIC_FEEDBACK
- `${PLAN_LOOP_ID}` → Replace with the string stored in PLAN_LOOP_ID
- `${ANALYST_LOOP_ID}` → Replace with the string stored in ANALYST_LOOP_ID
- `${STRUCTURED_OBJECTIVES}` → Replace with the text stored in STRUCTURED_OBJECTIVES
- `${ANALYST_SCORE}` → Replace with the number stored in ANALYST_SCORE
- `${ANALYST_FEEDBACK}` → Replace with the text stored in ANALYST_FEEDBACK

## Step 1: Initialize Planning Loop

**Initialize the MCP refinement loop for strategic planning:**

Use the MCP tool `initialize_refinement_loop`:
- Call `initialize_refinement_loop(loop_type='plan')`
- Store the returned `PLAN_LOOP_ID` for tracking throughout the plan refinement process

**Set initial context:**
- Use `$ARGUMENTS` as initial conversation context
- If no arguments provided, start with: "I need help creating a strategic plan for my project"
- Set PREVIOUS_FEEDBACK as empty string

## Step 2: Conversational Requirements Gathering

**Use the /plan-conversation command to conduct conversational discovery.**

Collect all responses in structured format:
```json
{
  "vision": {
    "problem_statement": "...",
    "desired_outcome": "...",
    "success_metrics": "..."
  },
  "business_context": {
    "business_drivers": "...",
    "stakeholder_needs": "...",
    "organizational_constraints": "..."
  },
  "requirements": {
    "functional": [...],
    "user_experience": [...],
    "integration": [...],
    "performance": [...],
    "security": [...],
    "technical_constraints": [...]
  },
  "constraints": {
    "timeline": [...],
    "resource": [...],
    "business": [...],
    "technical": [...]
  },
  "priorities": {
    "must_have": [...],
    "nice_to_have": [...]
  }
}
```

Store complete conversation as CONVERSATION_CONTEXT.

## Step 3: Create Strategic Plan Document

**Transform conversation context into a strategic plan document:**

Using the structured `CONVERSATION_CONTEXT` from /plan-conversation, create a comprehensive strategic plan document with the following sections:

**Strategic Plan Template:**
```markdown
# Strategic Plan: [Project Name from conversation]

## Executive Summary
[High-level overview from vision section]

## Business Context
[Problem statement and business drivers from conversation]

## Business Objectives
[Specific, measurable goals extracted from conversation]

## Functional Requirements
[Core features and capabilities from requirements section]

## Technical Constraints
[Integration and technology limitations from constraints]

## Success Criteria
[Quantitative metrics and qualitative goals from success_metrics]

## Risk Assessment
[Potential challenges and mitigation strategies]

## Timeline Considerations
[Phased approach from timeline constraints]

## Resource Requirements
[Team, infrastructure, budget from resource constraints]
```

**Process the CONVERSATION_CONTEXT:**
1. **Extract information** from each JSON section in CONVERSATION_CONTEXT
2. **Structure into strategic plan format** using the template above
3. **Incorporate previous feedback** if PREVIOUS_FEEDBACK is not empty
4. **Store the complete strategic plan as CURRENT_PLAN**

## Step 4: Quality Assessment

Invoke the plan-critic agent with this context:

```text
Strategic Plan:
${CURRENT_PLAN}
```

**Parse the plan-critic response:**
1. **Extract QUALITY_SCORE:**
   - Look for "SCORE:" anywhere in response (case-insensitive)
   - Extract the number following "SCORE:" (should be 0-100)
   - Handle variations: "Score: 85", "SCORE: 85", "Quality Score: 85"
   - Store as QUALITY_SCORE variable
2. **Extract CRITIC_FEEDBACK:**
   - Look for "FEEDBACK:" anywhere in response (case-insensitive)
   - Extract all text after "FEEDBACK:" until end or next section
   - Handle variations: "Feedback:", "FEEDBACK:", "Improvement feedback:"
   - Store as CRITIC_FEEDBACK variable
3. **Validate extraction:**
   - Verify QUALITY_SCORE is an integer between 0-100
   - Verify CRITIC_FEEDBACK is not empty
   - If parsing fails, retry the plan-critic with the same context

## Step 5: Refinement Loop

**Call the MCP Server for next action decision:**

Use the MCP tool `decide_loop_next_action`:
- Call `decide_loop_next_action(LOOP_ID=${PLAN_LOOP_ID}, current_score=${QUALITY_SCORE})`
- The MCP Server will determine the next action based on configured criteria
- Store the returned status as PLAN_LOOP_STATUS
- Display the quality score and MCP decision to the user

**Process the MCP Server decision:**

**If status is "refine":**
- Set PREVIOUS_FEEDBACK = CRITIC_FEEDBACK
- Update CONVERSATION_CONTEXT by appending: "\\n\\nRefinement needed: " + CRITIC_FEEDBACK
- Continue to the next iteration of the loop (return to Step 3)

**If status is "user_input":**
- The MCP Server has detected stagnation in the refinement process
- Present the current quality score and areas needing clarification to the user
- Request specific user input with this structured message format:

```text
## Strategic Planning Input Required

**Current Status:**
- Quality Score: ${QUALITY_SCORE}%
- Refinement Iteration: [Current iteration number]
- Stagnation Point Detected: Score improvement has plateaued

**Areas Requiring Clarification:**

### Critical Issues (Score Impact: High)
${CRITIC_FEEDBACK}

### Guidance Questions
To help improve the plan quality, please address one or more of these areas:

1. **Requirements Clarification**: Are there missing requirements or constraints we should consider?
2. **Priority Adjustment**: Should we re-prioritize any objectives based on business needs?
3. **Scope Refinement**: Should we expand or narrow the project scope?
4. **Success Criteria**: Do the current success metrics accurately reflect your goals?
5. **Risk Assessment**: Are there additional risks or mitigation strategies to consider?

**Your Response:**
Please provide specific details for the areas that need clarification above.
```

- Wait for user response
- Update CONVERSATION_CONTEXT by appending: "\\n\\nUser clarification: " + user_response
- Set PREVIOUS_FEEDBACK = "Incorporate user's clarification into the plan focusing on: " + user_response
- Continue the refinement loop (return to Step 3)

**If status is "completed":**
- Display completion message with final quality score
- Exit the refinement loop and proceed to Step 6

## Error Recovery and Resilience

### Agent Invocation Failures

**strategic plan creation failures:**
1. **Empty or Invalid Context**: If CONVERSATION_CONTEXT is empty or malformed:
   - Retry /plan-conversation command with same initial context
   - If second attempt fails, continue with placeholder: "Plan creation failed - proceeding with basic template"
   - Update CURRENT_PLAN with failure notification for critic evaluation

2. **Context Overflow**: If CONVERSATION_CONTEXT exceeds processing limits:
   - Trigger context summarization: Extract key points from CONVERSATION_CONTEXT
   - Create strategic plan with summarized context (max 2000 characters)
   - If still fails, proceed with minimal template-based planning

3. **Template Processing Errors**: If strategic plan template cannot be populated:
   - Continue with basic markdown structure
   - Document template failure in CURRENT_PLAN output
   - Notify user of reduced functionality

**plan-critic failures:**
1. **Score Extraction Failure**: If QUALITY_SCORE cannot be parsed:
   - Use fallback score for MCP decision processing
   - Set CRITIC_FEEDBACK = "Critic assessment failed - manual review required"
   - Continue refinement loop with manual oversight

2. **Empty Feedback**: If CRITIC_FEEDBACK is empty or unparsable:
   - Set CRITIC_FEEDBACK = "General improvement needed - refine based on FSDD framework"
   - Continue with generic refinement guidance

**plan-analyst failures:**
1. **Objective Extraction Failure**: If plan-analyst returns invalid structure:
   - Retry once with explicit format requirements
   - If still fails, provide manual objective extraction template
   - Continue with basic objective structure

### MCP Tool Failures

**initialize_refinement_loop failures:**
1. **Loop Creation Error**: If LOOP_ID generation fails:
   - Generate local tracking ID (timestamp-based)
   - Continue without MCP loop management
   - Use fallback decision logic without MCP guidance

2. **Server Unavailable**: If MCP server is unreachable:
   - Fall back to local loop management
   - Display warning: "MCP loop management unavailable - using local fallback"

**decide_loop_next_action failures:**
1. **Decision Service Error**: If decision cannot be retrieved:
   - Apply basic fallback decision logic based on previous iteration patterns
   - Continue with fallback decision
   - Log decision reasoning for user

### Context Management Edge Cases

**Context Window Exhaustion:**
1. **Warning Threshold (80% capacity)**: 
   - Trigger progressive summarization of CONVERSATION_CONTEXT
   - Preserve most recent 20% and highest-priority 30% of content
   - Continue with condensed context

2. **Critical Threshold (95% capacity)**:
   - Emergency context compression: Keep only current iteration data
   - Store full context in CURRENT_PLAN for persistence
   - Notify user of context limitation

3. **Context Loss Recovery**:
   - If context is lost during processing, attempt recovery from CURRENT_PLAN
   - Use plan-analyst to reconstruct key requirements
   - Continue with reconstructed minimal context

**Variable State Corruption:**
1. **Missing Variables**: If any tracked variable becomes undefined:
   - Reinitialize with safe defaults
   - Attempt recovery from previous agent outputs
   - Continue with recovered or default values

2. **Invalid Variable Types**: If variables contain unexpected data types:
   - Clean and convert to expected format
   - Log data cleaning actions
   - Continue with sanitized variables

## Step 6: Initialize Analyst Validation Loop

**Initialize the MCP refinement loop for analyst validation:**

Use the MCP tool `initialize_refinement_loop`:
- Call `initialize_refinement_loop(loop_type='analyst')`
- Store the returned `ANALYST_LOOP_ID` for tracking throughout the analyst validation process

## Step 7: Extract Objectives

After plan loop completion, invoke the plan-analyst agent with this context:

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

## Step 8: Analyst Quality Assessment

Invoke the analyst-critic agent with this context:

```text
Business Objectives Analysis:
${STRUCTURED_OBJECTIVES}

Original Strategic Plan:
${CURRENT_PLAN}
```

**Parse the analyst-critic response:**
1. **Extract ANALYST_SCORE:**
   - Look for "SCORE:" anywhere in response (case-insensitive)
   - Extract the number following "SCORE:" (should be 0-100)
   - Handle variations: "Score: 85", "SCORE: 85", "Analysis Score: 85"
   - Store as ANALYST_SCORE variable
2. **Extract ANALYST_FEEDBACK:**
   - Look for "FEEDBACK:" anywhere in response (case-insensitive)
   - Extract all text after "FEEDBACK:" until end or next section
   - Handle variations: "Feedback:", "FEEDBACK:", "Validation feedback:"
   - Store as ANALYST_FEEDBACK variable
3. **Validate extraction:**
   - Verify ANALYST_SCORE is an integer between 0-100
   - Verify ANALYST_FEEDBACK is not empty
   - If parsing fails, retry the analyst-critic with the same context

## Step 9: Analyst Validation Loop

**Call the MCP Server for analyst validation decision:**

Use the MCP tool `decide_loop_next_action`:
- Call `decide_loop_next_action(LOOP_ID=${ANALYST_LOOP_ID}, current_score=${ANALYST_SCORE})`
- The MCP Server will determine the next action based on configured criteria
- Store the returned status as ANALYST_LOOP_STATUS
- Display the analyst score and MCP decision to the user

**Process the MCP Server decision:**

**If status is "refine":**
- Store current objectives: `store_current_objective_feedback(ANALYST_LOOP_ID, STRUCTURED_OBJECTIVES, ANALYST_SCORE, ANALYST_FEEDBACK)`
- Set previous feedback context for plan-analyst refinement
- Re-invoke plan-analyst with refined context (return to Step 7)

**If status is "user_input":**
- Present current analyst score and request user clarification
- Wait for user response and incorporate into objectives analysis
- Continue analyst validation loop (return to Step 7)

**If status is "completed":**
- Store final objectives: `store_current_objective_feedback(ANALYST_LOOP_ID, STRUCTURED_OBJECTIVES, ANALYST_SCORE, ANALYST_FEEDBACK)`
- Display completion message with final analyst score
- Proceed to final output

## Final Output Format
```markdown
# Strategic Plan Output

## Plan Quality
- Final Plan Score: ${QUALITY_SCORE}%
- Plan Completion Status: ${PLAN_LOOP_STATUS}
- Plan Loop Result: ${PLAN_LOOP_STATUS}

## Analyst Validation
- Final Analyst Score: ${ANALYST_SCORE}%
- Analyst Completion Status: ${ANALYST_LOOP_STATUS}
- Analyst Loop Result: ${ANALYST_LOOP_STATUS}

## Strategic Plan Document
${CURRENT_PLAN}

## Structured Objectives
${STRUCTURED_OBJECTIVES}

## Next Steps
1. Review the strategic plan for accuracy
2. Proceed with technical specification using: /spec
3. The structured objectives will feed directly into spec-architect

## Metadata
- Plan Loop ID: ${PLAN_LOOP_ID}
- Analyst Loop ID: ${ANALYST_LOOP_ID}
- Timestamp: [current date/time]
```
"""
