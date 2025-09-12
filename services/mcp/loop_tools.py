from services.utils.models import LoopState, LoopType, MCPResponse
from services.utils.state_manager import StateManager, InMemoryStateManager
from services.utils.errors import LoopNotFoundError, LoopAlreadyExistsError, LoopValidationError, LoopStateError


class LoopTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def initialize_refinement_loop(self, loop_type: str) -> MCPResponse:
        try:
            loop_type_enum = LoopType(loop_type)
            loop_state = LoopState(loop_type=loop_type_enum)
            self.state.add_loop(loop_state)
            return loop_state.mcp_response
        except ValueError:
            valid_types = {'plan', 'spec', 'build_plan', 'build_code'}
            raise LoopValidationError('loop_type', f'Must be one of {valid_types}')
        except LoopAlreadyExistsError as e:
            raise LoopStateError('new', 'initialization', f'Failed to create loop: {str(e)}')
        except Exception as e:
            raise LoopStateError('new', 'initialization', f'Unexpected error: {str(e)}')

    def get_loop_status(self, loop_id: str) -> MCPResponse:
        try:
            return self.state.get_loop_status(loop_id)
        except LoopNotFoundError:
            raise LoopStateError(loop_id, 'status_retrieval', 'Loop does not exist')
        except Exception as e:
            raise LoopStateError(loop_id, 'status_retrieval', f'Unexpected error: {str(e)}')

    def list_active_loops(self) -> list[MCPResponse]:
        try:
            return self.state.list_active_loops()
        except Exception as e:
            raise LoopStateError('all', 'list_retrieval', f'Failed to retrieve loop list: {str(e)}')

    def decide_loop_next_action(self, loop_id: str, current_score: int) -> MCPResponse:
        """MCP tool to decide the next action for a refinement loop.

        This is the main MCP tool interface that external agents will call
        to determine whether to continue refining, complete the loop, or
        request user input based on quality scores and iteration count.
        """
        try:
            if not (0 <= current_score <= 100):
                raise LoopValidationError('score', 'Must be between 0 and 100')
            return self.state.decide_loop_next_action(loop_id, current_score)
        except LoopNotFoundError:
            raise LoopStateError(loop_id, 'decision', 'Loop does not exist')
        except LoopValidationError:
            raise  # Re-raise validation errors as-is
        except Exception as e:
            raise LoopStateError(loop_id, 'decision', f'Unexpected error: {str(e)}')

    def get_previous_objective_feedback(self, loop_id: str) -> MCPResponse:
        try:
            return self.state.get_objective_feedback(loop_id)
        except LoopNotFoundError:
            raise LoopStateError(loop_id, 'feedback_retrieval', 'Loop does not exist')
        except Exception as e:
            raise LoopStateError(loop_id, 'feedback_retrieval', f'Unexpected error: {str(e)}')

    def store_current_objective_feedback(self, loop_id: str, feedback: str) -> MCPResponse:
        try:
            return self.state.store_objective_feedback(loop_id, feedback)
        except LoopNotFoundError:
            raise LoopStateError(loop_id, 'feedback_storage', 'Loop does not exist')
        except Exception as e:
            raise LoopStateError(loop_id, 'feedback_storage', f'Unexpected error: {str(e)}')


loop_tools = LoopTools(InMemoryStateManager())
