from unittest.mock import Mock

import pytest

from services.mcp.roadmap_tools import RoadmapTools
from services.utils.enums import OperationStatus
from services.utils.errors import RoadmapNotFoundError, SpecNotFoundError
from services.utils.models import InitialSpec, OperationResponse, RoadMap
from services.utils.state_manager import StateManager


class TestRoadmapTools:
    @pytest.fixture
    def mock_state_manager(self) -> Mock:
        return Mock(spec=StateManager)

    @pytest.fixture
    def roadmap_tools(self, mock_state_manager: Mock) -> RoadmapTools:
        return RoadmapTools(mock_state_manager)

    @pytest.fixture
    def valid_spec_markdown(self) -> str:
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
"""

    @pytest.fixture
    def malformed_spec_markdown(self) -> str:
        return """# Some title
        
This is not properly formatted spec markdown.
Missing required sections and structure.
"""


class TestCreateRoadmap(TestRoadmapTools):
    def test_create_roadmap_returns_success_response(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.store_roadmap.return_value = 'test-project'

        result = roadmap_tools.create_roadmap('test-project', 'Test Roadmap')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project'
        assert result.status == OperationStatus.SUCCESS
        assert 'Test Roadmap' in result.message
        assert 'test-project' in result.message

    def test_create_roadmap_delegates_to_state_manager(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.store_roadmap.return_value = 'project-123'

        roadmap_tools.create_roadmap('project-123', 'My Roadmap')

        mock_state_manager.store_roadmap.assert_called_once()
        call_args = mock_state_manager.store_roadmap.call_args
        assert call_args[0][0] == 'project-123'  # project_id
        assert isinstance(call_args[0][1], RoadMap)  # roadmap instance
        assert call_args[0][1].name == 'My Roadmap'

    @pytest.mark.parametrize(
        'project_id,roadmap_name',
        [
            ('simple-project', 'Simple Roadmap'),
            ('project-with-special-chars!@#', 'Roadmap with émojis 🚀'),
            ('', 'Empty Project ID Test'),
            ('very-long-project-id-' + 'x' * 50, 'Long name test'),
        ],
    )
    def test_create_roadmap_handles_various_inputs(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, project_id: str, roadmap_name: str
    ) -> None:
        mock_state_manager.store_roadmap.return_value = project_id

        result = roadmap_tools.create_roadmap(project_id, roadmap_name)

        assert result.status == OperationStatus.SUCCESS
        assert result.id == project_id
        assert roadmap_name in result.message


class TestGetRoadmap(TestRoadmapTools):
    def test_get_roadmap_returns_success_with_spec_count(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_roadmap = RoadMap(name='Test Roadmap')
        mock_roadmap.specs = {'spec1': Mock(), 'spec2': Mock(), 'spec3': Mock()}
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        result = roadmap_tools.get_roadmap('test-project')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project'
        assert result.status == OperationStatus.SUCCESS
        assert 'Test Roadmap' in result.message
        assert '3 specs' in result.message

    def test_get_roadmap_returns_error_when_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.get_roadmap.side_effect = RoadmapNotFoundError('Not found')

        result = roadmap_tools.get_roadmap('non-existent-project')

        assert isinstance(result, OperationResponse)
        assert result.id == 'non-existent-project'
        assert result.status == OperationStatus.ERROR
        assert 'Error retrieving roadmap' in result.message

    def test_get_roadmap_handles_empty_roadmap(self, roadmap_tools: RoadmapTools, mock_state_manager: Mock) -> None:
        mock_roadmap = RoadMap(name='Empty Roadmap')
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        result = roadmap_tools.get_roadmap('empty-project')

        assert result.status == OperationStatus.SUCCESS
        assert '0 specs' in result.message


class TestAddSpec(TestRoadmapTools):
    def test_add_spec_returns_success_response(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.return_value = 'User Authentication'

        result = roadmap_tools.add_spec('test-project', 'Auth Spec', valid_spec_markdown)

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project-User Authentication'
        assert result.status == OperationStatus.SUCCESS
        assert 'Auth Spec' in result.message
        assert 'test-project' in result.message

    def test_add_spec_parses_markdown_before_storing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.return_value = 'Parsed Spec'

        roadmap_tools.add_spec('test-project', 'Display Name', valid_spec_markdown)

        mock_state_manager.store_spec.assert_called_once()
        call_args = mock_state_manager.store_spec.call_args
        assert call_args[0][0] == 'test-project'
        assert isinstance(call_args[0][1], InitialSpec)
        # Check that markdown was parsed correctly
        parsed_spec = call_args[0][1]
        assert parsed_spec.name == 'User Authentication'  # From markdown title
        assert 'Implement secure user authentication' in parsed_spec.objectives

    def test_add_spec_handles_malformed_markdown(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, malformed_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.return_value = 'Unnamed Spec'

        result = roadmap_tools.add_spec('test-project', 'Bad Spec', malformed_spec_markdown)

        # Should still succeed with fallback values
        assert result.status == OperationStatus.SUCCESS
        mock_state_manager.store_spec.assert_called_once()

    def test_add_spec_returns_error_on_storage_failure(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.side_effect = RoadmapNotFoundError('Roadmap not found')

        result = roadmap_tools.add_spec('non-existent-project', 'Spec Name', valid_spec_markdown)

        assert isinstance(result, OperationResponse)
        assert result.status == OperationStatus.ERROR
        assert 'Error adding spec' in result.message

    @pytest.mark.parametrize(
        'project_id,spec_name',
        [
            ('proj1', 'Simple Spec'),
            ('project-with-dashes', 'Spec with Special Chars: <>{}'),
            ('123', 'Numeric spec name 456'),
        ],
    )
    def test_add_spec_handles_various_identifiers(
        self,
        roadmap_tools: RoadmapTools,
        mock_state_manager: Mock,
        valid_spec_markdown: str,
        project_id: str,
        spec_name: str,
    ) -> None:
        mock_state_manager.store_spec.return_value = spec_name

        result = roadmap_tools.add_spec(project_id, spec_name, valid_spec_markdown)

        assert result.status == OperationStatus.SUCCESS
        assert project_id in result.id
        assert spec_name in result.message


class TestGetSpec(TestRoadmapTools):
    def test_get_spec_returns_success_response(self, roadmap_tools: RoadmapTools, mock_state_manager: Mock) -> None:
        mock_spec = InitialSpec(
            name='Test Spec',
            objectives='Test',
            scope='Test',
            dependencies='Test',
            deliverables='Test',
            architecture='Test',
        )
        mock_state_manager.get_spec.return_value = mock_spec

        result = roadmap_tools.get_spec('test-project', 'Test Spec')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project-Test Spec'
        assert result.status == OperationStatus.SUCCESS
        assert 'Test Spec' in result.message
        assert 'test-project' in result.message

    def test_get_spec_returns_not_found_when_spec_missing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.get_spec.side_effect = SpecNotFoundError('Spec not found')

        result = roadmap_tools.get_spec('test-project', 'Missing Spec')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project-Missing Spec'
        assert result.status == OperationStatus.NOT_FOUND
        assert 'Error retrieving spec' in result.message

    def test_get_spec_returns_not_found_when_roadmap_missing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.get_spec.side_effect = RoadmapNotFoundError('Roadmap not found')

        result = roadmap_tools.get_spec('missing-project', 'Any Spec')

        assert result.status == OperationStatus.NOT_FOUND
        assert 'Error retrieving spec' in result.message


class TestUpdateSpec(TestRoadmapTools):
    def test_update_spec_returns_success_response(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_roadmap = RoadMap(name='Test Roadmap')
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        result = roadmap_tools.update_spec('test-project', 'Auth Spec', valid_spec_markdown)

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project-Auth Spec'
        assert result.status == OperationStatus.SUCCESS
        assert 'Auth Spec' in result.message
        assert 'test-project' in result.message

    def test_update_spec_parses_markdown_and_updates_roadmap(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_roadmap = Mock()
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        roadmap_tools.update_spec('test-project', 'Update Spec', valid_spec_markdown)

        # Should get roadmap and call add_spec with parsed InitialSpec
        mock_state_manager.get_roadmap.assert_called_once_with('test-project')
        mock_roadmap.add_spec.assert_called_once()
        added_spec = mock_roadmap.add_spec.call_args[0][0]
        assert isinstance(added_spec, InitialSpec)
        assert added_spec.name == 'User Authentication'

    def test_update_spec_returns_error_on_roadmap_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.get_roadmap.side_effect = RoadmapNotFoundError('Not found')

        result = roadmap_tools.update_spec('missing-project', 'Spec', valid_spec_markdown)

        assert isinstance(result, OperationResponse)
        assert result.status == OperationStatus.ERROR
        assert 'Error updating spec' in result.message

    def test_update_spec_handles_malformed_markdown(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, malformed_spec_markdown: str
    ) -> None:
        mock_roadmap = Mock()
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        result = roadmap_tools.update_spec('test-project', 'Bad Spec', malformed_spec_markdown)

        # Should still succeed with fallback parsing
        assert result.status == OperationStatus.SUCCESS
        mock_roadmap.add_spec.assert_called_once()


class TestListSpecs(TestRoadmapTools):
    def test_list_specs_returns_success_with_spec_names(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.list_specs.return_value = ['Spec A', 'Spec B', 'Spec C']

        result = roadmap_tools.list_specs('test-project')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project'
        assert result.status == OperationStatus.SUCCESS
        assert 'Spec A, Spec B, Spec C' in result.message
        assert 'test-project' in result.message

    def test_list_specs_handles_empty_roadmap(self, roadmap_tools: RoadmapTools, mock_state_manager: Mock) -> None:
        mock_state_manager.list_specs.return_value = []

        result = roadmap_tools.list_specs('empty-project')

        assert result.status == OperationStatus.SUCCESS
        assert 'No specs found' in result.message

    def test_list_specs_returns_error_when_roadmap_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.list_specs.side_effect = RoadmapNotFoundError('Not found')

        result = roadmap_tools.list_specs('missing-project')

        assert isinstance(result, OperationResponse)
        assert result.status == OperationStatus.ERROR
        assert 'Error listing specs' in result.message

    @pytest.mark.parametrize(
        'spec_names,expected_message_part',
        [
            (['Single Spec'], 'Single Spec'),
            (['First', 'Second'], 'First, Second'),
            (['Alpha', 'Beta', 'Gamma', 'Delta'], 'Alpha, Beta, Gamma, Delta'),
            ([], 'No specs found'),
        ],
    )
    def test_list_specs_formats_different_spec_counts(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, spec_names: list[str], expected_message_part: str
    ) -> None:
        mock_state_manager.list_specs.return_value = spec_names

        result = roadmap_tools.list_specs('test-project')

        assert result.status == OperationStatus.SUCCESS
        assert expected_message_part in result.message


class TestDeleteSpec(TestRoadmapTools):
    def test_delete_spec_returns_success_when_spec_deleted(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = True

        result = roadmap_tools.delete_spec('test-project', 'Target Spec')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project-Target Spec'
        assert result.status == OperationStatus.SUCCESS
        assert 'Deleted spec' in result.message
        assert 'Target Spec' in result.message
        assert 'test-project' in result.message

    def test_delete_spec_returns_not_found_when_spec_missing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = False

        result = roadmap_tools.delete_spec('test-project', 'Missing Spec')

        assert isinstance(result, OperationResponse)
        assert result.id == 'test-project-Missing Spec'
        assert result.status == OperationStatus.NOT_FOUND
        assert 'not found' in result.message

    def test_delete_spec_returns_error_when_roadmap_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.side_effect = RoadmapNotFoundError('Not found')

        result = roadmap_tools.delete_spec('missing-project', 'Any Spec')

        assert isinstance(result, OperationResponse)
        assert result.status == OperationStatus.ERROR
        assert 'Error deleting spec' in result.message

    def test_delete_spec_delegates_correctly_to_state_manager(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = True

        roadmap_tools.delete_spec('project-123', 'spec-456')

        mock_state_manager.delete_spec.assert_called_once_with('project-123', 'spec-456')

    @pytest.mark.parametrize(
        'delete_result,expected_status',
        [
            (True, OperationStatus.SUCCESS),
            (False, OperationStatus.NOT_FOUND),
        ],
    )
    def test_delete_spec_maps_boolean_result_to_status(
        self,
        roadmap_tools: RoadmapTools,
        mock_state_manager: Mock,
        delete_result: bool,
        expected_status: OperationStatus,
    ) -> None:
        mock_state_manager.delete_spec.return_value = delete_result

        result = roadmap_tools.delete_spec('test-project', 'test-spec')

        assert result.status == expected_status


class TestRoadmapToolsIntegration(TestRoadmapTools):
    def test_complete_spec_lifecycle_workflow(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        # Setup mock returns for complete workflow
        mock_roadmap = Mock()
        mock_spec = InitialSpec(
            name='Workflow Spec',
            objectives='Test',
            scope='Test',
            dependencies='Test',
            deliverables='Test',
            architecture='Test',
        )

        mock_state_manager.store_roadmap.return_value = 'workflow-project'
        mock_state_manager.store_spec.return_value = 'Workflow Spec'
        mock_state_manager.get_spec.return_value = mock_spec
        mock_state_manager.get_roadmap.return_value = mock_roadmap
        mock_state_manager.delete_spec.return_value = True

        # Execute workflow
        create_result = roadmap_tools.create_roadmap('workflow-project', 'Workflow Roadmap')
        add_result = roadmap_tools.add_spec('workflow-project', 'Workflow Spec', valid_spec_markdown)
        get_result = roadmap_tools.get_spec('workflow-project', 'Workflow Spec')
        update_result = roadmap_tools.update_spec('workflow-project', 'Workflow Spec', valid_spec_markdown)
        delete_result = roadmap_tools.delete_spec('workflow-project', 'Workflow Spec')

        # All operations should succeed
        assert create_result.status == OperationStatus.SUCCESS
        assert add_result.status == OperationStatus.SUCCESS
        assert get_result.status == OperationStatus.SUCCESS
        assert update_result.status == OperationStatus.SUCCESS
        assert delete_result.status == OperationStatus.SUCCESS

        # Verify state manager was called appropriately
        mock_state_manager.store_roadmap.assert_called_once()
        mock_state_manager.store_spec.assert_called_once()
        mock_state_manager.get_spec.assert_called_once()
        mock_state_manager.get_roadmap.assert_called_once()
        mock_state_manager.delete_spec.assert_called_once()

    def test_error_scenarios_return_appropriate_responses(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        # Setup different error scenarios
        mock_state_manager.get_roadmap.side_effect = RoadmapNotFoundError('Roadmap not found')
        mock_state_manager.get_spec.side_effect = SpecNotFoundError('Spec not found')
        mock_state_manager.store_spec.side_effect = Exception('Storage failed')
        mock_state_manager.list_specs.side_effect = RoadmapNotFoundError('Roadmap not found')
        mock_state_manager.delete_spec.side_effect = Exception('Delete failed')

        # Test error responses
        get_roadmap_result = roadmap_tools.get_roadmap('missing-project')
        get_spec_result = roadmap_tools.get_spec('test-project', 'missing-spec')
        add_spec_result = roadmap_tools.add_spec('test-project', 'spec', valid_spec_markdown)
        list_specs_result = roadmap_tools.list_specs('missing-project')
        delete_spec_result = roadmap_tools.delete_spec('test-project', 'spec')

        # All should return error responses
        assert get_roadmap_result.status == OperationStatus.ERROR
        assert get_spec_result.status == OperationStatus.NOT_FOUND
        assert add_spec_result.status == OperationStatus.ERROR
        assert list_specs_result.status == OperationStatus.ERROR
        assert delete_spec_result.status == OperationStatus.ERROR

        # All should have descriptive error messages
        assert 'Error retrieving roadmap' in get_roadmap_result.message
        assert 'Error retrieving spec' in get_spec_result.message
        assert 'Error adding spec' in add_spec_result.message
        assert 'Error listing specs' in list_specs_result.message
        assert 'Error deleting spec' in delete_spec_result.message
