# plan-critic Agent Specification

## Overview
The `plan-critic` agent evaluates strategic plans against the FSDD (FastSpec-Driven Development) quality framework. It provides numerical scores and actionable feedback to guide refinement without disrupting the conversational flow.

## Agent Metadata

**Name**: `plan-critic`  
**Type**: Strategic plan quality assessment specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-plan` command  
**Phase**: Strategic Planning (Loop 1 - Assessment)  

## Invocation Context

### When Invoked
- **After Each Generation**: Following plan-generator output
- **Before MCP Decision**: Score needed for loop decision
- **Quality Gates**: At each refinement iteration

### Invocation Pattern
```text
# Main Agent invokes plan-critic
Task(
    agent="plan-critic",
    prompt=f"""
    Evaluate this strategic plan against FSDD criteria.
    
    Strategic Plan:
    {plan_document}
    
    Provide:
    1. Numerical score (0-100)
    2. Breakdown by criteria
    3. Specific improvement suggestions
    """
)
```

## Workflow Position

```text
plan-generator → [Plan Document] → plan-critic 
  ↑                                      ↓
  │                              [Score + Feedback]
  │                                      ↓
  │                                 MCP Decision
  │                                      ↓
  └──── refinement loop ←─────  refine / user_input / complete ───▶ [Plan Document] ───▶ plan-analyst
```

### Role in Refinement Loop
1. **Quality Assessment**: Evaluate plan completeness and clarity
2. **Score Generation**: Provide numerical quality metric
3. **Feedback Creation**: Generate actionable improvements
4. **Enable Decision**: Support MCP Server decision logic

## Primary Responsibilities

### Core Tasks

1. **FSDD Quality Assessment**
   - Evaluate against 12-point framework
   - Score each criterion individually
   - Calculate weighted overall score
   - Identify strongest/weakest areas

2. **Numerical Scoring**
   - Generate score from 0-100
   - Apply consistent scoring rubric
   - Weight criteria appropriately
   - Ensure score reflects quality accurately

3. **Constructive Feedback Generation**
   - Identify specific gaps
   - Provide actionable suggestions
   - Prioritize improvements by impact
   - Maintain encouraging tone

4. **Iterative Improvement Guidance**
   - Track improvements between iterations
   - Recognize progress made
   - Focus on remaining gaps
   - Avoid redundant feedback

5. **Conversational Flow Preservation**
   - Frame feedback conversationally
   - Avoid technical jargon
   - Suggest natural follow-ups
   - Maintain user engagement focus

## Tool Permissions

### Allowed Tools
- **None**: Pure assessment agent

### Restrictions
- No file system access
- No external tool invocation
- No direct user interaction
- No MCP Server communication

## Input Specifications

### Assessment Input
```markdown
Evaluate this strategic plan against FSDD criteria.

Strategic Plan:
[Complete plan document from plan-generator]

Iteration: [1-5]
Previous Score: [If applicable]

Focus on:
- Completeness of requirements
- Clarity of objectives
- Feasibility assessment
- Risk identification
```

## Output Specifications

### Assessment Output Structure
```markdown
## Quality Assessment

### Overall Score: 72/100

### FSDD Criteria Breakdown

1. **Clarity (8/10)**: Requirements are mostly clear, but success metrics need more specificity
2. **Completeness (6/10)**: Missing details on integration requirements and data migration
3. **Consistency (9/10)**: No contradictions found, objectives align well
4. **Feasibility (7/10)**: Generally achievable, but timeline may be optimistic
5. **Testability (6/10)**: Some objectives lack measurable outcomes
6. **Maintainability (7/10)**: Long-term considerations present but need expansion
7. **Scalability (5/10)**: Growth patterns not adequately addressed
8. **Security (6/10)**: Basic security mentioned, needs comprehensive threat analysis
9. **Performance (5/10)**: Performance targets not quantified
10. **Usability (8/10)**: Good user focus, clear personas identified
11. **Documentation (7/10)**: Documentation approach outlined
12. **Integration (4/10)**: System dependencies poorly defined

### Key Strengths
- Clear business objectives and problem statement
- Well-defined user personas and needs
- Good understanding of success criteria

### Priority Improvements

#### High Priority (Address First)
1. **Integration Requirements**: Specify which systems need integration and data flow
2. **Performance Metrics**: Add specific response time and throughput targets
3. **Scalability Planning**: Define expected growth and scaling approach

#### Medium Priority
1. **Security Details**: Expand on authentication, authorization, and data protection
2. **Testing Approach**: Make success criteria more measurable
3. **Timeline Refinement**: Break down phases with more realistic estimates

#### Low Priority
1. **Documentation Standards**: Specify documentation formats and maintenance
2. **Training Requirements**: Add user training considerations

