# Strategic Plan Creation Template - FSDD Enhanced

## Template Purpose
**Used by**: Strategic planning process (Claude Code command or manual creation)  
**When**: Creating new phase strategic plans  
**Context**: Part of Strategic Planning Integration - defines system-level functional specifications and architectural contracts that feed into Issue Creation Agent Flow  
**Enhancement**: Now uses Functional Specification-Driven Development (FSDD) to create testable, constraint-driven strategic plans

## Variable Requirements
**FSDD Strategic Variables (Tier 2)** - prevent hallucination through functional specifications:

### Core Phase Variables
- `PHASE_NUMBER`: Phase number (e.g., "2")
- `PHASE_DESCRIPTION`: Brief phase description
- `PRIMARY_GOAL`: Measurable outcome with success criteria

### Technology Stack Variables (NEW)
- `CURRENT_TECHNOLOGIES`: Technologies from detect-packages.sh selected by user for this phase
- `NEW_TECHNOLOGIES`: Technologies not in project that user wants to add
- `SELECTED_RESEARCH`: Existing research documents user selected from archive scan
- `RESEARCH_TOPICS`: User-specified technology combinations to research

### System Functional Specifications (NEW)
- `SYSTEM_INTERFACE_CONTRACTS`: EARS notation (WHEN/THEN) for all system interfaces
- `HARD_CONSTRAINT_DEFINITIONS`: Explicit SHALL/SHALL NOT system boundaries
- `PERFORMANCE_CONTRACTS`: Measurable system-level SLAs with specific numbers
- `INTEGRATION_SPECIFICATIONS`: Concrete connection points with existing systems

### Implementation Constraints Framework (NEW)
- `APPROVED_TECHNOLOGY_PATTERNS`: Explicit allowed libraries/frameworks/patterns only
- `FORBIDDEN_IMPLEMENTATIONS`: What SHALL NOT be built (scope boundaries)  
- `SCOPE_LOCK_BOUNDARIES`: Feature freeze definitions with rationale
- `VALIDATION_GATE_REQUIREMENTS`: System-level pass/fail criteria for iterations

### Architecture & Risk Analysis  
- `TECHNOLOGY_CHOICES`: Key technical decisions with rationale
- `MAJOR_COMPONENTS`: Component names, purposes, and boundaries
- `UI_REQUIREMENTS`: User interface components and experience requirements
- `DEPENDENCY_MAP`: Critical dependencies between components and potential bottlenecks
- `RISK_ANALYSIS`: High-risk assumptions and early validation strategies
- `ALTERNATIVE_APPROACHES`: Other valid implementation strategies considered

### Implementation Strategy Variables (Enhanced)
- `SEQUENCING_APPROACH`: Foundation, Building, and Validation phases with clear dependencies
- `CRITICAL_DEPENDENCIES`: External, internal, and team dependencies with specifications
- `RISK_MITIGATION_STRATEGY`: Technical, integration, and timeline risk mitigation with contingencies
- `QUALITY_FRAMEWORK_INTEGRATION`: Testing strategy, validation gates, and code quality standards

## FSDD Strategic Planning Context
This template creates **system-level functional specifications** that remain stable:
- System interface contracts using EARS notation (WHEN/THEN format)
- Hard constraint boundaries (SHALL/SHALL NOT definitions)  
- Performance contracts with measurable criteria
- Technology constraint frameworks (approved/forbidden patterns)

**Tactical functional specifications** (detailed input/output contracts, test scenarios, implementation acceptance criteria) are handled by Linear tickets created from this strategic plan using FSDD principles.

## Template Content

---

```markdown
# Phase ${PHASE_NUMBER}: ${PHASE_DESCRIPTION}

## Phase Objectives
- **Primary Goal**: ${PRIMARY_GOAL}
- **Secondary Goals**: [Supporting objectives that enable the primary goal]
- **Integration Requirements**: [How this phase builds on previous phases]

## Technology Stack

### Selected Technologies
**Current Technologies**: ${CURRENT_TECHNOLOGIES}
**New Technologies**: ${NEW_TECHNOLOGIES}

### Research Foundation
**Selected Research Documents**: ${SELECTED_RESEARCH}
**Research Topics for Future Research**: ${RESEARCH_TOPICS}

## System Functional Specifications

### System Interface Contracts
${SYSTEM_INTERFACE_CONTRACTS}

### Hard Constraint Definitions  
${HARD_CONSTRAINT_DEFINITIONS}

### Performance Contracts
${PERFORMANCE_CONTRACTS}

### Integration Specifications
${INTEGRATION_SPECIFICATIONS}

## Implementation Constraints Framework

### Approved Technology Patterns
${APPROVED_TECHNOLOGY_PATTERNS}

### Forbidden Implementations
${FORBIDDEN_IMPLEMENTATIONS}

### Scope Lock Boundaries
${SCOPE_LOCK_BOUNDARIES}

### Validation Gate Requirements
${VALIDATION_GATE_REQUIREMENTS}

## Architecture Framework

### Key Technical Decisions
${TECHNOLOGY_CHOICES}

### Component Architecture
${MAJOR_COMPONENTS}

### User Interface Requirements
${UI_REQUIREMENTS}

## Risk & Dependency Analysis
**Critical Dependencies**: ${DEPENDENCY_MAP}

**Risk Assessment**: ${RISK_ANALYSIS}

**Alternative Approaches Considered**: ${ALTERNATIVE_APPROACHES}

## Implementation Strategy

### Sequencing Approach
${SEQUENCING_APPROACH}

### Critical Dependencies
${CRITICAL_DEPENDENCIES}

### Risk Mitigation Strategy
${RISK_MITIGATION_STRATEGY}

### Quality Framework Integration
${QUALITY_FRAMEWORK_INTEGRATION}

## Implementation Step Guidance (for issue-parser synthesis)
Each implementation step should be extractable from strategic specifications with:
- **Function Signatures**: Derivable from system interface contracts
- **EARS Specifications**: Based on system interface WHEN/THEN contracts
- **Error Handling**: Inferred from hard constraint boundaries 
- **Performance Requirements**: Specific to each step from performance contracts
- **Input/Output Specs**: Concrete examples based on system interfaces
- **Test Scenarios**: Happy path, edge cases, integration scenarios from validation gates
- **Technology Usage**: Constrained by approved technology patterns
- **Scope Boundaries**: Enforced by forbidden implementations and scope lock

## Linear Integration Points
- **Specification Inheritance**: How tactical specifications derive from strategic contracts
- **Constraint Enforcement**: How Linear tickets enforce strategic boundaries
- **Traceability Links**: Connection between system contracts and implementation specifications
- **Feedback Protocol**: How implementation discoveries update strategic specifications
```

