# Architecture Guide

Complete architectural overview of the Spec-Driven Workflow MCP Server system.

## Overview

The Spec-Driven Workflow system is a sophisticated AI-powered development platform that orchestrates strategic planning, technical specification, and implementation workflows through MCP (Model Context Protocol) tools. It bridges human strategic thinking with AI-driven technical execution through a multi-layered architecture.

## System Architecture

### Core Components

```text
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code CLI                              │
│                      (Main Agent)                               │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │            Workflow Orchestrator                        │   │
│   │  • Command-driven task execution                        │   │
│   │  • Subagent coordination (Task calls)                   │   │
│   │  • MCP tool orchestration                               │   │
│   │  • Data passing between workflow stages                 │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ MCP Tools & Loop State Requests
┌─────────────────────▼───────────────────────────────────────────┐
│              Spec-Driven Workflow MCP Server                    │
│                    (State  Manager)                             │
│  ┌──────────────┬────────────────┬───────────────────────────┐  │
│  │ Loop State   │    Template    │       Platform            │  │
│  │ Management   │     System     │       Managers            │  │
│  │              │                │                           │  │
│  │ • Plan       │ • Dynamic      │ • Tool Mapping            │  │
│  │ • Spec       │   Commands     │   (Linear/GitHub/MD)      │  │
│  │ • Build Plan │ • Dynamic      │ • MCP Status Checking     │  │
│  │ • Build Code │   Agents       │   (claude mcp list)       │  │
│  └──────────────┴────────────────┴───────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Platform-Specific API Calls
┌─────────────────────▼───────────────────────────────────────────┐
│                  Platform Integrations                          │
│  ┌─────────────┬──────────────┬────────────────────────────────┐│
│  │   Linear    │   GitHub     │         Markdown               ││
│  │   Issues    │   Issues     │       File  System             ││
│  │   (MCP)     │   (MCP)      │       (Read/Write)             ││
│  └─────────────┴──────────────┴────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Scope Architecture

### User Scope (Global Configuration)

**Location**: `~/.claude/mcp_servers/`

**Purpose**: System-wide MCP server registration and availability

**Contents**:
- MCP server executable registration
- Global tool availability across all workspaces
- Template definitions (source of truth)

**What's NOT Here**:
- Generated commands or agents
- Project-specific configurations
- Platform selections

### Project Scope (Workspace-Specific)

**Location**: `project/.claude/`

**Purpose**: Project-specific workflow customization

#### Target Project Directory Structure
```text
project/
├── .claude/
│   ├── commands/
│   │   ├── plan.md                    # Static (always present)
│   │   ├── plan-conversation.md           # Static (conversation command)
│   │   ├── spec.md                    # Generated (platform-specific)
│   │   ├── build.md                   # Generated (platform-specific)
│   │   ├── spec-manager.md            # Generated (management interface)
│   │   └── [refinement commands]      # Generated (quality tools)
│   └── agents/
│       ├── plan-critic.md             # Static (always present)
│       ├── plan-analyst.md            # Static (always present)
│       ├── spec-architect.md          # Generated (technical design)
│       ├── spec-critic.md             # Generated (technical design)
│       ├── build-planner.md           # Generated (implementation planning)
│       ├── build-critic.md            # Generated (implementation quality)
│       ├── build-coder.md             # Generated (execution)
│       └── build-reviewer.md          # Generated (validation)
└── .specter/
    ├── config/
    │   ├── platform.json              # Platform choice and settings
    │   └── quality-gates.json         # FSDD thresholds
    ├── plans/                         # Markdown SpecManager Only
    ├── specs/                         # Markdown SpecManager Only
    └── scripts/
        ├── detect-packages.sh
        └── research-advisor-archive-scan.sh
