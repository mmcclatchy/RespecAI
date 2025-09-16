import pytest

from services.models.initial_spec import InitialSpec
from services.models.enums import SpecStatus


@pytest.fixture
def sample_initial_spec_markdown() -> str:
    """Sample markdown for InitialSpec parsing tests."""
    return """# Technical Specification: User Authentication System
<!-- ID: abc12345 -->

## Overview
- **Objectives**: Implement secure user login and registration
- **Scope**: Login, logout, password reset functionality
- **Dependencies**: Database, encryption library
- **Deliverables**: Working authentication system

## Metadata
- **Status**: draft
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-02
- **Owner**: Development Team
"""


class TestInitialSpecParsing:
    def test_parse_markdown_extracts_basic_fields(self, sample_initial_spec_markdown: str) -> None:
        """Test that InitialSpec can parse basic fields from markdown."""
        spec = InitialSpec.parse_markdown(sample_initial_spec_markdown)

        assert spec.phase_name == 'User Authentication System'
        assert spec.objectives == 'Implement secure user login and registration'
        assert spec.scope == 'Login, logout, password reset functionality'
        assert spec.dependencies == 'Database, encryption library'
        assert spec.deliverables == 'Working authentication system'
        assert spec.spec_status == SpecStatus.DRAFT
        assert spec.creation_date == '2024-01-01'
        assert spec.last_updated == '2024-01-02'
        assert spec.spec_owner == 'Development Team'

    def test_initial_spec_generates_8_char_id(self) -> None:
        """Test that InitialSpec generates 8-character UUID."""
        spec = InitialSpec(
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='None',
            deliverables='Test deliverables',
            spec_status=SpecStatus.DRAFT,
            creation_date='2024-01-01',
            last_updated='2024-01-01',
            spec_owner='Test Owner',
        )

        assert len(spec.id) == 8
        assert spec.id.isalnum()

    def test_build_markdown_creates_initial_spec_format(self) -> None:
        """Test that build_markdown creates proper InitialSpec format."""
        spec = InitialSpec(
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            spec_status=SpecStatus.DRAFT,
            creation_date='2024-01-15',
            last_updated='2024-01-15',
            spec_owner='Test Owner',
        )

        markdown = spec.build_markdown()

        assert '# Technical Specification: Test Spec' in markdown
        assert '<!-- ID:' in markdown
        assert '- **Objectives**: Test objectives' in markdown
        assert '- **Scope**: Test scope' in markdown
        assert '- **Dependencies**: Test dependencies' in markdown
        assert '- **Deliverables**: Test deliverables' in markdown
        assert '- **Status**: draft' in markdown
        assert '- **Created**: 2024-01-15' in markdown
        assert '- **Last Updated**: 2024-01-15' in markdown
        assert '- **Owner**: Test Owner' in markdown

    def test_round_trip_parsing_maintains_data_integrity(self, sample_initial_spec_markdown: str) -> None:
        """Test that parsing and rebuilding maintains complete data integrity."""
        original_spec = InitialSpec.parse_markdown(sample_initial_spec_markdown)

        rebuilt_markdown = original_spec.build_markdown()

        reparsed_spec = InitialSpec.parse_markdown(rebuilt_markdown)

        assert original_spec.phase_name == reparsed_spec.phase_name
        assert original_spec.objectives == reparsed_spec.objectives
        assert original_spec.scope == reparsed_spec.scope
        assert original_spec.dependencies == reparsed_spec.dependencies
        assert original_spec.deliverables == reparsed_spec.deliverables
        assert original_spec.spec_status == reparsed_spec.spec_status
        assert original_spec.creation_date == reparsed_spec.creation_date
        assert original_spec.last_updated == reparsed_spec.last_updated
        assert original_spec.spec_owner == reparsed_spec.spec_owner


class TestInitialSpecUtilities:
    def test_recursive_traversal_utilities_exist(self) -> None:
        """Test that shared utilities exist."""
        assert hasattr(InitialSpec, '_find_nodes_by_type')
        assert hasattr(InitialSpec, '_extract_text_content')
