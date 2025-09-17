from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from pydantic import ValidationError

from services.models.project_plan import ProjectPlan
from services.utils.enums import LoopStatus, LoopType
from services.utils.errors import LoopNotFoundError
from services.utils.models import LoopState, MCPResponse
from services.utils.state_manager import StateManager


from services.shared import state_manager


class ProjectPlanTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state
        self._project_plans: dict[str, ProjectPlan] = {}

    def create_project_plan(self, project_plan: ProjectPlan) -> MCPResponse:
        try:
            if project_plan is None:
                raise ValueError('ProjectPlan cannot be None')

            loop_state = LoopState(loop_type=LoopType.PLAN)
            self.state.add_loop(loop_state)
            self._project_plans[loop_state.id] = project_plan
            return MCPResponse(
                id=loop_state.id,
                status=loop_state.status,
                message=f'Created project plan: {project_plan.project_name}',
            )
        except ValidationError:
            raise ToolError('Invalid project plan data provided')
        except ValueError:
            raise ToolError('Invalid project plan: cannot be None')
        except Exception as e:
            raise ToolError(f'Unexpected error creating project plan: {str(e)}')

    def store_project_plan(self, project_plan: ProjectPlan, loop_id: str) -> MCPResponse:
        try:
            if project_plan is None:
                raise ValueError('ProjectPlan cannot be None')

            loop_state = self.state.get_loop(loop_id)
            self._project_plans[loop_id] = project_plan
            return MCPResponse(
                id=loop_id, status=loop_state.status, message=f'Stored project plan: {project_plan.project_name}'
            )
        except ValidationError:
            raise ToolError('Invalid project plan data provided')
        except ValueError:
            raise ToolError('Invalid project plan: cannot be None')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error storing project plan: {str(e)}')

    def get_project_plan_data(self, loop_id: str) -> ProjectPlan:
        try:
            # Check if loop exists
            self.state.get_loop(loop_id)

            if loop_id not in self._project_plans:
                raise ResourceError('No project plan stored for this loop')

            return self._project_plans[loop_id]
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except (ResourceError, ToolError):
            raise  # Re-raise FastMCP exceptions as-is
        except Exception as e:
            raise ToolError(f'Unexpected error retrieving project plan: {str(e)}')

    def get_project_plan_markdown(self, loop_id: str) -> MCPResponse:
        try:
            loop_state = self.state.get_loop(loop_id)
            project_plan = self.get_project_plan_data(loop_id)

            markdown = project_plan.build_markdown()
            return MCPResponse(id=loop_id, status=loop_state.status, message=markdown)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error generating markdown: {str(e)}')

    def list_project_plans(self, count: int = 10) -> MCPResponse:
        try:
            if not self._project_plans:
                return MCPResponse(id='list', status=LoopStatus.INITIALIZED, message='No project plans found')

            # Get recent plans (limited by count)
            plan_items = list(self._project_plans.items())[-count:]
            plan_count = len(plan_items)

            plan_summaries = []
            for loop_id, plan in plan_items:
                summary = f'ID: {loop_id}, Project: {plan.project_name}'
                plan_summaries.append(summary)

            message = f'Found {plan_count} project plan{"s" if plan_count != 1 else ""}: ' + '; '.join(plan_summaries)
            return MCPResponse(id='list', status=LoopStatus.COMPLETED, message=message)
        except Exception as e:
            raise ToolError(f'Unexpected error listing project plans: {str(e)}')

    def delete_project_plan(self, loop_id: str) -> MCPResponse:
        try:
            # Check if loop exists
            self.state.get_loop(loop_id)

            # Remove project plan
            if loop_id in self._project_plans:
                plan_name = self._project_plans[loop_id].project_name
                del self._project_plans[loop_id]
            else:
                plan_name = 'Unknown'
            return MCPResponse(id=loop_id, status=LoopStatus.COMPLETED, message=f'Deleted project plan: {plan_name}')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error deleting project plan: {str(e)}')


def register_project_plan_tools(mcp: FastMCP) -> None:
    project_plan_tools = ProjectPlanTools(state_manager)

    @mcp.tool()
    async def create_project_plan(project_plan_markdown: str, ctx: Context) -> MCPResponse:
        """Create a new project plan with a new loop.

        Parses markdown content into a ProjectPlan model and creates it with
        a new loop automatically.

        Parameters:
        - project_plan_markdown: Complete project plan in markdown format

        Returns:
        - MCPResponse: Contains new loop_id, status, and confirmation message
        """
        await ctx.info('Creating new project plan with auto-generated loop')

        try:
            # Parse markdown into ProjectPlan model
            project_plan = ProjectPlan.parse_markdown(project_plan_markdown)
            result = project_plan_tools.create_project_plan(project_plan)

            await ctx.info(f'Created project plan with ID: {result.id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to create project plan: {str(e)}')
            raise ToolError(f'Failed to create project plan: {str(e)}')

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
