# Roadmap & Spec Model Refactoring Implementation Plan

## Overview

This document outlines the refactoring of the roadmap and spec models to support dynamic spec creation and progressive enhancement from InitialSpec → PartialSpec → TechnicalSpec.

**CURRENT STATUS**: Implementation is in early stages. Templates and models still use legacy regex-based parsing with format inconsistencies. The MarkdownIt-native approach described below represents the target architecture.

## MarkdownIt-Native Template & Parsing Strategy

### Template-First Design Philosophy

This implementation redesigns templates to work seamlessly with MarkdownIt's natural parsing capabilities instead of fighting against them:

**Core Principle:** Templates are flexible, external packages are not. Structure templates to leverage MarkdownIt's strengths.

**Key Advantages:**
- **Simplicity**: Consistent `- **Field**: value` list format throughout all templates
- **Reliability**: Uses MarkdownIt's battle-tested list parsing instead of complex regex
- **Maintainability**: No special cases or format inconsistencies to handle
- **Performance**: Single recursive traversal instead of multiple parsing passes
- **Extensibility**: Easy to add new fields without changing parsing logic

**Dependencies:**
```bash
uv add markdown-it-py mdformat
```

**Template Structure:**
```markdown
# Document Title: {name}

## Section Name
- **Field Name**: {field_value}
- **Another Field**: {another_value}

## Another Section
- **More Fields**: {more_values}
```

**Parsing Strategy:**
- Recursive tree traversal using `_find_nodes_by_type()`
- Extract text from list items with simple string operations
- No regex patterns or special case handling required

## Current State Analysis

### Issues to Resolve
- Fixed 3-phase structure in Roadmap model limits flexibility
- No clear relationship between roadmap phases and specs
- TechnicalSpec cannot handle partial completion during refinement loops
- Hardcoded phase parsing in templates
- **FORMAT INCONSISTENCY**: TechnicalSpec uses regex parsing with `**Field**: \`value\`` format
- **TEMPLATE MISMATCH**: Current templates don't match MarkdownIt-native examples
- **ROUND-TRIP FAILURE**: Character-for-character reconstruction tests failing

### Architecture Goals
- Dynamic spec count (3-7 specs per roadmap)
- Progressive enhancement: InitialSpec → PartialSpec → TechnicalSpec
- Clear ID-based relationships between models
- Flexible markdown parsing and generation

## Model Architecture Design

### Three-Tier Spec Progression

```python
InitialSpec:
  - id: str = uuid4()[:8]
  - Basic spec outline from roadmap
  - Foundation fields only

PartialSpec:
  - id: str  # use id from InitialSpec
  - All TechnicalSpec fields with default=""
  - Loose validation for iteration

TechnicalSpec:
  - id: str  # use id from PartialSpec
  - All fields required/validated
  - Complete specification
```

### Updated Roadmap Structure

```python
Roadmap:
  - project_name: str
  - project_goal: str
  - total_duration: str
  - team_size: str
  - roadmap_budget: str
  - specs: list[InitialSpec]  # Dynamic list
  - metadata fields...
```

## TDD Implementation Plan

### Phase 1: MarkdownIt-Native Template & Parsing Foundation

#### Template Restructuring Strategy
1. **Redesign All Templates to Use Consistent List Format**
   - Convert `**Field**: \`value\`` patterns to `- **Field**: {value}`
   - Remove special case sections that require complex parsing
   - Group related fields under logical section headings
   - Use Python string formatting for clean variable substitution

2. **Template Examples**

   **New Roadmap Template:**
   ```markdown
   # Project Roadmap: {project_name}

   ## Project Details
   - **Project Goal**: {project_goal}
   - **Total Duration**: {total_duration}
   - **Team Size**: {team_size}
   - **Budget**: {roadmap_budget}

   ## Specifications
   {specs_list}

   ## Risk Assessment
   - **Critical Path Analysis**: {critical_path_analysis}
   - **Key Risks**: {key_risks}
   ```

   **New Spec Template:**
   ```markdown
   # Technical Specification: {phase_name}
   <!-- ID: {id} -->

   ## Overview
   - **Objectives**: {objectives}
   - **Scope**: {scope}
   - **Dependencies**: {dependencies}

   ## Technical Details
   - **Architecture**: {architecture}
   - **Technology Stack**: {technology_stack}
   ```

