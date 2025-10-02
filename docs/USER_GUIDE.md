# Specter User Guide

Complete guide to using Specter for AI-driven specification-based development.

## What is Specter?

Specter is a **meta MCP server** that generates platform-specific workflow tools for AI-driven development. It creates custom Claude Code commands and agents tailored to your project management platform (Linear, GitHub, or local Markdown files).

### Key Benefits

- **Platform flexibility** - Work with Linear issues, GitHub issues, or local Markdown files
- **Automated setup** - Generate complete workflow tools with a single command
- **Type-safe integration** - Platform-specific tools properly configured for your environment
- **Refinement loops** - Quality-driven development with critic agents and iterative improvement

## Getting Started

### Prerequisites

- **Claude Code CLI** installed and configured
- **Platform MCP Server** (Linear or GitHub) if using external platforms

**For local installation:**
- **uv** (Python version and package manager)
- **Python 3.12+**
- **Unix-like operating system** (Linux, macOS, or Windows Subsystem for Linux)

**For containerized MCP servers:**
- **Docker** (Linux)
- **Docker Desktop** (macOS, Windows, Windows Subsystem for Linux)

### Installation

Choose one of three installation methods:

#### Method 1: Remote Installation (Recommended)

Install directly from GitHub:

```bash
# Install with default platform (markdown)
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash

# Install with specific platform
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash -s -- linear

# Install to specific directory
curl -fsSL https://raw.githubusercontent.com/mmcclatchy/spec-driven-development/main/scripts/install-specter.sh | bash -s -- --platform github --path ~/my-project
```

#### Method 2: Local Installation

If you have the Specter repository cloned:

```bash
# From current directory
./scripts/install-specter.sh

# With specific platform
./scripts/install-specter.sh linear

# To specific directory
./scripts/install-specter.sh --platform linear --path ~/my-project
```

#### Method 3: Bootstrap via Claude Code

Ask Claude Code to bootstrap Specter files:

```text
Install the Specter bootstrap files for this project
```

This will:
1. Claude Code calls the `get_bootstrap_files` MCP tool internally
2. Writes the `specter-setup.md` command to `.claude/commands/`
3. You then run `/specter-setup [platform]` to complete installation

**When to use:** Alternative to the installation script - useful when you prefer Claude to handle file creation or when the script isn't accessible.

### Project Setup

After installation, set up your project:

1. **Navigate to your project**:
   ```bash
   cd /path/to/your/project
   claude
   ```

2. **Run setup command**:
   ```text
   /specter-setup
   ```

   Or specify platform directly:
   ```text
   /specter-setup linear
   ```

3. **Verify MCP server availability**:
   ```text
   /mcp list
   ```

### What Gets Created

After setup, your project will have:

```text
project/
├── .claude/
│   ├── commands/
│   │   ├── specter-plan.md
│   │   ├── specter-spec.md
│   │   ├── specter-build.md
│   │   ├── specter-roadmap.md
│   │   └── specter-plan-conversation.md
│   └── agents/
│       ├── plan-analyst.md
│       ├── plan-critic.md
│       ├── analyst-critic.md
│       ├── plan-roadmap.md
│       ├── roadmap-critic.md
│       ├── create-spec.md
│       ├── spec-architect.md (future)
│       ├── spec-critic.md (future)
│       ├── build-planner.md (future)
│       ├── build-critic.md (future)
│       ├── build-coder.md (future)
│       └── build-reviewer.md (future)
└── .specter/
    ├── config/
    │   └── platform.json
    └── projects/ (markdown only)
```

## Platform Selection

### Choosing Your Platform

Specter supports three platforms with different capabilities:

#### Linear Platform

**Best for:** Teams using Linear for project management

**Capabilities:**
- ✅ Issue tracking
- ✅ Projects
- ✅ Comments
- ✅ Labels
- ✅ Cycles (sprint planning)
- ✅ Real-time collaboration
- ✅ External integration

**Requirements:**
- Linear MCP server configured in Claude Code
- Linear API access

