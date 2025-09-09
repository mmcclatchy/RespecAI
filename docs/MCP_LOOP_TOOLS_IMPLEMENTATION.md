# MCP Loop Tools Implementation Plan

Comprehensive step-by-step implementation plan for MCP Loop Tools using Test-Driven Development methodology.

## Implementation Overview

### Architecture Summary
- **Session-scoped state management** - No cross-session persistence
- **Simple stagnation detection** - 2 consecutive iterations below improvement threshold
- **Per-loop configuration** - Individual thresholds via Pydantic Settings
- **Main Agent feedback handling** - MCP Server focused on decision logic only
- **Sequential loop coordination** - Ordered progression through phases
- **Graceful error handling** - Simple but robust error management

### TDD Implementation Phases

Each implementation step follows strict Red → Green → Refactor methodology:

- **Red Phase**: Write failing tests first, verify they fail for correct reasons
- **Green Phase**: Write minimal code to make tests pass, focus on functionality over elegance
- **Refactor Phase**: Improve code quality while maintaining passing tests with full compliance

## Phase 1: Core Models and Configuration

### Step 1.1: Loop Configuration Models

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/models/test_loop_config.py
- Test LoopThresholds model validation with various loop types
- Test invalid threshold values (negative, zero, excessive)
- Test environment variable loading and defaults
- Test per-loop threshold access methods
- Verify tests fail with "ModuleNotFoundError" or similar
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/models/loop_config.py
- Implement LoopThresholds Pydantic model with required fields
- Add validation methods for threshold ranges
- Implement environment variable binding
- Add per-loop threshold accessor methods
- Run tests until all pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues  
- ✅ Run pytest - all tests pass, no warnings
- ✅ Review code for self-documenting variable names
- ✅ Remove unnecessary comments or docstrings
- ✅ Verify max 3 levels of nesting
- ✅ Confirm all imports at file top
- ✅ Validate Pydantic v2 usage patterns
```

### Step 1.2: Loop Data Models

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/models/test_loop_data.py
- Test LoopData model creation and validation
- Test score improvement calculations
- Test iteration tracking and limits
- Test invalid score ranges (outside 0-100)
- Test missing required fields
- Verify tests fail appropriately
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/models/loop_data.py
- Implement LoopData Pydantic model
- Add score validation (0-100 range)
- Implement improvement calculation methods
- Add iteration tracking functionality
- Ensure all tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Ensure clear, self-documenting method names
- ✅ Remove obvious comments and docstrings
- ✅ Validate typing completeness (`str | None` syntax)
- ✅ Check import organization
```

## Phase 2: Decision Logic Engine

### Step 2.1: Stagnation Detection

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/services/test_stagnation_detector.py
- Test improvement threshold detection
- Test consecutive low improvement tracking
- Test stagnation flag with various score patterns
- Test edge cases (first iteration, identical scores)
- Test boundary conditions (exactly at threshold)
- Verify tests fail before implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/stagnation_detector.py
- Implement detect_stagnation function
- Add improvement calculation logic
- Implement consecutive tracking mechanism
- Handle edge cases appropriately
- Ensure all tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Analyze if tests are correct vs implementation issues
- ✅ Fix implementation bugs rather than changing tests
- ✅ Ensure algorithmic clarity through naming
- ✅ Remove algorithm comments if logic is self-evident
```

### Step 2.2: Decision Engine Core

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/services/test_decision_engine.py
- Test "complete" decisions (score >= threshold)
- Test "refine" decisions (improving scores)
- Test "user-input" decisions (stagnation detected)
- Test max iteration limits
- Test all decision path combinations
- Verify each test fails before implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/decision_engine.py
- Implement decide_next_action function
- Add threshold comparison logic
- Integrate stagnation detection
- Implement max iteration checking
- Ensure complete decision path coverage
- Run tests until all pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Review decision logic for clarity and correctness
- ✅ Ensure function names clearly indicate purpose
- ✅ Remove conditional logic comments if self-evident
- ✅ Validate error handling approaches
- ✅ Check typing completeness for all parameters
```

