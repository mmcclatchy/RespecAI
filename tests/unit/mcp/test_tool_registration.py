from unittest.mock import Mock

import pytest
from fastmcp import FastMCP

from services.mcp.tools import register_all_tools


class TestToolRegistration:
    @pytest.fixture
    def mock_mcp(self) -> Mock:
        return Mock(spec=FastMCP)

    def test_register_all_tools_calls_all_registration_functions(self, mock_mcp: Mock) -> None:
        register_all_tools(mock_mcp)

        # Verify that tools are registered by checking mcp.tool() was called
        assert mock_mcp.tool.called
        # Should have 20+ tool registrations based on server.py analysis
        assert mock_mcp.tool.call_count >= 20

    def test_register_all_tools_with_none_raises_error(self) -> None:
        with pytest.raises(AttributeError):
            register_all_tools(None)  # type: ignore

    def test_register_all_tools_handles_invalid_mcp_instance(self) -> None:
        with pytest.raises(AttributeError):
            register_all_tools('not_an_mcp_instance')  # type: ignore
