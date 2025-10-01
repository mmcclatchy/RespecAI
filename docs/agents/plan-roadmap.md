# roadmap Agent Specification

## Overview
The `roadmap` agent transforms strategic plans and business objectives into phased implementation roadmaps. It analyzes requirements to create discrete, implementable phases that each deliver user value.

## Agent Metadata

**Name**: `roadmap`  
**Type**: Implementation planning specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/specter-roadmap` command  
**Phase**: Implementation Roadmap Generation

## Invocation Context

### When Invoked
- **Initial**: Start of `/specter-roadmap` command with strategic plan
- **Refinement**: When roadmap-critic feedback requires phase restructuring
- **User Guidance**: With specific phasing preferences provided

### Invocation Pattern
```text
# Main Agent invokes roadmap
Task(
    agent="roadmap",
    prompt=f"""
    Strategic Plan: {strategic_plan}
    Structured Objectives: {objectives_analysis}
    {critic_feedback if refining else ""}
    
    Create implementation roadmap with discrete phases.
    Each phase should be implementable in 2-4 weeks.
    """
)
```

## Workflow Position

```text
Strategic Plan → roadmap → Implementation Roadmap → roadmap-critic
                      ↓                                          ↓
              Phase Breakdown                          Quality Assessment
                      ↓                                          ↓
              Dependency Mapping                      Refinement Decision
```

### Role in Roadmap Creation
1. **Requirements Analysis**: Parse strategic plan for implementable units
2. **Phase Design**: Create logical implementation phases
3. **Dependency Mapping**: Establish phase relationships
4. **Context Preparation**: Provide spec-ready information per phase

## Primary Responsibilities

### Core Tasks

1. **Strategic Plan Analysis**
   - Parse complete strategic plan document
   - Extract functional requirements and features
   - Identify technical constraints and dependencies
   - Understand business priorities and timeline
   - Recognize critical success factors

2. **Phase Decomposition**
   - Break requirements into 3-7 implementation phases
   - Ensure each phase delivers user value
   - Size phases for 2-4 week implementation cycles
   - Balance complexity across phases
   - Front-load critical infrastructure

3. **Dependency Management**
   - Identify technical dependencies between features
   - Establish clear phase sequencing
   - Document integration requirements
   - Map data flow between phases
   - Highlight blocking dependencies

4. **Scope Definition**
   - Define clear boundaries for each phase
   - Specify included features and capabilities
   - Document explicitly excluded items
   - Identify phase-specific constraints
   - Establish success criteria per phase

5. **Spec Context Generation**
   - Provide technical focus areas for each phase
   - Identify architecture decisions needed
   - Document research requirements
   - Suggest technology choices
   - Prepare integration considerations

## Tool Permissions

### Allowed Tools
- **Read**: Access strategic plan documents and requirements files
- **Grep**: Search for specific patterns within strategic plans
- **Glob**: Find related documentation and context files

### Restrictions
- No file writing capabilities (roadmap returned to Main Agent)
- No external network access
- No MCP Server communication
- No direct user interaction

## Input Specifications

### Initial Invocation Input
```markdown
Strategic Plan:
[Complete strategic plan document from /specter-plan command]

Structured Objectives:
[Business objectives analysis from plan-analyst]

Phasing Preferences (optional):
[User guidance like "2-week sprints" or "MVP in 3 months"]

Create implementation roadmap with discrete phases.
Each phase should be implementable in 2-4 weeks.
```

### Refinement Invocation Input
```markdown
Previous Roadmap:
[Current implementation roadmap]

Critic Feedback:
- Score: [X]%
- Issues: [list of problems]
- Suggestions: [improvements]

Enhance the roadmap addressing the feedback.
Focus on: [specific areas needing improvement]
```

## Output Specifications

### Implementation Roadmap Structure
```markdown
# Implementation Roadmap: [Project Name]

## Overview
[Phasing strategy and implementation approach]

## Phase Summary
- Total Phases: [3-7 phases]
- Estimated Duration: [total timeline]
- Critical Path: [key dependencies]

## Phase 1: [Foundation/Core Infrastructure]
**Duration**: 2-3 weeks
**Priority**: Critical
**Dependencies**: None

### Scope
[Clear description of included functionality]

### Deliverables
- [Specific, measurable deliverable]
- [Specific, measurable deliverable]
- [Specific, measurable deliverable]

### Technical Focus
- [Key technical area, e.g., "Authentication system"]
- [Key technical area, e.g., "Database schema"]
- [Key technical area, e.g., "API framework"]

### Success Criteria
- [Measurable outcome, e.g., "Users can register and login"]
- [Measurable outcome, e.g., "Core data models implemented"]

### Spec Context
**Focus Areas**: [Technical domains for /specter-spec command]
**Key Decisions**: [Architecture choices needed]
**Research Needs**: [Technologies to investigate]
**Integration Points**: [External systems or APIs]

## Phase 2: [Core Features]
**Duration**: 2-4 weeks
**Priority**: High
**Dependencies**: Phase 1 complete

[Same structure as Phase 1]

## Phase 3: [Enhanced Functionality]
**Duration**: 2-3 weeks
**Priority**: Medium
**Dependencies**: Phase 2 complete

[Same structure as Phase 1]

[Additional phases as needed]

## Risk Mitigation
- [Cross-phase risk]: [Mitigation strategy]
- [Technical risk]: [Mitigation approach]

