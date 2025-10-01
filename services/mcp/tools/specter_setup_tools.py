import json
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError

from services.platform.models import CreateSpecAgentTools, PlanRoadmapAgentTools
from services.platform.platform_orchestrator import PlatformOrchestrator
from services.platform.platform_selector import PlatformType
from services.platform.tool_enums import AbstractOperation, CommandTemplate
from services.platform.tool_registry import ToolRegistry
from services.templates.agents.analyst_critic import generate_analyst_critic_template
from services.templates.agents.create_spec import generate_create_spec_template
from services.templates.agents.plan_analyst import generate_plan_analyst_template
from services.templates.agents.plan_critic import generate_plan_critic_template
from services.templates.agents.plan_roadmap import generate_plan_roadmap_template
from services.templates.agents.roadmap_critic import generate_roadmap_critic_template


class SpecterSetupTools:
    def __init__(self, orchestrator: PlatformOrchestrator) -> None:
        self.orchestrator = orchestrator

    def generate_specter_setup(
        self, project_path: str, platform: Literal['linear', 'github', 'markdown']
    ) -> dict[str, Any]:
        try:
            platform_type = PlatformType(platform)
        except ValueError:
            raise ValueError(f'Invalid platform: {platform}')

        files: list[dict[str, str]] = []

        command_templates = [
            CommandTemplate.PLAN,
            CommandTemplate.SPEC,
            CommandTemplate.BUILD,
            CommandTemplate.PLAN_ROADMAP,
            CommandTemplate.PLAN_CONVERSATION,
        ]

        for cmd in command_templates:
            try:
                content = self.orchestrator.template_coordinator.generate_command_template(cmd, platform_type)
                files.append({'path': f'.claude/commands/{cmd.value}.md', 'content': content, 'type': 'command'})
            except Exception as e:
                raise ToolError(f'Failed to generate command template {cmd.value}: {str(e)}')

        tool_registry = ToolRegistry()

        plan_roadmap_tools = PlanRoadmapAgentTools(
            create_spec_external=tool_registry.get_tool_for_platform(
                AbstractOperation.CREATE_SPEC_TOOL.value, platform_type
            )
        )
        create_spec_tools = CreateSpecAgentTools(
            create_spec_tool=tool_registry.get_tool_for_platform(
                AbstractOperation.CREATE_SPEC_TOOL.value, platform_type
            ),
            get_spec_tool=tool_registry.get_tool_for_platform(AbstractOperation.GET_SPEC_TOOL.value, platform_type),
            update_spec_tool=tool_registry.get_tool_for_platform(
                AbstractOperation.UPDATE_SPEC_TOOL.value, platform_type
            ),
        )

        agent_templates_to_generate = [
            ('specter-plan-analyst', generate_plan_analyst_template()),
            ('specter-plan-critic', generate_plan_critic_template()),
            ('specter-roadmap', generate_plan_roadmap_template(plan_roadmap_tools)),
            ('specter-roadmap-critic', generate_roadmap_critic_template()),
            ('specter-create-spec', generate_create_spec_template(create_spec_tools)),
            ('specter-analyst-critic', generate_analyst_critic_template()),
        ]

        for agent_name, content in agent_templates_to_generate:
            try:
                files.append({'path': f'.claude/agents/{agent_name}.md', 'content': content, 'type': 'agent'})
            except Exception as e:
                raise ToolError(f'Failed to generate agent template {agent_name}: {str(e)}')

        config = {'platform': platform, 'created_at': datetime.now().isoformat(), 'version': '1.0'}
        files.append(
            {'path': '.specter/config/platform.json', 'content': json.dumps(config, indent=2), 'type': 'config'}
        )

        return {
            'success': True,
            'platform': platform,
            'project_path': project_path,
            'files': files,
            'total_files': len(files),
            'instructions': 'Use Write tool to create each file at specified path',
        }

    def validate_specter_setup(self, project_path: str) -> dict[str, Any]:
        project = Path(project_path)
        errors: list[str] = []

        required_commands = ['specter-plan', 'specter-spec', 'specter-build', 'specter-roadmap']
        for cmd in required_commands:
            cmd_path = project / '.claude' / 'commands' / f'{cmd}.md'
            if not cmd_path.exists():
                errors.append(f'Missing command file: {cmd}.md')

        required_agents = [
            'specter-plan-analyst',
            'specter-plan-critic',
            'specter-create-spec',
            'specter-roadmap-critic',
        ]
        for agent in required_agents:
            agent_path = project / '.claude' / 'agents' / f'{agent}.md'
            if not agent_path.exists():
                errors.append(f'Missing agent file: {agent}.md')

        config_path = project / '.specter' / 'config' / 'platform.json'
        if not config_path.exists():
            errors.append('Missing platform configuration file')

        return {'success': len(errors) == 0, 'project_path': project_path, 'errors': errors}


