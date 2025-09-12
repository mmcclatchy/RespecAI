# MCP Tools Specification

## Overview
The MCP (Model Context Protocol) Server provides centralized loop state management and decision logic for the Spec-Driven Workflow system. It implements quality-driven refinement loops with stagnation detection and intelligent escalation.

## Core Architecture

### FastMCP Framework Integration
```python
from fastmcp import FastMCP, Context
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

# Server initialization with middleware pipeline
mcp = FastMCP("Loop Management Server")
mcp.add_middleware(ErrorHandlingMiddleware(...))
mcp.add_middleware(LoggingMiddleware(...))
```

### State Management
- **In-Memory Storage**: Session-scoped state management
- **Loop History**: Queue-based with configurable size (default: 10)
- **No Persistence**: States cleared between sessions
- **Concurrent Loops**: Support for multiple active loops

## MCP Tool Specifications

### 1. initialize_refinement_loop

#### Purpose
Creates a new refinement loop session for quality-driven content improvement.

#### Signature
```python
@mcp.tool()
async def initialize_refinement_loop(
    loop_type: str,
    ctx: Context
) -> MCPResponse
```

#### Parameters
- **loop_type**: One of `'plan'`, `'spec'`, `'build_plan'`, `'build_code'`
- **ctx**: FastMCP context for client communication

#### Returns
```python
MCPResponse(
    id="abc12345",  # 8-character UUID prefix
    status=LoopStatus.INITIALIZED
)
```

#### Decision Logic
```python
def initialize_refinement_loop(loop_type: str) -> MCPResponse:
    # 1. Validate loop type
    if loop_type not in ['plan', 'spec', 'build_plan', 'build_code']:
        raise LoopValidationError('loop_type', 'Invalid loop type')
    
    # 2. Create LoopState with type-specific configuration
    loop_state = LoopState(
        loop_type=LoopType(loop_type),
        status=LoopStatus.INITIALIZED,
        threshold=get_threshold(loop_type),  # 85/85/80/95
        max_iterations=get_max_iterations(loop_type)  # 5 for all
    )
    
    # 3. Add to state manager
    state_manager.add_loop(loop_state)
    
    # 4. Return initial response
    return loop_state.mcp_response
```

#### Error Handling
- **LoopValidationError**: Invalid loop_type provided
- **LoopAlreadyExistsError**: Duplicate loop ID (rare collision)
- **LoopStateError**: Unexpected state management error

#### Example Usage
```python
# Main Agent initializes plan refinement loop
response = await mcp.initialize_refinement_loop(
    loop_type='plan',
    ctx=context
)
# Returns: MCPResponse(id='a1b2c3d4', status='initialized')
```

---

### 2. decide_loop_next_action

#### Purpose
Analyzes quality scores and iteration history to determine next refinement action.

#### Signature
```python
@mcp.tool()
async def decide_loop_next_action(
    loop_id: str,
    current_score: int,
    ctx: Context
) -> MCPResponse
```

#### Parameters
- **loop_id**: Unique identifier of the loop
- **current_score**: Quality score from 0-100
- **ctx**: FastMCP context for client communication

#### Returns
```python
MCPResponse(
    id="abc12345",
    status=LoopStatus.COMPLETED |  # Score >= threshold
           LoopStatus.REFINE |      # Continue refinement
           LoopStatus.USER_INPUT    # Stagnation detected
)
```

#### Decision Logic
```python
def decide_next_loop_action(self) -> MCPResponse:
    # 1. Check quality threshold
    if self.current_score >= self.loop_type.threshold:
        self.status = LoopStatus.COMPLETED
        return self.mcp_response
    
    # 2. Check iteration limit
    if self.iteration >= self.loop_type.max_iterations:
        self.status = LoopStatus.USER_INPUT
        return self.mcp_response
    
    # 3. Check stagnation
    if self._detect_stagnation():
        self.status = LoopStatus.USER_INPUT
        return self.mcp_response
    
    # 4. Continue refinement
    self.status = LoopStatus.REFINE
    self.increment_iteration()
    return self.mcp_response
```

#### Stagnation Detection Algorithm
```python
def _detect_stagnation(self) -> bool:
    # Need at least 3 scores for comparison
    if len(self.score_history) < 3:
        return False
    
    # Check last 2 improvements
    improvement_threshold = 5  # Points
    recent_improvements = [
        self._calculate_improvement(2),  # 2 iterations ago
        self._calculate_improvement(1),  # 1 iteration ago
    ]
    
    # Stagnant if both improvements < 5 points
    return all(imp < improvement_threshold for imp in recent_improvements)
```

