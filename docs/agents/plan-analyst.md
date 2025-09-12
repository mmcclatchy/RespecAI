# plan-analyst Agent Specification

## Overview
The `plan-analyst` agent extracts and structures business objectives from conversational strategic plans. It transforms natural language requirements into clear, actionable objectives ready for technical specification.

## Agent Metadata

**Name**: `plan-analyst`  
**Type**: Business objective extraction specialist  
**Model**: Claude Sonnet  
**Invoked By**: Main Agent via `/plan` command  
**Phase**: Strategic Planning (Post-Loop Extraction)  

## Invocation Context

### When Invoked
- **After Loop Completion**: When plan reaches quality threshold
- **Post-Refinement**: Following successful plan refinement
- **One-Time Extraction**: Not part of refinement loop

### Invocation Pattern
```python
# Main Agent invokes plan-analyst after loop completion
response = Task(
    agent="plan-analyst",
    prompt=f"""
    Extract and structure business objectives from this strategic plan.
    
    Strategic Plan:
    {completed_plan}
    
    Create clear, measurable objectives ready for technical specification.
    """
)
```

## Workflow Position

```text
[plan-generator ↔ plan-critic loop] → Completed Plan → plan-analyst
                                                            ↓
                                                    Structured Objectives
                                                            ↓
                                                    Ready for /spec
```

### Role in Planning Phase
1. **Final Processing**: Transform conversational plan
2. **Objective Extraction**: Identify key business goals
3. **Structure Creation**: Organize for technical use
4. **Handoff Preparation**: Ready for spec-architect

## Primary Responsibilities

### Core Tasks

1. **Business Objective Extraction**
   - Identify primary business goals
   - Extract secondary objectives
   - Recognize implicit requirements
   - Separate must-have from nice-to-have

2. **Success Criteria Definition**
   - Convert vague goals to measurable outcomes
   - Quantify where possible
   - Define validation methods
   - Set achievement timelines

3. **Requirement Categorization**
   - Group by functional area
   - Identify dependencies
   - Prioritize by business value
   - Note technical constraints

4. **Stakeholder Mapping**
   - Identify user types
   - Define stakeholder needs
   - Map objectives to stakeholders
   - Clarify decision makers

5. **Risk and Constraint Documentation**
   - Extract identified risks
   - Document constraints
   - Note assumptions made
   - Highlight critical dependencies

## Tool Permissions

### Allowed Tools
- **None**: Pure analysis agent

### Restrictions
- No file system access
- No external tool invocation
- No user interaction
- No modification capabilities

## Input Specifications

### Analysis Input
```markdown
Extract and structure business objectives from this strategic plan.

Strategic Plan:
[Complete conversational plan from plan-generator]

Focus on:
- Clear business objectives
- Measurable success criteria
- Stakeholder needs
- Technical constraints
- Risk factors
```

## Output Specifications

### Structured Objectives Output
```markdown
# Business Objectives Analysis

## Primary Business Objective
**Reduce customer support response time by 60% through AI-powered automation**

### Success Metrics
- Average response time: From 4 hours to < 1.5 hours
- First-contact resolution: Increase from 45% to 70%
- Customer satisfaction: Maintain or improve current 4.2/5 rating
- Cost per ticket: Reduce by 40%

### Timeline
- Phase 1 (Months 1-2): Core categorization system
- Phase 2 (Months 3-4): Priority automation
- Phase 3 (Months 5-6): Full AI integration

## Secondary Objectives

### 1. Improve Support Team Efficiency
**Goal**: Enable support staff to focus on complex issues
- **Metric**: Reduce manual categorization time by 90%
- **Metric**: Increase complex issue resolution rate by 30%
- **Stakeholder**: Support Team Managers

### 2. Enhance Customer Experience
**Goal**: Provide faster, more accurate support responses
- **Metric**: Reduce escalation rate by 35%
- **Metric**: Improve self-service success rate to 60%
- **Stakeholder**: End Customers

### 3. Enable Data-Driven Insights
**Goal**: Generate actionable insights from support patterns
- **Metric**: Weekly trend reports with 95% accuracy
- **Metric**: Predictive issue detection with 80% accuracy
- **Stakeholder**: Product Team

## Functional Requirements

### Core Capabilities
1. **Automated Ticket Categorization**
   - Multi-label classification
   - 95% accuracy target
   - Real-time processing

2. **Intelligent Priority Assignment**
   - Dynamic priority based on content
   - Customer tier consideration
   - SLA compliance tracking

3. **Smart Routing System**
   - Skill-based assignment
   - Load balancing
   - Escalation paths

### Integration Requirements
- **CRM System**: Bidirectional sync with Salesforce
- **Email Platform**: Direct ingestion from support@
- **Chat System**: Live chat integration
- **Analytics**: Export to business intelligence tools

## Stakeholder Analysis

### Primary Stakeholders
| Stakeholder | Need | Success Criteria |
|-------------|------|------------------|
| Support Agents | Reduce manual work | 50% less time on categorization |
| Support Managers | Improve metrics | Meet all SLA targets |
| Customers | Faster resolution | <2 hour first response |
| Product Team | Insight access | Daily pattern reports |

### Decision Makers
- **Sponsor**: VP of Customer Success
- **Technical Lead**: Head of Engineering
- **Budget Owner**: CFO (for >$100k decisions)

## Constraints and Assumptions

### Technical Constraints
- Must integrate with existing Salesforce instance
- Cannot modify current email infrastructure
- Must comply with GDPR and CCPA
- Response time must be <200ms for API calls

### Business Constraints
- Budget: $250,000 initial, $50,000/year ongoing
- Timeline: 6-month implementation deadline
- Team: Maximum 5 dedicated developers
- Training: Minimal disruption to support operations

### Key Assumptions
- Support volume will remain 400-600 tickets/day
- Current categorization taxonomy is sufficient
- Support team will adopt new tools
- Historical data is available for training

## Risk Analysis

### High Priority Risks
1. **AI Accuracy Below Target**
   - Impact: User trust erosion
   - Mitigation: Human-in-loop validation phase
   - Contingency: Manual override capabilities

2. **Integration Complexity**
   - Impact: Timeline delays
   - Mitigation: Early spike on Salesforce API
   - Contingency: Phased integration approach

### Medium Priority Risks
1. **User Adoption Resistance**
   - Impact: Reduced ROI
   - Mitigation: Change management program
   - Contingency: Gradual rollout plan

## Implementation Priorities

### Phase 1: Foundation (Must Have)
1. Basic categorization system
2. Manual priority override
3. CRM integration
4. Basic reporting

### Phase 2: Enhancement (Should Have)
1. AI-powered categorization
2. Dynamic priority assignment
3. Advanced analytics
4. Automated routing

### Phase 3: Optimization (Nice to Have)
1. Predictive analytics
2. Sentiment analysis
3. Auto-response generation
4. Proactive issue detection

## Success Validation

### Acceptance Criteria
- [ ] 95% categorization accuracy on test set
- [ ] All API responses under 200ms
- [ ] Zero data loss during integration
- [ ] Support team satisfaction score >7/10
- [ ] Customer satisfaction maintained or improved

### Measurement Plan
- Daily: Ticket processing metrics
- Weekly: Accuracy assessments
- Monthly: Stakeholder satisfaction surveys
- Quarterly: ROI analysis
```

