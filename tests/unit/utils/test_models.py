import pytest

from services.utils.enums import LoopStatus, OperationStatus
from services.utils.errors import SpecNotFoundError
from services.utils.models import InitialSpec, MCPResponse, OperationResponse, RoadMap


class TestInitialSpec:
    @pytest.fixture
    def valid_markdown(self) -> str:
        return """# Technical Specification: User Authentication

## Overview

**Objectives**: `Implement secure user authentication system`  
**Scope**: `Login, logout, session management`  
**Dependencies**: `Database setup, encryption library`

## Expected Deliverables

- User login/logout endpoints
- Session management middleware
- Password encryption utilities

## Technical Architecture

REST API endpoints using FastAPI with JWT tokens for session management.
Database integration using PostgreSQL for user storage.

## Quality Gates

- [ ] All objectives met and validated
- [ ] Scope boundaries respected  
- [ ] Dependencies properly integrated
"""

    @pytest.fixture
    def malformed_markdown(self) -> str:
        return """# Technical Specification: Broken Spec

## Overview
Missing objectives format

**Scope**: `API development only`  
**Dependencies**: `None specified`

## Expected Deliverables
Basic API structure

## Technical Architecture
Minimal implementation
"""

    @pytest.fixture
    def empty_markdown(self) -> str:
        return ''

    @pytest.mark.parametrize(
        'markdown_fixture,expected_name,expected_objectives',
        [
            ('valid_markdown', 'User Authentication', 'Implement secure user authentication system'),
            ('malformed_markdown', 'Broken Spec', 'Objectives not specified'),
            ('empty_markdown', 'Unnamed Spec', 'Objectives not specified'),
        ],
    )
    def test_parse_markdown_extracts_correct_fields(
        self, request: pytest.FixtureRequest, markdown_fixture: str, expected_name: str, expected_objectives: str
    ) -> None:
        markdown = request.getfixturevalue(markdown_fixture)

        spec = InitialSpec.parse_markdown(markdown)

        assert spec.name == expected_name
        assert spec.objectives == expected_objectives
        assert isinstance(spec.scope, str)
        assert isinstance(spec.dependencies, str)
        assert isinstance(spec.deliverables, str)
        assert isinstance(spec.architecture, str)

    def test_parse_markdown_handles_special_characters(self) -> None:
        markdown_with_special_chars = """# Technical Specification: API & Database Integration

## Overview

**Objectives**: `Handle UTF-8 & special chars: <>{}[]`  
**Scope**: `Multi-line
content with breaks`  
**Dependencies**: `Libraries: pytest>=7.0, fastapi>=0.100`

## Expected Deliverables

- Feature with "quotes" and 'apostrophes'
- Support for émojis 🚀 and unicode

## Technical Architecture

Implementation using <generic> types and [array] structures.
"""

        spec = InitialSpec.parse_markdown(markdown_with_special_chars)

        assert 'API & Database Integration' in spec.name
        assert 'UTF-8 & special chars' in spec.objectives
        assert 'Multi-line' in spec.scope
        assert 'pytest>=7.0' in spec.dependencies
        assert 'émojis 🚀' in spec.deliverables
        assert '<generic>' in spec.architecture

    def test_build_markdown_creates_valid_format(self, valid_markdown: str) -> None:
        spec = InitialSpec(
            name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            architecture='Test architecture',
        )

        result_markdown = spec.build_markdown()

        # Check structure
        assert '# Technical Specification: Test Spec' in result_markdown
        assert '## Overview' in result_markdown
        assert '**Objectives**: `Test objectives`' in result_markdown
        assert '**Scope**: `Test scope`' in result_markdown
        assert '**Dependencies**: `Test dependencies`' in result_markdown
        assert '## Expected Deliverables' in result_markdown
        assert 'Test deliverables' in result_markdown
        assert '## Technical Architecture' in result_markdown
        assert 'Test architecture' in result_markdown
        assert '## Quality Gates' in result_markdown

    def test_markdown_round_trip_consistency(self, valid_markdown: str) -> None:
        # Parse original markdown
        original_spec = InitialSpec.parse_markdown(valid_markdown)

        # Build new markdown
        rebuilt_markdown = original_spec.build_markdown()

        # Parse rebuilt markdown
        rebuilt_spec = InitialSpec.parse_markdown(rebuilt_markdown)

        # Should maintain core data
        assert rebuilt_spec.name == original_spec.name
        assert rebuilt_spec.objectives == original_spec.objectives
        assert rebuilt_spec.scope == original_spec.scope
        assert rebuilt_spec.dependencies == original_spec.dependencies


class TestRoadMap:
    def test_add_spec_stores_by_name(self) -> None:
        roadmap = RoadMap(name='Test Roadmap')
        spec = InitialSpec(
            name='Test Spec',
            objectives='Test',
            scope='Test',
            dependencies='Test',
            deliverables='Test',
            architecture='Test',
        )

        roadmap.add_spec(spec)

        assert 'Test Spec' in roadmap.specs
        assert roadmap.specs['Test Spec'] == spec

    def test_add_spec_overwrites_existing(self) -> None:
        roadmap = RoadMap(name='Test Roadmap')
        original_spec = InitialSpec(
            name='Same Name',
            objectives='Original',
            scope='Test',
            dependencies='Test',
            deliverables='Test',
            architecture='Test',
        )
        updated_spec = InitialSpec(
            name='Same Name',
            objectives='Updated',
            scope='Test',
            dependencies='Test',
            deliverables='Test',
            architecture='Test',
        )

        roadmap.add_spec(original_spec)
        roadmap.add_spec(updated_spec)

        assert len(roadmap.specs) == 1
        assert roadmap.specs['Same Name'].objectives == 'Updated'

    def test_get_spec_retrieves_correct_spec(self) -> None:
        roadmap = RoadMap(name='Test Roadmap')
        spec = InitialSpec(
            name='Target Spec',
            objectives='Find me',
            scope='Test',
            dependencies='Test',
            deliverables='Test',
            architecture='Test',
        )
        roadmap.add_spec(spec)

        retrieved_spec = roadmap.get_spec('Target Spec')

        assert retrieved_spec == spec
        assert retrieved_spec.objectives == 'Find me'

    def test_get_spec_raises_error_when_not_found(self) -> None:
        roadmap = RoadMap(name='Empty Roadmap')

        with pytest.raises(SpecNotFoundError) as exc_info:
            roadmap.get_spec('Non-existent Spec')

        assert 'Non-existent Spec' in str(exc_info.value)


class TestResponseModels:
    def test_operation_response_creation(self) -> None:
        response = OperationResponse(
            id='test-123', status=OperationStatus.SUCCESS, message='Operation completed successfully'
        )

        assert response.id == 'test-123'
        assert response.status == OperationStatus.SUCCESS
        assert response.message == 'Operation completed successfully'

    def test_mcp_response_creation(self) -> None:
        response = MCPResponse(id='loop-456', status=LoopStatus.COMPLETED, message='Loop completed')

        assert response.id == 'loop-456'
        assert response.status == LoopStatus.COMPLETED
        assert response.message == 'Loop completed'