#### Quality Thresholds by Loop Type
| Loop Type | Threshold | Max Iterations | Environment Variable |
|-----------|-----------|----------------|---------------------|
| plan | 85% | 5 | FSDD_LOOP_PLAN_THRESHOLD |
| spec | 85% | 5 | FSDD_LOOP_SPEC_THRESHOLD |
| build_plan | 80% | 5 | FSDD_LOOP_BUILD_PLAN_THRESHOLD |
| build_code | 95% | 5 | FSDD_LOOP_BUILD_CODE_THRESHOLD |

#### Error Handling
- **LoopNotFoundError**: Invalid loop_id provided
- **LoopValidationError**: Score outside 0-100 range
- **LoopStateError**: Unexpected decision logic error

#### Example Usage
```python
# Main Agent submits quality score for decision
response = await mcp.decide_loop_next_action(
    loop_id='a1b2c3d4',
    current_score=72,
    ctx=context
)

# Possible responses:
# MCPResponse(id='a1b2c3d4', status='refine')     # Continue
# MCPResponse(id='a1b2c3d4', status='completed')  # Done
# MCPResponse(id='a1b2c3d4', status='user_input') # Stuck
```

---

### 3. get_loop_status

#### Purpose
Retrieves current state and history of a refinement loop.

#### Signature
```python
@mcp.tool()
async def get_loop_status(
    loop_id: str,
    ctx: Context
) -> MCPResponse
```

#### Parameters
- **loop_id**: Unique identifier of the loop
- **ctx**: FastMCP context for client communication

#### Returns
```python
MCPResponse(
    id="abc12345",
    status=LoopStatus.INITIALIZED |
           LoopStatus.IN_PROGRESS |
           LoopStatus.COMPLETED |
           LoopStatus.USER_INPUT |
           LoopStatus.REFINE
)
```

#### Internal State Structure
```python
LoopState(
    id="abc12345",
    loop_type=LoopType.PLAN,
    status=LoopStatus.REFINE,
    current_score=72,
    score_history=[45, 62, 72],
    iteration=3,
    created_at="2025-01-15T10:30:00"
)
```

#### Error Handling
- **LoopNotFoundError**: Invalid loop_id provided
- **LoopStateError**: State retrieval error

#### Example Usage
```python
# Main Agent checks loop status
response = await mcp.get_loop_status(
    loop_id='a1b2c3d4',
    ctx=context
)
# Returns: MCPResponse(id='a1b2c3d4', status='refine')
```

---

### 4. list_active_loops

#### Purpose
Returns all currently active refinement loops in the session.

#### Signature
```python
@mcp.tool()
async def list_active_loops(
    ctx: Context
) -> list[MCPResponse]
```

#### Parameters
- **ctx**: FastMCP context for client communication

#### Returns
```python
[
    MCPResponse(id="abc12345", status=LoopStatus.REFINE),
    MCPResponse(id="def67890", status=LoopStatus.COMPLETED),
    MCPResponse(id="ghi11121", status=LoopStatus.USER_INPUT)
]
```

#### State Management
- Returns all loops in current session
- Maximum of 10 loops retained (FIFO)
- Oldest loops dropped when limit exceeded

#### Error Handling
- **LoopStateError**: List retrieval error

#### Example Usage
```python
# Main Agent lists all active loops
loops = await mcp.list_active_loops(ctx=context)
# Returns: [MCPResponse(...), MCPResponse(...)]

for loop in loops:
    print(f"Loop {loop.id}: {loop.status}")
```

---

## Configuration Management

### Environment Variables
```bash
# Quality thresholds (1-100)
FSDD_LOOP_PLAN_THRESHOLD=85
FSDD_LOOP_SPEC_THRESHOLD=85
FSDD_LOOP_BUILD_PLAN_THRESHOLD=80
FSDD_LOOP_BUILD_CODE_THRESHOLD=95

# Maximum iterations (1-20)
FSDD_LOOP_PLAN_MAX_ITERATIONS=5
FSDD_LOOP_SPEC_MAX_ITERATIONS=5
FSDD_LOOP_BUILD_PLAN_MAX_ITERATIONS=5
FSDD_LOOP_BUILD_CODE_MAX_ITERATIONS=5

# MCP Server settings
FSDD_MCP_SERVER_NAME="Loop Management Server"
FSDD_MCP_HOST="0.0.0.0"
FSDD_MCP_PORT=8000
FSDD_MCP_DEBUG=false
```