**Workflow:**
- Specs created as Linear issues
- Plans stored as Linear projects
- Comments for feedback and discussion

#### GitHub Platform

**Best for:** Teams using GitHub for project management

**Capabilities:**
- ✅ Issue tracking
- ✅ Projects (boards)
- ✅ Comments
- ✅ Labels
- ✅ Milestones
- ❌ Real-time collaboration
- ✅ External integration

**Requirements:**
- GitHub MCP server configured in Claude Code
- GitHub API access

**Workflow:**
- Specs created as GitHub issues
- Plans stored as GitHub project boards
- Comments for feedback

#### Markdown Platform

**Best for:** Solo developers or teams preferring local files

**Capabilities:**
- ✅ Issue tracking (via structured files)
- ✅ Projects (via markdown files)
- ✅ Comments (via markdown sections)
- ❌ Labels
- ❌ Real-time collaboration
- ❌ External integration

**Requirements:**
- None (uses built-in Claude Code tools)

**Workflow:**
- Specs stored as markdown files in `.specter/projects/[project-name]/specter-specs/`
- Plans stored as markdown files
- Git-friendly version control

### Platform Recommendations

**Choose Linear if:**
- Your team uses Linear for project management
- You need real-time collaboration
- You want native Linear integration

**Choose GitHub if:**
- Your team uses GitHub issues
- You want project board integration
- You need milestone tracking

**Choose Markdown if:**
- You're working solo
- You prefer local files
- You want Git-based version control
- You don't need external platform integration

## Available Commands

### `/specter-plan`

**Purpose:** Create strategic project plans through interactive discovery

**Workflow:**
1. Uses `/specter-plan-conversation` for natural language requirements gathering
2. Creates strategic plan document
3. Evaluates plan quality with plan-critic agent
4. Refines through iterative improvement loops
5. Extracts business objectives with plan-analyst agent
6. Validates extraction with analyst-critic agent

**When to use:**
- Starting a new project or feature
- Need to understand business objectives
- Want structured strategic planning

**Example:**
```text
User: /specter-plan

Claude: I'll help you create a strategic plan. Let me start by understanding your goals.

[Interactive conversation begins...]
```

### `/specter-plan-conversation`

**Purpose:** Interactive conversation for requirements gathering

**Workflow:**
1. Asks clarifying questions about project goals
2. Explores business objectives and constraints
3. Gathers context for strategic planning
4. Provides input for plan creation

**When to use:**
- This is not to be used by end-users
- This command is used as a subcommand of `/specter-plan`

### `/specter-roadmap`

**Purpose:** Generate multi-phase implementation roadmaps

**Workflow:**
1. Analyzes project scope and complexity
2. Creates phase-based implementation roadmap
3. Evaluates roadmap with roadmap-critic agent
4. Generates initial specifications for each phase
5. Refines through iterative improvement

**When to use:**
- Starting large, complex projects
- Need phase-based planning
- Want to break work into manageable chunks

**Example:**
```text
User: /specter-roadmap [project-name]

Claude: I'll create a multi-phase implementation roadmap.
[Generates roadmap with phases, milestones, and initial specs]
```

### `/specter-spec`

**Purpose:** Convert strategic plans into detailed technical specifications

**Workflow:**
1. Retrieves existing strategic plan
2. Creates technical specification using spec-architect agent
3. Evaluates spec quality with spec-critic agent
4. Refines through iterative improvement
5. Creates spec in your platform (Linear issue, GitHub issue, or Markdown file)

**When to use:**
- After completing strategic planning
- Need detailed technical specifications
- Ready to break down implementation approach

**Example:**
```text
User: /specter-spec [spec-name]

Claude: I'll create a technical specification from your strategic plan.
[Generates spec with technical details, architecture, and implementation approach]
```

### `/specter-build`

**Purpose:** Implement specifications with automated code generation

**Workflow:**
1. Retrieves technical specification
2. Creates build plan with build-planner agent
3. Evaluates plan with build-critic agent
4. Generates code with build-coder agent
5. Reviews code with build-reviewer agent
6. Refines through quality loops