---

## FSDD Usage Instructions
1. **System Contract Definition**: Replace all `${VARIABLE}` placeholders with concrete functional specifications using EARS notation (WHEN/THEN format)
2. **Constraint Framework**: Define explicit boundaries using SHALL/SHALL NOT language with measurable criteria  
3. **Issue Creation Handoff**: Strategic contracts become input constraints for tactical specifications in Linear tickets
4. **Specification Validation**: All strategic specifications must be testable and measurable
5. **Implementation Feedback**: Plan synchronization assessments validate implementation against strategic contracts

## FSDD Integration Flow
- **Strategic Contracts** → **issue-parser** (extracts system interface requirements for tactical specifications)
- **Constraint Framework** → **issue-classifier** (enforces strategic boundaries in ticket specifications)  
- **Strategic Specifications** ← **impl-verifier** (validates implementation compliance with system contracts)
- **Performance Contracts** ← **test results** (validates system meets specified SLA requirements)

## Implementation Strategy (Enhanced)

### Sequencing Approach
- **Foundation Phase**: Core components that must be built first, with clear dependencies
- **Building Phase**: Components that build on foundation, with integration points defined
- **Validation Phase**: How phases integrate and validate together with measurement criteria

### Critical Dependencies
- **External Dependencies**: Third-party services, APIs, libraries required with version specifications
- **Internal Dependencies**: Previous phase outputs, existing system integration requirements
- **Team Dependencies**: Knowledge requirements, skill development needed, training timelines

### Risk Mitigation Strategy
- **Technical Risk**: Specific mitigation approach with fallback options and contingency plans
- **Integration Risk**: Validation strategy for component interactions and interface compatibility
- **Timeline Risk**: Buffer strategies and scope adjustment protocols with milestone checkpoints

### Quality Framework Integration
- **Testing Strategy**: Comprehensive approach covering unit, integration, system, and acceptance testing aligned with FSDD principles
- **Validation Gates**: System-level pass/fail criteria for each phase with measurable outcomes
- **Code Quality Standards**: CLAUDE.md compliance, review processes, automation requirements, and continuous integration

## Linear Integration Points (Enhanced)

### Ticket Creation Triggers
- **When**: Specific conditions that trigger creation of Linear tickets from strategic contracts
- **What**: Types of tickets to create (technical specifications, implementation tasks, validation scenarios)
- **Who**: Responsibility assignment for ticket execution with clear ownership and accountability

### Information Flow Documentation
- **Strategic → Tactical**: How FSDD contracts inform ticket acceptance criteria and implementation constraints
- **Architecture → Research**: How technical decisions guide research requirements in Linear tickets
- **Quality Framework → Testing**: How strategic validation gates shape ticket testing requirements and scenarios

### Feedback Loops and Change Management
- **Implementation → Strategy**: How implementation discoveries update strategic contracts and constraints
- **Update Protocol**: Process for incorporating learnings back into strategic specifications
- **Change Management**: How to handle valid vs invalid divergences from strategic plan

## Plan Synchronization Protocol

### Synchronization Assessment Framework
Each Linear ticket includes plan synchronization evaluation following this framework:

**Valid Divergence Triggers**:
- Implementation reveals better understanding of system requirements or technical constraints
- Technical limitations require different architectural approach than initially planned
- Better solution discovered during implementation that improves system contracts
- Performance requirements necessitate design changes while maintaining strategic objectives

**Invalid Divergence Triggers**:
- Implementation exceeds intended scope without architectural justification or strategic approval
- Key FSDD requirements ignored or bypassed during implementation without constraint analysis
- Technology choices made without considering strategic decisions and approved patterns
- Quality requirements bypassed without plan consultation and impact assessment

### Change Management Framework

**Strategic-Level Changes**:
- Architecture modifications require impact assessment across all system contracts and components
- Component boundary changes may affect multiple implementation tickets and integration points
- Technology choice changes require broad evaluation, constraint analysis, and plan updates

**Context Preservation Strategy**:
- Deferred functionality captured in Linear tickets with full FSDD analysis and rationale
- Implementation discoveries documented with impact on strategic contracts and future phases
- Alternative approaches preserved with evaluation criteria for potential future consideration