## Quality Criteria

### Extraction Completeness
1. **All Objectives Identified**: Primary and secondary
2. **Metrics Quantified**: Specific, measurable targets
3. **Stakeholders Mapped**: Clear ownership
4. **Constraints Documented**: Technical and business
5. **Risks Assessed**: With mitigation strategies

### Structural Clarity
1. **Logical Organization**: Hierarchical structure
2. **Clear Relationships**: Dependencies identified
3. **Priority Evident**: Must/should/nice classification
4. **Timeline Defined**: Phased approach clear
5. **Success Measurable**: Validation criteria specific

## Error Handling

### Extraction Challenges

1. **Vague Objectives**
   - Make reasonable assumptions
   - Note assumptions clearly
   - Suggest clarification needs
   - Provide range estimates

2. **Missing Information**
   - Flag gaps explicitly
   - Provide standard defaults
   - Note as risks
   - Suggest follow-up questions

3. **Conflicting Requirements**
   - Document both perspectives
   - Suggest resolution approach
   - Flag for clarification
   - Note impact on timeline

4. **Unrealistic Expectations**
   - Document as stated
   - Note feasibility concerns
   - Suggest alternatives
   - Flag for discussion

## Example Interactions

### Standard Extraction
```markdown
Analyzing strategic plan for AI-powered customer feedback system...

Extracted primary objective: Reduce support response time by 60%

Key findings:
- Clear business driver: Support team overwhelm
- Quantified success metrics: 4 hours → 1.5 hours
- Defined stakeholders: Support, Customers, Product
- Technical constraints: Salesforce, GDPR
- Implementation timeline: 6 months

Structuring objectives for technical specification...
[Full structured output follows]
```

### Handling Ambiguity
```markdown
Analyzing strategic plan...

Note: Some objectives require clarification:
- "Improve customer satisfaction" - No current baseline provided, assuming industry standard 4/5
- "Handle more tickets" - No volume specified, estimating 30% increase capability
- "Quick implementation" - Interpreting as 6-month timeline based on complexity

Proceeding with documented assumptions...
[Structured output with assumptions noted]
```

## Performance Considerations

### Analysis Efficiency
- Single-pass extraction
- Focus on actionable items
- Avoid over-analysis
- Maintain practical focus

### Output Size Management
- Concise but complete
- Avoid redundancy
- Use tables for clarity
- Link related items

## Success Metrics

### Quantitative Metrics
- **Extraction Coverage**: >95% of objectives captured
- **Metric Quantification**: >80% have numbers
- **Processing Time**: <30 seconds
- **Structure Clarity**: Consistent format

### Qualitative Metrics
- **Actionability**: Ready for technical design
- **Completeness**: No major gaps
- **Clarity**: Unambiguous objectives
- **Usefulness**: Enables specification phase

## Common Patterns and Anti-Patterns

### Effective Patterns ✓
- Clear objective hierarchy
- Quantified success metrics
- Stakeholder mapping
- Risk documentation
- Phased approach

### Anti-Patterns to Avoid ✗
- Over-interpretation of requirements
- Adding unstated objectives
- Ignoring constraints
- Missing dependencies
- Vague success criteria

## Integration Notes

### Input from plan-generator
- Receives completed plan
- Works with conversational format
- Extracts from natural language
- Preserves user intent

### Output for spec-architect
- Provides structured objectives
- Enables technical design
- Clarifies requirements
- Sets clear targets

## Related Documentation
- **Command**: [`/plan` Command Specification](../commands/plan.md)
- **Generator**: [`plan-generator` Agent Specification](plan-generator.md)
- **Critic**: [`plan-critic` Agent Specification](plan-critic.md)
- **Next Phase**: [`spec-architect` Agent Specification](spec-architect.md)