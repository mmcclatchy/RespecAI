import pytest
from services.mcp.loop_tools import initialize_refinement_loop, reset_loop_state, get_loop_status, list_active_loops


class TestLoopManagement:
    def test_initialize_refinement_loop_valid_inputs(self) -> None:
        result = initialize_refinement_loop('plan', 'Initial plan content')

        assert isinstance(result, dict)
        assert 'loop_id' in result
        assert 'status' in result
        assert result['status'] == 'initialized'
        assert isinstance(result['loop_id'], str)
        assert len(result['loop_id']) > 0

    def test_initialize_refinement_loop_invalid_loop_type(self) -> None:
        with pytest.raises(ValueError, match='Invalid loop_type'):
            initialize_refinement_loop('invalid_type', 'Some content')

    def test_initialize_refinement_loop_empty_content(self) -> None:
        with pytest.raises(ValueError, match='initial_content cannot be empty'):
            initialize_refinement_loop('plan', '')

    def test_reset_loop_state_existing_loop(self) -> None:
        init_result = initialize_refinement_loop('spec', 'Test content')
        loop_id = init_result['loop_id']

        reset_result = reset_loop_state(loop_id)

        assert isinstance(reset_result, dict)
        assert 'loop_id' in reset_result
        assert 'status' in reset_result
        assert reset_result['loop_id'] == loop_id
        assert reset_result['status'] == 'reset'

    def test_reset_loop_state_nonexistent_loop(self) -> None:
        with pytest.raises(ValueError, match='Loop not found'):
            reset_loop_state('nonexistent-loop-id')

    def test_get_loop_status_existing_loop(self) -> None:
        init_result = initialize_refinement_loop('build_plan', 'Build content')
        loop_id = init_result['loop_id']

        status_result = get_loop_status(loop_id)

        assert isinstance(status_result, dict)
        assert 'loop_id' in status_result
        assert 'loop_type' in status_result
        assert 'status' in status_result
        assert 'iteration_count' in status_result
        assert 'score_history' in status_result
        assert 'created_at' in status_result
        assert status_result['loop_id'] == loop_id
        assert status_result['loop_type'] == 'build_plan'
        assert isinstance(status_result['score_history'], list)

    def test_get_loop_status_nonexistent_loop(self) -> None:
        with pytest.raises(ValueError, match='Loop not found'):
            get_loop_status('nonexistent-loop-id')

    def test_list_active_loops_empty(self) -> None:
        result = list_active_loops()

        assert isinstance(result, list)

    def test_list_active_loops_with_loops(self) -> None:
        init1 = initialize_refinement_loop('plan', 'Plan content 1')
        init2 = initialize_refinement_loop('spec', 'Spec content 2')

        result = list_active_loops()

        assert isinstance(result, list)
        assert len(result) >= 2

        loop_ids = [loop['loop_id'] for loop in result]
        assert init1['loop_id'] in loop_ids
        assert init2['loop_id'] in loop_ids

    def test_concurrent_loop_management(self) -> None:
        loop1 = initialize_refinement_loop('plan', 'Content 1')
        loop2 = initialize_refinement_loop('spec', 'Content 2')

        status1 = get_loop_status(loop1['loop_id'])
        status2 = get_loop_status(loop2['loop_id'])

        assert status1['loop_id'] != status2['loop_id']
        assert status1['loop_type'] == 'plan'
        assert status2['loop_type'] == 'spec'

    def test_session_scoped_loop_state_persistence(self) -> None:
        init_result = initialize_refinement_loop('build_code', 'Code content')
        loop_id = init_result['loop_id']

        status_before = get_loop_status(loop_id)

        # Simulate loop progression
        reset_loop_state(loop_id)

        status_after = get_loop_status(loop_id)

        assert status_before['loop_id'] == status_after['loop_id']
        assert status_after['status'] == 'reset'

    def test_loop_id_generation_uniqueness(self) -> None:
        loop1 = initialize_refinement_loop('plan', 'Content 1')
        loop2 = initialize_refinement_loop('plan', 'Content 2')

        assert loop1['loop_id'] != loop2['loop_id']
        assert isinstance(loop1['loop_id'], str)
        assert isinstance(loop2['loop_id'], str)
