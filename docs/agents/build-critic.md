# build-critic Agent Specification

## Overview
The `build-critic` agent evaluates implementation plans for completeness, feasibility, and alignment with specifications. It ensures plans are actionable, properly sequenced, and include comprehensive testing strategies.

## Agent Metadata

**Name**: `build-critic`  
**Type**: Implementation plan assessment specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-build` command  
**Phase**: Implementation Planning (Loop 3 - Assessment)  

## Invocation Context

### When Invoked
- **After Each Planning**: Following build-planner output
- **Quality Gate**: Before proceeding to coding
- **Refinement Trigger**: Provides improvement feedback

### Invocation Pattern
```python
# Main Agent invokes build-critic
response = Task(
    agent="build-critic",
    prompt=f"""
    Evaluate this implementation plan for quality and completeness.
    
    Implementation Plan:
    {plan_document}
    
    Technical Specification:
    {specification_summary}
    
    Assess actionability, completeness, and feasibility.
    Provide score (0-100) and specific improvements.
    """
)
```

## Workflow Position

```text
build-planner → [Implementation Plan] → build-critic → [Score + Feedback]
                                              ↓
                                         MCP Decision
                                              ↓
                                 refine / complete / user_input
```

### Role in Planning Loop
1. **Plan Assessment**: Evaluate implementation approach
2. **Feasibility Check**: Verify realistic execution
3. **Completeness Validation**: Ensure all aspects covered
4. **Quality Scoring**: Enable MCP decisions

## Primary Responsibilities

### Core Tasks

1. **Task Specificity Assessment**
   - Verify tasks are actionable
   - Check for clear acceptance criteria
   - Ensure measurable outcomes
   - Validate task granularity
   - Assess effort estimates

2. **Dependency Validation**
   - Verify logical sequencing
   - Check for circular dependencies
   - Validate prerequisite availability
   - Assess parallel execution opportunities
   - Identify blocking tasks

3. **Test Coverage Evaluation**
   - Check test strategy completeness
   - Verify test types coverage
   - Assess test data planning
   - Validate performance testing
   - Review security testing

4. **Research Integration Check**
   - Verify research findings applied
   - Check best practices adoption
   - Validate pattern implementation
   - Assess anti-pattern avoidance
   - Confirm tool recommendations used

5. **Risk Assessment Review**
   - Validate risk identification
   - Check mitigation strategies
   - Assess contingency planning
   - Verify rollback procedures
   - Evaluate checkpoint definitions

## Tool Permissions

### Allowed Tools
- **None**: Pure assessment agent

### Restrictions
- No file system access
- No code execution
- No external validation
- No plan modification

## Input Specifications

### Assessment Input
```text
Evaluate this implementation plan for quality and completeness.

Implementation Plan:
[Complete plan from build-planner]

Technical Specification Summary:
[Key requirements and constraints]

Iteration: [1-5]
Previous Score: [If applicable]

Focus on:
- Task actionability
- Dependency clarity
- Test completeness
- Risk mitigation
```

## Output Specifications

### Plan Assessment Output
```markdown
## Implementation Plan Assessment

### Overall Score: 82/100

### Assessment Criteria

1. **Task Specificity (8/10)**
   - Most tasks are actionable
   - Missing: Specific file paths for some tasks
   - Missing: Time estimates for Phase 3

2. **Dependency Management (9/10)**
   - Clear task sequencing
   - Dependencies well mapped
   - Minor: Could identify more parallel opportunities

3. **Phase Organization (8/10)**
   - Logical progression
   - Good milestone definition
   - Gap: Phase 4 could be split further

4. **Test Strategy (7/10)**
   - Unit tests well planned
   - Missing: Integration test scenarios
   - Missing: Load test specifications

5. **Code Structure (8/10)**
   - Clear file organization
   - Component structure defined
   - Gap: Service layer not fully specified

6. **Research Integration (9/10)**
   - Excellent use of research findings
   - Patterns properly applied
   - Minor: One research doc not referenced

