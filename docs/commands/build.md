# /build Command Specification

## Overview
The `/build` command orchestrates the complete implementation workflow, transforming technical specifications into production-ready code through parallel research synthesis, implementation planning, and code development with comprehensive quality validation.

## Command Metadata

**Name**: `/build`  
**Type**: User-invoked workflow command  
**Phase**: Implementation (Phases 3-4 of 4)  
**Model**: Claude Sonnet (default)  

## Invocation

### Who Invokes It
- **Primary**: End user via Claude Code CLI
- **Context**: After successful completion of `/spec` command
- **Prerequisites**: Completed technical specification with research requirements

### Trigger Format
```
/build [specification-identifier]
```

## Workflow Position

```text
Technical Spec → /build → Parallel Research → Planning Loop → Coding Loop → Implementation
                    │              │               │               │
                    │              ↓               ↓               ↓
                    │         Documentation    Build Plan     Production Code
                    │         Synthesis       with Tests      with Validation
                    │
                    └── Environment Discovery → Technology Detection
```

### Position in End-to-End Flow
1. **Third & Fourth Phases**: Implementation planning and code development
2. **Precedes**: Deployment and production release
3. **Dependencies**: Requires completed technical specification
4. **Output**: Production-ready implementation with tests

## Primary Responsibilities

### Core Tasks

1. **Technology Environment Discovery**
   - Execute `detect-packages.sh` to identify project stack
   - Analyze `package.json`, `requirements.txt`, `go.mod`, etc.
   - Determine testing frameworks and build tools
   - Configure implementation context

2. **Parallel Research Orchestration**
   - Parse Research Requirements from specification
   - Identify existing documentation paths (Read operations)
   - Identify external research needs (Synthesize operations)
   - Execute parallel operations for all research items
   - Collect documentation paths (not content)

3. **Implementation Planning Loop**
   - Initialize MCP refinement loop for build_plan
   - Invoke `build-planner` with research paths
   - Assess plan quality with `build-critic`
   - Iterate until plan quality threshold met

4. **Code Implementation Loop**
   - Initialize MCP refinement loop for build_code
   - Invoke `build-coder` for TDD implementation
   - Validate with `build-reviewer` for quality
   - Iterate until code quality threshold met

5. **Platform Integration & Documentation**
   - Update specification with implementation status
   - Link code changes to specification
   - Document completion in platform
   - Generate implementation summary

## Orchestration Pattern

### Complete Workflow Orchestration
```text
Main Agent (via /build)
    │
    ├── 1. Retrieve Specification
    │   └── Platform-specific retrieval or path access
    │
    ├── 2. Environment Discovery
    │   └── Bash: detect-packages.sh → technology context
    │
    ├── 3. Parallel Research Execution
    │   ├── Parse Research Requirements section
    │   ├── For each "Read: [path]" item:
    │   │   └── Read tool (parallel)
    │   ├── For each "Synthesize: [prompt]" item:
    │   │   └── Task: research-synthesizer (parallel)
    │   └── Collect: All documentation paths
    │
    ├── 4. Implementation Planning Loop
    │   ├── mcp_tool: initialize_refinement_loop(loop_type='build_plan')
    │   ├── Task: build-planner (with doc paths)
    │   ├── Task: build-critic → score
    │   └── mcp_tool: decide_loop_next_action(loop_id, score)
    │
    ├── 5. Code Implementation Loop
    │   ├── mcp_tool: initialize_refinement_loop(loop_type='build_code')
    │   ├── Task: build-coder (TDD approach)
    │   ├── Task: build-reviewer → score
    │   └── mcp_tool: decide_loop_next_action(loop_id, score)
    │
    └── 6. Completion & Documentation
        └── Platform update with results
```

### Parallel Research Pattern
```python
# Main Agent executes research in parallel
research_tasks = []

for item in research_requirements:
    if item.startswith("Read:"):
        path = extract_path(item)
        research_tasks.append(Read(path))
    elif item.startswith("Synthesize:"):
        prompt = extract_prompt(item)
        research_tasks.append(Task("research-synthesizer", prompt))

# Execute all tasks in parallel
results = await parallel_execute(research_tasks)

# Collect paths for build-planner
documentation_paths = [r.path for r in results]
```

## Quality Gates

