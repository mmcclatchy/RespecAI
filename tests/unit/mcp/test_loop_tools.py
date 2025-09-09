import pytest


class TestLoopToolsMCP:
    def test_decide_loop_next_action_complete_decision(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        result = decide_loop_next_action(loop_type='plan', current_score=90, previous_scores=[85, 87], iteration=3)

        assert result == 'complete'

    def test_decide_loop_next_action_refine_decision(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        result = decide_loop_next_action(
            loop_type='spec',
            current_score=70,
            previous_scores=[60],  # Good improvement, not stagnating
            iteration=2,
        )

        assert result == 'refine'

    def test_decide_loop_next_action_user_input_decision(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        result = decide_loop_next_action(
            loop_type='build_code', current_score=80, previous_scores=[78, 79], iteration=15
        )

        assert result == 'user-input'

    def test_decide_loop_next_action_parameter_validation(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test invalid loop type
        with pytest.raises(ValueError, match='Invalid loop_type'):
            decide_loop_next_action(loop_type='invalid_type', current_score=80, previous_scores=[], iteration=1)

    def test_decide_loop_next_action_score_validation(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test score below 0
        with pytest.raises(ValueError, match='current_score must be between 0 and 100'):
            decide_loop_next_action(loop_type='plan', current_score=-5, previous_scores=[], iteration=1)

        # Test score above 100
        with pytest.raises(ValueError, match='current_score must be between 0 and 100'):
            decide_loop_next_action(loop_type='plan', current_score=105, previous_scores=[], iteration=1)

    def test_decide_loop_next_action_iteration_validation(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test iteration below 1
        with pytest.raises(ValueError, match='iteration must be >= 1'):
            decide_loop_next_action(loop_type='plan', current_score=80, previous_scores=[], iteration=0)

    def test_decide_loop_next_action_with_max_iterations(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        result = decide_loop_next_action(
            loop_type='plan', current_score=70, previous_scores=[], iteration=5, max_iterations=5
        )

        assert result == 'user-input'

    def test_decide_loop_next_action_configuration_loading(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test that configuration is loaded and used correctly
        result = decide_loop_next_action(
            loop_type='build_plan',
            current_score=80,  # Should be >= default threshold (80)
            previous_scores=[],
            iteration=1,
        )

        assert result == 'complete'

    def test_decide_loop_next_action_integration_with_decision_engine(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test stagnation detection integration
        result = decide_loop_next_action(
            loop_type='spec',
            current_score=75,
            previous_scores=[73, 74],  # Small improvements indicating stagnation
            iteration=5,
        )

        # Should trigger stagnation detection and return user-input
        assert result == 'user-input'

    def test_decide_loop_next_action_error_handling_missing_parameters(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test missing required parameters
        with pytest.raises(TypeError):
            decide_loop_next_action()  # type: ignore[call-arg]

    def test_decide_loop_next_action_return_value_format(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        result = decide_loop_next_action(loop_type='plan', current_score=85, previous_scores=[], iteration=1)

        # Ensure return value is a string
        assert isinstance(result, str)
        # Ensure return value is one of expected actions
        assert result in ['complete', 'refine', 'user-input']

    def test_decide_loop_next_action_previous_scores_validation(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test with invalid previous scores
        with pytest.raises(ValueError, match='All previous_scores must be between 0 and 100'):
            decide_loop_next_action(loop_type='plan', current_score=80, previous_scores=[70, -5, 85], iteration=4)

    def test_decide_loop_next_action_empty_previous_scores(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test with empty previous scores (first iteration)
        result = decide_loop_next_action(loop_type='plan', current_score=70, previous_scores=[], iteration=1)

        # Should return refine since score is below threshold
        assert result == 'refine'
