# /plan-conversation Command Specification

## Overview
The `/plan-conversation` command conducts structured conversational requirements gathering through natural dialogue with users. It operates as an interactive discovery tool that transforms business ideas into comprehensive structured context for strategic planning, emphasizing user comfort and natural conversation flow over formal requirements elicitation.

## Command Metadata

**Name**: `/plan-conversation`
**Type**: Interactive conversational discovery tool
**Phase**: Requirements Gathering (Sub-phase of Strategic Planning)
**Model**: Claude Sonnet (default)
**Tools**: None (pure conversation, no tool access)

## Invocation

### Who Invokes It
- **Primary**: `/plan` command during strategic planning workflow
- **Secondary**: Can be invoked independently for requirements exploration
- **Context**: When comprehensive user requirements need to be gathered through dialogue

### Trigger Format
```text
/plan-conversation [optional-context]
```

### Parameters
- **optional-context**: Starting context or initial prompt to begin conversation

## Workflow Position

```text
/plan command → /plan-conversation → Structured Context → Strategic Plan Generation
                       ↓
               [3-Stage Progressive Dialogue]
                       ↓
               [Natural Conversation Flow]
                       ↓
               [Structured JSON Output]
```

### Position in Strategic Planning Flow
1. **Sub-Command**: Called by `/plan` command for requirements gathering
2. **Input**: Optional initial context or starting prompt
3. **Process**: Interactive 3-stage conversation with user
4. **Output**: Structured JSON context for strategic plan generation
5. **Handoff**: Returns control to `/plan` command with conversation results

## Primary Responsibilities

### Core Tasks

1. **Natural Conversation Facilitation**
   - Conduct comfortable, non-interrogative dialogue
   - Build understanding progressively from general to specific
   - Encourage voluntary information sharing and user engagement
   - Maintain natural conversation pacing and flow

2. **Progressive Requirements Discovery**
   - Guide conversation through 3 structured stages
   - Validate understanding before advancing to new topics
   - Bridge conversation topics for comprehensive coverage
   - Identify and resolve contradictions through dialogue

3. **Structured Context Generation**
   - Transform conversational insights into organized JSON structure
   - Capture vision, requirements, constraints, and priorities
   - Document conversation quality and engagement metrics
   - Prepare context for strategic plan generation

4. **Conversation Quality Management**
   - Monitor engagement levels and adjust approach accordingly
   - Handle conversation stalls, overwhelm, and technical confusion
   - Ensure completion criteria are met before finishing
   - Provide recovery patterns for conversation challenges

## Conversation Methodology

### Stage 1: Vision and Context Discovery

**Purpose**: Build broad understanding of project vision and driving factors

**Conversation Approach**:
- **Vision Understanding**: "Tell me about what you're trying to build or achieve"
- **Context Gathering**: "What's driving this project? What problem are you solving?"
- **Success Exploration**: "How will you know when this is successful?"
- **Stakeholder Context**: "Who are the main people involved or affected by this?"

**Conversational Techniques**:
- **Follow-up Questions**: Build naturally on user responses with related questions
- **Clarifying Examples**: Use examples to validate understanding and prompt additional details
- **Active Listening**: "I hear that [X] is important because..."
- **Gentle Probing**: Ask for more information when answers seem incomplete without being pushy
- **Context Bridging**: Connect different parts of the conversation to build comprehensive understanding
- **Open Space**: Give user time to add what they think matters

### Stage 2: Progressive Requirement Refinement

**Purpose**: Guide conversation toward specific details while maintaining natural flow

**Conversation Approach**:
- **Scope Clarification**: "Let's talk about what this includes and what it doesn't"
- **User Experience Focus**: "Walk me through how someone would use this"
- **Integration Context**: "What other systems or tools does this need to work with?"
- **Constraint Exploration**: "What limitations or requirements do we need to work within?"

**Understanding Validation**:
- **Summarization**: "So if I understand correctly, you're looking for..."
- **Gap Identification**: "I want to make sure I'm not missing anything important..."
- **Priority Confirmation**: "It sounds like [X] is more important than [Y], is that right?"
- **Constraint Validation**: "Given what you've told me about [constraint], does that mean...?"

### Stage 3: Detail and Validation

**Purpose**: Refine understanding with specific validation and priority clarification

