from abc import ABC, abstractmethod
from collections import deque

from services.models.initial_spec import InitialSpec
from services.models.roadmap import Roadmap
from services.models.spec import TechnicalSpec
from services.utils.errors import LoopAlreadyExistsError, LoopNotFoundError, RoadmapNotFoundError, SpecNotFoundError
from services.utils.loop_state import LoopState, MCPResponse


class StateManager(ABC):
    # Loop Management
    @abstractmethod
    def add_loop(self, loop: LoopState) -> None: ...

    @abstractmethod
    def get_loop(self, loop_id: str) -> LoopState: ...

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

    # Roadmap Management
    @abstractmethod
    def store_roadmap(self, project_id: str, roadmap: Roadmap) -> str: ...

    @abstractmethod
    def get_roadmap(self, project_id: str) -> Roadmap: ...

    # Initial Spec Management (Business Requirements)
    @abstractmethod
    def store_initial_spec(self, project_id: str, spec: InitialSpec) -> str: ...

    @abstractmethod
    def get_initial_spec(self, project_id: str, spec_name: str) -> InitialSpec: ...

    @abstractmethod
    def list_initial_specs(self, project_id: str) -> list[str]: ...

    @abstractmethod
    def delete_initial_spec(self, project_id: str, spec_name: str) -> bool: ...

    # Technical Spec Management (Implementation Details)
    @abstractmethod
    def store_technical_spec(self, project_id: str, spec: TechnicalSpec) -> str: ...

    @abstractmethod
    def get_technical_spec(self, project_id: str, spec_name: str) -> TechnicalSpec: ...

    @abstractmethod
    def list_technical_specs(self, project_id: str) -> list[str]: ...

    @abstractmethod
    def delete_technical_spec(self, project_id: str, spec_name: str) -> bool: ...


class Queue[T]:
    def __init__(self, maxlen: int) -> None:
        self._deque: deque[T] = deque(maxlen=maxlen)
        self.maxlen = maxlen

    def append(self, item: T) -> T | None:
        # Check if we're at capacity before adding
        dropped_item = None
        if len(self._deque) == self.maxlen:
            # Will be dropped when new item is added
            dropped_item = self._deque[0]

        self._deque.append(item)
        return dropped_item


class InMemoryStateManager(StateManager):
    def __init__(self, max_history_size: int = 10) -> None:
        self._active_loops: dict[str, LoopState] = {}
        self._loop_history: Queue[str] = Queue(maxlen=max_history_size)
        self._objective_feedback: dict[str, str] = {}
        self._roadmaps: dict[str, Roadmap] = {}
        self._initial_specs: dict[str, dict[str, InitialSpec]] = {}  # project_id -> {spec_name -> InitialSpec}
        self._technical_specs: dict[str, dict[str, TechnicalSpec]] = {}  # project_id -> {spec_name -> TechnicalSpec}

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

    def store_roadmap(self, project_id: str, roadmap: Roadmap) -> str:
        self._roadmaps[project_id] = roadmap
        return project_id

    def get_roadmap(self, project_id: str) -> Roadmap:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')
        return self._roadmaps[project_id]

    def store_initial_spec(self, project_id: str, spec: InitialSpec) -> str:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        # Store the InitialSpec separately
        if project_id not in self._initial_specs:
            self._initial_specs[project_id] = {}
        self._initial_specs[project_id][spec.phase_name] = spec

        # Add spec to roadmap if not already there
        roadmap = self._roadmaps[project_id]
        roadmap.add_spec(spec)

        return spec.phase_name

    def get_initial_spec(self, project_id: str, spec_name: str) -> InitialSpec:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        if project_id not in self._initial_specs or spec_name not in self._initial_specs[project_id]:
            raise SpecNotFoundError(f'Initial spec not found: {spec_name}')

        return self._initial_specs[project_id][spec_name]

    def list_initial_specs(self, project_id: str) -> list[str]:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')
        roadmap = self._roadmaps[project_id]
        return [spec.phase_name for spec in roadmap.specs]

    def delete_initial_spec(self, project_id: str, spec_name: str) -> bool:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        # Remove from both the initial specs storage and roadmap
        removed_from_specs = False
        if project_id in self._initial_specs and spec_name in self._initial_specs[project_id]:
            del self._initial_specs[project_id][spec_name]
            removed_from_specs = True

        roadmap = self._roadmaps[project_id]
        # Find and remove spec by phase_name
        for i, spec in enumerate(roadmap.specs):
            if spec.phase_name == spec_name:
                roadmap.specs.pop(i)
                roadmap.spec_count = len(roadmap.specs)
                return True

        return removed_from_specs

    def store_technical_spec(self, project_id: str, spec: TechnicalSpec) -> str:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        # Store the TechnicalSpec separately
        if project_id not in self._technical_specs:
            self._technical_specs[project_id] = {}
        self._technical_specs[project_id][spec.phase_name] = spec

        return spec.phase_name

    def get_technical_spec(self, project_id: str, spec_name: str) -> TechnicalSpec:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        if project_id not in self._technical_specs or spec_name not in self._technical_specs[project_id]:
            raise SpecNotFoundError(f'Technical spec not found: {spec_name}')

        return self._technical_specs[project_id][spec_name]

    def list_technical_specs(self, project_id: str) -> list[str]:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        if project_id not in self._technical_specs:
            return []

        return list(self._technical_specs[project_id].keys())

    def delete_technical_spec(self, project_id: str, spec_name: str) -> bool:
        if project_id not in self._roadmaps:
            raise RoadmapNotFoundError(f'Roadmap not found for project: {project_id}')

        # Remove from technical specs storage
        if project_id in self._technical_specs and spec_name in self._technical_specs[project_id]:
            del self._technical_specs[project_id][spec_name]
            return True

        return False
