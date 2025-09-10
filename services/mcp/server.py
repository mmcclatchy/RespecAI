from fastmcp import FastMCP
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Literal
from services.mcp import loop_tools


class MCPSettings(BaseSettings):
    server_name: str = 'Loop Management Server'
    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = False

    model_config = {'env_prefix': 'MCP_', 'env_file': '.env'}


class HealthStatus(BaseModel):
    status: Literal['healthy', 'unhealthy']
    tools_count: int = 0
    error: str | None = None


def get_server_config() -> MCPSettings:
    return MCPSettings()


def create_mcp_server() -> FastMCP:
    config = get_server_config()
    mcp = FastMCP(config.server_name)

    # Register the existing decide_loop_next_action tool
    # Function accessed by FastMCP framework, not directly by our code
    @mcp.tool()
    def decide_loop_next_action(
        loop_type: str, current_score: int, previous_scores: list[int], iteration: int, max_iterations: int = 5
    ) -> str:
        """Decide next action for refinement loop progression.

        This MCP tool implements the core decision logic for quality-driven
        refinement loops. It analyzes current quality scores, improvement trends,
        and iteration counts to determine whether to continue refining content,
        complete the loop, or escalate to human input.

        Decision Logic:
        - "complete": Score meets or exceeds threshold for the loop type
        - "refine": Score below threshold but showing improvement or early iterations
        - "user-input": Stagnation detected (2 consecutive low improvements) or max iterations reached

        Parameters:
        - loop_type: One of 'plan', 'spec', 'build_plan', 'build_code'
        - current_score: Quality score from 0-100 for current iteration
        - previous_scores: List of scores from previous iterations (chronological order)
        - iteration: Current iteration number (must be >= 1)
        - max_iterations: Maximum iterations before forcing user-input (default: 5)

        Returns:
        - "complete": Quality threshold met, proceed to next phase
        - "refine": Continue refinement loop with critic feedback
        - "user-input": Request human intervention due to stagnation or limits

        Raises:
        - ValueError: Invalid parameters (scores outside 0-100, invalid loop_type, etc.)

        Example Usage:
        ```
        # High quality score - should complete
        action = decide_loop_next_action("plan", 90, [85, 87], 3)
        # Returns: "complete"

        # Improving score below threshold - should refine
        action = decide_loop_next_action("spec", 70, [60], 2)
        # Returns: "refine"

        # Stagnating scores - should request user input
        action = decide_loop_next_action("build_code", 75, [73, 74], 5)
        # Returns: "user-input"
        ```
        """
        return loop_tools.decide_loop_next_action(loop_type, current_score, previous_scores, iteration, max_iterations)

    @mcp.tool()
    def initialize_refinement_loop(loop_type: str, initial_content: str) -> dict:
        """Initialize a new refinement loop with initial content.

        Creates a new refinement loop session with the provided initial content.
        Returns loop ID for tracking and managing the loop state throughout
        the refinement process.

        Parameters:
        - loop_type: One of 'plan', 'spec', 'build_plan', 'build_code'
        - initial_content: Initial content to start refining (cannot be empty)

        Returns:
        - dict: Contains 'loop_id' (unique identifier) and 'status' ('initialized')

        Raises:
        - ValueError: Invalid loop_type or empty initial_content
        """
        return loop_tools.initialize_refinement_loop(loop_type, initial_content)

    @mcp.tool()
    def reset_loop_state(loop_id: str) -> dict:
        """Reset loop state for fresh start.

        Clears iteration count and score history while preserving the loop
        configuration and initial content. Useful for restarting a loop
        from the beginning.

        Parameters:
        - loop_id: Unique identifier of the loop to reset

        Returns:
        - dict: Contains 'loop_id' and 'status' ('reset')

        Raises:
        - ValueError: Loop ID not found
        """
        return loop_tools.reset_loop_state(loop_id)

    @mcp.tool()
    def get_loop_status(loop_id: str) -> dict:
        """Get current status and history of a loop.

        Returns complete loop information including current status,
        iteration count, score history, and metadata.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - dict: Complete loop state with all metadata and history

        Raises:
        - ValueError: Loop ID not found
        """
        return loop_tools.get_loop_status(loop_id)

    @mcp.tool()
    def list_active_loops() -> list[dict]:
        """List all currently active refinement loops.

        Returns summary information for all active loops in the current
        session. Useful for managing multiple concurrent refinement processes.

        Returns:
        - list[dict]: List of active loops with their current status
        """
        return loop_tools.list_active_loops()

    return mcp


def run_local_server() -> None:
    server = create_mcp_server()
    server.run(transport='stdio')


async def health_check(server: FastMCP) -> HealthStatus:
    try:
        tools = await server.get_tools()
        return HealthStatus(status='healthy', tools_count=len(tools))
    except Exception as e:
        return HealthStatus(status='unhealthy', error=str(e))
