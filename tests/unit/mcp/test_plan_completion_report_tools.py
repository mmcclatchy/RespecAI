import pytest
from unittest.mock import Mock, patch
from fastmcp.exceptions import ResourceError, ToolError

from services.mcp.tools.plan_completion_report_tools import PlanCompletionReportTools
from services.models.plan_completion_report import PlanCompletionReport
from services.utils.enums import LoopStatus, LoopType
from services.utils.errors import LoopNotFoundError
from services.utils.models import LoopState, MCPResponse


from services.mcp.tools.plan_completion_report_tools import register_plan_completion_report_tools


class TestPlanCompletionReportTools:
    """Test suite for PlanCompletionReportTools class."""

    @pytest.fixture
    def mock_state_manager(self) -> Mock:
        return Mock()

    @pytest.fixture
    def completion_report_tools(self, mock_state_manager: Mock) -> PlanCompletionReportTools:
        return PlanCompletionReportTools(mock_state_manager)

    @pytest.fixture
    def sample_completion_report(self) -> PlanCompletionReport:
        return PlanCompletionReport(
            report_title='Test Completion Report',
            final_plan_score='85',
            final_analyst_score='90',
            strategic_plan_document='# Test Plan\nContent here',
            structured_objectives='Test objectives',
            analyst_loop_id='test-loop-123',
        )

    @pytest.fixture
    def sample_loop_state(self) -> LoopState:
        return LoopState(loop_type=LoopType.PLAN)

    def test_create_completion_report_success(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = completion_report_tools.create_completion_report(sample_completion_report, loop_id)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert result.status == sample_loop_state.status
        assert 'Test Completion Report' in result.message
        mock_state_manager.get_loop.assert_called_once_with(loop_id)
        assert completion_report_tools._completion_reports[loop_id] == sample_completion_report

    def test_create_completion_report_none_report(
        self, completion_report_tools: PlanCompletionReportTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'test-loop-123'

        with pytest.raises(ToolError, match='Invalid input: PlanCompletionReport cannot be None'):
            completion_report_tools.create_completion_report(None, loop_id)  # type: ignore

    def test_create_completion_report_empty_loop_id(
        self, completion_report_tools: PlanCompletionReportTools, sample_completion_report: PlanCompletionReport
    ) -> None:
        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.create_completion_report(sample_completion_report, '')

        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.create_completion_report(sample_completion_report, '   ')

    def test_create_completion_report_duplicate(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        # Create first report
        completion_report_tools.create_completion_report(sample_completion_report, loop_id)

        # Try to create another report for same loop
        with pytest.raises(ToolError, match='Invalid input: Completion report already exists for loop'):
            completion_report_tools.create_completion_report(sample_completion_report, loop_id)

    def test_create_completion_report_loop_not_found(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
    ) -> None:
        loop_id = 'non-existent-loop'
        mock_state_manager.get_loop.side_effect = LoopNotFoundError('Loop not found')

        with pytest.raises(ResourceError, match='Loop does not exist'):
            completion_report_tools.create_completion_report(sample_completion_report, loop_id)

    def test_store_completion_report_success(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = completion_report_tools.store_completion_report(sample_completion_report, loop_id)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert 'Test Completion Report' in result.message
        assert completion_report_tools._completion_reports[loop_id] == sample_completion_report

    def test_get_completion_report_data_success(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state
        completion_report_tools._completion_reports[loop_id] = sample_completion_report

        result = completion_report_tools.get_completion_report_data(loop_id)

        assert result == sample_completion_report
        mock_state_manager.get_loop.assert_called_once_with(loop_id)

    def test_get_completion_report_data_not_found(
        self, completion_report_tools: PlanCompletionReportTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        with pytest.raises(ResourceError, match='No completion report stored for this loop'):
            completion_report_tools.get_completion_report_data(loop_id)

    def test_get_completion_report_markdown_success(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state
        completion_report_tools._completion_reports[loop_id] = sample_completion_report

        result = completion_report_tools.get_completion_report_markdown(loop_id)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert '# Test Completion Report' in result.message
        assert '## Plan Quality' in result.message

    def test_update_completion_report_success(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state
        completion_report_tools._completion_reports[loop_id] = sample_completion_report

        updated_report = PlanCompletionReport(report_title='Updated Report', final_plan_score='95')

        result = completion_report_tools.update_completion_report(updated_report, loop_id)

        assert isinstance(result, MCPResponse)
        assert 'Updated Report' in result.message
        assert completion_report_tools._completion_reports[loop_id] == updated_report

    def test_update_completion_report_not_found(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        with pytest.raises(ResourceError, match='No completion report stored for this loop'):
            completion_report_tools.update_completion_report(sample_completion_report, loop_id)

    def test_list_completion_reports_empty(self, completion_report_tools: PlanCompletionReportTools) -> None:
        result = completion_report_tools.list_completion_reports()

        assert isinstance(result, MCPResponse)
        assert result.id == 'list'
        assert result.status == LoopStatus.INITIALIZED
        assert 'No completion reports found' in result.message

    def test_list_completion_reports_with_data(
        self, completion_report_tools: PlanCompletionReportTools, sample_completion_report: PlanCompletionReport
    ) -> None:
        loop_id1 = 'loop-1'
        loop_id2 = 'loop-2'

        report1 = PlanCompletionReport(report_title='Report 1', final_plan_score='80')
        report2 = PlanCompletionReport(report_title='Report 2', final_plan_score='90')

        completion_report_tools._completion_reports[loop_id1] = report1
        completion_report_tools._completion_reports[loop_id2] = report2

        result = completion_report_tools.list_completion_reports(count=10)

        assert isinstance(result, MCPResponse)
        assert result.status == LoopStatus.COMPLETED
        assert 'Found 2 completion reports' in result.message
        assert 'Report 1' in result.message
        assert 'Report 2' in result.message
        assert '80%' in result.message
        assert '90%' in result.message

    def test_list_completion_reports_with_count_limit(self, completion_report_tools: PlanCompletionReportTools) -> None:
        # Create 5 reports
        for i in range(5):
            loop_id = f'loop-{i}'
            report = PlanCompletionReport(report_title=f'Report {i}', final_plan_score=f'{80 + i}')
            completion_report_tools._completion_reports[loop_id] = report

        result = completion_report_tools.list_completion_reports(count=3)

        assert 'Found 3 completion reports' in result.message
        # Should return the last 3 (most recent)
        assert 'Report 2' in result.message
        assert 'Report 3' in result.message
        assert 'Report 4' in result.message
        assert 'Report 0' not in result.message
        assert 'Report 1' not in result.message

    def test_list_completion_reports_invalid_count(self, completion_report_tools: PlanCompletionReportTools) -> None:
        with pytest.raises(ToolError, match='Invalid input: Count must be a positive integer'):
            completion_report_tools.list_completion_reports(count=0)

        with pytest.raises(ToolError, match='Invalid input: Count must be a positive integer'):
            completion_report_tools.list_completion_reports(count=-5)

    def test_get_completion_report_data_empty_loop_id(self, completion_report_tools: PlanCompletionReportTools) -> None:
        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.get_completion_report_data('')

        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.get_completion_report_data('   ')

    def test_store_completion_report_empty_loop_id(
        self, completion_report_tools: PlanCompletionReportTools, sample_completion_report: PlanCompletionReport
    ) -> None:
        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.store_completion_report(sample_completion_report, '')

    def test_update_completion_report_empty_loop_id(
        self, completion_report_tools: PlanCompletionReportTools, sample_completion_report: PlanCompletionReport
    ) -> None:
        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.update_completion_report(sample_completion_report, '')

    def test_delete_completion_report_empty_loop_id(self, completion_report_tools: PlanCompletionReportTools) -> None:
        with pytest.raises(ToolError, match='Invalid input: Loop ID cannot be empty'):
            completion_report_tools.delete_completion_report('')

    def test_delete_completion_report_success(
        self,
        completion_report_tools: PlanCompletionReportTools,
        mock_state_manager: Mock,
        sample_completion_report: PlanCompletionReport,
        sample_loop_state: LoopState,
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state
        completion_report_tools._completion_reports[loop_id] = sample_completion_report

        result = completion_report_tools.delete_completion_report(loop_id)

        assert isinstance(result, MCPResponse)
        assert result.id == loop_id
        assert result.status == LoopStatus.COMPLETED
        assert 'Test Completion Report' in result.message
        assert loop_id not in completion_report_tools._completion_reports

    def test_delete_completion_report_not_stored(
        self, completion_report_tools: PlanCompletionReportTools, mock_state_manager: Mock, sample_loop_state: LoopState
    ) -> None:
        loop_id = 'test-loop-123'
        mock_state_manager.get_loop.return_value = sample_loop_state

        result = completion_report_tools.delete_completion_report(loop_id)

        assert isinstance(result, MCPResponse)
        assert 'Unknown' in result.message

    def test_delete_completion_report_loop_not_found(
        self, completion_report_tools: PlanCompletionReportTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'non-existent-loop'
        mock_state_manager.get_loop.side_effect = LoopNotFoundError('Loop not found')

        with pytest.raises(ResourceError, match='Loop does not exist'):
            completion_report_tools.delete_completion_report(loop_id)

    def test_exception_handling_in_methods(
        self, completion_report_tools: PlanCompletionReportTools, mock_state_manager: Mock
    ) -> None:
        loop_id = 'test-loop'

        # Test unexpected exception in create
        mock_state_manager.get_loop.side_effect = Exception('Unexpected error')
        sample_report = PlanCompletionReport()

        with pytest.raises(ToolError, match='Unexpected error creating completion report'):
            completion_report_tools.create_completion_report(sample_report, loop_id)

        # Test unexpected exception in get_completion_report_data
        mock_state_manager.get_loop.side_effect = Exception('Unexpected error')

        with pytest.raises(ToolError, match='Unexpected error retrieving completion report'):
            completion_report_tools.get_completion_report_data(loop_id)

        # Test unexpected exception in list
        completion_report_tools._completion_reports = Mock()
        completion_report_tools._completion_reports.__bool__ = Mock(side_effect=Exception('Unexpected error'))

        with pytest.raises(ToolError, match='Unexpected error listing completion reports'):
            completion_report_tools.list_completion_reports()


class TestPlanCompletionReportToolsRegistration:
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

    @patch('services.mcp.tools.plan_completion_report_tools.state_manager')
    def test_mcp_tools_registration(self, mock_state_manager: Mock, mock_mcp: Mock) -> None:
        register_plan_completion_report_tools(mock_mcp)

        # Verify that mcp.tool() was called for each tool
        assert mock_mcp.tool.call_count == 6  # 6 tools total

    @patch('services.mcp.tools.plan_completion_report_tools.PlanCompletionReportTools')
    @patch('services.mcp.tools.plan_completion_report_tools.state_manager')
    def test_create_tool_integration(
        self, mock_state_manager: Mock, mock_tools_class: Mock, mock_mcp: Mock, mock_context: Mock
    ) -> None:
        # Setup mock
        mock_tools_instance = Mock()
        mock_tools_class.return_value = mock_tools_instance
        mock_tools_instance.create_completion_report.return_value = MCPResponse(
            id='test-id', status=LoopStatus.COMPLETED, message='Success'
        )

        register_plan_completion_report_tools(mock_mcp)

        # Verify that mcp.tool() was called the expected number of times
        assert mock_mcp.tool.call_count == 6  # 6 tools registered
