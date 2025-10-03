# Specter-Spec Workflow Optimization Implementation Guide

---

**📋 IMPLEMENTATION STATUS**: Specification Complete - Implementation Pending

**FOR IMPLEMENTERS**: This document describes the OPTIMAL final state of the specter-spec workflow. For concrete implementation tasks, jump directly to the [Implementation Checklist](#implementation-checklist) section.

**⚡ QUICK START** - If you're implementing this workflow:
1. **Context** (5 min): Read [Executive Summary](#executive-summary) to understand the optimization
2. **Visualization** (3 min): Review [Data Flow Diagram](#data-flow-diagram) for the complete flow
3. **Execute** (2-3 hours): Complete tasks in [Implementation Checklist](#implementation-checklist) order
4. **Validate** (30 min): Verify using [Validation Criteria](#validation-criteria)

**📊 COMPLETION TRACKER**:
- ✅ Analysis Complete
- ✅ Optimal Workflow Defined (20 steps, down from 24)
- ✅ MCP Tools Verified (all exist and are correctly named)
- 🚧 Command Specification - Pending
- 🚧 Agent Specifications - Pending
- 🚧 Integration Testing - Pending

---

## Document Purpose

This implementation guide provides a comprehensive blueprint for refining the `/specter-spec` workflow into an optimal state with clear responsibility boundaries and tight actor-to-actor handshakes. It consolidates the analysis of existing MCP infrastructure and defines the complete workflow from user invocation to platform storage.

**What This Document Provides**:
- ✅ Complete 20-step optimized workflow specification
- ✅ Responsibility boundaries for all actors
- ✅ Data flow diagrams with handshakes
- ✅ Tool usage patterns
- ✅ Concrete implementation tasks with file paths
- ✅ Validation criteria for verification

## Executive Summary

### Current State vs Optimized State

**Previous Issues**:
- Missing InitialSpec retrieval (starter template not used)
- Incorrect MCP tool naming conventions
- Unclear responsibility boundaries between actors
- Loose handshakes with implicit state assumptions
- Command used `project_id` instead of user-friendly `project_name`

**Optimized Solution**:
- InitialSpec retrieved first as requirements baseline
- All MCP tools use `mcp__specter__` namespace
- Clear responsibility matrix per actor
- Explicit handshakes with defined inputs/outputs
- User-friendly `project_name` parameter

### Infrastructure Leveraged

**Existing MCP Tools**:
- Loop management: 7 tools for state tracking and decisions
- Feedback system: 2 tools for history and storage
- Specification system: 4 tools for spec storage and retrieval
- Roadmap system: 6 tools for InitialSpec management
- Project plan system: 5 tools for strategic context

**Key Innovation**: Complete workflow operates through MCP Server with zero implicit state.

---

## Implementation Checklist

This section provides concrete, actionable tasks for implementing the optimized workflow. Complete these in order.

### ✅ Prerequisites (Already Complete)

- ✅ All MCP tools exist and are correctly named with `mcp__specter__` prefix
- ✅ Loop management infrastructure in place
- ✅ Feedback system operational
- ✅ Specification storage system working
- ✅ Roadmap system with InitialSpec support active

### 🚧 Priority 1: Update Command Specification

**File**: [docs/commands/specter-spec.md](../commands/specter-spec.md)
**Status**: 🚧 Not Started
**Estimated Time**: 30-45 minutes

**Required Changes**:

1. **Update Command Signature** (Line ~10)
   ```markdown
   BEFORE:
   /specter-spec [focus]

   AFTER:
   /specter-spec <project_name> <spec_name> [focus]
   ```

2. **Add Parameter Descriptions**
   - `project_name`: User-friendly project identifier (same value as project_id)
   - `spec_name`: Specification phase name (e.g., "Phase 1: Core API")
   - `focus`: Optional technical area emphasis (e.g., "API design")

3. **Update Workflow Description** (Main workflow section)
   - Change from 24-step to 20-step process
   - Remove old Step 6: "spec-architect retrieves InitialSpec via MCP"
   - Remove old Step 11: "Main Agent retrieves spec after storing"
   - Update Step 16B: Architect returns markdown, Main Agent stores (loop to Steps 8→9)
   - Reference this document's [Complete Workflow](#complete-workflow-20-step-process) section

4. **Add Critical Notes**
   - Note: `project_id` equals `project_name` in this system
   - Note: Architect receives InitialSpec from Main Agent, does NOT retrieve via MCP
   - Note: Main Agent keeps TechnicalSpec markdown from Step 8 to pass to critic (no retrieval needed)

**Validation Criteria**:
- [ ] Command signature shows `<project_name> <spec_name> [focus]`
- [ ] Workflow references 20 steps (not 24)
- [ ] No mention of architect calling `mcp__specter__get_spec`
- [ ] No mention of Main Agent calling `get_technical_spec_markdown` between storing and critic invocation

---

### 🚧 Priority 2: Update spec-architect Agent Specification

**File**: [docs/agents/spec-architect.md](../agents/spec-architect.md)
**Status**: 🚧 Not Started
**Estimated Time**: 45-60 minutes

**Required Changes**:

1. **Remove Retrieval Step** (Currently around line 143-158 in old doc)
   ```markdown
   DELETE THIS ENTIRE STEP:
   #### Step 6: spec-architect - Retrieve InitialSpec
   **Action**: Call mcp__specter__get_spec(project_id, spec_name)
   [entire step removed]
   ```

2. **Update Initial Step** (First step in agent workflow)
   ```markdown
   REPLACE:
   #### Step 1: Retrieve InitialSpec baseline

   WITH:
   #### Step 1: Use Provided InitialSpec
   **Action**: Use InitialSpec markdown provided by Main Agent
   **Source**: InitialSpec passed by Main Agent in invocation
   **Note**: Do NOT retrieve InitialSpec via MCP - use what was passed
   ```

3. **Update Invocation Context** (Near top of document)
   ```markdown
   ADD TO INVOCATION SECTION:

   ### Inputs Received from Main Agent:
   - loop_id: For tracking this refinement loop
   - project_id: Project identifier
   - spec_name: Specification phase name
   - **InitialSpec markdown**: Requirements baseline (DO NOT retrieve via MCP)
   - **ProjectPlan markdown**: Strategic context (DO NOT retrieve via MCP)
   - focus: Optional technical area (if provided)
   - iteration: Current iteration number
   - feedback_history: Only for iterations > 1
   ```

4. **Update Tool Permissions Section**
   ```markdown
   BEFORE:
   **Tool Permissions**:
   - mcp__specter__get_spec (read InitialSpec)
   - Bash (archive scanning)
   - Read, Grep, Glob (archive access)
   - mcp__specter__get_feedback_history (iterations > 1)

   AFTER:
   **Tool Permissions**:
   - Bash (archive scanning)
   - Read, Grep, Glob (archive access)
   - mcp__specter__get_feedback_history (iterations > 1, for retrieving latest feedback)

   **NOT Permitted**:
   - mcp__specter__get_spec (InitialSpec provided by Main Agent)
   - mcp__specter__store_technical_spec (Main Agent's responsibility)
   ```

5. **Update Primary Responsibilities**
   ```markdown
   CHANGE:
   - Retrieve InitialSpec baseline

   TO:
   - Use InitialSpec baseline provided by Main Agent
   ```

6. **Add Critical Boundary Note**
   ```markdown
   ADD TO RESPONSIBILITY BOUNDARY SECTION:

   **Critical Design Points**:
   - Architect receives InitialSpec from Main Agent, does NOT retrieve it via MCP
   - Architect GENERATES TechnicalSpec markdown, Main Agent STORES it
   - Architect RETURNS markdown to Main Agent, does NOT call store_technical_spec
   ```

**Validation Criteria**:
- [ ] No step mentions calling `mcp__specter__get_spec`
- [ ] Invocation section lists InitialSpec as input
- [ ] Tool permissions do NOT include `get_spec`
- [ ] Responsibilities section says "Use InitialSpec provided" not "Retrieve InitialSpec"
- [ ] Critical boundary notes are present

---

### 🚧 Priority 3: Update spec-critic Agent Specification

**File**: [docs/agents/spec-critic.md](../agents/spec-critic.md)
**Status**: 🚧 Not Started
**Estimated Time**: 30-45 minutes

**Required Changes**:

1. **Add Feedback History Retrieval Step** (Add as first workflow step)
   ```markdown
   ADD AS FIRST STEP:

   #### Step 1: Retrieve Feedback History
   **Action**: Call mcp__specter__get_feedback_history(loop_id, count=3)
   **Purpose**: Load previous assessments for consistency and trend analysis
   **Inputs**:
   - loop_id: Provided by Main Agent
   - count: 3 (retrieve last 3 feedback items)
   **Outputs**:
   - List of recent CriticFeedback items (empty if first iteration)
   - Previous scores and recommendations
   **Note**: First iteration returns empty list - this is normal
   ```

2. **Update Invocation Context**
   ```markdown
   ADD TO INPUTS SECTION:

   ### Inputs Received from Main Agent:
   - loop_id: For tracking and retrieving feedback history
   - TechnicalSpec markdown: Specification to evaluate
   - iteration: Current iteration number (for context)

   **Note**: Main Agent passes TechnicalSpec markdown directly (from Step 8).
   Main Agent does NOT retrieve it from MCP after storing.
   ```

3. **Add Feedback Storage Step** (After feedback generation)
   ```markdown
   ADD STEP:

   #### Step [N]: Store Feedback
   **Action**: Call mcp__specter__store_critic_feedback(loop_id, feedback_markdown)
   **Purpose**: Persist feedback in MCP Server loop state
   **Inputs**:
   - loop_id: Provided by Main Agent
   - feedback_markdown: CriticFeedback generated in previous step
   **Outputs**:
   - Parsed CriticFeedback stored in LoopState.feedback_history
   - Score automatically added to LoopState.score_history
   - LoopStatus updated to IN_PROGRESS
   **Critical**: Critic stores feedback DIRECTLY, not through Main Agent
   ```

4. **Update Tool Permissions**
   ```markdown
   BEFORE:
   **Tool Permissions**:
   - None: Pure assessment agent

   AFTER:
   **Tool Permissions**:
   - mcp__specter__get_feedback_history (read history)
   - mcp__specter__store_critic_feedback (write feedback)

   **Restrictions**:
   - No file system access
   - No specification modification
   - No platform interaction
   ```

5. **Update Responsibilities**
   ```markdown
   ADD TO RESPONSIBILITIES:
   - Retrieve feedback history for context
   - Store feedback in MCP Server (NOT through Main Agent)

   UPDATE CRITICAL BOUNDARY:
   **Critical Boundary**:
   - Critic STORES feedback directly via MCP tool call
   - This ensures critic controls feedback format and timing
   - Main Agent does NOT store feedback on behalf of critic
   ```

**Validation Criteria**:
- [ ] First step retrieves feedback history via `get_feedback_history`
- [ ] Workflow includes step to call `store_critic_feedback`
- [ ] Invocation section lists loop_id as input
- [ ] Tool permissions include both `get_feedback_history` and `store_critic_feedback`
- [ ] Responsibilities mention storing feedback directly

---

### 🚧 Priority 4: Create Integration Test Plan

**File**: NEW - `docs/testing/specter-spec-integration-test.md`
**Status**: 🚧 Not Started
**Estimated Time**: 1-2 hours

**Test Scenarios**:

1. **Happy Path - First Iteration Passes**
   - Invoke `/specter-spec test-project "Phase 1"`
   - Verify InitialSpec retrieved once
   - Verify architect does NOT call get_spec
   - Verify Main Agent passes markdown to critic (no retrieval)
   - Verify critic stores feedback
   - Verify score ≥ 85 triggers COMPLETED

2. **Refinement Path - Multiple Iterations**
   - Invoke with spec that scores 70
   - Verify REFINE decision
   - Verify improvement analysis retrieved
   - Verify architect re-invoked with feedback
   - Verify loop returns to Steps 8→9 (architect returns, Main Agent stores)
   - Verify second iteration increments counter

3. **User Input Path - Stagnation**
   - Create scenario with 2 iterations < 5 point improvement
   - Verify USER_INPUT decision
   - Verify feedback summary retrieved
   - Verify user prompted

4. **Error Handling - Invalid InitialSpec**
   - Invoke with non-existent spec_name
   - Verify graceful error from Step 3

**Validation Criteria**:
- [ ] All 4 test scenarios documented
- [ ] Expected MCP tool call sequence defined
- [ ] Success criteria for each scenario clear

---

## Validation Criteria

Use this checklist to verify the implementation is correct.

### Command Specification Validation

**File**: `docs/commands/specter-spec.md`

- [ ] Command signature: `/specter-spec <project_name> <spec_name> [focus]`
- [ ] Parameters documented with examples
- [ ] Workflow description references 20 steps
- [ ] No mention of old redundant steps (6, 11)
- [ ] project_id = project_name relationship documented
- [ ] References this implementation guide

### Agent Specification Validation

**File**: `docs/agents/spec-architect.md`

- [ ] NO step calls `mcp__specter__get_spec`
- [ ] Invocation section shows InitialSpec as INPUT
- [ ] Tool permissions do NOT include `get_spec`
- [ ] Responsibilities say "Use InitialSpec provided by Main Agent"
- [ ] Critical boundary notes present
- [ ] Does NOT call `store_technical_spec`

**File**: `docs/agents/spec-critic.md`

- [ ] First workflow step retrieves feedback history
- [ ] Workflow includes step calling `store_critic_feedback`
- [ ] Tool permissions include `get_feedback_history`
- [ ] Tool permissions include `store_critic_feedback`
- [ ] Invocation section shows loop_id as INPUT
- [ ] Responsibilities mention storing feedback directly

### Integration Validation

- [ ] End-to-end test passes without errors
- [ ] Total MCP calls for single iteration: ~13 (down from ~15 in old workflow)
- [ ] No redundant get_spec call by architect
- [ ] No redundant get_technical_spec_markdown call between Steps 9-10
- [ ] Critic feedback appears in LoopState.feedback_history
- [ ] Score tracking works across iterations

---

## Before/After Examples

### Example 1: Command Signature

**Before** (docs/commands/specter-spec.md):
```markdown
## Usage

/specter-spec [focus]

Example:
/specter-spec "API design"
```

**After** (docs/commands/specter-spec.md):
```markdown
## Usage

/specter-spec <project_name> <spec_name> [focus]

**Parameters**:
- `project_name`: Project identifier (user-friendly name, equals project_id)
- `spec_name`: Specification phase name
- `focus`: Optional technical area emphasis

**Examples**:
/specter-spec best-practices-graph "Phase 1: Core API"
/specter-spec best-practices-graph "Phase 1: Core API" "API design"
```

---

### Example 2: Architect Workflow

**Before** (docs/agents/spec-architect.md):
```markdown
## Workflow

### Step 1: Retrieve InitialSpec
**Action**: Call mcp__specter__get_spec(project_id, spec_name)
**Purpose**: Fetch requirements baseline

### Step 2: Archive Research
**Action**: Execute archive scanning script
...
```

**After** (docs/agents/spec-architect.md):
```markdown
## Workflow

### Step 1: Use Provided Context
**Action**: Use InitialSpec and ProjectPlan provided by Main Agent
**Source**: Both documents passed in agent invocation
**Note**: Do NOT retrieve InitialSpec via MCP - use what was passed

### Step 2: Archive Research
**Action**: Execute archive scanning script
...
```

---

### Example 3: Critic Responsibilities

**Before** (docs/agents/spec-critic.md):
```markdown
## Responsibilities

- Evaluate against FSDD criteria
- Generate quality scores
- Create feedback markdown
```

**After** (docs/agents/spec-critic.md):
```markdown
## Responsibilities

- Retrieve feedback history for context
- Evaluate against FSDD criteria
- Generate quality scores
- Create feedback markdown
- **Store feedback in MCP Server** (directly, not through Main Agent)
```

---

## Complete Workflow: 20-Step Process

### Phase 1: Initialization (Steps 1-5)

#### Step 1: User Invocation
**Actor**: User
**Action**: Execute `/specter-spec <project_name> <spec_name> [focus]`
**Responsibility**: Trigger workflow with project context

**Inputs**:
- `project_name`: Project identifier (user-friendly name)
- `spec_name`: Specification phase name (e.g., "Phase 1: Core API")
- `focus` (optional): Technical area emphasis (e.g., "API design")

**Outputs**:
- Command activation signal to Main Agent

**Handshake**: Main Agent receives command with validated parameters

---

#### Step 2: Main Agent - Initialize Loop
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__initialize_refinement_loop(loop_type='spec')`
**Responsibility**: Create specification refinement loop state

**Inputs**:
- `loop_type`: "spec"

**Outputs**:
- `MCPResponse`:
  - `loop_id`: Unique identifier (e.g., "a3f8c9d1")
  - `status`: INITIALIZED

**Handshake**: Loop state created in MCP Server, loop_id stored for all subsequent operations

---

#### Step 3: Main Agent - Retrieve InitialSpec
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__get_spec(project_id, spec_name)`
**Responsibility**: Fetch starter specification template from roadmap

**Inputs**:
- `project_id`: In this system, project_id is the same as project_name (user-friendly identifier)
- `spec_name`: From user input

**Outputs**:
- InitialSpec markdown:
  - Phase name
  - Objectives (business requirements)
  - Scope boundaries
  - Dependencies
  - Deliverables
  - Status: DRAFT

**Handshake**: InitialSpec markdown passed to architect as requirements baseline

**Critical Design Point**: InitialSpec is the starter template created during roadmap phase. TechnicalSpec is the filled-out version produced by architect.

**Note on project_id**: The project_id parameter uses the same value as project_name. The system treats them as identical for simplicity.

---

#### Step 4: Main Agent - Retrieve Strategic Plan
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__get_project_plan_markdown(project_name)`
**Responsibility**: Fetch strategic context for technical decisions

**Inputs**:
- `project_name`: From user input

**Outputs**:
- ProjectPlan markdown:
  - Project vision
  - Business objectives
  - Success criteria
  - Constraints

**Handshake**: ProjectPlan markdown passed to architect for context

---

#### Step 5: Main Agent - Invoke spec-architect
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Launch `specter-spec-architect` agent via Task tool
**Responsibility**: Delegate technical design to specialized agent

**Inputs** (passed to architect):
- `loop_id`: From Step 2
- `project_id`: From Step 1 (derived)
- `spec_name`: From Step 1
- InitialSpec markdown: From Step 3
- ProjectPlan markdown: From Step 4
- `focus` (optional): From Step 1
- `iteration`: 1 (first iteration)
- `feedback_history`: None (first iteration)

**Outputs**:
- Agent activation signal

**Handshake**: Architect receives complete context bundle

---

### Phase 2: Architecture Design (Steps 6-9)

#### Step 6: spec-architect - Archive Research
**Actor**: `specter-spec-architect` agent
**Action**: Execute `~/.claude/scripts/research-advisor-archive-scan.sh`
**Responsibility**: Search best-practices archive for relevant patterns

**Inputs**:
- Technical keywords extracted from InitialSpec + ProjectPlan (both provided by Main Agent in Step 5)
- Archive script path

**Outputs**:
- List of matching archive documents (0-N)
- Document paths (e.g., `~/.claude/best-practices/event-driven-architecture.md`)

**Handshake**: Archive results inform research requirements section

**Error Handling**: If archive unavailable, continue without archive data, note in research section

**Note**: Architect uses InitialSpec provided by Main Agent in Step 5, does NOT retrieve it again via MCP.

---

#### Step 7: spec-architect - Create TechnicalSpec
**Actor**: `specter-spec-architect` agent
**Action**: Design comprehensive technical specification
**Responsibility**: Expand InitialSpec into complete TechnicalSpec

**Inputs**:
- InitialSpec (requirements baseline, from Main Agent in Step 5)
- ProjectPlan (strategic context, from Main Agent in Step 5)
- Archive results (best practices, from Step 6)
- Feedback history (if iteration > 1, retrieved via `mcp__specter__get_feedback_history`)

**Outputs**:
- TechnicalSpec markdown with sections:
  - **Overview**: Objectives, Scope, Dependencies, Deliverables (from InitialSpec)
  - **System Design**: Architecture, Technology Stack
  - **Implementation**: Functional/Non-Functional Requirements, Development Plan, Testing Strategy
  - **Additional Details**: Research Requirements, Success Criteria, Integration Context
  - **Metadata**: Status (DRAFT)

**Handshake**: Complete specification ready for return to Main Agent

**Responsibility Boundary**: Architect generates markdown, does NOT store it. Storage is Main Agent's responsibility.

---

#### Step 8: spec-architect - Return to Main Agent
**Actor**: `specter-spec-architect` agent
**Action**: Complete agent task, return TechnicalSpec markdown
**Responsibility**: Signal design completion

**Inputs**:
- TechnicalSpec markdown (from Step 7)

**Outputs**:
- Agent completion signal
- TechnicalSpec markdown returned to Main Agent

**Handshake**: Main Agent receives markdown for storage

---

#### Step 9: Main Agent - Store TechnicalSpec
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__store_technical_spec(loop_id, spec_markdown)`
**Responsibility**: Parse and persist specification in MCP Server

**Inputs**:
- `loop_id`: From Step 2
- `spec_markdown`: From Step 8

**Outputs**:
- `MCPResponse`:
  - Parsed TechnicalSpec model stored in state manager
  - Confirmation message
  - Validation errors (if markdown malformed)

**Handshake**: TechnicalSpec stored in MCP Server, Main Agent retains markdown from Step 8 for critic

**Error Handling**: If parsing fails, return to architect with validation errors

**Note**: Main Agent keeps the markdown from Step 8 to pass directly to critic in Step 10. No need to retrieve it again.

---

### Phase 3: Quality Assessment (Steps 10-14)

#### Step 10: Main Agent - Invoke spec-critic
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Launch `specter-spec-critic` agent via Task tool
**Responsibility**: Delegate quality assessment to specialized agent

**Inputs** (passed to critic):
- `loop_id`: From Step 2
- TechnicalSpec markdown: From Step 8 (kept by Main Agent, not retrieved)
- `iteration`: Current iteration number
- Instruction to retrieve feedback history

**Outputs**:
- Agent activation signal

**Handshake**: Critic receives specification and loop context

---

#### Step 11: spec-critic - Retrieve Feedback History
**Actor**: `specter-spec-critic` agent
**Action**: Call `mcp__specter__get_feedback_history(loop_id, count=3)`
**Responsibility**: Load previous assessments for consistency

**Inputs**:
- `loop_id`: Provided by Main Agent
- `count`: 3 (recent feedback items)

**Outputs**:
- `MCPResponse`:
  - List of recent CriticFeedback items (empty if iteration 1)
  - Previous scores and recommendations

**Handshake**: Feedback history informs assessment approach

**Responsibility Boundary**: Critic reads history, never modifies previous feedback

---

#### Step 12: spec-critic - FSDD Assessment
**Actor**: `specter-spec-critic` agent
**Action**: Evaluate specification against 12 technical FSDD criteria
**Responsibility**: Generate quality scores per criterion

**Inputs**:
- TechnicalSpec markdown
- Feedback history (context)
- FSDD criteria:
  1. Architecture Completeness (0-10)
  2. Technology Justification (0-10)
  3. Data Model Definition (0-10)
  4. API Specification (0-10)
  5. Security Architecture (0-10)
  6. Performance Requirements (0-10)
  7. Scalability Planning (0-10)
  8. Testing Strategy (0-10)
  9. Deployment Architecture (0-10)
  10. Monitoring Plan (0-10)
  11. Documentation Approach (0-10)
  12. Research Requirements (0-10)

**Outputs**:
- Individual scores (0-10 per criterion)
- Overall quality score (0-100, weighted average)
- Assessment reasoning per criterion

**Handshake**: Scores feed feedback generation

---

#### Step 13: spec-critic - Generate CriticFeedback
**Actor**: `specter-spec-critic` agent
**Action**: Create structured feedback markdown
**Responsibility**: Package assessment for storage and architect consumption

**Inputs**:
- FSDD scores (from Step 12)
- TechnicalSpec content analysis
- Previous feedback (for trend analysis)

**Outputs**:
- CriticFeedback markdown:
  - `loop_id`: Loop identifier
  - `iteration`: Current iteration
  - `overall_score`: 0-100 quality score
  - `assessment_summary`: Brief evaluation
  - `detailed_feedback`: Criterion-by-criterion analysis
  - `key_issues`: List of critical problems (3-5)
  - `recommendations`: Prioritized improvements (Critical/Important/Nice-to-Have)
  - `research_requirements_feedback`: Specific research section feedback

**Handshake**: Structured feedback ready for storage

**Responsibility Boundary**: Critic generates feedback and DOES store it directly via MCP call (Step 14).

---

#### Step 14: spec-critic - Store Feedback
**Actor**: `specter-spec-critic` agent
**Action**: Call `mcp__specter__store_critic_feedback(loop_id, feedback_markdown)`
**Responsibility**: Persist feedback in MCP Server loop state

**Inputs**:
- `loop_id`: Provided by Main Agent
- `feedback_markdown`: From Step 13

**Outputs**:
- `MCPResponse`:
  - Parsed CriticFeedback stored in LoopState.feedback_history
  - Score automatically added to LoopState.score_history
  - LoopStatus updated to IN_PROGRESS

**Handshake**: Feedback persisted, score available for decision

**Critical Design Point**: Feedback storage is critic's responsibility. This ensures critic controls feedback format and timing.

---

### Phase 4: Loop Decision (Steps 15-17)

#### Step 15: Main Agent - Loop Decision
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Retrieve current score from LoopState, call `mcp__specter__decide_loop_next_action(loop_id, current_score)`
**Responsibility**: Determine refinement path based on quality

**Inputs**:
- `loop_id`: From Step 2
- `current_score`: Retrieved from LoopState (auto-populated by feedback storage in Step 14, passed as validation parameter)

**How Score is Retrieved**:
1. Critic stored feedback in Step 14, which auto-populated `LoopState.current_score`
2. Main Agent retrieves this score from LoopState via `get_loop_status(loop_id)` or accesses it from the MCPResponse
3. Main Agent passes the score to `decide_loop_next_action` as confirmation/validation parameter

**MCP Server Evaluation**:
- Threshold: 85 (LoopType.SPEC.threshold)
- Max iterations: 5 (LoopType.SPEC.max_iterations)
- Current iteration count
- Improvement threshold: 5 points
- Stagnation detection: Last 2 improvements < 5 points

**Outputs**:
- `MCPResponse` with status:
  - **COMPLETED**: Score ≥ 85
  - **REFINE**: Score < 85, iteration < 5, improving
  - **USER_INPUT**: Max iterations or stagnation

**Handshake**: Decision status determines workflow path

**Responsibility Boundary**: Main Agent retrieves score and calls MCP, MCP Server executes decision logic. No business logic in Main Agent.

---

#### Step 16A: Refinement Path - Get Improvement Analysis
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__get_loop_improvement_analysis(loop_id)`
**Responsibility**: Retrieve improvement trends for architect guidance

**Inputs**:
- `loop_id`: From Step 2

**Outputs**:
- `MCPResponse`:
  - Improvement trend (improving/declining/stable)
  - Average improvement score
  - Last improvement delta
  - Recurring issues list

**Handshake**: Analysis informs refinement strategy

---

#### Step 16B: Refinement Path - Re-invoke Architect
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Re-launch `specter-spec-architect` agent
**Responsibility**: Provide feedback for iterative improvement

**Inputs** (passed to architect):
- `loop_id`: From Step 2
- `project_id`: From Step 1
- `spec_name`: From Step 1
- InitialSpec: From Step 3 (passed again for consistency)
- ProjectPlan: From Step 4 (passed again for consistency)
- Previous TechnicalSpec: Via `mcp__specter__get_technical_spec_markdown(loop_id)`
- Latest feedback: Architect retrieves via `mcp__specter__get_feedback_history(loop_id, count=1)` in its workflow
- Improvement analysis: From Step 16A
- `iteration`: N+1

**Outputs**:
- Improved TechnicalSpec markdown returned to Main Agent

**Handshake**: Loop returns to Step 8 where architect returns improved TechnicalSpec to Main Agent, then Step 9 where Main Agent stores it

**Critical Fix**: Architect RETURNS the improved TechnicalSpec markdown. Main Agent STORES it in Step 9. Architect does NOT store specifications.

---

#### Step 17A: User Input Path - Get Feedback Summary
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__get_loop_feedback_summary(loop_id)`
**Responsibility**: Gather comprehensive context for user

**Inputs**:
- `loop_id`: From Step 2

**Outputs**:
- `MCPResponse`:
  - Total feedback count
  - Current score
  - Score trend
  - Recent assessment summaries

**Handshake**: Summary presented to user for clarification

---

#### Step 17B: User Input Path - Request Clarification
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Prompt user for technical guidance
**Responsibility**: Escalate when automated refinement exhausted

**Inputs**:
- Feedback summary (from Step 17A)
- Latest feedback highlighting ambiguities
- Specific questions from recurring issues

**Outputs**:
- User clarification responses
- Additional requirements/constraints

**Handshake**: User input incorporated, loop returns to Step 5 where architect is re-invoked with user guidance

---

### Phase 5: Completion (Steps 18-20)

#### Step 18: Main Agent - Finalize Specification
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__get_technical_spec_markdown(loop_id)`
**Responsibility**: Retrieve approved specification

**Inputs**:
- `loop_id`: From Step 2

**Outputs**:
- `MCPResponse`:
  - Final TechnicalSpec markdown
  - Loop status: COMPLETED
  - Final quality score ≥ 85

**Handshake**: Final specification ready for platform storage

---

#### Step 19: Main Agent - Update InitialSpec Status
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Call `mcp__specter__update_spec(project_id, spec_name, updated_spec_markdown)`
**Responsibility**: Mark InitialSpec as approved in roadmap

**Inputs**:
- `project_id`: From Step 1
- `spec_name`: From Step 1
- Updated InitialSpec markdown: Retrieve original InitialSpec from Step 3, change ONLY the status field from DRAFT to APPROVED

**How to Update**:
1. Take the original InitialSpec markdown retrieved in Step 3
2. Parse it to extract all fields (phase_name, objectives, scope, dependencies, deliverables, status)
3. Change status field from `DRAFT` to `APPROVED`
4. Rebuild the InitialSpec markdown with the new status
5. Pass updated markdown to `update_spec`

**Outputs**:
- Confirmation message
- InitialSpec status updated in roadmap (content unchanged, only status field modified)

**Handshake**: Roadmap reflects specification completion

**Note**: This updates ONLY the status field. The InitialSpec content remains unchanged. TechnicalSpec is stored separately and contains the full technical details.

---

#### Step 20: Main Agent - Platform Storage and User Notification
**Actor**: `/specter-spec` command (Main Agent)
**Action**: Store TechnicalSpec to detected platform and notify user
**Responsibility**: Persist specification and inform user of completion

**Inputs**:
- Final TechnicalSpec markdown (from Step 18)
- Platform detection (environment variables/config)
- Final quality score
- Iteration count
- Research requirements count

**Platform-Specific Actions**:

**Linear**:
- Tool: `mcp__linear-server__create_issue`
- Location: Linear issue with detailed description
- Labels: Technical specification, architecture
- Output: Issue ID

**GitHub**:
- Tool: `mcp__github__create_issue`
- Location: GitHub issue with technical details
- Labels: specification, technical-design
- Output: Issue ID

**Markdown**:
- Tool: `Write`
- Location: `docs/specter-specs/[timestamp]-[project_name]-[spec_name].md`
- Output: File path

**User Notification**:
- User message:
  ```text
  Technical specification completed!
  - Quality score: 87/100
  - Iterations: 3
  - Platform: Linear Issue #1234
  - Research requirements: 8 items documented

  Next step: /specter-build <project_name> <spec_name>
  ```

**Handshake**: Workflow complete, specification stored, user notified

**Error Handling**: If platform storage fails, fallback to Markdown

---

## Responsibility Boundary Matrix

### Main Agent (`/specter-spec` command)

**Responsibilities**:
- Workflow orchestration
- MCP tool invocation
- Agent coordination
- Platform detection
- User communication
- Error escalation

**NOT Responsible For**:
- Technical design decisions
- Quality assessment logic
- Specification content generation
- Feedback generation
- Loop decision logic (delegated to MCP)

**Tool Permissions**:
- All `mcp__specter__*` tools
- `Task` tool for agent invocation
- `Write` tool for Markdown fallback
- Platform-specific tools (Linear/GitHub)

---

### spec-architect Agent

**Responsibilities**:
- Use InitialSpec baseline provided by Main Agent
- Design system architecture
- Create TechnicalSpec markdown
- Execute archive research
- Address critic feedback (iterations > 1)
- Return TechnicalSpec to Main Agent

**NOT Responsible For**:
- Retrieving InitialSpec (Main Agent passes it)
- Storing TechnicalSpec (Main Agent's job)
- Quality assessment
- Loop decision logic
- Platform storage
- User communication

**Tool Permissions**:
- `Bash` (archive scanning)
- `Read`, `Grep`, `Glob` (archive access)
- `mcp__specter__get_feedback_history` (iterations > 1, for retrieving latest feedback)

**Critical Boundary**:
- Architect receives InitialSpec from Main Agent, does NOT retrieve it via MCP
- Architect GENERATES TechnicalSpec markdown, Main Agent STORES it

---

### spec-critic Agent

**Responsibilities**:
- Retrieve feedback history
- Evaluate against FSDD criteria
- Generate quality scores
- Create CriticFeedback markdown
- Store feedback in MCP Server
- Return completion signal

**NOT Responsible For**:
- Specification modification
- Loop decision logic
- User communication
- Platform storage

**Tool Permissions**:
- `mcp__specter__get_feedback_history` (read history)
- `mcp__specter__store_critic_feedback` (write feedback)

**Critical Boundary**: Critic STORES feedback directly, not through Main Agent.

---

### MCP Server

**Responsibilities**:
- Loop state management
- Feedback history storage
- Score tracking
- Decision logic execution
- TechnicalSpec storage
- InitialSpec management
- Improvement analytics

**NOT Responsible For**:
- Content generation
- User interaction
- Platform-specific operations

**Provides**:
- Stateful loop tracking
- Automated decision rules
- Historical context
- Analytics and trends

---

## Data Flow Diagram

```text
User Input (project_name, spec_name, focus)
    ↓
[Main Agent]
    ├─→ Step 2: mcp__specter__initialize_refinement_loop → [MCP Server] → loop_id
    ├─→ Step 3: mcp__specter__get_spec → [MCP Server] → InitialSpec
    ├─→ Step 4: mcp__specter__get_project_plan_markdown → [MCP Server] → ProjectPlan
    │
    ├─→ Step 5: Invoke [spec-architect Agent] (with InitialSpec + ProjectPlan)
    │       ├─→ Step 6: Bash: archive scan → Archive results
    │       ├─→ Step 7: Creates TechnicalSpec (uses InitialSpec from Step 5, no re-fetch)
    │       ├─→ (if iteration > 1) mcp__specter__get_feedback_history → Feedback
    │       └─→ Step 8: Returns TechnicalSpec markdown to Main Agent
    │
    ├─→ Step 9: mcp__specter__store_technical_spec → [MCP Server] → Stored
    │   (Main Agent keeps markdown from Step 8 for critic, no retrieval needed)
    │
    ├─→ Step 10: Invoke [spec-critic Agent] (with markdown from Step 8)
    │       ├─→ Step 11: mcp__specter__get_feedback_history → [MCP Server] → History
    │       ├─→ Step 12: Evaluates FSDD → Scores
    │       ├─→ Step 13: Generates CriticFeedback markdown
    │       └─→ Step 14: mcp__specter__store_critic_feedback → [MCP Server] → Stored
    │
    ├─→ Step 15: Retrieve score from LoopState, mcp__specter__decide_loop_next_action → Decision
    │
    ├─→ If REFINE (Steps 16A-16B):
    │       ├─→ mcp__specter__get_loop_improvement_analysis → [MCP Server] → Trends
    │       └─→ Loop to Step 5 (re-invoke architect, iteration N+1)
    │           └─→ Architect returns to Step 8 → Main Agent stores in Step 9
    │
    ├─→ If USER_INPUT (Steps 17A-17B):
    │       ├─→ mcp__specter__get_loop_feedback_summary → [MCP Server] → Summary
    │       └─→ User clarification → Loop to Step 5 (re-invoke architect with guidance)
    │
    └─→ If COMPLETED (Steps 18-20):
            ├─→ Step 18: mcp__specter__get_technical_spec_markdown → Final spec
            ├─→ Step 19: mcp__specter__update_spec → [MCP Server] → InitialSpec status APPROVED
            └─→ Step 20: Platform tool (Linear/GitHub/Write) → Storage + User notification
```

**Key Optimizations in This Flow**:
1. **Removed Step 6 (old)**: Architect no longer retrieves InitialSpec; uses what Main Agent passed
2. **Removed Step 11 (old)**: Main Agent no longer retrieves spec after storing; passes markdown from Step 8 to critic
3. **Fixed Step 16B**: Architect returns markdown, Main Agent stores (loop to Steps 8→9)
4. **Total Steps**: 20 (down from 24, more efficient)

---

## Error Handling Escalation Hierarchy

### Level 1: Agent-Level Errors
**Handler**: Individual agents
**Examples**:
- Archive unavailable → Continue without, note in research section
- Malformed markdown → Fix and retry

**Escalation**: If cannot recover → Return error to Main Agent

---

### Level 2: Main Agent Errors
**Handler**: Main Agent
**Examples**:
- Parsing failure → Return to architect with validation errors
- Platform storage failure → Fallback to Markdown
- MCP tool unavailable → Retry with exponential backoff

**Escalation**: If cannot recover → User notification with error context

---

### Level 3: MCP Server Errors
**Handler**: MCP Server
**Examples**:
- Loop not found → Return ResourceError
- Invalid score → Return ValidationError
- State corruption → Return ToolError

**Escalation**: Logged and returned to Main Agent for user notification

---

### Level 4: Unrecoverable Errors
**Handler**: User
**Examples**:
- Max iterations reached with low score
- Critical MCP infrastructure failure
- Platform configuration invalid

**Action**: Present error, save state, request user intervention

---

## Integration Points

### With Roadmap System
- **Input**: InitialSpec via `mcp__specter__get_spec`
- **Output**: Updated InitialSpec status via `mcp__specter__update_spec`
- **Relationship**: InitialSpec is starter, TechnicalSpec is filled version

### With Project Plan System
- **Input**: ProjectPlan via `mcp__specter__get_project_plan_markdown`
- **Purpose**: Strategic context for technical decisions

### With Loop Management System
- **Input**: Loop state via `mcp__specter__initialize_refinement_loop`
- **Output**: Loop decisions via `mcp__specter__decide_loop_next_action`
- **Relationship**: Loop tracks all iterations and scores

### With Feedback System
- **Input**: Feedback history via `mcp__specter__get_feedback_history`
- **Output**: New feedback via `mcp__specter__store_critic_feedback`
- **Relationship**: Automatic score tracking in loop state

### With Build Phase
- **Output**: TechnicalSpec ready for `/specter-build` consumption
- **Handshake**: TechnicalSpec stored in MCP Server accessible by build phase

---

## Tool Usage Patterns

### Main Agent Workflow Pattern

**Initialization Phase**:
1. Call `mcp__specter__initialize_refinement_loop(loop_type='spec')` to create loop state
2. Extract `loop_id` from MCPResponse for all subsequent operations
3. Call `mcp__specter__get_spec(project_id, spec_name)` to retrieve InitialSpec
4. Call `mcp__specter__get_project_plan_markdown(project_name)` to retrieve strategic context

**Architecture Generation Phase**:
1. Invoke `specter-spec-architect` agent via Task tool with:
   - `loop_id` for tracking
   - InitialSpec markdown for requirements baseline
   - ProjectPlan markdown for context
   - Optional focus area
2. Receive TechnicalSpec markdown from architect
3. Call `mcp__specter__store_technical_spec(loop_id, spec_markdown)` to persist specification

**Quality Assessment Phase**:
1. Call `mcp__specter__get_technical_spec_markdown(loop_id)` to retrieve stored spec
2. Invoke `specter-spec-critic` agent via Task tool with:
   - `loop_id` for tracking
   - TechnicalSpec markdown for evaluation
3. Critic stores feedback directly via `mcp__specter__store_critic_feedback()`

**Decision Phase**:
1. Call `mcp__specter__decide_loop_next_action(loop_id, current_score)` to get next action
2. Handle decision based on status:
   - **REFINE**: Call `mcp__specter__get_loop_improvement_analysis(loop_id)`, then re-invoke architect
   - **USER_INPUT**: Call `mcp__specter__get_loop_feedback_summary(loop_id)`, prompt user, then re-invoke architect
   - **COMPLETED**: Call `mcp__specter__get_technical_spec_markdown(loop_id)`, proceed to platform storage

---

### spec-architect Agent Workflow Pattern

**Use Provided Context**:
1. Use InitialSpec markdown provided by Main Agent in invocation (Step 5)
2. Use ProjectPlan markdown provided by Main Agent in invocation (Step 5)
3. Validate InitialSpec structure contains objectives, scope, dependencies, deliverables

**Note**: Architect does NOT retrieve InitialSpec via MCP tool - it uses the markdown passed to it by Main Agent.

**Archive Research** (optional):
1. Execute `Bash: ~/.claude/scripts/research-advisor-archive-scan.sh "<topic>"` for relevant patterns
2. Use `Read` tool to access found archive documents
3. Catalog existing documentation paths for Research Requirements section

**Feedback Integration** (iterations > 1):
1. Call `mcp__specter__get_feedback_history(loop_id, count=1)` to retrieve latest feedback
2. Review CriticFeedback for specific improvement areas
3. Focus refinement on lowest-scoring FSDD criteria

**Specification Creation**:
1. Design TechnicalSpec by expanding InitialSpec with:
   - System architecture and technology stack
   - Functional and non-functional requirements
   - Development plan and testing strategy
   - Research requirements (Read paths + Synthesize prompts)
   - Success criteria and integration context
2. Return TechnicalSpec markdown to Main Agent

**Critical Boundary**: Architect generates and returns markdown but does NOT store it. Main Agent handles storage via `mcp__specter__store_technical_spec()`.

---

### spec-critic Agent Workflow Pattern

**Context Retrieval**:
1. Call `mcp__specter__get_feedback_history(loop_id, count=3)` to retrieve recent assessments
2. Review previous feedback for consistency and trend analysis
3. Empty history is normal for first iteration

**FSDD Assessment**:
1. Evaluate TechnicalSpec against 12 technical criteria (0-10 each):
   - Architecture Completeness
   - Technology Justification
   - Data Model Definition
   - API Specification
   - Security Architecture
   - Performance Requirements
   - Scalability Planning
   - Testing Strategy
   - Deployment Architecture
   - Monitoring Plan
   - Documentation Approach
   - Research Requirements
2. Calculate overall quality score (0-100, weighted average)

**Feedback Generation**:
1. Create CriticFeedback markdown with:
   - Overall score and assessment summary
   - Detailed criterion-by-criterion analysis
   - Key issues list (3-5 critical problems)
   - Prioritized recommendations (Critical/Important/Nice-to-Have)
   - Research requirements feedback
2. Call `mcp__specter__store_critic_feedback(loop_id, feedback_markdown)` to persist
3. Return completion signal to Main Agent

**Critical Boundary**: Critic stores feedback directly via MCP tool call, not through Main Agent. This ensures critic controls feedback format and timing.

---

## Migration Notes

### Changes from Previous Workflow

1. **Command Signature**
   - Old: `/specter-spec [focus]`
   - New: `/specter-spec <project_name> <spec_name> [focus]`

2. **InitialSpec Integration**
   - Old: Not retrieved, architect started from scratch
   - New: Retrieved first as requirements baseline

3. **Tool Naming**
   - Old: Generic names (e.g., `store_technical_spec`)
   - New: Namespaced (e.g., `mcp__specter__store_technical_spec`)

4. **Storage Responsibility**
   - Old: Unclear who stores what
   - New: Architect returns, Main Agent stores TechnicalSpec; Critic stores own feedback

5. **Feedback History**
   - Old: Not explicitly used
   - New: Retrieved by both architect and critic for context

6. **Loop Analytics**
   - Old: Manual decision logic in command
   - New: Automated via MCP Server with improvement analysis

### Backward Compatibility
- None required (new system)
- Previous specifications remain accessible via roadmap tools

---

## Success Metrics

### Quantitative Targets
- Loop initialization: 99% success rate
- InitialSpec retrieval: 95% success rate
- Feedback storage: 98% success rate
- Loop decision accuracy: 99% success rate
- Platform storage: 85% success rate

### Qualitative Targets
- Clear responsibility boundaries (binary: yes/no)
- Explicit handshakes at every step (binary: yes/no)
- No implicit state assumptions (binary: yes/no)
- User-friendly command interface (binary: yes/no)

---

## Related Documentation

- [Command Specification](../commands/specter-spec.md)
- [spec-architect Agent Specification](../agents/spec-architect.md)
- [spec-critic Agent Specification](../agents/spec-critic.md)
- [MCP Tools Reference](../../services/mcp/tools/)
- [Loop State Management](../../services/utils/loop_state.py)
- [State Manager](../../services/utils/state_manager.py)

---

## Version History

**Version 1.1** (2025-10-03)
- **CRITICAL FIXES**: Corrected workflow based on actual MCP infrastructure
- Removed Step 6 (redundant InitialSpec retrieval by architect)
- Removed Step 11 (redundant spec retrieval by Main Agent)
- Fixed Step 16B storage responsibility (architect returns, Main Agent stores)
- Clarified Step 15 score retrieval logic
- Clarified Step 19 InitialSpec status update process
- Documented project_id derivation in Step 3
- Updated data flow diagram to reflect optimizations
- **New Total**: 20 steps (down from 24, more efficient)
- Updated all cross-references and step numbers

**Version 1.0** (2025-10-03)
- Initial comprehensive implementation guide
- Complete workflow structure defined
- Responsibility boundaries established
- Tool usage patterns documented
