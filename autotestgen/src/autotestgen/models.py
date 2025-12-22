from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Requirement(BaseModel):
    text: str = Field(..., description="原始需求文本")
    domain: str = Field(default="generic", description="识别到的领域/模块")
    assumptions: list[str] = Field(default_factory=list, description="基于输入不足的默认假设")


class TestPoint(BaseModel):
    id: str
    title: str
    description: str = ""
    category: str = "通用"
    tags: list[str] = Field(default_factory=list)


class TestCase(BaseModel):
    id: str
    title: str
    test_point_id: str
    priority: Literal["P0", "P1", "P2"] = "P1"
    type: Literal["正向", "异常", "边界"] = "正向"
    preconditions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class TreeNode(BaseModel):
    """用于脑图输出的简单树。"""

    title: str
    children: list["TreeNode"] = Field(default_factory=list)

    def add(self, title: str, children: list["TreeNode"] | None = None) -> "TreeNode":
        node = TreeNode(title=title, children=children or [])
        self.children.append(node)
        return node
