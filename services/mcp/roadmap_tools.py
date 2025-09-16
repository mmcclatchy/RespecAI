from fastmcp.exceptions import ResourceError, ToolError

from services.shared import state_manager
from services.utils.models import InitialSpec, RoadMap
from services.utils.state_manager import StateManager


class RoadmapTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def create_roadmap(self, project_id: str, roadmap_name: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not roadmap_name:
            raise ToolError('Roadmap name cannot be empty')

        try:
            roadmap = RoadMap(name=roadmap_name)
            self.state.store_roadmap(project_id, roadmap)
            return f'Created roadmap "{roadmap_name}" for project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to create roadmap: {str(e)}')

    def get_roadmap(self, project_id: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')

        try:
            roadmap = self.state.get_roadmap(project_id)
            spec_count = len(roadmap.specs)
            return f'Roadmap "{roadmap.name}" found with {spec_count} specs'
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
            self.state.store_spec(project_id, spec)
            return f'Added spec "{spec_name}" to project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to add spec: {str(e)}')

    def get_spec(self, project_id: str, spec_name: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not spec_name:
            raise ToolError('Spec name cannot be empty')

        try:
            self.state.get_spec(project_id, spec_name)
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
            roadmap = self.state.get_roadmap(project_id)
            roadmap.add_spec(spec)  # This will overwrite existing spec
            return f'Updated spec "{spec_name}" in project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to update spec: {str(e)}')

    def list_specs(self, project_id: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')

        try:
            spec_names = self.state.list_specs(project_id)
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
            was_deleted = self.state.delete_spec(project_id, spec_name)
            if was_deleted:
                return f'Deleted spec "{spec_name}" from project {project_id}'
            else:
                raise ResourceError(f'Spec "{spec_name}" not found in project {project_id}')
        except Exception as e:
            raise ToolError(f'Failed to delete spec: {str(e)}')


roadmap_tools = RoadmapTools(state_manager)
