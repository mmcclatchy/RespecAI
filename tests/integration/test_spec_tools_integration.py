from services.mcp.tools.spec_tools import SpecTools
from services.mcp.tools.loop_tools import LoopTools
from services.models.spec import TechnicalSpec
from services.models.enums import SpecStatus
from services.utils.enums import LoopStatus
from services.utils.state_manager import InMemoryStateManager


class TestSpecToolsIntegration:
    def test_store_technical_spec_end_to_end(self) -> None:
        state_manager = InMemoryStateManager()
        spec_tools = SpecTools(state_manager)
        loop_tools = LoopTools(state_manager)

        loop_response = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_response.id

        technical_spec = TechnicalSpec(
            phase_name='AI-Powered Analytics Platform',
            objectives='Build real-time analytics system',
            scope='Customer behavior analysis and prediction',
            dependencies='External data APIs, ML model infrastructure',
            deliverables='Analytics dashboard, ML pipeline, API endpoints',
            architecture='Microservices with event-driven processing',
            technology_stack='Python, FastAPI, PostgreSQL, Redis, React',
            functional_requirements='Real-time data processing, visualization',
            non_functional_requirements='99.9% uptime, <100ms response time',
            development_plan='4-phase implementation over 6 months',
            testing_strategy='Unit, integration, and load testing',
            research_requirements='ML deployment patterns, streaming architecture',
            success_criteria='Performance targets met, user adoption >80%',
            integration_context='Integrate with existing CRM and billing',
            spec_status=SpecStatus.DRAFT,
        )

        result = spec_tools.store_technical_spec(technical_spec, loop_id)

        assert result.id == loop_id
        assert result.status in [LoopStatus.INITIALIZED, LoopStatus.IN_PROGRESS]
        assert 'AI-Powered Analytics Platform' in result.message

        stored_spec = spec_tools.get_technical_spec_data(loop_id)
        assert stored_spec.phase_name == 'AI-Powered Analytics Platform'
        assert stored_spec.objectives == 'Build real-time analytics system'

    def test_get_technical_spec_markdown_integration(self) -> None:
        state_manager = InMemoryStateManager()
        spec_tools = SpecTools(state_manager)
        loop_tools = LoopTools(state_manager)

        loop_response = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_response.id

        technical_spec = TechnicalSpec(
            phase_name='Data Processing Pipeline',
            objectives='Process customer feedback data efficiently',
            scope='ETL pipeline for feedback analysis',
            architecture='Lambda architecture with batch and stream processing',
            technology_stack='Apache Kafka, Apache Spark, PostgreSQL',
        )

        spec_tools.store_technical_spec(technical_spec, loop_id)
        result = spec_tools.get_technical_spec_markdown(loop_id)

        assert result.id == loop_id
        assert 'Data Processing Pipeline' in result.message
        assert 'Process customer feedback data efficiently' in result.message
        assert '## System Design' in result.message
        assert '### Architecture' in result.message

    def test_list_technical_specs_integration(self) -> None:
        state_manager = InMemoryStateManager()
        spec_tools = SpecTools(state_manager)
        loop_tools = LoopTools(state_manager)

        specs_data = [
            ('Recommendation Engine', 'Machine learning recommendation system'),
            ('User Authentication', 'OAuth2 authentication service'),
            ('Payment Processing', 'Secure payment gateway integration'),
        ]

        for phase_name, objectives in specs_data:
            loop_response = loop_tools.initialize_refinement_loop('spec')
            loop_id = loop_response.id

            technical_spec = TechnicalSpec(
                phase_name=phase_name,
                objectives=objectives,
            )
            spec_tools.store_technical_spec(technical_spec, loop_id)

        result = spec_tools.list_technical_specs(2)
        assert 'Found 2 technical spec' in result.message
        assert 'Payment Processing' in result.message
        assert 'User Authentication' in result.message

    def test_delete_technical_spec_integration(self) -> None:
        state_manager = InMemoryStateManager()
        spec_tools = SpecTools(state_manager)
        loop_tools = LoopTools(state_manager)

        loop_response = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_response.id

        technical_spec = TechnicalSpec(
            phase_name='Cache Management System',
            objectives='Distributed caching solution',
        )

        spec_tools.store_technical_spec(technical_spec, loop_id)
        result = spec_tools.delete_technical_spec(loop_id)

        assert result.id == loop_id
        assert 'Cache Management System' in result.message

    def test_technical_spec_not_found_error(self) -> None:
        state_manager = InMemoryStateManager()
        spec_tools = SpecTools(state_manager)
        loop_tools = LoopTools(state_manager)

        loop_response = loop_tools.initialize_refinement_loop('spec')
        loop_id = loop_response.id

        try:
            spec_tools.get_technical_spec_data(loop_id)
            assert False, 'Should have raised ResourceError'
        except Exception as e:
            assert 'No technical specification stored' in str(e)

    def test_loop_not_found_error(self) -> None:
        state_manager = InMemoryStateManager()
        spec_tools = SpecTools(state_manager)

        technical_spec = TechnicalSpec(
            phase_name='Invalid Loop Test',
            objectives='Test error handling',
        )

        try:
            spec_tools.store_technical_spec(technical_spec, 'invalid-loop-id')
            assert False, 'Should have raised ResourceError'
        except Exception as e:
            assert 'Loop does not exist' in str(e)
