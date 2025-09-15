import re
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from .enums import BuildStatus


class BuildPlan(BaseModel):
    project_name: str
    project_goal: str
    total_duration: str
    team_size: str
    primary_language: str
    framework: str
    database: str
    development_environment: str
    database_schema: str
    api_architecture: str
    frontend_architecture: str
    core_features: str
    integration_points: str
    testing_strategy: str
    code_standards: str
    performance_requirements: str
    security_implementation: str
    build_status: BuildStatus
    creation_date: str
    last_updated: str
    build_owner: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        if '# Build Plan:' not in markdown:
            raise ValueError('Invalid build plan format: missing title')

        sections = {
            'project_goal': r'\*\*Project Goal\*\*:\s*`([^`]+)`',
            'total_duration': r'\*\*Total Duration\*\*:\s*`([^`]+)`',
            'team_size': r'\*\*Team Size\*\*:\s*`([^`]+)`',
            'primary_language': r'\*\*Primary Language\*\*:\s*`([^`]+)`',
            'framework': r'\*\*Framework\*\*:\s*`([^`]+)`',
            'database': r'\*\*Database\*\*:\s*`([^`]+)`',
            'development_environment': r'### Development Environment Setup\s*\n`([^`]+)`',
            'database_schema': r'### Database Schema Design\s*\n`([^`]+)`',
            'api_architecture': r'### API Architecture\s*\n`([^`]+)`',
            'frontend_architecture': r'### Frontend Architecture\s*\n`([^`]+)`',
            'core_features': r'### Core Features Implementation\s*\n`([^`]+)`',
            'integration_points': r'### Integration Points\s*\n`([^`]+)`',
            'testing_strategy': r'### Testing Strategy\s*\n`([^`]+)`',
            'code_standards': r'### Code Standards\s*\n`([^`]+)`',
            'performance_requirements': r'### Performance Requirements\s*\n`([^`]+)`',
            'security_implementation': r'### Security Implementation\s*\n`([^`]+)`',
            'build_status': r'\*\*Status\*\*:\s*`([^`]+)`',
            'creation_date': r'\*\*Created\*\*:\s*`([^`]+)`',
            'last_updated': r'\*\*Last Updated\*\*:\s*`([^`]+)`',
            'build_owner': r'\*\*Owner\*\*:\s*`([^`]+)`',
        }

        name_match = re.search(r'# Build Plan:\s*(.+)', markdown)
        project_name = name_match.group(1).strip() if name_match else 'Unnamed Project'

        extracted: dict[str, str] = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                if field == 'build_status':
                    extracted[field] = 'planning'
                else:
                    extracted[field] = f'{field.replace("_", " ").title()} not specified'

        return cls(
            project_name=project_name,
            project_goal=extracted['project_goal'],
            total_duration=extracted['total_duration'],
            team_size=extracted['team_size'],
            primary_language=extracted['primary_language'],
            framework=extracted['framework'],
            database=extracted['database'],
            development_environment=extracted['development_environment'],
            database_schema=extracted['database_schema'],
            api_architecture=extracted['api_architecture'],
            frontend_architecture=extracted['frontend_architecture'],
            core_features=extracted['core_features'],
            integration_points=extracted['integration_points'],
            testing_strategy=extracted['testing_strategy'],
            code_standards=extracted['code_standards'],
            performance_requirements=extracted['performance_requirements'],
            security_implementation=extracted['security_implementation'],
            build_status=BuildStatus(extracted['build_status']),
            creation_date=extracted['creation_date'],
            last_updated=extracted['last_updated'],
            build_owner=extracted['build_owner'],
        )

    def build_markdown(self) -> str:
        return f"""# Build Plan: {self.project_name}

## Development Overview

**Project Goal**: `{self.project_goal}`
**Total Duration**: `{self.total_duration}`
**Team Size**: `{self.team_size}`

## Technical Foundation

**Primary Language**: `{self.primary_language}`
**Framework**: `{self.framework}`
**Database**: `{self.database}`

## Implementation Plan

### Development Environment Setup
`{self.development_environment}`

### Database Schema Design
`{self.database_schema}`

### API Architecture
`{self.api_architecture}`

### Frontend Architecture
`{self.frontend_architecture}`

### Core Features Implementation
`{self.core_features}`

### Integration Points
`{self.integration_points}`

### Testing Strategy
`{self.testing_strategy}`

## Code Quality

### Code Standards
`{self.code_standards}`

### Performance Requirements
`{self.performance_requirements}`

### Security Implementation
`{self.security_implementation}`

---

**Status**: `{self.build_status.value}`
**Created**: `{self.creation_date}`
**Last Updated**: `{self.last_updated}`
**Owner**: `{self.build_owner}`
"""
