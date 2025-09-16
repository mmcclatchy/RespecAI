"""Integration tests for MCP tools with StateManager.

These tests verify end-to-end integration between MCP tools and StateManager
without any mocking, following TDD Red-Green-Refactor methodology.
"""

from datetime import datetime

from services.mcp.feedback_tools import FeedbackTools
from services.mcp.project_plan_tools import ProjectPlanTools
from services.mcp.loop_tools import LoopTools
from services.mcp.roadmap_tools import RoadmapTools
from services.models.feedback import CriticFeedback
from services.models.project_plan import ProjectPlan
from services.models.enums import CriticAgent, ProjectStatus
from services.utils.enums import LoopStatus
from services.utils.state_manager import InMemoryStateManager


class TestFeedbackToolsIntegration:
    def test_store_critic_feedback_end_to_end(self) -> None:
        """Test storing critic feedback through complete integration stack."""
        state_manager = InMemoryStateManager()
        feedback_tools = FeedbackTools(state_manager)
        loop_tools = LoopTools(state_manager)

        # Create a loop first
        loop_response = loop_tools.initialize_refinement_loop('plan')
        loop_id = loop_response.id

        # Create critic feedback
        feedback = CriticFeedback(
            loop_id=loop_id,
            critic_agent=CriticAgent.PLAN_CRITIC,
            iteration=1,
            overall_score=68,  # Based on manual calculation
            assessment_summary='Good start but needs improvement',
            detailed_feedback='The plan shows promise but requires more detail in key areas',
            key_issues=['Lacks detail in objectives', 'Success criteria unclear'],
            recommendations=['Add more detail to objectives', 'Clarify success criteria'],
            timestamp=datetime.now(),
        )

        # Store feedback - this should work end-to-end
        result = feedback_tools.store_critic_feedback(feedback)

        # Verify integration worked
        assert result.id == loop_id
        assert result.status in [LoopStatus.IN_PROGRESS, LoopStatus.REFINE]

        # Verify feedback was stored in loop state
        loop_state = state_manager.get_loop(loop_id)
        assert len(loop_state.feedback_history) == 1
        assert loop_state.feedback_history[0].critic_agent == CriticAgent.PLAN_CRITIC
        assert loop_state.current_score == 68  # Based on manual calculation

    def test_get_feedback_history_integration(self) -> None:
        """Test retrieving feedback history through integration stack."""
        state_manager = InMemoryStateManager()
        feedback_tools = FeedbackTools(state_manager)
        loop_tools = LoopTools(state_manager)

        loop_response = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_response.id

        # Add multiple feedbacks
        for i in range(3):
            feedback = CriticFeedback(
                loop_id=loop_id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=i + 1,
                overall_score=50 + (i * 10),
                assessment_summary=f'Feedback {i + 1}',
                detailed_feedback=f'Detailed feedback for iteration {i + 1}',
                key_issues=[f'Issue {i + 1}'],
                recommendations=[f'Improvement {i + 1}'],
                timestamp=datetime.now(),
            )
            feedback_tools.store_critic_feedback(feedback)

        # Get feedback history
        result = feedback_tools.get_feedback_history(loop_id, 2)

        # Verify we got the last 2 feedbacks
        assert 'Retrieved 2 feedback items' in result.message
        assert 'Iteration 2' in result.message and 'Iteration 3' in result.message


class TestProjectPlanToolsIntegration:
    def test_store_project_plan_with_loop_integration(self) -> None:
        """Test storing project plan with loop state integration."""
        state_manager = InMemoryStateManager()
        project_plan_tools = ProjectPlanTools(state_manager)

        # Create project plan
        project_plan = ProjectPlan(
            project_name='Test Integration Project',
            project_vision='Test vision',
            project_mission='Test mission',
            project_timeline='6 months',
            project_budget='$100k',
            primary_objectives='Build great software',
            success_metrics='All tests pass',
            key_performance_indicators='Coverage: 100%, Uptime: 99.9%',
            included_features='Authentication, API, Frontend',
            excluded_features='Mobile app',
            project_assumptions='Team available',
            project_constraints='Budget and time',
            project_sponsor='Product Owner',
            key_stakeholders='Product team',
            end_users='Developers',
            work_breakdown='Backend, Frontend, Testing',
            phases_overview='Phase 1: 2 months, Phase 2: 4 months',
            project_dependencies='Third-party APIs',
            team_structure='5 developers',
            technology_requirements='AWS infrastructure',
            infrastructure_needs='Cloud hosting and database',
            identified_risks='Technical complexity',
            mitigation_strategies='Incremental development',
            contingency_plans='Reduce scope if needed',
            quality_standards='100% test coverage',
            testing_strategy='Automated testing',
            acceptance_criteria='All features working',
            reporting_structure='Weekly reports',
            meeting_schedule='Daily standups',
            documentation_standards='Markdown documentation',
            project_status=ProjectStatus.DRAFT,
            creation_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            version='1.0',
        )

        # Store without loop_id - should create new loop
        result = project_plan_tools.store_project_plan(project_plan)

        # Verify loop was created and project plan stored
        assert result.id is not None
        assert result.status == LoopStatus.INITIALIZED
        assert 'Test Integration Project' in result.message


