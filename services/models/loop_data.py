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
    previous_score: int | None = Field(default=None, ge=0, le=100)
    iteration: int = Field(ge=1)

    def calculate_improvement(self) -> int:
        if self.previous_score is None:
            return 0
        return self.current_score - self.previous_score

    def is_first_iteration(self) -> bool:
        return self.iteration == 1
