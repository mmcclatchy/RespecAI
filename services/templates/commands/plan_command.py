from services.models.project_plan import ProjectPlan
from services.models.plan_completion_report import PlanCompletionReport


# Create template instance with instructional placeholders
project_plan_template = ProjectPlan(
    project_name='[Project Name from conversation]',
    project_vision='[High-level project vision from conversation]',
    project_mission='[Project mission statement from conversation]',
    project_timeline='[Phased approach from timeline constraints]',
    project_budget='[Budget considerations from resource constraints]',
    primary_objectives='[Specific, measurable goals extracted from conversation]',
    success_metrics='[Quantitative metrics and qualitative goals from success_metrics]',
    key_performance_indicators='[Key metrics to track project success]',
    included_features='[Core features and capabilities from requirements section]',
    excluded_features='[Features explicitly excluded from scope]',
    project_assumptions='[Key assumptions underlying the project plan]',
    project_constraints='[Integration and technology limitations from constraints]',
    project_sponsor='[Project sponsor identified from stakeholder discussion]',
    key_stakeholders='[Primary stakeholders from conversation context]',
    end_users='[Target users and user groups from requirements]',
    work_breakdown='[High-level work breakdown from project structure discussion]',
    phases_overview='[Project phases from timeline and scope conversation]',
    project_dependencies='[Dependencies identified from requirements and constraints]',
    team_structure='[Team composition from resource requirements discussion]',
    technology_requirements='[Technology stack from technical constraints]',
    infrastructure_needs='[Infrastructure requirements from resource discussion]',
    identified_risks='[Potential challenges and risks from conversation]',
    mitigation_strategies='[Risk mitigation approaches from discussion]',
    contingency_plans='[Backup plans for major risks identified]',
    quality_standards='[Quality requirements from success criteria discussion]',
    testing_strategy='[Testing approach from quality requirements]',
    acceptance_criteria='[Acceptance criteria from success metrics discussion]',
    reporting_structure='[Reporting needs from stakeholder discussion]',
    meeting_schedule='[Communication cadence from project management discussion]',
    documentation_standards='[Documentation requirements from quality standards]',
).build_markdown()

# Create completion report template instance with instructional placeholders
plan_completion_template = PlanCompletionReport(
    final_plan_score='${QUALITY_SCORE}',
    user_decision='${USER_DECISION}',
    final_analyst_score='${ANALYST_SCORE}',
    analyst_completion_status='${ANALYST_LOOP_STATUS}',
    analyst_loop_result='${ANALYST_LOOP_STATUS}',
    strategic_plan_document='${CURRENT_PLAN}',
    structured_objectives='${STRUCTURED_OBJECTIVES}',
    analyst_loop_id='${ANALYST_LOOP_ID}',
    completion_timestamp='[current date/time]',
).build_markdown()


