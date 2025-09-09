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

**Target Project Directory Structure**:
```text
project/
├── .claude/
│   ├── commands/
│   │   ├── plan.md                    # Static (always present)
│   │   ├── spec.md                    # Generated (platform-specific)
│   │   ├── build.md                   # Generated (platform-specific)
│   │   ├── spec-manager.md            # Generated (management interface)
│   │   └── [refinement commands]      # Generated (quality tools)
│   └── agents/
│       ├── plan-generator.md          # Static (always present)
│       ├── plan-critic.md             # Static (always present)
│       ├── plan-analyst.md            # Static (always present)
│       ├── spec-architect.md          # Generated (technical design)
│       ├── spec-critic.md             # Generated (technical design)
│       ├── build-planner.md           # Generated (implementation planning)
│       ├── build-critic.md            # Generated (implementation quality)
│       ├── build-coder.md             # Generated (execution)
│       └── build-verifier.md          # Generated (validation)
└── .fsdd/
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
1. **Platform Selection**: User chooses Linear/GitHub/Markdown via `/spec-setup`
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
- **`spec_architect_template`**: Technical design and architecture (with iterative refinement)
- **`spec_critic_template`**: Technical specification quality assessment
- **`build_planner_template`**: Implementation planning (with iterative refinement)
- **`build_critic_template`**: Implementation plan quality assessment
- **`build_coder_template`**: Code execution and development (with iterative refinement)
- **`build_verifier_template`**: Code implementation quality validation

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

## MCP Tool Orchestration

### Workflow Coordination

The MCP server provides high-level orchestration tools that coordinate complex workflows:

#### Strategic Planning Tools
- **`execute_plan_workflow`**: Conversational requirements discovery
- **`assess_content_fssd`**: Quality gate evaluation for plans

#### Technical Specification Tools
- **`execute_spec_workflow`**: Plan-to-specification conversion
- **`render_agent_dynamic`**: Platform-specific agent generation

#### Implementation Planning Tools
- **`execute_build_workflow`**: Specification-to-implementation conversion
- **`execute_refinement_loop`**: Quality-driven iterative improvement

#### System Management Tools
- **`get_project_config`**: Project state inspection
- **`configure_project_spec_manager`**: Platform selection and setup
- **`configure_markdown_directories`**: Markdown platform customization

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
- **Minimum Score**: 0.70 (70%) - Basic acceptance
- **Production Ready**: 0.85 (85%) - Release quality
- **Excellence**: 0.95 (95%) - Best practice standard

#### Refinement Loop Architecture

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
│ Planner     │              ✓ Quality ≥ 0.85:     "complete"
│ Refines     │              ✗ Quality < 0.85:     "refine"
│ Content     │              ✗ Quality Stagnation: "user-input"
└─────────────┘                (or max loop iterations)
```

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
- Strategic plans → `docs/plans/[project-name].md`
- Technical specifications → `docs/specs/[spec-name].md`
- Implementation plans → `docs/builds/[build-name].md`
- Quality reports → `docs/quality/[assessment-name].md`

**Version Control Integration**:
- Git-based change tracking for all specifications
- Branch-based specification development
- Merge-based quality gate enforcement
- Tag-based release coordination

## Workflow Orchestration Patterns

### Multi-Stage Development Workflow

#### Stage 1: Strategic Planning (`/plan`)
**Input**: Natural language business requirements
**Process**:
1. Conversational requirements analysis
    a. User Conversational Refinement Loop
        - `plan-generator` agent
        - `plan-critic` agent
2. Business objective extraction
    a. `plan-analyst` agent (rename for clarity)
3. Constraint identification
4. Technology stack consideration
**Output**: Strategic plan document with clear objectives

#### Stage 2: Technical Specification (`/spec`)
**Input**: Strategic plan + technical focus area
**Process**:
1. Plan analysis and requirement extraction
2. Technical architecture design
    a. Refinement Loop
        - `spec-architect` agent
        - `spec-critic` agent
3. Platform-specific specification creation
4. FSDD quality gate validation
**Output**: Detailed technical specification in chosen platform

#### Stage 3: Implementation Workflow (`/build`)
**Input**: Technical specification identifier
**Process**: Streamlined workflow with 2 meaningful quality loops
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
- **Implementation/Verification Loop** (refine-build-code): Generate verified code with coder/verifier loop
  - Agents:
    - `build-coder` agent (creates + refines based on feedback)
    - `build-verifier` agent (evaluates implementation + provides feedback)
- **Platform Integration & Completion**: Document results and update tickets
**Output**: Complete implementation with comprehensive validation and platform integration

**Key Architecture Improvement**: Eliminated redundant refinement agents and combined planning/quality assessment into a single meaningful loop, resulting in cleaner separation of concerns between planning quality and implementation quality.

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

### Error Tracking
- **Detailed Logging**: Comprehensive error logging with context preservation
- **User Feedback**: Clear error messages with actionable resolution steps
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

The Spec-Driven Workflow architecture provides a flexible, extensible foundation for AI-powered software development workflows. Its separation of concerns between user/project scopes, platform-agnostic template system, and quality-driven approach enables teams to maintain high development standards while leveraging AI capabilities for enhanced productivity.

The system's modular design ensures that new platforms, quality frameworks, and workflow patterns can be integrated without disrupting existing functionality, providing a sustainable foundation for evolving development practices.
