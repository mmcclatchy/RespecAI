import pytest

from services.models.enums import RoadmapStatus
from services.models.roadmap import Roadmap


class TestRoadmapParsing:
    def test_parse_markdown_extracts_all_fields(self) -> None:
        markdown = """# Project Roadmap: E-Commerce Platform Development

## Roadmap Overview

**Project Goal**: `Build a comprehensive e-commerce platform with modern features`
**Total Duration**: `12 months`
**Team Size**: `8 developers`
**Budget**: `$500,000`

## Phase Breakdown

### Phase 1: Foundation Setup
**Duration**: `3 months`
**Objectives**: `Set up development infrastructure and core architecture`
**Deliverables**: `Development environment, database schema, basic API structure`
**Success Criteria**: `All environments deployed, core APIs functional, team onboarded`
**Dependencies**: `Cloud infrastructure approval, team hiring complete`
**Team**: `2 backend developers, 1 DevOps engineer, 1 architect`
**Technical Focus**: `Infrastructure as code, CI/CD pipeline, database design`

### Phase 2: Core Features Development
**Duration**: `6 months`
**Objectives**: `Implement user authentication, product catalog, and shopping cart`
**Deliverables**: `User management system, product browsing, cart functionality`
**Success Criteria**: `Users can register, browse products, add to cart, basic checkout`
**Dependencies**: `Phase 1 completion, payment gateway integration approved`
**Team**: `4 full-stack developers, 1 UI/UX designer, 1 QA engineer`
**Technical Focus**: `Frontend development, API implementation, database optimization`

### Phase 3: Advanced Features and Launch
**Duration**: `3 months`
**Objectives**: `Add payment processing, order management, and admin dashboard`
**Deliverables**: `Complete e-commerce platform ready for production launch`
**Success Criteria**: `Full transaction flow working, admin tools functional, performance targets met`
**Dependencies**: `Phase 2 completion, security audit passed, load testing complete`
**Team**: `Full team for integration, additional security specialist`
**Technical Focus**: `Payment integration, security hardening, performance optimization`

## Risk Assessment

### Critical Path Analysis
`Phase 1 infrastructure setup is critical - delays here impact entire timeline`

### Key Risks
`Payment gateway integration complexity, team scaling challenges, security compliance`

### Mitigation Plans
`Early payment gateway prototyping, phased team onboarding, security review at each phase`

### Buffer Time
`2 weeks buffer built into each phase, 1 month final buffer before launch`

## Resource Planning

### Development Resources
`8 developers (mix of senior/junior), 1 architect, 1 DevOps, 1 designer, 2 QA`

### Infrastructure Requirements
`AWS cloud setup, staging and production environments, CI/CD tools, monitoring`

### External Dependencies
`Payment gateway partnership, SSL certificates, compliance audits, load testing tools`

### Quality Assurance
`Unit testing (90% coverage), integration testing, security testing, performance testing`

## Success Metrics

### Technical Milestones
`Infrastructure ready (Month 3), Core features complete (Month 9), Launch ready (Month 12)`

### Business Milestones
`MVP demo (Month 6), Beta testing (Month 10), Public launch (Month 12), 1000 users (Month 13)`

### Quality Gates
`Code review approval, security scan pass, performance benchmarks met, accessibility compliance`

### Performance Targets
`Page load <2s, 99.9% uptime, support 10,000 concurrent users, mobile responsive`

---

**Status**: `in-progress`
**Created**: `2024-01-01`
**Last Updated**: `2024-02-15`
**Phase Count**: `3`"""

        roadmap = Roadmap.parse_markdown(markdown)

        assert roadmap.project_name == 'E-Commerce Platform Development'
        assert roadmap.project_goal == 'Build a comprehensive e-commerce platform with modern features'
        assert roadmap.total_duration == '12 months'
        assert roadmap.team_size == '8 developers'
        assert roadmap.roadmap_budget == '$500,000'

        # Phase 1
        assert roadmap.phase_1_name == 'Foundation Setup'
        assert roadmap.phase_1_duration == '3 months'
        assert 'Set up development infrastructure' in roadmap.phase_1_objectives
        assert 'Development environment, database schema' in roadmap.phase_1_deliverables
        assert 'All environments deployed' in roadmap.phase_1_success_criteria
        assert 'Cloud infrastructure approval' in roadmap.phase_1_dependencies
        assert '2 backend developers' in roadmap.phase_1_team
        assert 'Infrastructure as code' in roadmap.phase_1_technical_focus

        # Phase 2
        assert roadmap.phase_2_name == 'Core Features Development'
        assert roadmap.phase_2_duration == '6 months'
        assert 'user authentication, product catalog' in roadmap.phase_2_objectives

        # Phase 3
        assert roadmap.phase_3_name == 'Advanced Features and Launch'
        assert roadmap.phase_3_duration == '3 months'
        assert 'payment processing, order management' in roadmap.phase_3_objectives

        # Risk assessment
        assert 'Phase 1 infrastructure setup is critical' in roadmap.critical_path_analysis
        assert 'Payment gateway integration complexity' in roadmap.key_risks
        assert 'Early payment gateway prototyping' in roadmap.mitigation_plans
        assert '2 weeks buffer built into each phase' in roadmap.buffer_time

        # Resource planning
        assert '8 developers (mix of senior/junior)' in roadmap.development_resources
        assert 'AWS cloud setup' in roadmap.infrastructure_requirements
        assert 'Payment gateway partnership' in roadmap.external_dependencies
        assert 'Unit testing (90% coverage)' in roadmap.quality_assurance_plan

        # Success metrics
        assert 'Infrastructure ready (Month 3)' in roadmap.technical_milestones
        assert 'MVP demo (Month 6)' in roadmap.business_milestones
        assert 'Code review approval' in roadmap.quality_gates
        assert 'Page load <2s' in roadmap.performance_targets

        # Metadata
        assert roadmap.roadmap_status == RoadmapStatus.IN_PROGRESS
        assert roadmap.creation_date == '2024-01-01'
        assert roadmap.last_updated == '2024-02-15'
        assert roadmap.phase_count == '3'

    def test_parse_markdown_handles_missing_sections(self) -> None:
        markdown = """# Project Roadmap: Simple Project

## Roadmap Overview

**Project Goal**: `Build a simple app`
**Total Duration**: `6 months`
**Team Size**: `3 developers`
**Budget**: `$100,000`

## Phase Breakdown

### Phase 1: Setup
**Duration**: `2 months`
**Objectives**: `Initial setup`
**Deliverables**: `Basic framework`
**Success Criteria**: `Framework running`
**Dependencies**: `None`
**Team**: `2 developers`
**Technical Focus**: `Basic setup`

---

**Status**: `draft`
**Created**: `2024-01-01`
**Last Updated**: `2024-01-01`
**Phase Count**: `1`"""

        roadmap = Roadmap.parse_markdown(markdown)

        assert roadmap.project_name == 'Simple Project'
        assert roadmap.phase_1_name == 'Setup'
        # Missing phase 2 and 3 should have default values
        assert 'Phase 2 Name not specified' in roadmap.phase_2_name
        assert 'Phase 3 Name not specified' in roadmap.phase_3_name
        # Missing risk assessment sections should have defaults
        assert 'Critical Path Analysis not specified' in roadmap.critical_path_analysis

    def test_parse_markdown_invalid_format_raises_error(self) -> None:
        invalid_markdown = """This is not a roadmap format"""

        with pytest.raises(ValueError, match='Invalid roadmap format: missing title'):
            Roadmap.parse_markdown(invalid_markdown)


