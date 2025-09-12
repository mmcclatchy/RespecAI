from enum import Enum

from services.utils.setting_configs import loop_config


class LoopType(Enum):
    PLAN = 'plan'
    SPEC = 'spec'
    BUILD_PLAN = 'build_plan'
    BUILD_CODE = 'build_code'

    @property
    def threshold(self) -> int:
        return getattr(loop_config, f'{self.value}_threshold')

    @property
    def improvement_threshold(self) -> int:
        return getattr(loop_config, f'{self.value}_improvement_threshold')

    @property
    def max_iterations(self) -> int:
        return getattr(loop_config, f'{self.value}_max_iterations')


class LoopStatus(Enum):
    INITIALIZED = 'initialized'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    USER_INPUT = 'user_input'
    REFINE = 'refine'


class HealthState(Enum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'
