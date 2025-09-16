from datetime import datetime
from typing import Self
from uuid import uuid4

from pydantic import BaseModel, Field
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from .enums import SpecStatus


class PartialSpec(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    initial_spec_id: str
    phase_name: str
    objectives: str = ''
    scope: str = ''
    dependencies: str = ''
    deliverables: str = ''
    architecture: str = ''
    technology_stack: str = ''
    functional_requirements: str = ''
    non_functional_requirements: str = ''
    development_plan: str = ''
    testing_strategy: str = ''
    research_requirements: str = ''
    success_criteria: str = ''
    integration_context: str = ''
    spec_status: SpecStatus
    phase_number: str = '1'
    total_phases: str = '1'
    creation_date: str = ''
    last_updated: str = ''
    spec_owner: str = ''
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def _find_nodes_by_type(cls, node: SyntaxTreeNode, node_type: str) -> list[SyntaxTreeNode]:
        """Recursively find all nodes of a specific type in the tree."""
        nodes = []

        if node.type == node_type:
            nodes.append(node)

        if hasattr(node, 'children') and node.children:
            for child in node.children:
                nodes.extend(cls._find_nodes_by_type(child, node_type))

        return nodes

    @classmethod
    def _extract_text_content(cls, node: SyntaxTreeNode) -> str:
        """Recursively extract all text content from a node."""
        if not hasattr(node, 'children') or not node.children:
            return getattr(node, 'content', '')

        return ' '.join(cls._extract_text_content(child) for child in node.children)

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        """Parse using markdown-it-py native list parsing with loose validation."""
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

        # Handle special phase parsing (Phase: 1 of 3)
        if 'phase' in fields and ' of ' in fields['phase']:
            phase_parts = fields['phase'].split(' of ')
            if len(phase_parts) == 2:
                fields['phase_number'] = phase_parts[0].strip()
                fields['total_phases'] = phase_parts[1].strip()

        # Set defaults for missing fields (loose validation - empty strings allowed)
        field_defaults = {
            'phase_name': 'Unnamed Spec',
            'objectives': '',
            'scope': '',
            'dependencies': '',
            'deliverables': '',
            'architecture': '',
            'technology_stack': '',
            'functional_requirements': '',
            'non_functional_requirements': '',
            'development_plan': '',
            'testing_strategy': '',
            'research_requirements': '',
            'success_criteria': '',
            'integration_context': '',
            'spec_status': 'draft',
            'phase_number': '1',
            'total_phases': '1',
            'creation_date': '',
            'last_updated': '',
            'spec_owner': '',
        }

        for field, default_value in field_defaults.items():
            if field not in fields:
                fields[field] = default_value

        return cls(
            initial_spec_id='',  # Will be set by service layer
            phase_name=fields['phase_name'],
            objectives=fields['objectives'],
            scope=fields['scope'],
            dependencies=fields['dependencies'],
            deliverables=fields['deliverables'],
            architecture=fields['architecture'],
            technology_stack=fields['technology_stack'],
            functional_requirements=fields['functional_requirements'],
            non_functional_requirements=fields['non_functional_requirements'],
            development_plan=fields['development_plan'],
            testing_strategy=fields['testing_strategy'],
            research_requirements=fields['research_requirements'],
            success_criteria=fields['success_criteria'],
            integration_context=fields['integration_context'],
            spec_status=SpecStatus(fields['spec_status']),
            phase_number=fields['phase_number'],
            total_phases=fields['total_phases'],
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

## System Design
- **Architecture**: {self.architecture}
- **Technology Stack**: {self.technology_stack}

## Implementation
- **Functional Requirements**: {self.functional_requirements}
- **Non-Functional Requirements**: {self.non_functional_requirements}
- **Development Plan**: {self.development_plan}
- **Testing Strategy**: {self.testing_strategy}

## Additional Details
- **Research Requirements**: {self.research_requirements}
- **Success Criteria**: {self.success_criteria}
- **Integration Context**: {self.integration_context}

## Metadata
- **Status**: {self.spec_status.value}
- **Phase**: {self.phase_number} of {self.total_phases}
- **Created**: {self.creation_date}
- **Last Updated**: {self.last_updated}
- **Owner**: {self.spec_owner}
"""
