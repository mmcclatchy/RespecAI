import pytest
from fastmcp.exceptions import ResourceError

from services.mcp.tools.feedback_tools import FeedbackTools
from services.models.enums import CriticAgent
from services.models.feedback import CriticFeedback
from services.utils.enums import LoopStatus, LoopType
from services.utils.loop_state import LoopState, MCPResponse
from services.utils.state_manager import InMemoryStateManager


@pytest.fixture
def state_manager() -> InMemoryStateManager:
    return InMemoryStateManager(max_history_size=3)


@pytest.fixture
def feedback_tools(state_manager: InMemoryStateManager) -> FeedbackTools:
    return FeedbackTools(state_manager)


@pytest.fixture
def sample_loop(state_manager: InMemoryStateManager) -> LoopState:
    loop_state = LoopState(loop_type=LoopType.SPEC)
    state_manager.add_loop(loop_state)
    return loop_state


@pytest.fixture
def sample_feedback(sample_loop: LoopState) -> CriticFeedback:
    return CriticFeedback(
        loop_id=sample_loop.id,
        critic_agent=CriticAgent.SPEC_CRITIC,
        iteration=1,
        overall_score=85,
        assessment_summary='Good specification with room for improvement',
        detailed_feedback='The specification covers most requirements but needs security details and integration patterns.',
        key_issues=['Missing security requirements', 'Integration patterns unclear'],
        recommendations=['Add security details', 'Clarify integration patterns'],
    )


class TestFeedbackTools:
    pass


class TestStoreCriticFeedback:
    def test_store_critic_feedback_returns_success_response(
        self, feedback_tools: FeedbackTools, sample_feedback: CriticFeedback
    ) -> None:
        response = feedback_tools.store_critic_feedback(sample_feedback)

        assert isinstance(response, MCPResponse)
        assert response.id == sample_feedback.loop_id
        assert response.status == LoopStatus.IN_PROGRESS

    def test_store_critic_feedback_adds_feedback_to_loop_state(
        self, feedback_tools: FeedbackTools, sample_feedback: CriticFeedback
    ) -> None:
        feedback_tools.store_critic_feedback(sample_feedback)

        updated_loop = feedback_tools.state.get_loop(sample_feedback.loop_id)
        assert len(updated_loop.feedback_history) == 1

        stored_feedback = updated_loop.feedback_history[0]
        assert stored_feedback.loop_id == sample_feedback.loop_id
        assert stored_feedback.critic_agent == sample_feedback.critic_agent
        assert stored_feedback.assessment_summary == sample_feedback.assessment_summary
        assert stored_feedback.key_issues == sample_feedback.key_issues
        assert stored_feedback.recommendations == sample_feedback.recommendations

    def test_store_critic_feedback_updates_loop_score(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState, sample_feedback: CriticFeedback
    ) -> None:
        initial_score = sample_loop.current_score

        feedback_tools.store_critic_feedback(sample_feedback)

        updated_loop = feedback_tools.state.get_loop(sample_feedback.loop_id)
        assert updated_loop.current_score != initial_score
        assert updated_loop.current_score == 85  # Overall score from feedback

    def test_store_critic_feedback_works_with_all_loop_types(
        self, feedback_tools: FeedbackTools, state_manager: InMemoryStateManager
    ) -> None:
        # Test all 6 loop types to ensure universal functionality
        loop_types = [
            LoopType.PLAN,
            LoopType.ROADMAP,
            LoopType.SPEC,
            LoopType.BUILD_PLAN,
            LoopType.BUILD_CODE,
            LoopType.ANALYST,
        ]

        for loop_type in loop_types:
            loop_state = LoopState(loop_type=loop_type)
            state_manager.add_loop(loop_state)

            feedback = CriticFeedback(
                loop_id=loop_state.id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=1,
                overall_score=70,
                assessment_summary=f'Assessment for {loop_type.value}',
                detailed_feedback=f'Detailed analysis for {loop_type.value}',
                key_issues=[f'Issue for {loop_type.value}'],
                recommendations=[f'Improvement for {loop_type.value}'],
            )

            response = feedback_tools.store_critic_feedback(feedback)

            assert response.status == LoopStatus.IN_PROGRESS
            updated_loop = feedback_tools.state.get_loop(loop_state.id)
            assert len(updated_loop.feedback_history) == 1
            assert updated_loop.current_score == 70

    def test_store_critic_feedback_raises_error_when_loop_not_found(self, feedback_tools: FeedbackTools) -> None:
        feedback = CriticFeedback(
            loop_id='non-existent-loop',
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=1,
            overall_score=80,
            assessment_summary='Test assessment',
            detailed_feedback='Test detailed feedback',
            key_issues=[],
            recommendations=[],
        )

        with pytest.raises(ResourceError):
            feedback_tools.store_critic_feedback(feedback)

    def test_store_critic_feedback_validates_score_range(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        with pytest.raises(ValueError, match='Overall score must be between 0 and 100'):
            CriticFeedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=1,
                overall_score=150,  # Invalid: > 100
                assessment_summary='Test assessment',
                detailed_feedback='Test detailed feedback',
                key_issues=[],
                recommendations=[],
            )


