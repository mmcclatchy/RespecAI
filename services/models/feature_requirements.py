from datetime import datetime
from typing import Self

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
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
    def _find_nodes_by_type(cls, node: SyntaxTreeNode, node_type: str) -> list[SyntaxTreeNode]:
        nodes = []

        if node.type == node_type:
            nodes.append(node)

        if hasattr(node, 'children') and node.children:
            for child in node.children:
                nodes.extend(cls._find_nodes_by_type(child, node_type))

        return nodes

    @classmethod
    def _extract_text_content(cls, node: SyntaxTreeNode) -> str:
        if not hasattr(node, 'children') or not node.children:
            return getattr(node, 'content', '')

        return ' '.join(cls._extract_text_content(child) for child in node.children)

    @classmethod
    def _extract_content_by_header_path(cls, tree: SyntaxTreeNode, path: list[str]) -> str:
        h2_header = path[0]
        h3_header = path[1] if len(path) > 1 else None

        nodes = tree.children if hasattr(tree, 'children') else []
        h2_start_idx = None

        for i, node in enumerate(nodes):
            if node.type == 'heading' and node.tag == 'h2':
                header_text = cls._extract_text_content(node).strip()
                if header_text == h2_header:
                    h2_start_idx = i
                    break

        if h2_start_idx is None:
            return ''

        if h3_header is None:
            content_parts = []
            for j in range(h2_start_idx + 1, len(nodes)):
                next_node = nodes[j]
                if next_node.type == 'heading' and next_node.tag == 'h2':
                    break
                if next_node.type in ['paragraph', 'list', 'blockquote', 'code_block']:
                    content_parts.append(cls._extract_text_content(next_node).strip())
            return '\n\n'.join(content_parts).strip()

        h3_start_idx = None
        for j in range(h2_start_idx + 1, len(nodes)):
            next_node = nodes[j]
            if next_node.type == 'heading' and next_node.tag == 'h2':
                break
            if next_node.type == 'heading' and next_node.tag == 'h3':
                header_text = cls._extract_text_content(next_node).strip()
                if header_text == h3_header:
                    h3_start_idx = j
                    break

        if h3_start_idx is None:
            return ''

        content_parts = []
        for j in range(h3_start_idx + 1, len(nodes)):
            next_node = nodes[j]
            if next_node.type == 'heading' and next_node.tag in ['h2', 'h3']:
                break
            if next_node.type in ['paragraph', 'list', 'blockquote', 'code_block']:
                content_parts.append(cls._extract_text_content(next_node).strip())

        return '\n\n'.join(content_parts).strip()

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        if '# Feature Requirements:' not in markdown:
            raise ValueError('Invalid feature requirements format: missing title')

        md = MarkdownIt('commonmark')
        tree = SyntaxTreeNode(md.parse(markdown))

        fields = {}

        # Extract title
        for node in cls._find_nodes_by_type(tree, 'heading'):
            if node.tag != 'h1':
                continue
            title_text = cls._extract_text_content(node)
            if 'Feature Requirements:' not in title_text:
                continue
            fields['project_name'] = title_text.split(':', 1)[1].strip()
            break

        # Extract content by header paths
        header_path_mapping = {
            'feature_description': ['Overview', 'Feature Description'],
            'problem_statement': ['Overview', 'Problem Statement'],
            'target_users': ['Overview', 'Target Users'],
            'business_value': ['Overview', 'Business Value'],
            'user_stories': ['Requirements', 'User Stories'],
            'acceptance_criteria': ['Requirements', 'Acceptance Criteria'],
            'user_experience_goals': ['Requirements', 'User Experience Goals'],
            'functional_requirements': ['Technical Specifications', 'Functional Requirements'],
            'non_functional_requirements': ['Technical Specifications', 'Non-Functional Requirements'],
            'integration_requirements': ['Technical Specifications', 'Integration Requirements'],
            'user_metrics': ['Metrics', 'User Metrics'],
            'performance_metrics': ['Metrics', 'Performance Metrics'],
            'technical_metrics': ['Metrics', 'Technical Metrics'],
            'must_have_features': ['Feature Prioritization', 'Must Have'],
            'should_have_features': ['Feature Prioritization', 'Should Have'],
            'could_have_features': ['Feature Prioritization', 'Could Have'],
            'wont_have_features': ['Feature Prioritization', "Won't Have"],
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

            field_mapping = {'status': 'requirements_status', 'created': 'creation_date', 'owner': 'feature_owner'}
            model_field_name = field_mapping.get(field_name, field_name)
            fields[model_field_name] = field_value

        # Set defaults for missing fields
        field_defaults = {
            'project_name': 'Unnamed Project',
            'feature_description': 'Feature Description not specified',
            'problem_statement': 'Problem Statement not specified',
            'target_users': 'Target Users not specified',
            'business_value': 'Business Value not specified',
            'user_stories': 'User Stories not specified',
            'acceptance_criteria': 'Acceptance Criteria not specified',
            'user_experience_goals': 'User Experience Goals not specified',
            'functional_requirements': 'Functional Requirements not specified',
            'non_functional_requirements': 'Non Functional Requirements not specified',
            'integration_requirements': 'Integration Requirements not specified',
            'user_metrics': 'User Metrics not specified',
            'performance_metrics': 'Performance Metrics not specified',
            'technical_metrics': 'Technical Metrics not specified',
            'must_have_features': 'Must Have Features not specified',
            'should_have_features': 'Should Have Features not specified',
            'could_have_features': 'Could Have Features not specified',
            'wont_have_features': 'Wont Have Features not specified',
            'requirements_status': 'draft',
            'creation_date': 'Creation Date not specified',
            'last_updated': 'Last Updated not specified',
            'feature_owner': 'Feature Owner not specified',
        }

        for field, default_value in field_defaults.items():
            if field not in fields:
                fields[field] = default_value

        return cls(
            project_name=fields['project_name'],
            feature_description=fields['feature_description'],
            problem_statement=fields['problem_statement'],
            target_users=fields['target_users'],
            business_value=fields['business_value'],
            user_stories=fields['user_stories'],
            acceptance_criteria=fields['acceptance_criteria'],
            user_experience_goals=fields['user_experience_goals'],
            functional_requirements=fields['functional_requirements'],
            non_functional_requirements=fields['non_functional_requirements'],
            integration_requirements=fields['integration_requirements'],
            user_metrics=fields['user_metrics'],
            performance_metrics=fields['performance_metrics'],
            technical_metrics=fields['technical_metrics'],
            must_have_features=fields['must_have_features'],
            should_have_features=fields['should_have_features'],
            could_have_features=fields['could_have_features'],
            wont_have_features=fields['wont_have_features'],
            requirements_status=RequirementsStatus(fields['requirements_status']),
            creation_date=fields['creation_date'],
            last_updated=fields['last_updated'],
            feature_owner=fields['feature_owner'],
        )

    def build_markdown(self) -> str:
        return f"""# Feature Requirements: {self.project_name}

## Overview

### Feature Description
{self.feature_description}

### Problem Statement
{self.problem_statement}

### Target Users
{self.target_users}

### Business Value
{self.business_value}

## Requirements

### User Stories
{self.user_stories}

### Acceptance Criteria
{self.acceptance_criteria}

### User Experience Goals
{self.user_experience_goals}

## Technical Specifications

### Functional Requirements
{self.functional_requirements}

### Non-Functional Requirements
{self.non_functional_requirements}

### Integration Requirements
{self.integration_requirements}

## Metrics

### User Metrics
{self.user_metrics}

### Performance Metrics
{self.performance_metrics}

### Technical Metrics
{self.technical_metrics}

## Feature Prioritization

### Must Have
{self.must_have_features}

### Should Have
{self.should_have_features}

### Could Have
{self.could_have_features}

### Won't Have
{self.wont_have_features}

## Metadata
- **Status**: {self.requirements_status.value}
- **Created**: {self.creation_date}
- **Last Updated**: {self.last_updated}
- **Owner**: {self.feature_owner}
"""