**Conversation Approach**:
- **Requirement Validation**: "Let me make sure I understand correctly..."
- **Priority Clarification**: "What's most important if we had to prioritize?"
- **Timeline Context**: "What's the timeline you're thinking about?"
- **Success Criteria**: "How will we measure if this is working well?"

**Conversation Management**:
- **Pacing**: Allow natural conversation flow without rushing toward detailed requirements
- **Context Bridging**: Connect different parts of conversation to maintain comprehensive understanding
- **Comfort Building**: Create a comfortable environment for sharing incomplete thoughts and ideas
- **Active Response**: Respond to what the user emphasizes and follow their natural direction

## Quality Indicators

### Good Conversation Flow
- User provides information voluntarily without feeling interrogated
- Conversation builds naturally from general to specific
- User asks questions and engages actively in the discussion
- Understanding is validated before moving to new topics
- User expresses confidence that their needs are being understood

### Effective Requirement Gathering
- Requirements emerge naturally from conversation rather than through direct questioning
- User provides context and reasoning behind requirements
- Contradictions or conflicts are identified and resolved through discussion
- Priorities become clear through natural conversation progression
- User feels heard and understood throughout the process

### Conversation Completion Criteria

**Ready to Complete When**:
- All three stages have been conducted with meaningful user engagement
- User has provided sufficient detail in each major area (vision, requirements, constraints, priorities)
- Key questions have been answered and understanding has been validated
- User expresses satisfaction that their needs have been captured
- No critical information gaps remain that would prevent strategic plan creation

**Completion Checklist**:
- [ ] Vision and desired outcomes clearly articulated
- [ ] Key requirements and constraints identified
- [ ] Priorities and trade-offs discussed
- [ ] Success criteria defined
- [ ] User confirms understanding is accurate

## Output Specifications

### Structured Context Format
After completing all conversation stages and meeting completion criteria, generate structured JSON context:

```json
{
  "vision": {
    "problem_statement": "Clear description of the problem being solved",
    "desired_outcome": "What success looks like from user perspective",
    "success_metrics": "How success will be measured"
  },
  "business_context": {
    "business_drivers": "Key business motivations and pressures",
    "stakeholder_needs": "Different stakeholder requirements and concerns",
    "organizational_constraints": "Company or team limitations affecting the project"
  },
  "requirements": {
    "functional": ["Core features and capabilities needed"],
    "user_experience": ["User interaction and experience requirements"],
    "integration": ["Systems and tools that need to connect"],
    "performance": ["Speed, reliability, and efficiency needs"],
    "security": ["Data protection and access control requirements"],
    "technical_constraints": ["Technology limitations and preferences"]
  },
  "constraints": {
    "timeline": ["Time-related limitations and milestones"],
    "resource": ["Budget, team, and infrastructure constraints"],
    "business": ["Policy, compliance, and organizational limitations"],
    "technical": ["Technology stack and architecture constraints"]
  },
  "priorities": {
    "must_have": ["Essential features that define project success"],
    "nice_to_have": ["Desired features that can be deferred if needed"]
  },
  "conversation_summary": {
    "total_stages_completed": 3,
    "key_insights": ["Most important discoveries from the conversation"],
    "areas_of_emphasis": ["Topics the user stressed or returned to frequently"],
    "user_engagement_level": "high|medium|low"
  }
}
```

### Handoff Protocol
Once structured context is generated, return control to calling `/plan` command with:
- **CONVERSATION_CONTEXT**: Complete JSON structure populated with conversation insights
- **Completion Status**: Confirmation that all stages were completed successfully
- **Quality Assessment**: Engagement level and conversation effectiveness summary

## Error Handling and Recovery

### Conversation Stalls
**Symptoms**: User becomes unresponsive or provides minimal answers
**Recovery Strategies**:
- Rephrase questions using simpler language or concrete examples
- Offer multiple-choice options to jumpstart engagement
- Break complex questions into smaller, more manageable parts
- Example: "I notice you're hesitating. Would it help if I gave you some examples of what I mean?"

### Scope Overwhelm
**Symptoms**: User seems overwhelmed by the scope of questions
**Recovery Strategies**:
- Focus on one area at a time and reassure about the process
- Emphasize that incomplete answers can be refined later
- Suggest starting with what they're most confident about
- Example: "Let's start with just the core problem you're trying to solve. We can build from there."

