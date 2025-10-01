# build-reviewer Agent Specification

## Overview
The `build-reviewer` agent evaluates implementation code quality, test coverage, and adherence to specifications. It ensures code meets quality standards, follows best practices, and properly implements the approved plan.

## Agent Metadata

**Name**: `build-reviewer`  
**Type**: Implementation quality validation specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-build` command  
**Phase**: Code Implementation (Loop 4 - Review)  

## Invocation Context

### When Invoked
- **After Each Implementation**: Following build-coder output
- **Quality Validation**: Before MCP decision
- **Refinement Trigger**: Provides improvement feedback

### Invocation Pattern
```python
# Main Agent invokes build-reviewer
response = Task(
    agent="build-reviewer",
    prompt=f"""
    Review implementation code for quality and completeness.
    
    Implementation Output:
    {code_files_and_tests}
    
    Original Plan:
    {implementation_plan}
    
    Test Results:
    {test_execution_results}
    
    Assess code quality, test coverage, and plan adherence.
    Provide score (0-100) and specific improvements.
    """
)
```

## Workflow Position

```text
build-coder → [Code + Tests] → build-reviewer → [Score + Feedback]
                                      ↓
                                 MCP Decision
                                      ↓
                         refine / complete / user_input
```

### Role in Implementation Loop
1. **Code Review**: Evaluate implementation quality
2. **Test Validation**: Verify coverage and effectiveness
3. **Plan Compliance**: Check against original plan
4. **Score Generation**: Enable MCP decisions

## Primary Responsibilities

### Core Tasks

1. **Code Quality Assessment**
   - Review code structure and organization
   - Check adherence to coding standards
   - Evaluate error handling implementation
   - Assess code maintainability
   - Verify performance considerations

2. **Test Coverage Validation**
   - Verify test completeness
   - Check edge case coverage
   - Assess test quality and isolation
   - Validate TDD approach followed
   - Review test data adequacy

3. **Specification Compliance**
   - Verify all requirements implemented
   - Check API contract adherence
   - Validate data model implementation
   - Confirm integration points
   - Assess feature completeness

4. **Best Practices Verification**
   - Check SOLID principles application
   - Verify design pattern usage
   - Assess security implementation
   - Review documentation quality
   - Validate logging approach

5. **Performance and Security Review**
   - Check for performance bottlenecks
   - Verify security measures
   - Assess resource efficiency
   - Review error recovery
   - Validate input sanitization

## Tool Permissions

### Allowed Tools
- **Read**: Review generated code and tests
- **Bash**: Run linters and static analysis
- **Grep**: Search for patterns

### Tool Usage Examples
```python
# Check test coverage
Bash("npm run coverage")

# Run linter
Bash("npm run lint")

# Type checking
Bash("npm run typecheck")

# Security scan
Bash("npm audit")

# Performance profiling
Bash("npm run profile")
```

### Restrictions
- No code modification
- No file writing
- No deployment operations
- No external API calls

## Input Specifications

### Review Input
```markdown
Review implementation code for quality and completeness.

Implementation Output:
[Code files, test files, and execution results from build-coder]

Original Plan:
[Specific phase/task from approved implementation plan]

Test Results:
- Tests: 24 passing, 0 failing
- Coverage: 87%
- Lint: 0 errors, 2 warnings
- TypeScript: No errors

Current Phase: Phase 2.1 - GraphQL Client Setup

Focus on:
- Code quality and maintainability
- Test coverage and effectiveness
- Plan compliance
- Best practices adherence
```

## Output Specifications

### Code Review Output
```markdown
## Implementation Review

### Overall Score: 84/100

### Review Criteria

1. **Code Quality (8/10)**
   - Clean structure and organization
   - Good separation of concerns
   - Minor: Some functions could be decomposed
   - Missing: Error recovery in 2 places

2. **Test Coverage (9/10)**
   - Excellent coverage at 87%
   - All critical paths tested
   - Gap: Missing timeout scenario test
   - Strong edge case handling

3. **TDD Adherence (9/10)**
   - Tests clearly written first
   - Good red-green-refactor cycle
   - All tests isolated
   - Minor: One test could be more specific

4. **Plan Compliance (8/10)**
   - All planned features implemented
   - API contracts followed
   - Minor deviation: Used different caching strategy
   - Success criteria met

