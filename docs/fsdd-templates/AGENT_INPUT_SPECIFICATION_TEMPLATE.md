# Agent Input Specification Template

## Purpose
Template for creating clear, actionable input specifications that drive predictable agent behavior. Use this format when defining how agents should receive and process context.

## Template Structure

### Input Specifications
```markdown
Analyze this strategic plan against FSDD criteria.

Strategic Plan:
{plan_document}

Provide:
1. Numerical score (0-100)
2. Breakdown by criteria
3. Specific improvement suggestions
```

## Usage Guidelines

### When to Use This Template
- Defining agent input patterns in command templates
- Creating consistent data exchange formats
- Ensuring predictable agent responses
- Documenting inter-agent communication

### Template Variables
- `{plan_document}` - Replace with actual content variable name
- `{criteria}` - Replace with specific assessment framework
- `{output_format}` - Define expected response structure

### Implementation Example
In command templates, use this pattern:
```text
Invoke the plan-critic agent with this context:

Strategic Plan:
${CURRENT_PLAN}
```

## Benefits
- Clear expectations for integration
- Predictable agent responses
- Reduced debugging time
- Consistent behavior patterns
