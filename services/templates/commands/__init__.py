from typing import Callable

from .build_command_template import generate_build_command_template
from .refine_build_command_template import generate_refine_build_command_template
from .refine_spec_command_template import generate_refine_spec_command_template
from .spec_command_template import generate_spec_command_template
from .spec_manager_template import generate_spec_manager_command
from .spec_setup_command_template import generate_spec_setup_command_template
from .validate_command_template import generate_validate_command_template

COMMAND_TEMPLATE_FUNCTIONS: dict[str, Callable[..., str]] = {
    'spec': generate_spec_command_template,
    'build': generate_build_command_template,
    'refine-spec': generate_refine_spec_command_template,
    'refine-build': generate_refine_build_command_template,
    'validate': generate_validate_command_template,
    'spec-manager': generate_spec_manager_command,
    'spec-setup': generate_spec_setup_command_template,
}
