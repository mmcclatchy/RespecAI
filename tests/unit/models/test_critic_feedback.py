from datetime import datetime

import pytest

from services.models.enums import CriticAgent, FSSDCriteria
from services.models.feedback import CriticFeedback


class TestCriticFeedback:
    def test_critic_feedback_creation_with_all_fields(self) -> None:
        fsdd_scores = {
            FSSDCriteria.CLARITY: 8,
            FSSDCriteria.COMPLETENESS: 7,
            FSSDCriteria.CONSISTENCY: 9,
            FSSDCriteria.FEASIBILITY: 8,
            FSSDCriteria.TESTABILITY: 7,
            FSSDCriteria.MAINTAINABILITY: 8,
            FSSDCriteria.SCALABILITY: 6,
            FSSDCriteria.SECURITY: 9,
            FSSDCriteria.PERFORMANCE: 7,
            FSSDCriteria.USABILITY: 8,
            FSSDCriteria.DOCUMENTATION: 6,
            FSSDCriteria.INTEGRATION: 8,
        }

        feedback = CriticFeedback(
            session_id='test-session-123',
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=3,
            overall_assessment='Good technical specification with minor improvements needed',
            improvements=['Add more security details', 'Clarify integration patterns'],
            fsdd_scores=fsdd_scores,
        )

        assert feedback.session_id == 'test-session-123'
        assert feedback.critic_agent == CriticAgent.SPEC_CRITIC
        assert feedback.iteration == 3
        assert feedback.overall_assessment == 'Good technical specification with minor improvements needed'
        assert feedback.improvements == ['Add more security details', 'Clarify integration patterns']
        assert feedback.fsdd_scores == fsdd_scores
        assert isinstance(feedback.timestamp, datetime)

    def test_quality_score_automatically_calculated_from_fsdd_scores(self) -> None:
        fsdd_scores = {
            FSSDCriteria.CLARITY: 8,
            FSSDCriteria.COMPLETENESS: 7,
            FSSDCriteria.CONSISTENCY: 9,
            FSSDCriteria.FEASIBILITY: 8,
            FSSDCriteria.TESTABILITY: 7,
            FSSDCriteria.MAINTAINABILITY: 8,
            FSSDCriteria.SCALABILITY: 6,
            FSSDCriteria.SECURITY: 9,
            FSSDCriteria.PERFORMANCE: 7,
            FSSDCriteria.USABILITY: 8,
            FSSDCriteria.DOCUMENTATION: 6,
            FSSDCriteria.INTEGRATION: 8,
        }

        feedback = CriticFeedback(
            session_id='test-session',
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=1,
            overall_assessment='Test assessment',
            improvements=[],
            fsdd_scores=fsdd_scores,
        )

        # Average = (8+7+9+8+7+8+6+9+7+8+6+8) / 12 = 91 / 12 = 7.58333...
        # Overall score = 7.58333... * 10 = 75.8333... -> 76 (rounded)
        expected_score = 76
        assert feedback.quality_score == expected_score

    def test_quality_score_with_empty_scores_returns_zero(self) -> None:
        feedback = CriticFeedback(
            session_id='test-session',
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=1,
            overall_assessment='Test assessment',
            improvements=[],
            fsdd_scores={},
        )

        assert feedback.quality_score == 0

    def test_quality_score_with_all_scores_equal_returns_correct_percentage(self) -> None:
        fsdd_scores = {criteria: 8 for criteria in FSSDCriteria}

        feedback = CriticFeedback(
            session_id='test-session',
            critic_agent=CriticAgent.SPEC_CRITIC,
            iteration=1,
            overall_assessment='Test assessment',
            improvements=[],
            fsdd_scores=fsdd_scores,
        )

        # All scores are 8, so average is 8, overall score is 80
        assert feedback.quality_score == 80

    def test_fsdd_scores_validation_ensures_valid_score_range(self) -> None:
        invalid_scores = {
            FSSDCriteria.CLARITY: 11,  # Invalid: > 10
            FSSDCriteria.COMPLETENESS: -1,  # Invalid: < 0
        }

        with pytest.raises(ValueError, match='FSDD scores must be between 0 and 10'):
            CriticFeedback(
                session_id='test-session',
                critic_agent=CriticAgent.SPEC_CRITIC,
                iteration=1,
                overall_assessment='Test assessment',
                improvements=[],
                fsdd_scores=invalid_scores,
            )
