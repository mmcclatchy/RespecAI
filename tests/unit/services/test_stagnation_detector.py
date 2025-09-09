from services.models.loop_data import LoopData, LoopType
from services.stagnation_detector import detect_stagnation


def test_detect_stagnation_with_good_improvement() -> None:
    previous_data = LoopData(loop_type=LoopType.PLAN, current_score=70, previous_scores=[60], iteration=2)
    current_data = LoopData(loop_type=LoopType.PLAN, current_score=80, previous_scores=[60, 70], iteration=3)

    result = detect_stagnation([previous_data, current_data], improvement_threshold=5)
    assert result is False


def test_detect_stagnation_with_low_improvement_single_iteration() -> None:
    previous_data = LoopData(loop_type=LoopType.PLAN, current_score=70, previous_scores=[60], iteration=2)
    current_data = LoopData(loop_type=LoopType.PLAN, current_score=72, previous_scores=[60, 70], iteration=3)

    result = detect_stagnation([previous_data, current_data], improvement_threshold=5)
    assert result is False


def test_detect_stagnation_with_two_consecutive_low_improvements() -> None:
    first_data = LoopData(loop_type=LoopType.PLAN, current_score=70, previous_scores=[68], iteration=2)
    second_data = LoopData(loop_type=LoopType.PLAN, current_score=72, previous_scores=[68, 70], iteration=3)

    result = detect_stagnation([first_data, second_data], improvement_threshold=5)
    assert result is True


def test_detect_stagnation_with_negative_improvement() -> None:
    first_data = LoopData(loop_type=LoopType.PLAN, current_score=70, previous_scores=[72], iteration=2)
    second_data = LoopData(loop_type=LoopType.PLAN, current_score=68, previous_scores=[72, 70], iteration=3)

    result = detect_stagnation([first_data, second_data], improvement_threshold=5)
    assert result is True


def test_detect_stagnation_with_first_iteration_only() -> None:
    first_iteration = LoopData(loop_type=LoopType.PLAN, current_score=70, previous_scores=[], iteration=1)

    result = detect_stagnation([first_iteration], improvement_threshold=5)
    assert result is False


def test_detect_stagnation_with_empty_history() -> None:
    result = detect_stagnation([], improvement_threshold=5)
    assert result is False


def test_detect_stagnation_boundary_condition_exactly_at_threshold() -> None:
    first_data = LoopData(loop_type=LoopType.PLAN, current_score=70, previous_scores=[65], iteration=2)
    second_data = LoopData(loop_type=LoopType.PLAN, current_score=75, previous_scores=[65, 70], iteration=3)

    result = detect_stagnation([first_data, second_data], improvement_threshold=5)
    assert result is False


def test_detect_stagnation_mixed_improvements() -> None:
    first_data = LoopData(loop_type=LoopType.PLAN, current_score=72, previous_scores=[70], iteration=2)
    second_data = LoopData(loop_type=LoopType.PLAN, current_score=82, previous_scores=[70, 72], iteration=3)

    result = detect_stagnation([first_data, second_data], improvement_threshold=5)
    assert result is False
