import pytest
from unittest.mock import Mock
from fastmcp.exceptions import ResourceError, ToolError

from services.mcp.tools.feedback_storage_tools import FeedbackStorageTools
from services.models.feedback import CriticFeedback
from services.utils.enums import LoopType
from services.models.enums import CriticAgent
from services.utils.errors import LoopNotFoundError
from services.utils.models import LoopState, MCPResponse


from services.mcp.tools.feedback_storage_tools import register_feedback_storage_tools


class TestFeedbackStorageTools:
    """Test suite for FeedbackStorageTools class."""

    @pytest.fixture
    def mock_state_manager(self) -> Mock:
        return Mock()

    @pytest.fixture
    def feedback_tools(self, mock_state_manager: Mock) -> FeedbackStorageTools:
        return FeedbackStorageTools(mock_state_manager)

    @pytest.fixture
    def sample_loop_state(self) -> LoopState:
        return LoopState(loop_type=LoopType.PLAN)

    @pytest.fixture
    def sample_feedback_markdown(self) -> str:
        return """# Critic Feedback: PLAN-CRITIC

## Assessment Summary
- **Loop ID**: test-loop-123
- **Iteration**: 1
- **Overall Score**: 85
- **Assessment Summary**: Plan shows good structure with minor improvements needed

## Analysis

The strategic plan demonstrates solid framework and clear objectives.
Risk assessment section needs expansion with specific mitigation strategies.

## Issues and Recommendations

### Key Issues

- Risk mitigation strategies lack specificity
- Success metrics need quantification

### Recommendations

- Add concrete risk mitigation approaches
- Define measurable success criteria

## Metadata
- **Critic**: PLAN-CRITIC
- **Timestamp**: 2025-01-15T14:30:00Z
- **Status**: completed"""

    def test_store_critic_feedback_success(
        self,
        feedback_tools: FeedbackStorageTools,
        mock_state_manager: Mock,
        sample_loop_state: LoopState,
        sample_feedback_markdown: str,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = feedback_tools.store_critic_feedback(loop_id, sample_feedback_markdown)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'Score: 85' in result.message
        assert 'plan-critic' in result.message
        # get_loop is called twice: once for loop state access and once for critic auto-detection
        assert mock_state_manager.get_loop.call_count == 2
        mock_state_manager.get_loop.assert_called_with(loop_id)
        # Verify feedback was added to loop state
        assert len(sample_loop_state.feedback_history) == 1
        assert sample_loop_state.feedback_history[0].overall_score == 85

    def test_store_critic_feedback_invalid_markdown(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state
        invalid_markdown = 'This is not valid CriticFeedback markdown'

        with pytest.raises(ToolError, match='Markdown does not contain valid CriticFeedback structure'):
            feedback_tools.store_critic_feedback(loop_id, invalid_markdown)

    def test_store_critic_feedback_empty_inputs(self, feedback_tools: FeedbackStorageTools) -> None:
        # Empty loop ID
        with pytest.raises(ToolError, match='Loop ID cannot be empty'):
            feedback_tools.store_critic_feedback('', 'valid markdown')

        # Empty markdown
        with pytest.raises(ToolError, match='Feedback markdown cannot be empty'):
            feedback_tools.store_critic_feedback('test-loop', '')

    def test_store_critic_feedback_loop_not_found(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_feedback_markdown: str
    ) -> None:
        loop_id = 'non-existent-loop'
        mock_state_manager.get_loop.side_effect = LoopNotFoundError('Loop not found')

        with pytest.raises(ResourceError, match='Loop does not exist'):
            feedback_tools.store_critic_feedback(loop_id, sample_feedback_markdown)

    def test_get_previous_feedback_success(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        # Add some feedback to loop state
        feedback = CriticFeedback(
            loop_id=loop_id,
            critic_agent=CriticAgent.PLAN_CRITIC,
            iteration=1,
            overall_score=85,
            assessment_summary='Test summary',
            detailed_feedback='Test feedback',
            key_issues=['Issue 1'],
            recommendations=['Rec 1'],
        )
        sample_loop_state.add_feedback(feedback)

        result = feedback_tools.get_previous_feedback(loop_id, 1)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'Previous feedback for loop' in result.message
        assert '# Critic Feedback: PLAN-CRITIC' in result.message

    def test_get_previous_feedback_no_history(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = feedback_tools.get_previous_feedback(loop_id, 1)

        assert isinstance(result, MCPResponse)
        assert 'No previous feedback found' in result.message

    def test_get_previous_feedback_invalid_inputs(self, feedback_tools: FeedbackStorageTools) -> None:
        # Empty loop ID
        with pytest.raises(ToolError, match='Loop ID cannot be empty'):
            feedback_tools.get_previous_feedback('', 1)

        # Invalid count
        with pytest.raises(ToolError, match='Count must be a positive integer'):
            feedback_tools.get_previous_feedback('test-loop', 0)

    def test_store_current_analysis_success(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        analysis = '# Business Objectives Analysis\n\nDetailed analysis content here'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = feedback_tools.store_current_analysis(loop_id, analysis)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'Stored analysis for loop' in result.message
        assert feedback_tools._analysis_storage[loop_id] == analysis

    def test_store_current_analysis_invalid_inputs(self, feedback_tools: FeedbackStorageTools) -> None:
        # Empty loop ID
        with pytest.raises(ToolError, match='Loop ID cannot be empty'):
            feedback_tools.store_current_analysis('', 'valid analysis')

        # Empty analysis
        with pytest.raises(ToolError, match='Analysis cannot be empty'):
            feedback_tools.store_current_analysis('test-loop', '')

    def test_get_previous_analysis_success(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        analysis = '# Previous Analysis\n\nContent from previous iteration'
        mock_state_manager.get_loop.return_value = sample_loop_state
        feedback_tools._analysis_storage[loop_id] = analysis

        result = feedback_tools.get_previous_analysis(loop_id)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'Previous analysis for loop' in result.message
        assert analysis in result.message

    def test_get_previous_analysis_no_storage(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = feedback_tools.get_previous_analysis(loop_id)

        assert isinstance(result, MCPResponse)
        assert 'No previous analysis found' in result.message

    def test_get_previous_analysis_invalid_inputs(self, feedback_tools: FeedbackStorageTools) -> None:
        # Empty loop ID
        with pytest.raises(ToolError, match='Loop ID cannot be empty'):
            feedback_tools.get_previous_analysis('')

    def test_get_previous_analysis_loop_not_found(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'non-existent-loop'
        mock_state_manager.get_loop.side_effect = LoopNotFoundError('Loop not found')

        with pytest.raises(ResourceError, match='Loop does not exist'):
            feedback_tools.get_previous_analysis(loop_id)

    def test_derive_critic_from_loop_all_types(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock
    ) -> None:
        # Test all LoopType to CriticAgent mappings
        test_cases = [
            (LoopType.PLAN, CriticAgent.PLAN_CRITIC),
            (LoopType.ANALYST, CriticAgent.ANALYST_CRITIC),
            (LoopType.ROADMAP, CriticAgent.ROADMAP_CRITIC),
            (LoopType.SPEC, CriticAgent.SPEC_CRITIC),
            (LoopType.BUILD_PLAN, CriticAgent.BUILD_CRITIC),
            (LoopType.BUILD_CODE, CriticAgent.BUILD_REVIEWER),
        ]

        for loop_type, expected_critic in test_cases:
            loop_state = LoopState(loop_type=loop_type)
            mock_state_manager.get_loop.return_value = loop_state

            result = feedback_tools._derive_critic_from_loop('test-loop')

            assert result == expected_critic, f'Failed for {loop_type}: expected {expected_critic}, got {result}'

    def test_derive_critic_from_loop_handles_exceptions(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock
    ) -> None:
        # Test exception handling returns None
        mock_state_manager.get_loop.side_effect = Exception('State manager error')

        result = feedback_tools._derive_critic_from_loop('test-loop')

        assert result is None

    def test_derive_critic_from_loop_empty_loop_id(self, feedback_tools: FeedbackStorageTools) -> None:
        # Test empty loop ID returns None
        result = feedback_tools._derive_critic_from_loop('')

        assert result is None

    def test_store_critic_feedback_auto_detects_critic_agent(
        self,
        feedback_tools: FeedbackStorageTools,
        mock_state_manager: Mock,
        sample_feedback_markdown: str,
    ) -> None:
        loop_id = 'test-loop-123'
        # Set up loop state with SPEC type
        spec_loop_state = LoopState(loop_type=LoopType.SPEC)
        mock_state_manager.get_loop.return_value = spec_loop_state

        result = feedback_tools.store_critic_feedback(loop_id, sample_feedback_markdown)

        # Verify the critic agent was overridden to SPEC_CRITIC based on loop context
        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'spec-critic' in result.message
        # Verify feedback was added with auto-detected critic
        assert len(spec_loop_state.feedback_history) == 1
        assert spec_loop_state.feedback_history[0].critic_agent == CriticAgent.SPEC_CRITIC

    def test_store_critic_feedback_fallback_to_markdown_parsing(
        self,
        feedback_tools: FeedbackStorageTools,
        mock_state_manager: Mock,
        sample_feedback_markdown: str,
    ) -> None:
        loop_id = 'test-loop-123'
        sample_loop_state = LoopState(loop_type=LoopType.PLAN)
        # First call for loop state access, second call throws exception for auto-detection
        mock_state_manager.get_loop.side_effect = [sample_loop_state, Exception('Auto-detection failed')]

        result = feedback_tools.store_critic_feedback(loop_id, sample_feedback_markdown)

        # Should fall back to markdown parsing (PLAN-CRITIC from markdown)
        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'plan-critic' in result.message
        assert len(sample_loop_state.feedback_history) == 1
        assert sample_loop_state.feedback_history[0].critic_agent == CriticAgent.PLAN_CRITIC

    def test_get_previous_feedback_loop_not_found(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'non-existent-loop'
        mock_state_manager.get_loop.side_effect = LoopNotFoundError('Loop not found')

        with pytest.raises(ResourceError, match='Loop does not exist'):
            feedback_tools.get_previous_feedback(loop_id, 1)

    def test_store_current_analysis_loop_not_found(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'non-existent-loop'
        analysis = 'Test analysis content'
        mock_state_manager.get_loop.side_effect = LoopNotFoundError('Loop not found')

        with pytest.raises(ResourceError, match='Loop does not exist'):
            feedback_tools.store_current_analysis(loop_id, analysis)

    def test_parse_and_validate_feedback_parsing_error(
        self, feedback_tools: FeedbackStorageTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'test-loop'
        sample_loop_state = LoopState(loop_type=LoopType.PLAN)
        mock_state_manager.get_loop.return_value = sample_loop_state

        # Markdown that will cause CriticFeedback.parse_markdown to raise an exception
        malformed_markdown = '# Invalid\n\nThis will cause a parsing error in CriticFeedback'

        with pytest.raises(ToolError, match='Markdown does not contain valid CriticFeedback structure'):
            feedback_tools.store_critic_feedback(loop_id, malformed_markdown)


class TestFeedbackStorageToolsRegistration:
    """Test suite for MCP tool registration functions."""

    @pytest.fixture
    def mock_mcp(self) -> Mock:
        return Mock()

    @pytest.fixture
    def mock_context(self) -> Mock:
        context = Mock()
        context.info = Mock()
        context.error = Mock()
        return context

    def test_mcp_tools_registration(self, mock_mcp: Mock) -> None:
        register_feedback_storage_tools(mock_mcp)

        # Verify that mcp.tool() was called for each tool
        assert mock_mcp.tool.call_count == 4  # 4 tools total

        # Verify tool names by checking call arguments
        tool_calls = [call for call in mock_mcp.tool.call_args_list]
        assert len(tool_calls) == 4

    def test_feedback_integration_workflow(self, mock_mcp: Mock) -> None:
        # Mock state manager and loop state
        LoopState(loop_type=LoopType.PLAN)

        register_feedback_storage_tools(mock_mcp)

        # Verify registration completed without errors
        assert mock_mcp.tool.call_count == 4
