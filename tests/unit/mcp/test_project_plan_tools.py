import pytest

from services.mcp.project_plan_tools import ProjectPlanTools
from services.models.enums import ProjectStatus
from services.models.project_plan import ProjectPlan
from services.utils.enums import LoopStatus, LoopType
from services.utils.errors import LoopStateError
from services.utils.models import LoopState, MCPResponse
from services.utils.state_manager import InMemoryStateManager


@pytest.fixture
def state_manager() -> InMemoryStateManager:
    return InMemoryStateManager(max_history_size=3)


@pytest.fixture
def project_plan_tools(state_manager: InMemoryStateManager) -> ProjectPlanTools:
    return ProjectPlanTools(state_manager)


def create_project_plan(name: str = 'AI-Powered Customer Support System') -> ProjectPlan:
    return ProjectPlan(
        project_name=name,
        project_vision=f'Transform {name.lower()} with automation',
        project_mission=f'Deliver instant, accurate {name.lower()}',
        project_timeline='Q2 2024 completion',
        project_budget='$500K development budget',
        primary_objectives='Reduce response time by 60%, improve satisfaction by 40%',
        success_metrics='Response time < 2 hours, CSAT > 90%',
        key_performance_indicators='Average response time, CSAT score, automation rate',
        included_features='AI chatbot, ticket routing, knowledge base',
        excluded_features='Video chat, phone support, multilingual',
        project_assumptions='Support volume remains stable',
        project_constraints='Budget, timeline, team size limitations',
        project_sponsor='VP of Customer Success',
        key_stakeholders='Support team, Engineering, Product',
        end_users='Customer support agents, customers',
        work_breakdown='Phase 1: Core AI, Phase 2: Integration, Phase 3: Optimization',
        phases_overview='3 phases over 6 months',
        project_dependencies='AI service, existing CRM system',
        team_structure='3 engineers, 1 designer, 1 PM',
        technology_requirements='Python, FastAPI, OpenAI API',
        infrastructure_needs='Cloud hosting, database, monitoring',
        identified_risks='Technical complexity, timeline pressure',
        mitigation_strategies='Prototype early, weekly reviews',
        contingency_plans='Reduce scope if needed',
        quality_standards='95% test coverage, code reviews',
        testing_strategy='Unit, integration, user acceptance testing',
        acceptance_criteria='All features working, performance targets met',
        reporting_structure='Weekly team updates, monthly stakeholder reports',
        meeting_schedule='Daily standups, weekly planning',
        documentation_standards='API docs, user guides, technical specs',
        project_status=ProjectStatus.DRAFT,
        creation_date='2024-01-01',
        last_updated='2024-01-01',
        version='1.0',
    )


@pytest.fixture
def sample_project_plan() -> ProjectPlan:
    return create_project_plan()


class TestProjectPlanTools:
    pass


