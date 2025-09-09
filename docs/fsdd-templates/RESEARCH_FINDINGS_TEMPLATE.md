# Research Findings Template

## Template Purpose
**Used by**: impl-researcher agent  
**When**: Documenting comprehensive research results after executing Priority 1-4 research workflow  
**Context**: Part of Implementation Agent Flow - provides research-based implementation guidance to impl-coder agent via Linear comment  

## Variable Requirements
**Flow Variables (Tier 1)** - from Linear ticket research sections:
- `STEP_NAME`: Step name for comment header
- `ARCHIVE_KEYWORDS`: Keywords used for Priority 1 archive scanning
- `TECH_A`, `TECH_B`, `TECH_C`, `USE_CASE`: Variables for Priority 2 integration research queries
- `ISOLATED_TECHNOLOGY_1`: Variable for Priority 3 individual research queries
- `VALIDATION_TOPIC`: Variable for Priority 4 validation research queries

**Generated Output Variables (Tier 1)** - created by impl-researcher for downstream agents:
- `IMPLEMENTATION_APPROACH`: Specific implementation approach based on synthesized research findings
- `KEY_CONSIDERATIONS`: Critical technical points and constraints identified through research

## Research Context
This template consolidates findings from the complete Priority 1-4 research workflow:
- **Priority 1**: Archive scanning results and user engagement decisions
- **Priority 2**: Integration research for multi-technology scenarios  
- **Priority 3**: Individual technology research for isolated implementations
- **Priority 4**: Validation research to fill remaining gaps

The synthesized guidance feeds directly into TDD implementation by impl-coder agent via Linear comment.

## Template Content

---

```markdown
# Research Findings for ${STEP_NAME}

## Archive Scan Results
**Keywords Used**: "${ARCHIVE_KEYWORDS}"
**Files Reviewed**: [list of files examined]
**Relevance Assessment**: [Tight/Loose/No Match with rationale]
**User Decision**: [Use/Supplement/Skip] - [rationale provided by user]

## External Research Summary

### Integration Patterns (Priority 2)
**Research Query**: "Search for best practices integrating ${TECH_A} + ${TECH_B} + ${TECH_C} for ${USE_CASE}"
**Key Findings**:
- [Synthesized findings from research]

### Individual Technology (Priority 3)
**Research Query**: "Search for best practices for ${ISOLATED_TECHNOLOGY_1}"
**Key Findings**:
- [Synthesized findings from research]

### Validation Research (Priority 4)
**Research Query**: "Search for best practices integrating ${VALIDATION_TOPIC}"
**Key Findings**:
- [Synthesized findings from research]

## Implementation Guidance

### Recommended Approach
${IMPLEMENTATION_APPROACH}

### Critical Considerations
${KEY_CONSIDERATIONS}

## Research Decision Log
- **Archive Decision**: [Use/Supplement/Skip] - [user rationale]
- **External Research Scope**: [what was researched and why]
- **Implementation Confidence**: [High/Medium/Low based on research quality]
```

---

## Usage Instructions
1. **impl-researcher agent**: Replace all `${VARIABLE}` placeholders with research findings
2. **Research Synthesis**: Fill in actual findings from Priority 1-4 research execution
3. **Implementation Guidance**: Generate specific IMPLEMENTATION_APPROACH and KEY_CONSIDERATIONS variables
4. **Handoff**: Created comment is consumed by impl-coder agent for TDD implementation
5. **Linear Integration**: Add as comment to current Linear ticket using `mcp__linear-server__create_comment`

## Integration Flow
- **Linear ticket research sections** → **impl-researcher** (executes research)
- **impl-researcher** → **this template** (documents findings as Linear comment)
- **Research findings comment** → **impl-coder** (guides implementation)
- **impl-coder** → **impl-verifier** (validates results)
