from fastmcp.exceptions import ResourceError, ToolError
from pydantic import ValidationError

from services.models.project_plan import ProjectPlan
from services.utils.enums import LoopStatus, LoopType
from services.utils.errors import LoopNotFoundError
from services.utils.models import LoopState, MCPResponse
from services.utils.state_manager import StateManager


class ProjectPlanTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state
        self._project_plans: dict[str, ProjectPlan] = {}

    def store_project_plan(self, project_plan: ProjectPlan, loop_id: str | None = None) -> MCPResponse:
        try:
            if project_plan is None:
                raise ValueError('ProjectPlan cannot be None')

            if loop_id:
                # Update existing loop
                loop_state = self.state.get_loop(loop_id)
                self._project_plans[loop_id] = project_plan
                return MCPResponse(
                    id=loop_id, status=loop_state.status, message=f'Updated project plan: {project_plan.project_name}'
                )
            else:
                # Create new loop
                loop_state = LoopState(loop_type=LoopType.PLAN)
                self.state.add_loop(loop_state)
                self._project_plans[loop_state.id] = project_plan
                return MCPResponse(
                    id=loop_state.id,
                    status=loop_state.status,
                    message=f'Stored project plan: {project_plan.project_name}',
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