### Pydantic Settings Models
```python
class LoopConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra='forbid',
        env_prefix='FSDD_LOOP_'
    )
    
    plan_threshold: int = Field(default=85, ge=1, le=100)
    spec_threshold: int = Field(default=85, ge=1, le=100)
    build_plan_threshold: int = Field(default=80, ge=1, le=100)
    build_code_threshold: int = Field(default=95, ge=1, le=100)
    
    plan_max_iterations: int = Field(default=5, ge=1, le=20)
    # ... etc
```

## Error Handling Architecture

### Service Boundary Pattern
```python
# Domain exceptions mapped at service layer
class LoopTools:
    def initialize_refinement_loop(self, loop_type: str) -> MCPResponse:
        try:
            # Domain logic
            loop_state = LoopState(loop_type=LoopType(loop_type))
            self.state.add_loop(loop_state)
            return loop_state.mcp_response
        except ValueError:
            # Map to FastMCP-compatible exception
            raise LoopValidationError('loop_type', 'Invalid type')
        except LoopAlreadyExistsError as e:
            raise LoopStateError('new', 'initialization', str(e))
```

### FastMCP Middleware Pipeline
1. **ErrorHandlingMiddleware**: Catches and transforms exceptions
2. **LoggingMiddleware**: Logs all tool calls and responses
3. **Context Communication**: Real-time client updates

### Exception Hierarchy
```
LoopError (Base)
├── LoopValidationError (Invalid inputs)
├── LoopStateError (State management issues)
├── LoopNotFoundError (Missing loop)
└── LoopAlreadyExistsError (Duplicate ID)
```

## Usage Patterns

### Complete Refinement Loop Flow
```python
# 1. Initialize loop
loop = await mcp.initialize_refinement_loop('plan', ctx)

# 2. Refinement iterations
while True:
    # Generate content (via agents)
    content = await generate_content()
    
    # Assess quality (via critic)
    score = await assess_quality(content)
    
    # Get decision from MCP
    decision = await mcp.decide_loop_next_action(loop.id, score, ctx)
    
    # Handle decision
    if decision.status == LoopStatus.COMPLETED:
        break  # Quality threshold met
    elif decision.status == LoopStatus.REFINE:
        continue  # Continue refinement
    elif decision.status == LoopStatus.USER_INPUT:
        await request_user_clarification()
        break  # Stagnation detected
```

### Parallel Loop Management
```python
# Multiple loops can run simultaneously
plan_loop = await mcp.initialize_refinement_loop('plan', ctx)
spec_loop = await mcp.initialize_refinement_loop('spec', ctx)

# Independent decision making
plan_decision = await mcp.decide_loop_next_action(plan_loop.id, 85, ctx)
spec_decision = await mcp.decide_loop_next_action(spec_loop.id, 72, ctx)
```

## Testing Considerations

### Unit Testing
```python
def test_stagnation_detection():
    loop = LoopState(loop_type=LoopType.PLAN)
    
    # Add improving scores
    loop.add_score(50)
    loop.add_score(65)  # +15 improvement
    loop.add_score(70)  # +5 improvement
    
    # Should not be stagnant
    assert not loop._detect_stagnation()
    
    # Add stagnant scores
    loop.add_score(73)  # +3 improvement
    loop.add_score(75)  # +2 improvement
    
    # Should detect stagnation (both < 5)
    assert loop._detect_stagnation()
```

### Integration Testing
```python
async def test_complete_workflow():
    # Initialize
    loop = await mcp.initialize_refinement_loop('spec', ctx)
    assert loop.status == LoopStatus.INITIALIZED
    
    # Low score - should refine
    decision = await mcp.decide_loop_next_action(loop.id, 70, ctx)
    assert decision.status == LoopStatus.REFINE
    
    # High score - should complete
    decision = await mcp.decide_loop_next_action(loop.id, 90, ctx)
    assert decision.status == LoopStatus.COMPLETED
```

## Performance Characteristics

### Benchmarks
- **Tool Call Latency**: <10ms average
- **Decision Logic**: <1ms computation
- **State Management**: O(1) operations
- **Memory Usage**: <100KB per loop

### Scalability
- **Concurrent Loops**: Up to 10 active
- **Score History**: Unlimited per loop
- **Session Duration**: No time limits
- **Request Rate**: >1000 req/s capability

## Related Documentation
- **Implementation**: [MCP Loop Tools Implementation](MCP_LOOP_TOOLS_IMPLEMENTATION.md)
- **Commands**: [Command Specifications](commands/)
- **Agents**: [Agent Specifications](agents/)
- **Workflow**: [Workflow Orchestration](WORKFLOW_ORCHESTRATION.md)
- **Quality**: [Quality Framework](QUALITY_FRAMEWORK.md)