class TestStoreProjectPlan:
    def test_store_project_plan_creates_new_loop_state(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        response = project_plan_tools.store_project_plan(sample_project_plan)

        assert isinstance(response, MCPResponse)
        assert response.status == LoopStatus.INITIALIZED
        assert 'Stored project plan' in response.message

        # Verify loop state was created
        loop_state = project_plan_tools.state.get_loop(response.id)
        assert loop_state is not None
        assert loop_state.loop_type.value == 'plan'
        assert loop_state.status == LoopStatus.INITIALIZED

    def test_store_project_plan_updates_existing_loop_state(
        self,
        project_plan_tools: ProjectPlanTools,
        state_manager: InMemoryStateManager,
        sample_project_plan: ProjectPlan,
    ) -> None:
        # Create existing loop
        existing_loop = LoopState(loop_type=LoopType.PLAN)
        state_manager.add_loop(existing_loop)

        response = project_plan_tools.store_project_plan(sample_project_plan, existing_loop.id)

        assert response.id == existing_loop.id
        assert response.status == LoopStatus.INITIALIZED
        assert 'Updated project plan' in response.message

    def test_store_project_plan_stores_structured_data(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        response = project_plan_tools.store_project_plan(sample_project_plan)

        # Verify structured data is stored (not just markdown)
        stored_plan = project_plan_tools.get_project_plan_data(response.id)
        assert stored_plan.project_name == sample_project_plan.project_name
        assert stored_plan.project_vision == sample_project_plan.project_vision
        assert stored_plan.primary_objectives == sample_project_plan.primary_objectives

    def test_store_project_plan_validates_project_plan_model(self, project_plan_tools: ProjectPlanTools) -> None:
        # Test validation will be handled by the tool implementation
        # This test expects the tool to catch and translate ValidationError
        # We'll use a mock or invalid data that causes validation to fail

        # Test validation will be handled by the tool implementation
        # This test expects the tool to catch and translate ValidationError
        with pytest.raises(LoopStateError):
            project_plan_tools.store_project_plan(None)  # type: ignore[arg-type]  # Intentionally testing None


class TestGetProjectPlan:
    def test_get_project_plan_returns_structured_data(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        # Store plan first
        response = project_plan_tools.store_project_plan(sample_project_plan)

        # Retrieve plan
        retrieved_plan = project_plan_tools.get_project_plan_data(response.id)

        assert isinstance(retrieved_plan, ProjectPlan)
        assert retrieved_plan.project_name == sample_project_plan.project_name
        assert retrieved_plan.project_vision == sample_project_plan.project_vision
        assert retrieved_plan.primary_objectives == sample_project_plan.primary_objectives

    def test_get_project_plan_raises_error_when_loop_not_found(self, project_plan_tools: ProjectPlanTools) -> None:
        with pytest.raises(LoopStateError) as exc_info:
            project_plan_tools.get_project_plan_data('non-existent-loop')

        assert 'non-existent-loop' in str(exc_info.value)
        assert 'project_plan_retrieval' in str(exc_info.value)

    def test_get_project_plan_raises_error_when_no_plan_stored(
        self, project_plan_tools: ProjectPlanTools, state_manager: InMemoryStateManager
    ) -> None:
        # Create loop without storing plan
        loop_state = LoopState(loop_type=LoopType.PLAN)
        state_manager.add_loop(loop_state)

        with pytest.raises(LoopStateError) as exc_info:
            project_plan_tools.get_project_plan_data(loop_state.id)

        assert 'No project plan stored' in str(exc_info.value)


class TestGetProjectPlanMarkdown:
    def test_get_project_plan_markdown_generates_platform_output(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        # Store plan first
        response = project_plan_tools.store_project_plan(sample_project_plan)

        # Generate markdown
        markdown_response = project_plan_tools.get_project_plan_markdown(response.id)

        assert isinstance(markdown_response, MCPResponse)
        assert markdown_response.id == response.id
        assert markdown_response.status == LoopStatus.INITIALIZED
        assert '# Project Plan:' in markdown_response.message
        assert sample_project_plan.project_name in markdown_response.message
        assert sample_project_plan.project_vision in markdown_response.message

    def test_get_project_plan_markdown_works_with_all_platforms(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        # Store plan first
        response = project_plan_tools.store_project_plan(sample_project_plan)

        # Test platform-specific markdown generation
        platforms = ['linear', 'github', 'local']

        for platform in platforms:
            markdown_response = project_plan_tools.get_project_plan_markdown(response.id, platform)
            assert isinstance(markdown_response, MCPResponse)
            assert sample_project_plan.project_name in markdown_response.message

    def test_get_project_plan_markdown_raises_error_when_loop_not_found(
        self, project_plan_tools: ProjectPlanTools
    ) -> None:
        with pytest.raises(LoopStateError) as exc_info:
            project_plan_tools.get_project_plan_markdown('non-existent-loop')

        assert 'non-existent-loop' in str(exc_info.value)
        assert 'project_plan_markdown_generation' in str(exc_info.value)


class TestListProjectPlans:
    def test_list_project_plans_returns_empty_for_no_plans(self, project_plan_tools: ProjectPlanTools) -> None:
        response = project_plan_tools.list_project_plans()

        assert isinstance(response, MCPResponse)
        assert response.status == LoopStatus.INITIALIZED
        assert 'No project plans found' in response.message

    def test_list_project_plans_returns_multiple_plans(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        # Store multiple plans
        plan1_response = project_plan_tools.store_project_plan(sample_project_plan)

        plan2 = ProjectPlan(
            project_name='E-commerce Analytics Platform',
            project_vision='Data-driven sales optimization',
            project_mission='Increase conversion through analytics',
            project_timeline='Q3 2024',
            project_budget='$300K',
            primary_objectives='Increase conversion by 25%',
            success_metrics='Conversion rate > 3%',
            key_performance_indicators='Conversion rate, revenue per visit',
            included_features='Dashboard, reports, API',
            excluded_features='Real-time alerts',
            project_assumptions='Historical data available',
            project_constraints='Budget and timeline',
            project_sponsor='VP Sales',
            key_stakeholders='Sales, Marketing',
            end_users='Sales team, analysts',
            work_breakdown='Phase 1: Data, Phase 2: Analytics',
            phases_overview='2 phases over 4 months',
            project_dependencies='Existing CRM data',
            team_structure='2 engineers, 1 analyst',
            technology_requirements='Python, SQL, Tableau',
            infrastructure_needs='Data warehouse, BI tools',
            identified_risks='Data quality issues',
            mitigation_strategies='Data validation processes',
            contingency_plans='Manual reporting fallback',
            quality_standards='Data accuracy > 95%',
            testing_strategy='Unit tests, data validation',
            acceptance_criteria='All KPIs tracked accurately',
            reporting_structure='Weekly reports to VP Sales',
            meeting_schedule='Bi-weekly status updates',
            documentation_standards='Data dictionary, user guides',
            project_status=ProjectStatus.DRAFT,
            creation_date='2024-01-15',
            last_updated='2024-01-15',
            version='1.0',
        )
        plan2_response = project_plan_tools.store_project_plan(plan2)

        # List all plans
        response = project_plan_tools.list_project_plans()

        assert 'Found 2 project plans:' in response.message
        assert sample_project_plan.project_name in response.message
        assert plan2.project_name in response.message
        assert plan1_response.id in response.message
        assert plan2_response.id in response.message

    def test_list_project_plans_respects_count_limit(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        # Store 3 plans
        for i in range(3):
            plan = create_project_plan(f'Project {i + 1}')
            project_plan_tools.store_project_plan(plan)

        # List with limit
        response = project_plan_tools.list_project_plans(count=2)

        assert 'Found 2 project plans:' in response.message
        assert 'Project 2' in response.message
        assert 'Project 3' in response.message
        assert 'Project 1' not in response.message


class TestDeleteProjectPlan:
    def test_delete_project_plan_removes_plan_and_loop(
        self, project_plan_tools: ProjectPlanTools, sample_project_plan: ProjectPlan
    ) -> None:
        # Store plan first
        response = project_plan_tools.store_project_plan(sample_project_plan)

        # Delete plan
        delete_response = project_plan_tools.delete_project_plan(response.id)

        assert isinstance(delete_response, MCPResponse)
        assert delete_response.id == response.id
        assert 'Deleted project plan' in delete_response.message

        # Verify plan and loop are removed
        with pytest.raises(LoopStateError):
            project_plan_tools.get_project_plan_data(response.id)

    def test_delete_project_plan_raises_error_when_loop_not_found(self, project_plan_tools: ProjectPlanTools) -> None:
        with pytest.raises(LoopStateError) as exc_info:
            project_plan_tools.delete_project_plan('non-existent-loop')

        assert 'non-existent-loop' in str(exc_info.value)
        assert 'project_plan_deletion' in str(exc_info.value)
