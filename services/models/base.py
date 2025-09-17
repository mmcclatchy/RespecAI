from abc import ABC, abstractmethod
from typing import Any, ClassVar, Self

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from pydantic import BaseModel


class MCPModel(BaseModel, ABC):
    # Class variables - won't be treated as model fields
    TITLE_PATTERN: ClassVar[str] = ''
    TITLE_FIELD: ClassVar[str] = ''
    HEADER_FIELD_MAPPING: ClassVar[dict[str, list[str]]] = {}

    @classmethod
    def _find_nodes_by_type(cls, node: SyntaxTreeNode, node_type: str) -> list[SyntaxTreeNode]:
        nodes = []

        if node.type == node_type:
            nodes.append(node)

        if hasattr(node, 'children') and node.children:
            for child in node.children:
                nodes.extend(cls._find_nodes_by_type(child, node_type))

        return nodes

    @classmethod
    def _extract_text_content(cls, node: SyntaxTreeNode) -> str:
        if not hasattr(node, 'children') or not node.children:
            return getattr(node, 'content', '')

        return ' '.join(cls._extract_text_content(child) for child in node.children)

    @classmethod
    def _extract_content_by_header_path(cls, tree: SyntaxTreeNode, path: list[str]) -> str:
        h2_header = path[0]
        h3_header = path[1] if len(path) > 1 else None

        nodes = tree.children if hasattr(tree, 'children') else []
        h2_start_idx = None

        for i, node in enumerate(nodes):
            if node.type == 'heading' and node.tag == 'h2':
                header_text = cls._extract_text_content(node).strip()
                if header_text == h2_header:
                    h2_start_idx = i
                    break

        if h2_start_idx is None:
            return ''

        if h3_header is None:
            content_parts = []
            for j in range(h2_start_idx + 1, len(nodes)):
                next_node = nodes[j]
                if next_node.type == 'heading' and next_node.tag == 'h2':
                    break
                if next_node.type in ['paragraph', 'list', 'blockquote', 'code_block']:
                    content_parts.append(cls._extract_text_content(next_node).strip())
            return '\n\n'.join(content_parts).strip()

        h3_start_idx = None
        for j in range(h2_start_idx + 1, len(nodes)):
            next_node = nodes[j]
            if next_node.type == 'heading' and next_node.tag == 'h2':
                break
            if next_node.type == 'heading' and next_node.tag == 'h3':
                header_text = cls._extract_text_content(next_node).strip()
                if header_text == h3_header:
                    h3_start_idx = j
                    break

        if h3_start_idx is None:
            return ''

        content_parts = []
        for j in range(h3_start_idx + 1, len(nodes)):
            next_node = nodes[j]
            if next_node.type == 'heading' and next_node.tag in ['h2', 'h3']:
                break
            if next_node.type in ['paragraph', 'list', 'blockquote', 'code_block']:
                content_parts.append(cls._extract_text_content(next_node).strip())

        return '\n\n'.join(content_parts).strip()

    @classmethod
    def _extract_list_items_by_header_path(cls, tree: SyntaxTreeNode, path: list[str]) -> list[str]:
        h2_header = path[0]
        h3_header = path[1] if len(path) > 1 else None

        nodes = tree.children if hasattr(tree, 'children') else []
        h2_start_idx = None

        for i, node in enumerate(nodes):
            if node.type == 'heading' and node.tag == 'h2':
                header_text = cls._extract_text_content(node).strip()
                if header_text == h2_header:
                    h2_start_idx = i
                    break

        if h2_start_idx is None:
            return []

        if h3_header is None:
            for j in range(h2_start_idx + 1, len(nodes)):
                next_node = nodes[j]
                if next_node.type == 'heading' and next_node.tag == 'h2':
                    break
                if next_node.type == 'bullet_list':
                    items = []
                    for item in cls._find_nodes_by_type(next_node, 'list_item'):
                        item_text = cls._extract_text_content(item).strip()
                        if item_text and item_text not in ['None identified', 'None provided']:
                            items.append(item_text)
                    return items
            return []

        h3_start_idx = None
        for j in range(h2_start_idx + 1, len(nodes)):
            next_node = nodes[j]
            if next_node.type == 'heading' and next_node.tag == 'h2':
                break
            if next_node.type == 'heading' and next_node.tag == 'h3':
                header_text = cls._extract_text_content(next_node).strip()
                if header_text == h3_header:
                    h3_start_idx = j
                    break

        if h3_start_idx is None:
            return []

        for j in range(h3_start_idx + 1, len(nodes)):
            next_node = nodes[j]
            if next_node.type == 'heading' and next_node.tag in ['h2', 'h3']:
                break
            if next_node.type == 'bullet_list':
                items = []
                for item in cls._find_nodes_by_type(next_node, 'list_item'):
                    item_text = cls._extract_text_content(item).strip()
                    if item_text and item_text not in ['None identified', 'None provided']:
                        items.append(item_text)
                return items

        return []

    @classmethod
    def parse_markdown(cls, markdown: str) -> Self:
        if cls.TITLE_PATTERN not in markdown:
            # Convert class name from CamelCase to readable format
            readable_name = (
                cls.__name__.replace('Plan', ' Plan').replace('Spec', ' Spec').replace('Requirements', ' Requirements')
            )
            readable_name = ' '.join(readable_name.split()).lower()
            raise ValueError(f'Invalid {readable_name} format: missing title')

        md = MarkdownIt('commonmark')
        tree = SyntaxTreeNode(md.parse(markdown))

        fields: dict[str, Any] = {}

        # Extract title
        for node in cls._find_nodes_by_type(tree, 'heading'):
            if node.tag != 'h1':
                continue
            title_text = cls._extract_text_content(node)
            title_pattern = cls.TITLE_PATTERN.replace('# ', '').split(':')[0]
            if title_pattern not in title_text:
                continue
            title_value = title_text.split(':', 1)[1].strip()
            fields[cls.TITLE_FIELD] = title_value
            break

        # Extract fields using header path mapping
        for field_name, header_path in cls.HEADER_FIELD_MAPPING.items():
            if field_name.endswith('_list'):
                # Handle list fields - extract as list and store under base field name
                base_field = field_name.replace('_list', '')
                extracted_list = cls._extract_list_items_by_header_path(tree, header_path)
                if extracted_list:  # Only set if we found actual content
                    # Store the list under the base field name
                    fields[base_field] = extracted_list
            else:
                # Handle content fields - extract as string
                extracted_content = cls._extract_content_by_header_path(tree, header_path)
                if extracted_content:  # Only set if we found actual content
                    fields[field_name] = extracted_content

        # Backward compatibility: Extract metadata from bullet points (- **Field**: value)
        for item in cls._find_nodes_by_type(tree, 'list_item'):
            text = cls._extract_text_content(item).strip()

            # Check for bullet point format with bold text (- **Field**: value)
            # The text content might not include ** due to markdown parsing
            if ':' not in text:
                continue

            # Check if this looks like a metadata field
            field_part, value_part = text.split(':', 1)
            potential_field = field_part.strip().lower().replace(' ', '_').replace('-', '_')

            # Look for common metadata fields even without ** formatting
            metadata_fields = ['status', 'created', 'last_updated', 'version']
            if potential_field not in metadata_fields:
                continue

            field_name = field_part.replace('**', '').strip().lower().replace(' ', '_').replace('-', '_')
            field_value = value_part.strip()

            # Map common field names - ensure all enum fields are properly mapped
            field_mapping = {
                'status': 'project_status',
                'created': 'creation_date',
                'version': 'version',
                'last_updated': 'last_updated',
            }
            model_field_name = field_mapping.get(field_name, field_name)

            # Only set if not already extracted from hierarchical headers
            if model_field_name not in fields or not fields[model_field_name]:
                fields[model_field_name] = field_value

        return cls(**fields)

    @abstractmethod
    def build_markdown(self) -> str:
        pass