## Phase 3: MCP Tool Implementation

### Step 3.1: MCP Tool Interface

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/mcp/test_loop_tools.py
- Test decide_loop_next_action MCP tool function
- Test parameter validation and type checking
- Test integration with configuration loading
- Test integration with decision engine
- Test error handling for invalid inputs
- Test return value format validation
- Verify tests fail without MCP implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/mcp/loop_tools.py
- Implement decide_loop_next_action MCP tool
- Add parameter validation and type conversion
- Integrate configuration loading
- Connect decision engine logic
- Implement error handling and logging
- Add MCP tool registration
- Ensure all tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Add docstring for MCP tool (public API interface)
- ✅ Ensure parameter names are self-documenting
- ✅ Remove implementation detail comments
- ✅ Validate async/await usage if applicable
- ✅ Check error message clarity for external agents
- ✅ Verify service layer separation from MCP interface
```

### Step 3.2: Error Handling and Validation

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/services/test_error_handling.py
- Test invalid score handling (outside 0-100)
- Test missing parameter scenarios
- Test invalid loop type values
- Test configuration loading failures
- Test graceful degradation scenarios
- Verify error conditions trigger expected behaviors
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/error_handling.py
- Implement score validation and clamping
- Add parameter existence checking
- Implement configuration fallback mechanisms
- Add logging for error conditions
- Ensure graceful failure modes
- Make all tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Evaluate if error handling is too complex (simplify)
- ✅ Ensure error messages are clear for debugging
- ✅ Remove obvious error handling comments
- ✅ Validate exception types and handling patterns
```

## Phase 4: Integration Testing

### Step 4.1: End-to-End MCP Tool Testing

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/integration/test_loop_tools_integration.py
- Test complete MCP tool workflow end-to-end
- Test realistic score progression scenarios
- Test stagnation detection in full context
- Test configuration loading from environment
- Test error recovery scenarios
- Mock external dependencies appropriately
- Verify integration test failures before full implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Ensure all components integrate properly
- Fix integration issues discovered in testing
- Adjust configuration loading if needed
- Resolve any component interaction problems
- Complete MCP tool registration
- Ensure all integration tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run full test suite - all tests pass, no warnings
- ✅ Run mypy on entire codebase - zero errors
- ✅ Run ruff on entire codebase - zero issues
- ✅ Review integration test quality and coverage
- ✅ Ensure test names clearly indicate scenarios
- ✅ Remove unnecessary test implementation comments
- ✅ Validate mock usage follows pytest-mock patterns
- ✅ Check for proper test isolation
```

### Step 4.2: Performance and Load Testing

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/integration/test_loop_performance.py
- Test decision engine performance with large iteration counts
- Test configuration loading performance
- Test memory usage patterns during long loops
- Test concurrent access scenarios if applicable
- Verify performance tests fail before optimizations
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Identify and fix performance bottlenecks
- Optimize configuration loading if needed
- Ensure memory usage remains reasonable
- Add performance logging if necessary
- Make performance tests pass within acceptable limits
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run full test suite - all tests pass, no warnings
- ✅ Run mypy - zero errors across codebase
- ✅ Run ruff - zero linting issues across codebase
- ✅ Review performance optimizations for clarity
- ✅ Ensure optimizations don't sacrifice readability
- ✅ Remove performance measurement comments
- ✅ Validate typing remains complete after optimizations
```

## Phase 5: Documentation and Deployment

