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

### Step 3.3: FastMCP Server Integration

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/integration/test_fastmcp_server.py
- Test FastMCP server initialization and tool registration
- Test MCP tool discovery and metadata
- Test server startup/shutdown lifecycle
- Test error handling at server level
- Test tool parameter validation through FastMCP
- Verify tests fail without FastMCP implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create services/mcp/server.py with FastMCP server setup
- Register existing decide_loop_next_action as @mcp.tool()
- Add server configuration via Pydantic settings
- Implement graceful server lifecycle management
- Add health check endpoints
- Ensure proper async/await patterns if needed
- Make all tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Add comprehensive docstrings for FastMCP tools
- ✅ Validate production-ready configuration
- ✅ Ensure proper error handling at server level
- ✅ Follow FastMCP best practices from documentation
- ✅ Verify service layer separation maintained
```

### Step 3.4: Loop Management Tools

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/unit/mcp/test_loop_management.py
- Test initialize_refinement_loop MCP tool
- Test reset_loop_state MCP tool
- Test get_loop_status MCP tool
- Test list_active_loops MCP tool
- Test concurrent loop management scenarios
- Test session-scoped loop state persistence
- Test loop ID generation and tracking
- Verify tests fail without loop management implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Extend services/mcp/loop_tools.py with new MCP tools:
  - initialize_refinement_loop(loop_type, initial_content)
  - reset_loop_state(loop_id)
  - get_loop_status(loop_id)
  - list_active_loops()
- Implement session-scoped loop state storage
- Add loop ID generation and tracking mechanisms
- Register new tools with FastMCP server
- Ensure all tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run mypy - resolve all type errors
- ✅ Run ruff - fix all linting issues
- ✅ Run pytest - all tests pass, no warnings
- ✅ Add proper error handling for loop management
- ✅ Ensure clean separation between loop management and decision logic
- ✅ Add comprehensive tool documentation for MCP interfaces
- ✅ Validate loop state management patterns
- ✅ Check concurrent access safety (session-scoped)
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

### Step 4.3: Production MCP Server (UPDATED)

**Red Phase - Create failing tests**:
```text
Test Coverage Required:
- Create tests/e2e/test_production_mcp_server.py
- Test complete workflow: initialize → iterate → complete
- Test real MCP client integration scenarios
- Test configuration loading from environment variables
- Test multi-loop concurrent scenarios
- Test FastMCP server production deployment patterns
- Test health check endpoints and monitoring
- Verify tests fail before production server implementation
```

**Green Phase - Minimal implementation**:
```text
Implementation Tasks:
- Create main.py or mcp_server.py as production entry point
- Add proper logging configuration for production
- Implement production server configuration with FastMCP
- Add monitoring and health endpoints
- Create deployment configuration (Docker, environment files)
- Integrate all MCP tools (decision + loop management) with server
- Ensure production-ready error handling and graceful shutdown
- Make all production tests pass
```

**Refactor Phase - Quality compliance**:
```text
Quality Gates:
- ✅ Run complete test suite - 100% pass rate, zero warnings
- ✅ Run mypy on entire project - zero errors
- ✅ Run ruff on entire project - zero linting issues
- ✅ Final production readiness review
- ✅ Performance optimization validation
- ✅ Complete deployment documentation
- ✅ Validate against FastMCP production best practices
- ✅ Verify all logging and monitoring works correctly
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
- [ ] **FastMCP framework integration** - Production-ready MCP server implementation

### Quality Gate Validation
- [ ] **All endpoints delegate to services** - No business logic in MCP tools
- [ ] **All functions fully typed** - Complete type coverage
- [ ] **Tests cover service layer** - Comprehensive test coverage
- [ ] **mypy passes** - Zero type errors
- [ ] **ruff passes** - Zero linting issues
- [ ] **pytest passes** - All tests pass with no warnings
- [ ] **FastMCP tools properly registered** - All tools discoverable and functional

## Updated Tool Architecture

### Complete MCP Server Structure
```python
# Production MCP Server with FastMCP Integration
from fastmcp import FastMCP

mcp = FastMCP("Loop Management Server")

@mcp.tool()
def initialize_refinement_loop(loop_type: str, initial_content: str) -> dict:
    """Start a new refinement loop with initial content.
    
    Args:
        loop_type: Type of loop (plan, spec, build_plan, build_code)
        initial_content: Initial content to start refining
        
    Returns:
        dict: Loop initialization result with loop_id and status
    """
    # Implementation using existing services

@mcp.tool() 
def decide_loop_next_action(
    loop_type: str,
    current_score: int, 
    previous_scores: list[int],
    iteration: int,
    max_iterations: int = 20
) -> str:
    """Decide next action for refinement loop progression.
    
    This is the core decision tool - already implemented and tested.
    """
    # Current implementation - no changes needed
    
@mcp.tool()
def reset_loop_state(loop_id: str) -> dict:
    """Reset or clear loop state for fresh start."""
    # New implementation needed

@mcp.tool()
def get_loop_status(loop_id: str) -> dict:
    """Get current status and history of a loop."""
    # New implementation needed
    
@mcp.tool()
def list_active_loops() -> list[dict]:
    """List all currently active refinement loops."""
    # New implementation needed
```

## Implementation Success Criteria (UPDATED)

### Functional Requirements
- **MCP Loop Tools**: Correctly implement decision logic for all four loop types
- **Loop Management**: Complete loop lifecycle management (initialize, iterate, complete)
- **Stagnation Detection**: Accurately identifies improvement plateau scenarios
- **Configuration System**: Supports per-loop threshold customization
- **Error Handling**: Graceful failure modes without system crashes
- **FastMCP Integration**: Production-ready MCP server with proper tool registration
- **Multi-Loop Support**: Concurrent loop management with session-scoped state
- **Main Agent Integration**: Seamless workflow patterns for external agent calls

### Quality Requirements
- Complete adherence to project coding standards as defined in CLAUDE.md
- Full test coverage with TDD methodology followed throughout implementation
- Zero mypy errors and zero ruff linting issues across entire codebase
- Self-documenting code through clear naming conventions
- Comprehensive documentation for all MCP tool public interfaces
- FastMCP best practices compliance for production deployment

### Performance Requirements
- Decision engine processes loop data efficiently for typical iteration counts
- Configuration loading performs adequately for session-scoped usage
- Memory usage remains reasonable during extended loop sequences
- Error handling doesn't introduce significant performance overhead
- FastMCP server handles concurrent requests efficiently
- Loop state management scales appropriately for multiple active loops

This implementation plan ensures systematic development of robust MCP Loop Tools while maintaining strict quality standards and following Test-Driven Development methodology throughout the entire process.
