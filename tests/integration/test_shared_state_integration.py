import pytest
from fastmcp.exceptions import ResourceError

from services.mcp.loop_tools import LoopTools
from services.mcp.roadmap_tools import RoadmapTools
from services.shared import state_manager
from services.utils.enums import LoopStatus
from services.utils.errors import LoopStateError
from services.utils.state_manager import InMemoryStateManager


def create_test_roadmap_markdown(project_name: str) -> str:
    return f"""# Project Roadmap: {project_name}

## Project Details
- **Project Goal**: Build and deploy {project_name}
- **Total Duration**: 6 months
- **Team Size**: 5 developers
- **Budget**: $100,000

## Specifications


## Risk Assessment
- **Critical Path Analysis**: Critical path analysis pending
- **Key Risks**: Standard development risks
- **Mitigation Plans**: Standard mitigation strategies
- **Buffer Time**: 2 weeks

## Resource Planning
- **Development Resources**: 5 developers, 1 PM
- **Infrastructure Requirements**: AWS cloud infrastructure
- **External Dependencies**: None identified
- **Quality Assurance Plan**: Automated testing and manual QA

## Success Metrics
- **Technical Milestones**: Alpha, Beta, Production release
- **Business Milestones**: User adoption targets
- **Quality Gates**: Code review, testing, security review
- **Performance Targets**: Sub-2s response times

## Metadata
- **Status**: draft
- **Created**: 2024-01-01
- **Last Updated**: 2024-01-01
- **Spec Count**: 0
"""


