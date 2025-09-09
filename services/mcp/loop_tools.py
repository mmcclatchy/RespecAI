from services.models.loop_data import LoopData, LoopType
from services.models.loop_config import LoopThresholds
from services.decision_engine import decide_next_action


def decide_loop_next_action(
    loop_type: str, current_score: int, previous_scores: list[int], iteration: int, max_iterations: int = 20
) -> str:
    """MCP tool to decide the next action for a refinement loop.

    This is the main MCP tool interface that external agents will call
    to determine whether to continue refining, complete the loop, or
    request user input based on quality scores and iteration count.
    """
    _validate_parameters(loop_type, current_score, previous_scores, iteration)

    config = LoopThresholds()

    loop_data = _build_loop_data(loop_type, current_score, previous_scores, iteration)
    history = _build_history(loop_type, current_score, previous_scores, iteration)

    return decide_next_action(loop_data, config, history, max_iterations)


def _validate_parameters(loop_type: str, current_score: int, previous_scores: list[int], iteration: int) -> None:
    valid_loop_types = {'plan', 'spec', 'build_plan', 'build_code'}
    if loop_type not in valid_loop_types:
        raise ValueError(f'Invalid loop_type: {loop_type}. Must be one of {valid_loop_types}')

    if not (0 <= current_score <= 100):
        raise ValueError('current_score must be between 0 and 100')

    if iteration < 1:
        raise ValueError('iteration must be >= 1')

    for score in previous_scores:
        if not (0 <= score <= 100):
            raise ValueError('All previous_scores must be between 0 and 100')


def _build_loop_data(loop_type: str, current_score: int, previous_scores: list[int], iteration: int) -> LoopData:
    loop_type_enum = LoopType(loop_type.lower())
    return LoopData(
        loop_type=loop_type_enum, current_score=current_score, previous_scores=previous_scores, iteration=iteration
    )


def _build_history(loop_type: str, current_score: int, previous_scores: list[int], iteration: int) -> list[LoopData]:
    loop_type_enum = LoopType(loop_type.lower())
    history = []

    for i, score in enumerate(previous_scores, 1):
        prev_scores = previous_scores[: i - 1] if i > 1 else []
        data = LoopData(loop_type=loop_type_enum, current_score=score, previous_scores=prev_scores, iteration=i)
        history.append(data)

    current_data = LoopData(
        loop_type=loop_type_enum, current_score=current_score, previous_scores=previous_scores, iteration=iteration
    )
    history.append(current_data)

    return history
