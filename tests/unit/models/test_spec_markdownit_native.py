import pytest

from services.models.enums import SpecStatus
from services.models.spec import TechnicalSpec


@pytest.fixture
def markdownit_native_spec_markdown() -> str:
    """New MarkdownIt-native list format template."""
    return """# Technical Specification: User Authentication System
<!-- ID: abc12345 -->

## Overview
- **Objectives**: Implement secure user login and registration
- **Scope**: Login, logout, password reset functionality
- **Dependencies**: Database, encryption library
- **Deliverables**: Working authentication system

## System Design
- **Architecture**: Microservices architecture with API gateway
- **Technology Stack**: Python FastAPI, PostgreSQL, JWT

## Implementation
- **Functional Requirements**: User registration, login, logout, password reset
- **Non-Functional Requirements**: Response time < 200ms, 99.9% uptime
- **Development Plan**: Phase 1: Backend, Phase 2: Frontend integration
- **Testing Strategy**: Unit tests, integration tests, security testing

## Additional Details
- **Research Requirements**: OAuth integration patterns, JWT best practices
- **Success Criteria**: 100% test coverage, security audit passed
- **Integration Context**: Connects to user service, notification service

## Metadata
- **Status**: in-development
- **Phase**: 1 of 3
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-02
- **Owner**: Development Team"""


class TestMarkdownItNativeParsing:
    def test_parse_markdownit_native_format_extracts_all_fields(self, markdownit_native_spec_markdown: str) -> None:
        """Test that new list-based format can be parsed correctly."""
        spec = TechnicalSpec.parse_markdown(markdownit_native_spec_markdown)

        assert spec.phase_name == 'User Authentication System'
        assert spec.objectives == 'Implement secure user login and registration'
        assert spec.scope == 'Login, logout, password reset functionality'
        assert spec.dependencies == 'Database, encryption library'
        assert spec.deliverables == 'Working authentication system'
        assert spec.architecture == 'Microservices architecture with API gateway'
        assert spec.technology_stack == 'Python FastAPI, PostgreSQL, JWT'
        assert spec.functional_requirements == 'User registration, login, logout, password reset'
        assert spec.non_functional_requirements == 'Response time < 200ms, 99.9% uptime'
        assert spec.development_plan == 'Phase 1: Backend, Phase 2: Frontend integration'
        assert spec.testing_strategy == 'Unit tests, integration tests, security testing'
        assert spec.research_requirements == 'OAuth integration patterns, JWT best practices'
        assert spec.success_criteria == '100% test coverage, security audit passed'
        assert spec.integration_context == 'Connects to user service, notification service'
        assert spec.spec_status == SpecStatus.IN_DEVELOPMENT
        assert spec.phase_number == '1'
        assert spec.total_phases == '3'
        assert spec.creation_date == '2024-01-01'
        assert spec.last_updated == '2024-01-02'
        assert spec.spec_owner == 'Development Team'

    def test_build_markdown_creates_markdownit_native_format(self) -> None:
        """Test that build_markdown creates the new list-based format."""
        spec = TechnicalSpec(
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            architecture='Test architecture',
            technology_stack='Python, FastAPI',
            functional_requirements='Login functionality',
            non_functional_requirements='High performance',
            development_plan='3-phase approach',
            testing_strategy='TDD approach',
            research_requirements='Security patterns',
            success_criteria='All tests pass',
            integration_context='API integration',
            spec_status=SpecStatus.APPROVED,
            phase_number='1',
            total_phases='3',
            creation_date='2024-01-15',
            last_updated='2024-01-15',
            spec_owner='Test Owner',
        )

        markdown = spec.build_markdown()

        # Should use new list format
        assert '# Technical Specification: Test Spec' in markdown
        assert '## Overview' in markdown
        assert '- **Objectives**: Test objectives' in markdown
        assert '- **Scope**: Test scope' in markdown
        assert '- **Dependencies**: Test dependencies' in markdown
        assert '- **Deliverables**: Test deliverables' in markdown
        assert '## System Design' in markdown
        assert '- **Architecture**: Test architecture' in markdown
        assert '- **Technology Stack**: Python, FastAPI' in markdown
        assert '## Implementation' in markdown
        assert '- **Functional Requirements**: Login functionality' in markdown
        assert '- **Non-Functional Requirements**: High performance' in markdown
        assert '- **Development Plan**: 3-phase approach' in markdown
        assert '- **Testing Strategy**: TDD approach' in markdown
        assert '## Additional Details' in markdown
        assert '- **Research Requirements**: Security patterns' in markdown
        assert '- **Success Criteria**: All tests pass' in markdown
        assert '- **Integration Context**: API integration' in markdown
        assert '## Metadata' in markdown
        assert '- **Status**: approved' in markdown
        assert '- **Phase**: 1 of 3' in markdown
        assert '- **Created**: 2024-01-15' in markdown
        assert '- **Last Updated**: 2024-01-15' in markdown
        assert '- **Owner**: Test Owner' in markdown

    def test_round_trip_parsing_maintains_data_integrity(self, markdownit_native_spec_markdown: str) -> None:
        """Test that parsing and rebuilding maintains complete data integrity."""
        original_spec = TechnicalSpec.parse_markdown(markdownit_native_spec_markdown)

        rebuilt_markdown = original_spec.build_markdown()

        reparsed_spec = TechnicalSpec.parse_markdown(rebuilt_markdown)

        assert original_spec.phase_name == reparsed_spec.phase_name
        assert original_spec.objectives == reparsed_spec.objectives
        assert original_spec.scope == reparsed_spec.scope
        assert original_spec.dependencies == reparsed_spec.dependencies
        assert original_spec.deliverables == reparsed_spec.deliverables
        assert original_spec.architecture == reparsed_spec.architecture
        assert original_spec.technology_stack == reparsed_spec.technology_stack
        assert original_spec.functional_requirements == reparsed_spec.functional_requirements
        assert original_spec.non_functional_requirements == reparsed_spec.non_functional_requirements
        assert original_spec.development_plan == reparsed_spec.development_plan
        assert original_spec.testing_strategy == reparsed_spec.testing_strategy
        assert original_spec.research_requirements == reparsed_spec.research_requirements
        assert original_spec.success_criteria == reparsed_spec.success_criteria
        assert original_spec.integration_context == reparsed_spec.integration_context
        assert original_spec.spec_status == reparsed_spec.spec_status
        assert original_spec.phase_number == reparsed_spec.phase_number
        assert original_spec.total_phases == reparsed_spec.total_phases
        assert original_spec.creation_date == reparsed_spec.creation_date
        assert original_spec.last_updated == reparsed_spec.last_updated
        assert original_spec.spec_owner == reparsed_spec.spec_owner


class TestRecursiveTraversalUtilities:
    def test_find_nodes_by_type_utility_exists(self) -> None:
        """Test that _find_nodes_by_type utility method exists."""
        # This will fail until we implement the utility
        assert hasattr(TechnicalSpec, '_find_nodes_by_type')

    def test_extract_text_content_utility_exists(self) -> None:
        """Test that _extract_text_content utility method exists."""
        # This will fail until we implement the utility
        assert hasattr(TechnicalSpec, '_extract_text_content')