class TestSharedStateIntegration:
    @pytest.fixture
    def loop_tools(self) -> LoopTools:
        return LoopTools(state_manager)

    @pytest.fixture
    def roadmap_tools(self) -> RoadmapTools:
        return RoadmapTools(state_manager)

    @pytest.fixture
    def sample_spec_markdown(self) -> str:
        return """# Technical Specification: Shared State Test

## Overview

**Objectives**: `Test shared state between tools`
**Scope**: `Integration testing of state management`
**Dependencies**: `In-memory state manager`

## Expected Deliverables

- Verified state consistency across tool sets
- Concurrent access validation
- State isolation verification

## Technical Architecture

Using shared InMemoryStateManager instance across LoopTools and RoadmapTools.
"""

    def test_tools_share_same_state_manager_instance(self, loop_tools: LoopTools, roadmap_tools: RoadmapTools) -> None:
        # Both should reference the same state manager from services.shared
        assert loop_tools.state is state_manager
        assert roadmap_tools.state is state_manager
        assert loop_tools.state is roadmap_tools.state

    def test_independent_operations_dont_interfere(
        self, loop_tools: LoopTools, roadmap_tools: RoadmapTools, sample_spec_markdown: str
    ) -> None:
        # Create loop state
        loop_result = loop_tools.initialize_refinement_loop('spec')
        assert loop_result.status == LoopStatus.INITIALIZED
        loop_id = loop_result.id

        # Create roadmap and spec
        roadmap_markdown = create_test_roadmap_markdown('Test Roadmap')
        roadmap_result = roadmap_tools.create_roadmap('test-project', roadmap_markdown)
        assert isinstance(roadmap_result, str)
        assert 'Created roadmap' in roadmap_result

        spec_result = roadmap_tools.add_spec('test-project', 'Test Spec', sample_spec_markdown)
        assert isinstance(spec_result, str)
        assert 'Added spec' in spec_result

        # Both domains should work independently
        loop_status = loop_tools.get_loop_status(loop_id)
        assert loop_status.status == LoopStatus.INITIALIZED

        roadmap_status = roadmap_tools.get_roadmap('test-project')
        assert isinstance(roadmap_status, str)
        assert '1 specs' in roadmap_status

    def test_state_manager_handles_concurrent_access(
        self, loop_tools: LoopTools, roadmap_tools: RoadmapTools, sample_spec_markdown: str
    ) -> None:
        project_id = 'concurrent-test'

        # Interleave operations between both tool sets

        # Step 1: Create roadmap
        roadmap_markdown = create_test_roadmap_markdown('Concurrent Test Roadmap')
        roadmap_tools.create_roadmap(project_id, roadmap_markdown)

        # Step 2: Initialize loop
        loop_result = loop_tools.initialize_refinement_loop('plan')
        loop_id = loop_result.id

        # Step 3: Add spec
        roadmap_tools.add_spec(project_id, 'Concurrent Spec', sample_spec_markdown)

        # Step 4: Progress loop
        loop_tools.decide_loop_next_action(loop_id, 70)  # Should REFINE

        # Step 5: List specs
        list_result = roadmap_tools.list_specs(project_id)

        # Step 6: Get loop status
        status_result = loop_tools.get_loop_status(loop_id)

        # All operations should succeed
        assert 'Shared State Test' in list_result  # Spec from markdown parsing
        assert status_result.status == LoopStatus.REFINE

    def test_state_manager_memory_limits_affect_only_loops(
        self, loop_tools: LoopTools, roadmap_tools: RoadmapTools, sample_spec_markdown: str
    ) -> None:
        # Create roadmap and specs (no limits here)
        roadmap_markdown = create_test_roadmap_markdown('Memory Test Roadmap')
        roadmap_tools.create_roadmap('memory-test', roadmap_markdown)

        # Add multiple specs
        for i in range(10):
            spec_markdown = sample_spec_markdown.replace('Shared State Test', f'Spec {i}')
            roadmap_tools.add_spec('memory-test', f'Spec {i}', spec_markdown)

        # Create many loops to trigger history management
        loop_ids = []
        for i in range(15):  # More than default max_history_size (10) from state_manager initialization
            result = loop_tools.initialize_refinement_loop('spec')
            loop_ids.append(result.id)

        # Older loops should be dropped due to history management
        with pytest.raises(LoopStateError):
            loop_tools.get_loop_status(loop_ids[0])  # First loop should be gone

        # But all specs should still exist
        list_result = roadmap_tools.list_specs('memory-test')
        assert isinstance(list_result, str)
        # Should contain all 10 specs
        for i in range(10):
            assert f'Spec {i}' in list_result

    def test_state_persistence_across_tool_instances(self, sample_spec_markdown: str) -> None:
        # Create initial tools and add data
        initial_roadmap_tools = RoadmapTools(state_manager)
        initial_loop_tools = LoopTools(state_manager)

        # Add data through initial instances
        roadmap_markdown = create_test_roadmap_markdown('Persistence Roadmap')
        initial_roadmap_tools.create_roadmap('persistence-test', roadmap_markdown)
        initial_roadmap_tools.add_spec('persistence-test', 'Persistence Spec', sample_spec_markdown)

        loop_result = initial_loop_tools.initialize_refinement_loop('build_plan')
        loop_id = loop_result.id

        # Create new tool instances
        new_roadmap_tools = RoadmapTools(state_manager)
        new_loop_tools = LoopTools(state_manager)

        # Data should be accessible through new instances
        roadmap_result = new_roadmap_tools.get_roadmap('persistence-test')
        assert isinstance(roadmap_result, str)
        assert 'Persistence Roadmap' in roadmap_result

        loop_status = new_loop_tools.get_loop_status(loop_id)
        assert loop_status.status == LoopStatus.INITIALIZED

    def test_cross_domain_error_isolation(self, loop_tools: LoopTools, roadmap_tools: RoadmapTools) -> None:
        # Create valid data in both domains
        roadmap_markdown = create_test_roadmap_markdown('Isolation Roadmap')
        roadmap_tools.create_roadmap('isolation-test', roadmap_markdown)
        loop_result = loop_tools.initialize_refinement_loop('analyst')
        loop_id = loop_result.id

        # Cause error in roadmap domain
        with pytest.raises(ResourceError):
            roadmap_tools.get_roadmap('non-existent-project')

        # Loop domain should still work
        loop_status = loop_tools.get_loop_status(loop_id)
        assert loop_status.status == LoopStatus.INITIALIZED

        # Cause error in loop domain
        with pytest.raises(LoopStateError):
            loop_tools.get_loop_status('non-existent-loop')

        # Roadmap domain should still work
        good_roadmap = roadmap_tools.get_roadmap('isolation-test')
        assert isinstance(good_roadmap, str)
        assert 'Isolation Roadmap' in good_roadmap

    def test_state_manager_initialization_affects_both_tools(self) -> None:
        # Create custom state manager with different config
        custom_state = InMemoryStateManager(max_history_size=1)  # Very small history

        custom_loop_tools = LoopTools(custom_state)
        custom_roadmap_tools = RoadmapTools(custom_state)

        # Create two loops - second should evict first
        loop1 = custom_loop_tools.initialize_refinement_loop('plan')
        loop2 = custom_loop_tools.initialize_refinement_loop('spec')

        # First loop should be gone
        with pytest.raises(LoopStateError):
            custom_loop_tools.get_loop_status(loop1.id)

        # Second loop should be there
        loop2_status = custom_loop_tools.get_loop_status(loop2.id)
        assert loop2_status.status == LoopStatus.INITIALIZED

        # But roadmap operations should be unaffected by loop history limits
        roadmap_markdown = create_test_roadmap_markdown('Custom Roadmap')
        custom_roadmap_tools.create_roadmap('custom-test', roadmap_markdown)
        result = custom_roadmap_tools.get_roadmap('custom-test')
        assert isinstance(result, str)
        assert 'Custom Roadmap' in result

    def test_mixed_workflow_realistic_scenario(
        self, loop_tools: LoopTools, roadmap_tools: RoadmapTools, sample_spec_markdown: str
    ) -> None:
        project_id = 'mixed-workflow'

        # 1. Create project roadmap
        roadmap_markdown = create_test_roadmap_markdown('Mixed Workflow Project')
        roadmap_tools.create_roadmap(project_id, roadmap_markdown)

        # 2. Initialize spec refinement loop
        loop_result = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_result.id

        # 3. Add initial spec draft
        roadmap_tools.add_spec(project_id, 'Initial Draft', sample_spec_markdown)

        # 4. Start refinement process
        refinement_1 = loop_tools.decide_loop_next_action(loop_id, 60)  # Low score, should refine
        assert refinement_1.status == LoopStatus.REFINE

        # 5. Update spec after first refinement
        updated_markdown = sample_spec_markdown.replace(
            'Test shared state between tools', 'Refined: Test shared state between tools with improvements'
        )
        roadmap_tools.update_spec(project_id, 'First Refinement', updated_markdown)

        # 6. Continue refinement
        refinement_2 = loop_tools.decide_loop_next_action(loop_id, 75)  # Better score, still refining
        assert refinement_2.status == LoopStatus.REFINE

        # 7. Final spec update
        final_markdown = updated_markdown.replace('Refined: Test shared state', 'Final: Test shared state')
        roadmap_tools.update_spec(project_id, 'Final Version', final_markdown)

        # 8. Complete refinement loop
        completion = loop_tools.decide_loop_next_action(loop_id, 90)  # High score, should complete
        assert completion.status == LoopStatus.COMPLETED

        # 9. Verify final state
        final_roadmap = roadmap_tools.get_roadmap(project_id)
        assert '1 specs' in final_roadmap  # Should have one spec (updated)

        final_loop_status = loop_tools.get_loop_status(loop_id)
        assert final_loop_status.status == LoopStatus.COMPLETED

    def test_state_manager_thread_safety_simulation(self, sample_spec_markdown: str) -> None:
        # Create custom state manager with small history limit for testing
        small_state = InMemoryStateManager(max_history_size=3)
        test_loop_tools = LoopTools(small_state)
        test_roadmap_tools = RoadmapTools(small_state)

        # This test simulates what would happen with concurrent access
        # by rapidly alternating between loop and roadmap operations

        results = []

        # Rapid alternating operations
        for i in range(5):
            # Loop operation
            loop_result = test_loop_tools.initialize_refinement_loop('spec')
            results.append(('loop', loop_result.status == LoopStatus.INITIALIZED))

            # Roadmap operation
            roadmap_markdown = create_test_roadmap_markdown(f'Roadmap {i}')
            roadmap_result = test_roadmap_tools.create_roadmap(f'concurrent-{i}', roadmap_markdown)
            results.append(('roadmap', isinstance(roadmap_result, str) and 'Created roadmap' in roadmap_result))

            # Mixed operation
            spec_result = test_roadmap_tools.add_spec(f'concurrent-{i}', f'Spec {i}', sample_spec_markdown)
            results.append(('spec', isinstance(spec_result, str) and 'Added spec' in spec_result))

            # Loop progress
            loop_progress = test_loop_tools.decide_loop_next_action(loop_result.id, 85)
            results.append(('progress', loop_progress.status == LoopStatus.COMPLETED))

        # All operations should have succeeded
        assert all(success for operation_type, success in results)

        # Verify final state consistency
        loop_count = len(test_loop_tools.list_active_loops())
        assert loop_count <= 3  # Limited by history size (3), but all should be completed anyway

        # All roadmaps should exist
        for i in range(5):
            roadmap_check = test_roadmap_tools.get_roadmap(f'concurrent-{i}')
            assert isinstance(roadmap_check, str)
            assert f'Roadmap {i}' in roadmap_check