### Technical Confusion
**Symptoms**: User gets bogged down in technical implementation details
**Recovery Strategies**:
- Redirect to business outcomes and user value
- Defer technical implementation discussions
- Focus on "what" rather than "how"
- Example: "Let's focus on what you want to achieve first. We'll figure out the technical approach later."

### Information Gaps
**Symptoms**: Critical information is missing after all stages
**Recovery Strategies**:
- Identify specific gaps and ask targeted follow-up questions
- Use hypothetical scenarios to help user think through unclear areas
- Suggest reasonable assumptions that can be validated later
- Document gaps clearly for strategic plan generation

### Conversation Recovery
**Symptoms**: Conversation derails or becomes unproductive
**Recovery Strategies**:
- Summarize progress made so far to re-establish momentum
- Identify the most important remaining areas to cover
- Offer to change approach or take a break if needed
- Example: "We've made good progress on X and Y. Let's focus on Z to wrap up the key pieces."

## Error Escalation
If conversation cannot be completed due to persistent issues:
- Populate `CONVERSATION_CONTEXT` with available information
- Include detailed notes in `conversation_summary` about challenges encountered
- Mark `user_engagement_level` as "low" with specific reasons
- Return partial context to `/plan` command with completion status

## Integration with /plan Command

### Command Relationship
- **Called By**: `/plan` command during Step 2 of strategic planning workflow
- **Purpose**: Replace direct requirements gathering with natural conversation
- **Context Handoff**: Receives optional starting context, returns structured JSON
- **Error Handling**: Reports completion status and engagement quality to caller

### Variable Integration
- **Input Variable**: Uses starting context from `/plan` command's `$ARGUMENTS`
- **Output Variable**: Populates `CONVERSATION_CONTEXT` for strategic plan generation
- **State Management**: Operates independently without MCP tools or persistent state

### Success Integration
When conversation completes successfully:
1. **Context Ready**: Structured JSON context prepared for strategic plan generation
2. **Quality Validated**: All completion criteria met and user satisfaction confirmed
3. **Handoff Clean**: Clear return to `/plan` command for strategic plan creation
4. **Error Free**: No conversation issues or information gaps requiring escalation

## Implementation Notes

### Key Considerations for Claude Code

1. **Natural Dialogue Priority**
   - Emphasize conversational comfort over formal requirements gathering
   - Allow user to drive conversation direction while ensuring coverage
   - Build trust and engagement before diving into detailed requirements

2. **Progressive Discovery**
   - Start broad and narrow focus gradually through natural conversation flow
   - Validate understanding at each stage before progressing
   - Handle topic switching and conversation branching gracefully

3. **Context Quality**
   - Ensure JSON structure captures nuanced conversation insights
   - Balance structured data with preservation of user intent and emphasis
   - Document conversation quality for downstream strategic plan generation

4. **Error Resilience**
   - Multiple recovery patterns for different conversation challenges
   - Graceful degradation when full completion isn't possible
   - Clear escalation path to `/plan` command with partial results

5. **User Experience Focus**
   - Maintain conversational flow without feeling like form-filling
   - Encourage elaboration and storytelling over brief answers
   - Create safe space for incomplete thoughts and evolving ideas

## Success Metrics

### Quantitative Metrics
- **Completion Rate**: Target >95% successful completion with all stages
- **Engagement Quality**: Target "high" user engagement level >80% of conversations
- **Context Completeness**: Target >90% of JSON fields populated with meaningful content
- **Stage Progression**: Target smooth progression through all 3 stages >95% of time

### Qualitative Metrics
- **User Satisfaction**: Users feel heard and understood throughout conversation
- **Natural Flow**: Conversation feels collaborative rather than interrogative
- **Comprehensive Coverage**: All major project aspects discovered through dialogue
- **Strategic Plan Readiness**: Context sufficient for high-quality strategic plan generation

## Related Documentation
- **Parent Command**: [`/plan` Command Specification](plan.md)
- **Output Usage**: Strategic plan generation and ProjectPlan model creation
- **Quality Framework**: FSDD assessment preparation through comprehensive context
- **Integration Pattern**: Sub-command invocation and structured context handoff
