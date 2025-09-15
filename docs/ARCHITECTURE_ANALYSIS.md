# Spec-Driven Workflow Architecture Analysis

Complete architectural understanding of the Spec-Driven Workflow MCP Server system based on comprehensive analysis and clarifications.

## Project Overview

### Primary Goal
The Spec-Driven Workflow system is a **sophisticated AI workflow orchestration platform** that transforms natural language business requirements into production-ready code through structured, quality-driven development phases. The system bridges human strategic thinking with AI-driven technical execution using a multi-layered architecture with specialized agents and quality gates.

### Core Value Proposition
- **Multi-stage refinement loops** with specialized critic agents at each phase
- **Platform-agnostic storage** (Linear/GitHub/Markdown) with conversion capabilities  
- **Quality-driven progression** through FSDD gates with automated and human-in-the-loop fallbacks
- **Research integration** via global research-synthesizer agent using Exa MCP Server

## Complete Research Flow Architecture

### Research Orchestration Pipeline

```text
spec-architect identifies research needs
    ↓
Archive Scanning: research-advisor-archive-scan.sh checks ~/.claude/best-practices
    ↓
Gap Analysis: spec-architect identifies missing external research
    ↓
Research Prompt Creation: "Best practices when integrating [technologies] [current_year]"
    ↓
/build command orchestrates parallel research-synthesizer calls
    ↓
research-synthesizer instances create documentation files → return file paths
    ↓
build-planner reads ALL provided documentation → creates implementation plan
```

### Research Integration Strategy

**Archive-First Approach**:
- `spec-architect` uses `scripts/research-advisor-archive-scan.sh` to check existing documentation
- Script scans `~/.claude/best-practices` for relevant content using topic queries
- Only missing knowledge triggers external research requests

**External Research Orchestration**:
- Main Agent coordinates parallel `research-synthesizer` instances
- Research prompts follow structured pattern: "Best practices when integrating [technologies] [current_year]"
- Each research instance creates documentation file and returns path (not content)
- `build-planner` receives file paths and reads documentation to create coherent plans

**Research Responsibilities**:
- `spec-architect`: Identify research needs and gaps
- Main Agent: Orchestrate research calls, pass file paths
- `research-synthesizer`: Execute web research via Exa MCP Server
- `build-planner`: Consume all research documentation and synthesize implementation plans

## Quality Scoring & Loop Management Framework

### Scoring Architecture
- **Scale**: 0-100 numerical scores from critic agents
- **Thresholds**: Environment variables managed via Pydantic-Settings (tunable during testing)
- **Assessment**: LLM-based evaluation with structured criteria for consistency
- **MVP Approach**: Accepts reasonable consistency over perfect objectivity

### MCP Server Decision Engine

```text
Critic Score → MCP Server State Management → Next Action Decision:
├── High Score → "complete" (proceed to next phase)
├── Improving Score → "refine" (continue loop with feedback)  
└── Stagnation → "user-input" (escalate to human intervention)
```

### Stagnation Detection Logic
- **Score Plateauing**: No improvement over successive iterations
- **Max Iterations**: Hard limit reached regardless of progress
- **User Escalation**: System requests clarification when automated refinement fails
- **MVP Scope**: No cross-session persistence - stateless loop management

## Five Refinement Loops Architecture

### Loop 1: Strategic Planning (`/plan`)

**Participants**: Main Agent orchestration with `plan-critic`, `plan-analyst`, `analyst-critic`

**Process Flow**: Dual-loop orchestration workflow
1. **Initialize Planning Loop**: MCP state management setup
2. **Conversational Discovery**: `/plan-conversation` command guides natural language requirements gathering
3. **Strategic Plan Creation**: Main Agent processes conversation context using template
4. **Plan Quality Assessment**: `plan-critic` evaluates against FSDD framework
5. **Plan Refinement Loop**: MCP manages plan refinement iterations
6. **Initialize Analyst Loop**: Second validation loop setup
7. **Objective Extraction**: `plan-analyst` structures business objectives
8. **Analyst Quality Assessment**: `analyst-critic` validates extraction quality
9. **Analyst Validation Loop**: MCP manages analyst refinement iterations

**Quality Gate**: MCP Server-determined thresholds for strategic planning
**Output**: Strategic plan document with dual validation scores

### Loop 2: Implementation Roadmap (`/plan-roadmap`)

**Participants**: `plan-roadmap` ↔ `roadmap-critic`

**Process Flow**:
1. **Strategic Plan Context Gathering**: Access completed strategic plan and structured objectives
2. **Phase Decomposition**: Break down strategic plan into 3-7 implementable phases
3. **Dependency Mapping**: Establish logical sequencing and prerequisite relationships
4. **Roadmap Generation**: Create implementation roadmap with phase-specific contexts
5. **Quality Validation**: `roadmap-critic` assesses phase scoping, dependencies, and implementation readiness
6. **Spec Scaffolding**: Generate initial technical specifications for each phase
7. **Platform Integration**: Store roadmap and scaffolded specs in chosen platform

