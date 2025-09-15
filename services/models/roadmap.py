import re
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from .enums import RoadmapStatus


class Roadmap(BaseModel):
    project_name: str
    project_goal: str
    total_duration: str
    team_size: str
    roadmap_budget: str
    phase_1_name: str
    phase_1_duration: str
    phase_1_objectives: str
    phase_1_deliverables: str
    phase_1_success_criteria: str
    phase_1_dependencies: str
    phase_1_team: str
    phase_1_technical_focus: str
    phase_2_name: str
    phase_2_duration: str
    phase_2_objectives: str
    phase_2_deliverables: str
    phase_2_success_criteria: str
    phase_2_dependencies: str
    phase_2_team: str
    phase_2_technical_focus: str
    phase_3_name: str
    phase_3_duration: str
    phase_3_objectives: str
    phase_3_deliverables: str
    phase_3_success_criteria: str
    phase_3_dependencies: str
    phase_3_team: str
    phase_3_technical_focus: str
    critical_path_analysis: str
    key_risks: str
    mitigation_plans: str
    buffer_time: str
    development_resources: str
    infrastructure_requirements: str
    external_dependencies: str
    quality_assurance_plan: str
    technical_milestones: str
    business_milestones: str
    quality_gates: str
    performance_targets: str
    roadmap_status: RoadmapStatus
    creation_date: str
    last_updated: str
    phase_count: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        """Parse roadmap_template.md format into structured fields.

        Implements regex parsing for roadmap variable extraction with phase-specific patterns.
        """
        if '# Project Roadmap:' not in markdown:
            raise ValueError('Invalid roadmap format: missing title')

        sections = {
            'project_goal': r'\*\*Project Goal\*\*:\s*`([^`]+)`',
            'total_duration': r'\*\*Total Duration\*\*:\s*`([^`]+)`',
            'team_size': r'\*\*Team Size\*\*:\s*`([^`]+)`',
            'roadmap_budget': r'\*\*Budget\*\*:\s*`([^`]+)`',
            'phase_1_name': r'### Phase 1:\s*(.+?)(?=\n|$)',
            'phase_1_duration': r'### Phase 1:.*?\n\*\*Duration\*\*:\s*`([^`]+)`',
            'phase_1_objectives': r'### Phase 1:.*?\n\*\*Objectives\*\*:\s*`([^`]+)`',
            'phase_1_deliverables': r'### Phase 1:.*?\n\*\*Deliverables\*\*:\s*`([^`]+)`',
            'phase_1_success_criteria': r'### Phase 1:.*?\n\*\*Success Criteria\*\*:\s*`([^`]+)`',
            'phase_1_dependencies': r'### Phase 1:.*?\n\*\*Dependencies\*\*:\s*`([^`]+)`',
            'phase_1_team': r'### Phase 1:.*?\n\*\*Team\*\*:\s*`([^`]+)`',
            'phase_1_technical_focus': r'### Phase 1:.*?\n\*\*Technical Focus\*\*:\s*`([^`]+)`',
            'phase_2_name': r'### Phase 2:\s*(.+?)(?=\n|$)',
            'phase_2_duration': r'### Phase 2:.*?\n\*\*Duration\*\*:\s*`([^`]+)`',
            'phase_2_objectives': r'### Phase 2:.*?\n\*\*Objectives\*\*:\s*`([^`]+)`',
            'phase_2_deliverables': r'### Phase 2:.*?\n\*\*Deliverables\*\*:\s*`([^`]+)`',
            'phase_2_success_criteria': r'### Phase 2:.*?\n\*\*Success Criteria\*\*:\s*`([^`]+)`',
            'phase_2_dependencies': r'### Phase 2:.*?\n\*\*Dependencies\*\*:\s*`([^`]+)`',
            'phase_2_team': r'### Phase 2:.*?\n\*\*Team\*\*:\s*`([^`]+)`',
            'phase_2_technical_focus': r'### Phase 2:.*?\n\*\*Technical Focus\*\*:\s*`([^`]+)`',
            'phase_3_name': r'### Phase 3:\s*(.+?)(?=\n|$)',
            'phase_3_duration': r'### Phase 3:.*?\n\*\*Duration\*\*:\s*`([^`]+)`',
            'phase_3_objectives': r'### Phase 3:.*?\n\*\*Objectives\*\*:\s*`([^`]+)`',
            'phase_3_deliverables': r'### Phase 3:.*?\n\*\*Deliverables\*\*:\s*`([^`]+)`',
            'phase_3_success_criteria': r'### Phase 3:.*?\n\*\*Success Criteria\*\*:\s*`([^`]+)`',
            'phase_3_dependencies': r'### Phase 3:.*?\n\*\*Dependencies\*\*:\s*`([^`]+)`',
            'phase_3_team': r'### Phase 3:.*?\n\*\*Team\*\*:\s*`([^`]+)`',
            'phase_3_technical_focus': r'### Phase 3:.*?\n\*\*Technical Focus\*\*:\s*`([^`]+)`',
            'critical_path_analysis': r'### Critical Path Analysis\s*\n`([^`]+)`',
            'key_risks': r'### Key Risks\s*\n`([^`]+)`',
            'mitigation_plans': r'### Mitigation Plans\s*\n`([^`]+)`',
            'buffer_time': r'### Buffer Time\s*\n`([^`]+)`',
            'development_resources': r'### Development Resources\s*\n`([^`]+)`',
            'infrastructure_requirements': r'### Infrastructure Requirements\s*\n`([^`]+)`',
            'external_dependencies': r'### External Dependencies\s*\n`([^`]+)`',
            'quality_assurance_plan': r'### Quality Assurance\s*\n`([^`]+)`',
            'technical_milestones': r'### Technical Milestones\s*\n`([^`]+)`',
            'business_milestones': r'### Business Milestones\s*\n`([^`]+)`',
            'quality_gates': r'### Quality Gates\s*\n`([^`]+)`',
            'performance_targets': r'### Performance Targets\s*\n`([^`]+)`',
            'roadmap_status': r'\*\*Status\*\*:\s*`([^`]+)`',
            'creation_date': r'\*\*Created\*\*:\s*`([^`]+)`',
            'last_updated': r'\*\*Last Updated\*\*:\s*`([^`]+)`',
            'phase_count': r'\*\*Phase Count\*\*:\s*`([^`]+)`',
        }

        name_match = re.search(r'# Project Roadmap:\s*(.+)', markdown)
        project_name = name_match.group(1).strip() if name_match else 'Unnamed Project'

        extracted = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                if field == 'roadmap_status':
                    extracted[field] = 'draft'
                else:
                    extracted[field] = f'{field.replace("_", " ").title()} not specified'

        return cls(
            project_name=project_name,
            project_goal=extracted['project_goal'],
            total_duration=extracted['total_duration'],
            team_size=extracted['team_size'],
            roadmap_budget=extracted['roadmap_budget'],
            phase_1_name=extracted['phase_1_name'],
            phase_1_duration=extracted['phase_1_duration'],
            phase_1_objectives=extracted['phase_1_objectives'],
            phase_1_deliverables=extracted['phase_1_deliverables'],
            phase_1_success_criteria=extracted['phase_1_success_criteria'],
            phase_1_dependencies=extracted['phase_1_dependencies'],
            phase_1_team=extracted['phase_1_team'],
            phase_1_technical_focus=extracted['phase_1_technical_focus'],
            phase_2_name=extracted['phase_2_name'],
            phase_2_duration=extracted['phase_2_duration'],
            phase_2_objectives=extracted['phase_2_objectives'],
            phase_2_deliverables=extracted['phase_2_deliverables'],
            phase_2_success_criteria=extracted['phase_2_success_criteria'],
            phase_2_dependencies=extracted['phase_2_dependencies'],
            phase_2_team=extracted['phase_2_team'],
            phase_2_technical_focus=extracted['phase_2_technical_focus'],
            phase_3_name=extracted['phase_3_name'],
            phase_3_duration=extracted['phase_3_duration'],
            phase_3_objectives=extracted['phase_3_objectives'],
            phase_3_deliverables=extracted['phase_3_deliverables'],
            phase_3_success_criteria=extracted['phase_3_success_criteria'],
            phase_3_dependencies=extracted['phase_3_dependencies'],
            phase_3_team=extracted['phase_3_team'],
            phase_3_technical_focus=extracted['phase_3_technical_focus'],
            critical_path_analysis=extracted['critical_path_analysis'],
            key_risks=extracted['key_risks'],
            mitigation_plans=extracted['mitigation_plans'],
            buffer_time=extracted['buffer_time'],
            development_resources=extracted['development_resources'],
            infrastructure_requirements=extracted['infrastructure_requirements'],
            external_dependencies=extracted['external_dependencies'],
            quality_assurance_plan=extracted['quality_assurance_plan'],
            technical_milestones=extracted['technical_milestones'],
            business_milestones=extracted['business_milestones'],
            quality_gates=extracted['quality_gates'],
            performance_targets=extracted['performance_targets'],
            roadmap_status=RoadmapStatus(extracted['roadmap_status']),
            creation_date=extracted['creation_date'],
            last_updated=extracted['last_updated'],
            phase_count=extracted['phase_count'],
        )

    def build_markdown(self) -> str:
        return f"""# Project Roadmap: {self.project_name}

## Roadmap Overview

**Project Goal**: `{self.project_goal}`
**Total Duration**: `{self.total_duration}`
**Team Size**: `{self.team_size}`
**Budget**: `{self.roadmap_budget}`

## Phase Breakdown

### Phase 1: {self.phase_1_name}
**Duration**: `{self.phase_1_duration}`
**Objectives**: `{self.phase_1_objectives}`
**Deliverables**: `{self.phase_1_deliverables}`
**Success Criteria**: `{self.phase_1_success_criteria}`
**Dependencies**: `{self.phase_1_dependencies}`
**Team**: `{self.phase_1_team}`
**Technical Focus**: `{self.phase_1_technical_focus}`

### Phase 2: {self.phase_2_name}
**Duration**: `{self.phase_2_duration}`
**Objectives**: `{self.phase_2_objectives}`
**Deliverables**: `{self.phase_2_deliverables}`
**Success Criteria**: `{self.phase_2_success_criteria}`
**Dependencies**: `{self.phase_2_dependencies}`
**Team**: `{self.phase_2_team}`
**Technical Focus**: `{self.phase_2_technical_focus}`

### Phase 3: {self.phase_3_name}
**Duration**: `{self.phase_3_duration}`
**Objectives**: `{self.phase_3_objectives}`
**Deliverables**: `{self.phase_3_deliverables}`
**Success Criteria**: `{self.phase_3_success_criteria}`
**Dependencies**: `{self.phase_3_dependencies}`
**Team**: `{self.phase_3_team}`
**Technical Focus**: `{self.phase_3_technical_focus}`

## Risk Assessment

### Critical Path Analysis
`{self.critical_path_analysis}`

### Key Risks
`{self.key_risks}`

### Mitigation Plans
`{self.mitigation_plans}`

### Buffer Time
`{self.buffer_time}`

## Resource Planning

### Development Resources
`{self.development_resources}`

### Infrastructure Requirements
`{self.infrastructure_requirements}`

### External Dependencies
`{self.external_dependencies}`

### Quality Assurance
`{self.quality_assurance_plan}`

## Success Metrics

### Technical Milestones
`{self.technical_milestones}`

### Business Milestones
`{self.business_milestones}`

### Quality Gates
`{self.quality_gates}`

### Performance Targets
`{self.performance_targets}`

---

**Status**: `{self.roadmap_status.value}`
**Created**: `{self.creation_date}`
**Last Updated**: `{self.last_updated}`
**Phase Count**: `{self.phase_count}`"""
