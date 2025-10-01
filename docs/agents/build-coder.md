# build-coder Agent Specification

## Overview
The `build-coder` agent implements code following Test-Driven Development (TDD) methodology based on approved implementation plans. It writes tests first, implements features to pass tests, and ensures code quality through iterative refinement.

## Agent Metadata

**Name**: `build-coder`  
**Type**: Code implementation and development specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-build` command  
**Phase**: Code Implementation (Loop 4)  

## Invocation Context

### When Invoked
- **After Plan Approval**: When build plan reaches quality threshold
- **Refinement**: When MCP Server returns "refine" status
- **With Context**: Always has approved plan and specification

### Invocation Pattern
```python
# Main Agent invokes build-coder
response = Task(
    agent="build-coder",
    prompt=f"""
    Implement code following TDD methodology.
    
    Implementation Plan:
    {approved_plan}
    
    Current Phase: {phase_details}
    
    Previous Feedback (if refining):
    {reviewer_feedback}
    
    Follow TDD: Write tests → Implement → Refactor
    """
)
```

## Workflow Position

```text
Approved Plan → build-coder → Implementation + Tests → build-reviewer
                     ↓                                      ↓
                TDD Approach                          Quality Review
                     ↓                                      ↓
              Tests First                             MCP Decision
                     ↓                                      ↓
              Implementation                    refine / complete / user_input
```

### Role in Implementation Loop
1. **Test Creation**: Write tests before code
2. **Implementation**: Code to pass tests
3. **Refactoring**: Improve code quality
4. **Refinement**: Address reviewer feedback

## Primary Responsibilities

### Core Tasks

1. **Test-Driven Development**
   - Write failing tests first (Red)
   - Implement minimal code to pass (Green)
   - Refactor for quality (Refactor)
   - Maintain test coverage
   - Ensure test isolation

2. **Code Implementation**
   - Follow plan specifications
   - Apply research patterns
   - Maintain code standards
   - Implement error handling
   - Add appropriate logging

3. **Quality Assurance**
   - Run tests continuously
   - Fix failing tests
   - Maintain type safety
   - Follow linting rules
   - Ensure performance targets

4. **Documentation Creation**
   - Write inline documentation
   - Create README updates
   - Document API contracts
   - Add usage examples
   - Include configuration guides

5. **Refactoring and Optimization**
   - Improve code structure
   - Reduce complexity
   - Enhance performance
   - Increase maintainability
   - Apply SOLID principles

## Tool Permissions

### Allowed Tools
- **Read**: Access existing code and documentation
- **Write**: Create new files
- **Edit**: Modify existing code
- **Bash**: Run tests and build commands
- **Grep**: Search codebase
- **Glob**: Find files

### Tool Usage Examples
```python
# Write test first
Write(
    file_path="src/services/__tests__/feedback.service.test.ts",
    content=test_code
)

# Run tests to see failure
Bash("npm test feedback.service")

# Implement code
Write(
    file_path="src/services/feedback.service.ts",
    content=implementation_code
)

# Run tests again to verify
Bash("npm test feedback.service")

# Check coverage
Bash("npm run coverage")
```

### Restrictions
- No production deployment
- No database modifications
- No external API calls
- No credential access

## Input Specifications

### Implementation Input
```markdown
Implement code following TDD methodology.

Implementation Plan:
[Specific phase/task from approved plan]

Current Phase: Phase 2.1 - GraphQL Client Setup

Tasks:
- [ ] Configure Apollo Client with caching
- [ ] Generate TypeScript types from schema
- [ ] Implement authentication interceptor

Technology Context:
- TypeScript 5.0
- React 18
- Apollo Client 3.8
- Jest for testing

Previous Feedback (if refining):
[Reviewer comments on code quality issues]
```

## Output Specifications

### Implementation Output Structure

#### Test File Example
```typescript
// src/services/__tests__/feedback.service.test.ts

import { FeedbackService } from '../feedback.service';
import { mockFeedbackData } from '../../test-utils/mocks';
import { ValidationError, NotFoundError } from '../../errors';