```

**Workflow**:
1. **Platform Selection**: User chooses Linear/GitHub/Markdown via `/specter-spec-setup`
2. **Template Resolution**: System generates commands with platform-specific tools
3. **Agent Creation**: Specialized agents receive platform-appropriate tool sets
4. **Quality Configuration**: FSDD gates configured per project requirements

## Template System

### Template Architecture

The template system dynamically generates commands and agents based on platform selection:

```python
# Template Function Signature
def generate_template(
    platform_tools: dict[str, str],    # Resolved platform-specific tools
    platform_type: str,                # 'linear' | 'github' | 'markdown'
    platform_examples: dict,           # Usage examples and patterns
    **kwargs                           # Template-specific parameters
) -> str                               # Generated markdown content
```

### Template Types

#### 1. Command Templates
Generate user-facing commands that orchestrate workflows:

- **`plan_roadmap_command_template`**: Transforms strategic plans into phased implementation roadmaps
- **`spec_command_template`**: Converts strategic plans to technical specifications
- **`build_command_template`**: Creates implementation plans from specifications
- **`refine_spec_command_template`**: Quality improvement for specifications
- **`refine_build_command_template`**: Quality improvement for implementations
- **`validate_command_template`**: Quality gate validation
- **`spec_manager_command_template`**: Platform configuration interface
- **`spec_setup_command_template`**: Project setup and validation

#### 2. Agent Templates
Generate specialized AI agents with platform-specific capabilities:

- **`plan_analyst_template`**: Business requirement extraction (with iterative refinement)
- **`plan_critic_template`**: Strategic plan quality assessment
- **`plan_roadmap_template`**: Implementation roadmap generation and phase decomposition
- **`roadmap_critic_template`**: Implementation roadmap quality assessment
- **`spec_architect_template`**: Technical design and architecture (with iterative refinement)
- **`spec_critic_template`**: Technical specification quality assessment
- **`build_planner_template`**: Implementation planning (with iterative refinement)
- **`build_critic_template`**: Implementation plan quality assessment
- **`build_coder_template`**: Code execution and development (with iterative refinement)
- **`build_reviewer_template`**: Code implementation quality validation

### Platform Tool Resolution

The system maps abstract workflow operations to platform-specific tools:

```python
PLATFORM_TOOL_MAPPING = {
    'linear': {
        'create_spec_tool': 'mcp__linear-server__create_issue',
        'get_spec_tool': 'mcp__linear-server__get_issue',
        'add_comment_tool': 'mcp__linear-server__create_comment',
        'update_spec_tool': 'mcp__linear-server__update_issue',
        'list_comments_tool': 'mcp__linear-server__list_comments'
    },
    'github': {
        'create_spec_tool': 'mcp__github__create_issue',
        'get_spec_tool': 'mcp__github__get_issue',
        'add_comment_tool': 'mcp__github__create_comment',
        'update_spec_tool': 'mcp__github__update_issue',
        'list_comments_tool': 'mcp__github__list_comments'
    },
    'markdown': {
        'create_spec_tool': 'Write',
        'get_spec_tool': 'Read',
        'add_comment_tool': 'Edit',
        'update_spec_tool': 'Edit',
        'list_comments_tool': 'Read'
    }
}
```

## MCP Tool Orchestration - Production Implementation

### Production Workflow Coordination

The MCP server provides **30 production MCP tools** across 6 modules (1,264+ lines) that coordinate complex workflows:

#### Loop Management Tools (services/mcp/tools/loop_tools.py)
- **`initialize_refinement_loop`**: Initialize refinement loops for any workflow type
- **`decide_loop_next_action`**: Intelligent decision engine with stagnation detection
- **`get_loop_status`**: Monitor loop progress and iteration status
- **`list_active_loops`**: Retrieve all active loop states
- **`get_previous_objective_feedback`**: Context-aware feedback retrieval
- **`store_current_objective_feedback`**: Structured feedback storage
- **`get_loop_feedback_summary`**: Comprehensive feedback analysis
- **`get_loop_improvement_analysis`**: Progress tracking and trend analysis

#### Feedback Management Tools (services/mcp/tools/feedback_tools.py)
- **`store_critic_feedback`**: Universal structured feedback storage for all loop types
- **`get_feedback_history`**: Context-aware feedback history for critic consistency

#### Project Plan Tools (services/mcp/tools/project_plan_tools.py)
- **`create_project_plan`**: Create structured project plans from markdown
- **`store_project_plan`**: Associate project plans with specific loops
- **`get_project_plan_markdown`**: Retrieve formatted markdown output
- **`list_project_plans`**: Manage multiple project plans
- **`delete_project_plan`**: Clean project plan storage

#### Technical Specification Tools (services/mcp/tools/specter-spec_tools.py)
- **`create_technical_spec`**: Create structured technical specifications
- **`store_technical_spec`**: Associate specs with loops and projects
- **`get_technical_spec_markdown`**: Generate platform-specific outputs
- **`list_technical_specs`**: Manage specification lifecycle

#### Roadmap Management Tools (services/mcp/tools/roadmap_tools.py)
- **`create_roadmap`**: Create structured implementation roadmaps
- **`store_roadmap`**: Associate roadmaps with planning loops
- **`get_roadmap_markdown`**: Generate roadmap documentation

#### Build Plan Tools (services/mcp/tools/specter-build_plan_tools.py)
- **`create_build_plan`**: Create structured implementation plans
- **`store_build_plan`**: Associate build plans with specification loops
- **`get_build_plan_markdown`**: Generate implementation documentation

### Quality Framework Integration

#### FSDD (FastSpec-Driven Development) Quality Gates

**12-Point Quality Framework**:
1. **Clarity** - Requirements clearly stated
2. **Completeness** - All aspects covered
3. **Consistency** - No contradictions
4. **Feasibility** - Technically achievable
5. **Testability** - Verifiable outcomes
6. **Maintainability** - Long-term sustainability
7. **Scalability** - Growth accommodation
8. **Security** - Risk mitigation
9. **Performance** - Efficiency requirements
10. **Usability** - User experience quality
11. **Documentation** - Knowledge preservation
12. **Integration** - System compatibility

**Quality Thresholds**:
- **Plan Phase**: MCP Server-determined thresholds for strategic planning
- **Spec Phase**: MCP Server-determined thresholds for technical specifications
- **Build Plan Phase**: Configurable via environment variables
- **Build Code Phase**: MCP Server-determined excellence standards for implementation

*For detailed threshold configuration, see [MCP Loop Tools Implementation](MCP_LOOP_TOOLS_IMPLEMENTATION.md#phase-1-core-models-and-configuration)*

#### Refinement Loop Architecture

*Detailed loop implementation architecture and decision logic documented in [MCP Loop Tools Implementation](MCP_LOOP_TOOLS_IMPLEMENTATION.md)*

```text
┌─────────────┐    ┌─────────────────────────────────┐
│             │───▶│        Critic Agent             │
│   Initial   │    │  • FSDD Assessment              │
│   Content   │    │  • Quality Score Calculation    │
│             │    │  • Specific Feedback            │
└─────────────┘    └─────────────┬───────────────────┘
       ▲                         │
       │                         ▼
       │               ┌──────────────────────────┐
       │               │       Main Agent         │
       │               │   (via /refine-xxxxx)    │
       │               │  • Sends to MCP Server   │
       │               └──────────────────────────┘
       │                         │
       │                         ▼
       │                  ┌──────────────────────────┐
       │                  │     MCP Server           │
       │◀─────────────────│ • Loop State Management  │
       │  Next Action:    │ • Next Action Decisions  │
       │  • "refine"      └──────────────────────────┘
       │  • "complete"           │
       │  • "user-input"         │
