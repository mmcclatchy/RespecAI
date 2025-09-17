from fastmcp import Context, FastMCP
from fastmcp.exceptions import ResourceError, ToolError
from pydantic import ValidationError

from services.models.spec import TechnicalSpec
from services.shared import state_manager
from services.utils.enums import LoopStatus
from services.utils.errors import LoopNotFoundError
from services.utils.models import MCPResponse
from services.utils.state_manager import StateManager


class SpecTools:
    def __init__(self, state: StateManager) -> None:
        self.state = state
        self._technical_specs: dict[str, TechnicalSpec] = {}

    def store_technical_spec(self, spec: TechnicalSpec, loop_id: str) -> MCPResponse:
        try:
            if spec is None:
                raise ValueError('TechnicalSpec cannot be None')

            loop_state = self.state.get_loop(loop_id)
            self._technical_specs[loop_id] = spec
            return MCPResponse(
                id=loop_id,
                status=loop_state.status,
                message=f'Stored technical specification: {spec.phase_name}',
            )
        except ValidationError:
            raise ToolError('Invalid technical specification data provided')
        except ValueError:
            raise ToolError('Invalid technical specification: cannot be None')
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error storing technical specification: {str(e)}')

    def get_technical_spec_data(self, loop_id: str) -> TechnicalSpec:
        try:
            self.state.get_loop(loop_id)

            if loop_id not in self._technical_specs:
                raise ResourceError('No technical specification stored for this loop')

            return self._technical_specs[loop_id]
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except (ResourceError, ToolError):
            raise
        except Exception as e:
            raise ToolError(f'Unexpected error retrieving technical specification: {str(e)}')

    def get_technical_spec_markdown(self, loop_id: str) -> MCPResponse:
        try:
            loop_state = self.state.get_loop(loop_id)
            technical_spec = self.get_technical_spec_data(loop_id)

            markdown = technical_spec.build_markdown()
            return MCPResponse(id=loop_id, status=loop_state.status, message=markdown)
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error generating markdown: {str(e)}')

    def list_technical_specs(self, count: int = 10) -> MCPResponse:
        try:
            if not self._technical_specs:
                return MCPResponse(
                    id='list', status=LoopStatus.INITIALIZED, message='No technical specifications found'
                )

            spec_items = list(self._technical_specs.items())[-count:]
            spec_count = len(spec_items)

            spec_summaries = []
            for loop_id, spec in spec_items:
                summary = f'ID: {loop_id}, Specification: {spec.phase_name}'
                spec_summaries.append(summary)

            message = f'Found {spec_count} technical spec{"s" if spec_count != 1 else ""}: ' + '; '.join(spec_summaries)
            return MCPResponse(id='list', status=LoopStatus.COMPLETED, message=message)
        except Exception as e:
            raise ToolError(f'Unexpected error listing technical specifications: {str(e)}')

    def delete_technical_spec(self, loop_id: str) -> MCPResponse:
        try:
            self.state.get_loop(loop_id)

            if loop_id in self._technical_specs:
                spec_name = self._technical_specs[loop_id].phase_name
                del self._technical_specs[loop_id]
            else:
                spec_name = 'Unknown'
            return MCPResponse(
                id=loop_id, status=LoopStatus.COMPLETED, message=f'Deleted technical specification: {spec_name}'
            )
        except LoopNotFoundError:
            raise ResourceError('Loop does not exist')
        except Exception as e:
            raise ToolError(f'Unexpected error deleting technical specification: {str(e)}')


def register_spec_tools(mcp: FastMCP) -> None:
    spec_tools = SpecTools(state_manager)

    @mcp.tool()
    async def store_technical_spec(loop_id: str, spec_markdown: str, ctx: Context) -> MCPResponse:
        """Store technical specification from markdown.

        Parses markdown content into a TechnicalSpec model and stores it with
        the specified loop.

        Parameters:
        - loop_id: Loop ID to store the technical specification in
        - spec_markdown: Complete technical specification in markdown format

        Returns:
        - MCPResponse: Contains loop_id, status, and confirmation message
        """
        await ctx.info(f'Parsing and storing technical specification with loop_id: {loop_id}')

        try:
            technical_spec = TechnicalSpec.parse_markdown(spec_markdown)
            result = spec_tools.store_technical_spec(technical_spec, loop_id)

            await ctx.info(f'Stored technical specification with ID: {result.id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to store technical specification: {str(e)}')
            raise ToolError(f'Failed to store technical specification: {str(e)}')

    @mcp.tool()
    async def get_technical_spec_markdown(loop_id: str, ctx: Context) -> MCPResponse:
        """Generate markdown for technical specification.

        Retrieves stored technical specification and formats as markdown

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and formatted markdown content
        """
        await ctx.info(f'Generating markdown for technical specification {loop_id}')
        try:
            result = spec_tools.get_technical_spec_markdown(loop_id)
            await ctx.info(f'Generated markdown for technical specification {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to generate technical specification markdown: {str(e)}')
            raise ResourceError(f'Technical specification not found for loop {loop_id}: {str(e)}')

    @mcp.tool()
    async def list_technical_specs(count: int, ctx: Context) -> MCPResponse:
        """List available technical specifications.

        Returns summary of stored technical specifications with basic metadata.

        Parameters:
        - count: Maximum number of specifications to return

        Returns:
        - MCPResponse: Contains list status and technical specification summaries
        """
        await ctx.info(f'Listing up to {count} technical specifications')
        try:
            result = spec_tools.list_technical_specs(count)
            await ctx.info('Retrieved technical specification list')
            return result
        except Exception as e:
            await ctx.error(f'Failed to list technical specifications: {str(e)}')
            raise ToolError(f'Failed to list technical specifications: {str(e)}')

    @mcp.tool()
    async def delete_technical_spec(loop_id: str, ctx: Context) -> MCPResponse:
        """Delete a stored technical specification.

        Removes technical specification data associated with the given loop ID.

        Parameters:
        - loop_id: Unique identifier of the loop

        Returns:
        - MCPResponse: Contains loop_id, status, and deletion confirmation
        """
        await ctx.info(f'Deleting technical specification {loop_id}')
        try:
            result = spec_tools.delete_technical_spec(loop_id)
            await ctx.info(f'Deleted technical specification {loop_id}')
            return result
        except Exception as e:
            await ctx.error(f'Failed to delete technical specification: {str(e)}')
            raise ToolError(f'Failed to delete technical specification: {str(e)}')
