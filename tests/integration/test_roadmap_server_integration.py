import asyncio

import pytest
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError, ToolError

from services.mcp.roadmap_tools import roadmap_tools
from services.mcp.server import create_mcp_server


class TestRoadmapServerIntegration:
    @pytest.fixture
    def server(self) -> FastMCP:
        return create_mcp_server()

    @pytest.fixture
    def valid_spec_markdown(self) -> str:
        return """# Technical Specification: Integration Test Spec

## Overview
- **Objectives**: Test MCP server integration with roadmap tools
- **Scope**: End-to-end testing of spec lifecycle
- **Dependencies**: MCP server, FastAPI, state management
- **Deliverables**: Complete CRUD operations through MCP interface

## Metadata
- **Status**: draft
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-01
- **Owner**: Test Suite
"""

    def _get_tools_sync(self, server: FastMCP) -> dict:
        return asyncio.run(server.get_tools())

    @pytest.mark.asyncio
    async def test_roadmap_tool_discovery(self, server: FastMCP) -> None:
        tools = await server.get_tools()

        roadmap_tools_list = [
            'create_roadmap',
            'get_roadmap',
            'add_spec',
            'get_spec',
            'update_spec',
            'list_specs',
            'delete_spec',
        ]

        for tool_name in roadmap_tools_list:
            assert tool_name in tools
            tool = tools[tool_name]
            assert tool.name == tool_name
            # Tool may or may not have description, just verify it's registered

    def test_create_roadmap_integration(self, server: FastMCP) -> None:
        # Test that tool is properly registered
        tools = self._get_tools_sync(server)
        assert 'create_roadmap' in tools

        # Test tool functionality through direct call
        result = roadmap_tools.create_roadmap('integration-test-1', 'Integration Test Roadmap')

        assert isinstance(result, str)
        assert 'Integration Test Roadmap' in result
        assert 'integration-test-1' in result
        assert 'Created roadmap' in result

    def test_get_roadmap_integration(self, server: FastMCP) -> None:
        # Setup: create a roadmap first
        roadmap_tools.create_roadmap('integration-test-2', 'Test Roadmap for Get')

        # Test that tool is registered
        tools = self._get_tools_sync(server)
        assert 'get_roadmap' in tools

        # Test tool functionality
        result = roadmap_tools.get_roadmap('integration-test-2')

        assert isinstance(result, str)
        assert 'Test Roadmap for Get' in result
        assert '0 specs' in result

    def test_add_spec_integration(self, server: FastMCP, valid_spec_markdown: str) -> None:
        project_id = 'spec-test-project'

        # Setup: create roadmap first
        roadmap_tools.create_roadmap(project_id, 'Spec Test Roadmap')

        # Test that tool is registered
        tools = self._get_tools_sync(server)
        assert 'add_spec' in tools

        # Test tool functionality
        result = roadmap_tools.add_spec(project_id, 'Test Spec', valid_spec_markdown)

        assert isinstance(result, str)
        assert 'Test Spec' in result
        assert 'Added spec' in result

    def test_get_spec_integration(self, server: FastMCP, valid_spec_markdown: str) -> None:
        project_id = 'get-spec-project'

        # Setup: create roadmap and add spec
        roadmap_tools.create_roadmap(project_id, 'Get Spec Test')
        roadmap_tools.add_spec(project_id, 'Retrievable Spec', valid_spec_markdown)

        # Test that tool is registered
        tools = self._get_tools_sync(server)
        assert 'get_spec' in tools

        # Test tool functionality
        result = roadmap_tools.get_spec(project_id, 'Integration Test Spec')  # Use parsed name from markdown

        assert isinstance(result, str)
        assert 'Retrieved spec' in result
        assert 'Integration Test Spec' in result

    def test_update_spec_integration(self, server: FastMCP, valid_spec_markdown: str) -> None:
        project_id = 'update-spec-project'

        # Setup: create roadmap and add spec
        roadmap_tools.create_roadmap(project_id, 'Update Spec Test')
        roadmap_tools.add_spec(project_id, 'Original Spec', valid_spec_markdown)

        # Test that tool is registered
        tools = self._get_tools_sync(server)
        assert 'update_spec' in tools

        # Update with new markdown
        updated_markdown = valid_spec_markdown.replace('Integration Test Spec', 'Updated Integration Test Spec')

        result = roadmap_tools.update_spec(project_id, 'Updated Name', updated_markdown)

        assert isinstance(result, str)
        assert 'Updated Name' in result
        assert 'Updated spec' in result

    def test_list_specs_integration(self, server: FastMCP, valid_spec_markdown: str) -> None:
        project_id = 'list-specs-project'

        # Setup: create roadmap and add multiple specs
        roadmap_tools.create_roadmap(project_id, 'Multi Spec Roadmap')

        # Add first spec
        roadmap_tools.add_spec(project_id, 'First Spec', valid_spec_markdown)

        # Add second spec with different content
        second_spec_markdown = valid_spec_markdown.replace('Integration Test Spec', 'Second Test Spec')
        roadmap_tools.add_spec(project_id, 'Second Spec', second_spec_markdown)

        # Test that tool is registered
        tools = self._get_tools_sync(server)
        assert 'list_specs' in tools

        # Test tool functionality
        result = roadmap_tools.list_specs(project_id)

        assert isinstance(result, str)
        # Should contain both spec names (parsed from markdown)
        assert 'Integration Test Spec' in result
        assert 'Second Test Spec' in result

    def test_delete_spec_integration(self, server: FastMCP, valid_spec_markdown: str) -> None:
        project_id = 'delete-spec-project'

        # Setup: create roadmap and add spec
        roadmap_tools.create_roadmap(project_id, 'Delete Test Roadmap')
        roadmap_tools.add_spec(project_id, 'Deletable Spec', valid_spec_markdown)

        # Test that tool is registered
        tools = self._get_tools_sync(server)
        assert 'delete_spec' in tools

        # Test tool functionality
        result = roadmap_tools.delete_spec(project_id, 'Integration Test Spec')  # Use parsed name

        assert isinstance(result, str)
        assert 'Deleted spec' in result
        assert 'Integration Test Spec' in result

    def test_complete_roadmap_workflow_integration(self, server: FastMCP, valid_spec_markdown: str) -> None:
        project_id = 'workflow-project'
        spec_name_from_markdown = 'Integration Test Spec'

        # Verify all tools are registered
        tools = self._get_tools_sync(server)
        required_tools = [
            'create_roadmap',
            'get_roadmap',
            'add_spec',
            'get_spec',
            'update_spec',
            'list_specs',
            'delete_spec',
        ]
        for tool_name in required_tools:
            assert tool_name in tools

        # Step 1: Create roadmap
        create_result = roadmap_tools.create_roadmap(project_id, 'Complete Workflow Roadmap')
        assert isinstance(create_result, str)
        assert 'Created roadmap' in create_result

        # Step 2: Verify empty roadmap
        empty_roadmap = roadmap_tools.get_roadmap(project_id)
        assert '0 specs' in empty_roadmap

        # Step 3: Add spec
        add_result = roadmap_tools.add_spec(project_id, 'Workflow Spec', valid_spec_markdown)
        assert isinstance(add_result, str)
        assert 'Added spec' in add_result

        # Step 4: Verify roadmap now has spec
        populated_roadmap = roadmap_tools.get_roadmap(project_id)
        assert '1 specs' in populated_roadmap

        # Step 5: List specs
        list_result = roadmap_tools.list_specs(project_id)
        assert spec_name_from_markdown in list_result

        # Step 6: Get specific spec
        get_result = roadmap_tools.get_spec(project_id, spec_name_from_markdown)
        assert isinstance(get_result, str)
        assert 'Retrieved spec' in get_result

        # Step 7: Update spec (content changes but name stays the same)
        updated_markdown = valid_spec_markdown.replace(
            'End-to-end testing of spec lifecycle', 'Updated end-to-end testing of spec lifecycle'
        )
        update_result = roadmap_tools.update_spec(project_id, 'Updated Display Name', updated_markdown)
        assert isinstance(update_result, str)
        assert 'Updated spec' in update_result

        # Step 8: Delete spec (use original spec name since names don't change)
        delete_result = roadmap_tools.delete_spec(project_id, spec_name_from_markdown)
        assert isinstance(delete_result, str)
        assert 'Deleted spec' in delete_result

        # Step 9: Verify empty roadmap again
        final_roadmap = roadmap_tools.get_roadmap(project_id)
        assert '0 specs' in final_roadmap

    def test_error_handling_integration(self, server: FastMCP) -> None:
        # Verify error handling tools are registered
        tools = self._get_tools_sync(server)
        error_handling_tools = ['get_roadmap', 'add_spec', 'get_spec', 'delete_spec']
        for tool_name in error_handling_tools:
            assert tool_name in tools

        # Test getting non-existent roadmap
        with pytest.raises(ResourceError):
            roadmap_tools.get_roadmap('non-existent-project')

        # Test adding spec to non-existent roadmap
        with pytest.raises(ToolError):
            roadmap_tools.add_spec('missing-project', 'Test Spec', '# Test\n\nSome content')

        # Test getting non-existent spec
        roadmap_tools.create_roadmap('error-test-project', 'Error Test Roadmap')
        with pytest.raises(ResourceError):
            roadmap_tools.get_spec('error-test-project', 'non-existent-spec')

        # Test deleting non-existent spec
        with pytest.raises(ToolError):
            roadmap_tools.delete_spec('error-test-project', 'non-existent-spec')

    def test_server_tools_consistency_integration(self, server: FastMCP) -> None:
        # Test multiple tool discovery calls return same results
        tools1 = self._get_tools_sync(server)
        tools2 = self._get_tools_sync(server)

        assert len(tools1) == len(tools2)
        assert set(tools1.keys()) == set(tools2.keys())

        # Verify all expected roadmap tools are present
        expected_roadmap_tools = [
            'create_roadmap',
            'get_roadmap',
            'add_spec',
            'get_spec',
            'update_spec',
            'list_specs',
            'delete_spec',
        ]

        for tool_name in expected_roadmap_tools:
            assert tool_name in tools1
            assert tool_name in tools2

            # Verify tool metadata consistency
            tool1 = tools1[tool_name]
            tool2 = tools2[tool_name]
            assert tool1.name == tool2.name
            # Description may be None, just verify they're consistent
            assert tool1.description == tool2.description

    def test_roadmap_tools_state_consistency_integration(self, server: FastMCP) -> None:
        # Verify tools are registered
        tools = self._get_tools_sync(server)
        assert len([name for name in tools.keys() if 'roadmap' in name or 'spec' in name]) >= 7

        # Test state consistency across multiple projects
        project_ids = ['consistency-test-1', 'consistency-test-2', 'consistency-test-3']

        # Create multiple projects
        for i, project_id in enumerate(project_ids):
            result = roadmap_tools.create_roadmap(project_id, f'Consistency Test Roadmap {i}')
            assert isinstance(result, str)
            assert 'Created roadmap' in result

        # Verify all projects exist independently
        for i, project_id in enumerate(project_ids):
            result = roadmap_tools.get_roadmap(project_id)
            assert isinstance(result, str)
            assert f'Consistency Test Roadmap {i}' in result

        # Add specs to each project independently
        spec_markdown = """# Technical Specification: Test Spec

## Overview
- **Objectives**: Consistency testing
- **Scope**: Integration validation
- **Dependencies**: None
- **Deliverables**: Consistent state validation

## Metadata
- **Status**: draft
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-01
- **Owner**: Test Suite
"""

        for project_id in project_ids:
            result = roadmap_tools.add_spec(project_id, f'Spec for {project_id}', spec_markdown)
            assert isinstance(result, str)
            assert 'Added spec' in result

        # Verify each project has exactly one spec
        for project_id in project_ids:
            roadmap_result = roadmap_tools.get_roadmap(project_id)
            assert '1 specs' in roadmap_result

            list_result = roadmap_tools.list_specs(project_id)
            assert 'Test Spec' in list_result  # Parsed name from markdown