### Build Planning Quality
- **Quality Threshold**: 80% (configurable via `FSDD_LOOP_BUILD_PLAN_THRESHOLD`)
- **Maximum Iterations**: 5 (configurable via `FSDD_LOOP_BUILD_PLAN_MAX_ITERATIONS`)
- **Assessment Focus**: Completeness, feasibility, test coverage

### Code Implementation Quality
- **Quality Threshold**: 95% (configurable via `FSDD_LOOP_BUILD_CODE_THRESHOLD`)
- **Maximum Iterations**: 5 (configurable via `FSDD_LOOP_BUILD_CODE_MAX_ITERATIONS`)
- **Assessment Focus**: Code quality, test passing, best practices

### Stagnation Detection
- **Both Loops**: Less than 5 points improvement over 2 iterations
- **Action**: MCP Server returns "user_input" status
- **Recovery**: Request specific guidance on blocked areas

## Research Integration Details

### Research Requirements Processing
```markdown
## Example Research Requirements Section

### Existing Documentation
- Read: ~/.claude/best-practices/react-hooks-patterns.md
- Read: ~/.claude/best-practices/testing-strategies.md

### External Research Needed
- Synthesize: Best practices for React Server Components in 2025
- Synthesize: Integration patterns for GraphQL with TypeScript
```

### Parallel Execution Strategy
```text
Main Agent identifies 4 research items:
    │
    ├── Read: react-hooks-patterns.md ────┐
    ├── Read: testing-strategies.md ───────┤ PARALLEL
    ├── Synthesize: React Server... ───────┤ EXECUTION
    └── Synthesize: GraphQL TypeScript... ─┘
                    │
                    ↓
    Collect 4 documentation paths
                    │
                    ↓
    Pass paths to build-planner
```

### Research Synthesizer Output
```markdown
# Research: [Topic]
## Synthesized: [Timestamp]

### Key Findings
[Detailed research results]

### Best Practices
[Actionable recommendations]

### Implementation Guidance
[Specific technical guidance]
```

## Platform-Specific Behavior

### Linear Platform
- **Specification Retrieval**: `mcp__linear-server__get_issue`
- **Progress Updates**: Comments on issue
- **Completion**: Update issue status and labels
- **Code Links**: Reference commits in comments

### GitHub Platform
- **Specification Retrieval**: `mcp__github__get_issue`
- **Progress Updates**: Issue comments
- **Completion**: Close issue with implementation PR
- **Code Links**: Auto-linked via commit messages

### Markdown Platform
- **Specification Retrieval**: `Read` from file path
- **Progress Updates**: Append to specification file
- **Completion**: Create implementation summary document
- **Code Links**: Document file paths and changes

## Input/Output Specifications

### Input Requirements
- **Specification Identifier**: Platform-specific reference or file path
- **Format**: Issue ID (Linear/GitHub) or file path (Markdown)
- **Required Sections**: Must contain Research Requirements

### Output Specifications

#### Build Plan Output
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

#### Implementation Output
- **Source Code**: Implemented features with tests
- **Test Results**: Passing test suites
- **Documentation**: Code comments and updates
- **Platform Updates**: Specification marked complete

## Error Handling

### Common Failure Scenarios

1. **Specification Not Found**
   - **Error**: "Cannot retrieve specification"
   - **Recovery**: Request specification location
   - **User Message**: "Please provide specification ID or path"

2. **Research Execution Failure**
   - **Error**: "Research synthesis failed for [topic]"
   - **Recovery**: Retry failed items, continue with available
   - **User Message**: "Some research failed. Proceeding with [X/Y] successful items."

3. **Environment Detection Failure**
   - **Error**: "Cannot detect project technology"
   - **Recovery**: Request manual technology specification
   - **User Message**: "Please specify: language, framework, test runner"

4. **Test Failures in Implementation**
   - **Error**: "Tests failing after max iterations"
   - **Recovery**: Present code with test report
   - **User Message**: "Implementation complete with test failures: [details]"

5. **Quality Threshold Not Met**
   - **Error**: "Quality below threshold after max iterations"
   - **Recovery**: Present best available with warnings
   - **User Message**: "Quality: [score]%. Key issues: [list]. Manual review recommended."

## Example Usage

