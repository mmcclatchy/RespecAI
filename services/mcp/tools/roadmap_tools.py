from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError

from services.models.initial_spec import InitialSpec
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

    def add_spec(self, project_id: str, spec_name: str, spec_markdown: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not spec_name:
            raise ToolError('Spec name cannot be empty')
        if not spec_markdown:
            raise ToolError('Spec markdown cannot be empty')

        try:
            spec = InitialSpec.parse_markdown(spec_markdown)
            self.state.store_initial_spec(project_id, spec)
            return f'Added spec "{spec_name}" to project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to add spec: {str(e)}')

    def get_spec(self, project_id: str, spec_name: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not spec_name:
            raise ToolError('Spec name cannot be empty')

        try:
            self.state.get_initial_spec(project_id, spec_name)
            return f'Retrieved spec "{spec_name}" from project {project_id}'
        except Exception as e:
            raise ResourceError(f'Spec "{spec_name}" not found in project {project_id}: {str(e)}')

    def update_spec(self, project_id: str, spec_name: str, spec_markdown: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not spec_name:
            raise ToolError('Spec name cannot be empty')
        if not spec_markdown:
            raise ToolError('Spec markdown cannot be empty')

        try:
            spec = InitialSpec.parse_markdown(spec_markdown)
            # Use state manager to store the updated spec
            self.state.store_initial_spec(project_id, spec)
            return f'Updated spec "{spec_name}" in project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to update spec: {str(e)}')

    def list_specs(self, project_id: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')

        try:
            spec_names = self.state.list_initial_specs(project_id)
            spec_list = ', '.join(spec_names) if spec_names else 'No specs found'
            return f'Specs in project {project_id}: {spec_list}'
        except Exception as e:
            raise ResourceError(f'Failed to list specs for project {project_id}: {str(e)}')

    def delete_spec(self, project_id: str, spec_name: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not spec_name:
            raise ToolError('Spec name cannot be empty')

        try:
            was_deleted = self.state.delete_initial_spec(project_id, spec_name)
            if was_deleted:
                return f'Deleted spec "{spec_name}" from project {project_id}'
            else:
                raise ResourceError(f'Spec "{spec_name}" not found in project {project_id}')
        except Exception as e:
            raise ToolError(f'Failed to delete spec: {str(e)}')


def register_roadmap_tools(mcp: FastMCP) -> None:
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


roadmap_tools = RoadmapTools(state_manager)
