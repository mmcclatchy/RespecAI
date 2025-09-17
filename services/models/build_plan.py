from datetime import datetime
from typing import Self

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from pydantic import Field

from .base import MCPModel
from .enums import BuildStatus


class BuildPlan(MCPModel):
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

        md = MarkdownIt('commonmark')
        tree = SyntaxTreeNode(md.parse(markdown))

        fields = {}

        # Extract title
        for node in cls._find_nodes_by_type(tree, 'heading'):
            if node.tag != 'h1':
                continue
            title_text = cls._extract_text_content(node)
            if 'Build Plan:' not in title_text:
                continue
            fields['project_name'] = title_text.split(':', 1)[1].strip()
            break

        # Extract content by header paths
        header_path_mapping = {
            'project_goal': ['Project Overview', 'Goal'],
            'total_duration': ['Project Overview', 'Duration'],
            'team_size': ['Project Overview', 'Team Size'],
            'primary_language': ['Technology Stack', 'Primary Language'],
            'framework': ['Technology Stack', 'Framework'],
            'database': ['Technology Stack', 'Database'],
            'development_environment': ['Architecture', 'Development Environment'],
            'database_schema': ['Architecture', 'Database Schema'],
            'api_architecture': ['Architecture', 'API Architecture'],
            'frontend_architecture': ['Architecture', 'Frontend Architecture'],
            'core_features': ['Implementation', 'Core Features'],
            'integration_points': ['Implementation', 'Integration Points'],
            'testing_strategy': ['Quality Management', 'Testing Strategy'],
            'code_standards': ['Quality Management', 'Code Standards'],
            'performance_requirements': ['Quality Management', 'Performance Requirements'],
            'security_implementation': ['Quality Management', 'Security Implementation'],
        }

        for field_name, header_path in header_path_mapping.items():
            content = cls._extract_content_by_header_path(tree, header_path)
            if content:
                fields[field_name] = content

        # Handle metadata section separately
        for item in cls._find_nodes_by_type(tree, 'list_item'):
            text = cls._extract_text_content(item).strip()
            if ':' not in text:
                continue
            field_part, value_part = text.split(':', 1)
            field_name = field_part.strip().lower().replace(' ', '_').replace('-', '_')
            field_value = value_part.strip()

            field_mapping = {'status': 'build_status', 'created': 'creation_date', 'owner': 'build_owner'}
            model_field_name = field_mapping.get(field_name, field_name)
            fields[model_field_name] = field_value

        # Set defaults for missing fields
        field_defaults = {
            'project_name': 'Unnamed Project',
            'project_goal': 'Project Goal not specified',
            'total_duration': 'Total Duration not specified',
            'team_size': 'Team Size not specified',
            'primary_language': 'Primary Language not specified',
            'framework': 'Framework not specified',
            'database': 'Database not specified',
            'development_environment': 'Development Environment not specified',
            'database_schema': 'Database Schema not specified',
            'api_architecture': 'Api Architecture not specified',
            'frontend_architecture': 'Frontend Architecture not specified',
            'core_features': 'Core Features not specified',
            'integration_points': 'Integration Points not specified',
            'testing_strategy': 'Testing Strategy not specified',
            'code_standards': 'Code Standards not specified',
            'performance_requirements': 'Performance Requirements not specified',
            'security_implementation': 'Security Implementation not specified',
            'build_status': 'planning',
            'creation_date': 'Creation Date not specified',
            'last_updated': 'Last Updated not specified',
            'build_owner': 'Build Owner not specified',
        }

        for field, default_value in field_defaults.items():
            if field not in fields:
                fields[field] = default_value

        return cls(
            project_name=fields['project_name'],
            project_goal=fields['project_goal'],
            total_duration=fields['total_duration'],
            team_size=fields['team_size'],
            primary_language=fields['primary_language'],
            framework=fields['framework'],
            database=fields['database'],
            development_environment=fields['development_environment'],
            database_schema=fields['database_schema'],
            api_architecture=fields['api_architecture'],
            frontend_architecture=fields['frontend_architecture'],
            core_features=fields['core_features'],
            integration_points=fields['integration_points'],
            testing_strategy=fields['testing_strategy'],
            code_standards=fields['code_standards'],
            performance_requirements=fields['performance_requirements'],
            security_implementation=fields['security_implementation'],
            build_status=BuildStatus(fields['build_status']),
            creation_date=fields['creation_date'],
            last_updated=fields['last_updated'],
            build_owner=fields['build_owner'],
        )

    def build_markdown(self) -> str:
        return f"""# Build Plan: {self.project_name}

## Project Overview

### Goal
{self.project_goal}

### Duration
{self.total_duration}

### Team Size
{self.team_size}

## Technology Stack

### Primary Language
{self.primary_language}

### Framework
{self.framework}

### Database
{self.database}

## Architecture

### Development Environment
{self.development_environment}

### Database Schema
{self.database_schema}

### API Architecture
{self.api_architecture}

### Frontend Architecture
{self.frontend_architecture}

## Implementation

### Core Features
{self.core_features}

### Integration Points
{self.integration_points}

## Quality Management

### Testing Strategy
{self.testing_strategy}

### Code Standards
{self.code_standards}

### Performance Requirements
{self.performance_requirements}

### Security Implementation
{self.security_implementation}

## Metadata
- **Status**: {self.build_status.value}
- **Created**: {self.creation_date}
- **Last Updated**: {self.last_updated}
- **Owner**: {self.build_owner}
"""
