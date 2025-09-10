import pytest

from services.mcp.loop_tools import loop_tools
from services.utils.enums import LoopStatus
from services.utils.errors import LoopStateError, LoopValidationError
from services.utils.models import MCPResponse


class TestLoopToolsMCP:
    def test_decide_loop_next_action_complete_decision(self) -> None:
        # Initialize a build_code loop (threshold 95%)
        init_result = loop_tools.initialize_refinement_loop('build_code')
        loop_id = init_result.id

        # High score should complete
        result = loop_tools.decide_loop_next_action(loop_id, 96)

        assert isinstance(result, MCPResponse)
        assert result.status == LoopStatus.COMPLETED

    def test_decide_loop_next_action_refine_decision(self) -> None:
        # Initialize a spec loop (threshold 85%)
        init_result = loop_tools.initialize_refinement_loop('spec')
        loop_id = init_result.id

        # Score below threshold should refine
        result = loop_tools.decide_loop_next_action(loop_id, 70)

        assert isinstance(result, MCPResponse)
        assert result.status == LoopStatus.REFINE

    def test_decide_loop_next_action_user_input_decision(self) -> None:
        # Initialize a plan loop
        init_result = loop_tools.initialize_refinement_loop('plan')
        loop_id = init_result.id

        # Add multiple low improvement scores to trigger stagnation
        loop_tools.decide_loop_next_action(loop_id, 60)
        loop_tools.decide_loop_next_action(loop_id, 61)
        loop_tools.decide_loop_next_action(loop_id, 62)

        # Should detect stagnation and request user input
        result = loop_tools.decide_loop_next_action(loop_id, 63)

        assert isinstance(result, MCPResponse)
        assert result.status == LoopStatus.USER_INPUT

    def test_decide_loop_next_action_invalid_loop_id(self) -> None:
        with pytest.raises(LoopStateError):
            loop_tools.decide_loop_next_action('nonexistent-loop-id', 80)

    def test_decide_loop_next_action_score_validation(self) -> None:
        init_result = loop_tools.initialize_refinement_loop('plan')
        loop_id = init_result.id

        # Test valid score ranges
        result = loop_tools.decide_loop_next_action(loop_id, 0)
        assert isinstance(result, MCPResponse)

        result = loop_tools.decide_loop_next_action(loop_id, 100)
        assert isinstance(result, MCPResponse)

        # Test invalid score ranges
        with pytest.raises(LoopValidationError):
            loop_tools.decide_loop_next_action(loop_id, -1)

        with pytest.raises(LoopValidationError):
            loop_tools.decide_loop_next_action(loop_id, 101)

    def test_decide_loop_next_action_max_iterations(self) -> None:
        # Initialize a plan loop with low max_iterations for testing
        init_result = loop_tools.initialize_refinement_loop('plan')
        loop_id = init_result.id

        # Add scores until we hit max iterations (5 for plan loops)
        for score in [60, 61, 62, 63, 64]:
            result = loop_tools.decide_loop_next_action(loop_id, score)

        # Should request user input due to max iterations
        assert result.status == LoopStatus.USER_INPUT

    def test_initialize_refinement_loop_integration(self) -> None:
        result = loop_tools.initialize_refinement_loop('build_plan')

        assert isinstance(result, MCPResponse)
        assert result.status == LoopStatus.INITIALIZED
        assert len(result.id) > 0

    def test_get_loop_status_integration(self) -> None:
        init_result = loop_tools.initialize_refinement_loop('spec')
        loop_id = init_result.id

        status = loop_tools.get_loop_status(loop_id)

        assert isinstance(status, MCPResponse)
        assert status.id == loop_id
        assert status.status == LoopStatus.INITIALIZED

    def test_list_active_loops_integration(self) -> None:
        # Create multiple loops
        loop1 = loop_tools.initialize_refinement_loop('plan')
        loop2 = loop_tools.initialize_refinement_loop('spec')

        active_loops = loop_tools.list_active_loops()

        assert isinstance(active_loops, list)
        assert len(active_loops) >= 2

        loop_ids = [loop.id for loop in active_loops]
        assert loop1.id in loop_ids
        assert loop2.id in loop_ids
