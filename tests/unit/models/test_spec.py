import pytest

from services.models.enums import SpecStatus
from services.models.spec import TechnicalSpec


@pytest.fixture
def complete_spec_markdown() -> str:
    return """# Technical Specification: Test Phase

## Overview
**Objectives**: `Implement user authentication system`
**Scope**: `Login, logout, password reset functionality`
**Dependencies**: `User database, JWT library`

## Deliverables
`Authentication service, login UI, password reset flow`

## System Design

### Architecture
`Microservice architecture with JWT tokens`

### Technology Stack
`Python FastAPI, PostgreSQL, JWT`

## Implementation

### Functional Requirements
`User login with email/password, secure password storage`

### Non-Functional Requirements
`Response time < 200ms, 99.9% uptime`

### Development Plan
`Phase 1: Backend service, Phase 2: Frontend integration`

### Testing Strategy
`Unit tests, integration tests, security testing`

## Research Requirements
`OAuth integration patterns, JWT best practices`

## Success Criteria
`100% test coverage, security audit passed`

## Integration
`Connects to user service, notification service`

---

**Status**: `in-development`
**Phase**: `1` of `3`
**Created**: `2024-01-15`
**Last Updated**: `2024-01-16`
**Owner**: `Test Owner`
"""


@pytest.fixture
def minimal_spec_markdown() -> str:
    return """# Technical Specification: Minimal Spec

## Overview
**Objectives**: `Basic functionality`
"""


@pytest.fixture
def round_trip_spec_markdown() -> str:
    return """# Technical Specification: Round Trip Test

## Overview
**Objectives**: `Test round trip parsing`
**Scope**: `Complete data preservation`
**Dependencies**: `None`

## Deliverables
`Validated parsing system`

## System Design

### Architecture
`Clean architecture pattern`

### Technology Stack
`Python 3.11, Pydantic`

## Implementation

### Functional Requirements
`Complete field mapping`

### Non-Functional Requirements
`Zero data loss`

### Development Plan
`Single iteration`

### Testing Strategy
`Round-trip validation`

## Research Requirements
`Parsing best practices`

## Success Criteria
`Character-for-character match`

## Integration
`Standalone component`

---

**Status**: `approved`
**Phase**: `1` of `1`
**Created**: `2024-01-15`
**Last Updated**: `2024-01-15`
**Owner**: `Test Owner`
"""


class TestTechnicalSpecParsing:
    def test_parse_markdown_extracts_all_fields(self, complete_spec_markdown: str) -> None:
        spec = TechnicalSpec.parse_markdown(complete_spec_markdown)

        assert spec.phase_name == 'Test Phase'
        assert spec.objectives == 'Implement user authentication system'
        assert spec.scope == 'Login, logout, password reset functionality'
        assert spec.dependencies == 'User database, JWT library'
        assert spec.deliverables == 'Authentication service, login UI, password reset flow'
        assert spec.architecture == 'Microservice architecture with JWT tokens'
        assert spec.technology_stack == 'Python FastAPI, PostgreSQL, JWT'
        assert spec.functional_requirements == 'User login with email/password, secure password storage'
        assert spec.non_functional_requirements == 'Response time < 200ms, 99.9% uptime'
        assert spec.development_plan == 'Phase 1: Backend service, Phase 2: Frontend integration'
        assert spec.testing_strategy == 'Unit tests, integration tests, security testing'
        assert spec.research_requirements == 'OAuth integration patterns, JWT best practices'
        assert spec.success_criteria == '100% test coverage, security audit passed'
        assert spec.integration_context == 'Connects to user service, notification service'
        assert spec.spec_status == 'in-development'
        assert spec.phase_number == '1'
        assert spec.total_phases == '3'
        assert spec.creation_date == '2024-01-15'
        assert spec.last_updated == '2024-01-16'
        assert spec.spec_owner == 'Test Owner'

    def test_parse_markdown_handles_missing_sections(self, minimal_spec_markdown: str) -> None:
        spec = TechnicalSpec.parse_markdown(minimal_spec_markdown)

        assert spec.phase_name == 'Minimal Spec'
        assert spec.objectives == 'Basic functionality'
        assert spec.scope != ''
        assert spec.technology_stack != ''

    def test_parse_markdown_invalid_format_raises_error(self) -> None:
        invalid_markdown = 'This is not a valid specification'

        with pytest.raises(ValueError, match='Invalid specification format'):
            TechnicalSpec.parse_markdown(invalid_markdown)


class TestTechnicalSpecMarkdownBuilding:
    def test_build_markdown_creates_valid_template_format(self) -> None:
        spec = TechnicalSpec(
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test deps',
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

        assert '# Technical Specification: Test Spec' in markdown
        assert '- **Objectives**: Test objectives' in markdown
        assert '- **Scope**: Test scope' in markdown
        assert '- **Dependencies**: Test deps' in markdown
        assert '- **Deliverables**: Test deliverables' in markdown
        assert '- **Architecture**: Test architecture' in markdown
        assert '- **Technology Stack**: Python, FastAPI' in markdown
        assert '- **Functional Requirements**: Login functionality' in markdown
        assert '- **Non-Functional Requirements**: High performance' in markdown
        assert '- **Development Plan**: 3-phase approach' in markdown
        assert '- **Testing Strategy**: TDD approach' in markdown

    def test_round_trip_parsing_maintains_data_integrity(self, round_trip_spec_markdown: str) -> None:
        spec = TechnicalSpec.parse_markdown(round_trip_spec_markdown)

        rebuilt_markdown = spec.build_markdown()

        parsed_spec = TechnicalSpec.parse_markdown(rebuilt_markdown)

        assert spec.phase_name == parsed_spec.phase_name
        assert spec.objectives == parsed_spec.objectives
        assert spec.scope == parsed_spec.scope
        assert spec.dependencies == parsed_spec.dependencies
        assert spec.deliverables == parsed_spec.deliverables
        assert spec.architecture == parsed_spec.architecture
        assert spec.research_requirements == parsed_spec.research_requirements
        assert spec.success_criteria == parsed_spec.success_criteria
        assert spec.integration_context == parsed_spec.integration_context

    def test_round_trip_data_integrity_validation(self, round_trip_spec_markdown: str) -> None:
        """Test that round-trip parsing preserves data integrity (format may change during migration)."""
        original_spec = TechnicalSpec.parse_markdown(round_trip_spec_markdown)

        rebuilt_markdown = original_spec.build_markdown()

        reparsed_spec = TechnicalSpec.parse_markdown(rebuilt_markdown)

        # Verify data integrity is preserved through round-trip
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
