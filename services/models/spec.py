from typing import ClassVar
from uuid import uuid4

from pydantic import Field

from .base import MCPModel
from .enums import SpecStatus


class TechnicalSpec(MCPModel):
    # Class configuration for MCPModel
    TITLE_PATTERN: ClassVar[str] = '# Technical Specification'
    TITLE_FIELD: ClassVar[str] = 'phase_name'
    HEADER_FIELD_MAPPING: ClassVar[dict[str, tuple[str, ...]]] = {
        'objectives': ('Overview', 'Objectives'),
        'scope': ('Overview', 'Scope'),
        'dependencies': ('Overview', 'Dependencies'),
        'deliverables': ('Overview', 'Deliverables'),
        'architecture': ('System Design', 'Architecture'),
        'technology_stack': ('System Design', 'Technology Stack'),
        'functional_requirements': ('Implementation', 'Functional Requirements'),
        'non_functional_requirements': ('Implementation', 'Non-Functional Requirements'),
        'development_plan': ('Implementation', 'Development Plan'),
        'testing_strategy': ('Implementation', 'Testing Strategy'),
        'research_requirements': ('Additional Details', 'Research Requirements'),
        'success_criteria': ('Additional Details', 'Success Criteria'),
        'integration_context': ('Additional Details', 'Integration Context'),
        'spec_status': ('Metadata', 'Status'),
    }

    # Model fields with defaults
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    initial_spec_id: str | None = None
    phase_name: str = 'Unnamed Specification'
    objectives: str = 'Objectives not specified'
    scope: str = 'Scope not specified'
    dependencies: str = 'Dependencies not specified'
    deliverables: str = 'Deliverables not specified'
    architecture: str = 'Architecture not specified'
    technology_stack: str = 'Technology Stack not specified'
    functional_requirements: str = 'Functional Requirements not specified'
    non_functional_requirements: str = 'Non-Functional Requirements not specified'
    development_plan: str = 'Development Plan not specified'
    testing_strategy: str = 'Testing Strategy not specified'
    research_requirements: str = 'Research Requirements not specified'
    success_criteria: str = 'Success Criteria not specified'
    integration_context: str = 'Integration Context not specified'
    spec_status: SpecStatus = SpecStatus.DRAFT

    def build_markdown(self) -> str:
        return f"""{self.TITLE_PATTERN}: {self.phase_name}

## Overview

### Objectives
{self.objectives}

### Scope
{self.scope}

### Dependencies
{self.dependencies}

### Deliverables
{self.deliverables}

## System Design

### Architecture
{self.architecture}

### Technology Stack
{self.technology_stack}

## Implementation

### Functional Requirements
{self.functional_requirements}

### Non-Functional Requirements
{self.non_functional_requirements}

### Development Plan
{self.development_plan}

### Testing Strategy
{self.testing_strategy}

## Additional Details

### Research Requirements
{self.research_requirements}

### Success Criteria
{self.success_criteria}

### Integration Context
{self.integration_context}

## Metadata

### Status
{self.spec_status.value}
"""
