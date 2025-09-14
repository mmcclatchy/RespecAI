from services.shared import state_manager
from services.utils.enums import OperationStatus
from services.utils.models import InitialSpec, OperationResponse, RoadMap
from services.utils.state_manager import StateManager


class RoadmapTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def create_roadmap(self, project_id: str, roadmap_name: str) -> OperationResponse:
        roadmap = RoadMap(name=roadmap_name)
        stored_id = self.state.store_roadmap(project_id, roadmap)
        return OperationResponse(
            id=stored_id,
            status=OperationStatus.SUCCESS,
            message=f'Created roadmap "{roadmap_name}" for project {project_id}',
        )

    def get_roadmap(self, project_id: str) -> OperationResponse:
        try:
            roadmap = self.state.get_roadmap(project_id)
            spec_count = len(roadmap.specs)
            return OperationResponse(
                id=project_id,
                status=OperationStatus.SUCCESS,
                message=f'Roadmap "{roadmap.name}" found with {spec_count} specs',
            )
        except Exception as e:
            return OperationResponse(
                id=project_id, status=OperationStatus.ERROR, message=f'Error retrieving roadmap: {str(e)}'
            )

    def add_spec(self, project_id: str, spec_name: str, spec_markdown: str) -> OperationResponse:
        try:
            spec = InitialSpec.parse_markdown(spec_markdown)
            stored_name = self.state.store_spec(project_id, spec)
            return OperationResponse(
                id=f'{project_id}-{stored_name}',
                status=OperationStatus.SUCCESS,
                message=f'Added spec "{spec_name}" to project {project_id}',
            )
        except Exception as e:
            return OperationResponse(
                id=f'{project_id}-{spec_name}', status=OperationStatus.ERROR, message=f'Error adding spec: {str(e)}'
            )

    def get_spec(self, project_id: str, spec_name: str) -> OperationResponse:
        try:
            self.state.get_spec(project_id, spec_name)
            return OperationResponse(
                id=f'{project_id}-{spec_name}',
                status=OperationStatus.SUCCESS,
                message=f'Retrieved spec "{spec_name}" from project {project_id}',
            )
        except Exception as e:
            return OperationResponse(
                id=f'{project_id}-{spec_name}',
                status=OperationStatus.NOT_FOUND,
                message=f'Error retrieving spec: {str(e)}',
            )

    def update_spec(self, project_id: str, spec_name: str, spec_markdown: str) -> OperationResponse:
        try:
            spec = InitialSpec.parse_markdown(spec_markdown)
            roadmap = self.state.get_roadmap(project_id)
            roadmap.add_spec(spec)  # This will overwrite existing spec

            return OperationResponse(
                id=f'{project_id}-{spec_name}',
                status=OperationStatus.SUCCESS,
                message=f'Updated spec "{spec_name}" in project {project_id}',
            )
        except Exception as e:
            return OperationResponse(
                id=f'{project_id}-{spec_name}', status=OperationStatus.ERROR, message=f'Error updating spec: {str(e)}'
            )

    def list_specs(self, project_id: str) -> OperationResponse:
        try:
            spec_names = self.state.list_specs(project_id)
            spec_list = ', '.join(spec_names) if spec_names else 'No specs found'

            return OperationResponse(
                id=project_id, status=OperationStatus.SUCCESS, message=f'Specs in project {project_id}: {spec_list}'
            )
        except Exception as e:
            return OperationResponse(
                id=project_id, status=OperationStatus.ERROR, message=f'Error listing specs: {str(e)}'
            )

    def delete_spec(self, project_id: str, spec_name: str) -> OperationResponse:
        try:
            was_deleted = self.state.delete_spec(project_id, spec_name)
            if was_deleted:
                return OperationResponse(
                    id=f'{project_id}-{spec_name}',
                    status=OperationStatus.SUCCESS,
                    message=f'Deleted spec "{spec_name}" from project {project_id}',
                )
            else:
                return OperationResponse(
                    id=f'{project_id}-{spec_name}',
                    status=OperationStatus.NOT_FOUND,
                    message=f'Spec "{spec_name}" not found in project {project_id}',
                )
        except Exception as e:
            return OperationResponse(
                id=f'{project_id}-{spec_name}', status=OperationStatus.ERROR, message=f'Error deleting spec: {str(e)}'
            )


roadmap_tools = RoadmapTools(state_manager)
