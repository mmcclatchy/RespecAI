import json
from pathlib import Path

from services.mcp.tools.specter_setup_tools import SpecterSetupTools
from services.platform.platform_orchestrator import PlatformOrchestrator


class TestSpecterSetupEndToEnd:
    def test_full_linear_project_setup_workflow(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = str(tmp_path / 'test_project')
        result = setup_tools.generate_specter_setup(project_path=project_path, platform='linear')

        assert result['success'] is True
        assert result['platform'] == 'linear'
        assert result['total_files'] > 0

        (tmp_path / 'test_project' / '.claude' / 'commands').mkdir(parents=True)
        (tmp_path / 'test_project' / '.claude' / 'agents').mkdir(parents=True)
        (tmp_path / 'test_project' / '.specter' / 'config').mkdir(parents=True)

        for file_info in result['files']:
            file_path = tmp_path / 'test_project' / file_info['path']
            file_path.write_text(file_info['content'])

        validation_result = setup_tools.validate_specter_setup(project_path)

        assert validation_result['success'] is True
        assert len(validation_result['errors']) == 0

    def test_full_github_project_setup_workflow(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = str(tmp_path / 'test_project')
        result = setup_tools.generate_specter_setup(project_path=project_path, platform='github')

        assert result['success'] is True
        assert result['platform'] == 'github'

        (tmp_path / 'test_project' / '.claude' / 'commands').mkdir(parents=True)
        (tmp_path / 'test_project' / '.claude' / 'agents').mkdir(parents=True)
        (tmp_path / 'test_project' / '.specter' / 'config').mkdir(parents=True)

        for file_info in result['files']:
            file_path = tmp_path / 'test_project' / file_info['path']
            file_path.write_text(file_info['content'])

        validation_result = setup_tools.validate_specter_setup(project_path)

        assert validation_result['success'] is True

    def test_full_markdown_project_setup_workflow(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = str(tmp_path / 'test_project')
        result = setup_tools.generate_specter_setup(project_path=project_path, platform='markdown')

        assert result['success'] is True
        assert result['platform'] == 'markdown'

        (tmp_path / 'test_project' / '.claude' / 'commands').mkdir(parents=True)
        (tmp_path / 'test_project' / '.claude' / 'agents').mkdir(parents=True)
        (tmp_path / 'test_project' / '.specter' / 'config').mkdir(parents=True)

        for file_info in result['files']:
            file_path = tmp_path / 'test_project' / file_info['path']
            file_path.write_text(file_info['content'])

        validation_result = setup_tools.validate_specter_setup(project_path)

        assert validation_result['success'] is True

    def test_command_templates_contain_platform_specific_tools(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = str(tmp_path / 'test_project')

        for platform in ['linear', 'github', 'markdown']:
            result = setup_tools.generate_specter_setup(
                project_path=project_path,
                platform=platform,  # type: ignore[arg-type]
            )

            spec_command = next(f for f in result['files'] if f['path'] == '.claude/commands/specter-spec.md')

            if platform == 'linear':
                assert 'mcp__linear-server__create_issue' in spec_command['content']
            elif platform == 'github':
                assert 'mcp__github__create_issue' in spec_command['content']
            elif platform == 'markdown':
                assert 'Write' in spec_command['content']

    def test_agent_templates_contain_platform_specific_tools(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = str(tmp_path / 'test_project')

        for platform in ['linear', 'github', 'markdown']:
            result = setup_tools.generate_specter_setup(
                project_path=project_path,
                platform=platform,  # type: ignore[arg-type]
            )

            create_spec_agent = next(f for f in result['files'] if f['path'] == '.claude/agents/specter-create-spec.md')

            if platform == 'linear':
                assert 'mcp__linear-server__create_issue' in create_spec_agent['content']
            elif platform == 'github':
                assert 'mcp__github__create_issue' in create_spec_agent['content']
            elif platform == 'markdown':
                assert 'Write' in create_spec_agent['content']

    def test_platform_config_contains_correct_metadata(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = str(tmp_path / 'test_project')
        result = setup_tools.generate_specter_setup(project_path=project_path, platform='linear')

        config_file = next(f for f in result['files'] if f['path'] == '.specter/config/platform.json')

        config_data = json.loads(config_file['content'])

        assert config_data['platform'] == 'linear'
        assert 'created_at' in config_data
        assert config_data['version'] == '1.0'

    def test_validation_detects_missing_command_file(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = tmp_path / 'incomplete_project'
        (project_path / '.claude' / 'commands').mkdir(parents=True)
        (project_path / '.claude' / 'agents').mkdir(parents=True)
        (project_path / '.specter' / 'config').mkdir(parents=True)

        (project_path / '.claude' / 'commands' / 'specter-plan.md').write_text('# Plan')
        (project_path / '.claude' / 'commands' / 'specter-build.md').write_text('# Build')

        (project_path / '.claude' / 'agents' / 'specter-plan-analyst.md').write_text('# Analyst')
        (project_path / '.claude' / 'agents' / 'specter-plan-critic.md').write_text('# Critic')
        (project_path / '.claude' / 'agents' / 'specter-create-spec.md').write_text('# Spec')
        (project_path / '.claude' / 'agents' / 'specter-roadmap-critic.md').write_text('# Roadmap')

        (project_path / '.specter' / 'config' / 'platform.json').write_text('{"platform": "linear"}')

        validation_result = setup_tools.validate_specter_setup(str(project_path))

        assert validation_result['success'] is False
        assert any('specter-spec.md' in error for error in validation_result['errors'])
        assert any('specter-roadmap.md' in error for error in validation_result['errors'])

    def test_validation_detects_missing_agent_file(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = tmp_path / 'incomplete_project'
        (project_path / '.claude' / 'commands').mkdir(parents=True)
        (project_path / '.claude' / 'agents').mkdir(parents=True)
        (project_path / '.specter' / 'config').mkdir(parents=True)

        (project_path / '.claude' / 'commands' / 'specter-plan.md').write_text('# Plan')
        (project_path / '.claude' / 'commands' / 'specter-spec.md').write_text('# Spec')
        (project_path / '.claude' / 'commands' / 'specter-build.md').write_text('# Build')
        (project_path / '.claude' / 'commands' / 'specter-roadmap.md').write_text('# Roadmap')

        (project_path / '.claude' / 'agents' / 'plan-analyst.md').write_text('# Analyst')
        (project_path / '.claude' / 'agents' / 'create-spec.md').write_text('# Spec')

        (project_path / '.specter' / 'config' / 'platform.json').write_text('{"platform": "linear"}')

        validation_result = setup_tools.validate_specter_setup(str(project_path))

        assert validation_result['success'] is False
        assert any('plan-critic.md' in error for error in validation_result['errors'])
        assert any('roadmap-critic.md' in error for error in validation_result['errors'])

    def test_validation_detects_missing_platform_config(self, tmp_path: Path) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        project_path = tmp_path / 'incomplete_project'
        (project_path / '.claude' / 'commands').mkdir(parents=True)
        (project_path / '.claude' / 'agents').mkdir(parents=True)
        (project_path / '.specter' / 'config').mkdir(parents=True)

        (project_path / '.claude' / 'commands' / 'specter-plan.md').write_text('# Plan')
        (project_path / '.claude' / 'commands' / 'specter-spec.md').write_text('# Spec')
        (project_path / '.claude' / 'commands' / 'specter-build.md').write_text('# Build')
        (project_path / '.claude' / 'commands' / 'specter-roadmap.md').write_text('# Roadmap')

        (project_path / '.claude' / 'agents' / 'specter-plan-analyst.md').write_text('# Analyst')
        (project_path / '.claude' / 'agents' / 'specter-plan-critic.md').write_text('# Critic')
        (project_path / '.claude' / 'agents' / 'specter-create-spec.md').write_text('# Spec')
        (project_path / '.claude' / 'agents' / 'specter-roadmap-critic.md').write_text('# Roadmap')

        validation_result = setup_tools.validate_specter_setup(str(project_path))

        assert validation_result['success'] is False
        assert any('platform configuration' in error.lower() for error in validation_result['errors'])
