from __future__ import annotations

from autotestgen.generator import generate


def test_generate_autosar_nm_smoke() -> None:
    r = generate("ECU支持AUTOSAR网络管理")
    assert r.requirement.domain == "autosar_nm"
    assert len(r.test_points) >= 4
    assert len(r.test_cases) == len(r.test_points) * 3
    assert "```mermaid" in r.mindmap_markdown
    assert "mindmap" in r.mindmap_markdown