7. **Risk Mitigation (7/10)**
   - Main risks identified
   - Basic mitigation strategies
   - Missing: Detailed rollback procedures

8. **Success Criteria (8/10)**
   - Most tasks have clear outcomes
   - Metrics defined
   - Gap: Some criteria not measurable

9. **Timeline Realism (7/10)**
   - Generally realistic
   - Some phases may be optimistic
   - Needs buffer time

10. **Documentation Planning (6/10)**
    - Basic approach mentioned
    - Missing: Specific documentation tasks
    - Missing: Documentation standards

### Key Strengths
- Excellent phase-based structure with clear progression
- Strong research integration with specific patterns applied
- Good use of code examples from research
- Clear component architecture

### Priority Improvements

#### High Priority
1. **Test Scenario Detail**
   - Add specific test cases for each component
   - Include test data requirements
   - Specify performance benchmarks
   - Add security test scenarios

2. **Task Granularity**
   ```markdown
   Current: "Implement feedback service"
   Better: 
   - [ ] Create feedback.service.ts with IFeedbackService interface
   - [ ] Implement getFeedback(id: string) method
   - [ ] Add createFeedback(data: CreateFeedbackDto) method
   - [ ] Write unit tests for service methods
   ```

3. **Rollback Procedures**
   - Add specific rollback steps for each phase
   - Include data migration rollback
   - Specify feature flag approach

#### Medium Priority
1. **Time Estimates**
   - Add hour estimates to tasks
   - Include buffer for unknowns
   - Specify critical path

2. **Documentation Tasks**
   - Add API documentation generation
   - Include README updates
   - Specify inline documentation standards

#### Low Priority
1. **Parallel Execution**
   - Identify tasks that can run simultaneously
   - Note resource requirements
   - Optimize timeline

### Feasibility Assessment
- **Technical Feasibility**: High - approach is sound
- **Timeline Feasibility**: Medium - may need 20% buffer
- **Resource Feasibility**: High - within team capabilities
- **Risk Level**: Medium - manageable with proposed mitigations

### Specific Examples Needed

#### For API Implementation
```typescript
// Add this level of detail:
interface FeedbackAPI {
  GET /api/feedback?page=1&limit=20
  POST /api/feedback
  PUT /api/feedback/:id
  DELETE /api/feedback/:id
}

// With specific error handling:
try {
  const result = await feedbackService.create(data);
  return res.status(201).json(result);
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({ error: error.message });
  }
  // ... more error cases
}
```

### Research Gaps
- Research document on caching strategies mentioned but not applied
- Consider adding Redis caching tasks to Phase 2

### Overall Assessment
The plan provides a solid foundation for implementation with good research integration. Adding more specificity to tasks and test scenarios will make it truly developer-ready. The phased approach is excellent and risk awareness is good.
```

## Quality Criteria

### Scoring Rubric

#### Component Scores (0-10)
- **0-4**: Critical planning gaps
- **5-6**: Basic plan, needs work
- **7-8**: Good plan, minor gaps
- **9-10**: Excellent, fully actionable

#### Overall Score Interpretation
- **0-39**: Not implementable
- **40-59**: Major planning gaps
- **60-79**: Implementable with clarification
- **80-89**: Ready for development
- **90-100**: Exceptional planning

### Assessment Focus Areas

1. **Actionability**
   - Can developer start immediately?
   - Are tasks self-contained?
   - Is success measurable?

2. **Completeness**
   - All requirements addressed?
   - Testing strategy comprehensive?
   - Documentation planned?

3. **Feasibility**
   - Timeline realistic?
   - Resources adequate?
   - Risks manageable?

4. **Quality**
   - Best practices followed?
   - Research applied?
   - Standards defined?

## Refinement Behavior

### Iteration-Specific Focus

#### First Iteration
- Overall structure assessment
- Major gap identification
- Feasibility concerns
- Risk completeness

#### Middle Iterations
- Task specificity
- Test detail
- Timeline refinement
- Documentation planning

#### Final Iterations
- Fine-tuning estimates
- Example code completeness
- Edge case handling
- Operational readiness

### Feedback Progression
```python
def generate_feedback(iteration: int, score: int):
    if iteration == 1:
        focus = "plan structure and completeness"
    elif iteration <= 3:
        focus = "task specificity and testing"
    else:
        focus = "implementation readiness"
    
    if score < 60:
        urgency = "Critical gaps need addressing"
    elif score < 80:
        urgency = "Good progress, key improvements needed"
    else:
        urgency = "Nearly ready, final refinements"
    
    return f"{urgency}. Focus: {focus}"
