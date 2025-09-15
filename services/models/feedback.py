from datetime import datetime

from pydantic import BaseModel, Field, computed_field, field_validator

from .enums import CriticAgent, FSSDCriteria


class CriticFeedback(BaseModel):
    session_id: str
    critic_agent: CriticAgent
    iteration: int
    overall_assessment: str
    improvements: list[str]
    fsdd_scores: dict[FSSDCriteria, int]
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('fsdd_scores')
    @classmethod
    def validate_fsdd_score_range(cls, scores: dict[FSSDCriteria, int]) -> dict[FSSDCriteria, int]:
        for _, score in scores.items():
            if not (0 <= score <= 10):
                raise ValueError('FSDD scores must be between 0 and 10')
        return scores

    @computed_field
    def quality_score(self) -> int:
        if not self.fsdd_scores:
            return 0
        avg_score = sum(self.fsdd_scores.values()) / len(self.fsdd_scores)
        return round(avg_score * 10)
