from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError

from services.models.roadmap import Roadmap
from services.shared import state_manager
from services.utils.state_manager import StateManager


class RoadmapTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def create_roadmap(self, project_id: str, roadmap_data: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not roadmap_data:
            raise ToolError('Roadmap data cannot be empty')

        try:
            roadmap = Roadmap.parse_markdown(roadmap_data)

            self.state.store_roadmap(project_id, roadmap)
            return f'Created roadmap "{roadmap.project_name}" for project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to create roadmap: {str(e)}')

    def get_roadmap(self, project_id: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')

        try:
            roadmap = self.state.get_roadmap(project_id)
            return roadmap.build_markdown()
        except Exception as e:
            raise ResourceError(f'Roadmap not found for project {project_id}: {str(e)}')


def register_roadmap_tools(mcp: FastMCP) -> None:
    roadmap_tools = RoadmapTools(state_manager)

    @mcp.tool()
    async def create_roadmap(project_id: str, roadmap_name: str, ctx: Context) -> str:
        """Create a new roadmap for a project.

        Parameters:
        - project_id: Project identifier
        - roadmap_name: Roadmap markdown content

        Returns:
        - str: Confirmation message
        """
        await ctx.info(f'Creating roadmap for project {project_id}')
        result = roadmap_tools.create_roadmap(project_id, roadmap_name)
        await ctx.info(f'Created roadmap for project {project_id}')
        return result

    @mcp.tool()
    async def get_roadmap(project_id: str, ctx: Context) -> str:
        """Retrieve roadmap as markdown.

        Parameters:
        - project_id: Project identifier

        Returns:
        - str: Roadmap markdown
        """
        await ctx.info(f'Getting roadmap for project {project_id}')
        result = roadmap_tools.get_roadmap(project_id)
        await ctx.info(f'Got roadmap for project {project_id}')
        return result


roadmap_tools = RoadmapTools(state_manager)
