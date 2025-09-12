def generate_build_command_template(
    get_spec_tool: str, list_comments_tool: str, add_comment_tool: str, update_spec_tool: str, spec_implementation: str
) -> str:
    return f"""---
allowed-tools:
  - Bash(~/.claude/scripts/detect-packages.sh)
  - Read(~/.claude/best-practices/)
  - Task(research-synthesizer)
  - Task(build-planner)
  - Task(refine-build)
  - Task(build-coder)
  - Task(build-verifier)
  - {get_spec_tool}
  - {list_comments_tool}
  - {add_comment_tool}
  - {update_spec_tool}
argument-hint: [ticket-id]
description: Enhanced build workflow with technology-aware refinement and context preservation
---

# Enhanced Build Implementation Command

Execute comprehensive build workflow with automatic refinement integration and technology context preservation.

## Your Task

Execute enhanced implementation for spec ticket: $ARGUMENTS

## Command Flow

### Phase 0: Technology Context Discovery (NEW)

1. **Detect Current Environment**
   ```bash
   ~/.claude/scripts/detect-packages.sh
   ```
   - Parse detected packages, versions, and environment
   - Store technology context for entire workflow

2. **Analyze Project Structure**
   - Identify src/, tests/, docs/ directories
   - Note build tools and configuration files
   - Capture git status for context

### Step 2: Research Requirements Orchestration (Main Agent Pipeline)
# **Role**: Main Agent handles everything - NO MCP Server involvement
# **Pattern**: Simple orchestration using existing tools only

**⚠️ IMPORTANT: The following are EXAMPLES of the pattern - NOT hardcoded implementations**
**Parse ticket content dynamically - do NOT hardcode specific research items**

**Main Agent Instructions** (follow pattern, not literal examples):

1. **Get ticket content** → Use {get_spec_tool}: $ARGUMENTS
2. **Parse research section** → Extract lines starting with "- Read:" and "- Synthesize:" FROM ACTUAL TICKET
3. **Read existing docs** → Use Read(path) for EACH ACTUAL PATH FOUND IN TICKET
4. **Launch synthesis** → Use Task('research-synthesizer', {{}}) for EACH ACTUAL PROMPT FOUND
5. **Collect paths** → Create list of ALL ACTUAL research file paths (existing + newly generated)
6. **Pass to Step 3** → Provide research paths to build-planner

**Process**:

1. **Retrieve Ticket and Extract Research Requirements** (EXAMPLE):
   ```text
   # EXAMPLE - use actual ticket parsing logic:
   ticket_result = {get_spec_tool}($ARGUMENTS)
   
   # Parse RESEARCH_REQUIREMENTS_FOR_BUILD_PHASE section FROM ACTUAL TICKET
   # EXAMPLE types you might find (actual content varies):
   # Type A: - Read: ~/.claude/best-practices/[ACTUAL-FILE].md
   # Type B: - Synthesize: "[ACTUAL PROMPT FROM TICKET]"
   ```

2. **Execute Research Collection in Parallel** (EXAMPLES):
   
   **For Existing Documentation** (EXAMPLE):
   ```text
   # EXAMPLE - read actual files found in ticket, not these hardcoded ones:
   existing_docs = [
       Read([ACTUAL_PATH_FROM_TICKET]),
       Read([ACTUAL_PATH_FROM_TICKET]),
       Read([ACTUAL_PATH_FROM_TICKET])
       # Use ACTUAL paths parsed from ticket - NOT these examples
   ]
   ```

   **For Research Prompts** (EXAMPLE):
   ```text
   # EXAMPLE - use actual prompts from ticket:
   synthesis_results = [
       Task('research-synthesizer', {{
           'query': "[ACTUAL PROMPT FROM TICKET]",
           'technology_context': [detected from Step 1],
           'canonical_topic': "[DYNAMICALLY EXTRACTED]"
       }})
       # For EACH ACTUAL synthesis prompt found in ticket
   ]
   ```

3. **Collect All Documentation Paths** (EXAMPLE OUTPUT FORMAT):
   ```text
   # EXAMPLE structure - actual data comes from processing above:
   all_research_paths = {{
       'existing_documentation_paths': [ACTUAL paths to existing docs],
       'new_research_file_paths': [ACTUAL paths to synthesis result files],
       'research_execution_timestamp': [ACTUAL current timestamp],
       'total_research_items': [ACTUAL count of all items]
   }}
   ```

**Output**: List of all research documentation paths (existing + newly researched files)

### Step 3: Implementation Planning with Research Context (Main Agent Pipeline)
# **Role**: Main Agent handles everything - NO MCP Server involvement
# **Pattern**: Simple orchestration using existing tools and subagent calls

**⚠️ IMPORTANT: The following are EXAMPLES of the pattern - NOT hardcoded implementations**
**Use actual research results from Step 2 - do NOT hardcode context packages**

**Main Agent Instructions** (follow pattern, not literal examples):

1. **Gather coding standards** → Read(CLAUDE.md) and Read(~/.claude/CLAUDE.md)
2. **Launch build-planner** → Task(build-planner, {{ACTUAL_CONTEXT_FROM_STEPS_1_AND_2}})
3. **Receive implementation plan** → Get detailed plan from build-planner response
4. **Pass to Step 4** → Provide implementation plan for quality assessment

**Process** (EXAMPLE - use actual data):

1. **Gather All Context** (EXAMPLE):
   ```text
   # EXAMPLE - read actual standards files:
   coding_standards = Read(CLAUDE.md)  # Project workspace standards
   global_standards = Read(~/.claude/CLAUDE.md)  # Global user standards
   ```

2. **Launch build-planner with Complete Research Context** (EXAMPLE):
   ```text
   # EXAMPLE - use ACTUAL context from previous steps:
   plan_result = Task(build-planner, {{
     ticket_content: [ACTUAL ticket data from Step 2],
     technology_context: [ACTUAL context from Step 1],
     research_documentation_paths: [ACTUAL paths from Step 2],
     coding_standards: [ACTUAL CLAUDE.md content],
     global_standards: [ACTUAL ~/.claude/CLAUDE.md content]
   }})
   ```

**Expected build-planner output** (EXAMPLE format):
- DETAILED_FILE_CHANGES: Exact file modifications with line-level specificity
  # EXAMPLE: "services/auth.py:45-52: Add AUTH_TOKEN_EXPIRED constant"
- CODE_PATTERNS_TO_USE: Specific patterns from research applied to codebase
  # EXAMPLE: "BaseService inheritance pattern from best-practices/service-layer.md"
- IMPLEMENTATION_SEQUENCE: Step-by-step order with prerequisites
  # EXAMPLE: "Step 1: Create base service, Step 2: Add auth methods, Step 3: Write tests"
- INTEGRATION_STRATEGY: Codebase-specific connection approaches
  # EXAMPLE: "Use existing dependency injection pattern from services/base.py:78"
- ESCALATION_SCENARIOS: When build-coder should escalate vs. proceed
  # EXAMPLE: "Escalate if JWT library conflicts with existing crypto imports"

### Step 4: Plan Quality Assessment & Refinement (Hybrid Orchestration)
# **Pattern**: Main Agent pipeline + MCP Server loop state management
# **Role**: Main Agent follows MCP instructions exactly - NO decision making

**⚠️ IMPORTANT: The following are EXAMPLES of the pattern - NOT hardcoded implementations**
**DO NOT implement these exact function calls - use actual MCP tools and dynamic logic**

**Main Agent Instructions** (explicit pipeline behavior):

1. **Initialize refinement** → Call MCP tool (EXAMPLE: initialize_refinement_loop)
2. **Follow MCP instructions** → Execute exactly what `next_action` specifies  
3. **Call agents as directed** → Use Task calls based on MCP guidance
4. **Update loop state** → Pass agent results back to MCP tools
5. **Continue until MCP says stop** → Check MCP-provided termination conditions

**Hybrid Orchestration Process** (EXAMPLE PATTERN - NOT LITERAL CODE):

**Step 4.1: Loop Initialization (EXAMPLE)**
```text
# EXAMPLE - use actual MCP tools available:
loop_state = [CALL APPROPRIATE MCP TOOL]({{
  content: plan_file_content,
  quality_threshold: 0.85, 
  max_iterations: 3
}})

# EXAMPLE MCP response format (actual format may vary):
# {{
#   loop_id: "generated_id",
#   initial_quality: [calculated_score],
#   next_action: [mcp_determined_action],
#   should_continue: [boolean]
# }}
```

**Step 4.2: Agent Loop (EXAMPLE PATTERN)**
```text
# EXAMPLE - actual implementation should use dynamic MCP guidance:
WHILE [MCP SAYS CONTINUE]:
  
  IF [MCP SAYS] == "call_critic_agent":
    critique = Task(build-critic, {{content: current_content}})
    [UPDATE MCP STATE WITH CRITIQUE RESULT]
    
  IF [MCP SAYS] == "call_refiner_agent":
    refined = Task(build-refiner, {{content: current_content, critique: critique}})  
    [UPDATE MCP STATE WITH REFINED RESULT]
```

**Step 4.3: Loop Completion (EXAMPLE)**
```text
# EXAMPLE final MCP response (actual format determined by implementation):
# {{
#   should_continue: false,
#   final_content: "quality-validated plan",
#   termination_reason: [reason],
#   iterations_completed: [count]
# }}
```

**Output**: Quality-validated implementation plan (received from MCP Server)

### Phase 4: Implementation with Refined Plan (Main Agent Pipeline)
# **Role**: Main Agent handles everything - NO MCP Server involvement
# **Pattern**: Simple orchestration using existing tools only

**⚠️ IMPORTANT: The following are EXAMPLES of the pattern - NOT hardcoded implementations**
**Use actual data from previous phases - do NOT hardcode context packages**

**Main Agent Instructions** (follow pattern, not literal examples):

1. **Launch build-coder with context** → Task(build-coder, {{ACTUAL_CONTEXT_FROM_PREVIOUS_PHASES}})
2. **Receive implementation results** → Get code files, tests, and documentation from build-coder response
3. **Pass to Phase 5** → Provide implementation results for verification

**Process** (EXAMPLE - use actual data):

1. **Launch build-coder with Complete Context** (EXAMPLE):
   ```text
   # EXAMPLE - use ACTUAL context from previous phases:
   implementation_result = Task(build-coder, {{
     implementation_plan: [ACTUAL refined or original plan from Phase 4],
     technology_context: [ACTUAL context from Phase 0],
     optimizations: [ACTUAL optimizations from refinement if applied],
     risk_mitigations: [ACTUAL risk mitigations from refinement if applied]
   }})
   ```

**Expected build-coder output** (EXAMPLE format):
- Code implementation following refined plan
- Tests with >90% coverage
- Documentation updates

### Phase 5: Verification with Context Validation (Main Agent Pipeline)
# **Role**: Main Agent handles everything - NO MCP Server involvement  
# **Pattern**: Simple orchestration using existing tools only

**⚠️ IMPORTANT: The following are EXAMPLES of the pattern - NOT hardcoded implementations**
**Use actual results from Phase 4 - do NOT hardcode verification data**

**Main Agent Instructions** (follow pattern, not literal examples):

1. **Launch build-verifier with context** → Task(build-verifier, {{ACTUAL_CONTEXT_FROM_PHASES_0_AND_4}})
2. **Receive verification results** → Get compliance metrics, quality scores, and recommendations from build-verifier
3. **Pass to Phase 6** → Provide verification results for final handoff

**Process** (EXAMPLE - use actual data):

1. **Launch build-verifier with Complete Context** (EXAMPLE):
   ```text
   # EXAMPLE - use ACTUAL context from previous phases:
   verification_result = Task(build-verifier, {{
     implementation: [ACTUAL implementation from build-coder in Phase 4],
     refined_plan: [ACTUAL refined plan from Phase 3],
     technology_context: [ACTUAL context from Phase 0], 
     compliance_requirements: [ACTUAL plan alignment, quality standards, TDD coverage]
   }})
   ```

**Expected build-verifier output** (EXAMPLE format):
- Plan compliance validation (target: >90%)
- Quality metrics assessment
- Test coverage verification  
- Performance optimization checks

### Phase 6: Quality Handoff and Reporting (Main Agent Pipeline)
# **Role**: Main Agent handles everything - NO MCP Server involvement
# **Pattern**: Simple tool calls using spec manager tools

**⚠️ IMPORTANT: The following are EXAMPLES of the pattern - NOT hardcoded implementations**
**Use actual verification results from Phase 5 - do NOT hardcode summary data**

**Main Agent Instructions** (follow pattern, not literal examples):

1. **Create comprehensive spec comment** → Use {add_comment_tool} with ACTUAL summary data
2. **Update ticket status** → Use {update_spec_tool} with ACTUAL verification-based status
3. **Report completion** → Provide final workflow summary

**Process** (EXAMPLE - use actual data):

1. **Create Spec Comment with Actual Results** (EXAMPLE):
   ```text
   # EXAMPLE - use ACTUAL results from Phase 5:
   {add_comment_tool}({{
     ticket_id: $ARGUMENTS,
     body: [ACTUAL formatted summary with all phases from verification_result]
   }})
   ```

2. **Update Ticket Status with Actual State** (EXAMPLE):
   ```text
   # EXAMPLE - use ACTUAL state based on verification results:
   {update_spec_tool}({{
     ticket_id: $ARGUMENTS,
     state: [ACTUAL state based on verification results - "completed" if passed, "needs_work" if failed]
   }})
   ```

## Quality Gates

### Refinement Trigger
- Quality threshold: 0.85
- Max iterations: 3
- Stagnation detection: < 0.02 improvement

### Success Criteria
- Plan compliance: >90%
- Test coverage: >90%
- Quality score: >0.85
- All risk mitigations implemented

## Context Preservation

Throughout the workflow, maintain:
- Full file system access
- Git integration
- Environment variables
- Package detection results
- Project structure understanding

This demonstrates command-based supervisor advantages over MCP server isolation.

## Error Handling

### Refinement Failures
- Log failure reason
- Continue with original plan
- Note in {spec_implementation} comment

### Build Failures
- Capture error details
- Attempt recovery if possible
- Update ticket with failure status

### API Failures
- Retry with exponential backoff
- Fallback to console output
- Preserve partial progress

## Output Format

Final spec comment should include:
```markdown
## Build Execution Summary

**Ticket**: [ID]
**Technology Context**: [detected packages]
**Refinement Applied**: Yes/No
**Quality Achieved**: [score]

### Implementation Details
- Files created: [list]
- Files modified: [list]
- Tests written: [list]

### Quality Metrics
- Plan compliance: [%]
- Test coverage: [%]
- Performance optimizations: [list]

### Next Steps
[Recommendations from verifier]
```
"""
