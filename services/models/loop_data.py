from enum import Enum

from pydantic import BaseModel, Field


class LoopType(Enum):
    PLAN = 'plan'
    SPEC = 'spec'
    BUILD_PLAN = 'build_plan'
    BUILD_CODE = 'build_code'


class LoopData(BaseModel):
    loop_type: LoopType
    current_score: int = Field(ge=0, le=100)
    previous_scores: list[int] = Field(default_factory=list)
    iteration: int = Field(ge=1)

    def calculate_improvement(self) -> int:
        if not self.previous_scores:
            return 0
        return self.current_score - self.previous_scores[-1]

    def is_first_iteration(self) -> bool:
        return self.iteration == 1