**When to use:**
- After completing technical specifications
- Ready to implement features
- Want automated code generation with quality checks

**Example:**
```text
User: /specter-build [spec-name]

Claude: I'll implement the specification with automated code generation.
[Creates build plan, generates code, reviews quality]
```

## Workflow Examples

### Example 1: New Feature Development

**Scenario:** Adding user authentication to an application

```text
1. Strategic Planning:
   User: /specter-plan [project-name]
   [Interactive conversation about authentication needs]
   → Creates strategic plan with business objectives

2. Technical Specification:
   User: /specter-spec [spec-name]
   → Generates technical spec with architecture details
   → Creates Linear issue (or GitHub issue, or markdown file)

3. Implementation:
   User: /specter-build [spec-name]
   → Creates build plan with implementation steps
   → Generates authentication code
   → Reviews code quality
   → Implements feature
```

### Example 2: Large Project Roadmap

**Scenario:** Building a complete SaaS application

```text
1. Strategic Planning:
   User: /specter-plan [project-name]
   → Creates strategic plan for entire SaaS application
   → Defines business objectives and high-level requirements

2. Roadmap Creation:
   User: /specter-roadmap [project-name]
   → Breaks down strategic plan into implementation phases:
     - Phase 1: User authentication
     - Phase 2: Core features
     - Phase 3: Payment integration
     - Phase 4: Analytics dashboard
   → Creates initial specs for each phase automatically

3. Phase Implementation:
   For each phase/spec created by roadmap:
   User: /specter-spec [spec-name] (to elaborate technical details)
   User: /specter-build [spec-name] (to implement the phase)
```

### Example 3: Requirements Discovery

**Scenario:** Unclear project requirements

```text
1. Strategic Planning with Conversational Discovery:
   User: /specter-plan [project-name]
   Claude: (runs /specter-plan-conversation internally)
   Claude: What problem are you trying to solve?
   User: I want users to collaborate in real-time
   Claude: What kind of collaboration? Document editing? Chat? Screen sharing?
   [Conversation continues to clarify requirements]
   → Claude creates strategic plan based on conversation
   → Evaluates and refines plan through quality loops

2. Continue with roadmap or spec creation...
```

## Quality & Refinement Loops

Specter uses two types of quality loops:

### 1. Human-in-the-Loop with Quality Validation

**Used by:** `/specter-plan`

**Process:**
1. **Conversation:** `/specter-plan-conversation` conducts interactive Q&A to gather requirements
2. **Generation:** Creates strategic plan from conversation context
3. **Quality Check:** `plan-critic` evaluates the plan and provides quality score
4. **Human Review:** User sees quality score and decides: continue conversation, refine plan, or accept
5. **Analysis:** `plan-analyst` extracts structured business objectives
6. **Validation:** `analyst-critic` validates the extraction through MCP refinement loop
7. **Completion:** Final validated strategic plan

This is a **hybrid approach** - conversational gathering with automated quality validation and user decision points.

### 2. Automated Refinement Loops (MCP-Driven)

**Used by:** `/specter-roadmap`, `/specter-spec`, `/specter-build`

**Process:**
1. **Generation:** A generative agent creates content (roadmap, spec, build plan, code)
2. **Evaluation:** A critic agent scores quality (0-100)
3. **Decision:** MCP server determines next action:
   - **High score** → Proceed to next phase
   - **Improving score** → Refine with feedback
   - **Stagnation** → Request user input

### Critic Agents

**For Human-in-the-Loop (`/specter-plan`):**

**plan-critic:**
- Evaluates strategic plans after conversational gathering
- Provides quality score for user decision-making
- No automated refinement loop - user decides next action

**analyst-critic:**
- Validates business objective extraction
- Uses MCP-driven automated refinement loop
- Ensures completeness and accuracy of analysis

**For Automated Loops (`/specter-roadmap`, `/specter-spec`, `/specter-build`):**

**roadmap-critic:**
- Evaluates implementation roadmaps
- Checks phase breakdown and sizing
- Validates dependencies and ordering

