# build-planner Agent Specification

## Overview
The `build-planner` agent creates detailed implementation plans from technical specifications and research documentation. It analyzes the current codebase, integrates research findings, and produces actionable development roadmaps.

## Agent Metadata

**Name**: `build-planner`  
**Type**: Implementation planning specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-build` command  
**Phase**: Implementation Planning (Loop 3)  

## Invocation Context

### When Invoked
- **Initial Planning**: After research synthesis completes
- **Refinement**: When MCP Server returns "refine" status
- **With Research**: Always receives documentation paths

### Invocation Pattern
```python
# Main Agent invokes build-planner with research paths
response = Task(
    agent="build-planner",
    prompt=f"""
    Create implementation plan from specification and research.
    
    Technical Specification:
    {specification}
    
    Technology Stack Detected:
    {environment_info}
    
    Research Documentation Paths:
    {documentation_paths}  # List of file paths to read
    
    Previous Feedback (if refining):
    {critic_feedback}
    
    Create detailed, actionable implementation plan.
    """
)
```

## Workflow Position

```text
Research Synthesis → Documentation Paths → build-planner → Implementation Plan
                                                ↓
                                          build-critic
                                                ↓
                                          MCP Decision
                                                ↓
                                    refine / complete / user_input
```

### Role in Build Phase
1. **Research Integration**: Read and apply research findings
2. **Plan Creation**: Develop step-by-step implementation
3. **Task Breakdown**: Create actionable work items
4. **Refinement**: Improve based on critic feedback

## Primary Responsibilities

### Core Tasks

1. **Codebase Analysis**
   - Understand existing project structure
   - Identify integration points
   - Recognize existing patterns
   - Find reusable components
   - Map dependencies

2. **Research Documentation Consumption**
   - Read all provided documentation paths
   - Extract implementation patterns
   - Apply best practices
   - Integrate recommendations
   - Avoid anti-patterns

3. **Implementation Roadmap Creation**
   - Break down into phases
   - Define specific tasks
   - Estimate complexity
   - Sequence dependencies
   - Set milestones

4. **Test Strategy Development**
   - Define test approaches
   - Specify test scenarios
   - Plan test data
   - Include performance tests
   - Coverage targets

5. **Risk Mitigation Planning**
   - Identify implementation risks
   - Plan fallback approaches
   - Define validation checkpoints
   - Include rollback strategies

## Tool Permissions

### Allowed Tools
- **Read**: Access research documentation and codebase
- **Grep**: Search for patterns in code
- **Glob**: Find relevant files
- **Bash**: Run analysis scripts (read-only)

### Tool Usage Examples
```python
# Read research documentation
for path in documentation_paths:
    Read(file_path=path)

# Analyze codebase structure
Glob(pattern="**/*.{js,ts,py}")
Grep(pattern="class.*Controller", path="src/")

# Check testing setup
Bash("npm test --listTests")
```

### Restrictions
- No file modifications
- No code execution beyond analysis
- No external network calls
- No platform-specific tools

## Input Specifications

### Planning Input
```markdown
Create implementation plan from specification and research.

Technical Specification:
[Complete specification with Research Requirements section]

Technology Stack Detected:
- Language: TypeScript
- Framework: React 18
- Testing: Jest, React Testing Library
- Build: Vite
- State: Redux Toolkit

Research Documentation Paths:
- ~/.claude/research/2025-01-15-react-patterns.md
- ~/.claude/research/2025-01-15-graphql-integration.md
- ~/.claude/best-practices/testing-strategies.md

Previous Feedback (if refining):
[Critic feedback on plan improvements needed]
```

## Output Specifications

### Implementation Plan Structure
```markdown
# Implementation Plan: [Project Name]

## Overview
[Brief summary of implementation approach based on research findings]

## Technology Decisions
Based on research and current stack:
- **State Management**: Redux Toolkit with RTK Query (per research recommendation)
- **API Layer**: GraphQL with Apollo Client
- **Testing**: Jest + RTL with MSW for mocking
- **Component Pattern**: Composition with hooks

## Phase 1: Foundation (Days 1-3)

### 1.1 Project Setup and Configuration
**Priority**: Critical
**Complexity**: Low
**Dependencies**: None

#### Tasks:
- [ ] Initialize TypeScript configuration with strict mode
- [ ] Configure ESLint with recommended rules
- [ ] Setup Jest with React Testing Library
- [ ] Configure MSW for API mocking
- [ ] Setup pre-commit hooks with Husky

#### Test Approach:
- Verify build pipeline works
- Confirm linting rules apply
- Test that test suite runs

#### Success Criteria:
- Clean build with no warnings
- All tools properly configured
- CI/CD pipeline ready

