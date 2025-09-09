def generate_refine_build_command_template(
    get_spec_tool: str,
    list_comments_tool: str,
    refinement_loop_tool: str,
    parse_command_tool: str,
    add_comment_tool: str,
    technology_analysis_summary: str,
    performance_improvements: str,
    risk_mitigation_plans: str,
    refined_implementation_roadmap: str,
    quality_gate_implementation: str,
) -> str:
    return f"""---
allowed-tools:
  - {get_spec_tool}
  - {list_comments_tool}
  - Bash(~/.claude/scripts/detect-packages.sh)
  - {refinement_loop_tool}
  - {parse_command_tool}
  - {add_comment_tool}
argument-hint: [ticket-id]
description: Optimize implementation plans with RefinementLoop tool for technology-aware feasibility and performance analysis
---

You are executing the `/refine-build` command to optimize implementation plans through critic/refiner loops.

## Command Execution Flow

### 1. Technology Stack Analysis
Execute comprehensive technology inventory:
```bash
~/.claude/scripts/detect-packages.sh
```

Analyze for:
- Current dependencies and versions
- Compatibility matrix
- Performance characteristics
- Integration patterns
- Development tool chain

### 2. Implementation Plan Retrieval
Use spec management tools to get current implementation plan:
```python
# Retrieve ticket and implementation plan
ticket_data = await {get_spec_tool}(ticket_id="$ARGUMENTS")
current_plan = ticket_data['description']

# Get implementation context from comments
comments = await {list_comments_tool}(issue_id="$ARGUMENTS")
implementation_context = extract_technical_context(comments)
```

### 3. RefinementLoop Execution for Implementation Optimization

Execute critic/refiner loop focused on implementation feasibility and performance:

**Technology-Aware Implementation Refinement**
```python
# Execute refinement with build-specific focus
result = await {refinement_loop_tool}(
    critic_agent='build-plan-critic',
    refiner_agent='build-plan-refiner', 
    content=current_plan,
    content_type='implementation_plan',
    quality_threshold=0.85,
    max_iterations=3,
    
    # Technology context for feasibility analysis
    technology_context={{
        'current_stack': detected_packages,
        'performance_requirements': extract_performance_reqs(ticket_data),
        'integration_constraints': extract_integration_constraints(comments),
        'resource_limitations': extract_resource_constraints(ticket_data)
    }}
)
```

### 4. Feasibility and Performance Analysis

#### Technical Feasibility Assessment
Analyze refined plan for technical feasibility:
- **Technology Compatibility**: Verify all components work with current stack
- **Integration Complexity**: Assess integration effort and risk
- **Performance Impact**: Evaluate performance implications of approach
- **Resource Requirements**: Validate resource needs against constraints
- **Timeline Feasibility**: Assess development timeline against plan complexity

#### Performance Optimization Analysis
Focus on performance aspects of implementation:
- **Scalability Patterns**: Ensure implementation scales with usage
- **Performance Bottlenecks**: Identify and address potential bottlenecks
- **Resource Optimization**: Optimize memory, CPU, and I/O usage
- **Caching Strategies**: Implement appropriate caching where beneficial
- **Database Optimization**: Ensure efficient data access patterns

### 5. Risk Assessment and Mitigation

#### Implementation Risk Analysis
Identify and assess implementation risks:
- **Technical Risks**: Complex integrations, new technologies, performance challenges
- **Timeline Risks**: Scope creep, dependency delays, complexity underestimation  
- **Resource Risks**: Skill gaps, capacity constraints, external dependencies
- **Quality Risks**: Testing complexity, debugging challenges, maintenance burden

#### Risk Mitigation Strategies
Develop specific mitigation approaches:
- **Technical Mitigation**: Proof of concepts, incremental implementation, fallback options
- **Timeline Mitigation**: Buffer allocation, scope prioritization, parallel development
- **Resource Mitigation**: Training plans, external support, skill sharing
- **Quality Mitigation**: Testing strategies, code review processes, monitoring plans

### 6. Enhanced Implementation Plan Documentation

#### Optimized Implementation Roadmap
Create refined implementation plan including:
- **Optimized Development Sequence**: Most efficient order of implementation
- **Technology-Specific Approaches**: Best practices for each technology component
- **Performance Implementation Patterns**: Specific patterns for performance requirements
- **Integration Implementation Strategy**: Step-by-step integration approach
- **Quality Gate Implementation**: Testing and validation at each development phase

#### Implementation Guidance Enhancement
Provide detailed implementation guidance:
- **Code Pattern Examples**: Specific code patterns for key components
- **Technology Configuration**: Optimal configuration for performance and scalability
- **Development Environment Setup**: Environment configuration for efficient development
- **Testing Strategy Implementation**: Detailed testing approach with specific tools
- **Deployment Optimization**: Deployment patterns for performance and reliability

### 7. Stakeholder Communication and Documentation

#### Implementation Plan Updates
Document refined implementation approach:
```python
# Update ticket with refined implementation plan
await {add_comment_tool}(
    issue_id="$ARGUMENTS",
    body=f'''

## Implementation Plan Refinement Results

### Technology Analysis Summary
{technology_analysis_summary}

### Performance Optimization Improvements
{performance_improvements}

### Risk Mitigation Strategies
{risk_mitigation_plans}

### Updated Implementation Roadmap
{refined_implementation_roadmap}

### Quality Gate Integration
{quality_gate_implementation}
'''
)
```

#### Team Communication
Prepare team communication materials:
- **Technical Brief**: Summary of optimization improvements and rationale
- **Implementation Changes**: Specific changes from original implementation plan
- **Performance Expectations**: Expected performance improvements from optimization
- **Risk Awareness**: Key risks and mitigation strategies for team awareness

## Quality Gates for Refined Implementation Plans

### Technical Feasibility Gates
- ✅ All technology components verified compatible with current stack
- ✅ Integration complexity assessed and mitigated with specific approaches
- ✅ Performance requirements addressed with measurable optimization strategies  
- ✅ Resource requirements validated against available capacity
- ✅ Implementation timeline realistic given complexity and constraints

### Performance Optimization Gates
- ✅ Scalability patterns implemented for anticipated load growth
- ✅ Performance bottlenecks identified and addressed with specific solutions
- ✅ Resource optimization strategies defined with measurable targets
- ✅ Caching strategies appropriate for usage patterns and data characteristics
- ✅ Database optimization aligned with data access patterns and volume

### Risk Management Gates
- ✅ Implementation risks comprehensively identified with likelihood assessment
- ✅ Risk mitigation strategies specific and actionable
- ✅ Contingency plans defined for high-impact risks
- ✅ Risk monitoring and early warning indicators established
- ✅ Team equipped with risk awareness and mitigation tools

## Success Criteria

- Implementation plan optimized through systematic critic/refiner analysis
- Technology feasibility validated with current stack and constraints
- Performance optimization strategies integrated throughout implementation approach
- Implementation risks identified and mitigated with specific strategies
- Team has clear, optimized implementation roadmap with performance focus
- Quality gates established for monitoring implementation progress and success

## Tool Usage Notes

- Use {get_spec_tool} and {list_comments_tool} for implementation context
- Use {refinement_loop_tool} for systematic implementation optimization
- Use {add_comment_tool} for documenting optimization results and guidance
- Technology detection provides current environment context for feasibility analysis
- Focus refinement on technical feasibility, performance, and risk mitigation aspects
"""
