from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoopThresholds(BaseSettings):
    model_config = SettingsConfigDict(
        extra='forbid',
        validate_assignment=True,
    )
    plan_threshold: int = Field(default=85, ge=1, le=100)
    spec_threshold: int = Field(default=85, ge=1, le=100)
    build_plan_threshold: int = Field(default=80, ge=1, le=100)
    build_code_threshold: int = Field(default=95, ge=1, le=100)


loop_thresholds = LoopThresholds()
