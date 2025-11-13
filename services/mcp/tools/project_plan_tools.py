from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from pydantic import ValidationError

from services.models.project_plan import ProjectPlan
from services.shared import state_manager
from services.utils.enums import LoopStatus
from services.utils.loop_state import MCPResponse
from services.utils.state_manager import StateManager


class ProjectPlanTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state
        self._project_plans: dict[str, ProjectPlan] = {}  # "project_path:project_name" -> ProjectPlan

    def create_project_plan(self, project_path: str, project_plan: ProjectPlan) -> MCPResponse:
        try:
            if project_plan is None:
                raise ValueError('ProjectPlan cannot be None')

            project_name = project_plan.project_name
            if not project_name or project_name == 'Unnamed Project':
                raise ValueError('Project plan must have a valid project name')

            # Scope storage by project_path
            storage_key = f'{project_path}:{project_name}'
            self._project_plans[storage_key] = project_plan
            return MCPResponse(
                id=project_name,
                status=LoopStatus.INITIALIZED,
                message=f'Created project plan: {project_name}',
            )
        except ValidationError:
            raise ToolError('Invalid project plan data provided')
        except ValueError as e:
            raise ToolError(f'Invalid project plan: {str(e)}')
        except Exception as e:
            raise ToolError(f'Unexpected error creating project plan: {str(e)}')

    def store_project_plan(self, project_path: str, project_plan: ProjectPlan, project_name: str) -> MCPResponse:
        try:
            if project_plan is None:
                raise ValueError('ProjectPlan cannot be None')
            if not project_name:
                raise ValueError('Project name cannot be empty')

            # Scope storage by project_path
            storage_key = f'{project_path}:{project_name}'
            self._project_plans[storage_key] = project_plan
            return MCPResponse(
                id=project_name,
                status=LoopStatus.IN_PROGRESS,
                message=f'Stored project plan: {project_plan.project_name}',
            )
        except ValidationError:
            raise ToolError('Invalid project plan data provided')
        except ValueError as e:
            raise ToolError(f'Invalid project plan: {str(e)}')
        except Exception as e:
            raise ToolError(f'Unexpected error storing project plan: {str(e)}')

    def get_project_plan_data(self, project_path: str, project_name: str) -> ProjectPlan:
        try:
            if not project_name:
                raise ToolError('Project name cannot be empty')

            storage_key = f'{project_path}:{project_name}'
            if storage_key not in self._project_plans:
                raise ResourceError(f'No project plan found for project: {project_name}')

            return self._project_plans[storage_key]
        except (ResourceError, ToolError):
            raise  # Re-raise FastMCP exceptions as-is
        except Exception as e:
            raise ToolError(f'Unexpected error retrieving project plan: {str(e)}')

    def get_project_plan_markdown(self, project_path: str, project_name: str) -> MCPResponse:
        try:
            project_plan = self.get_project_plan_data(project_path, project_name)
            markdown = project_plan.build_markdown()
            return MCPResponse(id=project_name, status=LoopStatus.COMPLETED, message=markdown)
        except Exception as e:
            raise ToolError(f'Unexpected error generating markdown: {str(e)}')

    def list_project_plans(self, project_path: str, count: int = 10) -> MCPResponse:
        try:
            # Filter plans for this project only
            project_plans = {k: v for k, v in self._project_plans.items() if k.startswith(f'{project_path}:')}

            if not project_plans:
                return MCPResponse(id='list', status=LoopStatus.INITIALIZED, message='No project plans found')

            # Get recent plans (limited by count)
            plan_items = list(project_plans.items())[-count:]
            plan_count = len(plan_items)

            plan_summaries = []
            for storage_key, plan in plan_items:
                # Extract project name from storage key (format: "project_path:project_name")
                project_name = storage_key.split(':', 1)[1]
                summary = f'Project: {project_name}, Status: {plan.project_status.value}'
                plan_summaries.append(summary)

            message = f'Found {plan_count} project plan{"s" if plan_count != 1 else ""}: ' + '; '.join(plan_summaries)
            return MCPResponse(id='list', status=LoopStatus.COMPLETED, message=message)
        except Exception as e:
            raise ToolError(f'Unexpected error listing project plans: {str(e)}')

    def delete_project_plan(self, project_path: str, project_name: str) -> MCPResponse:
        try:
            if not project_name:
                raise ToolError('Project name cannot be empty')

            # Remove project plan
            storage_key = f'{project_path}:{project_name}'
            if storage_key in self._project_plans:
                del self._project_plans[storage_key]
                return MCPResponse(
                    id=project_name, status=LoopStatus.COMPLETED, message=f'Deleted project plan: {project_name}'
                )
            else:
                raise ResourceError(f'No project plan found for project: {project_name}')
        except (ResourceError, ToolError):
            raise  # Re-raise FastMCP exceptions as-is
        except Exception as e:
            raise ToolError(f'Unexpected error deleting project plan: {str(e)}')


