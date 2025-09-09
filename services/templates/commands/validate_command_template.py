def generate_validate_command_template(
    get_spec_tool: str, list_comments_tool: str, add_comment_tool: str, critic_agent_name: str
) -> str:
    return f"""---
allowed-tools:
  - Read
  - Task(plan-critic)
  - Task(spec-critic)
  - Task(build-plan-critic)
  - {get_spec_tool}
  - {list_comments_tool}
  - {add_comment_tool}
argument-hint: [plan-name-or-ticket-id]
description: Comprehensive quality assessment using 12-point FSDD quality gate system
---

# Quality Validation Command

Execute comprehensive quality assessment across strategic plans, specifications, and implementations using the 12-point FSDD quality gate system.

## Your Task

Validate quality of content identified by: $ARGUMENTS

## Validation Workflow

### Phase 1: Content Type Detection

Determine the type of content to validate based on the argument:

#### Strategic Plan Validation
If argument matches a strategic plan name:
- Read plan from `docs/strategic-plans/$ARGUMENTS.md`
- Apply strategic plan quality gates
- Use `Task(plan-critic)` for detailed assessment

#### Technical Specification Validation  
If argument appears to be a specification reference:
- Locate specification document or ticket
- Apply technical specification quality gates
- Use `Task(spec-critic)` for detailed assessment

#### Implementation Plan Validation
If argument references build plans or implementation:
- Read implementation documentation
- Apply implementation quality gates
- Use `Task(build-plan-critic)` for detailed assessment

#### Ticket-Based Validation
If argument is a ticket ID (detected pattern):
- Use {get_spec_tool} to retrieve ticket content
- Determine content type from ticket structure
- Apply appropriate quality gate framework

### Phase 2: FSDD Quality Gate Assessment

Execute comprehensive 12-point FSDD quality assessment:

#### Gate 1-4: Strategic Alignment Gates
- **Business Justification**: Clear business value and problem statement
- **Stakeholder Alignment**: Requirements meet stakeholder needs
- **Success Criteria**: Measurable outcomes and acceptance criteria
- **Scope Definition**: Clear boundaries and constraints

#### Gate 5-8: Technical Completeness Gates  
- **Architecture Definition**: System design and component structure
- **Technology Selection**: Appropriate technology choices with justification
- **Integration Planning**: System interfaces and data flows
- **Quality Standards**: Testing, monitoring, and quality requirements

#### Gate 9-12: Implementation Readiness Gates
- **Implementation Approach**: Clear development methodology and approach
- **Resource Planning**: Timeline, skills, and resource requirements
- **Risk Assessment**: Identified risks and mitigation strategies
- **Deployment Strategy**: Release and operational considerations

### Phase 3: Quality Assessment Execution

#### Automated Quality Checks
Execute systematic quality assessment:
```python
# Use appropriate critic agent based on content type
critic_result = await Task({critic_agent_name})(
    content=target_content,
    quality_framework="fssd",
    assessment_depth="comprehensive"
)
```

#### Manual Quality Review
Supplement automated checks with manual review:
- Review critic agent findings for accuracy and completeness
- Validate quality gate scoring against actual content
- Identify areas requiring human judgment or domain expertise
- Cross-reference with project context and constraints

### Phase 4: Gap Analysis and Recommendations

#### Quality Gap Identification
Systematically identify quality gaps:
- Compare current quality scores against FSDD thresholds
- Identify specific areas below quality standards
- Prioritize gaps by impact on project success
- Group related gaps for efficient remediation

#### Improvement Recommendations
Provide specific, actionable recommendations:
- Detailed steps to address each identified quality gap
- Prioritization of improvements based on impact and effort
- Resource requirements for implementing improvements
- Timeline estimates for quality remediation activities

### Phase 5: Documentation and Tracking

#### Quality Assessment Report
Generate comprehensive quality report including:
- FSDD quality gate scores with detailed breakdown
- Specific quality gaps identified with evidence
- Prioritized improvement recommendations with implementation guidance
- Overall quality assessment summary and next steps

#### Progress Tracking
Document assessment for ongoing quality management:
- Use {add_comment_tool} to record quality assessment results
- Create improvement tracking items with specific acceptance criteria
- Establish quality monitoring checkpoints for future assessments
- Link quality improvements to project milestones and deliverables

## Quality Scoring Framework

### FSDD Quality Gate Scoring
Each gate scored on 0-10 scale:
- **0-3**: Critical gaps requiring immediate attention
- **4-6**: Significant improvements needed before proceeding
- **7-8**: Good quality with minor improvements recommended
- **9-10**: Excellent quality meeting or exceeding standards

### Overall Quality Assessment
- **Minimum Threshold**: 7.0 average across all gates
- **Gate Minimums**: No individual gate below 5.0
- **Critical Gates**: Gates 1, 5, 9 must score 7.0+ (strategic, technical, implementation)
- **Quality Trends**: Track improvement over time through repeated assessments

## Validation Outcomes

### Quality Compliance Achieved
When quality standards are met:
- Document successful quality validation with evidence
- Provide quality certification for next development phase
- Establish quality monitoring checkpoints for ongoing compliance
- Archive quality assessment documentation for reference

### Quality Improvements Needed
When quality gaps are identified:
- Provide detailed improvement roadmap with specific actions
- Establish quality remediation timeline with milestones
- Assign improvement tasks to appropriate team members
- Schedule follow-up quality assessment after improvements

## Tool Usage

- Use {get_spec_tool} to retrieve ticket or specification content
- Use {list_comments_tool} to review previous quality discussions
- Use {add_comment_tool} to document quality assessment results and recommendations
- Use Task(critic-agents) to execute detailed quality assessments
- Use Read for accessing strategic plans and documentation files

## Success Criteria

- Comprehensive FSDD quality assessment completed with detailed scoring
- Specific quality gaps identified with actionable improvement recommendations
- Quality assessment results properly documented for team access
- Clear next steps provided for achieving quality compliance
- Quality monitoring process established for ongoing compliance verification
- Team equipped with specific guidance for quality improvements
"""
