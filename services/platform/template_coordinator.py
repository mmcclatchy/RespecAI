import importlib

from .platform_selector import PlatformSelector, PlatformType
from .tool_registry import ToolRegistry
from .tool_enums import CommandTemplate, AbstractOperation


from services.platform.template_helpers import create_plan_command_tools
from services.platform.models import PlanCommandTools
from services.platform.template_helpers import create_spec_command_tools
from services.platform.models import SpecCommandTools
from services.platform.template_helpers import create_build_command_tools
from services.platform.models import BuildCommandTools
from services.platform.template_helpers import create_plan_roadmap_tools
from services.platform.models import PlanRoadmapCommandTools


class TemplateCoordinator:
    def __init__(self) -> None:
        self.platform_selector = PlatformSelector()
        self.tool_registry = ToolRegistry()

        # Template function registry - using dynamic imports to avoid circular imports
        self._template_modules = {
            CommandTemplate.PLAN: ('services.templates.commands.plan_command', 'generate_plan_command_template'),
            CommandTemplate.SPEC: ('services.templates.commands.spec_command', 'generate_spec_command_template'),
            CommandTemplate.BUILD: ('services.templates.commands.build_command', 'generate_build_command_template'),
            CommandTemplate.PLAN_ROADMAP: (
                'services.templates.commands.plan_roadmap_command',
                'generate_plan_roadmap_command_template',
            ),
            CommandTemplate.PLAN_CONVERSATION: (
                'services.templates.commands.plan_conversation_command',
                'generate_plan_conversation_command_template',
            ),
        }

    def generate_command_template(self, command_name: str | CommandTemplate, platform: PlatformType) -> str:
        # Convert string to enum if needed
        if isinstance(command_name, str):
            try:
                command_enum = CommandTemplate(command_name)
            except ValueError:
                raise ValueError(f'Unknown command template: {command_name}')
        else:
            command_enum = command_name

        if command_enum not in self._template_modules:
            raise ValueError(f'Unknown command template: {command_enum.value}')

        # Dynamically import template function to avoid circular imports
        module_name, func_name = self._template_modules[command_enum]
        module = importlib.import_module(module_name)
        template_func = getattr(module, func_name)

        # Get platform-specific tools based on command requirements
        if command_enum == CommandTemplate.PLAN:
            tools = self._get_plan_tools(platform)
            platform_tools = [tools['create_project_external'], tools['create_project_completion_external']]

            tools_yaml = create_plan_command_tools(platform_tools)
            plan_tools = PlanCommandTools(
                tools_yaml=tools_yaml,
                create_project_external=tools['create_project_external'],
                create_project_completion_external=tools['create_project_completion_external'],
            )
            return template_func(plan_tools)

        elif command_enum == CommandTemplate.SPEC:
            tools = self._get_spec_tools(platform)
            platform_tools = [tools['create_spec_tool'], tools['get_spec_tool'], tools['update_spec_tool']]

            tools_yaml = create_spec_command_tools(platform_tools)
            spec_tools = SpecCommandTools(
                tools_yaml=tools_yaml,
                create_spec_tool=tools['create_spec_tool'],
                get_spec_tool=tools['get_spec_tool'],
                update_spec_tool=tools['update_spec_tool'],
            )
            return template_func(spec_tools)

        elif command_enum == CommandTemplate.BUILD:
            tools = self._get_build_tools(platform)
            platform_tools = [tools['get_spec_tool'], tools['comment_spec_tool']]

            tools_yaml = create_build_command_tools(platform_tools)
            build_tools = BuildCommandTools(
                tools_yaml=tools_yaml,
                get_spec_tool=tools['get_spec_tool'],
                comment_spec_tool=tools['comment_spec_tool'],
            )
            return template_func(build_tools)

        elif command_enum == CommandTemplate.PLAN_ROADMAP:
            tools = self._get_roadmap_tools(platform)
            platform_tools = [
                tools['get_project_plan_tool'],
                tools['update_project_plan_tool'],
                tools['create_spec_tool'],
                tools['get_spec_tool'],
                tools['update_spec_tool'],
            ]

            tools_yaml = create_plan_roadmap_tools(platform_tools)
            roadmap_tools = PlanRoadmapCommandTools(
                tools_yaml=tools_yaml,
                get_project_plan_tool=tools['get_project_plan_tool'],
                update_project_plan_tool=tools['update_project_plan_tool'],
                create_spec_tool=tools['create_spec_tool'],
                get_spec_tool=tools['get_spec_tool'],
                update_spec_tool=tools['update_spec_tool'],
            )
            return template_func(roadmap_tools)

        elif command_enum == CommandTemplate.PLAN_CONVERSATION:
            # This command has no platform tools - uses only hardcoded MCP tools
            return template_func()

        else:
            raise ValueError(f'Template generation not implemented for: {command_enum.value}')

    def _get_plan_tools(self, platform: PlatformType) -> dict[str, str]:
        return {
            'create_project_external': self.tool_registry.get_tool_for_platform(
                AbstractOperation.CREATE_PROJECT_EXTERNAL.value, platform
            ),
            'create_project_completion_external': self.tool_registry.get_tool_for_platform(
                AbstractOperation.CREATE_PROJECT_COMPLETION_EXTERNAL.value, platform
            ),
        }

    def _get_spec_tools(self, platform: PlatformType) -> dict[str, str]:
        return {
            'create_spec_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.CREATE_SPEC_TOOL.value, platform
            ),
            'get_spec_tool': self.tool_registry.get_tool_for_platform(AbstractOperation.GET_SPEC_TOOL.value, platform),
            'update_spec_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.UPDATE_SPEC_TOOL.value, platform
            ),
        }

    def _get_build_tools(self, platform: PlatformType) -> dict[str, str]:
        return {
            'get_spec_tool': self.tool_registry.get_tool_for_platform(AbstractOperation.GET_SPEC_TOOL.value, platform),
            'comment_spec_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.COMMENT_SPEC_TOOL.value, platform
            ),
        }

    def _get_roadmap_tools(self, platform: PlatformType) -> dict[str, str]:
        return {
            'get_project_plan_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.GET_PROJECT_PLAN_TOOL.value, platform
            ),
            'update_project_plan_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.UPDATE_PROJECT_PLAN_TOOL.value, platform
            ),
            'create_spec_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.CREATE_SPEC_TOOL.value, platform
            ),
            'get_spec_tool': self.tool_registry.get_tool_for_platform(AbstractOperation.GET_SPEC_TOOL.value, platform),
            'update_spec_tool': self.tool_registry.get_tool_for_platform(
                AbstractOperation.UPDATE_SPEC_TOOL.value, platform
            ),
        }

    def validate_template_generation(self, command_name: str | CommandTemplate, platform: PlatformType) -> bool:
        # Convert string to enum if needed
        if isinstance(command_name, str):
            command_enum = CommandTemplate(command_name)
        else:
            command_enum = command_name

        required_operations = self._get_required_operations(command_enum)
        return self.tool_registry.validate_platform_support(platform, required_operations)

    def _get_required_operations(self, command_template: CommandTemplate) -> list[str]:
        operations_map = {
            CommandTemplate.PLAN: [
                AbstractOperation.CREATE_PROJECT_EXTERNAL.value,
                AbstractOperation.CREATE_PROJECT_COMPLETION_EXTERNAL.value,
            ],
            CommandTemplate.SPEC: [
                AbstractOperation.CREATE_SPEC_TOOL.value,
                AbstractOperation.GET_SPEC_TOOL.value,
                AbstractOperation.UPDATE_SPEC_TOOL.value,
            ],
            CommandTemplate.BUILD: [AbstractOperation.GET_SPEC_TOOL.value, AbstractOperation.COMMENT_SPEC_TOOL.value],
            CommandTemplate.PLAN_ROADMAP: [
                AbstractOperation.GET_PROJECT_PLAN_TOOL.value,
                AbstractOperation.UPDATE_PROJECT_PLAN_TOOL.value,
                AbstractOperation.CREATE_SPEC_TOOL.value,
                AbstractOperation.GET_SPEC_TOOL.value,
                AbstractOperation.UPDATE_SPEC_TOOL.value,
            ],
            CommandTemplate.PLAN_CONVERSATION: [],  # No platform tools required
        }

        return operations_map.get(command_template, [])

    def get_available_commands(self) -> list[str]:
        return [cmd.value for cmd in self._template_modules.keys()]
