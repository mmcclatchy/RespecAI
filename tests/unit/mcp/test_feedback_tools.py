import pytest
from fastmcp.exceptions import ResourceError, ToolError

from services.mcp.feedback_tools import FeedbackTools
from services.models.enums import CriticAgent, FSSDCriteria
from services.utils.enums import LoopStatus, LoopType
from services.utils.models import LoopState, MCPResponse
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
def sample_feedback_data(sample_loop: LoopState) -> dict:
    return {
        'loop_id': sample_loop.id,
        'critic_agent': CriticAgent.SPEC_CRITIC.value,
        'iteration': 1,
        'overall_assessment': 'Good specification with room for improvement',
        'improvements': ['Add security details', 'Clarify integration patterns'],
        'fsdd_scores': {criteria: 8 for criteria in FSSDCriteria},
    }


class TestFeedbackTools:
    pass


class TestStoreCriticFeedback:
    def test_store_critic_feedback_returns_success_response(
        self, feedback_tools: FeedbackTools, sample_feedback_data: dict
    ) -> None:
        response = feedback_tools.store_critic_feedback(**sample_feedback_data)

        assert isinstance(response, MCPResponse)
        assert response.id == sample_feedback_data['loop_id']
        assert response.status == LoopStatus.IN_PROGRESS

    def test_store_critic_feedback_adds_feedback_to_loop_state(
        self, feedback_tools: FeedbackTools, sample_feedback_data: dict
    ) -> None:
        feedback_tools.store_critic_feedback(**sample_feedback_data)

        updated_loop = feedback_tools.state.get_loop(sample_feedback_data['loop_id'])
        assert len(updated_loop.feedback_history) == 1

        stored_feedback = updated_loop.feedback_history[0]
        assert stored_feedback.session_id == sample_feedback_data['loop_id']
        assert stored_feedback.critic_agent.value == sample_feedback_data['critic_agent']
        assert stored_feedback.overall_assessment == sample_feedback_data['overall_assessment']
        assert stored_feedback.improvements == sample_feedback_data['improvements']
        assert stored_feedback.fsdd_scores == sample_feedback_data['fsdd_scores']

    def test_store_critic_feedback_updates_loop_score(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState, sample_feedback_data: dict
    ) -> None:
        initial_score = sample_loop.current_score

        feedback_tools.store_critic_feedback(**sample_feedback_data)

        updated_loop = feedback_tools.state.get_loop(sample_feedback_data['loop_id'])
        assert updated_loop.current_score != initial_score
        assert updated_loop.current_score == 80  # All scores are 8, so 80%

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

            response = feedback_tools.store_critic_feedback(
                loop_id=loop_state.id,
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=1,
                overall_assessment=f'Assessment for {loop_type.value}',
                improvements=[f'Improvement for {loop_type.value}'],
                fsdd_scores={criteria: 7 for criteria in FSSDCriteria},
            )

            assert response.status == LoopStatus.IN_PROGRESS
            updated_loop = feedback_tools.state.get_loop(loop_state.id)
            assert len(updated_loop.feedback_history) == 1
            assert updated_loop.current_score == 70

    def test_store_critic_feedback_raises_error_when_loop_not_found(self, feedback_tools: FeedbackTools) -> None:
        with pytest.raises(ResourceError):
            feedback_tools.store_critic_feedback(
                loop_id='non-existent-loop',
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=1,
                overall_assessment='Test assessment',
                improvements=[],
                fsdd_scores={criteria: 8 for criteria in FSSDCriteria},
            )

    def test_store_critic_feedback_validates_critic_agent_enum(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        with pytest.raises(ToolError):
            feedback_tools.store_critic_feedback(
                loop_id=sample_loop.id,
                critic_agent='invalid-critic',
                iteration=1,
                overall_assessment='Test assessment',
                improvements=[],
                fsdd_scores={FSSDCriteria.CLARITY: 8},
            )

    def test_store_critic_feedback_validates_fsdd_score_range(
        self, feedback_tools: FeedbackTools, sample_loop: LoopState
    ) -> None:
        invalid_scores = {FSSDCriteria.CLARITY: 15}  # Invalid: > 10

        with pytest.raises(ToolError):
            feedback_tools.store_critic_feedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=1,
                overall_assessment='Test assessment',
                improvements=[],
                fsdd_scores=invalid_scores,
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
            feedback_tools.store_critic_feedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=i + 1,
                overall_assessment=f'Assessment {i + 1}',
                improvements=[f'Improvement {i + 1}'],
                fsdd_scores={criteria: 7 + i for criteria in FSSDCriteria},
            )

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
            feedback_tools.store_critic_feedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=i + 1,
                overall_assessment=f'Assessment {i + 1}',
                improvements=[],
                fsdd_scores={criteria: 7 for criteria in FSSDCriteria},
            )

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
            feedback_tools.store_critic_feedback(
                loop_id=loop_state.id,
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=1,
                overall_assessment=f'Assessment for {loop_type.value}',
                improvements=[],
                fsdd_scores={criteria: 8 for criteria in FSSDCriteria},
            )

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
            feedback_tools.store_critic_feedback(
                loop_id=sample_loop.id,
                critic_agent=CriticAgent.SPEC_CRITIC.value,
                iteration=i + 1,
                overall_assessment=f'Assessment {i + 1}',
                improvements=[],
                fsdd_scores={criteria: 7 for criteria in FSSDCriteria},
            )

        # Request default (should be 5)
        response = feedback_tools.get_feedback_history(sample_loop.id)

        assert '5 feedback items' in response.message
        assert 'Assessment 3' in response.message  # 5th from end
        assert 'Assessment 7' in response.message  # Most recent
        assert 'Assessment 1' not in response.message
        assert 'Assessment 2' not in response.message