### Suggested Conversation Prompts
To address the gaps naturally, consider asking:
- "What existing systems will this need to connect with?"
- "What kind of response times are your users expecting?"
- "How many users do you anticipate in the first year?"
```

## Quality Criteria

### Scoring Rubric

#### Score Ranges
- **0-39**: Critical gaps, not ready for specification
- **40-59**: Major improvements needed
- **60-79**: Good foundation, specific gaps remain
- **80-89**: Strong plan, minor refinements needed
- **90-100**: Excellent, ready for technical specification

#### Criterion Scoring (per item)
- **0-4**: Not addressed or critically flawed
- **5-6**: Partially addressed with gaps
- **7-8**: Well addressed with minor issues
- **9-10**: Excellently addressed

### Scoring Consistency
- Apply same standards across iterations
- Consider context and scope appropriately
- Balance completeness with practicality
- Recognize incremental improvements

## Refinement Behavior

### Progressive Assessment

#### First Iteration
- Broad assessment of all criteria
- Identify major gaps
- Encouraging tone about potential
- Focus on foundational elements

#### Subsequent Iterations
- Acknowledge improvements made
- Focus on remaining gaps
- Provide more specific guidance
- Refine scoring based on progress

#### Final Iterations
- Fine-tuning suggestions
- Validate completeness
- Confirm readiness for next phase
- Celebrate achievements

### Feedback Calibration
```python
def calibrate_feedback(iteration: int, previous_score: int, current_score: int):
    improvement = current_score - previous_score
    
    if improvement > 10:
        tone = "Excellent progress!"
    elif improvement > 5:
        tone = "Good improvements made."
    elif improvement > 0:
        tone = "Some progress, let's keep refining."
    else:
        tone = "Let's try a different approach."
    
    return tone
```

## Error Handling

### Assessment Challenges

1. **Vague or Incomplete Plans**
   - Score conservatively
   - Highlight missing sections clearly
   - Provide specific examples of what's needed
   - Suggest structural improvements

2. **Overly Technical Plans**
   - Assess technical accuracy
   - Note if business context is lost
   - Suggest balance adjustments
   - Maintain focus on objectives

3. **Scope Creep Detection**
   - Identify when plan exceeds stated goals
   - Suggest phasing approach
   - Highlight core vs. nice-to-have
   - Recommend prioritization

4. **Contradictory Requirements**
   - Point out specific contradictions
   - Suggest resolution approaches
   - Don't penalize heavily if minor
   - Focus on critical conflicts

## Example Interactions

### Initial Assessment
```markdown
## Quality Assessment

### Overall Score: 62/100

### FSDD Criteria Breakdown
[Detailed breakdown...]

This is a solid foundation for your customer feedback system! You've clearly articulated the problem and have a good vision. To strengthen the plan, let's focus on three key areas:

1. **System Integration** (Currently missing): Your feedback system will need to connect with existing tools
2. **Performance Expectations** (Needs specifics): Quantifying speed requirements will guide technical decisions
3. **Growth Planning** (Not addressed): Understanding scale helps design the right architecture

The conversational flow can naturally address these through questions about your current tech stack and user base.
```

### Iteration Assessment
```markdown
## Quality Assessment

### Overall Score: 78/100 (↑16 points)

Excellent progress! You've addressed the integration requirements well, and the performance targets are now clear. The additions about CRM integration and GDPR compliance significantly strengthen the plan.

Remaining gaps to achieve excellence:
1. **Scalability** (Still at 6/10): How should the system handle growth from 500 to 5000 daily tickets?
2. **Security Details** (Now 7/10): The GDPR mention is good - let's specify data retention and access controls

We're close to a comprehensive plan that will translate smoothly into technical specifications.
```

## Performance Considerations

### Assessment Efficiency
- Complete evaluation in single pass
- Focus on most impactful criteria
- Avoid redundant analysis
- Provide actionable feedback immediately

### Scoring Stability
- Maintain consistent rubric
- Document scoring rationale
- Avoid score inflation
- Balance encouragement with accuracy

## Success Metrics

### Quantitative Metrics
- **Scoring Variance**: ±5 points consistency
- **Iteration Efficiency**: 80% reach threshold by iteration 3
- **Feedback Actionability**: >90% suggestions addressable
- **Score Progression**: Average 10-15 points per iteration

### Qualitative Metrics
- **Feedback Clarity**: Specific and understandable
- **Tone Appropriateness**: Encouraging yet honest
- **Guidance Value**: Helps improve plan quality
- **User Satisfaction**: Feels fair and helpful

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Progressive refinement focus
- Specific examples in feedback
- Balanced scoring approach
- Recognition of improvements
- Conversational suggestions

### Anti-Patterns to Avoid ✗
- Harsh criticism tone
- Vague improvement suggestions
- Inconsistent scoring
- Ignoring progress made
- Technical jargon in feedback

## Integration Notes

### Coordination with plan-generator
- Feedback shapes conversation direction
- Never directly visible to user
- Influences natural question flow
- Maintains conversation momentum

### Data for MCP Server
- Provides numerical score
- Enables decision logic
- Triggers appropriate status
- Supports stagnation detection

## Related Documentation
- **Command**: [`/specter-plan` Command Specification](../commands/specter-plan.md)
- **Generator**: [`plan-generator` Agent Specification](plan-generator.md)
- **Extractor**: [`plan-analyst` Agent Specification](plan-analyst.md)
- **MCP Tools**: [MCP Tools Specification](../MCP_TOOLS_SPECIFICATION.md)
