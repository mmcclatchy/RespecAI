import pytest
from fastmcp import FastMCP


class TestFastMCPServerIntegration:
    def test_fastmcp_server_initialization(self) -> None:
        from services.mcp.server import create_mcp_server

        server = create_mcp_server()
        assert isinstance(server, FastMCP)
        assert server.name == 'Loop Management Server'

    @pytest.mark.asyncio
    async def test_mcp_tool_registration(self) -> None:
        from services.mcp.server import create_mcp_server

        server = create_mcp_server()

        # Check that all loop management tools are registered
        tools = await server.get_tools()
        expected_tools = [
            'decide_loop_next_action',
            'initialize_refinement_loop',
            'get_loop_status',
            'list_active_loops',
        ]

        for tool_name in expected_tools:
            assert tool_name in tools
            assert tools[tool_name].name == tool_name

    def test_production_server_creation(self) -> None:
        from services.mcp.server import create_mcp_server
        from services.utils.setting_configs import mcp_settings

        # Test server configuration
        assert mcp_settings.server_name == 'Loop Management Server'
        assert mcp_settings.host == '0.0.0.0'
        assert mcp_settings.port == 8000

        # Test server creation
        server = create_mcp_server()
        assert isinstance(server, FastMCP)
        assert server.name == 'Loop Management Server'

    @pytest.mark.asyncio
    async def test_mcp_tool_discovery_and_metadata(self) -> None:
        from services.mcp.server import create_mcp_server

        server = create_mcp_server()
        tools = await server.get_tools()

        # Find decide_loop_next_action tool
        decide_tool = tools.get('decide_loop_next_action')
        assert decide_tool is not None
        assert decide_tool.description is not None
        assert decide_tool.name == 'decide_loop_next_action'

    @pytest.mark.asyncio
    async def test_error_handling_at_server_level(self) -> None:
        from services.mcp.server import create_mcp_server

        server = create_mcp_server()

        # Test calling tool with invalid loop_id
        with pytest.raises(Exception):  # Should raise LoopNotFoundError
            await server._call_tool(
                'decide_loop_next_action',
                {'loop_id': 'nonexistent-id', 'current_score': 80},
            )

    def test_tool_parameter_validation_through_fastmcp(self) -> None:
        from services.mcp.loop_tools import loop_tools

        # Test with valid parameters using new API
        init_result = loop_tools.initialize_refinement_loop('plan')
        result = loop_tools.decide_loop_next_action(init_result.id, 90)

        from services.utils.enums import LoopStatus

        assert result.status == LoopStatus.COMPLETED

    def test_server_configuration_via_pydantic_settings(self) -> None:
        from services.utils.setting_configs import mcp_settings

        assert mcp_settings.server_name == 'Loop Management Server'
        assert mcp_settings.host == '0.0.0.0'
        assert mcp_settings.port == 8000
        assert mcp_settings.debug is False

    @pytest.mark.asyncio
    async def test_health_check_endpoints(self) -> None:
        from services.mcp.server import create_mcp_server, health_check
        from services.utils.models import HealthStatus
        from services.utils.enums import HealthState

        server = create_mcp_server()
        health_status = await health_check(server)

        assert isinstance(health_status, HealthStatus)
        assert health_status.status == HealthState.HEALTHY
        assert health_status.tools_count == 4  # All 4 loop management tools
        assert health_status.error is None
