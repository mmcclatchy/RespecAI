"""Tests for command template generation functions."""

from services.templates.commands.plan_roadmap_command import generate_plan_roadmap_command_template


class TestPlanRoadmapCommandTemplate:
    def test_template_has_required_tools(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get_tool',
            update_project_plan_tool='test_update_tool',
            create_spec_tool='test_create_tool',
            get_spec_tool='test_get_spec_tool',
            update_spec_tool='test_update_spec_tool',
        )

        # Check YAML frontmatter tools
        assert '- Task(plan-roadmap)' in template
        assert '- Task(roadmap-critic)' in template
        assert '- Task(create-spec)' in template
        assert '- test_get_tool' in template
        assert '- test_create_tool' in template
        assert '- mcp__specter__initialize_refinement_loop' in template
        assert '- mcp__specter__decide_loop_next_action' in template

    def test_template_includes_required_yaml_sections(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        assert '---' in template
        assert 'allowed-tools:' in template
        assert 'argument-hint:' in template
        assert 'description:' in template

    def test_template_is_orchestration_focused(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        # Should contain orchestration keywords
        orchestration_terms = ['Orchestration', 'Workflow', 'Coordination']
        has_orchestration = any(term in template for term in orchestration_terms)
        assert has_orchestration

        # Should NOT contain detailed implementation guidance
        detailed_implementation = [
            'Primary Tasks:',
            '1. Analyze the strategic plan for technical feasibility',
            'Expected Output Format:',
            'Step-by-step implementation sequence',
        ]
        for detail in detailed_implementation:
            assert detail not in template, f'Template should not contain detailed implementation: {detail}'

    def test_template_has_no_quality_thresholds(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        # Should not contain threshold percentages or direct threshold logic
        threshold_terms = ['85%', '90%', 'quality gate', 'threshold:', 'threshold =', 'if score >']
        for term in threshold_terms:
            assert term not in template, f'Template should not reference thresholds: {term}'

    def test_template_includes_parallel_spec_creation(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        # Should include create-spec agent and parallel coordination
        assert 'Task(create-spec)' in template
        assert 'parallel' in template.lower() or 'concurrent' in template.lower()

    def test_template_includes_mcp_action_handling(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        # Should include MCP action patterns
        mcp_actions = ['refine', 'complete', 'user_input']
        for action in mcp_actions:
            assert action in template, f'Template should handle MCP action: {action}'

    def test_template_size_is_reasonable(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        lines = template.split('\n')
        line_count = len(lines)

        # Target is 150-200 lines, allow some flexibility
        assert 100 <= line_count <= 300, f'Template should be 100-300 lines, got {line_count}'

    def test_template_has_no_agent_behavioral_instructions(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        # Should not contain agent behavioral instructions
        behavioral_instructions = [
            'Primary Tasks:',
            '1. Design technical architecture',
            '2. Analyze archive scan results',
            'You will analyze',
            'Your role is to',
            'Consider the implementation',
        ]

        for instruction in behavioral_instructions:
            assert instruction not in template, f'Template should not contain behavioral instruction: {instruction}'

    def test_template_includes_error_handling(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='test_get',
            update_project_plan_tool='test_update',
            create_spec_tool='test_create',
            get_spec_tool='test_get_spec',
            update_spec_tool='test_update_spec',
        )

        # Should include error handling
        error_handling_terms = ['Error Handling', 'ERROR', 'failure', 'graceful']
        has_error_handling = any(term in template for term in error_handling_terms)
        assert has_error_handling, 'Template should include error handling patterns'

    def test_template_maintains_platform_tool_injection(self) -> None:
        template = generate_plan_roadmap_command_template(
            get_project_plan_tool='mcp__linear__get_issue',
            update_project_plan_tool='mcp__linear__update_issue',
            create_spec_tool='mcp__linear__create_issue',
            get_spec_tool='mcp__linear__get_issue',
            update_spec_tool='mcp__linear__update_issue',
        )

        # Should properly inject platform tools
        assert 'mcp__linear__get_issue' in template
        assert 'mcp__linear__create_issue' in template
        assert 'mcp__linear__update_issue' in template
