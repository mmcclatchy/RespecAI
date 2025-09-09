def generate_spec_command_template(
    create_spec_tool: str,
    get_spec_tool: str,
    add_comment_tool: str,
    update_spec_tool: str,
    list_comments_tool: str,
    spec_implementation: str,
    tool_usage_examples: dict,
) -> str:
    return f"""---
allowed-tools:
  - Task(plan-analyst)
  - Task(spec-architect) 
  - execute_spec_workflow
  - render_agent_dynamic
  - {create_spec_tool}
  - {get_spec_tool}
  - {add_comment_tool}
  - {update_spec_tool}
  - {list_comments_tool}
  - Read
  - Glob
argument-hint: [project-name] [issue-name]
description: Convert strategic plans to technical specifications using {spec_implementation}
---

# Technical Specification Creation

Convert strategic plan into detailed technical specification for: $ARGUMENTS

## Your Task

Create a comprehensive technical specification by analyzing the strategic plan and orchestrating the MCP workflow for specification creation.

## Workflow Orchestration

### Phase 1: Strategic Plan Analysis

1. **Locate Strategic Plan**: Find the most recent strategic plan output from `/plan` command
   ```bash
   # Look for plan files in common locations
   find . -name "*plan*.md" -type f -newer $(date -d '7 days ago' +%Y-%m-%d) 2>/dev/null
   ```

2. **Extract Business Requirements**: Use plan-analyst agent to parse strategic plan
   ```bash
   Task(plan-analyst, {{
     "strategic_plan_content": "[strategic plan content]",
     "focus_area": "$ARGUMENTS",
     "extraction_mode": "business_requirements"
   }})
   ```

### Phase 2: Technical Architecture Design

1. **Generate Spec Architect Agent**: Create platform-specific agent with {spec_implementation} tools
   ```bash
   render_agent_dynamic('spec-architect', '{spec_implementation.lower()}')
   ```

2. **Create Technical Specification**: Use spec-architect with extracted requirements
   ```bash
   Task(spec-architect, {{
     "business_requirements": "[extracted from Phase 1]",
     "project_name": "[first argument]",
     "technical_focus": "[second argument]",
     "platform": "{spec_implementation}",
     "quality_threshold": 0.85
   }})
   ```

### Phase 3: {spec_implementation} Platform Integration

1. **Execute Spec Workflow**: Call MCP tool to orchestrate specification creation
   ```bash
   execute_spec_workflow("[strategic plan content with business requirements]")
   ```

2. **Create Platform Specification**: Use {spec_implementation} tools to create actual specification
   
   **{spec_implementation} Tool Usage:**
   ```python
   # Create new specification
   {tool_usage_examples.get('create_spec', f'{create_spec_tool}(title="Technical Specification: $ARGUMENTS", description="[spec content]")')}
   
   # Add detailed technical information
   {tool_usage_examples.get('add_comment', f'{add_comment_tool}(spec_id="[created_spec_id]", body="[technical details]")')}
   
   # Update specification with architecture decisions
   {tool_usage_examples.get('update_spec', f'{update_spec_tool}(spec_id="[spec_id]", updates={{...}})')}
   ```

### Phase 4: Quality Validation

1. **Apply FSDD Quality Gates**: Ensure specification meets quality standards
   ```bash
   # Quality assessment will be automatically applied by the spec-architect agent
   # Requirements: Overall score >= 0.85 across FSDD 12-point quality gates
   ```

2. **Validation Checklist**:
   - [ ] EARS notation compliance (WHEN/THEN format)
   - [ ] Hard constraints defined (SHALL/SHALL NOT)
   - [ ] Performance contracts measurable
   - [ ] Integration points specified
   - [ ] Technology stack explicitly chosen
   - [ ] Anti-patterns documented
   - [ ] Scope boundaries clear
   - [ ] Acceptance criteria measurable
   - [ ] API specifications complete
   - [ ] Validation mechanisms defined
   - [ ] Strategic vs tactical separation
   - [ ] Template compliance verified

### Phase 5: Specification Finalization

1. **Link to Strategic Plan**: Ensure traceability from business requirements to technical specs

2. **Platform-Specific Outputs**:
   - **{spec_implementation}**: Specification created as platform ticket/issue/document
   - **Quality Score**: FSDD compliance score and recommendations
   - **Architecture Decisions**: Technology choices and constraints documented
   - **Implementation Guidance**: Next steps for development teams

## Success Criteria

- ✅ Technical specification created on {spec_implementation} platform
- ✅ FSDD quality score >= 0.85
- ✅ All business requirements from strategic plan addressed
- ✅ Technology stack and architecture decisions documented
- ✅ Clear acceptance criteria and validation gates defined
- ✅ Traceability from strategic plan to technical implementation

## Platform-Specific Notes

**{spec_implementation} Integration:**
- Specifications created as: {spec_implementation} {'issues' if spec_implementation in ['Linear', 'GitHub'] else 'files'}
- Comments and updates tracked within platform
- Integration with existing {spec_implementation} workflows
- Platform-specific formatting and conventions applied

## Error Handling

If any phase fails:
1. Check platform tool availability ({spec_implementation} API accessible)
2. Validate strategic plan format and content
3. Ensure agents are properly generated with platform tools
4. Review quality gate feedback for specification improvements
5. Use refine-spec command if specification needs enhancement

## Next Steps

After successful specification creation:
1. Use `/build [spec-id]` to create implementation plan
2. Use `/refine-spec [spec-id]` if specification needs enhancement  
3. Use `/validate [spec-id]` for comprehensive quality validation

---

*Generated for {spec_implementation} platform with dynamic tool injection*
*Quality threshold: 85% FSDD compliance required*
*Workflow orchestration via MCP tools and Task agents*
"""
