import pytest
from unittest.mock import patch

from services.models.loop_data import LoopType
from services.models.loop_config import LoopThresholds


class TestErrorHandling:
    def test_validate_score_range_valid_scores(self) -> None:
        from services.error_handling import validate_score_range

        # Test valid scores
        validate_score_range(50)  # Should not raise
        validate_score_range(0)  # Boundary
        validate_score_range(100)  # Boundary

    def test_validate_score_range_invalid_scores(self) -> None:
        from services.error_handling import validate_score_range

        # Test invalid scores
        with pytest.raises(ValueError, match='Score must be between 0 and 100'):
            validate_score_range(-1)

        with pytest.raises(ValueError, match='Score must be between 0 and 100'):
            validate_score_range(101)

    def test_validate_score_range_with_clamp_option(self) -> None:
        from services.error_handling import validate_score_range

        # Test clamping functionality
        assert validate_score_range(-5, clamp=True) == 0
        assert validate_score_range(105, clamp=True) == 100
        assert validate_score_range(50, clamp=True) == 50

    def test_validate_loop_type_valid_types(self) -> None:
        from services.error_handling import validate_loop_type

        # Test valid loop types
        assert validate_loop_type('plan') == LoopType.PLAN
        assert validate_loop_type('spec') == LoopType.SPEC
        assert validate_loop_type('build_plan') == LoopType.BUILD_PLAN
        assert validate_loop_type('build_code') == LoopType.BUILD_CODE

    def test_validate_loop_type_invalid_types(self) -> None:
        from services.error_handling import validate_loop_type

        # Test invalid loop types
        with pytest.raises(ValueError, match='Invalid loop_type'):
            validate_loop_type('invalid')

        with pytest.raises(ValueError, match='Invalid loop_type'):
            validate_loop_type('')

    def test_validate_iteration_count_valid_values(self) -> None:
        from services.error_handling import validate_iteration_count

        # Test valid iteration counts
        validate_iteration_count(1)  # Should not raise
        validate_iteration_count(5)  # Should not raise
        validate_iteration_count(100)  # Should not raise

    def test_validate_iteration_count_invalid_values(self) -> None:
        from services.error_handling import validate_iteration_count

        # Test invalid iteration counts
        with pytest.raises(ValueError, match='Iteration must be >= 1'):
            validate_iteration_count(0)

        with pytest.raises(ValueError, match='Iteration must be >= 1'):
            validate_iteration_count(-1)

    def test_validate_previous_scores_valid_lists(self) -> None:
        from services.error_handling import validate_previous_scores

        # Test valid score lists
        validate_previous_scores([])  # Empty list
        validate_previous_scores([50, 60, 70])  # Valid scores
        validate_previous_scores([0, 100])  # Boundary values

    def test_validate_previous_scores_invalid_lists(self) -> None:
        from services.error_handling import validate_previous_scores

        # Test invalid score lists
        with pytest.raises(ValueError, match='All previous scores must be between 0 and 100'):
            validate_previous_scores([50, -5, 70])

        with pytest.raises(ValueError, match='All previous scores must be between 0 and 100'):
            validate_previous_scores([50, 105, 70])

    def test_safe_load_configuration_success(self) -> None:
        from services.error_handling import safe_load_configuration

        # Test successful configuration loading
        config = safe_load_configuration()
        assert isinstance(config, LoopThresholds)
        assert hasattr(config, 'plan_threshold')

    def test_safe_load_configuration_fallback_on_error(self) -> None:
        from services.error_handling import safe_load_configuration

        # Test fallback when configuration loading fails
        with patch('services.error_handling.LoopThresholds') as mock_config:
            mock_config.side_effect = Exception('Config loading failed')

            config = safe_load_configuration()

            # Should return default fallback config
            assert isinstance(config, LoopThresholds)

    def test_handle_parameter_validation_error_clear_message(self) -> None:
        from services.error_handling import handle_parameter_validation_error

        # Test parameter validation error handling
        try:
            raise ValueError('Invalid parameter value')
        except ValueError as e:
            error_msg = handle_parameter_validation_error(e, 'test_parameter')
            assert 'test_parameter' in error_msg
            assert 'Invalid parameter value' in error_msg

    def test_handle_configuration_loading_error_graceful_degradation(self) -> None:
        from services.error_handling import handle_configuration_loading_error

        # Test configuration loading error handling
        mock_error = Exception('Database connection failed')
        result = handle_configuration_loading_error(mock_error)

        assert 'configuration' in result.lower()
        assert isinstance(result, str)

    def test_validate_all_parameters_success(self) -> None:
        from services.error_handling import validate_all_parameters

        # Test successful validation of all parameters
        result = validate_all_parameters(loop_type='plan', current_score=75, previous_scores=[60, 70], iteration=3)

        # Should return normalized parameters
        assert result['loop_type'] == LoopType.PLAN
        assert result['current_score'] == 75
        assert result['previous_scores'] == [60, 70]
        assert result['iteration'] == 3

    def test_validate_all_parameters_with_errors(self) -> None:
        from services.error_handling import validate_all_parameters

        # Test parameter validation with multiple errors
        with pytest.raises(ValueError) as exc_info:
            validate_all_parameters(loop_type='invalid', current_score=-5, previous_scores=[60, 105], iteration=0)

        error_msg = str(exc_info.value)
        assert 'validation errors' in error_msg.lower()

    def test_graceful_degradation_scenario(self) -> None:
        from services.error_handling import graceful_degradation

        # Test graceful degradation with fallback values
        with patch('services.models.loop_config.LoopThresholds') as mock_config:
            mock_config.side_effect = Exception('System unavailable')

            result = graceful_degradation()

            # Should return safe default configuration
            assert isinstance(result, dict)
            assert 'plan_threshold' in result
            assert result['plan_threshold'] >= 0

    def test_error_logging_integration(self) -> None:
        from services.error_handling import log_validation_error

        # Test error logging functionality
        with patch('services.error_handling.logger') as mock_logger:
            error = ValueError('Test validation error')
            context = {'parameter': 'loop_type', 'value': 'invalid'}

            log_validation_error(error, context)

            # Verify logging was called with appropriate level
            mock_logger.warning.assert_called_once()
            args, kwargs = mock_logger.warning.call_args
            assert 'validation' in args[0].lower()

    def test_parameter_existence_checking(self) -> None:
        from services.error_handling import check_required_parameters

        # Test required parameter existence checking
        params = {'loop_type': 'plan', 'current_score': 75, 'iteration': 1}
        required = ['loop_type', 'current_score', 'previous_scores', 'iteration']

        with pytest.raises(ValueError, match='Missing required parameter'):
            check_required_parameters(params, required)

    def test_parameter_existence_checking_success(self) -> None:
        from services.error_handling import check_required_parameters

        # Test successful parameter existence checking
        params = {'loop_type': 'plan', 'current_score': 75, 'previous_scores': [], 'iteration': 1}
        required = ['loop_type', 'current_score', 'previous_scores', 'iteration']

        # Should not raise any exception
        check_required_parameters(params, required)
