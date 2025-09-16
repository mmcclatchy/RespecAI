import pytest

from services.models.partial_spec import PartialSpec
from services.models.enums import SpecStatus


@pytest.fixture
def sample_partial_spec_markdown() -> str:
    """Sample markdown for PartialSpec parsing tests."""
    return """# Technical Specification: User Authentication System (Draft)
<!-- ID: abc12345 -->

## Overview
- **Objectives**: Implement secure user login and registration
- **Scope**: Login, logout, password reset functionality
- **Dependencies**: Database, encryption library
- **Deliverables**: Working authentication system

## System Design
- **Architecture**: Microservices architecture
- **Technology Stack**: Python FastAPI, PostgreSQL

## Implementation
- **Functional Requirements**: User registration, login, logout
- **Non-Functional Requirements**: Response time < 200ms
- **Development Plan**: Phase 1: Backend, Phase 2: Frontend
- **Testing Strategy**: Unit tests, integration tests

## Additional Details
- **Research Requirements**: OAuth integration patterns
- **Success Criteria**: 100% test coverage
- **Integration Context**: Connects to user service

## Metadata
- **Status**: in-development
- **Phase**: 1 of 3
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-02
- **Owner**: Development Team
"""


class TestPartialSpecParsing:
    def test_parse_markdown_allows_partial_completion(self, sample_partial_spec_markdown: str) -> None:
        """Test that PartialSpec can parse partially completed specs."""
        spec = PartialSpec.parse_markdown(sample_partial_spec_markdown)

        assert spec.phase_name == 'User Authentication System (Draft)'
        assert spec.objectives == 'Implement secure user login and registration'
        assert spec.scope == 'Login, logout, password reset functionality'
        assert spec.architecture == 'Microservices architecture'
        assert spec.technology_stack == 'Python FastAPI, PostgreSQL'
        assert spec.spec_status == SpecStatus.IN_DEVELOPMENT

    def test_partial_spec_has_initial_spec_id_field(self) -> None:
        """Test that PartialSpec has initial_spec_id foreign key."""
        spec = PartialSpec(
            initial_spec_id='abc12345',
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            architecture='',  # Can be empty in partial spec
            technology_stack='',  # Can be empty in partial spec
            functional_requirements='Basic login',
            non_functional_requirements='',
            development_plan='',
            testing_strategy='',
            research_requirements='',
            success_criteria='',
            integration_context='',
            spec_status=SpecStatus.DRAFT,
            phase_number='1',
            total_phases='3',
            creation_date='2024-01-01',
            last_updated='2024-01-01',
            spec_owner='Test Owner',
        )

        assert spec.initial_spec_id == 'abc12345'
        assert len(spec.id) == 8

    def test_build_markdown_creates_partial_spec_format(self) -> None:
        """Test that build_markdown works with partial completion."""
        spec = PartialSpec(
            initial_spec_id='abc12345',
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            architecture='',  # Empty field
            technology_stack='Python, FastAPI',
            functional_requirements='Login functionality',
            non_functional_requirements='',  # Empty field
            development_plan='3-phase approach',
            testing_strategy='',  # Empty field
            research_requirements='Security patterns',
            success_criteria='',  # Empty field
            integration_context='API integration',
            spec_status=SpecStatus.IN_DEVELOPMENT,
            phase_number='1',
            total_phases='3',
            creation_date='2024-01-15',
            last_updated='2024-01-15',
            spec_owner='Test Owner',
        )

        markdown = spec.build_markdown()

        assert '# Technical Specification: Test Spec' in markdown
        assert '<!-- ID:' in markdown
        assert '- **Objectives**: Test objectives' in markdown
        assert '- **Architecture**: ' in markdown  # Empty field should still appear
        assert '- **Technology Stack**: Python, FastAPI' in markdown
        assert '- **Non-Functional Requirements**: ' in markdown  # Empty field
        assert '- **Status**: in-development' in markdown

    def test_round_trip_parsing_with_partial_data(self, sample_partial_spec_markdown: str) -> None:
        """Test round-trip parsing works with partially completed data."""
        original_spec = PartialSpec.parse_markdown(sample_partial_spec_markdown)

        rebuilt_markdown = original_spec.build_markdown()

        reparsed_spec = PartialSpec.parse_markdown(rebuilt_markdown)

        assert original_spec.phase_name == reparsed_spec.phase_name
        assert original_spec.objectives == reparsed_spec.objectives
        assert original_spec.architecture == reparsed_spec.architecture
        assert original_spec.spec_status == reparsed_spec.spec_status


class TestPartialSpecUtilities:
    def test_recursive_traversal_utilities_exist(self) -> None:
        """Test that shared utilities exist."""
        assert hasattr(PartialSpec, '_find_nodes_by_type')
        assert hasattr(PartialSpec, '_extract_text_content')
