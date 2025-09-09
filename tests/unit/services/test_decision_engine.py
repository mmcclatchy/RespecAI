from services.models.loop_data import LoopData, LoopType
from services.models.loop_config import LoopThresholds
from services.decision_engine import decide_next_action


class TestDecisionEngine:
    def test_complete_decision_when_score_meets_threshold(self) -> None:
        data = LoopData(loop_type=LoopType.PLAN, current_score=90, iteration=3)
        config = LoopThresholds(plan_threshold=85)
        history = [data]

        result = decide_next_action(data, config, history)
        assert result == 'complete'

    def test_complete_decision_when_score_equals_threshold(self) -> None:
        data = LoopData(loop_type=LoopType.SPEC, current_score=85, iteration=2)
        config = LoopThresholds(spec_threshold=85)
        history = [data]

        result = decide_next_action(data, config, history)
        assert result == 'complete'

    def test_refine_decision_when_score_below_threshold_improving(self) -> None:
        previous_data = LoopData(loop_type=LoopType.BUILD_PLAN, current_score=70, iteration=1)
        current_data = LoopData(loop_type=LoopType.BUILD_PLAN, current_score=75, previous_scores=[70], iteration=2)
        config = LoopThresholds(build_plan_threshold=80)
        history = [previous_data, current_data]

        result = decide_next_action(current_data, config, history)
        assert result == 'refine'

    def test_user_input_decision_when_stagnation_detected(self) -> None:
        data1 = LoopData(loop_type=LoopType.BUILD_CODE, current_score=80, iteration=1)
        data2 = LoopData(loop_type=LoopType.BUILD_CODE, current_score=82, previous_scores=[80], iteration=2)
        data3 = LoopData(loop_type=LoopType.BUILD_CODE, current_score=83, previous_scores=[80, 82], iteration=3)
        config = LoopThresholds(build_code_threshold=95)
        history = [data1, data2, data3]

        result = decide_next_action(data3, config, history)
        assert result == 'user-input'

    def test_user_input_decision_when_max_iterations_reached(self) -> None:
        data = LoopData(loop_type=LoopType.PLAN, current_score=75, iteration=10)
        config = LoopThresholds(plan_threshold=85)
        history = [data]

        result = decide_next_action(data, config, history, max_iterations=10)
        assert result == 'user-input'

    def test_refine_decision_when_max_iterations_not_reached(self) -> None:
        data = LoopData(loop_type=LoopType.SPEC, current_score=70, iteration=5)
        config = LoopThresholds(spec_threshold=85)
        history = [data]

        result = decide_next_action(data, config, history, max_iterations=10)
        assert result == 'refine'

    def test_threshold_lookup_for_different_loop_types(self) -> None:
        config = LoopThresholds(plan_threshold=85, spec_threshold=90, build_plan_threshold=75, build_code_threshold=95)

        plan_data = LoopData(loop_type=LoopType.PLAN, current_score=85, iteration=1)
        spec_data = LoopData(loop_type=LoopType.SPEC, current_score=90, iteration=1)
        build_plan_data = LoopData(loop_type=LoopType.BUILD_PLAN, current_score=75, iteration=1)
        build_code_data = LoopData(loop_type=LoopType.BUILD_CODE, current_score=95, iteration=1)

        assert decide_next_action(plan_data, config, [plan_data]) == 'complete'
        assert decide_next_action(spec_data, config, [spec_data]) == 'complete'
        assert decide_next_action(build_plan_data, config, [build_plan_data]) == 'complete'
        assert decide_next_action(build_code_data, config, [build_code_data]) == 'complete'

    def test_decision_path_combinations(self) -> None:
        config = LoopThresholds(plan_threshold=85)

        # High score -> complete
        high_score_data = LoopData(loop_type=LoopType.PLAN, current_score=90, iteration=2)
        assert decide_next_action(high_score_data, config, [high_score_data]) == 'complete'

        # Low score, first iteration -> refine
        first_iter_data = LoopData(loop_type=LoopType.PLAN, current_score=70, iteration=1)
        assert decide_next_action(first_iter_data, config, [first_iter_data]) == 'refine'

        # Max iterations -> user-input
        max_iter_data = LoopData(loop_type=LoopType.PLAN, current_score=70, iteration=15)
        assert decide_next_action(max_iter_data, config, [max_iter_data], max_iterations=15) == 'user-input'
