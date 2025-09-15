import re
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from .enums import RequirementsStatus


class FeatureRequirements(BaseModel):
    project_name: str
    feature_description: str
    problem_statement: str
    target_users: str
    business_value: str
    user_stories: str
    acceptance_criteria: str
    user_experience_goals: str
    functional_requirements: str
    non_functional_requirements: str
    integration_requirements: str
    user_metrics: str
    performance_metrics: str
    technical_metrics: str
    must_have_features: str
    should_have_features: str
    could_have_features: str
    wont_have_features: str
    requirements_status: RequirementsStatus
    creation_date: str
    last_updated: str
    feature_owner: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        if '# Feature Requirements:' not in markdown:
            raise ValueError('Invalid feature requirements format: missing title')

        sections = {
            'feature_description': r'\*\*Feature Description\*\*:\s*`([^`]+)`',
            'problem_statement': r'\*\*Problem Statement\*\*:\s*`([^`]+)`',
            'target_users': r'\*\*Target Users\*\*:\s*`([^`]+)`',
            'business_value': r'\*\*Business Value\*\*:\s*`([^`]+)`',
            'user_stories': r'### User Stories\s*\n`([^`]+)`',
            'acceptance_criteria': r'### Acceptance Criteria\s*\n`([^`]+)`',
            'user_experience_goals': r'### User Experience Goals\s*\n`([^`]+)`',
            'functional_requirements': r'### Functional Requirements\s*\n`([^`]+)`',
            'non_functional_requirements': r'### Non-Functional Requirements\s*\n`([^`]+)`',
            'integration_requirements': r'### Integration Requirements\s*\n`([^`]+)`',
            'user_metrics': r'### User Metrics\s*\n`([^`]+)`',
            'performance_metrics': r'### Performance Metrics\s*\n`([^`]+)`',
            'technical_metrics': r'### Technical Metrics\s*\n`([^`]+)`',
            'must_have_features': r'### Must Have Features\s*\n`([^`]+)`',
            'should_have_features': r'### Should Have Features\s*\n`([^`]+)`',
            'could_have_features': r'### Could Have Features\s*\n`([^`]+)`',
            'wont_have_features': r'### Won\'t Have Features\s*\n`([^`]+)`',
            'requirements_status': r'\*\*Status\*\*:\s*`([^`]+)`',
            'creation_date': r'\*\*Created\*\*:\s*`([^`]+)`',
            'last_updated': r'\*\*Last Updated\*\*:\s*`([^`]+)`',
            'feature_owner': r'\*\*Owner\*\*:\s*`([^`]+)`',
        }

        name_match = re.search(r'# Feature Requirements:\s*(.+)', markdown)
        project_name = name_match.group(1).strip() if name_match else 'Unnamed Project'

        extracted = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                if field == 'requirements_status':
                    extracted[field] = 'draft'
                else:
                    extracted[field] = f'{field.replace("_", " ").title()} not specified'

        return cls(
            project_name=project_name,
            feature_description=extracted['feature_description'],
            problem_statement=extracted['problem_statement'],
            target_users=extracted['target_users'],
            business_value=extracted['business_value'],
            user_stories=extracted['user_stories'],
            acceptance_criteria=extracted['acceptance_criteria'],
            user_experience_goals=extracted['user_experience_goals'],
            functional_requirements=extracted['functional_requirements'],
            non_functional_requirements=extracted['non_functional_requirements'],
            integration_requirements=extracted['integration_requirements'],
            user_metrics=extracted['user_metrics'],
            performance_metrics=extracted['performance_metrics'],
            technical_metrics=extracted['technical_metrics'],
            must_have_features=extracted['must_have_features'],
            should_have_features=extracted['should_have_features'],
            could_have_features=extracted['could_have_features'],
            wont_have_features=extracted['wont_have_features'],
            requirements_status=RequirementsStatus(extracted['requirements_status']),
            creation_date=extracted['creation_date'],
            last_updated=extracted['last_updated'],
            feature_owner=extracted['feature_owner'],
        )

    def build_markdown(self) -> str:
        return f"""# Feature Requirements: {self.project_name}

## Feature Purpose

**Feature Description**: `{self.feature_description}`
**Problem Statement**: `{self.problem_statement}`
**Target Users**: `{self.target_users}`
**Business Value**: `{self.business_value}`

## User Requirements

### User Stories
`{self.user_stories}`

### Acceptance Criteria
`{self.acceptance_criteria}`

### User Experience Goals
`{self.user_experience_goals}`

## Technical Requirements

### Functional Requirements
`{self.functional_requirements}`

### Non-Functional Requirements
`{self.non_functional_requirements}`

### Integration Requirements
`{self.integration_requirements}`

## Success Metrics

### User Metrics
`{self.user_metrics}`

### Performance Metrics
`{self.performance_metrics}`

### Technical Metrics
`{self.technical_metrics}`

## Implementation Scope

### Must Have Features
`{self.must_have_features}`

### Should Have Features
`{self.should_have_features}`

### Could Have Features
`{self.could_have_features}`

### Won't Have Features
`{self.wont_have_features}`

---

**Status**: `{self.requirements_status.value}`
**Created**: `{self.creation_date}`
**Last Updated**: `{self.last_updated}`
**Owner**: `{self.feature_owner}`
"""
