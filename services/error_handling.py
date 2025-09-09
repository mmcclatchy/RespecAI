import logging
from typing import Any

from services.models.loop_data import LoopType
from services.models.loop_config import LoopThresholds

logger = logging.getLogger(__name__)


def validate_score_range(score: int, clamp: bool = False) -> int:
    if clamp:
        return max(0, min(100, score))

    if not (0 <= score <= 100):
        raise ValueError('Score must be between 0 and 100')

    return score


def validate_loop_type(loop_type: str) -> LoopType:
    valid_types = {'plan', 'spec', 'build_plan', 'build_code'}

    if not loop_type or loop_type not in valid_types:
        raise ValueError(f'Invalid loop_type: {loop_type}. Must be one of {valid_types}')

    return LoopType(loop_type)


def validate_iteration_count(iteration: int) -> None:
    if iteration < 1:
        raise ValueError('Iteration must be >= 1')


def validate_previous_scores(previous_scores: list[int]) -> None:
    for score in previous_scores:
        if not (0 <= score <= 100):
            raise ValueError('All previous scores must be between 0 and 100')


def safe_load_configuration() -> LoopThresholds:
    try:
        return LoopThresholds()
    except Exception:
        # Fallback to default configuration on any error
        from services.models.loop_config import LoopThresholds as FallbackThresholds

        return FallbackThresholds(
            plan_threshold=85, spec_threshold=85, build_plan_threshold=80, build_code_threshold=95
        )


def handle_parameter_validation_error(error: Exception, parameter_name: str) -> str:
    return f"Parameter '{parameter_name}' validation failed: {str(error)}"


def handle_configuration_loading_error(error: Exception) -> str:
    return f'Configuration loading failed, using defaults: {str(error)}'


def validate_all_parameters(
    loop_type: str, current_score: int, previous_scores: list[int], iteration: int
) -> dict[str, Any]:
    errors = []

    try:
        validated_loop_type = validate_loop_type(loop_type)
    except ValueError:
        errors.append(f'Invalid loop_type: {loop_type}')
        validated_loop_type = None

    try:
        validated_score = validate_score_range(current_score)
    except ValueError:
        errors.append(f'Invalid current_score: {current_score}')
        validated_score = current_score

    try:
        validate_previous_scores(previous_scores)
    except ValueError:
        errors.append('Invalid previous_scores')

    try:
        validate_iteration_count(iteration)
    except ValueError:
        errors.append(f'Invalid iteration: {iteration}')

    if errors:
        raise ValueError(f'Multiple validation errors: {"; ".join(errors)}')

    return {
        'loop_type': validated_loop_type,
        'current_score': validated_score,
        'previous_scores': previous_scores,
        'iteration': iteration,
    }


def graceful_degradation() -> dict[str, Any]:
    return {'plan_threshold': 85, 'spec_threshold': 85, 'build_plan_threshold': 80, 'build_code_threshold': 95}


def log_validation_error(error: Exception, context: dict[str, Any]) -> None:
    logger.warning('Validation error occurred: %s, context: %s', str(error), context)


def check_required_parameters(params: dict[str, Any], required: list[str]) -> None:
    missing = [param for param in required if param not in params]
    if missing:
        raise ValueError(f'Missing required parameter: {missing[0]}')