### Step 5.1: MCP Tool Documentation

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/test_mcp_tool_documentation.py
- Test MCP tool registration and discovery
- Test tool parameter documentation accuracy
- Test example usage scenarios work correctly
- Test error message documentation matches implementation
- Verify documentation tests fail before docs exist
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Add comprehensive docstring to MCP tool function
- Document parameter types and expected ranges
- Add usage examples in docstring
- Document error conditions and responses
- Ensure MCP tool registration includes proper metadata
- Make documentation tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - verify docstring types match implementation
- ✅ Run ruff - ensure docstring formatting compliance
- ✅ Run pytest - all tests pass including documentation tests
- ✅ Review docstring for clarity and completeness
- ✅ Ensure examples in docstring are accurate
- ✅ Verify parameter documentation matches function signature
- ✅ Check that complex algorithm explanation is justified
```

### Step 5.2: System Integration Validation

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/e2e/test_system_integration.py
- Test complete loop scenarios with mock Main Agent calls
- Test configuration loading from actual environment
- Test all decision paths in realistic scenarios
- Test error handling in full system context
- Verify system tests fail before full integration
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Complete MCP server integration
- Ensure environment variable configuration works
- Test with realistic Main Agent interaction patterns
- Fix any remaining system-level issues
- Validate all system components work together
- Make all system tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run complete test suite - 100% pass rate, zero warnings
- ✅ Run mypy on entire project - zero errors
- ✅ Run ruff on entire project - zero linting issues
- ✅ Final code review for standards compliance
- ✅ Verify all function and variable names are self-documenting
- ✅ Confirm no unnecessary comments or docstrings remain
- ✅ Validate service layer separation is maintained
- ✅ Check that complex logic has appropriate documentation only
```

## Quality Assurance Checklist

### Code Standards Compliance
- [ ] **No test logic in production code** - Complete separation maintained
- [ ] **Minimal comments** - Only complex algorithms documented
- [ ] **Docstrings only for MCP tools** - Public API interfaces documented appropriately
- [ ] **No global variables** - Only UPPER_CASE constants if needed
- [ ] **Minimal nesting** - Maximum 3 levels deep throughout codebase
- [ ] **No inline imports** - All imports at file top
- [ ] **Python only** - No other languages introduced

### Technical Standards Compliance
- [ ] **uv virtual environment** - All operations use uv
- [ ] **Absolute imports** - All imports follow absolute path pattern
- [ ] **Full typing** - Every parameter and return value typed
- [ ] **Type syntax** - `str | None` format used consistently
- [ ] **Pydantic v2** - All models use current Pydantic version
- [ ] **Service layer separation** - Business logic separate from MCP interfaces
- [ ] **pytest + pytest-mock only** - No additional testing dependencies

### Quality Gate Validation
- [ ] **All endpoints delegate to services** - No business logic in MCP tools
- [ ] **All functions fully typed** - Complete type coverage
- [ ] **Tests cover service layer** - Comprehensive test coverage
- [ ] **mypy passes** - Zero type errors
- [ ] **ruff passes** - Zero linting issues
- [ ] **pytest passes** - All tests pass with no warnings

## Implementation Success Criteria

### Functional Requirements
- MCP Loop Tools correctly implement decision logic for all four loop types
- Stagnation detection accurately identifies improvement plateau scenarios
- Configuration system supports per-loop threshold customization
- Error handling provides graceful failure modes without system crashes
- Integration with Main Agent workflow patterns works seamlessly

### Quality Requirements
- Complete adherence to project coding standards as defined in CLAUDE.md
- Full test coverage with TDD methodology followed throughout implementation
- Zero mypy errors and zero ruff linting issues across entire codebase
- Self-documenting code through clear naming conventions
- Minimal but appropriate documentation for MCP tool public interfaces

### Performance Requirements
- Decision engine processes loop data efficiently for typical iteration counts
- Configuration loading performs adequately for session-scoped usage
- Memory usage remains reasonable during extended loop sequences
- Error handling doesn't introduce significant performance overhead

This implementation plan ensures systematic development of robust MCP Loop Tools while maintaining strict quality standards and following Test-Driven Development methodology throughout the entire process.