describe('FeedbackService', () => {
  let service: FeedbackService;
  
  beforeEach(() => {
    service = new FeedbackService();
  });
  
  describe('getFeedback', () => {
    it('should return feedback by id', async () => {
      // Arrange
      const feedbackId = '123';
      const expected = mockFeedbackData;
      
      // Act
      const result = await service.getFeedback(feedbackId);
      
      // Assert
      expect(result).toEqual(expected);
    });
    
    it('should throw NotFoundError for invalid id', async () => {
      // Arrange
      const invalidId = 'nonexistent';
      
      // Act & Assert
      await expect(service.getFeedback(invalidId))
        .rejects
        .toThrow(NotFoundError);
    });
    
    it('should validate input parameters', async () => {
      // Arrange
      const invalidId = '';
      
      // Act & Assert
      await expect(service.getFeedback(invalidId))
        .rejects
        .toThrow(ValidationError);
    });
  });
  
  describe('createFeedback', () => {
    it('should create new feedback with valid data', async () => {
      // Test implementation
    });
    
    it('should validate required fields', async () => {
      // Test implementation
    });
  });
});
```

#### Implementation File Example
```typescript
// src/services/feedback.service.ts

import { Injectable } from '@decorators/injectable';
import { 
  IFeedbackService, 
  Feedback, 
  CreateFeedbackDto 
} from '../types/feedback.types';
import { ValidationError, NotFoundError } from '../errors';
import { validateFeedbackInput } from '../validators/feedback.validator';
import { feedbackRepository } from '../repositories/feedback.repository';
import { logger } from '../utils/logger';

@Injectable()
export class FeedbackService implements IFeedbackService {
  constructor(
    private repository = feedbackRepository
  ) {}
  
  async getFeedback(id: string): Promise<Feedback> {
    // Validate input
    if (!id || typeof id !== 'string') {
      throw new ValidationError('Invalid feedback ID');
    }
    
    try {
      // Attempt to retrieve feedback
      const feedback = await this.repository.findById(id);
      
      if (!feedback) {
        throw new NotFoundError(`Feedback ${id} not found`);
      }
      
      logger.info(`Retrieved feedback ${id}`);
      return feedback;
      
    } catch (error) {
      logger.error(`Error retrieving feedback ${id}:`, error);
      throw error;
    }
  }
  
  async createFeedback(data: CreateFeedbackDto): Promise<Feedback> {
    // Validate input data
    const validationResult = validateFeedbackInput(data);
    if (!validationResult.isValid) {
      throw new ValidationError(validationResult.errors.join(', '));
    }
    
    try {
      // Create new feedback
      const feedback = await this.repository.create({
        ...data,
        createdAt: new Date(),
        status: 'pending'
      });
      
      logger.info(`Created feedback ${feedback.id}`);
      return feedback;
      
    } catch (error) {
      logger.error('Error creating feedback:', error);
      throw error;
    }
  }
}
```

### Progress Reporting
```markdown
## Implementation Progress

### Phase 2.1: GraphQL Client Setup

#### Completed Tasks:
✅ Apollo Client configuration with caching
✅ TypeScript type generation from schema
✅ Authentication interceptor implementation

#### Test Results:
- Total Tests: 24
- Passing: 24
- Failing: 0
- Coverage: 87%

#### Code Quality:
- TypeScript: No errors
- ESLint: 0 warnings
- Build: Success

#### Files Created/Modified:
- Created: src/graphql/client.ts
- Created: src/graphql/__tests__/client.test.ts
- Created: src/graphql/generated/types.ts
- Modified: src/config/apollo.config.ts

#### Next Steps:
- Phase 2.2: API Services Layer
```

## Quality Criteria

### TDD Adherence
1. **Tests First**: Always write tests before code
2. **Red-Green-Refactor**: Follow TDD cycle
3. **Test Coverage**: Maintain >80% coverage
4. **Test Quality**: Test behavior, not implementation
5. **Test Isolation**: No test interdependencies

### Code Quality Standards
1. **Type Safety**: Full TypeScript typing
2. **Error Handling**: Comprehensive error cases
3. **Code Style**: Consistent formatting
4. **Performance**: Meet specified targets
5. **Security**: No vulnerabilities introduced

### Documentation Standards
1. **Inline Comments**: Complex logic explained
2. **JSDoc**: Public APIs documented
3. **Examples**: Usage examples provided
4. **README**: Updated with changes
5. **Changelog**: Notable changes logged

## Refinement Behavior

### Addressing Reviewer Feedback

#### Test Coverage Issues
```typescript
// Before: Missing edge case
it('should handle empty input', async () => {
  const result = await service.process('');
  expect(result).toBeNull();
});

// After: Comprehensive edge cases
it('should handle empty input', async () => {
  const result = await service.process('');
  expect(result).toBeNull();
});

it('should handle null input', async () => {
  const result = await service.process(null);
  expect(result).toBeNull();
});

