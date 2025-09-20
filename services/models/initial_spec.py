from typing import ClassVar
from uuid import uuid4

from pydantic import Field

from .base import MCPModel
from .enums import SpecStatus


class InitialSpec(MCPModel):
    # Class configuration for MCPModel
    TITLE_PATTERN: ClassVar[str] = '# Technical Specification'
    TITLE_FIELD: ClassVar[str] = 'phase_name'
    HEADER_FIELD_MAPPING: ClassVar[dict[str, tuple[str, ...]]] = {
        'objectives': ('Overview', 'Objectives'),
        'scope': ('Overview', 'Scope'),
        'dependencies': ('Overview', 'Dependencies'),
        'deliverables': ('Overview', 'Deliverables'),
        'spec_status': ('Metadata', 'Status'),
    }
    # Model fields with defaults
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    phase_name: str = 'Unnamed Specification'
    objectives: str = 'Objectives not specified'
    scope: str = 'Scope not specified'
    dependencies: str = 'Dependencies not specified'
    deliverables: str = 'Deliverables not specified'
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

## Metadata

### Status
{self.spec_status.value}
"""