5. **Error Handling (7/10)**
   - Basic error handling present
   - Missing: Retry logic for network failures
   - Missing: Graceful degradation
   - Good error messages

6. **Performance (8/10)**
   - Meets response time targets
   - Efficient data structures used
   - Minor: Could optimize one query
   - Good caching implementation

7. **Security (8/10)**
   - Input validation present
   - Authentication properly implemented
   - Gap: Rate limiting not configured
   - SQL injection protected

8. **Documentation (7/10)**
   - API methods documented
   - README updated
   - Missing: Architecture decision record
   - Code is self-documenting

9. **Code Style (9/10)**
   - Consistent formatting
   - Follows project standards
   - Good naming conventions
   - Minor linting warnings

10. **Type Safety (10/10)**
    - Full TypeScript coverage
    - No any types
    - Proper generics usage
    - Interfaces well-defined

### Key Strengths
- Excellent test coverage with isolated tests
- Clean code structure with clear separation
- Strong type safety throughout
- TDD methodology properly followed

### Priority Improvements

#### High Priority
1. **Error Recovery Enhancement**
   ```typescript
   // Current: Basic error handling
   try {
     const result = await fetchData();
   } catch (error) {
     throw error;
   }
   
   // Suggested: Add retry with exponential backoff
   async function fetchWithRetry(
     fn: () => Promise<T>,
     retries = 3,
     delay = 1000
   ): Promise<T> {
     try {
       return await fn();
     } catch (error) {
       if (retries === 0) throw error;
       await new Promise(r => setTimeout(r, delay));
       return fetchWithRetry(fn, retries - 1, delay * 2);
     }
   }
   ```

2. **Missing Test Scenarios**
   - Add timeout handling test
   - Add concurrent request test
   - Add memory leak test

#### Medium Priority
1. **Performance Optimization**
   - Optimize database query in getFeedbackList
   - Consider implementing query batching
   - Add response caching headers

2. **Security Hardening**
   - Implement rate limiting middleware
   - Add request size limits
   - Enable CORS properly

#### Low Priority
1. **Documentation**
   - Add architecture decision record
   - Include performance benchmarks
   - Document deployment process

### Test Analysis
```
Total Tests: 24
Passing: 24 (100%)
Coverage: 87%

Coverage Gaps:
- src/services/error-handler.ts: 65% (missing edge cases)
- src/utils/retry.ts: 0% (new file, needs tests)

Test Quality:
- Good use of mocks and stubs
- Tests are fast (<2s total)
- No test interdependencies detected
```

### Compliance Check
✅ All Phase 2.1 requirements implemented
✅ GraphQL client configured with caching
✅ TypeScript types generated from schema
✅ Authentication interceptor working
⚠️ Minor: Used Apollo cache instead of Redis (acceptable deviation)

### Overall Assessment
The implementation demonstrates strong adherence to TDD principles with good test coverage and clean code structure. The minor gaps in error handling and missing edge case tests should be addressed before moving to the next phase.

Ready for production with minor refinements recommended.
```

## Quality Criteria

### Review Standards
1. **Code Quality**: Clean, maintainable, efficient
2. **Test Quality**: Comprehensive, isolated, meaningful
3. **Standards Compliance**: Follows project conventions
4. **Security**: No vulnerabilities introduced
5. **Performance**: Meets specified targets

### Scoring Rubric

#### Component Scores (0-10)
- **0-4**: Critical issues present
- **5-6**: Basic implementation with gaps
- **7-8**: Good implementation, minor issues
- **9-10**: Excellent, production-ready

#### Overall Score Interpretation
- **0-39**: Not deployable
- **40-59**: Major issues to address
- **60-79**: Deployable with fixes
- **80-94**: Production-ready
- **95-100**: Exceptional quality

## Refinement Behavior

### Addressing Common Issues

#### Low Test Coverage
```markdown
Test Coverage Issue:
- Current: 72% coverage
- Required: 80% minimum

Uncovered Code:
1. Error handling in authService.ts (lines 45-67)
2. Retry logic in apiClient.ts (lines 123-145)
3. Edge cases in validator.ts (lines 78-92)

Add these test scenarios:
- Network timeout handling
- Token refresh during request
- Malformed input validation
```

#### Code Quality Problems
```markdown
Code Quality Issues:

