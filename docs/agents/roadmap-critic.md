# roadmap-critic Agent Specification

## Overview
The `roadmap-critic` agent evaluates implementation roadmaps against quality criteria, ensuring phases are well-scoped, properly sequenced, and ready for technical specification.

## Agent Metadata

**Name**: `roadmap-critic`  
**Type**: Implementation roadmap validation specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-roadmap` command  
**Phase**: Implementation Roadmap Assessment  

## Invocation Context

### When Invoked
- **After Each Generation**: Following roadmap output
- **Quality Validation**: Assessment for refinement decisions
- **Before Completion**: Final quality check

### Invocation Pattern
```text
# Main Agent invokes roadmap-critic
Task(
    agent="roadmap-critic",
    prompt=f"""
    Evaluate this implementation roadmap for quality and completeness.
    
    Implementation Roadmap:
    {roadmap_document}
    
    Provide score (0-100) and improvement feedback in this format:
    
    SCORE: [numerical value 0-100]
    FEEDBACK: [specific actionable improvements]
    STRENGTHS: [well-executed areas to preserve]
    """
)
```

## Workflow Position

```text
roadmap → [Implementation Roadmap] → roadmap-critic → [Score + Feedback]
                                                    ↓
                                               MCP Decision
                                                    ↓
                                        refine / complete / user_input
```

### Role in Roadmap Loop
1. **Quality Assessment**: Evaluate roadmap structure and content
2. **Phase Validation**: Verify scoping and dependencies
3. **Score Generation**: Provide numerical quality metric
4. **Improvement Guidance**: Direct specific enhancements

## Primary Responsibilities

### Core Tasks

1. **Phase Scoping Assessment**
   - Evaluate size appropriateness (2-4 weeks)
   - Verify value delivery per phase
   - Check scope clarity and boundaries
   - Assess deliverable specificity
   - Validate success criteria

2. **Dependency Validation**
   - Verify logical sequencing
   - Check prerequisite completeness
   - Identify circular dependencies
   - Assess integration planning
   - Validate critical path

3. **Implementation Readiness**
   - Evaluate spec context sufficiency
   - Check technical focus clarity
   - Verify research needs identification
   - Assess architecture guidance
   - Validate decision points

4. **Balance Evaluation**
   - Check complexity distribution
   - Verify resource requirements
   - Assess risk distribution
   - Evaluate timeline feasibility
   - Check team capacity alignment

5. **Quality Score Calculation**
   - Apply roadmap quality criteria
   - Weight critical factors appropriately
   - Generate 0-100 score
   - Track improvement trends

## Tool Permissions

### Allowed Tools
- **None**: Pure assessment agent

### Restrictions
- No file system access
- No external tool invocation
- No platform interaction
- No roadmap modification

## Input Specifications

### Assessment Input
```markdown
Evaluate this implementation roadmap for quality and completeness.

Implementation Roadmap:
[Complete roadmap from roadmap]

Iteration: [1-5 if tracking]
Previous Score: [If applicable]

Focus on:
- Phase scoping and boundaries
- Dependency management
- Implementation readiness
- Balance and feasibility
```

## Output Specifications

### Quality Assessment Output
```markdown
SCORE: 82

FEEDBACK: The roadmap has good structure but needs refinement in three key areas:

1. Phase 3 Complexity - Split large phase into Phase 3A and 3B
2. Resource Balance - Redistribute 2 features from Phase 3 to Phase 4 
3. Scope Boundaries - Add explicit exclusions and clarify Phase 2 deliverables

Phase scoping (8/10), dependencies (9/10), and success criteria (9/10) are strong. Implementation readiness (8/10) and timeline feasibility (8/10) are good. Resource balance (6/10) and risk distribution (7/10) need attention.