class TestLoopToolsIntegration:
    def test_complete_loop_lifecycle(self) -> None:
        """Test complete loop lifecycle through integration."""
        state_manager = InMemoryStateManager()
        loop_tools = LoopTools(state_manager)

        # Initialize loop
        init_result = loop_tools.initialize_refinement_loop('build_plan')
        loop_id = init_result.id
        assert init_result.status == LoopStatus.INITIALIZED

        # Get loop status
        status_result = loop_tools.get_loop_status(loop_id)
        assert status_result.id == loop_id
        assert status_result.status == LoopStatus.INITIALIZED

        # List active loops
        active_loops = loop_tools.list_active_loops()
        assert len(active_loops) == 1
        assert active_loops[0].id == loop_id

        # Test loop decision making with score
        decision_result = loop_tools.decide_loop_next_action(loop_id, 85)
        assert decision_result.id == loop_id
        # Should be completed if score is high enough

        # Verify loop state was updated
        final_status = loop_tools.get_loop_status(loop_id)
        assert final_status.status in [LoopStatus.COMPLETED, LoopStatus.REFINE]


class TestRoadmapToolsIntegration:
    def test_roadmap_crud_operations(self) -> None:
        """Test roadmap CRUD operations through state manager."""
        state_manager = InMemoryStateManager()
        roadmap_tools = RoadmapTools(state_manager)

        # Create roadmap with markdown
        roadmap_markdown = """# Project Roadmap: Integration Test Project

## Project Details
- **Project Goal**: Test integration of roadmap tools
- **Total Duration**: 8 weeks
- **Team Size**: 4 developers
- **Budget**: $50,000

## Specifications
- **Spec 1**: Foundation
- **Spec 2**: Implementation

## Risk Assessment
- **Critical Path Analysis**: Sequential development phases
- **Key Risks**: Technical complexity
- **Mitigation Plans**: Incremental delivery
- **Buffer Time**: 2 weeks

## Resource Planning
- **Development Resources**: 4 developers full time
- **Infrastructure Requirements**: Cloud hosting and database
- **External Dependencies**: None
- **Quality Assurance Plan**: Automated testing

## Success Metrics
- **Technical Milestones**: Working MVP
- **Business Milestones**: User acceptance
- **Quality Gates**: All tests pass
- **Performance Targets**: Fast response times

## Metadata
- **Status**: draft
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-01
- **Spec Count**: 2
"""

        # Create roadmap
        create_result = roadmap_tools.create_roadmap('integration-test', roadmap_markdown)
        assert 'Integration Test Project' in create_result

        # Get roadmap
        get_result = roadmap_tools.get_roadmap('integration-test')
        assert 'Integration Test Project' in get_result
        assert '2 specs' in get_result

        # List specs
        list_result = roadmap_tools.list_specs('integration-test')
        assert 'Foundation' in list_result
        assert 'Implementation' in list_result


class TestCrossToolIntegration:
    def test_feedback_and_loop_tools_together(self) -> None:
        """Test feedback tools and loop tools working together."""
        state_manager = InMemoryStateManager()
        feedback_tools = FeedbackTools(state_manager)
        loop_tools = LoopTools(state_manager)

        # Create loop
        loop_result = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_result.id

        # Add feedback with low score
        low_feedback = CriticFeedback(
            loop_id=loop_id,
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=1,
            overall_score=25,
            assessment_summary='Needs significant improvement',
            detailed_feedback='Major issues identified requiring significant refactoring',
            key_issues=['Poor clarity', 'Incomplete information'],
            recommendations=['Major refactor needed'],
            timestamp=datetime.now(),
        )
        feedback_tools.store_critic_feedback(low_feedback)

        # Check loop decision - should continue refining
        decision = loop_tools.decide_loop_next_action(loop_id, 25)  # Low score
        assert decision.status == LoopStatus.REFINE

        # Add better feedback
        better_feedback = CriticFeedback(
            loop_id=loop_id,
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=2,
            overall_score=85,
            assessment_summary='Much better',
            detailed_feedback='Significant improvements made, only minor tweaks needed',
            key_issues=['Minor formatting issues'],
            recommendations=['Minor tweaks only'],
            timestamp=datetime.now(),
        )
        feedback_tools.store_critic_feedback(better_feedback)

        # Check loop decision - should complete if score is high enough
        decision = loop_tools.decide_loop_next_action(loop_id, 85)
        assert decision.status == LoopStatus.COMPLETED
