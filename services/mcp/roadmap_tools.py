from fastmcp.exceptions import ResourceError, ToolError

from services.shared import state_manager
from services.models.roadmap import Roadmap
from services.models.initial_spec import InitialSpec
from services.utils.state_manager import StateManager


from services.models.enums import RoadmapStatus
from datetime import datetime


class RoadmapTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def create_roadmap(self, project_id: str, roadmap_data: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')
        if not roadmap_data:
            raise ToolError('Roadmap data cannot be empty')

        try:
            # Check if this is markdown (contains '# Project Roadmap:') or just a name
            if '# Project Roadmap:' in roadmap_data:
                # New format: full markdown
                roadmap = Roadmap.parse_markdown(roadmap_data)
            else:
                # Legacy format: just a name - create minimal roadmap
                roadmap = Roadmap(
                    project_name=roadmap_data,
                    project_goal='Project Goal not specified',
                    total_duration='Total Duration not specified',
                    team_size='Team Size not specified',
                    roadmap_budget='Budget not specified',
                    specs=[],
                    critical_path_analysis='Critical Path Analysis not specified',
                    key_risks='Key Risks not specified',
                    mitigation_plans='Mitigation Plans not specified',
                    buffer_time='Buffer Time not specified',
                    development_resources='Development Resources not specified',
                    infrastructure_requirements='Infrastructure Requirements not specified',
                    external_dependencies='External Dependencies not specified',
                    quality_assurance_plan='Quality Assurance Plan not specified',
                    technical_milestones='Technical Milestones not specified',
                    business_milestones='Business Milestones not specified',
                    quality_gates='Quality Gates not specified',
                    performance_targets='Performance Targets not specified',
                    roadmap_status=RoadmapStatus.DRAFT,
                    creation_date=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat(),
                    spec_count=0,
                )

            self.state.store_roadmap(project_id, roadmap)
            return f'Created roadmap "{roadmap.project_name}" for project {project_id}'
        except Exception as e:
            raise ToolError(f'Failed to create roadmap: {str(e)}')

    def get_roadmap(self, project_id: str) -> str:
        if not project_id:
            raise ToolError('Project ID cannot be empty')

        try:
            roadmap = self.state.get_roadmap(project_id)
            spec_count = len(roadmap.specs)
            return f'Roadmap "{roadmap.project_name}" found with {spec_count} specs'
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
            # Use state manager to store the updated spec
            self.state.store_spec(project_id, spec)
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