**spec-critic:**
- Evaluates technical specifications
- Checks architecture design decisions
- Validates implementation approach

**build-critic:**
- Evaluates build plans
- Checks implementation steps
- Validates technology choices

**build-reviewer:**
- Reviews generated code
- Checks code quality and best practices
- Validates implementation correctness

### Quality Thresholds

Quality scores determine progression:

- **80-100:** Excellent quality, proceed
- **60-79:** Good quality, minor refinements
- **40-59:** Needs improvement, iterate
- **0-39:** Significant issues, major refinement

**Stagnation detection:**
- No improvement over successive iterations
- Max iterations reached (configurable)
- System requests user input

## Platform-Specific Workflows

### Linear Workflow

**Plan Storage:**
```text
1. /specter-plan creates strategic plan
2. Stored as Linear project
3. Issues linked to project
4. Cycles used for sprint planning
```

**Spec Creation:**
```text
1. /specter-spec creates Linear issue
2. Issue contains technical specification
3. Comments added for feedback
4. Labels applied for categorization
5. Project assigned for tracking
```

### GitHub Workflow

**Plan Storage:**
```text
1. /specter-plan creates strategic plan
2. Stored as GitHub project board
3. Issues linked to project
4. Milestones for phases
```

**Spec Creation:**
```text
1. /specter-spec creates GitHub issue
2. Issue contains technical specification
3. Comments for feedback
4. Labels for categorization
5. Milestone for tracking
```

### Markdown Workflow

**Plan Storage:**
```text
1. /specter-plan creates markdown file
2. Stored in .specter/projects/[project-name]/project_plan.md
3. Structured sections
4. Git commit for history
```

**Spec Creation:**
```text
1. /specter-spec creates markdown file
2. Stored in .specter/projects/[project-name]/specter-specs/
3. Structured markdown format
4. Git-friendly version control
5. Comments as markdown sections
```

## Configuration

### Platform Configuration

Platform selection stored in `.specter/config/platform.json`:

```json
{
  "platform": "linear",
  "created_at": "2025-10-01T12:00:00.000000",
  "version": "1.0",
  "bootstrap": true
}
```

### Changing Platforms

To switch platforms, simply re-run setup with the new platform:

```text
/specter-setup [new-platform]
```

The setup command will:
- Update `.specter/config/platform.json` with new platform
- Regenerate all commands in `.claude/commands/` with new platform-specific tools
- Regenerate all agents in `.claude/agents/` with updated configurations

**Note:** Existing work (plans, specs) won't automatically migrate between platforms. You'll need to manually recreate them in the new platform if needed.
- There are plans to add a migration tool in the future to help with this.

## Troubleshooting

### MCP Server Not Found

**Problem:** Platform MCP server not available

**Solution:**
```text
1. Check MCP server status:
   /mcp list

2. Install required MCP server:
   - Linear: Follow Linear MCP server setup docs
   - GitHub: Follow GitHub MCP server setup docs
   - Markdown: No external server required

3. Restart Claude Code after MCP server installation
```

### Commands Not Found

**Problem:** Specter commands don't appear

**Solution:**
```text
1. Verify setup completed:
   ls .claude/commands/specter-*

2. If missing, re-run setup:
   /specter-setup [platform]

3. Restart Claude Code to reload commands
```

### Platform Tools Not Working

**Problem:** Platform-specific operations fail

**Solution:**
```text
1. Verify platform configuration:
   cat .specter/config/platform.json

2. Check MCP server permissions:
   /mcp list
   [Verify Linear/GitHub MCP server has proper API access]

3. For Markdown platform, verify directory exists:
   ls .specter/projects/
```

### Refinement Loop Stuck

**Problem:** Quality scores not improving

**Solution:**
```text
1. System will auto-escalate after max iterations
2. Provide additional context when prompted
3. Check quality thresholds in critic feedback
4. Consider manual refinement if automated process stagnates
```

## Best Practices

### Strategic Planning

