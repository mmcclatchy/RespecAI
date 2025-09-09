from services.models.loop_data import LoopData


def detect_stagnation(history: list[LoopData], improvement_threshold: int) -> bool:
    if len(history) < 2:
        return False

    recent_improvements = []
    for data in history[-2:]:
        improvement = data.calculate_improvement()
        recent_improvements.append(improvement)

    consecutive_low_improvements = 0
    for improvement in recent_improvements:
        if improvement < improvement_threshold:
            consecutive_low_improvements += 1
        else:
            consecutive_low_improvements = 0

    return consecutive_low_improvements >= 2
