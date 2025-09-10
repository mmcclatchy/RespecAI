from fastmcp import FastMCP, Context
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware
from fastmcp.server.middleware import MiddlewareContext
import logging

from services.mcp.loop_tools import loop_tools
from services.utils.models import HealthStatus, MCPResponse
from services.utils.setting_configs import mcp_settings
from services.utils.enums import HealthState


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

    @mcp.tool()
    async def decide_loop_next_action(loop_id: str, current_score: int, ctx: Context) -> MCPResponse:
        """Decide next action for refinement loop progression.

        This MCP tool implements the core decision logic for quality-driven
        refinement loops. It analyzes current quality scores, improvement trends,
        and iteration counts to determine whether to continue refining content,
        complete the loop, or escalate to human input.

        Parameters:
        - loop_id: Unique identifier of the loop to process
        - current_score: Quality score from 0-100 for current iteration

        Returns:
        - MCPResponse: Contains loop_id and status ('completed', 'refine', 'user_input')
        """
        await ctx.info(f'Processing decision for loop {loop_id} with score {current_score}')
        result = loop_tools.decide_loop_next_action(loop_id, current_score)
        await ctx.info(f'Decision result for loop {loop_id}: {result.status}')
        return result

    @mcp.tool()
    async def initialize_refinement_loop(loop_type: str, ctx: Context) -> MCPResponse:
        """Initialize a new refinement loop.

        Creates a new refinement loop session.
        Returns loop ID for tracking and managing the loop state throughout
        the refinement process.

        Parameters:
        - loop_type: One of 'plan', 'spec', 'build_plan', 'build_code'

        Returns:
        - MCPResponse: Contains loop_id and status ('initialized')
        """
        await ctx.info(f'Initializing new {loop_type} loop')
        result = loop_tools.initialize_refinement_loop(loop_type)
        await ctx.info(f'Created {loop_type} loop with ID: {result.id}')
        return result

    @mcp.tool()
    async def get_loop_status(loop_id: str, ctx: Context) -> MCPResponse:
        """Get current status and history of a loop.

        Returns complete loop information including current status,
        iteration count, score history, and metadata.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Complete loop state with all metadata and history
        """
        await ctx.info(f'Retrieving status for loop {loop_id}')
        result = loop_tools.get_loop_status(loop_id)
        await ctx.info(f'Retrieved status for loop {loop_id}: {result.status}')
        return result

    @mcp.tool()
    async def list_active_loops(ctx: Context) -> list[MCPResponse]:
        """List all currently active refinement loops.

        Returns summary information for all active loops in the current
        session. Useful for managing multiple concurrent refinement processes.

        Returns:
        - list[MCPResponse]: List of active loops with their current status
        """
        await ctx.info('Retrieving list of active loops')
        result = loop_tools.list_active_loops()
        await ctx.info(f'Found {len(result)} active loops')
        return result

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
