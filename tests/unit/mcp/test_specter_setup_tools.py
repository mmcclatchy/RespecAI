from pathlib import Path

import pytest


from services.mcp.tools.specter_setup_tools import SpecterSetupTools
from services.platform.platform_orchestrator import PlatformOrchestrator
import json
from typing import Literal, cast


class TestSpecterSetupTools:
    def test_generate_specter_setup_returns_all_required_files(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform='linear')

        assert result['success'] is True
        assert result['platform'] == 'linear'
        assert result['project_path'] == '/test/project'
        assert 'files' in result
        assert len(result['files']) > 0
        assert 'total_files' in result
        assert result['total_files'] == len(result['files'])

    def test_generate_specter_setup_includes_all_command_templates(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform='linear')

        command_files = [f for f in result['files'] if f['type'] == 'command']
        command_names = {f['path'].split('/')[-1].replace('.md', '') for f in command_files}

        assert 'specter-plan' in command_names
        assert 'specter-spec' in command_names
        assert 'specter-build' in command_names
        assert 'specter-roadmap' in command_names

    def test_generate_specter_setup_includes_all_agent_templates(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform='linear')

        agent_files = [f for f in result['files'] if f['type'] == 'agent']
        agent_names = {f['path'].split('/')[-1].replace('.md', '') for f in agent_files}

        assert 'specter-plan-analyst' in agent_names
        assert 'specter-plan-critic' in agent_names
        assert 'specter-create-spec' in agent_names
        assert 'specter-roadmap-critic' in agent_names

    def test_generate_specter_setup_includes_platform_config(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform='linear')

        config_files = [f for f in result['files'] if f['type'] == 'config']
        assert len(config_files) == 1

        config_file = config_files[0]
        assert config_file['path'] == '.specter/config/platform.json'
        config_data = json.loads(config_file['content'])
        assert config_data['platform'] == 'linear'
        assert 'created_at' in config_data

    def test_generate_specter_setup_file_paths_are_relative(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform='linear')

        for file_info in result['files']:
            assert not file_info['path'].startswith('/')
            assert file_info['path'].startswith(('.claude/', '.specter/'))

    def test_generate_specter_setup_file_contents_not_empty(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform='linear')

        for file_info in result['files']:
            if file_info['type'] == 'config':
                assert len(file_info['content']) > 50
            else:
                assert len(file_info['content']) > 100
            assert file_info['content'].strip() != ''

    def test_generate_specter_setup_invalid_platform_raises_error(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        invalid_platform = cast(Literal['linear', 'github', 'markdown'], 'invalid-platform')
        with pytest.raises(ValueError, match='invalid-platform'):
            setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform=invalid_platform)

    def test_generate_specter_setup_supports_all_platforms(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        platforms: list[Literal['linear', 'github', 'markdown']] = ['linear', 'github', 'markdown']
        for platform in platforms:
            result = setup_tools.generate_specter_setup(project_path=str(Path('/test/project')), platform=platform)
            assert result['success'] is True
            assert result['platform'] == platform

    def test_validate_specter_setup_detects_missing_commands(self) -> None:
        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.validate_specter_setup(project_path=str(Path('/test/incomplete_project')))

        assert result['success'] is False
        assert 'errors' in result
        assert len(result['errors']) > 0

    def test_validate_specter_setup_passes_for_complete_setup(self, tmp_path: Path) -> None:
        (tmp_path / '.claude' / 'commands').mkdir(parents=True)
        (tmp_path / '.claude' / 'agents').mkdir(parents=True)
        (tmp_path / '.specter' / 'config').mkdir(parents=True)

        (tmp_path / '.claude' / 'commands' / 'specter-plan.md').write_text('# Plan Command')
        (tmp_path / '.claude' / 'commands' / 'specter-spec.md').write_text('# Spec Command')
        (tmp_path / '.claude' / 'commands' / 'specter-build.md').write_text('# Build Command')
        (tmp_path / '.claude' / 'commands' / 'specter-roadmap.md').write_text('# Roadmap Command')

        (tmp_path / '.claude' / 'agents' / 'specter-plan-analyst.md').write_text('# Plan Analyst')
        (tmp_path / '.claude' / 'agents' / 'specter-plan-critic.md').write_text('# Plan Critic')
        (tmp_path / '.claude' / 'agents' / 'specter-create-spec.md').write_text('# Create Spec')
        (tmp_path / '.claude' / 'agents' / 'specter-roadmap-critic.md').write_text('# Roadmap Critic')

        (tmp_path / '.specter' / 'config' / 'platform.json').write_text('{"platform": "linear"}')

        orchestrator = PlatformOrchestrator.create_with_default_config()
        setup_tools = SpecterSetupTools(orchestrator)

        result = setup_tools.validate_specter_setup(project_path=str(tmp_path))

        assert result['success'] is True
        assert 'errors' in result
        assert len(result['errors']) == 0