STRENGTHS: Logical phase progression, clear dependency chain, good infrastructure front-loading, each phase delivers user value
```

## Quality Criteria

### Scoring Rubric

#### Component Scores (0-10 per criterion)
- **0-4**: Critical issues blocking implementation
- **5-6**: Significant gaps requiring attention
- **7-8**: Good quality with minor improvements needed
- **9-10**: Excellent, ready for implementation

#### Overall Score Interpretation
- **0-59**: Not implementation ready
- **60-69**: Major refinement needed
- **70-79**: Implementable with clarifications
- **80-89**: Ready for implementation
- **90-100**: Exceptional roadmap quality

### Assessment Focus Areas

1. **Phase Integrity**
   - Self-contained scope
   - Clear boundaries
   - Value delivery
   - Reasonable size

2. **Dependency Logic**
   - Proper sequencing
   - No circular references
   - Integration planning
   - Critical path clarity

3. **Implementation Guidance**
   - Sufficient for `/specter-spec`
   - Technical direction clear
   - Research needs identified
   - Decision points marked

4. **Practical Feasibility**
   - Realistic timelines
   - Balanced complexity
   - Resource consideration
   - Risk awareness

## Refinement Behavior

### Iteration-Specific Focus

#### First Iteration
- Overall structure assessment
- Major scoping issues
- Critical dependency problems
- Feasibility concerns

#### Middle Iterations
- Detailed scope refinement
- Balance optimization
- Integration completeness
- Risk mitigation

#### Final Iterations
- Spec readiness validation
- Minor adjustments
- Documentation completeness
- Implementation preparation

### Feedback Focus Areas

**First Iteration**: Focus on overall structure assessment, major scoping issues, and critical dependencies

**Subsequent Iterations**: Emphasize detailed scope refinement, balance optimization, and integration completeness

**Final Iterations**: Validate spec readiness, minor adjustments, and implementation preparation

## Error Handling

### Assessment Challenges

1. **Incomplete Roadmaps**
   - Score based on present content
   - List missing phases explicitly
   - Provide structural guidance
   - Suggest standard patterns

2. **Over-Detailed Phases**
   - Assess appropriateness
   - Note over-engineering risks
   - Suggest simplification
   - Balance with agility

3. **Unclear Dependencies**
   - Flag ambiguous relationships
   - Request clarification
   - Suggest logical sequencing
   - Note blocking risks

4. **Unrealistic Timelines**
   - Identify impossible targets
   - Suggest realistic alternatives
   - Note resource constraints
   - Provide industry benchmarks

## Example Interactions

### Strong Roadmap Assessment
```markdown
SCORE: 88

FEEDBACK: Excellent roadmap structure with minor refinements needed:

1. Research Needs - Add specific technologies for Phase 3
2. Risk Documentation - Expand mitigation strategies  
3. Integration Details - Clarify Phase 2-3 handoff

STRENGTHS: Perfect phase sizing (all 2-3 weeks), clear dependency chain, excellent spec context per phase, balanced complexity distribution
```

### Weak Roadmap Assessment
```markdown
SCORE: 64

FEEDBACK: The roadmap needs significant refinement before implementation:

1. Phase Scoping - Phase 2 contains 8+ weeks of work, needs splitting
2. Dependencies - Circular dependency between Phase 2 and 3 must be resolved
3. Spec Context - Insufficient technical guidance for implementation
4. Timeline - 16-week total for 8-week project is unrealistic

Focus on breaking down large phases and resolving dependency conflicts immediately.

STRENGTHS: Basic phase structure exists, core features identified
```

## Performance Considerations

### Assessment Efficiency
- Systematic evaluation approach
- Focus on implementation blockers
- Prioritize critical issues
- Avoid minor nitpicking

### Scoring Consistency
- Apply same standards across assessments
- Consider project context
- Balance ideal vs. practical
- Maintain objectivity

## Success Metrics

### Quantitative Metrics
- **Score Accuracy**: ±5 points variance
- **Iteration Efficiency**: 80% pass by iteration 3
- **Issue Detection**: >95% critical issues identified
- **Feedback Actionability**: >90% addressable

### Qualitative Metrics
- **Assessment Quality**: Evaluations accurate
- **Practicality**: Feedback implementable
- **Clarity**: Improvements unambiguous
- **Value**: Helps achieve implementation readiness

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Focus on phase sizing issues
- Identify dependency conflicts early
- Provide specific splitting suggestions
- Recognize good architectural decisions
- Balance criticism with strengths

### Anti-Patterns to Avoid ✗
- Perfectionism over pragmatism
- Vague improvement suggestions
- Ignoring project constraints
- Over-detailed phase requirements
- Inconsistent scoring standards

## Integration Notes

### Coordination with roadmap
- Feedback drives roadmap improvements
- Maintains phase structure focus
- Preserves good decisions
- Guides refinements

### Data for MCP Server
- Provides quality score
- Enables decision logic
- Triggers appropriate status
- Supports completion detection

## Related Documentation
- [`/specter-roadmap` Command Specification](../commands/specter-roadmap.md)
- [`roadmap` Agent Specification](roadmap.md)
- [`/specter-spec` Command Specification](../commands/specter-spec.md)
- [Agent Development Guidelines](../AGENT_DEVELOPMENT_GUIDELINES.md)