```

## Error Handling

### Assessment Challenges

1. **Vague Task Descriptions**
   - Flag non-actionable tasks
   - Provide specific examples
   - Suggest decomposition
   - Show proper format

2. **Missing Test Strategy**
   - Highlight testing gaps
   - Suggest test types needed
   - Provide test examples
   - Recommend coverage targets

3. **Unrealistic Timeline**
   - Identify optimistic estimates
   - Suggest realistic ranges
   - Recommend buffer addition
   - Note complexity factors

4. **Poor Research Integration**
   - Point out unused research
   - Suggest applicable patterns
   - Highlight missed recommendations
   - Note anti-patterns present

## Example Interactions

### Strong Plan Assessment
```markdown
## Implementation Plan Assessment

### Overall Score: 91/100

Excellent implementation plan! This is developer-ready with minor enhancements possible.

Standout elements:
- Task breakdown is specific and actionable
- Excellent research integration throughout
- Comprehensive test strategy with scenarios
- Clear success criteria for each phase

Minor suggestions:
- Add performance profiling tasks in Phase 4
- Include accessibility testing checklist
- Specify monitoring setup tasks

Ready to proceed to implementation!
```

### Weak Plan Assessment
```markdown
## Implementation Plan Assessment

### Overall Score: 54/100

The plan has good intentions but lacks the specificity needed for implementation.

Critical gaps:
1. **Tasks too vague**: "Setup API" needs breakdown into specific endpoints
2. **No test details**: "Write tests" needs scenarios and coverage targets
3. **Missing dependencies**: Phase 2 assumes Phase 1 deliverables not specified
4. **No research applied**: Research docs mentioned but patterns not used

Immediate focus needed:
- Break each task into 2-4 hour chunks
- Add specific test scenarios
- Apply patterns from research docs
```

## Performance Considerations

### Assessment Efficiency
- Single-pass evaluation
- Focus on blocking issues
- Prioritize actionability
- Avoid perfectionism

### Scoring Consistency
- Apply same standards
- Consider project scope
- Balance ideal vs practical
- Maintain objectivity

## Success Metrics

### Quantitative Metrics
- **Score Accuracy**: ±5 points variance
- **Pass Rate**: 80% by iteration 3
- **Feedback Actionability**: >90%
- **Gap Detection**: >95% of issues

### Qualitative Metrics
- **Feedback Clarity**: Specific improvements
- **Example Quality**: Helpful code samples
- **Practicality**: Achievable suggestions
- **Value Add**: Improves plan quality

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Specific task examples
- Realistic time estimates
- Clear dependencies
- Comprehensive testing
- Research application

### Anti-Patterns to Avoid ✗
- Vague feedback
- Impossible standards
- Ignoring constraints
- Over-engineering
- Missing context

## Integration Notes

### Coordination with build-planner
- Provides improvement guidance
- Maintains plan structure
- Focuses on gaps
- Preserves strengths

### Data for MCP Server
- Provides quality score
- Enables decision logic
- Triggers status changes
- Supports loop completion

### Preparation for build-coder
- Ensures actionable plan
- Validates completeness
- Confirms feasibility
- Enables smooth coding

## Related Documentation
- **Command**: [`/specter-build` Command Specification](../commands/specter-build.md)
- **Planner**: [`build-planner` Agent Specification](build-planner.md)
- **Next Agent**: [`build-coder` Agent Specification](build-coder.md)
- **MCP Tools**: [MCP Tools Specification](../MCP_TOOLS_SPECIFICATION.md)
