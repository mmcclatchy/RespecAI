import pytest

from services.mcp.tools.feedback_storage_tools import FeedbackStorageTools
from services.models.enums import CriticAgent
from services.utils.enums import LoopType
from services.utils.models import LoopState, MCPResponse
from services.utils.state_manager import InMemoryStateManager


from fastmcp import FastMCP
from services.mcp.tools.feedback_storage_tools import register_feedback_storage_tools


class TestPlanFeedbackIntegrationFlow:
    """Integration tests for the complete plan feedback flow."""

    @pytest.fixture
    def state_manager(self) -> InMemoryStateManager:
        return InMemoryStateManager()

    @pytest.fixture
    def feedback_tools(self, state_manager: InMemoryStateManager) -> FeedbackStorageTools:
        return FeedbackStorageTools(state_manager)

    @pytest.fixture
    def plan_loop_state(self, state_manager: InMemoryStateManager) -> tuple[str, LoopState]:
        loop_id = 'plan-integration-test-123'
        loop_state = LoopState(id=loop_id, loop_type=LoopType.PLAN)
        state_manager.add_loop(loop_state)
        return loop_id, loop_state

    @pytest.fixture
    def analyst_loop_state(self, state_manager: InMemoryStateManager) -> tuple[str, LoopState]:
        loop_id = 'analyst-integration-test-456'
        loop_state = LoopState(id=loop_id, loop_type=LoopType.ANALYST)
        state_manager.add_loop(loop_state)
        return loop_id, loop_state

    @pytest.fixture
    def plan_critic_markdown(self) -> str:
        return """# Critic Feedback: PLAN-CRITIC

## Assessment Summary
- **Loop ID**: plan-integration-test-123
- **Iteration**: 1
- **Overall Score**: 78
- **Assessment Summary**: Strategic plan shows solid framework but needs refinement in risk mitigation

## Analysis

The strategic plan demonstrates good overall structure with clear objectives and stakeholder identification. However, the risk assessment section lacks specific mitigation strategies, and success metrics need more quantification. The technical feasibility appears sound, but resource allocation could be more detailed.

## Issues and Recommendations

### Key Issues

- Risk mitigation strategies are too generic and lack implementation details
- Success metrics need quantitative targets and measurement methods
- Resource allocation timeline conflicts with stated delivery dates

### Recommendations

- Develop specific risk mitigation plans for each identified risk category
- Add quantitative success metrics with baseline and target values
- Reconcile resource allocation with project timeline constraints

## Metadata
- **Critic**: PLAN-CRITIC
- **Timestamp**: 2025-01-15T10:30:00Z
- **Status**: completed
"""

    @pytest.fixture
    def analyst_critic_markdown(self) -> str:
        return """# Critic Feedback: ANALYST-CRITIC

## Assessment Summary
- **Loop ID**: analyst-integration-test-456
- **Iteration**: 1
- **Overall Score**: 82
- **Assessment Summary**: Objective extraction demonstrates good semantic accuracy with minor completeness gaps

## Analysis

The business objectives analysis correctly captures the primary goals from the strategic plan with accurate stakeholder mapping. Most success metrics are properly quantified, and dependency relationships are well documented. However, some secondary objectives from the constraints section were omitted, and risk assessment could be more comprehensive.

## Issues and Recommendations

### Key Issues

- Missing secondary objectives from constraints and integration sections
- Risk assessment lacks some technical implementation risks
- Success criteria need more specific measurement timelines

### Recommendations

- Review constraints section for additional implicit objectives
- Expand risk assessment to include technical implementation challenges
- Add specific measurement schedules to success criteria

## Metadata
- **Critic**: ANALYST-CRITIC
- **Timestamp**: 2025-01-15T11:45:00Z
- **Status**: completed
"""

    def test_complete_plan_critic_feedback_flow(
        self, feedback_tools: FeedbackStorageTools, plan_loop_state: tuple[str, LoopState], plan_critic_markdown: str
    ) -> None:
        loop_id, loop_state = plan_loop_state

        # Step 1: Store plan-critic feedback
        store_result = feedback_tools.store_critic_feedback(loop_id, plan_critic_markdown)

        # Verify storage success
        assert isinstance(store_result, MCPResponse)
        assert store_result.id == loop_id
        assert 'Score: 78' in store_result.message
        assert 'plan-critic' in store_result.message

        # Verify feedback was added to loop state
        assert len(loop_state.feedback_history) == 1
        feedback = loop_state.feedback_history[0]
        assert feedback.overall_score == 78
        assert feedback.critic_agent == CriticAgent.PLAN_CRITIC
        assert feedback.loop_id == loop_id

        # Step 2: Retrieve previous feedback
        retrieve_result = feedback_tools.get_previous_feedback(loop_id, 1)

        # Verify retrieval success
        assert isinstance(retrieve_result, MCPResponse)
        assert retrieve_result.id == loop_id
        assert '# Critic Feedback: PLAN-CRITIC' in retrieve_result.message
        assert 'Overall Score**: 78' in retrieve_result.message

    def test_complete_analyst_critic_feedback_flow(
        self,
        feedback_tools: FeedbackStorageTools,
        analyst_loop_state: tuple[str, LoopState],
        analyst_critic_markdown: str,
    ) -> None:
        loop_id, loop_state = analyst_loop_state

        # Step 1: Store analyst-critic feedback
        store_result = feedback_tools.store_critic_feedback(loop_id, analyst_critic_markdown)

        # Verify storage success
        assert isinstance(store_result, MCPResponse)
        assert store_result.id == loop_id
        assert 'Score: 82' in store_result.message
        assert 'analyst-critic' in store_result.message

        # Verify feedback was added to loop state
        assert len(loop_state.feedback_history) == 1
        feedback = loop_state.feedback_history[0]
        assert feedback.overall_score == 82
        assert feedback.critic_agent == CriticAgent.ANALYST_CRITIC
        assert feedback.loop_id == loop_id

        # Step 2: Retrieve previous feedback
        retrieve_result = feedback_tools.get_previous_feedback(loop_id, 1)

        # Verify retrieval success
        assert isinstance(retrieve_result, MCPResponse)
        assert retrieve_result.id == loop_id
        assert '# Critic Feedback: ANALYST-CRITIC' in retrieve_result.message
        assert 'Overall Score**: 82' in retrieve_result.message

    def test_analysis_storage_and_retrieval_flow(
        self, feedback_tools: FeedbackStorageTools, analyst_loop_state: tuple[str, LoopState]
    ) -> None:
        loop_id, loop_state = analyst_loop_state

        # Sample business objectives analysis
        analysis = """# Business Objectives Analysis

## Primary Objectives
1. Increase customer engagement by 25% within 6 months
2. Reduce operational costs by 15% through automation
3. Improve system reliability to 99.9% uptime

## Success Metrics
- Customer engagement: baseline 40%, target 50%
- Operational costs: baseline $100k/month, target $85k/month
- System uptime: baseline 99.5%, target 99.9%

## Stakeholder Mapping
- Primary: Product Manager, Engineering Team
- Secondary: Customer Success, Operations
"""

        # Step 1: Store analysis
        store_result = feedback_tools.store_current_analysis(loop_id, analysis)

        # Verify storage success
        assert isinstance(store_result, MCPResponse)
        assert store_result.id == loop_id
        assert 'Stored analysis for loop' in store_result.message

        # Step 2: Retrieve analysis
        retrieve_result = feedback_tools.get_previous_analysis(loop_id)

        # Verify retrieval success
        assert isinstance(retrieve_result, MCPResponse)
        assert retrieve_result.id == loop_id
        assert '# Business Objectives Analysis' in retrieve_result.message
        assert 'Increase customer engagement by 25%' in retrieve_result.message

    def test_multiple_feedback_iterations_flow(
        self, feedback_tools: FeedbackStorageTools, plan_loop_state: tuple[str, LoopState]
    ) -> None:
        loop_id, loop_state = plan_loop_state

        # First iteration
        feedback_v1 = """# Critic Feedback: PLAN-CRITIC

## Assessment Summary
- **Loop ID**: plan-integration-test-123
- **Iteration**: 1
- **Overall Score**: 65
- **Assessment Summary**: Initial plan draft requires significant improvements

## Analysis
Plan shows basic structure but lacks detail in key areas.

## Issues and Recommendations

### Key Issues
- Missing stakeholder analysis
- Unclear success metrics

### Recommendations
- Add detailed stakeholder mapping
- Define quantitative success criteria

## Metadata
- **Critic**: PLAN-CRITIC
- **Timestamp**: 2025-01-15T09:00:00Z
- **Status**: completed
"""

        # Second iteration
        feedback_v2 = """# Critic Feedback: PLAN-CRITIC

## Assessment Summary
- **Loop ID**: plan-integration-test-123
- **Iteration**: 2
- **Overall Score**: 85
- **Assessment Summary**: Significantly improved plan with minor refinements needed

## Analysis
Plan now includes comprehensive stakeholder analysis and clear success metrics.

## Issues and Recommendations

### Key Issues
- Timeline could be more detailed

### Recommendations
- Add milestone-specific timelines

## Metadata
- **Critic**: PLAN-CRITIC
- **Timestamp**: 2025-01-15T10:00:00Z
- **Status**: completed
"""

        # Store both iterations
        feedback_tools.store_critic_feedback(loop_id, feedback_v1)
        feedback_tools.store_critic_feedback(loop_id, feedback_v2)

        # Verify loop state has both feedback entries
        assert len(loop_state.feedback_history) == 2
        assert loop_state.feedback_history[0].overall_score == 65
        assert loop_state.feedback_history[1].overall_score == 85

        # Retrieve most recent feedback
        result = feedback_tools.get_previous_feedback(loop_id, 1)
        assert 'Overall Score**: 85' in result.message
        assert 'Iteration**: 2' in result.message

        # Verify the latest score updated the loop state current score
        assert loop_state.current_score == 85

    def test_cross_loop_isolation(
        self,
        feedback_tools: FeedbackStorageTools,
        plan_loop_state: tuple[str, LoopState],
        analyst_loop_state: tuple[str, LoopState],
        plan_critic_markdown: str,
        analyst_critic_markdown: str,
    ) -> None:
        plan_loop_id, plan_state = plan_loop_state
        analyst_loop_id, analyst_state = analyst_loop_state

        # Store feedback in both loops
        feedback_tools.store_critic_feedback(plan_loop_id, plan_critic_markdown)
        feedback_tools.store_critic_feedback(analyst_loop_id, analyst_critic_markdown)

        # Verify each loop only has its own feedback
        assert len(plan_state.feedback_history) == 1
        assert len(analyst_state.feedback_history) == 1
        assert plan_state.feedback_history[0].critic_agent == CriticAgent.PLAN_CRITIC
        assert analyst_state.feedback_history[0].critic_agent == CriticAgent.ANALYST_CRITIC

        # Verify retrieval is isolated
        plan_result = feedback_tools.get_previous_feedback(plan_loop_id, 1)
        analyst_result = feedback_tools.get_previous_feedback(analyst_loop_id, 1)

        assert 'PLAN-CRITIC' in plan_result.message
        assert 'ANALYST-CRITIC' in analyst_result.message
        assert 'ANALYST-CRITIC' not in plan_result.message
        assert 'PLAN-CRITIC' not in analyst_result.message

    def test_decision_logic_integration(
        self,
        feedback_tools: FeedbackStorageTools,
        analyst_loop_state: tuple[str, LoopState],
        analyst_critic_markdown: str,
    ) -> None:
        loop_id, loop_state = analyst_loop_state

        # Store feedback with score that should trigger refinement
        low_score_feedback = analyst_critic_markdown.replace('Overall Score**: 82', 'Overall Score**: 45')
        feedback_tools.store_critic_feedback(loop_id, low_score_feedback)

        # Verify loop state updated with the score
        assert loop_state.current_score == 45

        # Test decision logic (assuming 70 is the threshold)
        decision_response = loop_state.decide_next_loop_action()
        assert decision_response.status.value in ['refine', 'user_input']  # Low score should trigger refinement

        # Store feedback with high score
        high_score_feedback = analyst_critic_markdown.replace('Overall Score**: 82', 'Overall Score**: 95')
        feedback_tools.store_critic_feedback(loop_id, high_score_feedback)

        # Verify decision logic for high score
        assert loop_state.current_score == 95
        decision_response = loop_state.decide_next_loop_action()
        assert decision_response.status.value == 'completed'  # High score should complete

    @pytest.mark.asyncio
    async def test_mcp_tool_registration_integration(self) -> None:
        # Create FastMCP instance
        mcp = FastMCP()

        # Register feedback storage tools
        register_feedback_storage_tools(mcp)

        # Verify all tools are registered
        tools_dict = await mcp.get_tools()
        tool_names = list(tools_dict.keys())
        expected_tools = [
            'store_critic_feedback',
            'get_previous_feedback',
            'store_current_analysis',
            'get_previous_analysis',
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names, f'Tool {tool_name} not found in registered tools: {tool_names}'