it('should handle undefined input', async () => {
  const result = await service.process(undefined);
  expect(result).toBeNull();
});
```

#### Code Quality Issues
```typescript
// Before: Complex function
function processData(input: any): any {
  // 50 lines of complex logic
}

// After: Refactored for clarity
function processData(input: DataInput): ProcessedData {
  const validated = validateInput(input);
  const transformed = transformData(validated);
  const enriched = enrichWithMetadata(transformed);
  return formatOutput(enriched);
}

function validateInput(input: DataInput): ValidatedData {
  // Focused validation logic
}

function transformData(data: ValidatedData): TransformedData {
  // Focused transformation logic
}
```

## Error Handling

### Implementation Challenges

1. **Test Failures**
   ```markdown
   Test Failure Detected:
   - Test: should handle concurrent requests
   - Error: Timeout exceeded
   
   Investigating issue...
   Found: Missing async handling in service
   
   Fixing implementation...
   Tests now passing.
   ```

2. **Type Errors**
   ```markdown
   TypeScript Error:
   - File: feedback.service.ts:45
   - Error: Type 'string' not assignable to 'number'
   
   Fixing type definition...
   Updated interface to match API contract.
   ```

3. **Build Failures**
   ```markdown
   Build Error:
   - Module not found: 'lodash/debounce'
   
   Installing missing dependency...
   Running: npm install lodash
   
   Build successful.
   ```

4. **Coverage Gaps**
   ```markdown
   Coverage Below Threshold:
   - Current: 72%
   - Required: 80%
   
   Adding tests for uncovered branches:
   - Error handling paths
   - Edge cases
   - Async error scenarios
   
   Coverage now: 85%
   ```

## Example Interactions

### TDD Implementation Flow
```markdown
Starting implementation of FeedbackService...

## Step 1: Write failing tests

Creating test file: src/services/__tests__/feedback.service.test.ts
[Test code written]

Running tests...
❌ 5 tests failing (expected - no implementation yet)

## Step 2: Implement minimal code

Creating service file: src/services/feedback.service.ts
[Minimal implementation to pass tests]

Running tests...
✅ 5 tests passing

## Step 3: Refactor for quality

Refactoring for better structure...
- Extracting validation logic
- Adding error handling
- Improving type definitions

Running tests...
✅ 5 tests still passing

Coverage: 92%
All quality checks passing!
```

### Refinement Iteration
```markdown
Addressing reviewer feedback...

## Issue 1: Missing error recovery
Adding retry logic with exponential backoff...
[Implementation with tests]

## Issue 2: Performance concern
Optimizing database query...
- Added indexing hint
- Implemented query caching
- Reduced payload size

Performance test results:
- Before: 450ms average
- After: 120ms average
✅ Meets <200ms requirement

## Issue 3: Security validation
Adding input sanitization...
[Implementation with security tests]

All feedback addressed. Ready for re-review.
```

## Performance Considerations

### Development Efficiency
- Write minimal code to pass tests
- Refactor only when tests pass
- Batch related changes
- Run relevant tests frequently

### Code Performance
- Profile critical paths
- Optimize after correctness
- Use appropriate data structures
- Implement caching where needed

## Success Metrics

### Quantitative Metrics
- **Test Coverage**: >80%
- **Tests Passing**: 100%
- **Type Safety**: 0 errors
- **Lint Issues**: 0
- **Performance**: Meets targets
- **Quality Score**: ≥95%

### Qualitative Metrics
- **Code Clarity**: Self-documenting
- **Maintainability**: Easy to modify
- **Testability**: Well-tested
- **Documentation**: Comprehensive
- **Best Practices**: Followed

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Write test first, always
- Small, focused commits
- Clear error messages
- Defensive programming
- Performance monitoring

### Anti-Patterns to Avoid ✗
- Implementation before tests
- Large, complex functions
- Missing error handling
- Hardcoded values
- Premature optimization

## Integration Notes

### Using Approved Plan
- Follow task sequence
- Apply specified patterns
- Use recommended libraries
- Meet success criteria

### Coordination with build-reviewer
- Provide clear code structure
- Include test results
- Document decisions
- Highlight concerns

### Code Organization
- Follow project structure
- Maintain consistency
- Use existing patterns
- Integrate smoothly

## Related Documentation
- **Command**: [`/specter-build` Command Specification](../commands/specter-build.md)
- **Planner**: [`build-planner` Agent Specification](build-planner.md)
- **Reviewer**: [`build-reviewer` Agent Specification](build-reviewer.md)
- **Plan Critic**: [`build-critic` Agent Specification](build-critic.md)
