from fastmcp import Context, FastMCP

from services.models.feedback import CriticFeedback
from services.shared import state_manager
from fastmcp.exceptions import ResourceError, ToolError

from services.utils.errors import LoopNotFoundError
from services.utils.models import MCPResponse
from services.utils.state_manager import StateManager


class FeedbackStorageTools:
    """Tools for storing and retrieving critic feedback and analysis using LoopState."""

    def __init__(self, state: StateManager) -> None:
        self.state = state
        # Simple storage for plan-analyst analysis data
        self._analysis_storage: dict[str, str] = {}

    def store_critic_feedback(self, loop_id: str, feedback_markdown: str) -> MCPResponse:
        """Store critic feedback by parsing markdown and adding to LoopState.

        Args:
            loop_id: Loop identifier
            feedback_markdown: CriticFeedback in markdown format

        Returns:
            MCPResponse with confirmation and score
        """
        if not loop_id or not loop_id.strip():
            raise ToolError('Loop ID cannot be empty')

        if not feedback_markdown or not feedback_markdown.strip():
            raise ToolError('Feedback markdown cannot be empty')

        try:
            loop_state = self.state.get_loop(loop_id)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')

        # Parse feedback markdown into CriticFeedback model
        feedback = self._parse_and_validate_feedback(feedback_markdown)

        # Add feedback to loop state (this also updates the score)
        loop_state.add_feedback(feedback)

        return MCPResponse(
            id=loop_id,
            status=loop_state.status,
            message=f'Stored {feedback.critic_agent.value} feedback for loop {loop_id} (Score: {feedback.overall_score})',
        )

    def _parse_and_validate_feedback(self, feedback_markdown: str) -> CriticFeedback:
        try:
            feedback = CriticFeedback.parse_markdown(feedback_markdown)
        except Exception as e:
            raise ToolError(f'Failed to parse feedback markdown: {str(e)}')

        # Check for explicitly unknown critic in markdown
        if 'UNKNOWN' in feedback_markdown.upper():
            raise ToolError('Feedback must specify a valid critic agent. Unknown critic specification found.')

        # Check if markdown lacks proper critic feedback header structure
        if '# Critic Feedback:' not in feedback_markdown:
            raise ToolError('Feedback must specify a valid critic agent. Missing critic feedback header.')

        # Validate that parsing found meaningful content (fallback for malformed structure)
        if (
            feedback.loop_id == 'unknown'
            and feedback.overall_score == 0
            and feedback.assessment_summary == 'Assessment Summary not provided'
        ):
            raise ToolError('Feedback must specify a valid critic agent. Markdown structure is invalid.')

        return feedback

    def get_previous_feedback(self, loop_id: str, count: int = 1) -> MCPResponse:
        """Get previous critic feedback from LoopState.

        Args:
            loop_id: Loop identifier
            count: Number of recent feedback entries to retrieve

        Returns:
            MCPResponse with feedback content or empty message
        """
        if not loop_id or not loop_id.strip():
            raise ToolError('Loop ID cannot be empty')

        if count <= 0:
            raise ToolError('Count must be a positive integer')

        try:
            loop_state = self.state.get_loop(loop_id)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')

        # Get recent feedback from loop state
        recent_feedback = loop_state.get_recent_feedback(count)

        if recent_feedback:
            # Build markdown for the most recent feedback
            latest_feedback = recent_feedback[-1]
            feedback_markdown = latest_feedback.build_markdown()
            message = f'Previous feedback for loop {loop_id}:\n\n{feedback_markdown}'
        else:
            message = f'No previous feedback found for loop {loop_id}'

        return MCPResponse(id=loop_id, status=loop_state.status, message=message)

    def store_current_analysis(self, loop_id: str, analysis: str) -> MCPResponse:
        """Store current business objectives analysis.

        Args:
            loop_id: Loop identifier
            analysis: Structured objectives analysis in markdown format

        Returns:
            MCPResponse with confirmation
        """
        if not loop_id or not loop_id.strip():
            raise ToolError('Loop ID cannot be empty')

        if not analysis or not analysis.strip():
            raise ToolError('Analysis cannot be empty')

        try:
            loop_state = self.state.get_loop(loop_id)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')

        # Store the analysis
        self._analysis_storage[loop_id] = analysis

        return MCPResponse(id=loop_id, status=loop_state.status, message=f'Stored analysis for loop {loop_id}')

    def get_previous_analysis(self, loop_id: str) -> MCPResponse:
        """Get previous business objectives analysis.

        Args:
            loop_id: Loop identifier

        Returns:
            MCPResponse with analysis content or empty message
        """
        if not loop_id or not loop_id.strip():
            raise ToolError('Loop ID cannot be empty')

        try:
            loop_state = self.state.get_loop(loop_id)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')

        # Get analysis if it exists
        analysis = self._analysis_storage.get(loop_id, '')

        if analysis:
            message = f'Previous analysis for loop {loop_id}:\n\n{analysis}'
        else:
            message = f'No previous analysis found for loop {loop_id}'

        return MCPResponse(id=loop_id, status=loop_state.status, message=message)