### 1.2 Core Data Models
**Priority**: Critical
**Complexity**: Medium
**Dependencies**: 1.1

#### Tasks:
- [ ] Define TypeScript interfaces for all entities
- [ ] Create validation schemas with Zod
- [ ] Setup Redux store structure
- [ ] Implement data normalization utilities

#### Code Location:
```
src/
  types/
    feedback.types.ts
    analysis.types.ts
  store/
    store.ts
    slices/
      feedbackSlice.ts
```

#### Test Approach:
- Unit tests for validation schemas
- Type checking for interfaces
- Store initialization tests

## Phase 2: API Integration (Days 4-6)

### 2.1 GraphQL Client Setup
**Priority**: Critical
**Complexity**: High
**Dependencies**: Phase 1

#### Tasks:
- [ ] Configure Apollo Client with caching
- [ ] Generate TypeScript types from schema
- [ ] Implement authentication interceptor
- [ ] Setup error handling middleware
- [ ] Create query/mutation hooks

#### Implementation Pattern (from research):
```typescript
// Following research recommendations for 2025 patterns
const client = new ApolloClient({
  uri: process.env.GRAPHQL_ENDPOINT,
  cache: new InMemoryCache({
    typePolicies: {
      Feedback: {
        keyFields: ["id"],
        fields: {
          analysis: {
            merge: true
          }
        }
      }
    }
  })
});
```

#### Test Approach
- Mock GraphQL responses with MSW
- Test cache behavior
- Verify error handling
- Test authentication flow

### 2.2 API Services Layer
**Priority**: High
**Complexity**: Medium
**Dependencies**: 2.1

#### Tasks
- [ ] Create feedback service with CRUD operations
- [ ] Implement analysis service
- [ ] Add real-time subscription support
- [ ] Create batch operation utilities

## Phase 3: Core Features (Days 7-12)

### 3.1 Feedback List Component
**Priority**: Critical
**Complexity**: Medium
**Dependencies**: Phase 2

#### Tasks
- [ ] Create FeedbackList component with virtualization
- [ ] Implement filtering and sorting
- [ ] Add pagination with cursor-based approach
- [ ] Create loading and error states
- [ ] Implement optimistic updates

#### Component Structure
```typescript
// Based on research best practices
const FeedbackList: React.FC = () => {
  const { data, loading, error, fetchMore } = useFeedbackQuery({
    variables: { first: 20 }
  });
  
  // Virtualization for performance
  // Intersection Observer for infinite scroll
  // Error boundary for resilience
};
```

### 3.2 AI Analysis Integration
**Priority**: High
**Complexity**: High
**Dependencies**: 3.1

#### Tasks
- [ ] Create analysis trigger mechanism
- [ ] Implement progress tracking
- [ ] Add result visualization
- [ ] Create confidence score display
- [ ] Implement manual override capability

## Phase 4: Testing & Optimization (Days 13-15)

### 4.1 Comprehensive Testing
**Priority**: Critical
**Complexity**: Medium
**Dependencies**: All features

#### Test Coverage Plan
- Unit Tests: 85% coverage minimum
  - All utilities and helpers
  - Redux reducers and selectors
  - Custom hooks
  
- Integration Tests:
  - API communication flows
  - Component interactions
  - State management flows
  
- E2E Tests:
  - Critical user journeys
  - Error scenarios
  - Performance benchmarks

### 4.2 Performance Optimization
**Priority**: High
**Complexity**: Medium
**Dependencies**: 4.1

#### Optimization Tasks
- [ ] Implement code splitting
- [ ] Add React.memo where beneficial
- [ ] Optimize re-renders with useMemo/useCallback
- [ ] Implement virtual scrolling
- [ ] Add service worker for caching

## Risk Mitigation

### Technical Risks
1. **GraphQL Complexity**
   - Mitigation: Start with REST fallback
   - Use code generation for types
   - Implement gradual migration

2. **Performance at Scale**
   - Mitigation: Implement pagination early
   - Use virtualization from start
   - Add performance monitoring

3. **State Management Complexity**
   - Mitigation: Keep state normalized
   - Use RTK Query for cache
   - Document state shape clearly

## Implementation Notes

### Code Style Guidelines
- Follow Airbnb React style guide
- Use functional components exclusively
- Implement custom hooks for logic reuse
- Keep components under 200 lines
- Separate concerns clearly

### Testing Guidelines
- Write tests alongside implementation
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test user behavior, not implementation
- Maintain test isolation

### Documentation Requirements
- JSDoc for public APIs
- README for each major module
- Inline comments for complex logic
- Storybook for component library
- Architecture decision records

## Success Metrics
- All tests passing (100%)
- Performance benchmarks met (<200ms API, <2s load)
- Code coverage >85%
- No critical security issues
- Accessibility score >95%

