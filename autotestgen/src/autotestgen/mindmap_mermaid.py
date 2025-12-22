from __future__ import annotations

from autotestgen.models import TreeNode


def _escape_mermaid(text: str) -> str:
    # Mermaid mindmap 节点对特殊字符较敏感；最小处理：替换换行，避免破坏缩进结构
    return text.replace("\n", " ").strip()


def render_mermaid_mindmap(root: TreeNode) -> str:
    """
    输出为 Markdown，内含 Mermaid mindmap 代码块：

    ```mermaid
    mindmap
      root((xxx))
        child
    ```
    """

    lines: list[str] = ["```mermaid", "mindmap"]

    def walk(node: TreeNode, depth: int) -> None:
        indent = "  " * depth
        title = _escape_mermaid(node.title)
        if depth == 1:
            # root 节点用圆角强调
            lines.append(f"{indent}root(({title}))")
        else:
            lines.append(f"{indent}{title}")
        for child in node.children:
            walk(child, depth + 1)

    walk(root, 1)
    lines.append("```")
    return "\n".join(lines) + "\n"