def generate_plan_command_template() -> str:
    return f"""---
allowed-tools:
  - Task(plan-conversation)
  - Task(plan-critic)
  - Task(plan-analyst)
  - Task(analyst-critic)
  - mcp__specter__initialize_refinement_loop
  - mcp__specter__decide_loop_next_action
  - mcp__specter__get_previous_objective_feedback
  - mcp__specter__store_current_objective_feedback
  - mcp__specter__store_project_plan
  - mcp__specter__get_project_plan_markdown
  - mcp__specter__store_conversation_context
  - mcp__specter__store_critic_feedback
  - mcp__specter__get_previous_feedback
  - mcp__specter__store_current_analysis
  - mcp__specter__get_previous_analysis
  - mcp__specter__create_plan_completion_report
  - mcp__specter__store_plan_completion_report
  - mcp__specter__get_plan_completion_report_markdown
  - mcp__specter__update_plan_completion_report
argument-hint: [plan-name] [starting-prompt]
description: Orchestrate strategic planning workflow
---

# Strategic Planning Orchestration

## Variable Management
**Throughout the command execution, maintain these variables:**

- **PLAN_LOOP_ID**: String returned from MCP `mcp__specter__initialize_refinement_loop('plan')` - store and use for plan loop MCP calls
- **ANALYST_LOOP_ID**: String returned from MCP `mcp__specter__initialize_refinement_loop('analyst')` - store and use for analyst loop MCP calls
- **CONVERSATION_CONTEXT**: Accumulated conversation text - starts with `$ARGUMENTS` or default prompt
- **CURRENT_PLAN**: Strategic plan document created from conversation context
- **QUALITY_SCORE**: Integer from plan-critic (0-100) - extracted from critic response
- **CRITIC_FEEDBACK**: String with improvement suggestions - extracted from critic response
- **USER_DECISION**: String from user choice - values: "continue_conversation", "refine_plan", "accept_plan"
- **STRUCTURED_OBJECTIVES**: Business objectives analysis from plan-analyst
- **ANALYST_SCORE**: Integer from analyst-critic (0-100) - extracted from analyst-critic response
- **ANALYST_FEEDBACK**: String with validation suggestions - extracted from analyst-critic response
- **ANALYST_LOOP_STATUS**: String from MCP decision - values: "refine", "user_input", "completed"

**Variable Update Pattern:**
- After strategic plan creation: Update `CURRENT_PLAN`
- After plan-critic: Update `QUALITY_SCORE` and `CRITIC_FEEDBACK`
- After user decision: Update `USER_DECISION`
- After plan-analyst: Update `STRUCTURED_OBJECTIVES`
- After analyst-critic: Update `ANALYST_SCORE` and `ANALYST_FEEDBACK`
- After analyst MCP decision: Update `ANALYST_LOOP_STATUS`
- Before refinement: Update `CONVERSATION_CONTEXT` with user guidance

**Variable Interpolation:**
When you see `${{variable_name}}` in prompts or templates, replace it with the actual content of that variable:
- `${{CONVERSATION_CONTEXT}}` → Replace with the full text stored in CONVERSATION_CONTEXT
- `${{PREVIOUS_FEEDBACK}}` → Replace with the text stored in PREVIOUS_FEEDBACK
- `${{CURRENT_PLAN}}` → Replace with the text stored in CURRENT_PLAN
- `${{QUALITY_SCORE}}` → Replace with the number stored in QUALITY_SCORE
- `${{CRITIC_FEEDBACK}}` → Replace with the text stored in CRITIC_FEEDBACK
- `${{PLAN_LOOP_ID}}` → Replace with the string stored in PLAN_LOOP_ID
- `${{ANALYST_LOOP_ID}}` → Replace with the string stored in ANALYST_LOOP_ID
- `${{STRUCTURED_OBJECTIVES}}` → Replace with the text stored in STRUCTURED_OBJECTIVES
- `${{ANALYST_SCORE}}` → Replace with the number stored in ANALYST_SCORE
- `${{ANALYST_FEEDBACK}}` → Replace with the text stored in ANALYST_FEEDBACK

## Step 1: Initialize Conversation Context

**Set up the conversational planning workflow:**

**Set initial context:**
- Use `$ARGUMENTS` as initial conversation context
- If no arguments provided, start with: "I need help creating a strategic plan for my project"
- Initialize plan loop using MCP: `mcp__specter__initialize_refinement_loop(loop_type='plan')`
- Store the returned loop ID as PLAN_LOOP_ID for tracking throughout the planning process
- Initialize variables for state management throughout the human-driven process

## Step 2: Conversational Requirements Gathering

**Use the /plan-conversation command to conduct conversational discovery.**

Collect all responses in structured format:
```json
{{'vision': {{'problem_statement': "...",
    "desired_outcome": "...",
    "success_metrics": "..."
  }},
  "business_context": {{'business_drivers': "...",
    "stakeholder_needs": "...",
    "organizational_constraints": "..."
  }},
  "requirements": {{'functional': [...],
    "user_experience": [...],
    "integration": [...],
    "performance": [...],
    "security": [...],
    "technical_constraints": [...]
  }},
  "constraints": {{'timeline': [...],
    "resource": [...],
    "business": [...],
    "technical": [...]
  }},
  "priorities": {{'must_have': [...],
    "nice_to_have": [...]
  }}
}}
```

Store complete conversation as CONVERSATION_CONTEXT.

## Step 3: Create Strategic Plan Document

**Transform conversation context into a strategic plan document:**

Using the structured `CONVERSATION_CONTEXT` from /plan-conversation, create a comprehensive strategic plan document with the following sections:

**Strategic Plan Template:**
```markdown
{project_plan_template}
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
${{CURRENT_PLAN}}
```

**Store and parse the plan-critic response using MCP feedback tools:**
1. **Store the critic feedback:**
   - Store the critic response markdown using: `store_critic_feedback(PLAN_LOOP_ID, plan_critic_response_markdown)`
   - The MCP tool will parse the CriticFeedback markdown format automatically
   - Extract QUALITY_SCORE from the parsed feedback: access the overall_score field
   - Extract CRITIC_FEEDBACK from the parsed feedback: access the detailed_feedback field
2. **Validate parsing:**
   - Verify the MCP tool successfully stored the feedback
   - Verify QUALITY_SCORE is an integer between 0-100 from the parsed result
   - Verify CRITIC_FEEDBACK contains meaningful content from the parsed result
   - If parsing fails, retry the plan-critic with the same context

## Step 5: Present Quality Assessment and User Decision

**Present the quality assessment to the user:**

Display the plan quality results in a clear, actionable format:

```text
## Strategic Plan Quality Assessment

**Plan Overview:**
- Project: [Plan name/title from CURRENT_PLAN]
- Quality Score: ${{QUALITY_SCORE}}%

**Quality Summary:**
${{CRITIC_FEEDBACK}}

**Your Options:**

1. **Continue conversation** - Add more details through additional /plan-conversation
   - Best if: Missing requirements, unclear scope, or need more context
   - Action: Return to conversational discovery for specific areas

2. **Refine plan** - Generate improved version addressing feedback
   - Best if: Content exists but needs better organization or clarity
   - Action: Create new strategic plan version with targeted improvements

3. **Accept plan** - Proceed with current plan to objective extraction
   - Best if: Plan meets your needs and you're ready to move forward
   - Action: Continue to automated objective validation phase

**Please choose your preferred option (1, 2, or 3):**
```

**Wait for user response and process decision:**

**If user chooses "1" (Continue conversation):**
- Set USER_DECISION = "continue_conversation"
- Return to Step 2 with existing CONVERSATION_CONTEXT
- Use conversation context to continue where previous conversation left off

**If user chooses "2" (Refine plan):**
- Set USER_DECISION = "refine_plan"
- Update CONVERSATION_CONTEXT by appending: "\\n\\nRefinement needed: " + CRITIC_FEEDBACK
- Return to Step 3 to generate improved strategic plan

**If user chooses "3" (Accept plan):**
- Set USER_DECISION = "accept_plan"
- Store the current plan using MCP tool `mcp__specter__store_project_plan(project_plan_markdown=${{CURRENT_PLAN}})`
- Proceed to Step 6 for automated objective extraction

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

**mcp__specter__initialize_refinement_loop failures:**
1. **Loop Creation Error**: If LOOP_ID generation fails:
   - Generate local tracking ID (timestamp-based)
   - Continue without MCP loop management
   - Use fallback decision logic without MCP guidance

2. **Server Unavailable**: If MCP server is unreachable:
   - Fall back to local loop management
   - Display warning: "MCP loop management unavailable - using local fallback"

**mcp__specter__decide_loop_next_action failures:**
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

Use the MCP tool `mcp__specter__initialize_refinement_loop`:
- Call `mcp__specter__initialize_refinement_loop(loop_type='analyst')`
- Store the returned `ANALYST_LOOP_ID` for tracking throughout the analyst validation process

## Step 7: Extract Objectives

After plan loop completion, invoke the plan-analyst agent with this context:

```text
Strategic Plan:
${{CURRENT_PLAN}}
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
${{STRUCTURED_OBJECTIVES}}

Original Strategic Plan:
${{CURRENT_PLAN}}
```

**Store and parse the analyst-critic response using MCP feedback tools:**
1. **Store the analyst-critic feedback:**
   - Store the critic response markdown using: `store_critic_feedback(ANALYST_LOOP_ID, analyst_critic_response_markdown)`
   - The MCP tool will parse the CriticFeedback markdown format automatically
   - Extract ANALYST_SCORE from the parsed feedback: access the overall_score field
   - Extract ANALYST_FEEDBACK from the parsed feedback: access the detailed_feedback field
2. **Validate parsing:**
   - Verify the MCP tool successfully stored the feedback
   - Verify ANALYST_SCORE is an integer between 0-100 from the parsed result
   - Verify ANALYST_FEEDBACK contains meaningful content from the parsed result
   - If parsing fails, retry the analyst-critic with the same context

## Step 9: Analyst Validation Loop

**Call the MCP Server for analyst validation decision:**

Use the MCP tool `mcp__specter__decide_loop_next_action`:
- Call `mcp__specter__decide_loop_next_action(LOOP_ID=${{ANALYST_LOOP_ID}}, current_score=${{ANALYST_SCORE}})`
- The MCP Server will determine the next action based on configured criteria
- Store the returned status as ANALYST_LOOP_STATUS
- Display the analyst score and MCP decision to the user

**Process the MCP Server decision:**

**If status is "refine":**
- Store current objectives: `mcp__specter__store_current_objective_feedback(ANALYST_LOOP_ID, STRUCTURED_OBJECTIVES, ANALYST_SCORE, ANALYST_FEEDBACK)`
- Set previous feedback context for plan-analyst refinement
- Re-invoke plan-analyst with refined context (return to Step 7)

**If status is "user_input":**
- Present current analyst score and request user clarification
- Wait for user response and incorporate into objectives analysis
- Continue analyst validation loop (return to Step 7)

**If status is "completed":**
- Store final objectives: `mcp__specter__store_current_objective_feedback(ANALYST_LOOP_ID, STRUCTURED_OBJECTIVES, ANALYST_SCORE, ANALYST_FEEDBACK)`
- Generate completion report markdown by substituting template variables with actual values
- Store completion report: `mcp__specter__store_plan_completion_report(ANALYST_LOOP_ID, completion_report_markdown)`
- Display completion message with final analyst score
- Present final output using the stored completion report

## Final Output Format
```markdown
{plan_completion_template}
```
"""
