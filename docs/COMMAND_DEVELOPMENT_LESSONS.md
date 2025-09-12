# Command Development Lessons: /plan Command Analysis

## Executive Summary

This document captures essential lessons learned from developing the `/plan` command within the Spec-Driven Development workflow system. Through iterative refinement and architectural evolution, several key patterns emerged that significantly improved command reliability, maintainability, and user experience. These insights provide actionable guidance for future command development.

## Command Architecture Patterns

### 1. Commands as Orchestrators, Not Executors

**Principle**: Commands should coordinate specialized agents rather than performing work directly.

**Pattern**:
```text
Main Agent (Command)
├── Initializes workflow state
├── Coordinates specialized agents
├── Manages quality gates
└── Handles completion/escalation
```

**Implementation**:
- Commands invoke agents through Task calls
- State management delegated to MCP Server
- Business logic contained within specialized agents
- Commands handle only coordination and error escalation

**Benefits**:
- Clear separation of concerns
- Reusable agent components
- Predictable failure modes
- Simplified testing and debugging

**Anti-Pattern**: Commands that contain business logic or attempt to perform multiple specialized functions.

### 2. Quality-Driven Refinement Architecture

**Principle**: Every workflow stage must have measurable quality criteria and automatic improvement cycles.

**Pattern**:
```text
Producer Agent → Content → Critic Agent → Score → MCP Decision
     ↑                                                    ↓
     └────── Refinement Loop ←─── "refine" ←──────────────┘
```

**Implementation**:
- Producer agents generate content
- Critic agents evaluate against FSDD framework (12-point quality assessment)
- MCP Server makes objective decisions based on numerical scores
- Automatic termination when quality threshold reached (85%+)
- Stagnation detection prevents infinite loops

**Key Components**:
- **Quality Thresholds**: Configurable via environment variables
- **Stagnation Detection**: 2 consecutive iterations below 5-point improvement
- **Escalation Strategy**: User input requested when AI reaches limits

**Benefits**:
- Objective quality assessment
- Consistent improvement cycles
- Automatic termination conditions
- Predictable behavior across workflows

### 3. Dynamic Template Generation with Platform Tool Injection

**Pattern**: Create templates as functions that inject platform-specific tools at generation time.

**Platform Tool Mapping**:
```python
PLATFORM_TOOL_MAPPING = {
    'linear': {
        'create_spec': 'mcp__linear-server__create_issue',
        'update_spec': 'mcp__linear-server__update_issue',
        'get_spec': 'mcp__linear-server__get_issue'
    },
    'github': {
        'create_spec': 'mcp__github__create_issue',
        'update_spec': 'mcp__github__update_issue',
        'get_spec': 'mcp__github__get_issue'
    },
    'markdown': {
        'create_spec': 'Write',
        'update_spec': 'Edit',
        'get_spec': 'Read'
    }
}
```

**Template Function with Injection**:
```python
def generate_spec_command_template(
    create_spec_tool: str,
    get_spec_tool: str,
    update_spec_tool: str,
    spec_implementation: str,
) -> str:
    return f"""---
allowed-tools:
  - Task(plan-analyst)
  - Task(spec-architect) 
  - {create_spec_tool}
  - {get_spec_tool}
  - {update_spec_tool}
description: Convert strategic plans using {spec_implementation}
---

# Technical Specification Creation
Use {create_spec_tool} to create specifications on {spec_implementation} platform.
"""
```

**Generation Process**:
```python
# Platform-specific template generation
tools = PLATFORM_TOOL_MAPPING[platform]
template = generate_spec_command_template(
    create_spec_tool=tools['create_spec'],
    get_spec_tool=tools['get_spec'],
    update_spec_tool=tools['update_spec'],
    spec_implementation=platform.title()
)
```

**Benefits**:
- Single template function generates platform-specific commands
- Tools injected based on target platform (Linear/GitHub/Markdown)
- Consistent command logic with platform-appropriate tool usage
- Easy platform addition through tool mapping updates

## Documentation Structure for Predictable Behavior

### 1. Standardized Agent Specification Format

**Essential Sections**:

1. **Agent Metadata**
   - Name, type, model, invocation context
   - Creates clear identity and scope

2. **Invocation Context**
   - When invoked, invocation patterns with code examples
   - Eliminates ambiguity about usage

