import logging

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from fastmcp.server.middleware import MiddlewareContext
from fastmcp.server.middleware.error_handling import ErrorHandlingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware

from services.mcp.feedback_tools import FeedbackTools
from services.mcp.loop_tools import loop_tools
from services.mcp.project_plan_tools import ProjectPlanTools
from services.mcp.roadmap_tools import roadmap_tools
from services.models.feedback import CriticFeedback
from services.models.project_plan import ProjectPlan
from services.shared import state_manager
from services.utils.enums import HealthState
from services.utils.models import HealthStatus, MCPResponse
from services.utils.setting_configs import mcp_settings


def create_mcp_server() -> FastMCP:
    mcp = FastMCP(mcp_settings.server_name)

    # Initialize tool instances
    feedback_tools = FeedbackTools(state_manager)
    project_plan_tools = ProjectPlanTools(state_manager)

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

    # ============================================================================
    # LOOP MANAGEMENT TOOLS
    # ============================================================================

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

    @mcp.tool()
    async def get_previous_objective_feedback(loop_id: str, ctx: Context) -> MCPResponse:
        """Retrieve previous objective validation feedback for analyst-critic.

        Returns stored feedback from previous validation cycles to enable
        iterative improvement tracking and consistency assessment.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains previous feedback data with dimension scores and recommendations
        """
        await ctx.info(f'Retrieving previous objective feedback for loop {loop_id}')
        result = loop_tools.get_previous_objective_feedback(loop_id)
        await ctx.info(f'Retrieved objective feedback for loop {loop_id}')
        return result

    @mcp.tool()
    async def store_current_objective_feedback(loop_id: str, feedback: str, ctx: Context) -> MCPResponse:
        """Store current objective validation feedback for analyst-critic.

        Persists validation feedback including dimension scores, specific findings,
        and improvement recommendations for future refinement cycles.

        Parameters:
        - loop_id: Unique identifier of the loop
        - feedback: Complete validation feedback with scores and recommendations

        Returns:
        - MCPResponse: Confirmation of successful storage
        """
        await ctx.info(f'Storing objective feedback for loop {loop_id}')
        result = loop_tools.store_current_objective_feedback(loop_id, feedback)
        await ctx.info(f'Stored objective feedback for loop {loop_id}')
        return result

    @mcp.tool()
    async def get_loop_feedback_summary(loop_id: str, ctx: Context) -> MCPResponse:
        """Get structured feedback summary for loop decision making.

        Provides feedback metrics and trends to support intelligent
        loop progression decisions. Returns score progression,
        feedback count, and recent assessment summaries.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains feedback summary with metrics and trends
        """
        await ctx.info(f'Retrieving feedback summary for loop {loop_id}')
        result = loop_tools.get_loop_feedback_summary(loop_id)
        await ctx.info(f'Retrieved feedback summary for loop {loop_id}')
        return result

    @mcp.tool()
    async def get_loop_improvement_analysis(loop_id: str, ctx: Context) -> MCPResponse:
        """Analyze improvement patterns from structured feedback.

        Examines feedback history to identify improvement trends,
        recurring issues, and recommendation patterns. Supports
        intelligent refinement strategy decisions.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains improvement analysis with trends and patterns
        """
        await ctx.info(f'Retrieving improvement analysis for loop {loop_id}')
        result = loop_tools.get_loop_improvement_analysis(loop_id)
        await ctx.info(f'Retrieved improvement analysis for loop {loop_id}')
        return result

    # ============================================================================
    # FEEDBACK MANAGEMENT TOOLS
    # ============================================================================

    @mcp.tool()
    async def store_critic_feedback(
        loop_id: str,
        feedback_markdown: str,
        ctx: Context,
    ) -> MCPResponse:
        """Store structured critic feedback for any loop type from markdown.

        Parses markdown feedback into structured CriticFeedback and stores it.
        This universal tool works with ALL 5 workflow types and integrates
        with the existing sophisticated LoopState management system.

        Parameters:
        - feedback_markdown: Complete critic feedback in markdown format
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and storage confirmation
        """
        await ctx.info(f'Parsing and storing critic feedback for loop {loop_id}')
        try:
            # Parse markdown into structured feedback using the model's parse method
            feedback = CriticFeedback.parse_markdown(feedback_markdown)

            # Update loop_id to match the provided loop_id
            feedback.loop_id = loop_id

            result = feedback_tools.store_critic_feedback(feedback)
            await ctx.info(f'Stored feedback for loop {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to store critic feedback: {str(e)}')
            raise ToolError(f'Failed to store critic feedback: {str(e)}')

    @mcp.tool()
    async def get_feedback_history(loop_id: str, count: int, ctx: Context) -> MCPResponse:
        """Retrieve recent feedback history for any loop type.

        Returns structured feedback history that critics can use for context
        and consistency across iterations. Works with ALL loop types.

        Parameters:
        - loop_id: Unique identifier of the loop
        - count: Number of recent feedback items to retrieve

        Returns:
        - MCPResponse: Contains loop_id, status, and feedback history
        """
        await ctx.info(f'Retrieving feedback history for loop {loop_id}')
        try:
            result = feedback_tools.get_feedback_history(loop_id, count)
            await ctx.info(f'Retrieved {count} feedback items for loop {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to retrieve feedback history: {str(e)}')
            raise ResourceError(f'Feedback history unavailable for loop {loop_id}: {str(e)}')

    # ============================================================================
    # PROJECT PLAN MANAGEMENT TOOLS
    # ============================================================================

    @mcp.tool()
    async def store_project_plan(loop_id: str, project_plan_markdown: str, ctx: Context) -> MCPResponse:
        """Store structured project plan data from markdown.

        Parses markdown content into a ProjectPlan model and stores it with
        the specified loop.

        Parameters:
        - loop_id: Loop ID to store the project plan in
        - project_plan_markdown: Complete project plan in markdown format

        Returns:
        - MCPResponse: Contains loop_id, status, and confirmation message
        """

        await ctx.info(f'Parsing and storing project plan markdown with loop_id: {loop_id}')

        try:
            # Parse markdown into ProjectPlan model
            project_plan = ProjectPlan.parse_markdown(project_plan_markdown)
            result = project_plan_tools.store_project_plan(project_plan, loop_id)

            await ctx.info(f'Stored project plan with ID: {result.id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to store project plan: {str(e)}')
            raise ToolError(f'Failed to store project plan: {str(e)}')

    @mcp.tool()
    async def get_project_plan_markdown(loop_id: str, ctx: Context) -> MCPResponse:
        """Generate markdown for project plan.

        Retrieves stored project plan and formats as markdown

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and formatted markdown content
        """
        await ctx.info(f'Generating markdown for project plan {loop_id}')
        try:
            result = project_plan_tools.get_project_plan_markdown(loop_id)
            await ctx.info(f'Generated markdown for project plan {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to generate project plan markdown: {str(e)}')
            raise ResourceError(f'Project plan not found for loop {loop_id}: {str(e)}')

    @mcp.tool()
    async def list_project_plans(count: int, ctx: Context) -> MCPResponse:
        """List available project plans.

        Returns summary of stored project plans with basic metadata.

        Parameters:
        - count: Maximum number of plans to return

        Returns:
        - MCPResponse: Contains list status and project plan summaries
        """
        await ctx.info(f'Listing up to {count} project plans')
        try:
            result = project_plan_tools.list_project_plans(count)
            await ctx.info('Retrieved project plan list')
            return result
        except Exception as e:
            await ctx.error(f'Failed to list project plans: {str(e)}')
            raise ToolError(f'Failed to list project plans: {str(e)}')

    @mcp.tool()
    async def delete_project_plan(loop_id: str, ctx: Context) -> MCPResponse:
        """Delete a stored project plan.

        Removes project plan data associated with the given loop ID.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and deletion confirmation
        """
        await ctx.info(f'Deleting project plan {loop_id}')
        try:
            result = project_plan_tools.delete_project_plan(loop_id)
            await ctx.info(f'Deleted project plan {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to delete project plan: {str(e)}')
            raise ToolError(f'Failed to delete project plan: {str(e)}')

    # ============================================================================
    # ROADMAP MANAGEMENT TOOLS
    # ============================================================================

    @mcp.tool()
    async def create_roadmap(project_id: str, roadmap_name: str, ctx: Context) -> str:
        await ctx.info(f'Creating roadmap for project {project_id}')
        result = roadmap_tools.create_roadmap(project_id, roadmap_name)
        await ctx.info(f'Created roadmap for project {project_id}')
        return result

    @mcp.tool()
    async def get_roadmap(project_id: str, ctx: Context) -> str:
        await ctx.info(f'Getting roadmap for project {project_id}')
        result = roadmap_tools.get_roadmap(project_id)
        await ctx.info(f'Got roadmap for project {project_id}')
        return result

    @mcp.tool()
    async def add_spec(project_id: str, spec_name: str, spec_markdown: str, ctx: Context) -> str:
        await ctx.info(f'Storing spec {spec_name} for project {project_id}')
        result = roadmap_tools.add_spec(project_id, spec_name, spec_markdown)
        await ctx.info(f'Stored spec {spec_name} for project {project_id}')
        return result

    @mcp.tool()
    async def get_spec(project_id: str, spec_name: str, ctx: Context) -> str:
        await ctx.info(f'Getting spec {spec_name} for project {project_id}')
        result = roadmap_tools.get_spec(project_id, spec_name)
        await ctx.info(f'Got spec {spec_name} for project {project_id}')
        return result

    @mcp.tool()
    async def update_spec(project_id: str, spec_name: str, spec_markdown: str, ctx: Context) -> str:
        await ctx.info(f'Updating spec {spec_name} for project {project_id}')
        result = roadmap_tools.update_spec(project_id, spec_name, spec_markdown)
        await ctx.info(f'Updated spec {spec_name} for project {project_id}')
        return result

    @mcp.tool()
    async def list_specs(project_id: str, ctx: Context) -> str:
        await ctx.info(f'Listing specs for project {project_id}')
        result = roadmap_tools.list_specs(project_id)
        await ctx.info(f'Listed specs for project {project_id}')
        return result

    @mcp.tool()
    async def delete_spec(project_id: str, spec_name: str, ctx: Context) -> str:
        await ctx.info(f'Deleting spec {spec_name} for project {project_id}')
        result = roadmap_tools.delete_spec(project_id, spec_name)
        await ctx.info(f'Deleted spec {spec_name} for project {project_id}')
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