**Quality Gate**: MCP Server-determined thresholds for roadmap completeness and implementation readiness
**Output**: Implementation roadmap with phase-specific scaffolded specifications

### Loop 3: Technical Specification (`/spec`)

**Participants**: `spec-architect` ↔ `spec-critic`

**Process Flow**:
1. **Scaffolded Spec Analysis**: Review phase-specific specification template from roadmap
2. **Archive Integration**: `spec-architect` scans existing best practices documentation
3. **Research Gap Analysis**: Identifies external research requirements for phase focus areas
4. **Technical Architecture**: Complete detailed system architecture with technology stack integration
5. **Quality Validation**: `spec-critic` assesses technical completeness and FSDD compliance
6. **Platform Enhancement**: Enrich specification with comprehensive implementation guidance

**Quality Gate**: MCP Server-determined thresholds for production readiness
**Output**: Complete technical specification with full implementation guidance

### Loop 4: Implementation Planning (`/build` - Phase 1)

**Participants**: `build-planner` ↔ `build-critic`

**Process Flow**:
1. **Research Consumption**: `build-planner` reads all research documentation provided by Main Agent
2. **Codebase Analysis**: Analyzes current project structure and patterns
3. **Implementation Planning**: Creates detailed road maps tailored to current codebase
4. **Plan Validation**: `build-critic` reviews plan against spec requirements and internal criteria

**Quality Gate**: Configurable threshold via environment variables
**Output**: Detailed implementation roadmap with specific file modifications and sequences

### Loop 5: Code Implementation (`/build` - Phase 2)

**Participants**: `build-coder` ↔ `build-reviewer`

**Process Flow**:
1. **TDD Execution**: `build-coder` implements code following Test-Driven Development approach
2. **Quality Validation**: `build-reviewer` validates implementation quality, runs tests, checks compliance
3. **Plan Synchronization**: Assesses implementation alignment with strategic plan and technical specifications
4. **Completion or Reassignment**: Either completes with documentation or reassigns to appropriate upstream agent

**Quality Gate**: MCP Server-determined excellence standards for implementation
**Output**: Production-ready implementation with comprehensive validation

## Complete Command Flow Analysis

### `/plan` Command - Strategic Planning
```text
User Input: Natural language business requirements
    ↓
Dual-Loop Orchestration: Main Agent with MCP state management
├── Step 1: Initialize planning loop (MCP state setup)
├── Step 2: /plan-conversation command (conversational discovery)
├── Step 3: Main Agent strategic plan creation (template processing)
├── Steps 4-5: plan-critic evaluation + MCP plan refinement loop
├── Steps 6-9: plan-analyst extraction + analyst-critic + MCP analyst loop
└── Quality Gate: MCP Server-determined thresholds
    ↓
Output: Strategic plan document with dual validation scores
```

### `/plan-roadmap` Command - Implementation Roadmap
```text
Input: Strategic plan + optional phasing preferences
    ↓
Roadmap Generation Loop: plan-roadmap ↔ roadmap-critic
├── Step 1: Strategic plan context gathering and analysis
├── Step 2: Phase decomposition (3-7 implementable phases)
├── Step 3: Dependency mapping and sequencing
├── Step 4: Roadmap quality validation and refinement cycles
├── Step 5: Spec scaffolding for each phase
└── Quality Gate: MCP Server-determined thresholds (implementation readiness)
    ↓
Output: Implementation roadmap with phase-specific scaffolded specifications
```

### `/spec` Command - Technical Specification
```text
Input: Scaffolded specification from roadmap + technical focus area
    ↓
Enhanced Specification Phase:
├── Scaffolded spec analysis and phase context review
├── Archive scanning via research-advisor-archive-scan.sh
├── External research gap identification for phase-specific needs
└── Research prompt creation for missing knowledge
    ↓
Architecture Design Loop: spec-architect ↔ spec-critic
├── Complete detailed system architecture using selected technology stack
├── Research integration from archive and external sources
├── Platform-specific specification enhancement
└── Quality Gate: MCP Server-determined thresholds (production ready)
    ↓
Output: Complete technical specification with full implementation guidance
```

### `/build` Command - Implementation
```text
Input: Technical specification identifier
    ↓
Research Orchestration Phase:
├── Main Agent identifies external research needs from spec
├── Parallel research-synthesizer instances with specific prompts  
└── File path collection (not content reading)
    ↓
Build Planning Loop: build-planner ↔ build-critic
├── Documentation consumption and codebase analysis
├── Implementation plan creation
├── Plan validation against spec requirements
└── Quality Gate: Configurable threshold
    ↓
Build Implementation Loop: build-coder ↔ build-reviewer
├── TDD-based code implementation
├── Comprehensive quality validation (tests, types, compliance)
├── Plan synchronization assessment
└── Quality Gate: MCP Server-determined excellence standards
    ↓
Output: Production-ready implementation with platform integration
```

