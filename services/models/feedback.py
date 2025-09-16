import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from .enums import CriticAgent


class CriticFeedback(BaseModel):
    loop_id: str
    critic_agent: CriticAgent
    iteration: int
    overall_score: int
    assessment_summary: str
    detailed_feedback: str
    key_issues: list[str]
    recommendations: list[str]
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('overall_score')
    @classmethod
    def validate_score_range(cls, score: int) -> int:
        if not (0 <= score <= 100):
            raise ValueError('Overall score must be between 0 and 100')
        return score

    @property
    def quality_score(self) -> int:
        return self.overall_score

    @classmethod
    def parse_markdown(cls, markdown: str) -> 'CriticFeedback':
        # Define regex patterns for template sections
        sections = {
            'loop_id': r'\*\*Loop ID\*\*:\s*`([^`]+)`',
            'iteration': r'\*\*Iteration\*\*:\s*`([^`]+)`',
            'overall_score': r'\*\*Overall Score\*\*:\s*`([^`]+)`',
            'assessment_summary': r'## Assessment Summary\s*\n`([^`]+)`',
            'detailed_feedback': r'## Detailed Analysis\s*\n\n(.*?)(?=\n## |$)',
            'key_issues': r'## Key Issues\s*\n\n(.*?)(?=\n## |$)',
            'recommendations': r'## Recommendations\s*\n\n(.*?)(?=\n## |\n---|$)',
            'critic_agent': r'\*\*Critic\*\*:\s*`([^`]+)`',
        }

        # Extract critic agent from title if available
        title_match = re.search(r'# Critic Feedback:\s*(.+)', markdown)
        critic_name = title_match.group(1).strip() if title_match else 'ANALYST'

        # Extract sections using regex
        extracted = {}
        for field, pattern in sections.items():
            match = re.search(pattern, markdown, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
            else:
                # Set defaults for missing fields
                if field == 'loop_id':
                    extracted[field] = 'unknown'
                elif field == 'iteration':
                    extracted[field] = '1'
                elif field == 'overall_score':
                    extracted[field] = '0'
                elif field == 'critic_agent':
                    extracted[field] = critic_name
                else:
                    extracted[field] = f'{field.replace("_", " ").title()} not provided'

        # Parse critic agent enum - map common names to actual enum values
        agent_name = extracted['critic_agent'].upper()
        agent_mapping = {
            'ANALYST': CriticAgent.ANALYST_CRITIC,
            'ANALYST-CRITIC': CriticAgent.ANALYST_CRITIC,
            'PLAN': CriticAgent.PLAN_CRITIC,
            'PLAN-CRITIC': CriticAgent.PLAN_CRITIC,
            'ROADMAP': CriticAgent.ROADMAP_CRITIC,
            'ROADMAP-CRITIC': CriticAgent.ROADMAP_CRITIC,
            'SPEC': CriticAgent.SPEC_CRITIC,
            'SPEC-CRITIC': CriticAgent.SPEC_CRITIC,
            'BUILD': CriticAgent.BUILD_CRITIC,
            'BUILD-CRITIC': CriticAgent.BUILD_CRITIC,
            'BUILD-REVIEWER': CriticAgent.BUILD_REVIEWER,
            'REVIEWER': CriticAgent.BUILD_REVIEWER,
        }

        critic_agent = agent_mapping.get(agent_name, CriticAgent.ANALYST_CRITIC)

        # Parse iteration and score
        try:
            iteration = int(extracted['iteration'])
        except ValueError:
            iteration = 1

        try:
            overall_score = int(extracted['overall_score'])
        except ValueError:
            overall_score = 0

        # Parse list fields from markdown bullet points
        key_issues = []
        if extracted['key_issues'] and extracted['key_issues'] != 'Key Issues not provided':
            for line in extracted['key_issues'].split('\n'):
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    key_issues.append(line[2:].strip())

        recommendations = []
        if extracted['recommendations'] and extracted['recommendations'] != 'Recommendations not provided':
            for line in extracted['recommendations'].split('\n'):
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    recommendations.append(line[2:].strip())

        return cls(
            loop_id=extracted['loop_id'],
            critic_agent=critic_agent,
            iteration=iteration,
            overall_score=overall_score,
            assessment_summary=extracted['assessment_summary'],
            detailed_feedback=extracted['detailed_feedback'],
            key_issues=key_issues,
            recommendations=recommendations,
        )

    def build_markdown(self) -> str:
        # Format list items
        issues_md = '\n'.join([f'- {issue}' for issue in self.key_issues]) if self.key_issues else 'None identified'
        recommendations_md = (
            '\n'.join([f'- {rec}' for rec in self.recommendations]) if self.recommendations else 'None provided'
        )

        return f"""# Critic Feedback: {self.critic_agent.value.upper()}

**Loop ID**: `{self.loop_id}`
**Iteration**: `{self.iteration}`
**Overall Score**: `{self.overall_score}`

## Assessment Summary

`{self.assessment_summary}`

## Detailed Analysis

{self.detailed_feedback}

## Key Issues

{issues_md}

## Recommendations

{recommendations_md}

---

**Critic**: `{self.critic_agent.value.upper()}`
**Timestamp**: `{self.timestamp.isoformat()}`
**Status**: `completed`"""