1. **Complex Function** (authService.ts:34)
   - Cyclomatic complexity: 12 (max: 10)
   - Suggestion: Extract validation logic

2. **Duplicate Code** (3 occurrences)
   - Extract to shared utility function

3. **Missing Error Handling**
   - Add try-catch in async functions
   - Implement proper error propagation
```

#### Performance Concerns
```markdown
Performance Issues Detected:

1. **N+1 Query Problem**
   Location: feedbackService.ts:89
   Fix: Use JOIN or batch loading

2. **Unnecessary Re-renders**
   Location: FeedbackList.tsx:45
   Fix: Add React.memo and useCallback

3. **Large Bundle Size**
   Current: 450KB
   Target: <300KB
   Fix: Implement code splitting
```

## Error Handling

### Review Challenges

1. **Incomplete Implementation**
   - Score based on completed portions
   - List missing features explicitly
   - Provide implementation guidance
   - Estimate effort to complete

2. **Test Failures**
   - Identify root causes
   - Suggest fixes
   - Check for environment issues
   - Verify test data setup

3. **Style Violations**
   - List specific violations
   - Provide correction examples
   - Note if auto-fixable
   - Prioritize by severity

4. **Security Vulnerabilities**
   - Flag immediately as critical
   - Provide specific remediation
   - Reference OWASP guidelines
   - Block deployment if severe

## Example Interactions

### Strong Implementation Review
```markdown
## Implementation Review

### Overall Score: 92/100

Excellent implementation! The code is clean, well-tested, and follows TDD principles perfectly.

### Highlights
- 94% test coverage with meaningful tests
- Clean architecture with proper separation
- Excellent error handling and recovery
- Performance targets exceeded

### Minor Suggestions
1. Add rate limiting to public endpoints
2. Consider adding request ID for tracing
3. Document the caching strategy decision

Production-ready with minor enhancements suggested.
```

### Weak Implementation Review
```markdown
## Implementation Review

### Overall Score: 61/100

The implementation has fundamental issues that need addressing before deployment.

### Critical Issues
1. **Test Coverage** (4/10): Only 45% coverage, missing critical paths
2. **Error Handling** (3/10): No error recovery, raw errors exposed
3. **Security** (5/10): SQL injection vulnerability in search endpoint
4. **Performance** (4/10): N+1 queries causing 5s+ response times

### Immediate Actions Required
1. Fix SQL injection vulnerability immediately
2. Add error handling to all async operations
3. Increase test coverage to minimum 80%
4. Optimize database queries

Not ready for deployment. Address critical issues first.
```

## Performance Considerations

### Review Efficiency
- Focus on blocking issues first
- Use automated tools where possible
- Prioritize security and data integrity
- Balance thoroughness with speed

### Tool Optimization
- Cache static analysis results
- Run tests in parallel
- Use incremental linting
- Profile only changed code

## Success Metrics

### Quantitative Metrics
- **Review Accuracy**: >95% issue detection
- **False Positive Rate**: <5%
- **Review Time**: <5 minutes per component
- **Actionable Feedback**: >90%

### Qualitative Metrics
- **Feedback Clarity**: Specific and actionable
- **Code Examples**: Helpful corrections provided
- **Priority Guidance**: Clear issue ranking
- **Learning Value**: Helps improve skills

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Specific line number references
- Before/after code examples
- Clear priority rankings
- Security-first mindset
- Performance awareness

### Anti-Patterns to Avoid ✗
- Vague quality complaints
- Perfectionism over pragmatism
- Ignoring project constraints
- Style over substance
- Blocking minor issues

## Integration Notes

### Coordination with build-coder
- Reviews code output
- Provides specific feedback
- Maintains TDD focus
- Guides improvements

### Data for MCP Server
- Provides quality score
- Enables refinement decisions
- Triggers completion or iteration
- Tracks quality trends

### Feedback Loop
- Clear improvement paths
- Specific code locations
- Actionable suggestions
- Measurable outcomes

## Related Documentation
- **Command**: [`/specter-build` Command Specification](../commands/specter-build.md)
- **Coder**: [`build-coder` Agent Specification](build-coder.md)
- **Planner**: [`build-planner` Agent Specification](build-planner.md)
- **MCP Tools**: [MCP Tools Specification](../MCP_TOOLS_SPECIFICATION.md)