def register_feedback_storage_tools(mcp: FastMCP) -> None:
    feedback_tools = FeedbackStorageTools(state_manager)

    @mcp.tool()
    async def store_critic_feedback(loop_id: str, feedback_markdown: str, ctx: Context) -> MCPResponse:
        """Store critic feedback from plan-critic or analyst-critic.

        Parses structured markdown into CriticFeedback model and stores in LoopState.
        Used by both plan-critic and analyst-critic agents.

        Parameters:
        - loop_id: Loop identifier for the feedback
        - feedback_markdown: CriticFeedback in structured markdown format

        Returns:
        - MCPResponse: Contains loop_id, status, and confirmation with score
        """
        await ctx.info(f'Storing critic feedback for loop {loop_id}')

        try:
            result = feedback_tools.store_critic_feedback(loop_id, feedback_markdown)
            await ctx.info(f'Stored feedback for loop {loop_id}')
            return result
        except (ToolError, ResourceError) as e:
            await ctx.error(f'Failed to store feedback: {str(e)}')
            raise
        except Exception as e:
            await ctx.error(f'Unexpected error storing feedback: {str(e)}')
            raise ToolError(f'Unexpected error storing feedback: {str(e)}')

    @mcp.tool()
    async def get_previous_feedback(loop_id: str, count: int, ctx: Context) -> MCPResponse:
        """Get previous critic feedback for iterative improvement.

        Retrieves recent feedback from LoopState.feedback_history.
        Used by agents to review prior feedback before generating new assessments.

        Parameters:
        - loop_id: Loop identifier
        - count: Number of recent feedback entries to retrieve (default: 1)

        Returns:
        - MCPResponse: Contains previous feedback in markdown format
        """
        await ctx.info(f'Retrieving previous feedback for loop {loop_id}')

        try:
            result = feedback_tools.get_previous_feedback(loop_id, count)
            await ctx.info(f'Retrieved feedback for loop {loop_id}')
            return result
        except (ToolError, ResourceError) as e:
            await ctx.error(f'Failed to retrieve feedback: {str(e)}')
            raise
        except Exception as e:
            await ctx.error(f'Unexpected error retrieving feedback: {str(e)}')
            raise ResourceError(f'Unexpected error retrieving feedback for loop {loop_id}: {str(e)}')

    @mcp.tool()
    async def store_current_analysis(loop_id: str, analysis: str, ctx: Context) -> MCPResponse:
        """Store current business objectives analysis.

        Used by plan-analyst to store iterative analysis results.

        Parameters:
        - loop_id: Loop identifier for the analyst validation process
        - analysis: Structured objectives analysis in markdown format

        Returns:
        - MCPResponse: Contains loop_id, status, and confirmation message
        """
        await ctx.info(f'Storing analysis for loop {loop_id}')

        try:
            result = feedback_tools.store_current_analysis(loop_id, analysis)
            await ctx.info(f'Stored analysis for loop {loop_id}')
            return result
        except (ToolError, ResourceError) as e:
            await ctx.error(f'Failed to store analysis: {str(e)}')
            raise
        except Exception as e:
            await ctx.error(f'Unexpected error storing analysis: {str(e)}')
            raise ToolError(f'Unexpected error storing analysis: {str(e)}')

    @mcp.tool()
    async def get_previous_analysis(loop_id: str, ctx: Context) -> MCPResponse:
        """Get previous business objectives analysis.

        Used by plan-analyst to retrieve prior analysis for iterative improvement.

        Parameters:
        - loop_id: Loop identifier for the analyst validation process

        Returns:
        - MCPResponse: Contains previous analysis content or empty message
        """
        await ctx.info(f'Retrieving previous analysis for loop {loop_id}')

        try:
            result = feedback_tools.get_previous_analysis(loop_id)
            await ctx.info(f'Retrieved analysis for loop {loop_id}')
            return result
        except (ToolError, ResourceError) as e:
            await ctx.error(f'Failed to retrieve analysis: {str(e)}')
            raise
        except Exception as e:
            await ctx.error(f'Unexpected error retrieving analysis: {str(e)}')
            raise ResourceError(f'Unexpected error retrieving analysis for loop {loop_id}: {str(e)}')