class TestRoadmapMarkdownBuilding:
    @pytest.fixture
    def sample_roadmap(self) -> Roadmap:
        return Roadmap(
            project_name='Mobile App Development',
            project_goal='Create a cross-platform mobile application',
            total_duration='9 months',
            team_size='5 developers',
            roadmap_budget='$300,000',
            phase_1_name='Planning and Design',
            phase_1_duration='2 months',
            phase_1_objectives='Create detailed designs and technical architecture',
            phase_1_deliverables='UI/UX designs, technical specifications, project plan',
            phase_1_success_criteria='All designs approved, architecture documented',
            phase_1_dependencies='Stakeholder approval, designer availability',
            phase_1_team='1 designer, 1 architect, 1 project manager',
            phase_1_technical_focus='Design systems, architecture planning',
            phase_2_name='Core Development',
            phase_2_duration='5 months',
            phase_2_objectives='Implement core features and functionality',
            phase_2_deliverables='Working mobile application with core features',
            phase_2_success_criteria='All core features implemented and tested',
            phase_2_dependencies='Phase 1 completion, development team ready',
            phase_2_team='3 mobile developers, 1 backend developer',
            phase_2_technical_focus='React Native development, API integration',
            phase_3_name='Testing and Launch',
            phase_3_duration='2 months',
            phase_3_objectives='Complete testing and deploy to app stores',
            phase_3_deliverables='Published app in iOS and Android stores',
            phase_3_success_criteria='App approved by stores, initial user feedback positive',
            phase_3_dependencies='Phase 2 completion, store approval process',
            phase_3_team='Full team for final testing and deployment',
            phase_3_technical_focus='Testing, deployment, app store optimization',
            critical_path_analysis='Design approval is critical for timeline',
            key_risks='App store approval delays, platform compatibility issues',
            mitigation_plans='Early submission to stores, extensive device testing',
            buffer_time='1 week buffer per phase',
            development_resources='5 developers, 1 designer, 1 PM, testing devices',
            infrastructure_requirements='Development servers, CI/CD, app store accounts',
            external_dependencies='App store partnerships, third-party SDKs',
            quality_assurance_plan='Automated testing, manual testing, beta testing',
            technical_milestones='Designs complete, MVP ready, app submitted',
            business_milestones='Design approval, beta launch, store launch',
            quality_gates='Code review, security scan, performance testing',
            performance_targets='App launch <3s, 60fps animations, offline capability',
            roadmap_status=RoadmapStatus.APPROVED,
            creation_date='2024-01-05',
            last_updated='2024-01-20',
            phase_count='3',
        )

    def test_build_markdown_creates_valid_template_format(self, sample_roadmap: Roadmap) -> None:
        markdown = sample_roadmap.build_markdown()

        assert '# Project Roadmap: Mobile App Development' in markdown
        assert '**Project Goal**: `Create a cross-platform mobile application`' in markdown
        assert '### Phase 1: Planning and Design' in markdown
        assert '**Duration**: `2 months`' in markdown
        assert '### Phase 2: Core Development' in markdown
        assert '### Phase 3: Testing and Launch' in markdown
        assert '### Critical Path Analysis' in markdown
        assert '`Design approval is critical for timeline`' in markdown
        assert '**Status**: `approved`' in markdown
        assert '**Phase Count**: `3`' in markdown

    def test_round_trip_parsing_maintains_data_integrity(self, sample_roadmap: Roadmap) -> None:
        # Build markdown from the model
        markdown = sample_roadmap.build_markdown()

        # Parse it back into a model
        parsed_roadmap = Roadmap.parse_markdown(markdown)

        # Should match original (except timestamps)
        assert parsed_roadmap.project_name == sample_roadmap.project_name
        assert parsed_roadmap.project_goal == sample_roadmap.project_goal
        assert parsed_roadmap.total_duration == sample_roadmap.total_duration
        assert parsed_roadmap.team_size == sample_roadmap.team_size
        assert parsed_roadmap.roadmap_budget == sample_roadmap.roadmap_budget

        # Phase 1
        assert parsed_roadmap.phase_1_name == sample_roadmap.phase_1_name
        assert parsed_roadmap.phase_1_duration == sample_roadmap.phase_1_duration
        assert parsed_roadmap.phase_1_objectives == sample_roadmap.phase_1_objectives
        assert parsed_roadmap.phase_1_deliverables == sample_roadmap.phase_1_deliverables
        assert parsed_roadmap.phase_1_success_criteria == sample_roadmap.phase_1_success_criteria
        assert parsed_roadmap.phase_1_dependencies == sample_roadmap.phase_1_dependencies
        assert parsed_roadmap.phase_1_team == sample_roadmap.phase_1_team
        assert parsed_roadmap.phase_1_technical_focus == sample_roadmap.phase_1_technical_focus

        # Phase 2
        assert parsed_roadmap.phase_2_name == sample_roadmap.phase_2_name
        assert parsed_roadmap.phase_2_duration == sample_roadmap.phase_2_duration
        assert parsed_roadmap.phase_2_objectives == sample_roadmap.phase_2_objectives
        assert parsed_roadmap.phase_2_deliverables == sample_roadmap.phase_2_deliverables
        assert parsed_roadmap.phase_2_success_criteria == sample_roadmap.phase_2_success_criteria
        assert parsed_roadmap.phase_2_dependencies == sample_roadmap.phase_2_dependencies
        assert parsed_roadmap.phase_2_team == sample_roadmap.phase_2_team
        assert parsed_roadmap.phase_2_technical_focus == sample_roadmap.phase_2_technical_focus

        # Phase 3
        assert parsed_roadmap.phase_3_name == sample_roadmap.phase_3_name
        assert parsed_roadmap.phase_3_duration == sample_roadmap.phase_3_duration
        assert parsed_roadmap.phase_3_objectives == sample_roadmap.phase_3_objectives
        assert parsed_roadmap.phase_3_deliverables == sample_roadmap.phase_3_deliverables
        assert parsed_roadmap.phase_3_success_criteria == sample_roadmap.phase_3_success_criteria
        assert parsed_roadmap.phase_3_dependencies == sample_roadmap.phase_3_dependencies
        assert parsed_roadmap.phase_3_team == sample_roadmap.phase_3_team
        assert parsed_roadmap.phase_3_technical_focus == sample_roadmap.phase_3_technical_focus

        # Risk assessment
        assert parsed_roadmap.critical_path_analysis == sample_roadmap.critical_path_analysis
        assert parsed_roadmap.key_risks == sample_roadmap.key_risks
        assert parsed_roadmap.mitigation_plans == sample_roadmap.mitigation_plans
        assert parsed_roadmap.buffer_time == sample_roadmap.buffer_time

        # Resource planning
        assert parsed_roadmap.development_resources == sample_roadmap.development_resources
        assert parsed_roadmap.infrastructure_requirements == sample_roadmap.infrastructure_requirements
        assert parsed_roadmap.external_dependencies == sample_roadmap.external_dependencies
        assert parsed_roadmap.quality_assurance_plan == sample_roadmap.quality_assurance_plan

        # Success metrics
        assert parsed_roadmap.technical_milestones == sample_roadmap.technical_milestones
        assert parsed_roadmap.business_milestones == sample_roadmap.business_milestones
        assert parsed_roadmap.quality_gates == sample_roadmap.quality_gates
        assert parsed_roadmap.performance_targets == sample_roadmap.performance_targets

        # Metadata
        assert parsed_roadmap.roadmap_status == sample_roadmap.roadmap_status
        assert parsed_roadmap.creation_date == sample_roadmap.creation_date
        assert parsed_roadmap.last_updated == sample_roadmap.last_updated
        assert parsed_roadmap.phase_count == sample_roadmap.phase_count

    def test_character_for_character_round_trip_validation(self, sample_roadmap: Roadmap) -> None:
        # Build markdown
        original_markdown = sample_roadmap.build_markdown()

        # Parse and rebuild
        parsed_roadmap = Roadmap.parse_markdown(original_markdown)
        rebuilt_markdown = parsed_roadmap.build_markdown()

        # Should be identical
        assert original_markdown == rebuilt_markdown