def register_project_plan_tools(mcp: FastMCP) -> None:
    project_plan_tools = ProjectPlanTools(state_manager)

    @mcp.tool()
    async def create_project_plan(project_path: str, project_plan_markdown: str, ctx: Context) -> MCPResponse:
        """Create a new project plan with a new loop.

        Parses markdown content into a ProjectPlan model and creates it with
        a new loop automatically.

        Parameters:
        - project_path: Absolute path to project directory
        - project_plan_markdown: Complete project plan in markdown format

        Returns:
        - MCPResponse: Contains new loop_id, status, and confirmation message
        """
        await ctx.info(f'Creating new project plan for project: {project_path}')

        try:
            # Parse markdown into ProjectPlan model
            project_plan = ProjectPlan.parse_markdown(project_plan_markdown)
            result = project_plan_tools.create_project_plan(project_path, project_plan)

            await ctx.info(f'Created project plan with ID: {result.id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to create project plan: {str(e)}')
            raise ToolError(f'Failed to create project plan: {str(e)}')

    @mcp.tool()
    async def store_project_plan(
        project_path: str, project_name: str, project_plan_markdown: str, ctx: Context
    ) -> MCPResponse:
        """Store structured project plan data from markdown.

        Parses markdown content into a ProjectPlan model and stores it with
        the specified project name.

        Parameters:
        - project_path: Absolute path to project directory
        - project_name: Project name to store the project plan for
        - project_plan_markdown: Complete project plan in markdown format

        Returns:
        - MCPResponse: Contains project_name, status, and confirmation message
        """

        await ctx.info(f'Parsing and storing project plan markdown for project: {project_name} at {project_path}')

        try:
            # Parse markdown into ProjectPlan model
            project_plan = ProjectPlan.parse_markdown(project_plan_markdown)
            result = project_plan_tools.store_project_plan(project_path, project_plan, project_name)

            await ctx.info(f'Stored project plan with ID: {result.id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to store project plan: {str(e)}')
            raise ToolError(f'Failed to store project plan: {str(e)}')

    @mcp.tool()
    async def get_project_plan_markdown(project_path: str, project_name: str, ctx: Context) -> MCPResponse:
        """Generate markdown for project plan.

        Retrieves stored project plan and formats as markdown

        Parameters:
        - project_path: Absolute path to project directory
        - project_name: Name of the project

        Returns:
        - MCPResponse: Contains project_name, status, and formatted markdown content
        """
        await ctx.info(f'Generating markdown for project plan {project_name} at {project_path}')
        try:
            result = project_plan_tools.get_project_plan_markdown(project_path, project_name)
            await ctx.info(f'Generated markdown for project plan {project_name}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to generate project plan markdown: {str(e)}')
            raise ResourceError(f'Project plan not found for project {project_name}: {str(e)}')

    @mcp.tool()
    async def list_project_plans(project_path: str, count: int, ctx: Context) -> MCPResponse:
        """List available project plans.

        Returns summary of stored project plans with basic metadata.

        Parameters:
        - project_path: Absolute path to project directory
        - count: Maximum number of plans to return

        Returns:
        - MCPResponse: Contains list status and project plan summaries
        """
        await ctx.info(f'Listing up to {count} project plans for {project_path}')
        try:
            result = project_plan_tools.list_project_plans(project_path, count)
            await ctx.info('Retrieved project plan list')
            return result
        except Exception as e:
            await ctx.error(f'Failed to list project plans: {str(e)}')
            raise ToolError(f'Failed to list project plans: {str(e)}')

    @mcp.tool()
    async def delete_project_plan(project_path: str, project_name: str, ctx: Context) -> MCPResponse:
        """Delete a stored project plan.

        Removes project plan data associated with the given project name.

        Parameters:
        - project_path: Absolute path to project directory
        - project_name: Name of the project

        Returns:
        - MCPResponse: Contains project_name, status, and deletion confirmation
        """
        await ctx.info(f'Deleting project plan {project_name} at {project_path}')
        try:
            result = project_plan_tools.delete_project_plan(project_path, project_name)
            await ctx.info(f'Deleted project plan {project_name}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to delete project plan: {str(e)}')
            raise ToolError(f'Failed to delete project plan: {str(e)}')