3. **Workflow Position**
   - Visual diagrams showing agent's role in larger workflow
   - Prevents confusion about responsibilities

4. **Primary Responsibilities**
   - Numbered core tasks with clear boundaries
   - Prevents scope creep and capability drift

5. **Tool Permissions**
   - Explicitly allowed and restricted tools
   - Prevents unauthorized operations

6. **Input/Output Specifications**
   - Exact formats with examples
   - Enables reliable inter-agent communication

7. **Quality Criteria**
   - Measurable success metrics
   - Enables objective evaluation

8. **Error Handling**
   - Specific scenarios and responses
   - Ensures graceful degradation

9. **Example Interactions**
   - Concrete usage patterns
   - Reduces implementation ambiguity

### 2. Specification-Driven Behavior

**Principle**: Documentation should drive agent behavior, not describe it after the fact.

**Implementation**:
Use the [Agent Input Specification Template](../fsdd-templates/AGENT_INPUT_SPECIFICATION_TEMPLATE.md) to create clear, actionable input specifications that drive predictable agent behavior.

**Example Usage in Command Templates**:
```text
Invoke the plan-critic agent with this context:

Strategic Plan:
${CURRENT_PLAN}
```

**Benefits**:
- Predictable agent responses
- Clear expectations for integration
- Reduced debugging time
- Consistent behavior patterns

### 3. Visual Workflow Documentation

**Pattern**: Use ASCII diagrams to show data flow and agent relationships

```text
/plan command → plan-generator → Strategic Plan → plan-critic
       ↑                                              ↓
       └──────────── refinement loop ←───────────────┘
```

**Benefits**:
- Immediate understanding of system architecture
- Clear handoff points between components
- Visual debugging aid
- Simplified onboarding for new developers

## Variable Management Systems

### 1. Externalized State Management

**Principle**: Workflow state should be managed by dedicated services, not individual agents.

**Implementation**:
- MCP Server manages loop state and decision logic
- Agents remain stateless and receive complete context per invocation
- State transitions handled through centralized decision engine

**Pattern**:
```text
Invoke the plan-generator agent with this context:

Context: ${CONVERSATION_CONTEXT}
Previous Feedback: ${PREVIOUS_FEEDBACK}
```

**Benefits**:
- No state synchronization issues
- Predictable agent behavior
- Easy debugging and monitoring
- Consistent decision logic

### 2. Structured Data Exchange

**Principle**: Use well-defined document formats for inter-agent communication.

**Implementation**:
- Markdown documents as primary data exchange format
- Structured sections with consistent naming
- Complete context passed in each invocation
- No shared mutable state between agents

**Format Example**:
```markdown
# Strategic Plan: [Project Name]

## Executive Summary
[High-level overview]

## Business Objectives
- [Objective 1]
- [Objective 2]

## Success Criteria
[Measurable outcomes]
```

**Benefits**:
- Human-readable intermediate outputs
- Clear data contracts between agents
- Easy debugging and validation
- Maintains context across refinement cycles

## Error Handling Patterns for Reliability

### 1. Graceful Degradation Strategy

**Principle**: System should provide best available service even when components fail.

**Implementation**:
```text
If MCP Server unavailable:
- Continue with direct agent coordination
- Display warning about degraded functionality

If critic agent unavailable:
- Proceed with generator output only
- Skip quality assessment loop

Always provide best available output with warnings
```

**Benefits**:
- System remains functional during partial failures
- Users get value even in degraded scenarios
- Prevents complete workflow failure
- Maintains user confidence

### 2. Proactive Stagnation Detection

**Principle**: Detect and handle improvement plateaus before they become infinite loops.

**Algorithm**:
```text
Stagnation Detection Logic:
1. Track quality scores across iterations
2. Calculate improvement between consecutive iterations
3. Detect stagnation when:
   - 2 consecutive improvements < 5 points
   - Quality plateau reached
4. Escalate to user input when stagnation detected
```

**Response Strategy**:
- Automatic escalation to user with specific guidance
- Clear explanation of stagnation state
- Actionable suggestions for breaking the plateau

**Benefits**:
- Prevents infinite refinement loops
- Provides user with control when AI reaches limits
- Clear feedback about system state

### 3. Standardized Error Response Format

