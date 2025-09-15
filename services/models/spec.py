import re
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from .enums import SpecStatus


class TechnicalSpec(BaseModel):
    phase_name: str
    objectives: str
    scope: str
    dependencies: str
    deliverables: str
    architecture: str
    technology_stack: str
    functional_requirements: str
    non_functional_requirements: str
    development_plan: str
    testing_strategy: str
    research_requirements: str
    success_criteria: str
    integration_context: str
    spec_status: SpecStatus
    phase_number: str
    total_phases: str
    creation_date: str
    last_updated: str
    spec_owner: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        if '# Technical Specification:' not in markdown:
            raise ValueError('Invalid specification format: missing title')

        sections = {
            'objectives': r'\*\*Objectives\*\*:\s*`([^`]+)`',
            'scope': r'\*\*Scope\*\*:\s*`([^`]+)`',
            'dependencies': r'\*\*Dependencies\*\*:\s*`([^`]+)`',
            'deliverables': r'## Deliverables\s*\n`([^`]+)`',
            'architecture': r'### Architecture\s*\n`([^`]+)`',
            'technology_stack': r'### Technology Stack\s*\n`([^`]+)`',
            'functional_requirements': r'### Functional Requirements\s*\n`([^`]+)`',
            'non_functional_requirements': r'### Non-Functional Requirements\s*\n`([^`]+)`',
            'development_plan': r'### Development Plan\s*\n`([^`]+)`',
            'testing_strategy': r'### Testing Strategy\s*\n`([^`]+)`',
            'research_requirements': r'## Research Requirements\s*\n`([^`]+)`',
            'success_criteria': r'## Success Criteria\s*\n`([^`]+)`',
            'integration_context': r'## Integration\s*\n`([^`]+)`',
            'spec_status': r'\*\*Status\*\*:\s*`([^`]+)`',
            'phase_number': r'\*\*Phase\*\*:\s*`([^`]+)` of',
            'total_phases': r'of `([^`]+)`',
            'creation_date': r'\*\*Created\*\*:\s*`([^`]+)`',
            'last_updated': r'\*\*Last Updated\*\*:\s*`([^`]+)`',
            'spec_owner': r'\*\*Owner\*\*:\s*`([^`]+)`',
        }

        name_match = re.search(r'# Technical Specification:\s*(.+)', markdown)
        phase_name = name_match.group(1).strip() if name_match else 'Unnamed Spec'

        extracted = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                if field == 'spec_status':
                    extracted[field] = 'draft'
                else:
                    extracted[field] = f'{field.replace("_", " ").title()} not specified'

        return cls(
            phase_name=phase_name,
            objectives=extracted['objectives'],
            scope=extracted['scope'],
            dependencies=extracted['dependencies'],
            deliverables=extracted['deliverables'],
            architecture=extracted['architecture'],
            technology_stack=extracted['technology_stack'],
            functional_requirements=extracted['functional_requirements'],
            non_functional_requirements=extracted['non_functional_requirements'],
            development_plan=extracted['development_plan'],
            testing_strategy=extracted['testing_strategy'],
            research_requirements=extracted['research_requirements'],
            success_criteria=extracted['success_criteria'],
            integration_context=extracted['integration_context'],
            spec_status=SpecStatus(extracted['spec_status']),
            phase_number=extracted['phase_number'],
            total_phases=extracted['total_phases'],
            creation_date=extracted['creation_date'],
            last_updated=extracted['last_updated'],
            spec_owner=extracted['spec_owner'],
        )

    def build_markdown(self) -> str:
        return f"""# Technical Specification: {self.phase_name}

## Overview
**Objectives**: `{self.objectives}`
**Scope**: `{self.scope}`
**Dependencies**: `{self.dependencies}`

## Deliverables
`{self.deliverables}`

## System Design

### Architecture
`{self.architecture}`

### Technology Stack
`{self.technology_stack}`

## Implementation

### Functional Requirements
`{self.functional_requirements}`

### Non-Functional Requirements
`{self.non_functional_requirements}`

### Development Plan
`{self.development_plan}`

### Testing Strategy
`{self.testing_strategy}`

## Research Requirements
`{self.research_requirements}`

## Success Criteria
`{self.success_criteria}`

## Integration
`{self.integration_context}`

---

**Status**: `{self.spec_status.value}`
**Phase**: `{self.phase_number}` of `{self.total_phases}`
**Created**: `{self.creation_date}`
**Last Updated**: `{self.last_updated}`
**Owner**: `{self.spec_owner}`
"""