3. **Simplified Parsing Implementation**
   ```python
   @classmethod
   def _parse_markdown_fields(cls, markdown: str) -> dict[str, str]:
       """Parse using MarkdownIt's native list parsing."""
       md = MarkdownIt("commonmark")
       tree = SyntaxTreeNode(md.parse(markdown))

       fields = {}

       # Extract title
       for node in cls._find_nodes_by_type(tree, "heading"):
           if node.tag != "h1":
               continue
           title_text = cls._extract_text_content(node)
           # Extract title data...

       # Extract all field data from lists
       for item in cls._find_nodes_by_type(tree, "list_item"):
           text = cls._extract_text_content(item)
           if "**" not in text or ":" not in text:
               continue
           field_part, value_part = text.split(":", 1)
           field_name = field_part.replace("**", "").strip().lower().replace(" ", "_")
           fields[field_name] = value_part.strip()

       return fields
   ```

### Phase 2: Model Refactoring with MarkdownIt-Native Parsing

#### Recursive Tree Traversal Utilities

1. **Implement Common Parsing Utilities**
   ```python
   @classmethod
   def _find_nodes_by_type(cls, node: SyntaxTreeNode, node_type: str) -> list[SyntaxTreeNode]:
       """Recursively find all nodes of a specific type in the tree."""
       nodes = []

       if node.type == node_type:
           nodes.append(node)

       if hasattr(node, 'children') and node.children:
           for child in node.children:
               nodes.extend(cls._find_nodes_by_type(child, node_type))

       return nodes

   @classmethod
   def _extract_text_content(cls, node: SyntaxTreeNode) -> str:
       """Recursively extract all text content from a node."""
       if not hasattr(node, 'children') or not node.children:
           return getattr(node, 'content', '')

       return ' '.join(cls._extract_text_content(child) for child in node.children)
   ```

2. **Roadmap Model Priority (Proof of Concept)**
   - Convert Roadmap model to use list-based parsing
   - Test template compatibility and parsing accuracy
   - Validate character-for-character markdown reconstruction