class TestGetFeedbackHistory:
    def test_get_feedback_history_returns_empty_for_new_loop(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        response = feedback_tools.get_feedback_history(sample_loop.id)

        assert isinstance(response, MCPResponse)
        assert response.id == sample_loop.id
        assert response.status == LoopStatus.INITIALIZED
        assert 'No feedback history' in response.message

    def test_get_feedback_history_returns_recent_feedback(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        # Add multiple feedback items
        for i in range(3):
            feedback = CriticFeedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=i + 1,
                overall_score=70 + i * 5,
                assessment_summary=f'Assessment {i + 1}',
                detailed_feedback=f'Detailed analysis {i + 1}',
                key_issues=[f'Issue {i + 1}'],
                recommendations=[f'Improvement {i + 1}'],
            )
            feedback_tools.store_critic_feedback(feedback)

        response = feedback_tools.get_feedback_history(sample_loop.id, count=2)

        assert isinstance(response, MCPResponse)
        assert response.id == sample_loop.id
        assert '2 feedback items' in response.message
        assert 'Assessment 2' in response.message
        assert 'Assessment 3' in response.message

    def test_get_feedback_history_respects_count_limit(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        # Add 5 feedback items
        for i in range(5):
            feedback = CriticFeedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=i + 1,
                overall_score=70,
                assessment_summary=f'Assessment {i + 1}',
                detailed_feedback=f'Detailed analysis {i + 1}',
                key_issues=[],
                recommendations=[],
            )
            feedback_tools.store_critic_feedback(feedback)

        # Request only last 3
        response = feedback_tools.get_feedback_history(sample_loop.id, count=3)

        assert '3 feedback items' in response.message
        assert 'Assessment 3' in response.message
        assert 'Assessment 4' in response.message
        assert 'Assessment 5' in response.message
        assert 'Assessment 1' not in response.message
        assert 'Assessment 2' not in response.message

    def test_get_feedback_history_works_with_all_loop_types(
        self, feedback_tools: FeedbackTools, state_manager: InMemoryStateManager
    ) -> None:
        # Test feedback history retrieval works for all loop types
        loop_types = [
            LoopType.PLAN,
            LoopType.ROADMAP,
            LoopType.SPEC,
            LoopType.BUILD_PLAN,
            LoopType.BUILD_CODE,
            LoopType.ANALYST,
        ]

        for loop_type in loop_types:
            loop_state = LoopState(loop_type=loop_type)
            state_manager.add_loop(loop_state)

            # Add feedback
            feedback = CriticFeedback(
                loop_id=loop_state.id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=1,
                overall_score=80,
                assessment_summary=f'Assessment for {loop_type.value}',
                detailed_feedback=f'Detailed analysis for {loop_type.value}',
                key_issues=[],
                recommendations=[],
            )
            feedback_tools.store_critic_feedback(feedback)

            # Retrieve feedback
            response = feedback_tools.get_feedback_history(loop_state.id)
            assert '1 feedback item' in response.message
            assert f'Assessment for {loop_type.value}' in response.message

    def test_get_feedback_history_raises_error_when_loop_not_found(self, feedback_tools: FeedbackTools) -> None:
        with pytest.raises(ResourceError):
            feedback_tools.get_feedback_history('non-existent-loop')

    def test_get_feedback_history_default_count_is_five(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        # Add 7 feedback items
        for i in range(7):
            feedback = CriticFeedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=i + 1,
                overall_score=70,
                assessment_summary=f'Assessment {i + 1}',
                detailed_feedback=f'Detailed analysis {i + 1}',
                key_issues=[],
                recommendations=[],
            )
            feedback_tools.store_critic_feedback(feedback)

        # Request default (should be 5)
        response = feedback_tools.get_feedback_history(sample_loop.id)

        assert '5 feedback items' in response.message
        assert 'Assessment 3' in response.message  # 5th from end
        assert 'Assessment 7' in response.message  # Most recent
        assert 'Assessment 1' not in response.message
        assert 'Assessment 2' not in response.message