**Do:**
- Use `/specter-plan` which will automatically guide you through conversational discovery
- Be specific about business objectives when answering questions
- Include constraints and limitations
- Provide context about users and use cases

**Don't:**
- Skip strategic planning for large features
- Mix technical details with business objectives
- Rush through refinement loops
- Call `/specter-plan-conversation` directly (it's used internally by `/specter-plan`)

### Roadmap Planning

**Do:**
- Use `/specter-roadmap` for projects that benefit from phased decomposition
- Let the roadmap agent choose the phasing strategy that fits your project:
  - **Feature-based** for most application development (complete capabilities)
  - **Technical-layer** for infrastructure or platform projects (foundational components)
  - **Incremental-complexity** when requirements are evolving (MVP → enhancements)
  - **Risk-based** for innovative projects (tackle unknowns first)
- Ensure each phase delivers something testable and meaningful
- Consider dependencies between phases
- Define clear milestones for each phase

**Don't:**
- Force a specific number of phases without considering project needs
- Create phases that are too granular (sub-tasks, not complete features)
- Create phases that are too large (multiple independent features bundled)
- Skip phase validation before implementation
- Ignore phase dependencies

### Technical Specifications

**Do:**
- Reference strategic plan
- Include architecture decisions
- Document technology choices
- Consider security and performance

**Don't:**
- Skip spec creation before implementation
- Mix specs with code
- Ignore critic feedback

### Implementation

**Do:**
- Follow build plan structure
- Review generated code carefully
- Run tests after implementation
- Address quality feedback

**Don't:**
- Skip build planning
- Ignore code review feedback
- Bypass quality gates

### Platform Selection

**Do:**
- Choose platform based on team workflow
- Verify MCP server availability before setup
- Test platform integration after setup

**Don't:**
- Switch platforms mid-project
- Use external platforms without MCP servers
- Ignore platform capabilities

## Advanced Usage

### Custom Quality Thresholds

Configure refinement loop thresholds:

```bash
# Set via environment variables (future feature)
export SPECTER_PLAN_THRESHOLD=80
export SPECTER_SPEC_THRESHOLD=85
export SPECTER_BUILD_THRESHOLD=90
```

### Multi-Phase Projects

For complex projects:

1. Use `/specter-roadmap` for overall structure
2. Create separate strategic plans per phase
3. Generate specifications for each phase
4. Implement phases sequentially

### Collaborative Workflows

**With Linear:**
- Team members comment on Linear issues
- Assign issues to team members
- Track progress in cycles
- Use labels for organization

**With GitHub:**
- Team collaboration via issue comments
- Assign issues to team members
- Track in project boards
- Use milestones for releases

**With Markdown:**
- Share files via Git repository
- Review via pull requests
- Track changes with Git history
- Collaborate async

## Getting Help

### Documentation

- **Architecture:** See `docs/ARCHITECTURE.md` for system design
- **Analysis:** See `docs/ARCHITECTURE_ANALYSIS.md` for implementation details
- **Development:** See `docs/ARCHITECTURAL_REALIGNMENT.md` for technical implementation

### Common Questions

**Q: Can I use Specter without an external platform?**
A: Yes, use the Markdown platform for local file-based workflows.

**Q: Can I switch platforms after setup?**
A: Yes, but you'll need to delete configuration and re-run setup. Existing work won't automatically migrate.

**Q: Do I need all the generated agents?**
A: Yes, agents work together in refinement loops. Removing agents may break workflows.

**Q: Can I customize the templates?**
A: Templates are generated fresh each time. Customization requires modifying the Specter MCP server code.

**Q: How do I update Specter?**
A: Pull latest changes from repository and re-run installation script. Existing projects won't be affected.

## Next Steps

1. **Install Specter** using one of the installation methods
2. **Set up your project** with `/specter-setup`
3. **Start planning** with `/specter-plan`
4. **Breakdown the plan into specifications** with `/specter-roadmap`
5. **Design and Refine specifications** with `/specter-spec`
6. **Implement features** with `/specter-build`
