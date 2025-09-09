def generate_refine_spec_command_template(refinement_loop_tool: str, parse_command_tool: str) -> str:
    return f"""---
allowed-tools:
  - Read(docs/strategic-plans/)
  - Bash(~/.claude/scripts/detect-packages.sh)
  - {refinement_loop_tool}
  - {parse_command_tool}
  - Write(docs/strategic-plans/)
argument-hint: [spec-name]
description: Iteratively improve technical specifications using RefinementLoop tool with FSDD compliance
---

You are executing the `/refine-spec` command to iteratively improve technical specifications through critic/refiner loops.

## Command Execution Flow

### 1. Technology Context Discovery
Execute the package detection script to understand the current project technology stack:
```bash
~/.claude/scripts/detect-packages.sh
```
Parse the output to identify:
- Current technologies and versions
- Package managers in use
- Development environment configuration

### 2. Strategic Plan Analysis
Read the strategic plan from `docs/strategic-plans/${{PLAN_NAME}}.md`:
- Extract current content and structure
- Identify existing technology references
- Note any gaps in technology alignment

### 3. RefinementLoop Tool Execution

Use the refinement tools to orchestrate the critic/refiner loop:

**Option 1: Direct refinement tool call (recommended)**
```python
# Execute refinement loop with technology-aware agents
result = await {refinement_loop_tool}(
    critic_agent='spec-critic',
    refiner_agent='spec-refiner',
    content=current_spec_content,
    content_type='technical_specification',
    quality_threshold=0.85,  # FSDD compliance threshold
    max_iterations=3,        # Prevent infinite loops
    
    # Pass technology context to agents via execution context
    technology_context=detected_packages
)
```

**Option 2: Command parsing approach**
```python
# Parse and execute refinement command
await {parse_command_tool}(
    command="refine-spec",
    target_content=current_spec_content,
    quality_framework="fssd",
    technology_context=detected_packages
)
```

### 4. Content Integration and Validation

After refinement loop completion:

#### Content Update
- Apply refined content to specification document
- Maintain document structure and formatting
- Preserve technology context alignment
- Update modification timestamps and version information

#### Quality Validation
Verify the refined specification meets FSDD compliance:
- **Business Alignment**: Specification addresses all business requirements
- **Technical Completeness**: All technical components are specified
- **Implementation Clarity**: Clear guidance for implementation teams
- **Integration Coherence**: Consistent integration patterns and approaches
- **Quality Standards**: Meets defined quality thresholds and standards

### 5. Documentation and Handoff

#### Refinement Documentation
Document the refinement process results:
- Quality improvements achieved through refinement iterations
- Technology alignment enhancements
- Specific FSDD compliance improvements
- Remaining areas for future refinement

#### Stakeholder Communication
Prepare stakeholder communication:
- Summary of specification improvements
- Technology context integration results
- Quality compliance status
- Next steps for implementation planning

## Quality Gates

### FSDD Compliance Verification
- ✅ All 12 FSDD quality gates addressed in refined specification
- ✅ Business requirements clearly traced to technical components
- ✅ Technology choices justified and documented
- ✅ Implementation guidance is clear and actionable
- ✅ Integration patterns are consistent and well-defined

### Technology Alignment Validation
- ✅ Current technology stack properly integrated into specification
- ✅ Technology choices align with existing infrastructure
- ✅ Migration paths clearly defined where needed
- ✅ Performance and scalability considerations addressed
- ✅ Security requirements integrated with technology selections

### Implementation Readiness Assessment
- ✅ Specification provides sufficient detail for implementation planning
- ✅ Technology research requirements clearly identified
- ✅ Dependencies and integration points well-defined
- ✅ Quality standards and testing approaches specified
- ✅ Deployment and operational requirements documented

## Success Criteria

- Technical specification refined through systematic critic/refiner iterations
- FSDD compliance achieved with measurable quality improvements
- Technology context properly integrated throughout specification
- Implementation teams have clear, actionable technical guidance
- Stakeholders understand specification improvements and next steps
- Foundation established for effective implementation planning and execution

## Tool Usage Notes

- Use {refinement_loop_tool} for orchestrated quality improvement cycles
- Use {parse_command_tool} for command-based refinement execution
- Technology detection script provides current environment context
- Strategic plan documents provide business requirement traceability
- Refined specifications saved to strategic plans directory for team access
"""