┌─────────────┐                  │
│ Producer    │              ✓ Quality meets MCP criteria:  "complete"
│ Refines     │              ✗ Quality below MCP criteria:  "refine"
│ Content     │              ✗ Quality Stagnation:   "user-input"
└─────────────┘                (2 consecutive low improvements)
```

**Loop State Management**: Session-scoped with MCP-managed stagnation detection and threshold evaluation

## Platform Integration Patterns

### Linear Integration

**Specifications as Issues**:
- Strategic plans → Linear project documentation
- Technical specifications → Linear issues with detailed descriptions
- Implementation steps → Issue comments with task breakdowns
- Quality feedback → Issue updates and progress tracking

**Team Collaboration**:
- Assignee management for technical ownership
- Milestone tracking for delivery planning
- Label organization for specification categorization
- Comment threads for technical discussions

### GitHub Integration

**Specifications as Repository Assets**:
- Strategic plans → Repository documentation
- Technical specifications → GitHub issues with technical details
- Implementation steps → Issue comments with development tasks
- Code integration → Pull request linking with specifications

**Development Workflow**:
- Branch management aligned with specifications
- Pull request templates referencing specifications
- Issue templates for consistent specification structure
- Project boards for specification progress tracking

### Markdown Integration

**File-Based Specifications**:
- Strategic plans → `docs/specter-plans/[project-name].md`
- Technical specifications → `docs/specter-specs/[spec-name].md`
- Implementation plans → `docs/specter-builds/[build-name].md`
- Quality reports → `docs/quality/[assessment-name].md`

**Version Control Integration**:
- Git-based change tracking for all specifications
- Branch-based specification development
- Merge-based quality gate enforcement
- Tag-based release coordination

## Workflow Orchestration Patterns

### Multi-Stage Development Workflow

The workflow follows a **tightening and deepening of information** progression where each stage builds upon the previous with increasingly technical focus:

**ProjectPlan** → **FeatureRequirements** → **Roadmap** → **TechnicalSpec** → **BuildPlan**

#### Stage 1: Strategic Planning (`/specter-plan`)
**Input**: Natural language business requirements
**Process**: Dual-loop orchestration workflow
1. **Initialize Planning Loop**: MCP state management setup
2. **Conversational Requirements**: `/specter-plan-conversation` command guides discovery
3. **Strategic Plan Creation**: Main Agent processes conversation context using template
4. **Plan Quality Assessment**: `plan-critic` evaluates against FSDD framework
5. **Plan Refinement Loop**: MCP manages plan refinement iterations
6. **Initialize Analyst Loop**: Second validation loop setup
7. **Objective Extraction**: `plan-analyst` structures business objectives
8. **Analyst Quality Assessment**: `analyst-critic` validates extraction quality
9. **Analyst Validation Loop**: MCP manages analyst refinement iterations
**Quality Gate**: MCP Server-determined thresholds for strategic planning
**Output**: Big-picture overview providing understanding and context on what we're building and why

#### Stage 2: Feature Requirements (`/feature-requirements`)
**Input**: Strategic plan document
**Process**: Technical translation workflow
1. **Business Context Analysis**: Extract user workflows and business intent from strategic plan
2. **Constraint Definition**: Identify performance, scalability, compliance, and security requirements
3. **Success Criteria Definition**: Establish clear acceptance criteria and measurable outcomes
4. **Integration Context Mapping**: Document integration points and external dependencies
5. **Technical Assumptions Documentation**: Capture assumptions that will guide technical decisions
**Quality Gate**: Requirements completeness and clarity validation
**Output**: Technical translation of business needs defining intent and constraints on what is to be built

#### Stage 3: Implementation Roadmap (`/specter-roadmap`)
**Input**: Feature requirements + optional phasing preferences
**Process**: Quality-driven roadmap decomposition workflow
1. **Requirements Analysis**: Extract technical constraints and dependencies from feature requirements
2. **Phase Decomposition**: Break down implementation into 3-7 discrete phases based on constraints
3. **Dependency Mapping**: Establish logical phase sequencing ensuring requirements are met
4. **Roadmap Quality Loop**: MCP manages roadmap refinement iterations
   - `roadmap` agent creates phase breakdown
   - `roadmap-critic` evaluates phase scoping and dependencies
5. **Spec Scaffolding**: Create initial technical specifications for each phase
6. **Platform Integration**: Store roadmap and scaffolded specs in chosen platform
**Quality Gate**: MCP Server-determined thresholds for roadmap completeness
**Output**: High-level implementation roadmap organizing Specs in step-by-step manner with phase foundations

#### Stage 4: Technical Specification (`/specter-spec`)
**Input**: Scaffolded specification from roadmap + technical focus area
**Process**: Enhanced specification workflow with pre-structured context
1. **Scaffolded Spec Analysis**: Review phase-specific specification template with requirements context
2. **Research Integration**: Incorporate archive and external research findings for constraints
3. **Technical Architecture Design**: Complete detailed system architecture addressing requirements
   - Refinement Loop: `spec-architect` ↔ `spec-critic`
4. **Requirements Validation**: Ensure architecture meets feature requirements and constraints
5. **FSDD Quality Gate Validation**: Ensure specification meets production readiness criteria
**Quality Gate**: MCP Server-determined thresholds for technical specifications
**Output**: System Architecture Design - first Engineering-forward step creating Project System Design and identifying research needs

#### Stage 5: Build Planning (`/specter-build`)
**Input**: Technical specification identifier
**Process**: Detailed implementation planning workflow
- **Technology Environment Discovery**: Detect current project technology stack
- **Research Requirements Orchestration**: Gather implementation guidance
  - The Research Requirements section in the spec will have a list of items that can be either:
    - Read: A path to a previously existing document
    - Synthesize: A prompt to provide the `research-synthesizer` agent
      - The `research-synthesizer` agent will generate a new document and return the path to the new document
  - The paths to all documents will be provided to the `build-planner` agent to be read and used to inform the implementation plan
- **Implementation Planning Loop** (refine-build-plan): Create high-quality plan with planning/critic loop
  - Agents:
    - `build-planner` agent (creates + refines based on feedback)
    - `build-critic` agent (evaluates quality + provides feedback)
- **Implementation/Verification Loop** (refine-build-code): Generate verified code with coder/reviewer loop
  - Agents:
    - `build-coder` agent (creates + refines based on feedback)
    - `build-reviewer` agent (evaluates implementation + provides feedback)
- **Platform Integration & Completion**: Document results and update tickets
**Quality Gate**: Implementation readiness and code quality standards
**Output**: Detailed implementation plan taking Research and creating very detailed plan for how the Spec will be implemented using specific patterns and best-practices

**Key Architecture Improvements**:
- **Roadmap Bridge Phase**: Added implementation roadmap generation to bridge strategic planning and technical specification, improving phase-based development workflow
- **Spec Scaffolding**: Pre-structured specifications provide clear templates and context for technical specification completion
- **Streamlined Implementation**: Eliminated redundant refinement agents in build phase, resulting in cleaner separation between planning quality and implementation quality

### Quality-Driven Refinement

**Automatic Quality Assessment**:
- Every workflow output evaluated against FSDD gates
- Scores below threshold trigger refinement loops
- Iterative improvement until quality standards met

**Human-AI Collaboration**:
- AI handles technical analysis and generation
- Human provides strategic direction and approval
- System preserves context across refinement cycles

## Extension and Customization

### Adding New Platforms

1. **Create Spec Manager**: Implement `SpecManager` interface
2. **Define Tool Mapping**: Map workflow operations to platform tools
3. **Create Templates**: Customize commands/agents for platform capabilities
4. **Add Validation**: Implement platform connectivity and authentication checks
5. **Update Registry**: Register platform in configuration system

### Custom Quality Gates

1. **Define Assessment Criteria**: Create domain-specific quality metrics
2. **Implement Critic Agents**: Build specialized quality evaluation agents
3. **Configure Thresholds**: Set appropriate quality gate thresholds
4. **Create Refinement Strategies**: Define improvement approaches per criteria

### Workflow Extensions

1. **Create MCP Tools**: Implement workflow-specific orchestration functions
2. **Design Templates**: Generate commands and agents for new workflows
3. **Define Quality Framework**: Establish quality gates for new workflow types
4. **Integrate Platforms**: Ensure new workflows work across all supported platforms

## Performance and Scalability

### Workflow Execution
- **Async Operations**: All I/O operations use async/await patterns
- **Resource Management**: Automatic cleanup of temporary resources

## Monitoring and Observability

### Workflow Metrics
- **Success Rates**: Track completion rates for each workflow stage
- **Quality Scores**: Monitor FSDD quality gate performance over time
- **Platform Health**: Track platform integration reliability

### Error Handling and Tracking
- **FastMCP Integration**: Built-in ErrorHandlingMiddleware for consistent error processing
- **Service Boundary Mapping**: Domain exceptions mapped to FastMCP ToolError at service layer
- **Context-Based Communication**: Real-time error logging to MCP clients via Context parameter
- **Middleware-Driven Processing**: Centralized error handling through FastMCP middleware pipeline
- **User Feedback**: Clear, actionable error messages with validation feedback
- **Diagnostic Tools**: Built-in tools for troubleshooting common issues

## Development and Maintenance

### Testing Strategy
- **Unit Tests**: Individual component testing with mocking
- **Integration Tests**: Platform integration and workflow testing

### Documentation Standards
- **Architecture Documentation**: Detailed system design and patterns
- **User Guides**: Installation, migration, and troubleshooting guides
- **API Documentation**: MCP tool interfaces and usage patterns

## Conclusion

The Spec-Driven Workflow architecture has been **successfully implemented** as a production-ready foundation for AI-powered software development workflows. The system's separation of concerns between user/project scopes, platform-agnostic template system, and quality-driven approach enables teams to maintain high development standards while leveraging AI capabilities for enhanced productivity.

**Production Achievements:**
- ✅ **30 MCP Tools**: Comprehensive workflow orchestration across 6 modules (1,264+ lines)
- ✅ **Structured Data Models**: All 7 document models with sophisticated MCPModel base class
- ✅ **Advanced Loop Management**: Sophisticated refinement loops with stagnation detection
- ✅ **Production Server**: FastMCP with comprehensive middleware and error handling
- ✅ **Quality Framework**: FSDD integration with structured feedback tracking

The system's modular design has proven successful in practice, enabling extensible platform support and workflow patterns without disrupting core functionality. The production implementation provides a robust foundation for evolving development practices with proven reliability and comprehensive feature coverage.
