from fastmcp import FastMCP


from .loop_tools import register_loop_tools
from .feedback_tools import register_feedback_tools
from .project_plan_tools import register_project_plan_tools
from .roadmap_tools import register_roadmap_tools
from .spec_tools import register_spec_tools
from .build_plan_tools import register_build_plan_tools


def register_all_tools(mcp: FastMCP) -> None:
    register_loop_tools(mcp)
    register_feedback_tools(mcp)
    register_project_plan_tools(mcp)
    register_roadmap_tools(mcp)
    register_spec_tools(mcp)
    register_build_plan_tools(mcp)
