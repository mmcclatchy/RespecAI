from pydantic import ValidationError

from services.models.enums import CriticAgent, FSSDCriteria
from services.models.feedback import CriticFeedback
from services.utils.errors import LoopNotFoundError, LoopStateError
from services.utils.models import MCPResponse
from services.utils.state_manager import StateManager


class FeedbackTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state

    def store_critic_feedback(
        self,
        loop_id: str,
        critic_agent: str,
        iteration: int,
        overall_assessment: str,
        improvements: list[str],
        fsdd_scores: dict[FSSDCriteria, int],
    ) -> MCPResponse:
        """Store structured critic feedback for any loop type.

        This universal tool works with ALL 5 workflow types and integrates
        with the existing sophisticated LoopState management system.
        """
        try:
            agent_enum = CriticAgent(critic_agent)
            feedback = CriticFeedback(
                session_id=loop_id,
                critic_agent=agent_enum,
                iteration=iteration,
                overall_assessment=overall_assessment,
                improvements=improvements,
                fsdd_scores=fsdd_scores,
            )
            loop_state = self.state.get_loop(loop_id)
            loop_state.add_feedback(feedback)
            return loop_state.mcp_response
        except ValidationError:
            raise LoopStateError(loop_id, 'feedback_storage', 'Invalid feedback data provided')
        except ValueError:
            raise LoopStateError(loop_id, 'feedback_storage', f'Invalid critic agent: {critic_agent}')
        except LoopNotFoundError:
            raise LoopStateError(loop_id, 'feedback_storage', 'Loop does not exist')
        except Exception as e:
            raise LoopStateError(loop_id, 'feedback_storage', f'Unexpected error storing feedback: {str(e)}')

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
            raise LoopStateError(loop_id, 'feedback_retrieval', 'Loop does not exist')
        except Exception as e:
            raise LoopStateError(loop_id, 'feedback_retrieval', f'Unexpected error retrieving feedback: {str(e)}')

    def _format_feedback_summary(self, recent_feedback: list[CriticFeedback]) -> str:
        feedback_count = len(recent_feedback)
        feedback_summaries = []
        for feedback in recent_feedback:
            summary = f'Iteration {feedback.iteration}: {feedback.overall_assessment}'
            feedback_summaries.append(summary)

        return f'Retrieved {feedback_count} feedback item{"s" if feedback_count != 1 else ""}: ' + '; '.join(
            feedback_summaries
        )
