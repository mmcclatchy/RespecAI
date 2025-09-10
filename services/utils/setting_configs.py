from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LoopConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra='forbid',
        env_prefix='FSDD_LOOP_',
    )

    plan_threshold: int = Field(default=85, ge=1, le=100)
    spec_threshold: int = Field(default=85, ge=1, le=100)
    build_plan_threshold: int = Field(default=80, ge=1, le=100)
    build_code_threshold: int = Field(default=95, ge=1, le=100)

    plan_max_iterations: int = Field(default=5, ge=1, le=20)
    spec_max_iterations: int = Field(default=5, ge=1, le=20)
    build_plan_max_iterations: int = Field(default=5, ge=1, le=20)
    build_code_max_iterations: int = Field(default=5, ge=1, le=20)


class MCPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='forbid',
        env_prefix='FSDD_MCP_',
    )

    server_name: str = 'Loop Management Server'
    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = False


loop_config = LoopConfig()
mcp_settings = MCPSettings()
