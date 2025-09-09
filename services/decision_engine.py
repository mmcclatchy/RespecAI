from services.models.loop_data import LoopData, LoopType
from services.models.loop_config import LoopThresholds
from services.stagnation_detector import detect_stagnation


def decide_next_action(
    data: LoopData, config: LoopThresholds, history: list[LoopData], max_iterations: int = 20
) -> str:
    threshold = _get_threshold_for_loop_type(data.loop_type, config)

    if data.current_score >= threshold:
        return 'complete'

    if data.iteration >= max_iterations:
        return 'user-input'

    if detect_stagnation(history, improvement_threshold=5):
        return 'user-input'

    return 'refine'


def _get_threshold_for_loop_type(loop_type: LoopType, config: LoopThresholds) -> int:
    threshold_mapping = {
        LoopType.PLAN: config.plan_threshold,
        LoopType.SPEC: config.spec_threshold,
        LoopType.BUILD_PLAN: config.build_plan_threshold,
        LoopType.BUILD_CODE: config.build_code_threshold,
    }
    return threshold_mapping[loop_type]
