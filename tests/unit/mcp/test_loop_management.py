import pytest

from services.mcp.loop_tools import loop_tools
from services.utils.enums import LoopStatus
from services.utils.errors import LoopStateError, LoopValidationError
from services.utils.models import MCPResponse


class TestLoopManagement:
    def test_initialize_refinement_loop_valid_inputs(self) -> None:
        result = loop_tools.initialize_refinement_loop('plan')

        assert isinstance(result, MCPResponse)
        assert result.status == LoopStatus.INITIALIZED
        assert isinstance(result.id, str)
        assert len(result.id) > 0

    def test_initialize_refinement_loop_invalid_loop_type(self) -> None:
        with pytest.raises(LoopValidationError):
            loop_tools.initialize_refinement_loop('invalid_type')

    def test_get_loop_status_existing_loop(self) -> None:
        init_result = loop_tools.initialize_refinement_loop('build_plan')
        loop_id = init_result.id

        status_result = loop_tools.get_loop_status(loop_id)

        assert isinstance(status_result, MCPResponse)
        assert status_result.id == loop_id
        assert status_result.status == LoopStatus.INITIALIZED

    def test_get_loop_status_nonexistent_loop(self) -> None:
        with pytest.raises(LoopStateError):
            loop_tools.get_loop_status('nonexistent-loop-id')

    def test_list_active_loops_empty_initially(self) -> None:
        result = loop_tools.list_active_loops()
        assert isinstance(result, list)

    def test_list_active_loops_with_loops(self) -> None:
        init1 = loop_tools.initialize_refinement_loop('plan')
        init2 = loop_tools.initialize_refinement_loop('spec')

        result = loop_tools.list_active_loops()

        assert isinstance(result, list)
        assert len(result) >= 2

        loop_ids = [loop.id for loop in result]
        assert init1.id in loop_ids
        assert init2.id in loop_ids

    def test_concurrent_loop_management(self) -> None:
        loop1 = loop_tools.initialize_refinement_loop('plan')
        loop2 = loop_tools.initialize_refinement_loop('spec')

        status1 = loop_tools.get_loop_status(loop1.id)
        status2 = loop_tools.get_loop_status(loop2.id)

        assert status1.id != status2.id
        assert status1.status == LoopStatus.INITIALIZED
        assert status2.status == LoopStatus.INITIALIZED

    def test_decide_loop_next_action_functionality(self) -> None:
        init_result = loop_tools.initialize_refinement_loop('build_code')
        loop_id = init_result.id

        # Test decision with high score (should complete)
        decision_result = loop_tools.decide_loop_next_action(loop_id, 95)

        assert isinstance(decision_result, MCPResponse)
        assert decision_result.id == loop_id

    def test_loop_id_generation_uniqueness(self) -> None:
        loop1 = loop_tools.initialize_refinement_loop('plan')
        loop2 = loop_tools.initialize_refinement_loop('plan')

        assert loop1.id != loop2.id
        assert isinstance(loop1.id, str)
        assert isinstance(loop2.id, str)
