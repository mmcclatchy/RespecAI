from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from pydantic import ValidationError

from services.models.feedback import CriticFeedback
from services.utils.errors import LoopNotFoundError
from services.utils.models import MCPResponse
from services.utils.state_manager import StateManager


from services.shared import state_manager


class FeedbackTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def store_critic_feedback(self, feedback: CriticFeedback) -> MCPResponse:
        """Store structured critic feedback for any loop type.

        This universal tool works with ALL 5 workflow types and integrates
        with the existing sophisticated LoopState management system.
        """
        try:
            loop_state = self.state.get_loop(feedback.loop_id)
            loop_state.add_feedback(feedback)
            return loop_state.mcp_response
        except ValidationError:
            raise ToolError('Invalid feedback data provided')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error storing feedback: {str(e)}')

    def get_feedback_history(self, loop_id: str, count: int = 5) -> MCPResponse:
        """Retrieve recent feedback history for any loop type.

        Returns structured feedback history that critics can use for context
        and consistency across iterations. Works with ALL loop types.
        """
        try:
            loop_state = self.state.get_loop(loop_id)
            recent_feedback = loop_state.get_recent_feedback(count)

            if not recent_feedback:
                return MCPResponse(
                    id=loop_id, status=loop_state.status, message='No feedback history available for this loop'
                )

            message = self._format_feedback_summary(recent_feedback)
            return MCPResponse(id=loop_id, status=loop_state.status, message=message)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error retrieving feedback: {str(e)}')

    def _format_feedback_summary(self, recent_feedback: list[CriticFeedback]) -> str:
        feedback_count = len(recent_feedback)
        feedback_summaries = []
        for feedback in recent_feedback:
            summary = f'Iteration {feedback.iteration} (Score: {feedback.overall_score}): {feedback.assessment_summary}'
            feedback_summaries.append(summary)

        return f'Retrieved {feedback_count} feedback item{"s" if feedback_count != 1 else ""}: ' + '; '.join(
            feedback_summaries
        )


def register_feedback_tools(mcp: FastMCP) -> None:
    feedback_tools = FeedbackTools(state_manager)

    @mcp.tool()
    async def store_critic_feedback(
        loop_id: str,
        feedback_markdown: str,
        ctx: Context,
    ) -> MCPResponse:
        """Store structured critic feedback for any loop type from markdown.

        Parses markdown feedback into structured CriticFeedback and stores it.
        This universal tool works with ALL 5 workflow types and integrates
        with the existing sophisticated LoopState management system.

        Parameters:
        - feedback_markdown: Complete critic feedback in markdown format
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and storage confirmation
        """
        await ctx.info(f'Parsing and storing critic feedback for loop {loop_id}')
        try:
            # Parse markdown into structured feedback using the model's parse method
            feedback = CriticFeedback.parse_markdown(feedback_markdown)

            # Update loop_id to match the provided loop_id
            feedback.loop_id = loop_id

            result = feedback_tools.store_critic_feedback(feedback)
            await ctx.info(f'Stored feedback for loop {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to store critic feedback: {str(e)}')
            raise ToolError(f'Failed to store critic feedback: {str(e)}')

    @mcp.tool()
    async def get_feedback_history(loop_id: str, count: int, ctx: Context) -> MCPResponse:
        """Retrieve recent feedback history for any loop type.

        Returns structured feedback history that critics can use for context
        and consistency across iterations. Works with ALL loop types.

        Parameters:
        - loop_id: Unique identifier of the loop
        - count: Number of recent feedback items to retrieve

        Returns:
        - MCPResponse: Contains loop_id, status, and feedback history
        """
        await ctx.info(f'Retrieving feedback history for loop {loop_id}')
        try:
            result = feedback_tools.get_feedback_history(loop_id, count)
            await ctx.info(f'Retrieved {count} feedback items for loop {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to retrieve feedback history: {str(e)}')
            raise ResourceError(f'Feedback history unavailable for loop {loop_id}: {str(e)}')
