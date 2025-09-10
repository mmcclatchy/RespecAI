import uuid
from datetime import datetime
from services.models.loop_data import LoopData, LoopType
from services.models.loop_config import LoopThresholds
from services.decision_engine import decide_next_action


_active_loops: dict[str, dict] = {}


def initialize_refinement_loop(loop_type: str, initial_content: str) -> dict:
    valid_loop_types = {'plan', 'spec', 'build_plan', 'build_code'}
    if loop_type not in valid_loop_types:
        raise ValueError(f'Invalid loop_type: {loop_type}. Must be one of {valid_loop_types}')

    if not initial_content.strip():
        raise ValueError('initial_content cannot be empty')

    loop_id = str(uuid.uuid4())

    _active_loops[loop_id] = {
        'loop_id': loop_id,
        'loop_type': loop_type,
        'status': 'initialized',
        'iteration_count': 0,
        'score_history': [],
        'created_at': datetime.now().isoformat(),
        'initial_content': initial_content,
    }

    return {'loop_id': loop_id, 'status': 'initialized'}


def reset_loop_state(loop_id: str) -> dict:
    if loop_id not in _active_loops:
        raise ValueError(f'Loop not found: {loop_id}')

    _active_loops[loop_id]['status'] = 'reset'
    _active_loops[loop_id]['iteration_count'] = 0
    _active_loops[loop_id]['score_history'] = []

    return {'loop_id': loop_id, 'status': 'reset'}


def get_loop_status(loop_id: str) -> dict:
    if loop_id not in _active_loops:
        raise ValueError(f'Loop not found: {loop_id}')

    return _active_loops[loop_id].copy()


def list_active_loops() -> list[dict]:
    return list(_active_loops.values())


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
