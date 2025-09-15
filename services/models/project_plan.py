import re
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from .enums import ProjectStatus


class ProjectPlan(BaseModel):
    project_name: str
    project_vision: str
    project_mission: str
    project_timeline: str
    project_budget: str
    primary_objectives: str
    success_metrics: str
    key_performance_indicators: str
    included_features: str
    excluded_features: str
    project_assumptions: str
    project_constraints: str
    project_sponsor: str
    key_stakeholders: str
    end_users: str
    work_breakdown: str
    phases_overview: str
    project_dependencies: str
    team_structure: str
    technology_requirements: str
    infrastructure_needs: str
    identified_risks: str
    mitigation_strategies: str
    contingency_plans: str
    quality_standards: str
    testing_strategy: str
    acceptance_criteria: str
    reporting_structure: str
    meeting_schedule: str
    documentation_standards: str
    project_status: ProjectStatus
    creation_date: str
    last_updated: str
    version: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        if '# Project Plan:' not in markdown:
            raise ValueError('Invalid project plan format: missing title')

        sections = {
            'project_vision': r'\*\*Vision\*\*:\s*`([^`]+)`',
            'project_mission': r'\*\*Mission\*\*:\s*`([^`]+)`',
            'project_timeline': r'\*\*Timeline\*\*:\s*`([^`]+)`',
            'project_budget': r'\*\*Budget\*\*:\s*`([^`]+)`',
            'primary_objectives': r'### Primary Objectives\s*\n`([^`]+)`',
            'success_metrics': r'### Success Metrics\s*\n`([^`]+)`',
            'key_performance_indicators': r'### Key Performance Indicators\s*\n`([^`]+)`',
            'included_features': r'### Included Features\s*\n`([^`]+)`',
            'excluded_features': r'### Excluded Features\s*\n`([^`]+)`',
            'project_assumptions': r'### Assumptions\s*\n`([^`]+)`',
            'project_constraints': r'### Constraints\s*\n`([^`]+)`',
            'project_sponsor': r'### Project Sponsor\s*\n`([^`]+)`',
            'key_stakeholders': r'### Key Stakeholders\s*\n`([^`]+)`',
            'end_users': r'### End Users\s*\n`([^`]+)`',
            'work_breakdown': r'### Work Breakdown\s*\n`([^`]+)`',
            'phases_overview': r'### Phases Overview\s*\n`([^`]+)`',
            'project_dependencies': r'### Dependencies\s*\n`([^`]+)`',
            'team_structure': r'### Team Structure\s*\n`([^`]+)`',
            'technology_requirements': r'### Technology Stack\s*\n`([^`]+)`',
            'infrastructure_needs': r'### Infrastructure Needs\s*\n`([^`]+)`',
            'identified_risks': r'### Identified Risks\s*\n`([^`]+)`',
            'mitigation_strategies': r'### Mitigation Strategies\s*\n`([^`]+)`',
            'contingency_plans': r'### Contingency Plans\s*\n`([^`]+)`',
            'quality_standards': r'### Quality Standards\s*\n`([^`]+)`',
            'testing_strategy': r'### Testing Strategy\s*\n`([^`]+)`',
            'acceptance_criteria': r'### Acceptance Criteria\s*\n`([^`]+)`',
            'reporting_structure': r'### Reporting Structure\s*\n`([^`]+)`',
            'meeting_schedule': r'### Meeting Schedule\s*\n`([^`]+)`',
            'documentation_standards': r'### Documentation Standards\s*\n`([^`]+)`',
            'project_status': r'\*\*Status\*\*:\s*`([^`]+)`',
            'creation_date': r'\*\*Created\*\*:\s*`([^`]+)`',
            'last_updated': r'\*\*Last Updated\*\*:\s*`([^`]+)`',
            'version': r'\*\*Version\*\*:\s*`([^`]+)`',
        }

        # Extract project name from title
        name_match = re.search(r'# Project Plan:\s*(.+)', markdown)
        project_name = name_match.group(1).strip() if name_match else 'Unnamed Project'

        # Extract sections using regex
        extracted = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                if field == 'project_status':
                    extracted[field] = 'draft'
                else:
                    extracted[field] = f'{field.replace("_", " ").title()} not specified'

        return cls(
            project_name=project_name,
            project_vision=extracted['project_vision'],
            project_mission=extracted['project_mission'],
            project_timeline=extracted['project_timeline'],
            project_budget=extracted['project_budget'],
            primary_objectives=extracted['primary_objectives'],
            success_metrics=extracted['success_metrics'],
            key_performance_indicators=extracted['key_performance_indicators'],
            included_features=extracted['included_features'],
            excluded_features=extracted['excluded_features'],
            project_assumptions=extracted['project_assumptions'],
            project_constraints=extracted['project_constraints'],
            project_sponsor=extracted['project_sponsor'],
            key_stakeholders=extracted['key_stakeholders'],
            end_users=extracted['end_users'],
            work_breakdown=extracted['work_breakdown'],
            phases_overview=extracted['phases_overview'],
            project_dependencies=extracted['project_dependencies'],
            team_structure=extracted['team_structure'],
            technology_requirements=extracted['technology_requirements'],
            infrastructure_needs=extracted['infrastructure_needs'],
            identified_risks=extracted['identified_risks'],
            mitigation_strategies=extracted['mitigation_strategies'],
            contingency_plans=extracted['contingency_plans'],
            quality_standards=extracted['quality_standards'],
            testing_strategy=extracted['testing_strategy'],
            acceptance_criteria=extracted['acceptance_criteria'],
            reporting_structure=extracted['reporting_structure'],
            meeting_schedule=extracted['meeting_schedule'],
            documentation_standards=extracted['documentation_standards'],
            project_status=ProjectStatus(extracted['project_status']),
            creation_date=extracted['creation_date'],
            last_updated=extracted['last_updated'],
            version=extracted['version'],
        )

    def build_markdown(self) -> str:
        return f"""# Project Plan: {self.project_name}

## Executive Summary

**Vision**: `{self.project_vision}`
**Mission**: `{self.project_mission}`
**Timeline**: `{self.project_timeline}`
**Budget**: `{self.project_budget}`

## Business Objectives

### Primary Objectives
`{self.primary_objectives}`

### Success Metrics
`{self.success_metrics}`

### Key Performance Indicators
`{self.key_performance_indicators}`

## Project Scope

### Included Features
`{self.included_features}`

### Excluded Features
`{self.excluded_features}`

### Assumptions
`{self.project_assumptions}`

### Constraints
`{self.project_constraints}`

## Stakeholders

### Project Sponsor
`{self.project_sponsor}`

### Key Stakeholders
`{self.key_stakeholders}`

### End Users
`{self.end_users}`

## Project Structure

### Work Breakdown
`{self.work_breakdown}`

### Phases Overview
`{self.phases_overview}`

### Dependencies
`{self.project_dependencies}`

## Resource Requirements

### Team Structure
`{self.team_structure}`

### Technology Stack
`{self.technology_requirements}`

### Infrastructure Needs
`{self.infrastructure_needs}`

## Risk Management

### Identified Risks
`{self.identified_risks}`

### Mitigation Strategies
`{self.mitigation_strategies}`

### Contingency Plans
`{self.contingency_plans}`

## Quality Assurance

### Quality Standards
`{self.quality_standards}`

### Testing Strategy
`{self.testing_strategy}`

### Acceptance Criteria
`{self.acceptance_criteria}`

## Communication Plan

### Reporting Structure
`{self.reporting_structure}`

### Meeting Schedule
`{self.meeting_schedule}`

### Documentation Standards
`{self.documentation_standards}`

---

**Status**: `{self.project_status.value}`
**Created**: `{self.creation_date}`
**Last Updated**: `{self.last_updated}`
**Version**: `{self.version}`"""
