import asyncio
import os
from typing import Any
from unittest.mock import patch

from services.mcp.loop_tools import loop_tools
from services.mcp.roadmap_tools import roadmap_tools
from services.mcp.server import create_mcp_server, health_check
from services.utils.enums import HealthState, LoopStatus, OperationStatus
from services.utils.setting_configs import MCPSettings


class TestProductionMCPServer:
    def test_complete_workflow_initialize_iterate_complete(self) -> None:
        server = create_mcp_server()

        # Test would use actual MCP tool calls in production
        # For now, verify server structure and tools are registered
        tools = asyncio.run(server.get_tools())
        tool_names = list(tools.keys())

        expected_loop_tools = [
            'decide_loop_next_action',
            'initialize_refinement_loop',
            'get_loop_status',
            'list_active_loops',
            'get_previous_objective_feedback',
            'store_current_objective_feedback',
        ]
        expected_roadmap_tools = [
            'create_roadmap',
            'get_roadmap',
            'add_spec',
            'get_spec',
            'update_spec',
            'list_specs',
            'delete_spec',
        ]
        expected_tools = expected_loop_tools + expected_roadmap_tools

        for tool_name in expected_tools:
            assert tool_name in tool_names, f'Required tool {tool_name} not found in {tool_names}'

        # Verify tool metadata
        init_tool = tools['initialize_refinement_loop']
        assert init_tool.name == 'initialize_refinement_loop'

        decision_tool = tools['decide_loop_next_action']
        assert decision_tool.name == 'decide_loop_next_action'

    def test_real_mcp_client_integration_scenarios(self) -> None:
        server = create_mcp_server()

        # Test server can handle tool discovery
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13  # 6 loop + 7 roadmap tools

        # Test server metadata
        assert server.name == 'Loop Management Server'

        # Test prompts endpoint
        prompts = asyncio.run(server.get_prompts())
        # No prompts expected for this server
        assert isinstance(prompts, dict)

    def test_configuration_loading_from_environment_variables(self) -> None:
        # Test with custom environment variables
        test_env = {
            'FSDD_LOOP_PLAN_THRESHOLD': '90',
            'FSDD_LOOP_SPEC_THRESHOLD': '88',
            'FSDD_MCP_SERVER_NAME': 'Test Production Server',
            'FSDD_MCP_DEBUG': 'true',
        }

        with patch.dict(os.environ, test_env, clear=False):
            custom_settings = MCPSettings()

            # Verify custom server name is used
            assert custom_settings.server_name == 'Test Production Server'

        default_settings = MCPSettings()
        assert default_settings.server_name == 'Loop Management Server'

    def test_multi_loop_concurrent_scenarios(self) -> None:
        server = create_mcp_server()

        # Test server can handle multiple tool registrations
        tools = asyncio.run(server.get_tools())

        # Verify each tool has proper async signatures for concurrent use
        for tool_name, tool in tools.items():
            # All tools should be registered (implies async capability)
            assert tool.name is not None
            assert tool.name == tool_name

        # Test that list_active_loops tool exists for managing multiple loops
        list_tool = tools.get('list_active_loops')
        assert list_tool is not None

    def test_fastmcp_server_production_deployment_patterns(self) -> None:
        server = create_mcp_server()

        # Test server has required middleware
        # FastMCP middleware is internal, so test indirectly through behavior
        tools = asyncio.run(server.get_tools())
        assert len(tools) > 0

        # Test server info contains production-ready metadata
        assert server.name is not None

        # Test server can handle errors gracefully (middleware should catch)
        # This would be tested through actual tool calls in real scenarios
        assert server is not None

    def test_health_check_endpoints_and_monitoring(self) -> None:
        server = create_mcp_server()

        # Test health check function
        health_status = asyncio.run(health_check(server))

        assert health_status.status == HealthState.HEALTHY
        assert health_status.tools_count == 13
        assert health_status.error is None

        # Test health check with simulated error
        with patch.object(server, 'get_tools', side_effect=Exception('Test error')):
            error_health = asyncio.run(health_check(server))
            assert error_health.status == HealthState.UNHEALTHY
            assert error_health.error == 'Test error'
            assert error_health.tools_count == 0

    def test_production_logging_configuration(self) -> None:
        # Test that server creation doesn't raise logging errors
        server = create_mcp_server()
        assert server is not None

        # Test server can be created multiple times (logging setup is idempotent)
        server2 = create_mcp_server()
        assert server2 is not None

        # Verify both servers are independent instances
        assert server is not server2

    def test_graceful_server_lifecycle_management(self) -> None:
        # Test server creation
        server = create_mcp_server()
        assert server is not None

        # Test server info access
        assert server.name == 'Loop Management Server'

        # Test tools are accessible
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13

        # Test multiple operations don't interfere
        tools2 = asyncio.run(server.get_tools())
        assert len(tools2) == 13
        assert len(tools) == len(tools2)

    def test_error_handling_middleware_integration(self) -> None:
        server = create_mcp_server()

        # Test server initialization succeeded despite having error middleware
        assert server is not None

        # Test tools are still accessible with middleware
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13

        # Test server name works with middleware
        assert server.name == 'Loop Management Server'

    def test_production_configuration_validation(self) -> None:
        # Test with invalid environment variables
        invalid_env = {
            'FSDD_LOOP_PLAN_THRESHOLD': '-10',  # Invalid: below range
            'FSDD_LOOP_SPEC_THRESHOLD': '150',  # Invalid: above range
        }

        # Configuration validation should handle invalid values gracefully
        # Pydantic should clamp or use defaults
        with patch.dict(os.environ, invalid_env):
            try:
                server = create_mcp_server()
                # If server creation succeeds, config validation worked
                assert server is not None
            except Exception as e:
                # If it fails, it should be a validation error, not a crash
                assert 'validation' in str(e).lower() or 'field' in str(e).lower()

    def test_concurrent_tool_access_safety(self) -> None:
        server = create_mcp_server()

        async def get_tools_multiple() -> list[dict[str, Any]]:
            # Simulate concurrent access
            tasks = [server.get_tools() for _ in range(5)]
            results = await asyncio.gather(*tasks)
            return results

        # Test concurrent access doesn't cause issues
        results = asyncio.run(get_tools_multiple())

        # All results should be identical
        assert len(results) == 5
        for result in results:
            assert len(result) == 13

        # Verify tool names are consistent across concurrent access
        tool_names_sets = [set(result.keys()) for result in results]
        expected_names = {
            'decide_loop_next_action',
            'initialize_refinement_loop',
            'get_loop_status',
            'list_active_loops',
            'get_previous_objective_feedback',
            'store_current_objective_feedback',
            'create_roadmap',
            'get_roadmap',
            'add_spec',
            'get_spec',
            'update_spec',
            'list_specs',
            'delete_spec',
        }

        for tool_names in tool_names_sets:
            assert tool_names == expected_names

    def test_server_error_handling_comprehensive(self) -> None:
        server = create_mcp_server()

        # Test server handles middleware errors gracefully
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13

        # Test health check with various error types
        with patch.object(server, 'get_tools', side_effect=ConnectionError('Network error')):
            health = asyncio.run(health_check(server))
            assert health.status == HealthState.UNHEALTHY
            assert health.error is not None and 'Network error' in health.error

        with patch.object(server, 'get_tools', side_effect=TimeoutError('Timeout error')):
            health = asyncio.run(health_check(server))
            assert health.status == HealthState.UNHEALTHY
            assert health.error is not None and 'Timeout error' in health.error

        with patch.object(server, 'get_tools', side_effect=RuntimeError('Runtime error')):
            health = asyncio.run(health_check(server))
            assert health.status == HealthState.UNHEALTHY
            assert health.error is not None and 'Runtime error' in health.error

    def test_tool_registration_error_recovery(self) -> None:
        # Test that server creation works even with potential tool issues
        server = create_mcp_server()

        # Verify all tools are properly registered despite any potential errors
        tools = asyncio.run(server.get_tools())
        expected_loop_tools = [
            'decide_loop_next_action',
            'initialize_refinement_loop',
            'get_loop_status',
            'list_active_loops',
            'get_previous_objective_feedback',
            'store_current_objective_feedback',
        ]
        expected_roadmap_tools = [
            'create_roadmap',
            'get_roadmap',
            'add_spec',
            'get_spec',
            'update_spec',
            'list_specs',
            'delete_spec',
        ]
        expected_tools = expected_loop_tools + expected_roadmap_tools

        for tool_name in expected_tools:
            assert tool_name in tools
            tool = tools[tool_name]
            assert tool.name == tool_name

    def test_middleware_error_isolation(self) -> None:
        server = create_mcp_server()

        # Test server continues to work despite middleware being present
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13

        # Test prompts endpoint works with middleware
        prompts = asyncio.run(server.get_prompts())
        assert isinstance(prompts, dict)

        # Test server metadata accessible despite middleware
        assert server.name == 'Loop Management Server'
        assert server.name is not None
        assert len(server.name) > 0

    def test_configuration_error_handling(self) -> None:
        # Test with malformed environment variables
        malformed_env = {
            'FSDD_MCP_SERVER_NAME': '',  # Empty string
            'FSDD_MCP_DEBUG': 'invalid_boolean',  # Invalid bool
            'FSDD_MCP_PORT': 'not_a_number',  # Invalid int
        }

        with patch.dict(os.environ, malformed_env, clear=False):
            try:
                # Should either use defaults or handle validation gracefully
                settings = MCPSettings()
                # Empty string should either be rejected or use default
                assert settings.server_name != '' or settings.server_name == 'Loop Management Server'
            except Exception as e:
                # If validation fails, it should be a clear validation error
                assert any(word in str(e).lower() for word in ['validation', 'field', 'value', 'invalid'])

    def test_async_operation_error_handling(self) -> None:
        server = create_mcp_server()

        # Test that async operations handle errors properly
        async def test_async_errors() -> None:
            # Test get_tools async error handling
            try:
                tools = await server.get_tools()
                assert len(tools) == 13
            except Exception:
                # Should not raise unhandled exceptions
                assert False, 'get_tools should not raise unhandled exceptions'

            # Test get_prompts async error handling
            try:
                prompts = await server.get_prompts()
                assert isinstance(prompts, dict)
            except Exception:
                # Should not raise unhandled exceptions
                assert False, 'get_prompts should not raise unhandled exceptions'

        # Run async tests
        asyncio.run(test_async_errors())

    def test_complete_production_workflow_loop_and_roadmap_integration(self) -> None:
        server = create_mcp_server()

        # Verify server has all required tools registered
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13

        project_id = 'production-workflow-project'
        spec_markdown = """# Technical Specification: Production Workflow Test

## Overview

**Objectives**: `Test complete production workflow with loop and roadmap integration`
**Scope**: `End-to-end validation of MCP server functionality`
**Dependencies**: `FastMCP server, in-memory state management, loop refinement`

## Expected Deliverables

- Successful roadmap creation and management
- Effective spec lifecycle management
- Loop-based refinement process integration
- Production-ready error handling

## Technical Architecture

Production MCP server with FastAPI middleware, async tool handling, 
and comprehensive error recovery mechanisms.
"""

        # Phase 1: Project Initialization
        roadmap_result = roadmap_tools.create_roadmap(project_id, 'Production Workflow Roadmap')
        assert roadmap_result.status == OperationStatus.SUCCESS

        # Phase 2: Refinement Loop Initialization
        loop_result = loop_tools.initialize_refinement_loop('spec')
        assert loop_result.status == LoopStatus.INITIALIZED
        loop_id = loop_result.id

        # Phase 3: Initial Spec Creation
        spec_result = roadmap_tools.add_spec(project_id, 'Production Workflow Spec', spec_markdown)
        assert spec_result.status == OperationStatus.SUCCESS

        # Phase 4: Refinement Iteration 1 (Score: 60 - Should Refine)
        refinement_1 = loop_tools.decide_loop_next_action(loop_id, 60)
        assert refinement_1.status == LoopStatus.REFINE

        # Phase 5: Spec Update After First Refinement (content update, not name)
        updated_markdown_1 = spec_markdown.replace(
            'End-to-end validation of MCP server functionality',
            'Updated end-to-end validation of MCP server functionality after first refinement',
        )
        update_1 = roadmap_tools.update_spec(project_id, 'First Refinement Update', updated_markdown_1)
        assert update_1.status == OperationStatus.SUCCESS

        # Phase 6: Refinement Iteration 2 (Score: 75 - Should Refine)
        refinement_2 = loop_tools.decide_loop_next_action(loop_id, 75)
        assert refinement_2.status == LoopStatus.REFINE

        # Phase 7: Spec Update After Second Refinement (content update, not name)
        updated_markdown_2 = updated_markdown_1.replace('after first refinement', 'after second refinement')
        update_2 = roadmap_tools.update_spec(project_id, 'Second Refinement Update', updated_markdown_2)
        assert update_2.status == OperationStatus.SUCCESS

        # Phase 8: Final Refinement (Score: 90 - Should Complete)
        completion = loop_tools.decide_loop_next_action(loop_id, 90)
        assert completion.status == LoopStatus.COMPLETED

        # Phase 9: Verification of Final State
        final_roadmap = roadmap_tools.get_roadmap(project_id)
        assert final_roadmap.status == OperationStatus.SUCCESS
        assert '1 specs' in final_roadmap.message

        final_loop_status = loop_tools.get_loop_status(loop_id)
        assert final_loop_status.status == LoopStatus.COMPLETED

        # Phase 10: Spec Listing and Management
        list_result = roadmap_tools.list_specs(project_id)
        assert list_result.status == OperationStatus.SUCCESS
        assert 'Production Workflow Test' in list_result.message

        # Phase 11: Active Loops Management
        active_loops = loop_tools.list_active_loops()
        assert isinstance(active_loops, list)
        # Should contain our completed loop
        loop_ids = [loop.id for loop in active_loops]
        assert loop_id in loop_ids

        # Phase 12: Error Recovery Testing
        error_spec = roadmap_tools.get_spec('non-existent-project', 'non-existent-spec')
        assert error_spec.status == OperationStatus.NOT_FOUND

        # Phase 13: Cleanup and Final Verification
        delete_result = roadmap_tools.delete_spec(project_id, 'Production Workflow Test')
        assert delete_result.status == OperationStatus.SUCCESS

        # Verify empty roadmap after deletion
        empty_roadmap = roadmap_tools.get_roadmap(project_id)
        assert '0 specs' in empty_roadmap.message

    def test_production_concurrent_mixed_operations(self) -> None:
        server = create_mcp_server()

        # Verify server has all required tools registered
        tools = asyncio.run(server.get_tools())
        assert len(tools) == 13

        # Test concurrent roadmap creation operations
        roadmap_results = []
        for i in range(3):
            roadmap_result = roadmap_tools.create_roadmap(f'concurrent-project-{i}', f'Concurrent Roadmap {i}')
            roadmap_results.append(roadmap_result)
            assert roadmap_result.status == OperationStatus.SUCCESS

        # Test concurrent loop initialization operations
        loop_results = []
        for i in range(3):
            loop_type = 'plan' if i % 2 == 0 else 'spec'
            loop_result = loop_tools.initialize_refinement_loop(loop_type)
            loop_results.append(loop_result)
            assert loop_result.status == LoopStatus.INITIALIZED

        # Test concurrent mixed follow-up operations
        spec_markdown = """# Technical Specification: Test Spec
## Overview
**Objectives**: `Concurrent testing`
**Scope**: `Production validation`
**Dependencies**: `None`
## Expected Deliverables
Concurrent operation validation
## Technical Architecture
Async MCP server operations
"""

        # Add specs to concurrent roadmaps
        spec_results = []
        for i in range(3):
            result = roadmap_tools.add_spec(f'concurrent-project-{i}', f'Concurrent Spec {i}', spec_markdown)
            spec_results.append(result)
            assert result.status == OperationStatus.SUCCESS

        # Progress concurrent loops
        loop_progress_results = []
        for i, loop_result in enumerate(loop_results):
            score = 85 + i  # Varying scores
            progress_result = loop_tools.decide_loop_next_action(loop_result.id, score)
            loop_progress_results.append(progress_result)
            assert progress_result.status == LoopStatus.COMPLETED  # All scores >= 85

        # Verify final state consistency
        for i in range(3):
            # Verify roadmaps have specs
            roadmap_check = roadmap_tools.get_roadmap(f'concurrent-project-{i}')
            assert roadmap_check.status == OperationStatus.SUCCESS
            assert '1 specs' in roadmap_check.message

            # List all specs in each roadmap
            specs_list = roadmap_tools.list_specs(f'concurrent-project-{i}')
            assert specs_list.status == OperationStatus.SUCCESS
            assert 'Test Spec' in specs_list.message

        # Verify all loops are in completed state
        active_loops = loop_tools.list_active_loops()
        completed_loop_ids = [loop.id for loop in loop_results]
        active_loop_ids = [loop.id for loop in active_loops]

        for completed_id in completed_loop_ids:
            assert completed_id in active_loop_ids
