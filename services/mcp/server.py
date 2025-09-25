import logging

from fastmcp import FastMCP
from fastmcp.server.middleware import MiddlewareContext
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

from services.mcp.tools import register_all_tools
from services.utils.enums import HealthState
from services.utils.loop_state import HealthStatus
from services.utils.setting_configs import mcp_settings


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(mcp_settings.server_name)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('mcp_errors')

    def handle_error(error: Exception, context: MiddlewareContext) -> None:
        logger.error(f'MCP Error: {type(error).__name__} in {context.method}: {error}')

    mcp.add_middleware(
        ErrorHandlingMiddleware(
            include_traceback=mcp_settings.debug, transform_errors=True, error_callback=handle_error
        )
    )

    mcp.add_middleware(LoggingMiddleware(include_payloads=mcp_settings.debug, max_payload_length=200))

    # Register all tools
    register_all_tools(mcp)

    return mcp


def run_local_server() -> None:
    server = create_mcp_server()
    server.run(transport='stdio')


async def health_check(server: FastMCP) -> HealthStatus:
    try:
        tools = await server.get_tools()
        return HealthStatus(status=HealthState.HEALTHY, tools_count=len(tools))
    except Exception as e:
        return HealthStatus(status=HealthState.UNHEALTHY, error=str(e))
