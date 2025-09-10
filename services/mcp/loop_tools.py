from services.utils.models import LoopState, LoopType, MCPResponse
from services.utils.state_manager import StateManager, InMemoryStateManager


class LoopTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def initialize_refinement_loop(self, loop_type: str) -> MCPResponse:
        loop_type_enum = LoopType(loop_type)
        loop_state = LoopState(loop_type=loop_type_enum)
        self.state.add_loop(loop_state)
        return loop_state.mcp_response

    def get_loop_status(self, loop_id: str) -> MCPResponse:
        return self.state.get_loop_status(loop_id)

    def list_active_loops(self) -> list[MCPResponse]:
        return self.state.list_active_loops()

    def decide_loop_next_action(self, loop_id: str, current_score: int) -> MCPResponse:
        """MCP tool to decide the next action for a refinement loop.

        This is the main MCP tool interface that external agents will call
        to determine whether to continue refining, complete the loop, or
        request user input based on quality scores and iteration count.
        """
        return self.state.decide_loop_next_action(loop_id, current_score)


loop_tools = LoopTools(InMemoryStateManager())
