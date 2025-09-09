from typing import Callable

from .build_coder_template import generate_build_coder_template
from .build_planner_template import generate_build_planner_template
from .build_verifier_template import generate_build_verifier_template
from .plan_analyst_template import generate_plan_analyst_template
from .plan_conversation_analyst_template import generate_plan_conversation_analyst_template
from .plan_conversation_critic_template import generate_plan_conversation_critic_template
from .spec_architect_template import generate_spec_architect_template

AGENT_TEMPLATE_FUNCTIONS: dict[str, Callable[..., str]] = {
    'spec-architect': generate_spec_architect_template,
    'build-planner': generate_build_planner_template,
    'build-coder': generate_build_coder_template,
    'build-verifier': generate_build_verifier_template,
    'plan-analyst': generate_plan_analyst_template,
    'plan-conversation-analyst': generate_plan_conversation_analyst_template,
    'plan-conversation-critic': generate_plan_conversation_critic_template,
}