## Key Architectural Strengths

### 1. Separation of Concerns
- **Focused Responsibilities**: Each agent handles specific aspects without overlap
- **Clear Handoffs**: File-based communication between phases reduces coupling
- **Specialized Expertise**: Agents designed for specific roles (conversation, architecture, implementation, validation)
- **Service Boundary Pattern**: Domain logic separated from MCP protocol concerns with proper exception mapping

### 2. Quality-Driven Progression  
- **Progressive Standards**: MCP Server-managed quality thresholds with increasing rigor across workflow stages

*For detailed quality threshold configuration, see [MCP Loop Tools Implementation](MCP_LOOP_TOOLS_IMPLEMENTATION.md#phase-1-core-models-and-configuration)*
- **Automated Assessment**: LLM-based scoring with structured evaluation criteria
- **Human Fallback**: Intelligent escalation when automated refinement stagnates
- **FSDD Framework**: 12-point quality framework ensuring comprehensive evaluation

### 3. Research Integration Excellence
- **Archive-First Strategy**: Leverages existing knowledge before external searches
- **Parallel Efficiency**: Multiple research instances execute simultaneously
- **Structured Prompts**: Consistent research request formatting for reliability
- **Consumption Separation**: Research orchestration separate from consumption
- **Phase-Specific Research**: Roadmap-driven research focuses on phase requirements

### 4. Platform Flexibility
- **Markdown Foundation**: All content structured for portability across platforms
- **Tool Abstraction**: Platform-specific operations abstracted through template system
- **Conversion Capability**: Ability to switch between Linear/GitHub/Markdown
- **Storage Agnostic**: Business logic independent of storage platform choice
- **Spec Scaffolding**: Pre-structured specifications created in platform-appropriate format

### 5. Workflow Orchestration
- **MCP Server Coordination**: Centralized state management and decision logic
- **Template-Driven Generation**: Dynamic command and agent creation based on platform
- **Quality Gate Enforcement**: Systematic progression control through scoring thresholds
- **Scalable Extension**: Architecture supports new platforms and quality frameworks

### 6. FastMCP Error Handling Architecture
- see [ARCHITECTURE.md - Error Handling and Tracking](ARCHITECTURE.md#error-handling-and-tracking)

## MVP Scope Boundaries

### In Scope (Current MVP)
- **Five Refinement Loops**: All quality-driven feedback loops with critic agents (including roadmap loop)
- **Implementation Roadmap**: Phase-based development workflow with spec scaffolding
- **Research Orchestration**: Archive scanning + external research synthesis via Exa
- **Platform Integration**: Linear/GitHub/Markdown support with template system
- **Quality Framework**: FSDD gates with configurable thresholds via Pydantic-Settings
- **MCP Orchestration**: State management and workflow coordination
- **Template System**: Dynamic command and agent generation

### Deferred (Post-MVP)
- **Cross-Session Persistence**: Loop state and history tracking across sessions
- **Cross-Loop Context**: Shared context and memory between different refinement loops
- **Advanced Stagnation Detection**: Sophisticated algorithms beyond score plateauing
- **Platform Conversion Logic**: Automated conversion between different storage platforms
- **Performance Optimization**: Advanced caching and optimization strategies

## Technical Implementation Notes

*Comprehensive technical implementation details are documented in [MCP Loop Tools Implementation](MCP_LOOP_TOOLS_IMPLEMENTATION.md)*

### Key Implementation Aspects
- **Environment Configuration**: Quality thresholds managed via Pydantic-Settings
- **Session-Scoped State**: No cross-session persistence required for MVP
- **Simple Stagnation Detection**: 2 consecutive iterations below improvement threshold
- **Research Integration**: Archive scanning + external synthesis via Exa MCP Server

### File Organization Structure
- See [ARCHITECTURE.md - #### Target Project Directory Structure](ARCHITECTURE.md#target-project-directory-structure)

### Research Archive Structure
- Location: `~/.claude/best-practices/*.md`
- Scanning: Via `scripts/research-advisor-archive-scan.sh`
- Format: Structured markdown with topic headers and metadata

*For complete system architecture and platform integration details, see [System Architecture](ARCHITECTURE.md)*

## Conclusion

The Spec-Driven Workflow architecture represents a sophisticated yet maintainable approach to AI-assisted software development. Its strength lies in the clear separation of concerns, progressive quality enforcement, and intelligent research integration. The system balances automation with human oversight, providing fallback mechanisms when automated refinement reaches its limits.

The five-loop architecture ensures quality at every stage while maintaining efficiency through parallel processing and archive-first research strategies. The implementation roadmap bridge phase provides crucial structure between strategic planning and technical specification, enabling phase-based development with pre-scaffolded specifications. The platform-agnostic design enables teams to work within their preferred tools while maintaining consistent workflow quality.

This analysis serves as the foundation for understanding system behavior, planning implementations, and making architectural decisions during development and testing phases.
