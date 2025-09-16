from datetime import datetime
from typing import Self

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from pydantic import BaseModel, Field

from .enums import RoadmapStatus


from services.utils.errors import SpecNotFoundError


class Roadmap(BaseModel):
    project_name: str
    project_goal: str
    total_duration: str
    team_size: str
    roadmap_budget: str
    specs: list[str] = Field(default_factory=list)
    critical_path_analysis: str
    key_risks: str
    mitigation_plans: str
    buffer_time: str
    development_resources: str
    infrastructure_requirements: str
    external_dependencies: str
    quality_assurance_plan: str
    technical_milestones: str
    business_milestones: str
    quality_gates: str
    performance_targets: str
    roadmap_status: RoadmapStatus
    creation_date: str
    last_updated: str
    spec_count: int = Field(default=0)
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
        """Parse using markdown-it-py native list parsing."""
        if '# Project Roadmap:' not in markdown:
            raise ValueError('Invalid roadmap format: missing title')

        md = MarkdownIt('commonmark')
        tree = SyntaxTreeNode(md.parse(markdown))

        fields = {}
        specs = []

        # Extract title
        for node in cls._find_nodes_by_type(tree, 'heading'):
            if node.tag != 'h1':
                continue
            title_text = cls._extract_text_content(node)
            if 'Project Roadmap:' not in title_text:
                continue
            fields['project_name'] = title_text.split(':', 1)[1].strip()
            break

        # Extract all field data from lists
        for item in cls._find_nodes_by_type(tree, 'list_item'):
            text = cls._extract_text_content(item).strip()
            if ':' not in text:
                continue
            field_part, value_part = text.split(':', 1)
            field_name = field_part.strip().lower().replace(' ', '_').replace('-', '_')
            field_value = value_part.strip()

            # Handle spec entries (only numbered specs like spec_1, spec_2, etc.)
            if field_name.startswith('spec_') and field_name.replace('spec_', '').isdigit():
                # Only store the spec name - don't create InitialSpec objects
                # InitialSpec objects should only be created when we have actual content
                specs.append(field_value)
                continue

            # Map field names to model field names
            field_mapping = {'status': 'roadmap_status', 'created': 'creation_date', 'budget': 'roadmap_budget'}
            model_field_name = field_mapping.get(field_name, field_name)
            fields[model_field_name] = field_value

        # Set defaults for missing fields
        field_defaults = {
            'project_name': 'Unnamed Project',
            'project_goal': 'Project Goal not specified',
            'total_duration': 'Total Duration not specified',
            'team_size': 'Team Size not specified',
            'roadmap_budget': 'Budget not specified',
            'critical_path_analysis': 'Critical Path Analysis not specified',
            'key_risks': 'Key Risks not specified',
            'mitigation_plans': 'Mitigation Plans not specified',
            'buffer_time': 'Buffer Time not specified',
            'development_resources': 'Development Resources not specified',
            'infrastructure_requirements': 'Infrastructure Requirements not specified',
            'external_dependencies': 'External Dependencies not specified',
            'quality_assurance_plan': 'Quality Assurance Plan not specified',
            'technical_milestones': 'Technical Milestones not specified',
            'business_milestones': 'Business Milestones not specified',
            'quality_gates': 'Quality Gates not specified',
            'performance_targets': 'Performance Targets not specified',
            'roadmap_status': 'draft',
            'creation_date': 'Creation Date not specified',
            'last_updated': 'Last Updated not specified',
        }

        for field, default_value in field_defaults.items():
            if field not in fields:
                fields[field] = default_value

        return cls(
            project_name=fields['project_name'],
            project_goal=fields['project_goal'],
            total_duration=fields['total_duration'],
            team_size=fields['team_size'],
            roadmap_budget=fields['roadmap_budget'],
            specs=specs,
            critical_path_analysis=fields['critical_path_analysis'],
            key_risks=fields['key_risks'],
            mitigation_plans=fields['mitigation_plans'],
            buffer_time=fields['buffer_time'],
            development_resources=fields['development_resources'],
            infrastructure_requirements=fields['infrastructure_requirements'],
            external_dependencies=fields['external_dependencies'],
            quality_assurance_plan=fields['quality_assurance_plan'],
            technical_milestones=fields['technical_milestones'],
            business_milestones=fields['business_milestones'],
            quality_gates=fields['quality_gates'],
            performance_targets=fields['performance_targets'],
            roadmap_status=RoadmapStatus(fields['roadmap_status']),
            creation_date=fields['creation_date'],
            last_updated=fields['last_updated'],
            spec_count=len(specs),
        )

    def build_markdown(self) -> str:
        # Generate specs list dynamically
        specs_list = '\n'.join(f'- **Spec {i + 1}**: {spec}' for i, spec in enumerate(self.specs))

        return f"""# Project Roadmap: {self.project_name}

## Project Details
- **Project Goal**: {self.project_goal}
- **Total Duration**: {self.total_duration}
- **Team Size**: {self.team_size}
- **Budget**: {self.roadmap_budget}

## Specifications
{specs_list}

## Risk Assessment
- **Critical Path Analysis**: {self.critical_path_analysis}
- **Key Risks**: {self.key_risks}
- **Mitigation Plans**: {self.mitigation_plans}
- **Buffer Time**: {self.buffer_time}

## Resource Planning
- **Development Resources**: {self.development_resources}
- **Infrastructure Requirements**: {self.infrastructure_requirements}
- **External Dependencies**: {self.external_dependencies}
- **Quality Assurance Plan**: {self.quality_assurance_plan}

## Success Metrics
- **Technical Milestones**: {self.technical_milestones}
- **Business Milestones**: {self.business_milestones}
- **Quality Gates**: {self.quality_gates}
- **Performance Targets**: {self.performance_targets}

## Metadata
- **Status**: {self.roadmap_status.value}
- **Created**: {self.creation_date}
- **Last Updated**: {self.last_updated}
- **Spec Count**: {self.spec_count}
"""

    def add_spec_name(self, spec_name: str) -> None:
        """Add a spec name to the roadmap and update the count."""
        # Remove existing spec with same name if it exists
        if spec_name in self.specs:
            return

        # Add new spec name
        self.specs.append(spec_name)
        self.spec_count = len(self.specs)

    def get_spec_name(self, spec_name: str) -> str:
        """Get a spec name."""
        if spec_name in self.specs:
            return spec_name

        raise SpecNotFoundError(f'Spec not found: {spec_name}')
