from unittest.mock import Mock

import pytest
from fastmcp.exceptions import ResourceError, ToolError

from services.mcp.roadmap_tools import RoadmapTools
from services.models.roadmap import Roadmap
from services.models.initial_spec import InitialSpec
from services.utils.state_manager import StateManager


from services.models.enums import RoadmapStatus
from datetime import datetime
from services.models.enums import SpecStatus


def create_test_roadmap_markdown(project_name: str) -> str:
    return f"""# Project Roadmap: {project_name}

## Project Details
- **Project Goal**: Build and deploy {project_name}
- **Total Duration**: 6 months
- **Team Size**: 5 developers
- **Budget**: $100,000

## Specifications


## Risk Assessment
- **Critical Path Analysis**: Critical path analysis pending
- **Key Risks**: Standard development risks
- **Mitigation Plans**: Standard mitigation strategies
- **Buffer Time**: 2 weeks

## Resource Planning
- **Development Resources**: 5 developers, 1 PM
- **Infrastructure Requirements**: AWS cloud infrastructure
- **External Dependencies**: None identified
- **Quality Assurance Plan**: Automated testing and manual QA

## Success Metrics
- **Technical Milestones**: Alpha, Beta, Production release
- **Business Milestones**: User adoption targets
- **Quality Gates**: Code review, testing, security review
- **Performance Targets**: Sub-2s response times

## Metadata
- **Status**: draft
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-01
- **Spec Count**: 0
"""


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
- **Objectives**: Implement secure user authentication system
- **Scope**: Login, logout, session management
- **Dependencies**: Database setup, encryption library
- **Deliverables**: User login/logout endpoints, session management middleware

## Metadata
- **Status**: draft
- **Created**: 2024-01-15
- **Last Updated**: 2024-01-15
- **Owner**: Test Team
"""

    @pytest.fixture
    def malformed_spec_markdown(self) -> str:
        return """# Some title
        