### Complete Workflow Example
```
User: /build SPEC-1234

Main Agent: I'll implement the specification SPEC-1234. Let me start by retrieving it and setting up the implementation workflow.

[Retrieves specification from Linear]

Detecting project technology stack...
Found: React 18, TypeScript, Jest, GraphQL

Executing parallel research (4 items):
- Reading 2 existing documents...
- Synthesizing 2 external research topics...

[Parallel execution of research]

Research complete! Starting implementation planning...

[Invokes build-planner with documentation paths]

build-planner: Based on the research and specification, here's my implementation plan:

Phase 1: Setup GraphQL Schema
- Define type definitions
- Create resolver structure
- Setup Apollo Server

Phase 2: React Components
- Implement feedback list component
- Create detail view with AI insights
- Add filtering and sorting

Phase 3: Integration & Testing
- Connect frontend to GraphQL
- Write comprehensive tests
- Performance optimization

[Score: 82% - approved by build-critic]

Main Agent: Plan approved! Starting code implementation...

[Invokes build-coder]

build-coder: Implementing with TDD approach:

1. Writing tests for GraphQL schema...
2. Implementing schema to pass tests...
3. Writing component tests...
4. Implementing components...

[Shows code implementation]

[Score: 96% - approved by build-reviewer]

Main Agent: Implementation complete!
- All tests passing ✓
- Code quality: 96%
- Updated specification in Linear
- Ready for deployment

Summary:
- 15 files modified
- 42 tests passing
- 0 security issues
- Performance benchmarks met
```

## Implementation Notes

### Key Considerations for Claude Code

1. **Parallel Execution Management**
   - Use Promise.all or equivalent for research tasks
   - Handle partial failures gracefully
   - Timeout long-running research (30s max)

2. **Documentation Path Handling**
   - Pass paths, not content, to build-planner
   - Let build-planner read documents as needed
   - Avoid context overflow from large documents

3. **Technology Detection**
   - Cache detection results for session
   - Support multiple language projects
   - Fallback to user input if ambiguous

4. **Loop State Separation**
   - Maintain separate loop IDs for plan and code
   - Clear messaging about which loop is active
   - Show progress for each phase

5. **TDD Enforcement**
   - Ensure build-coder writes tests first
   - Validate test execution before implementation
   - Require green tests for completion

## Dependencies and Integration Points

### Required Components
- **MCP Server**: Dual loop state management
- **build-planner agent**: Implementation planning
- **build-critic agent**: Plan quality assessment
- **build-coder agent**: TDD implementation
- **build-reviewer agent**: Code quality validation
- **research-synthesizer agent**: External research

### MCP Tools Used
- `initialize_refinement_loop(loop_type='build_plan')`
- `initialize_refinement_loop(loop_type='build_code')`
- `decide_loop_next_action(loop_id, current_score)`
- Platform-specific retrieval and update tools

### Shell Scripts
- `~/.claude/scripts/detect-packages.sh`

### Environment Variables
- `FSDD_LOOP_BUILD_PLAN_THRESHOLD`: Plan quality (default: 80)
- `FSDD_LOOP_BUILD_PLAN_MAX_ITERATIONS`: Plan iterations (default: 5)
- `FSDD_LOOP_BUILD_CODE_THRESHOLD`: Code quality (default: 95)
- `FSDD_LOOP_BUILD_CODE_MAX_ITERATIONS`: Code iterations (default: 5)

## Success Metrics

### Quantitative Metrics
- **Plan Quality Score**: Target ≥80%
- **Code Quality Score**: Target ≥95%
- **Test Coverage**: Target >80%
- **Build Success Rate**: Target 100%
- **Research Success Rate**: Target >90%

### Qualitative Metrics
- **Implementation Completeness**: All specification requirements met
- **Code Maintainability**: Following best practices
- **Documentation Quality**: Clear and comprehensive
- **Performance**: Meeting specification benchmarks

## Related Documentation
- **Previous Phase**: [`/spec` Command Specification](spec.md)
- **Planning Agent**: [`build-planner` Agent Specification](../agents/build-planner.md)
- **Coding Agent**: [`build-coder` Agent Specification](../agents/build-coder.md)
- **Research Agent**: [`research-synthesizer` Agent Specification](../agents/research-synthesizer.md)
- **Refinement**: [`/refine-build-plan` Command](refine-build-plan.md) and [`/refine-build-code` Command](refine-build-code.md)