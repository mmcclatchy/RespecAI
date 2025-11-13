from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from pydantic import ValidationError

from services.models.build_plan import BuildPlan
from services.shared import state_manager
from services.utils.enums import LoopStatus
from services.utils.errors import LoopNotFoundError
from services.utils.loop_state import MCPResponse
from services.utils.state_manager import StateManager


class BuildPlanTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state
        self._build_plans: dict[str, BuildPlan] = {}  # "project_path:loop_id" -> BuildPlan

    def store_build_plan(self, project_path: str, plan: BuildPlan, loop_id: str) -> MCPResponse:
        try:
            if not project_path:
                raise ValueError('Project path cannot be empty')
            loop_state = self.state.get_loop(loop_id)
            if plan is None:
                raise ValueError('BuildPlan cannot be None')

            storage_key = f'{project_path}:{loop_id}'
            self._build_plans[storage_key] = plan
            return MCPResponse(
                id=loop_id,
                status=loop_state.status,
                message=f'Stored build plan: {plan.project_name}',
            )
        except ValidationError:
            raise ToolError('Invalid build plan data provided')
        except ValueError as e:
            raise ToolError(f'Invalid build plan: {str(e)}')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error storing build plan: {str(e)}')

    def get_build_plan_data(self, project_path: str, loop_id: str) -> BuildPlan:
        try:
            if not project_path:
                raise ValueError('Project path cannot be empty')
            self.state.get_loop(loop_id)

            storage_key = f'{project_path}:{loop_id}'
            if storage_key not in self._build_plans:
                raise ResourceError('No build plan stored for this loop')

            return self._build_plans[storage_key]
        except ValueError as e:
            raise ToolError(f'Invalid input: {str(e)}')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except (ResourceError, ToolError):
            raise
        except Exception as e:
            raise ToolError(f'Unexpected error retrieving build plan: {str(e)}')

    def get_build_plan_markdown(self, project_path: str, loop_id: str) -> MCPResponse:
        try:
            if not project_path:
                raise ValueError('Project path cannot be empty')
            loop_state = self.state.get_loop(loop_id)
            build_plan = self.get_build_plan_data(project_path, loop_id)

            markdown = build_plan.build_markdown()
            return MCPResponse(id=loop_id, status=loop_state.status, message=markdown)
        except ValueError as e:
            raise ToolError(f'Invalid input: {str(e)}')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error generating markdown: {str(e)}')

    def list_build_plans(self, project_path: str, count: int = 10) -> MCPResponse:
        try:
            if not project_path:
                raise ValueError('Project path cannot be empty')

            # Filter plans for this project only
            project_plans = {k: v for k, v in self._build_plans.items() if k.startswith(f'{project_path}:')}

            if not project_plans:
                return MCPResponse(id='list', status=LoopStatus.INITIALIZED, message='No build plans found')

            plan_items = list(project_plans.items())[-count:]
            plan_count = len(plan_items)

            plan_summaries = []
            for storage_key, plan in plan_items:
                # Extract loop_id from storage key (format: "project_path:loop_id")
                loop_id = storage_key.split(':', 1)[1]
                summary = f'ID: {loop_id}, Project: {plan.project_name}'
                plan_summaries.append(summary)

            message = f'Found {plan_count} build plan{"s" if plan_count != 1 else ""}: ' + '; '.join(plan_summaries)
            return MCPResponse(id='list', status=LoopStatus.COMPLETED, message=message)
        except ValueError as e:
            raise ToolError(f'Invalid input: {str(e)}')
        except Exception as e:
            raise ToolError(f'Unexpected error listing build plans: {str(e)}')

    def delete_build_plan(self, project_path: str, loop_id: str) -> MCPResponse:
        try:
            if not project_path:
                raise ValueError('Project path cannot be empty')
            self.state.get_loop(loop_id)

            storage_key = f'{project_path}:{loop_id}'
            if storage_key in self._build_plans:
                plan_name = self._build_plans[storage_key].project_name
                del self._build_plans[storage_key]
            else:
                plan_name = 'Unknown'
            return MCPResponse(id=loop_id, status=LoopStatus.COMPLETED, message=f'Deleted build plan: {plan_name}')
        except ValueError as e:
            raise ToolError(f'Invalid input: {str(e)}')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error deleting build plan: {str(e)}')


def register_build_plan_tools(mcp: FastMCP) -> None:
    build_plan_tools = BuildPlanTools(state_manager)

    @mcp.tool()
    async def store_build_plan(project_path: str, loop_id: str, plan_markdown: str, ctx: Context) -> MCPResponse:
        """Store implementation plan from markdown.

        Parses markdown content into a BuildPlan model and stores it with
        the specified loop.

        Parameters:
        - project_path: Absolute path to project directory
        - loop_id: Loop ID to store the build plan in
        - plan_markdown: Complete implementation plan in markdown format

        Returns:
        - MCPResponse: Contains loop_id, status, and confirmation message
        """
        await ctx.info(f'Parsing and storing build plan with loop_id: {loop_id} for project {project_path}')

        try:
            build_plan = BuildPlan.parse_markdown(plan_markdown)
            result = build_plan_tools.store_build_plan(project_path, build_plan, loop_id)

            await ctx.info(f'Stored build plan with ID: {result.id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to store build plan: {str(e)}')
            raise ToolError(f'Failed to store build plan: {str(e)}')

    @mcp.tool()
    async def get_build_plan_markdown(project_path: str, loop_id: str, ctx: Context) -> MCPResponse:
        """Generate markdown for implementation plan.

        Retrieves stored build plan and formats as markdown

        Parameters:
        - project_path: Absolute path to project directory
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and formatted markdown content
        """
        await ctx.info(f'Generating markdown for build plan {loop_id} in project {project_path}')
        try:
            result = build_plan_tools.get_build_plan_markdown(project_path, loop_id)
            await ctx.info(f'Generated markdown for build plan {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to generate build plan markdown: {str(e)}')
            raise ResourceError(f'Build plan not found for loop {loop_id}: {str(e)}')

    @mcp.tool()
    async def list_build_plans(project_path: str, count: int, ctx: Context) -> MCPResponse:
        """List available implementation plans.

        Returns summary of stored build plans with basic metadata.

        Parameters:
        - project_path: Absolute path to project directory
        - count: Maximum number of plans to return

        Returns:
        - MCPResponse: Contains list status and build plan summaries
        """
        await ctx.info(f'Listing up to {count} build plans for project {project_path}')
        try:
            result = build_plan_tools.list_build_plans(project_path, count)
            await ctx.info('Retrieved build plan list')
            return result
        except Exception as e:
            await ctx.error(f'Failed to list build plans: {str(e)}')
            raise ToolError(f'Failed to list build plans: {str(e)}')

    @mcp.tool()
    async def delete_build_plan(project_path: str, loop_id: str, ctx: Context) -> MCPResponse:
        """Delete a stored implementation plan.

        Removes build plan data associated with the given loop ID.

        Parameters:
        - project_path: Absolute path to project directory
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and deletion confirmation
        """
        await ctx.info(f'Deleting build plan {loop_id} from project {project_path}')
        try:
            result = build_plan_tools.delete_build_plan(project_path, loop_id)
            await ctx.info(f'Deleted build plan {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to delete build plan: {str(e)}')
            raise ToolError(f'Failed to delete build plan: {str(e)}')
