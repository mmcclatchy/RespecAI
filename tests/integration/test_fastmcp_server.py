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
            'reset_loop_state',
            'get_loop_status',
            'list_active_loops',
        ]

        for tool_name in expected_tools:
            assert tool_name in tools
            assert tools[tool_name].name == tool_name

    def test_production_server_creation(self) -> None:
        from services.mcp.server import create_mcp_server, get_server_config, MCPSettings

        # Test server configuration
        config = get_server_config()
        assert isinstance(config, MCPSettings)
        assert config.server_name == 'Loop Management Server'
        assert config.host == '0.0.0.0'
        assert config.port == 8000

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

        # Test calling tool with invalid parameters
        with pytest.raises(Exception):  # Should raise validation error
            await server._call_tool(
                'decide_loop_next_action',
                {'loop_type': 'invalid_type', 'current_score': -5, 'previous_scores': [], 'iteration': 0},
            )

    def test_tool_parameter_validation_through_fastmcp(self) -> None:
        from services.mcp.loop_tools import decide_loop_next_action

        # Test with valid parameters directly using the service function
        result = decide_loop_next_action(loop_type='plan', current_score=90, previous_scores=[85, 87], iteration=3)
        assert result == 'complete'

    def test_server_configuration_via_pydantic_settings(self) -> None:
        from services.mcp.server import get_server_config, MCPSettings

        config = get_server_config()
        assert isinstance(config, MCPSettings)
        assert config.server_name == 'Loop Management Server'
        assert config.host == '0.0.0.0'
        assert config.port == 8000
        assert config.debug is False

    @pytest.mark.asyncio
    async def test_health_check_endpoints(self) -> None:
        from services.mcp.server import create_mcp_server, health_check, HealthStatus

        server = create_mcp_server()
        health_status = await health_check(server)

        assert isinstance(health_status, HealthStatus)
        assert health_status.status == 'healthy'
        assert health_status.tools_count == 5  # All 5 loop management tools
        assert health_status.error is None
