import re
from datetime import datetime
from typing import Self
from uuid import uuid4

from pydantic import Field
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from .base import MCPModel
from .enums import SpecStatus


class TechnicalSpec(MCPModel):
    id: str = Field(default_factory=lambda: str(uuid4())[:8])
    initial_spec_id: str | None = None
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
        """Parse using MarkdownIt's native list parsing."""
        if '# Technical Specification:' not in markdown:
            raise ValueError('Invalid specification format: missing title')

        # Try MarkdownIt-native parsing first (new format)
        try:
            result = cls._parse_markdown_it_native(markdown)
            # Check if we actually parsed any meaningful data from lists
            if (
                result.objectives != 'Objectives not specified'
                or result.scope != 'Scope not specified'
                or result.dependencies != 'Dependencies not specified'
            ):
                return result
            else:
                # No list data found, try legacy parsing
                return cls._parse_legacy_regex(markdown)
        except Exception:
            # Fallback to regex parsing for backwards compatibility
            return cls._parse_legacy_regex(markdown)

    @classmethod
    def _parse_markdown_it_native(cls, markdown: str) -> Self:
        """Parse new markdown-it-py native list format."""
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

        # Set defaults for missing fields
        field_defaults = {
            'phase_name': 'Unnamed Spec',
            'objectives': 'Objectives not specified',
            'scope': 'Scope not specified',
            'dependencies': 'Dependencies not specified',
            'deliverables': 'Deliverables not specified',
            'architecture': 'Architecture not specified',
            'technology_stack': 'Technology Stack not specified',
            'functional_requirements': 'Functional Requirements not specified',
            'non_functional_requirements': 'Non-Functional Requirements not specified',
            'development_plan': 'Development Plan not specified',
            'testing_strategy': 'Testing Strategy not specified',
            'research_requirements': 'Research Requirements not specified',
            'success_criteria': 'Success Criteria not specified',
            'integration_context': 'Integration Context not specified',
            'spec_status': 'draft',
            'phase_number': '1',
            'total_phases': '1',
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

    @classmethod
    def _parse_legacy_regex(cls, markdown: str) -> Self:
        """Legacy regex parsing for backwards compatibility."""
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