## Integration Strategy
[How phases connect and build upon each other]
```

## Quality Criteria

### Phase Design Quality
1. **Value Delivery**: Each phase provides user value
2. **Scope Clarity**: Clear boundaries and deliverables
3. **Dependency Logic**: Sensible sequencing
4. **Balance**: Even complexity distribution
5. **Completeness**: All requirements addressed

### Technical Readiness
1. **Spec Preparation**: Sufficient context for `/specter-spec`
2. **Research Identification**: Knowledge gaps noted
3. **Integration Planning**: Touchpoints documented
4. **Risk Awareness**: Challenges identified
5. **Success Measurability**: Clear criteria

## Decomposition Strategies

### Phase Sizing Guidelines
```markdown
Small Phase (1-2 weeks):
- Single feature or component
- Limited integration complexity
- Well-understood technology
- Low risk implementation

Medium Phase (2-3 weeks):
- Multiple related features
- Moderate integration needs
- Some new technology
- Manageable risk

Large Phase (3-4 weeks):
- Complex feature set
- Significant integration
- Multiple new technologies
- Higher risk, more unknowns
```

### Decomposition Patterns

#### Pattern 1: Foundation First
```markdown
Phase 1: Core Infrastructure (auth, database, framework)
Phase 2: Primary Features (main business logic)
Phase 3: Enhancement Features (additional capabilities)
Phase 4: Optimization (performance, scaling)
```

#### Pattern 2: Vertical Slices
```markdown
Phase 1: Complete Feature A (end-to-end)
Phase 2: Complete Feature B (end-to-end)
Phase 3: Complete Feature C (end-to-end)
Phase 4: Integration and Polish
```

#### Pattern 3: MVP Progressive
```markdown
Phase 1: Minimal Viable Product
Phase 2: Essential Enhancements
Phase 3: Differentiation Features
Phase 4: Scale and Performance
```

## Refinement Behavior

### Addressing Common Feedback

#### Phase Too Large
- Split into smaller phases
- Move some features to later phases
- Identify natural breakpoints
- Reduce scope to core functionality

#### Missing Dependencies
- Reorder phases for proper sequencing
- Add prerequisite work to earlier phases
- Document integration requirements
- Clarify blocking relationships

#### Unclear Scope
- Add specific deliverables
- Define clear boundaries
- List excluded items explicitly
- Provide concrete examples

#### Imbalanced Complexity
- Redistribute features across phases
- Move complex items earlier
- Balance team capacity
- Even out implementation effort

## Error Handling

### Input Issues
```markdown
If strategic plan incomplete:
1. Work with available information
2. Note gaps in roadmap overview
3. Flag areas needing clarification
4. Provide best-effort decomposition

If objectives unclear:
1. Make reasonable assumptions
2. Document assumptions clearly
3. Focus on stated requirements
4. Note areas of uncertainty
```

### Decomposition Challenges
```markdown
If requirements too vague:
1. Create high-level phases
2. Note need for refinement
3. Focus on clear requirements
4. Document clarification needs

If timeline unrealistic:
1. Document timeline concerns
2. Propose realistic alternative
3. Identify minimum viable scope
4. Suggest priority adjustments
```

## Example Interactions

### Initial Decomposition
```markdown
roadmap: Analyzing strategic plan for AI-powered feedback system.

Identifying implementation phases based on:
- Core requirements: feedback collection, AI analysis, routing
- Technical dependencies: database before API, auth before features
- Business priorities: MVP in 6 weeks, full system in 12 weeks

Creating 4-phase roadmap:

Phase 1: Foundation (Weeks 1-2)
- Authentication and user management
- Database schema and core models
- Basic API framework

Phase 2: Feedback Collection (Weeks 3-5)
- Multi-channel feedback ingestion
- Data validation and storage
- Basic categorization

Phase 3: AI Integration (Weeks 6-8)
- ML model integration
- Automated analysis pipeline
- Priority assignment

Phase 4: Routing & Analytics (Weeks 9-11)
- Intelligent routing system
- Analytics dashboard
- Reporting capabilities
```

### Refinement Based on Feedback
```markdown
Previous feedback indicates Phase 2 too large and Phase 3 dependencies unclear.

Restructuring roadmap:

Splitting Phase 2 into:
- Phase 2A: Basic Feedback Collection (Week 3-4)
- Phase 2B: Multi-channel Integration (Week 5)

Clarifying Phase 3 dependencies:
- Requires: Phase 2A complete (basic feedback flow)
- Does not require: Phase 2B (can proceed in parallel)
```

## Performance Considerations

### Context Management
- Summarize lengthy strategic plans
- Focus on implementation-relevant sections
- Extract key requirements efficiently
- Maintain phase relationships clearly

### Output Optimization
- Keep phase descriptions concise
- Focus on actionable information
- Avoid redundant details
- Provide clear spec context

## Success Metrics

### Quantitative Metrics
- **Phase Count**: 3-7 phases optimal
- **Phase Size**: 2-4 weeks each
- **Dependency Clarity**: 100% mapped
- **Requirement Coverage**: >95%

### Qualitative Metrics
- **Implementability**: Phases clearly scoped
- **Value Delivery**: Each phase useful
- **Risk Distribution**: Balanced across phases
- **Spec Readiness**: Context sufficient

## Integration Notes

### Input from /specter-plan Command
- Receives complete strategic plan
- Uses structured objectives analysis
- Maintains business context
- Preserves success criteria

### Output for /specter-spec Command
- Provides phase-specific context
- Identifies technical focus areas
- Documents research needs
- Enables targeted specification

## Related Documentation
- [`/specter-roadmap` Command Specification](../commands/specter-roadmap.md)
- [`roadmap-critic` Agent Specification](roadmap-critic.md)
- [`/specter-plan` Command Specification](../commands/specter-plan.md)
- [`/specter-spec` Command Specification](../commands/specter-spec.md)
