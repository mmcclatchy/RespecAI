from abc import ABC, abstractmethod
from collections import deque

from services.utils.models import LoopState, MCPResponse
from services.utils.errors import LoopNotFoundError, LoopAlreadyExistsError


class StateManager(ABC):
    @abstractmethod
    def add_loop(self, loop: LoopState) -> None: ...

    @abstractmethod
    def get_loop(self, loop_id: str) -> LoopState | None: ...

    @abstractmethod
    def get_loop_status(self, loop_id: str) -> MCPResponse: ...

    @abstractmethod
    def decide_loop_next_action(self, loop_id: str, current_score: int) -> MCPResponse: ...

    @abstractmethod
    def list_active_loops(self) -> list[MCPResponse]: ...

    @abstractmethod
    def get_objective_feedback(self, loop_id: str) -> MCPResponse: ...

    @abstractmethod
    def store_objective_feedback(self, loop_id: str, feedback: str) -> MCPResponse: ...


class Queue[T]:
    def __init__(self, maxlen: int) -> None:
        self._deque: deque[T] = deque(maxlen=maxlen)
        self.maxlen = maxlen

    def append(self, item: T) -> T | None:
        self._deque.append(item)
        dropped_item = self._deque.popleft() if len(self._deque) > self.maxlen else None
        return dropped_item


class InMemoryStateManager(StateManager):
    def __init__(self, max_history_size: int = 10) -> None:
        self._active_loops: dict[str, LoopState] = {}
        self._loop_history: Queue[str] = Queue(maxlen=max_history_size)
        self._objective_feedback: dict[str, str] = {}

    def add_loop(self, loop: LoopState) -> None:
        if loop.id in self._active_loops:
            raise LoopAlreadyExistsError(f'Loop already exists: {loop.id}')
        self._active_loops[loop.id] = loop
        dropped_loop_id = self._loop_history.append(loop.id)
        if dropped_loop_id:
            self._active_loops.pop(dropped_loop_id)

    def get_loop(self, loop_id: str) -> LoopState:
        if loop_id in self._active_loops:
            return self._active_loops[loop_id]
        raise LoopNotFoundError(f'Loop not found: {loop_id}')

    def get_loop_status(self, loop_id: str) -> MCPResponse:
        loop_state = self.get_loop(loop_id)
        return loop_state.mcp_response

    def decide_loop_next_action(self, loop_id: str, current_score: int) -> MCPResponse:
        loop_state = self.get_loop(loop_id)
        loop_state.add_score(current_score)
        return loop_state.decide_next_loop_action()

    def list_active_loops(self) -> list[MCPResponse]:
        return [loop.mcp_response for loop in self._active_loops.values()]

    def get_objective_feedback(self, loop_id: str) -> MCPResponse:
        loop_state = self.get_loop(loop_id)
        feedback = self._objective_feedback.get(loop_id, '')
        return MCPResponse(
            id=loop_id, status=loop_state.status, message=feedback or 'No previous objective feedback found'
        )

    def store_objective_feedback(self, loop_id: str, feedback: str) -> MCPResponse:
        loop_state = self.get_loop(loop_id)
        self._objective_feedback[loop_id] = feedback
        return MCPResponse(
            id=loop_id, status=loop_state.status, message=f'Objective feedback stored for loop {loop_id}'
        )