## Dependencies and Blockers
- Requires API endpoints ready
- Needs design system finalized
- Authentication service must be available
- Test data needs to be prepared
```

## Quality Criteria

### Plan Completeness
1. **Phases Defined**: Clear progression
2. **Tasks Specific**: Actionable items
3. **Dependencies Mapped**: Clear sequence
4. **Tests Planned**: Coverage strategy
5. **Risks Addressed**: Mitigation included

### Research Integration
1. **Patterns Applied**: From documentation
2. **Best Practices**: Incorporated
3. **Anti-patterns**: Avoided
4. **Tools Utilized**: Recommended libraries
5. **Examples Used**: Code samples included

### Implementation Readiness
1. **Sufficient Detail**: Developer-ready
2. **Clear Structure**: File organization
3. **Test Strategy**: Comprehensive
4. **Success Criteria**: Measurable
5. **Timeline Realistic**: Achievable goals

## Refinement Behavior

### Addressing Critic Feedback

#### Low Task Specificity
- Break down into smaller tasks
- Add concrete acceptance criteria
- Include code examples
- Specify file locations

#### Missing Test Coverage
- Add test scenarios
- Specify test data needs
- Include performance tests
- Add security tests

#### Unclear Dependencies
- Create dependency graph
- Specify integration points
- Add validation steps
- Include rollback plans

## Error Handling

### Planning Challenges

1. **Research Access Issues**
   ```markdown
   Note: Could not access research document [path].
   Proceeding with specification details only.
   Recommendations may be less optimal.
   ```

2. **Codebase Complexity**
   ```markdown
   Warning: Existing codebase has high complexity.
   Plan includes refactoring tasks:
   - Decouple [component]
   - Extract [service]
   ```

3. **Conflicting Patterns**
   ```markdown
   Note: Research recommends Pattern A, but codebase uses Pattern B.
   Plan includes migration strategy:
   - Phase 1: Wrapper approach
   - Phase 2: Gradual migration
   ```

4. **Missing Information**
   ```markdown
   Gap Identified: [Missing detail]
   Assumption made: [Assumption]
   Risk: [Potential issue]
   Mitigation: [Approach]
   ```

## Example Interactions

### Initial Planning
```markdown
Analyzing specification and research documentation...

Read: ~/.claude/research/2025-01-15-react-patterns.md
Key findings:
- Server Components recommended for initial load
- Suspense boundaries for progressive enhancement
- Error boundaries at feature level

Read: ~/.claude/best-practices/testing-strategies.md
Applying:
- Test user behavior, not implementation
- MSW for API mocking
- Component testing over unit testing

Creating implementation plan with 4 phases...
[Full plan follows]
```

### Refinement Iteration
```markdown
Incorporating feedback to improve plan...

Addressing "insufficient test detail":
- Adding specific test scenarios for each component
- Including performance test benchmarks
- Adding security test cases

Addressing "missing error handling":
- Adding error boundary implementation tasks
- Including retry logic for API calls
- Adding user feedback for failures

Updated plan with enhanced detail...
[Refined plan follows]
```

## Performance Considerations

### Research Processing
- Read documents efficiently
- Extract key patterns quickly
- Focus on applicable sections
- Cache processed insights

### Plan Generation
- Structure logically
- Avoid redundancy
- Keep concise but complete
- Prioritize critical path

## Success Metrics

### Quantitative Metrics
- **Quality Score**: Target ≥80%
- **Task Specificity**: >90% actionable
- **Research Utilization**: >80% of docs referenced
- **Iteration Efficiency**: ≤3 to pass

### Qualitative Metrics
- **Developer Ready**: Can start immediately
- **Risk Aware**: Major risks identified
- **Test Complete**: Full coverage planned
- **Research Based**: Best practices applied

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Phase-based progression
- Clear task dependencies
- Specific code examples
- Test-first approach
- Research-driven decisions

### Anti-Patterns to Avoid ✗
- Vague task descriptions
- Missing dependencies
- Ignoring existing code
- Over-engineering
- Skipping test planning

## Integration Notes

### Research Consumption
- Reads all provided paths
- Extracts applicable patterns
- Integrates recommendations
- Notes source of decisions

### Coordination with build-critic
- Receives improvement feedback
- Refines weak areas
- Maintains plan structure
- Improves specificity

### Output for build-coder
- Provides clear roadmap
- Enables systematic implementation
- Defines success criteria
- Guides development sequence

## Related Documentation
- **Command**: [`/specter-build` Command Specification](../commands/specter-build.md)
- **Critic**: [`build-critic` Agent Specification](build-critic.md)
- **Implementation**: [`build-coder` Agent Specification](build-coder.md)
- **Research**: Research documentation (external)