3. **TechnicalSpec Model Update**
   - Replace regex parsing with MarkdownIt list parsing
   - Update template to match new list-based structure
   - Ensure backward compatibility during transition

   **Current Reality**: TechnicalSpec model (spec.py lines 42-97) uses complex regex patterns:
   ```python
   sections = {
       'objectives': r'\*\*Objectives\*\*:\s*`([^`]+)`',
       'scope': r'\*\*Scope\*\*:\s*`([^`]+)`',
       # ... 15+ more regex patterns
   }
   ```
   This contradicts the MarkdownIt-native goal.

#### Green Phase - Implement Minimal Models

1. **Create `services/models/initial_spec.py`**
   - Basic fields from roadmap spec outline
   - UUID generation: `uuid4()[:8]`
   - Markdown parsing for roadmap-generated content
   - No unnecessary docstrings per CLAUDE.md

2. **Create `services/models/partial_spec.py`**
   - Mirror TechnicalSpec fields with `str` defaults
   - `initial_spec_id: str` foreign key
   - Loose validation allowing empty strings
   - Progressive completion support

3. **Update `services/models/spec.py`**
   - Add `initial_spec_id: str` field
   - Enforce strict validation for all fields
   - Maintain existing functionality

4. **Refactor `services/models/roadmap.py`**
   - Replace fixed phase fields with `specs: list[InitialSpec]`
   - Use markdown-it-py for "## Spec Breakdown" section parsing
   - Token-based extraction of `### Spec N:` headers and content
   - MDRenderer for flexible markdown generation with round-trip fidelity
   - Replace regex patterns with robust SyntaxTreeNode traversal

#### Refactor Phase - Code Quality & Standards

1. **Coding Standards Compliance**
   - No obvious docstrings (only MCP tools and complex algorithms)
   - Type hints for all parameters and returns
   - No inline imports
   - Self-documenting variable names
   - Max 3 levels of nesting

2. **Quality Gates**
   - All mypy errors resolved
   - All ruff check errors resolved
   - No test warnings
   - 100% test coverage for new models
   - Round-trip parsing tests ensure data integrity for all models

### Phase 2: Service Layer Implementation

#### Red Phase - Service Tests

1. **InitialSpecService Tests**
   ```python
   test_create_initial_spec_from_roadmap()
   test_get_initial_spec_by_id()
   test_list_initial_specs_by_roadmap()
   ```

2. **PartialSpecService Tests**
   ```python
   test_create_partial_from_initial()
   test_update_partial_spec_content()
   test_promote_to_technical_spec()
   ```

3. **RoadmapService Updates**
   ```python
   test_create_roadmap_with_dynamic_specs()
   test_update_spec_breakdown_section()
   ```

#### Green Phase - Service Implementation

1. **Create `services/spec_service.py`**
   - InitialSpec CRUD operations
   - PartialSpec lifecycle management
   - Promotion logic to TechnicalSpec
   - Service layer separation per CLAUDE.md

2. **Update `services/roadmap_service.py`**
   - Dynamic spec creation from roadmap
   - Flexible spec count handling
   - Integration with InitialSpec creation

#### Refactor Phase - Service Quality

1. **Type Safety**
   - Full typing for all service methods
   - Proper error handling with custom exceptions
   - Async/await for I/O operations

2. **Testing**
   - pytest + pytest-mock only
   - Service layer focus (no endpoint logic)
   - Mock external dependencies

### Phase 3: MCP Integration

#### Red Phase - MCP Tool Tests

1. **New MCP Tools Tests**
   ```python
   test_create_partial_spec_from_initial_tool()
   test_update_partial_spec_tool()
   test_promote_to_technical_spec_tool()
   ```

2. **Updated Roadmap Tools Tests**
   ```python
   test_dynamic_spec_creation()
   test_flexible_spec_count_handling()
   ```

#### Green Phase - MCP Implementation

1. **Add to `services/mcp/server.py`**
   - New MCP tools for three-tier spec workflow
   - Proper docstrings for MCP tools (exception per CLAUDE.md)
   - Context logging and error handling

2. **Update `services/mcp/roadmap_tools.py`**
   - Support for dynamic spec creation
   - Integration with InitialSpec model

#### Refactor Phase - MCP Quality

1. **Error Handling**
   - FastMCP ToolError and ResourceError usage
   - Proper error messages for agents
   - Context logging for debugging

2. **Tool Documentation**
   - Docstrings for MCP tools only (CLAUDE.md compliance)
   - Clear parameter descriptions
   - Return value specifications

### Phase 4: Template & Integration

#### Red Phase - Template Tests

1. **Dynamic Template Tests**
   ```python
   test_spec_breakdown_parsing()
   test_variable_spec_count_generation()
   test_markdown_roundtrip_accuracy()
   test_template_round_trip_parsing_maintains_data_integrity()
   ```

#### Green Phase - Template Updates

1. **Roadmap Template Updates**
   - Rename "Phase Breakdown" to "Spec Breakdown"
   - Dynamic spec parsing (3-7 specs)
   - Flexible markdown generation

#### Refactor Phase - Integration Testing

1. **End-to-End Tests**
   - Full workflow: Roadmap → InitialSpec → PartialSpec → TechnicalSpec
   - MCP tool integration testing
   - Markdown parsing accuracy
   - Round-trip data integrity tests across entire workflow

## Updated Implementation Order

### **Phase 1: Template-First MarkdownIt-Native Foundation (Week 1)**

#### **Days 1-2: Template Restructuring**
- Redesign Roadmap template to use consistent `- **Field**: {value}` list format
- Redesign Spec templates (TechnicalSpec, PartialSpec) to use list-based structure
- Remove special case formatting that requires complex parsing
- Test templates render correctly and are human-readable

**Current State**: Templates still use legacy formats with complex parsing requirements

#### **Days 3-4: Simplified Model Parsing**
- Implement `_find_nodes_by_type()` recursive traversal utility
- Refactor Roadmap model to use MarkdownIt-native list parsing
- Update TechnicalSpec model parsing to match new template structure
- Replace complex regex patterns with simple list item text extraction
- Use early returns and guard clauses to minimize nesting

**Current State**: TechnicalSpec still uses regex parsing (lines 42-97). Roadmap model needs assessment.

#### **Days 5-6: Exact Markdown Reconstruction**
- Implement MarkdownIt-based markdown generation from structured data
- Test character-for-character reproduction of original markdown
- Validate round-trip parsing maintains complete data integrity
- Benchmark performance vs current regex approach

**Current State**: Character-for-character round-trip tests are failing. Need template/parsing alignment.

#### **Day 7: Validation & Testing**
- End-to-end tests: parse → modify → reconstruct → parse again
- Template readability validation with sample documents
- Performance comparison and optimization
- Integration test with existing codebase

### **Phase 2: Model Migration & Service Updates (Week 2)**
1. InitialSpec and PartialSpec model updates for new parsing
2. Service layer integration with new parsing methods
3. MCP tool compatibility testing
4. Error handling improvements

### **Phase 3: Full Ecosystem Migration (Week 3)**
1. Remaining template conversions
2. End-to-end workflow validation
3. Performance optimization
4. Documentation updates

## Success Criteria

### Functional Requirements
- Templates use consistent MarkdownIt-native list format throughout
- Parsing logic uses recursive tree traversal with no regex patterns
- Character-for-character markdown reconstruction capability
- All templates render correctly and remain human-readable
- Roadmaps support dynamic spec creation (3-7 specs)
- Clear model progression: InitialSpec → PartialSpec → TechnicalSpec

### Quality Requirements
- Zero mypy errors
- Zero ruff check errors
- 100% test coverage for new code
- All tests passing with no warnings
- CLAUDE.md coding standards compliance

### Integration Requirements
- MCP tools work with new model structure
- Markdown parsing/generation accuracy
- Backward compatibility not required (greenfield)

## Risk Mitigation

### Technical Risks
- **Model Complexity**: Keep models focused, single responsibility
- **Parsing Reliability**: markdown-it-py ensures CommonMark compliance and eliminates regex edge cases
- **State Management**: Clear ID-based relationships
- **Dependency Management**: markdown-it-py and mdformat add external dependencies but provide substantial parsing benefits

### Quality Risks
- **Standards Compliance**: Automated linting and type checking
- **Test Coverage**: TDD approach ensures comprehensive testing
- **Performance**: Monitor model creation/parsing performance

## File Structure

```text
services/models/
├── initial_spec.py      # ✅ EXISTS: Uses MarkdownIt parsing
├── partial_spec.py      # ✅ EXISTS: Uses MarkdownIt parsing
├── spec.py             # ❌ NEEDS UPDATE: Still uses regex parsing
├── roadmap.py          # ❌ NEEDS ASSESSMENT: Parsing method unclear
└── enums.py            # ✅ EXISTS: Contains SpecStatus enum

services/
├── spec_service.py     # New: Spec lifecycle management
└── roadmap_service.py  # Updated: Dynamic spec creation

services/mcp/
├── server.py           # Updated: New MCP tools
├── roadmap_tools.py    # Updated: Dynamic spec support
└── spec_tools.py       # New: Spec workflow tools

tests/
├── unit/models/        # Model tests
├── unit/services/      # Service tests
├── unit/utils/         # Markdown parser utility tests
├── integration/mcp/    # MCP tool tests
└── e2e/               # End-to-end workflow tests
```

This implementation follows strict TDD methodology while maintaining CLAUDE.md coding standards and ensuring comprehensive test coverage throughout the development process.