def register_specter_setup_tools(mcp: FastMCP) -> None:
    orchestrator = PlatformOrchestrator.create_with_default_config()
    setup_tools = SpecterSetupTools(orchestrator)

    @mcp.tool()
    async def generate_specter_setup(
        project_path: str, platform: Literal['linear', 'github', 'markdown'], ctx: Context
    ) -> dict[str, Any]:
        """Generate complete Specter setup configuration and templates.

        Returns all file contents for Claude Agent to write. MCP server does NOT
        write files - that's Claude's responsibility via Write/Bash tools.

        Parameters:
        - project_path: Target project directory path
        - platform: Platform choice (linear, github, or markdown)

        Returns:
        - Dictionary containing success status, platform, and list of files with
          paths and contents
        """
        await ctx.info(f'Generating Specter setup for {project_path} with platform {platform}')
        try:
            result = setup_tools.generate_specter_setup(project_path, platform)
            await ctx.info(f'Generated {result["total_files"]} files for Specter setup')
            return result
        except ValueError as e:
            await ctx.error(f'Invalid platform specified: {str(e)}')
            raise ToolError(f'Invalid platform: {str(e)}')
        except Exception as e:
            await ctx.error(f'Failed to generate Specter setup: {str(e)}')
            raise ToolError(f'Failed to generate Specter setup: {str(e)}')

    @mcp.tool()
    async def validate_specter_setup(project_path: str, ctx: Context) -> dict[str, Any]:
        """Validate existing Specter setup is complete.

        Checks for presence of all required command files, agent files, and
        configuration.

        Parameters:
        - project_path: Project directory path to validate

        Returns:
        - Dictionary containing success status and list of any errors found
        """
        await ctx.info(f'Validating Specter setup at {project_path}')
        try:
            result = setup_tools.validate_specter_setup(project_path)
            if result['success']:
                await ctx.info('Specter setup validation passed')
            else:
                await ctx.info(f'Specter setup validation found {len(result["errors"])} errors')
            return result
        except Exception as e:
            await ctx.error(f'Failed to validate Specter setup: {str(e)}')
            raise ToolError(f'Failed to validate Specter setup: {str(e)}')

    @mcp.tool()
    async def get_bootstrap_files(ctx: Context) -> dict[str, Any]:
        """Get Specter bootstrap files for installation.

        Returns the specter-setup command file content. Claude Agent should
        use Write tool to save to .claude/commands/specter-setup.md, then
        user can run /specter-setup <platform> to complete installation.

        This tool enables installation when Specter MCP server is containerized.

        Returns:
        - Dictionary containing file path, content, and installation instructions
        """
        await ctx.info('Retrieving Specter bootstrap files')
        try:
            setup_command_path = (
                Path(__file__).parent.parent.parent.parent / '.claude' / 'commands' / 'specter-setup.md'
            )

            if not setup_command_path.exists():
                raise ToolError(f'Bootstrap command not found at: {setup_command_path}')

            content = setup_command_path.read_text()

            await ctx.info('Bootstrap files retrieved successfully')
            return {
                'success': True,
                'files': [
                    {
                        'path': '.claude/commands/specter-setup.md',
                        'content': content,
                        'description': 'Specter setup command - enables full installation',
                    }
                ],
                'instructions': (
                    'Save this file using Write tool, then run:\n'
                    '  /specter-setup <platform>\n\n'
                    'Platform options: linear, github, markdown\n\n'
                    'To check MCP server availability: /mcp list'
                ),
            }
        except Exception as e:
            await ctx.error(f'Failed to retrieve bootstrap files: {str(e)}')
            raise ToolError(f'Failed to retrieve bootstrap files: {str(e)}')
