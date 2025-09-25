def generate_build_command_template(
    get_spec_tool: str,
    comment_spec_tool: str,
) -> str:
    # Safe Python list construction to prevent YAML injection
    base_tools = [
        'Task(build-planner)',
        'Task(build-critic)',
        'Task(build-coder)',
        'Task(build-reviewer)',
        'Task(research-synthesizer)',
        'Bash(~/.claude/scripts/detect-packages.sh:*)',
        'mcp__specter__initialize_refinement_loop',  # Fixed: mcp__loop_state__ -> mcp__specter__
        'mcp__specter__decide_loop_next_action',  # Fixed: mcp__loop_state__ -> mcp__specter__
        'mcp__specter__get_loop_status',  # Fixed: mcp__loop_state__ -> mcp__specter__
    ]

    # Add platform tools with validation
    platform_tools = [get_spec_tool, comment_spec_tool]
    all_tools = base_tools + platform_tools

    # Convert to YAML with proper escaping
    tools_yaml = '\n'.join(f'  - {tool}' for tool in all_tools)

    return f"""---
allowed-tools:
{tools_yaml}
argument-hint: [specification-identifier]
description: Transform technical specifications into production-ready code through parallel research, implementation planning, and TDD development
---

# /build Command: Implementation Orchestration

## Overview
Orchestrate the complete implementation workflow, transforming technical specifications into production-ready code through parallel research synthesis, implementation planning, and code development with comprehensive quality validation.

## Primary Responsibilities

### 1. Technology Environment Discovery
- Execute environment detection to identify project stack
- Analyze project configuration files and dependencies
- Determine testing frameworks and build tools
- Configure implementation context for agents

### 2. Parallel Research Orchestration
- Parse Research Requirements from specification
- Identify existing documentation paths
  - Just collect the paths. Do not read the content.
- Identify external research needs for synthesis
- Execute parallel research operations
- Collect documentation paths for build-planner

### 3. Implementation Planning Loop
- Initialize MCP refinement loop for build plan development
- Invoke build-planner with research documentation paths
- Assess plan quality with build-critic agent
- Iterate until plan quality threshold met

### 4. Code Implementation Loop
- Initialize MCP refinement loop for code development
- Invoke build-coder for TDD implementation approach
- Validate implementation with build-reviewer agent
- Iterate until code quality threshold met

### 5. Integration & Documentation
- Update specification with implementation status
- Link code changes to specification
- Document completion status
- Generate implementation summary

## Orchestration Pattern

```text
Main Agent (via /build)
    │
    ├── 1. Retrieve Specification
    │   └── {get_spec_tool} with specification identifier
    │
    ├── 2. Environment Discovery
    │   └── Bash: detect-packages.sh → technology context
    │
    ├── 3. Parallel Research Execution
    │   ├── Parse Research Requirements section
    │   ├── For each "Synthesize: [prompt]" item:
    │   │   └── Task: research-synthesizer (parallel)
    │   └── Collect: All documentation paths
    │
    ├── 4. Implementation Planning Loop
    │   ├── MCP: initialize_refinement_loop(loop_type='build_plan')
    │   ├── Task: build-planner (with documentation paths)
    │   ├── Task: build-critic → quality score
    │   └── MCP: decide_loop_next_action(loop_id, score)
    │
    ├── 5. Code Implementation Loop
    │   ├── MCP: initialize_refinement_loop(loop_type='build_code')
    │   ├── Task: build-coder (TDD approach)
    │   ├── Task: build-reviewer → quality score
    │   └── MCP: decide_loop_next_action(loop_id, score)
    │
    └── 6. Completion & Documentation
        └── {comment_spec_tool} with implementation results
```

## Implementation Instructions

### Step 1: Retrieve Specification and Environment Setup
Initialize the implementation workflow:

```
# Retrieve technical specification
SPECIFICATION_IDENTIFIER = [User provided specification identifier]

TECHNICAL_SPECIFICATION = {get_spec_tool}:
  identifier: ${{SPECIFICATION_IDENTIFIER}}

# Execute environment detection
TECHNOLOGY_CONTEXT = Bash: ~/.claude/scripts/detect-packages.sh --scan-project --output structured

# Extract key components
PROJECT_STACK = [detect-packages.sh output: languages, frameworks, tools]
RESEARCH_REQUIREMENTS = [TECHNICAL_SPECIFICATION: Research Requirements section]
SPECIFICATION_CONTENT = [TECHNICAL_SPECIFICATION: complete specification]
```

### Step 2: Parallel Research Execution
Coordinate research path collection:

```
# Initialize documentation paths collection
DOCUMENTATION_PATHS = []

# Process Research Requirements section
For each item in RESEARCH_REQUIREMENTS:

IF item starts with "Read:":
  EXISTING_PATH = [Extract path from "Read: [path]"]
  Add EXISTING_PATH to DOCUMENTATION_PATHS

IF item starts with "Synthesize:":
  RESEARCH_PROMPT = [Extract prompt from "Synthesize: [prompt]"]
  
  Invoke research-synthesizer agent with this input:
  ${{RESEARCH_PROMPT}}
  
  Expected Output Format:
  - Research document path for generated content
  - Key findings summary
  - Implementation guidance recommendations
  
  SYNTHESIZED_PATH = [research-synthesizer output: document path]
  Add SYNTHESIZED_PATH to DOCUMENTATION_PATHS

# Collect all paths for build-planner
COMPLETE_DOCUMENTATION_PATHS = [All collected paths from existing docs and research synthesis]
```

### Step 3: Implementation Planning Loop
Coordinate build plan development and refinement:

```
# Initialize planning refinement loop
PLANNING_LOOP_ID = mcp__specter__initialize_refinement_loop:
  loop_type: "build_plan"

# Begin planning cycle
Invoke build-planner agent with this input:

Technical Specification:
${{SPECIFICATION_CONTENT}}

Technology Context:
${{PROJECT_STACK}}

Documentation Paths:
${{COMPLETE_DOCUMENTATION_PATHS}}

Expected Output Format:
- Implementation plan in markdown format
- Phased approach with specific tasks
- Technology decisions with justifications
- Risk mitigation strategies

# Capture planning output
CURRENT_BUILD_PLAN = [build-planner output: complete implementation plan]
```

### Step 4: Planning Quality Assessment
Evaluate build plan quality:

```
# Assess plan quality
Invoke build-critic agent with this input:
${{CURRENT_BUILD_PLAN}}

Expected Output Format:
- Overall Quality Score: [0-100 numerical value]
- Priority Improvements: [List of specific actionable suggestions]
- Strengths: [List of well-executed areas to preserve]

# Extract assessment results
PLAN_QUALITY_SCORE = [build-critic output: Overall Quality Score (0-100)]
PLAN_IMPROVEMENT_FEEDBACK = [build-critic output: Priority Improvements and suggestions]

# MCP decision for planning loop
PLANNING_DECISION = mcp__specter__decide_loop_next_action:
  loop_id: ${{PLANNING_LOOP_ID}}
  current_score: ${{PLAN_QUALITY_SCORE}}

# Handle planning decisions
IF PLANNING_DECISION == "complete":
  → Proceed to Step 5: Code Implementation Loop

IF PLANNING_DECISION == "refine":
  → Return to Step 3 with refined context:
  
  Invoke build-planner agent with this input:
  
  Previous Plan: ${{CURRENT_BUILD_PLAN}}
  Quality Feedback: ${{PLAN_IMPROVEMENT_FEEDBACK}}
  Iteration: [increment counter]
  
  Expected Output Format: Refined implementation plan addressing feedback

IF PLANNING_DECISION == "user_input":
  → Escalate planning stagnation:
  
  Present to user:
  "Implementation planning has reached quality plateau at ${{PLAN_QUALITY_SCORE}}%.
  Key gaps identified: [Priority Improvements list]
  
  Please provide guidance on:
  1. [Specific technical approach preferences]
  2. [Alternative implementation strategies]
  3. [Accept current plan quality: yes/no]"
```

### Step 5: Code Implementation Loop
Coordinate TDD code development:

```
# Initialize code implementation loop
CODING_LOOP_ID = mcp__specter__initialize_refinement_loop:
  loop_type: "build_code"

# Begin coding cycle with approved plan
Invoke build-coder agent with this input:

Implementation Plan:
${{CURRENT_BUILD_PLAN}}

Technology Context:
${{PROJECT_STACK}}

Technical Specification:
${{SPECIFICATION_CONTENT}}

Expected Output Format:
- Source code implementation with tests
- Test execution results
- Implementation progress summary
- Code quality metrics

# Capture implementation output
CURRENT_IMPLEMENTATION = [build-coder output: complete code implementation with tests]
```

### Step 6: Code Quality Assessment
Evaluate implementation quality:

```
# Assess code quality
Invoke build-reviewer agent with this input:
${{CURRENT_IMPLEMENTATION}}

Expected Output Format:
- Overall Quality Score: [0-100 numerical value]
- Priority Improvements: [List of specific actionable suggestions]
- Strengths: [List of well-executed areas to preserve]
- Test Results: [Pass/fail status and coverage metrics]

# Extract assessment results
CODE_QUALITY_SCORE = [build-reviewer output: Overall Quality Score (0-100)]
CODE_IMPROVEMENT_FEEDBACK = [build-reviewer output: Priority Improvements and suggestions]
TEST_RESULTS = [build-reviewer output: Test Results and coverage]

# MCP decision for coding loop
CODING_DECISION = mcp__specter__decide_loop_next_action:
  loop_id: ${{CODING_LOOP_ID}}
  current_score: ${{CODE_QUALITY_SCORE}}

# Handle coding decisions
IF CODING_DECISION == "complete":
  → Proceed to Step 7: Integration & Documentation

IF CODING_DECISION == "refine":
  → Return to Step 5 with refined context:
  
  Invoke build-coder agent with this input:
  
  Previous Implementation: ${{CURRENT_IMPLEMENTATION}}
  Quality Feedback: ${{CODE_IMPROVEMENT_FEEDBACK}}
  Test Status: ${{TEST_RESULTS}}
  Iteration: [increment counter]
  
  Expected Output Format: Refined implementation addressing feedback

IF CODING_DECISION == "user_input":
  → Escalate implementation stagnation:
  
  Present to user:
  "Code implementation has reached quality plateau at ${{CODE_QUALITY_SCORE}}%.
  Key gaps identified: [Priority Improvements list]
  Test Status: ${{TEST_RESULTS}}
  
  Please provide guidance on:
  1. [Specific code quality concerns]
  2. [Alternative implementation approaches]
  3. [Accept current code quality: yes/no]"
```

### Step 7: Integration & Documentation
Complete implementation workflow:

```
# Update specification with implementation details
IMPLEMENTATION_SUMMARY = Generate summary including:
- Files modified count
- Test results and coverage
- Quality scores achieved
- Performance benchmarks met
- Security issues (if any)

{comment_spec_tool}:
  identifier: ${{SPECIFICATION_IDENTIFIER}}
  status: "Implementation Complete"
  implementation_details: ${{IMPLEMENTATION_SUMMARY}}
  build_plan_quality: ${{PLAN_QUALITY_SCORE}}%
  code_quality: ${{CODE_QUALITY_SCORE}}%
  test_results: ${{TEST_RESULTS}}
```

## Quality Gates

### Build Planning Quality
- **Quality Threshold**: 80% (configurable via FSDD_LOOP_BUILD_PLAN_THRESHOLD)
- **Maximum Iterations**: 5 (configurable via FSDD_LOOP_BUILD_PLAN_MAX_ITERATIONS)
- **Assessment Focus**: Completeness, feasibility, test coverage

### Code Implementation Quality
- **Quality Threshold**: 95% (configurable via FSDD_LOOP_BUILD_CODE_THRESHOLD)
- **Maximum Iterations**: 5 (configurable via FSDD_LOOP_BUILD_CODE_MAX_ITERATIONS)
- **Assessment Focus**: Code quality, test passing, best practices

### Stagnation Detection
- **Both Loops**: Less than 5 points improvement over 2 iterations
- **Action**: MCP Server returns "user_input" status
- **Recovery**: Request specific guidance on blocked areas

## Research Integration Strategy

### Parallel Research Pattern
```text
# Main Agent coordinates research path collection
For each item in research_requirements:

IF item starts with "Read:":
  → Extract path and add to documentation_paths list
  
IF item starts with "Synthesize:":
  → Invoke research-synthesizer agent with extracted prompt
  → Add research-synthesizer output path to documentation_paths list

Collect all documentation paths (both existing docs and research-synthesizer outputs)

Pass documentation_paths list to build-planner agent
```

### Research Requirements Processing
Research requirements processed by parsing specification sections and coordinating parallel execution of synthesis tasks while collecting documentation paths for build-planner consumption.

## Error Handling

### Standardized Error Response Format
All error scenarios return structured responses:

```json
{{
  "error_type": "spec_not_found|research_failure|environment_error|planning_failure|implementation_failure|quality_plateau",
  "error_message": "Detailed error description",
  "recovery_action": "Specific recovery steps taken",
  "user_guidance": "Clear instructions for user",
  "partial_output": "Any salvageable work completed"
}}
```

### Error Scenario Implementations

#### 1. Specification Not Found
```
IF specification retrieval fails:
  ERROR_RESPONSE = {{
    "error_type": "spec_not_found",
    "error_message": "Cannot retrieve specification with identifier: ${{SPECIFICATION_IDENTIFIER}}",
    "recovery_action": "Prompting user for correct specification identifier or path",
    "user_guidance": "Please provide valid specification ID or path",
    "partial_output": "Environment detection results if available"
  }}
  → Request specification location or alternative identifier
```

#### 2. Research Execution Failure
```
IF research-synthesizer tasks fail:
  ERROR_RESPONSE = {{
    "error_type": "research_failure",
    "error_message": "Research synthesis failed for [X] of [Y] topics",
    "recovery_action": "Continuing with available research and existing documentation",
    "user_guidance": "Some research failed. Proceeding with available documentation.",
    "partial_output": "Successfully completed research paths"
  }}
  → Continue with available documentation, note missing research in plan
```

#### 3. Environment Detection Failure
```
IF detect-packages.sh fails or returns unclear results:
  ERROR_RESPONSE = {{
    "error_type": "environment_error",
    "error_message": "Cannot detect project technology stack reliably",
    "recovery_action": "Requesting manual technology specification from user",
    "user_guidance": "Please specify: language, framework, testing tools",
    "partial_output": "Partial environment detection results"
  }}
  → Request manual specification of technology stack
```

#### 4. Planning Quality Failure
```
IF planning loop fails to reach quality threshold:
  ERROR_RESPONSE = {{
    "error_type": "planning_failure",
    "error_message": "Implementation plan quality below threshold after maximum iterations",
    "recovery_action": "Presenting best available plan with quality warnings",
    "user_guidance": "Plan Quality: ${{PLAN_QUALITY_SCORE}}%. Key issues: [list]. Review recommended.",
    "partial_output": "Implementation plan at ${{PLAN_QUALITY_SCORE}}% completeness"
  }}
  → Present plan with warnings, allow user to proceed or refine
```

#### 5. Implementation Quality Failure
```
IF coding loop fails to reach quality threshold or tests fail:
  ERROR_RESPONSE = {{
    "error_type": "implementation_failure",
    "error_message": "Code implementation quality below threshold or test failures persist",
    "recovery_action": "Presenting implementation with detailed failure analysis",
    "user_guidance": "Code Quality: ${{CODE_QUALITY_SCORE}}%. Test Status: ${{TEST_RESULTS}}. Manual review required.",
    "partial_output": "Implementation code with test results"
  }}
  → Present code with test reports and quality analysis
```

### Proactive Error Prevention
- Validate specification format and completeness before processing
- Test environment detection scripts before full workflow
- Check MCP tool availability before loop initialization
- Monitor research synthesis progress with timeouts
- Validate intermediate outputs before proceeding to next phase

## Expected Output Specifications

### Build Plan Output Structure
```markdown
# Implementation Plan: [Project Name]

## Overview
[Implementation approach summary]

## Phase 1: Setup and Configuration
- [ ] Task 1: [Description]
- [ ] Task 2: [Description]

## Phase 2: Core Implementation
- [ ] Task 3: [Description]
- [ ] Task 4: [Description]

## Phase 3: Testing and Validation
- [ ] Task 5: [Description]
- [ ] Task 6: [Description]

## Technology Decisions
[Specific libraries and patterns]

## Risk Mitigation
[Identified risks and solutions]
```

### Implementation Output Components
- **Source Code**: Implemented features with comprehensive tests
- **Test Results**: Passing test suites with coverage metrics
- **Documentation**: Code comments and implementation notes
- **Specification Updates**: Marked complete with implementation details

## Context Preservation

Maintain conversation flow while processing complex implementation workflow:
- Complete conversation history passed to each agent invocation
- Technical assessments and loop decisions hidden from user interaction
- Natural dialogue flow preserved despite multi-agent coordination
- Context summarization to manage size constraints across refinement cycles

## Implementation Integration Notes

### Specification Tools
- **Retrieval Tool**: {get_spec_tool}
- **Update Tool**: {comment_spec_tool}
- **Content Structure**: Platform-agnostic markdown maintained
- **Implementation Status**: Tracked in specification metadata

### Loop State Management
- **Planning Loop**: Separate loop ID for build plan refinement
- **Coding Loop**: Separate loop ID for code implementation refinement
- **State Isolation**: No shared state between planning and coding loops
- **Progress Tracking**: Clear messaging about active loop phase

### TDD Enforcement Strategy
- build-coder agent writes tests first before implementation
- Test execution validation required before considering implementation complete
- Green tests required for quality gate passage
- Test coverage metrics tracked and reported

## Success Metrics

### Quantitative Targets
- **Plan Quality Score**: Target ≥80%
- **Code Quality Score**: Target ≥95%
- **Test Coverage**: Target >80%
- **Build Success Rate**: Target 100%
- **Research Success Rate**: Target >90%

### Qualitative Indicators
- **Implementation Completeness**: All specification requirements met
- **Code Maintainability**: Following established best practices
- **Documentation Quality**: Clear and comprehensive implementation notes
- **Performance**: Meeting specification benchmarks and requirements

The implementation is ready for deployment. All quality gates passed and specification updated with completion status.
"""