This is not properly formatted spec markdown.
Missing required sections and structure.
"""


class TestCreateRoadmap(TestRoadmapTools):
    def test_create_roadmap_returns_success_message(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.store_roadmap.return_value = 'test-project'
        roadmap_markdown = create_test_roadmap_markdown('Test Roadmap')

        result = roadmap_tools.create_roadmap('test-project', roadmap_markdown)

        assert isinstance(result, str)
        assert 'Test Roadmap' in result
        assert 'test-project' in result
        assert 'Created roadmap' in result

    def test_create_roadmap_delegates_to_state_manager(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.store_roadmap.return_value = 'project-123'
        roadmap_markdown = create_test_roadmap_markdown('My Roadmap')

        roadmap_tools.create_roadmap('project-123', roadmap_markdown)

        mock_state_manager.store_roadmap.assert_called_once()
        call_args = mock_state_manager.store_roadmap.call_args
        assert call_args[0][0] == 'project-123'  # project_id
        assert isinstance(call_args[0][1], Roadmap)  # roadmap instance
        assert call_args[0][1].project_name == 'My Roadmap'

    def test_create_roadmap_raises_error_for_empty_project_id(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        with pytest.raises(ToolError, match='Project ID cannot be empty'):
            roadmap_tools.create_roadmap('', 'Test Roadmap')

    def test_create_roadmap_raises_error_for_empty_roadmap_data(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        with pytest.raises(ToolError, match='Roadmap data cannot be empty'):
            roadmap_tools.create_roadmap('test-project', '')

    @pytest.mark.parametrize(
        'project_id,roadmap_name',
        [
            ('simple-project', 'Simple Roadmap'),
            ('project-with-special-chars!@#', 'Roadmap with émojis 🚀'),
            ('very-long-project-id-' + 'x' * 50, 'Long name test'),
        ],
    )
    def test_create_roadmap_handles_various_inputs(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, project_id: str, roadmap_name: str
    ) -> None:
        mock_state_manager.store_roadmap.return_value = project_id
        roadmap_markdown = create_test_roadmap_markdown(roadmap_name)

        result = roadmap_tools.create_roadmap(project_id, roadmap_markdown)

        assert isinstance(result, str)
        assert roadmap_name in result


class TestGetRoadmap(TestRoadmapTools):
    def test_get_roadmap_returns_success_with_spec_count(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_roadmap = Roadmap(
            project_name='Test Roadmap',
            project_goal='Test goal',
            total_duration='6 months',
            team_size='5 developers',
            roadmap_budget='$100k',
            specs=['spec1', 'spec2', 'spec3'],  # Now a list of strings
            critical_path_analysis='Test analysis',
            key_risks='Test risks',
            mitigation_plans='Test plans',
            buffer_time='1 week',
            development_resources='Test resources',
            infrastructure_requirements='Test infrastructure',
            external_dependencies='Test dependencies',
            quality_assurance_plan='Test QA',
            technical_milestones='Test milestones',
            business_milestones='Test business',
            quality_gates='Test gates',
            performance_targets='Test performance',
            roadmap_status=RoadmapStatus.DRAFT,
            creation_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            spec_count=3,
        )
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        result = roadmap_tools.get_roadmap('test-project')

        assert isinstance(result, str)
        assert 'Test Roadmap' in result
        assert '3 specs' in result

    def test_get_roadmap_raises_error_when_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.get_roadmap.side_effect = Exception('Not found')

        with pytest.raises(ResourceError, match='Roadmap not found for project non-existent-project'):
            roadmap_tools.get_roadmap('non-existent-project')

    def test_get_roadmap_handles_empty_roadmap(self, roadmap_tools: RoadmapTools, mock_state_manager: Mock) -> None:
        mock_roadmap = Roadmap(
            project_name='Empty Roadmap',
            project_goal='Test goal',
            total_duration='6 months',
            team_size='5 developers',
            roadmap_budget='$100k',
            specs=[],  # Empty list
            critical_path_analysis='Test analysis',
            key_risks='Test risks',
            mitigation_plans='Test plans',
            buffer_time='1 week',
            development_resources='Test resources',
            infrastructure_requirements='Test infrastructure',
            external_dependencies='Test dependencies',
            quality_assurance_plan='Test QA',
            technical_milestones='Test milestones',
            business_milestones='Test business',
            quality_gates='Test gates',
            performance_targets='Test performance',
            roadmap_status=RoadmapStatus.DRAFT,
            creation_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            spec_count=0,
        )
        mock_state_manager.get_roadmap.return_value = mock_roadmap

        result = roadmap_tools.get_roadmap('empty-project')

        assert isinstance(result, str)
        assert '0 specs' in result


class TestAddSpec(TestRoadmapTools):
    def test_add_spec_returns_success_message(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.return_value = 'User Authentication'

        result = roadmap_tools.add_spec('test-project', 'Auth Spec', valid_spec_markdown)

        assert isinstance(result, str)
        assert 'Auth Spec' in result
        assert 'test-project' in result
        assert 'Added spec' in result

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
        assert parsed_spec.phase_name == 'User Authentication'  # From markdown title
        assert 'Implement secure user authentication' in parsed_spec.objectives

    def test_add_spec_handles_malformed_markdown(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, malformed_spec_markdown: str
    ) -> None:
        # New parser requires proper format, so malformed markdown should raise error
        with pytest.raises(ToolError, match='Failed to add spec'):
            roadmap_tools.add_spec('test-project', 'Bad Spec', malformed_spec_markdown)

    def test_add_spec_raises_error_on_storage_failure(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.side_effect = Exception('Storage failed')

        with pytest.raises(ToolError, match='Failed to add spec'):
            roadmap_tools.add_spec('non-existent-project', 'Spec Name', valid_spec_markdown)

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

        assert isinstance(result, str)
        assert spec_name in result


class TestGetSpec(TestRoadmapTools):
    def test_get_spec_returns_success_message(self, roadmap_tools: RoadmapTools, mock_state_manager: Mock) -> None:
        mock_spec = InitialSpec(
            phase_name='Test Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            spec_status=SpecStatus.DRAFT,
            creation_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            spec_owner='Test Owner',
        )
        mock_state_manager.get_spec.return_value = mock_spec

        result = roadmap_tools.get_spec('test-project', 'Test Spec')

        assert isinstance(result, str)
        assert 'Test Spec' in result
        assert 'test-project' in result
        assert 'Retrieved spec' in result

    def test_get_spec_raises_error_when_spec_missing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.get_spec.side_effect = Exception('Spec not found')

        with pytest.raises(ResourceError, match='Spec "Missing Spec" not found in project test-project'):
            roadmap_tools.get_spec('test-project', 'Missing Spec')

    def test_get_spec_raises_error_when_roadmap_missing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.get_spec.side_effect = Exception('Roadmap not found')

        with pytest.raises(ResourceError, match='Spec "Any Spec" not found in project missing-project'):
            roadmap_tools.get_spec('missing-project', 'Any Spec')


class TestUpdateSpec(TestRoadmapTools):
    def test_update_spec_returns_success_message(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.return_value = 'User Authentication'

        result = roadmap_tools.update_spec('test-project', 'Auth Spec', valid_spec_markdown)

        assert isinstance(result, str)
        assert 'Auth Spec' in result
        assert 'test-project' in result
        assert 'Updated spec' in result

    def test_update_spec_parses_markdown_and_stores_spec(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.return_value = 'User Authentication'

        roadmap_tools.update_spec('test-project', 'Update Spec', valid_spec_markdown)

        # Should call store_spec with parsed InitialSpec
        mock_state_manager.store_spec.assert_called_once()
        call_args = mock_state_manager.store_spec.call_args
        assert call_args[0][0] == 'test-project'
        assert isinstance(call_args[0][1], InitialSpec)
        stored_spec = call_args[0][1]
        assert stored_spec.phase_name == 'User Authentication'

    def test_update_spec_raises_error_on_storage_failure(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        mock_state_manager.store_spec.side_effect = Exception('Storage failed')

        with pytest.raises(ToolError, match='Failed to update spec'):
            roadmap_tools.update_spec('missing-project', 'Spec', valid_spec_markdown)

    def test_update_spec_handles_malformed_markdown(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, malformed_spec_markdown: str
    ) -> None:
        # New parser requires proper format, so malformed markdown should raise error
        with pytest.raises(ToolError, match='Failed to update spec'):
            roadmap_tools.update_spec('test-project', 'Bad Spec', malformed_spec_markdown)


class TestListSpecs(TestRoadmapTools):
    def test_list_specs_returns_success_with_spec_names(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.list_specs.return_value = ['Spec A', 'Spec B', 'Spec C']

        result = roadmap_tools.list_specs('test-project')

        assert isinstance(result, str)
        assert 'Spec A, Spec B, Spec C' in result
        assert 'test-project' in result

    def test_list_specs_handles_empty_roadmap(self, roadmap_tools: RoadmapTools, mock_state_manager: Mock) -> None:
        mock_state_manager.list_specs.return_value = []

        result = roadmap_tools.list_specs('empty-project')

        assert isinstance(result, str)
        assert 'No specs found' in result

    def test_list_specs_raises_error_when_roadmap_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.list_specs.side_effect = Exception('Not found')

        with pytest.raises(ResourceError, match='Failed to list specs for project missing-project'):
            roadmap_tools.list_specs('missing-project')

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

        assert isinstance(result, str)
        assert expected_message_part in result


class TestDeleteSpec(TestRoadmapTools):
    def test_delete_spec_returns_success_when_spec_deleted(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = True

        result = roadmap_tools.delete_spec('test-project', 'Target Spec')

        assert isinstance(result, str)
        assert 'Deleted spec' in result
        assert 'Target Spec' in result
        assert 'test-project' in result

    def test_delete_spec_raises_error_when_spec_missing(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = False

        with pytest.raises(ToolError, match='Failed to delete spec'):
            roadmap_tools.delete_spec('test-project', 'Missing Spec')

    def test_delete_spec_raises_error_when_roadmap_not_found(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.side_effect = Exception('Not found')

        with pytest.raises(ToolError, match='Failed to delete spec'):
            roadmap_tools.delete_spec('missing-project', 'Any Spec')

    def test_delete_spec_delegates_correctly_to_state_manager(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = True

        roadmap_tools.delete_spec('project-123', 'spec-456')

        mock_state_manager.delete_spec.assert_called_once_with('project-123', 'spec-456')

    def test_delete_spec_returns_success_message_when_deleted(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock
    ) -> None:
        mock_state_manager.delete_spec.return_value = True

        result = roadmap_tools.delete_spec('test-project', 'test-spec')

        assert isinstance(result, str)
        assert 'Deleted spec' in result


class TestRoadmapToolsIntegration(TestRoadmapTools):
    def test_complete_spec_lifecycle_workflow(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        # Setup mock returns for complete workflow
        mock_roadmap = Mock()
        mock_spec = InitialSpec(
            phase_name='Workflow Spec',
            objectives='Test objectives',
            scope='Test scope',
            dependencies='Test dependencies',
            deliverables='Test deliverables',
            spec_status=SpecStatus.DRAFT,
            creation_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            spec_owner='Test Owner',
        )

        mock_state_manager.store_roadmap.return_value = 'workflow-project'
        mock_state_manager.store_spec.return_value = 'Workflow Spec'
        mock_state_manager.get_spec.return_value = mock_spec
        mock_state_manager.get_roadmap.return_value = mock_roadmap
        mock_state_manager.delete_spec.return_value = True

        # Execute workflow
        roadmap_markdown = create_test_roadmap_markdown('Workflow Roadmap')
        create_result = roadmap_tools.create_roadmap('workflow-project', roadmap_markdown)
        add_result = roadmap_tools.add_spec('workflow-project', 'Workflow Spec', valid_spec_markdown)
        get_result = roadmap_tools.get_spec('workflow-project', 'Workflow Spec')
        update_result = roadmap_tools.update_spec('workflow-project', 'Workflow Spec', valid_spec_markdown)
        delete_result = roadmap_tools.delete_spec('workflow-project', 'Workflow Spec')

        # All operations should return success strings
        assert isinstance(create_result, str)
        assert isinstance(add_result, str)
        assert isinstance(get_result, str)
        assert isinstance(update_result, str)
        assert isinstance(delete_result, str)

        # Verify state manager was called appropriately
        mock_state_manager.store_roadmap.assert_called_once()
        # store_spec is called twice: once for add_spec and once for update_spec
        assert mock_state_manager.store_spec.call_count == 2
        mock_state_manager.get_spec.assert_called_once()
        mock_state_manager.delete_spec.assert_called_once()

    def test_error_scenarios_raise_appropriate_exceptions(
        self, roadmap_tools: RoadmapTools, mock_state_manager: Mock, valid_spec_markdown: str
    ) -> None:
        # Test various error scenarios that should raise exceptions
        mock_state_manager.get_roadmap.side_effect = Exception('Roadmap not found')
        with pytest.raises(ResourceError):
            roadmap_tools.get_roadmap('missing-project')

        mock_state_manager.get_spec.side_effect = Exception('Spec not found')
        with pytest.raises(ResourceError):
            roadmap_tools.get_spec('test-project', 'missing-spec')

        mock_state_manager.store_spec.side_effect = Exception('Storage failed')
        with pytest.raises(ToolError):
            roadmap_tools.add_spec('test-project', 'spec', valid_spec_markdown)

        mock_state_manager.list_specs.side_effect = Exception('Roadmap not found')
        with pytest.raises(ResourceError):
            roadmap_tools.list_specs('missing-project')

        mock_state_manager.delete_spec.side_effect = Exception('Delete failed')
        with pytest.raises(ToolError):
            roadmap_tools.delete_spec('test-project', 'spec')
