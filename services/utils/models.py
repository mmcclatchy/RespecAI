import re
import uuid
from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from services.utils.enums import HealthState, LoopStatus, LoopType, OperationStatus
from services.utils.errors import SpecNotFoundError

from services.models.feedback import CriticFeedback


# Import only for type annotations to avoid circular imports
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:


class InitialSpec(BaseModel):
    name: str
    objectives: str
    scope: str
    dependencies: str
    deliverables: str
    architecture: str

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        sections = {
            'objectives': r'## Overview\s*\n.*?\*\*Objectives\*\*:\s*`([^`]+)`',
            'scope': r'\*\*Scope\*\*:\s*`([^`]+)`',
            'dependencies': r'\*\*Dependencies\*\*:\s*`([^`]+)`',
            'deliverables': r'## Expected Deliverables\s*\n(.*?)(?=\n##|\n\*\*|\Z)',
            'architecture': r'## Technical Architecture\s*\n(.*?)(?=\n##|\n\*\*|\Z)',
        }

        # Extract name from title
        name_match = re.search(r'# Technical Specification:\s*(.+)', markdown)
        name = name_match.group(1).strip() if name_match else 'Unnamed Spec'

        # Extract sections using regex
        extracted = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                extracted[field] = f'{field.title()} not specified'

        return cls(name=name, **extracted)

    def build_markdown(self) -> str:
        return f"""# Technical Specification: {self.name}

## Overview

**Objectives**: `{self.objectives}`  
**Scope**: `{self.scope}`  
**Dependencies**: `{self.dependencies}`

## Expected Deliverables

{self.deliverables}

## Technical Architecture  

{self.architecture}

## Quality Gates

- [ ] All objectives met and validated
- [ ] Scope boundaries respected  
- [ ] Dependencies properly integrated
- [ ] Deliverables complete and tested
- [ ] Architecture decisions documented
"""


class RoadMap(BaseModel):
    name: str
    specs: dict[str, InitialSpec] = Field(default_factory=dict)

    def add_spec(self, spec: InitialSpec) -> None:
        self.specs[spec.name] = spec

    def get_spec(self, spec_name: str) -> InitialSpec:
        if spec_name not in self.specs:
            raise SpecNotFoundError(f'Spec not found: {spec_name}')
        return self.specs[spec_name]


class MCPRoadMapResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: LoopStatus
    roadmap: RoadMap


class MCPResponse(BaseModel):
    id: str
    status: LoopStatus
    message: str = ''


class OperationResponse(BaseModel):
    id: str
    status: OperationStatus
    message: str = ''


class LoopState(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    loop_type: LoopType
    status: LoopStatus = LoopStatus.INITIALIZED
    current_score: int = Field(default=0, ge=0, le=100)
    score_history: list[int] = Field(default_factory=list)
    iteration: int = Field(default=1, ge=1)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    feedback_history: list[CriticFeedback] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def mcp_response(self) -> MCPResponse:
        return MCPResponse(id=self.id, status=self.status)

    def is_first_iteration(self) -> bool:
        return self.iteration == 1

    def increment_iteration(self) -> int:
        self.iteration += 1
        return self.iteration

    def add_score(self, score: int) -> None:
        self.score_history.append(score)
        self.current_score = score

    def decide_next_loop_action(self) -> MCPResponse:
        if self.current_score >= self.loop_type.threshold:
            self.status = LoopStatus.COMPLETED
            return self.mcp_response

        if self.iteration >= self.loop_type.max_iterations or self._detect_stagnation():
            self.status = LoopStatus.USER_INPUT
            return self.mcp_response

        self.status = LoopStatus.REFINE
        return self.mcp_response

    def _calculate_improvement(self, scores_ago: int = 1) -> int:
        if not self.score_history:
            return 0
        score_ago_index = scores_ago * -1
        return self.score_history[score_ago_index] - self.score_history[score_ago_index - 1]

    def _detect_stagnation(self) -> bool:
        if len(self.score_history) < 3:
            return False

        threshold = self.loop_type.improvement_threshold
        recent_improvements: list[int] = [
            self._calculate_improvement(2),
            self._calculate_improvement(1),
        ]
        return all(improvement < threshold for improvement in recent_improvements)

    def add_feedback(self, feedback: CriticFeedback) -> None:
        self.feedback_history.append(feedback)
        self.add_score(feedback.quality_score)
        self.updated_at = datetime.now()

        # Update status to indicate loop is active with feedback
        if self.status == LoopStatus.INITIALIZED:
            self.status = LoopStatus.IN_PROGRESS

    def get_recent_feedback(self, count: int = 5) -> list[CriticFeedback]:
        return self.feedback_history[-count:] if self.feedback_history else []


class HealthStatus(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    status: HealthState = HealthState.HEALTHY
    tools_count: int = 0
    error: str | None = None
