from datetime import datetime
from typing import Self
from uuid import uuid4

from pydantic import Field
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from .base import MCPModel
from .enums import SpecStatus


class InitialSpec(MCPModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    phase_name: str
    objectives: str
    scope: str
    dependencies: str
    deliverables: str
    spec_status: SpecStatus
    creation_date: str
    last_updated: str
    spec_owner: str
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        """Parse using markdown-it-py native list parsing."""
        if '# Technical Specification:' not in markdown:
            raise ValueError('Invalid specification format: missing title')

        md = MarkdownIt('commonmark')
        tree = SyntaxTreeNode(md.parse(markdown))

        fields = {}

        # Extract title
        for node in cls._find_nodes_by_type(tree, 'heading'):
            if node.tag != 'h1':
                continue
            title_text = cls._extract_text_content(node)
            if 'Technical Specification:' not in title_text:
                continue
            fields['phase_name'] = title_text.split(':', 1)[1].strip()
            break

        # Extract all field data from lists
        for item in cls._find_nodes_by_type(tree, 'list_item'):
            text = cls._extract_text_content(item).strip()
            if ':' not in text:
                continue
            field_part, value_part = text.split(':', 1)
            field_name = field_part.strip().lower().replace(' ', '_').replace('-', '_')
            field_value = value_part.strip()

            # Map field names to model field names
            field_mapping = {'status': 'spec_status', 'created': 'creation_date', 'owner': 'spec_owner'}
            model_field_name = field_mapping.get(field_name, field_name)
            fields[model_field_name] = field_value

        # Set defaults for missing fields
        field_defaults = {
            'phase_name': 'Unnamed Spec',
            'objectives': 'Objectives not specified',
            'scope': 'Scope not specified',
            'dependencies': 'Dependencies not specified',
            'deliverables': 'Deliverables not specified',
            'spec_status': 'draft',
            'creation_date': 'Creation Date not specified',
            'last_updated': 'Last Updated not specified',
            'spec_owner': 'Spec Owner not specified',
        }

        for field, default_value in field_defaults.items():
            if field not in fields:
                fields[field] = default_value

        return cls(
            phase_name=fields['phase_name'],
            objectives=fields['objectives'],
            scope=fields['scope'],
            dependencies=fields['dependencies'],
            deliverables=fields['deliverables'],
            spec_status=SpecStatus(fields['spec_status']),
            creation_date=fields['creation_date'],
            last_updated=fields['last_updated'],
            spec_owner=fields['spec_owner'],
        )

    def build_markdown(self) -> str:
        return f"""# Technical Specification: {self.phase_name}
<!-- ID: {self.id} -->

## Overview
- **Objectives**: {self.objectives}
- **Scope**: {self.scope}
- **Dependencies**: {self.dependencies}
- **Deliverables**: {self.deliverables}

## Metadata
- **Status**: {self.spec_status.value}
- **Created**: {self.creation_date}
- **Last Updated**: {self.last_updated}
- **Owner**: {self.spec_owner}
"""