**Pattern**:
```json
{
  "error_type": "loop_stagnation|agent_failure|mcp_error|timeout",
  "error_message": "Detailed error description",
  "recovery_action": "Specific recovery steps",
  "user_guidance": "Clear instructions for user",
  "partial_output": "Any salvageable work"
}
```

**Benefits**:
- Consistent error handling across all components
- Clear guidance for users
- Actionable recovery information
- Preserves partial work when possible

## Context Preservation in Command Templates

### Context Preservation Strategy

**Principle**: Maintain conversation and workflow context across refinement cycles.

**Implementation**:
- Complete conversation history passed to each agent invocation
- Technical assessments hidden from user interaction
- Natural dialogue flow preserved despite complex backend processing
- Context summarization to manage size constraints

**Pattern**:
```text
Context Management Structure:
- CONVERSATION_CONTEXT: Full dialogue history
- PREVIOUS_FEEDBACK: Latest critic suggestions  
- CURRENT_PLAN: Most recent generator output
- QUALITY_SCORE: Numerical assessment (0-100)
- LOOP_STATUS: Current refinement state
```

**Benefits**:
- Seamless user experience
- Consistent refinement direction
- Preserved conversation flow
- Effective context utilization

## Template Optimization Techniques

### Template Function Structure and Organization

**Pattern**: Create command templates as Python functions with consistent structure and organization.

**Static Template Function** (for commands without platform-specific tools):
```python
def generate_plan_command_template() -> str:
    return """---
allowed-tools: 
  - Task(plan-generator)
  - Task(plan-critic)
  - Task(plan-analyst)
  - Bash(~/.claude/scripts/detect-packages.sh)
argument-hint: [plan-name] [starting-prompt]
description: Create strategic plans through conversational discovery
---

# /plan Command Template
[Static content - no platform-specific tools needed]
"""
```

**Directory Organization**:
```text
services/templates/
├── agents/
│   ├── plan-command.py
│   ├── spec-command.py
│   └── build-command.py
├── commands/
│   └── [generated files]
└── shared/
    └── common_patterns.py
```

**YAML Frontmatter Structure**:
- `allowed-tools`: List of permitted tools and agents
- `argument-hint`: Expected parameter format
- `description`: Clear purpose statement

**Benefits**:
- Programmatic generation enables customization
- Clear separation between templates and generated files
- Consistent metadata structure across all commands
- Easy validation of command requirements
- Self-documenting command capabilities

## Implementation Guidelines

### For Command Development

1. **Start with Orchestration Pattern**
   - Define main command as coordinator only
   - Identify required specialized agents
   - Plan MCP tool integration points

2. **Design Quality Framework First**
   - Define measurable success criteria
   - Create critic agent for assessment
   - Establish quality thresholds and refinement loops

3. **Implement Graceful Degradation**
   - Plan for component failures
   - Design fallback behaviors
   - Provide partial value when possible

4. **Document Before Implementation**
   - Create detailed specifications for all agents
   - Define input/output formats with examples
   - Document error scenarios and responses

## Success Metrics and Validation

### Quality Indicators

1. **Command Reliability**
   - Completion rate >95%
   - User escalation rate <20%
   - Average iterations to completion ≤3

2. **Agent Consistency**
   - Predictable responses to same inputs
   - Quality score variance <10%
   - Error rate <5%

3. **Documentation Effectiveness**
   - Implementation matches specification
   - Error scenarios properly handled
   - User understanding rate >90%

## Conclusion

The `/plan` command development process revealed that successful multi-agent workflow systems require:

1. **Clear Architecture**: Commands as orchestrators with specialized agents
2. **Quality-Driven Development**: Measurable criteria and automatic refinement
3. **Robust Documentation**: Specifications that drive predictable behavior
4. **Reliable State Management**: Externalized state with stateless agents
5. **Graceful Error Handling**: Proactive failure detection and recovery
6. **Template Optimization**: Dynamic generation with scope isolation

These patterns provide a foundation for creating reliable, maintainable, and extensible command systems that can evolve with changing requirements while maintaining consistent quality and user experience.

## Related Documentation

- [/plan Command Specification](commands/plan.md) - Complete command specification
- [MCP Tools Specification](MCP_TOOLS_SPECIFICATION.md) - Loop state management tools
- [Architecture Guide](ARCHITECTURE.md) - System architecture overview
- [Agent Development Guidelines](AGENT_DEVELOPMENT_GUIDELINES.md) - Agent creation standards
