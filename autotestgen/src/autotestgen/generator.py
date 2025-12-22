from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from autotestgen.kb import choose_test_points
from autotestgen.mindmap_mermaid import render_mermaid_mindmap
from autotestgen.models import Requirement, TestCase, TestPoint, TreeNode


@dataclass(frozen=True)
class GenerateResult:
    requirement: Requirement
    test_points: list[TestPoint]
    test_cases: list[TestCase]
    mindmap_markdown: str


def _mk_case_id(tp_id: str, suffix: str) -> str:
    return f"{tp_id}-{suffix}"


def generate(requirement_text: str) -> GenerateResult:
    domain, assumptions, test_points = choose_test_points(requirement_text)
    req = Requirement(text=requirement_text, domain=domain, assumptions=assumptions)

    cases: list[TestCase] = []
    for tp in test_points:
        # 最小策略：每个测试点 3 条用例（正向/异常/边界），并做少量领域特化描述
        base_pre = ["ECU 已刷写目标软件版本", "具备抓包/日志/测量点等可观测手段"]
        if req.domain == "autosar_nm":
            base_pre = [
                "ECU 已集成 NM（如 CanNm/EthNm 等）并完成网络配置",
                "网络中至少存在 1 个对端节点/仿真节点可参与 NM",
                "具备抓包/日志/测量点等可观测手段",
            ]

        cases.append(
            TestCase(
                id=_mk_case_id(tp.id, "P"),
                title=f"{tp.title}（正向）",
                test_point_id=tp.id,
                priority="P0" if tp.category in {"功能", "状态机"} else "P1",
                type="正向",
                preconditions=base_pre,
                steps=[
                    f"按配置启用相关能力：{tp.title}",
                    "触发主流程条件（如点火/上电、网络请求、对端入网等）",
                    "观察系统行为与网络侧报文/状态",
                ],
                expected=[
                    "行为满足需求描述",
                    "关键状态/事件可在报文或日志中被验证",
                ],
                tags=tp.tags + [tp.category],
            )
        )

        cases.append(
            TestCase(
                id=_mk_case_id(tp.id, "N"),
                title=f"{tp.title}（异常）",
                test_point_id=tp.id,
                priority="P1",
                type="异常",
                preconditions=base_pre,
                steps=[
                    "构造异常环境：丢包/延迟、对端不响应、总线错误或配置缺失（择一或多项）",
                    "触发与该测试点相关的流程",
                    "持续观察一段时间，确认系统是否进入错误/降级路径",
                ],
                expected=[
                    "系统不会死机/重启（除非有明确设计）",
                    "给出明确的错误处理/降级行为（日志/诊断/状态）",
                ],
                tags=tp.tags + ["Robustness"],
            )
        )

        cases.append(
            TestCase(
                id=_mk_case_id(tp.id, "B"),
                title=f"{tp.title}（边界）",
                test_point_id=tp.id,
                priority="P2",
                type="边界",
                preconditions=base_pre,
                steps=[
                    "将相关配置/触发条件调到边界值（如最小/最大周期、临界超时、频繁切换）",
                    "触发流程并记录行为",
                ],
                expected=[
                    "边界条件下仍满足基本功能与稳定性要求",
                    "若超出设计范围，应有清晰限制与提示",
                ],
                tags=tp.tags + ["Boundary"],
            )
        )

    mind_root = TreeNode(title=req.text)
    scope = mind_root.add("范围/假设")
    for a in req.assumptions:
        scope.add(a)

    tp_node = mind_root.add("测试点（按类别）")
    by_cat: dict[str, list[TestPoint]] = {}
    for tp in test_points:
        by_cat.setdefault(tp.category, []).append(tp)
    for cat in sorted(by_cat.keys()):
        cat_node = tp_node.add(cat)
        for tp in by_cat[cat]:
            cat_node.add(f"{tp.id} {tp.title}")

    cases_node = mind_root.add("用例集（每点：正向/异常/边界）")
    cases_node.add(f"用例总数：{len(cases)}")

    mind_md = render_mermaid_mindmap(mind_root)
    return GenerateResult(requirement=req, test_points=test_points, test_cases=cases, mindmap_markdown=mind_md)


def write_outputs(result: GenerateResult, out_dir: Path) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    paths: dict[str, Path] = {}

    design_path = out_dir / "test_design.md"
    design_path.write_text(result.mindmap_markdown, encoding="utf-8")
    paths["test_design_md"] = design_path

    tp_path = out_dir / "test_points.json"
    tp_path.write_text(
        json.dumps([tp.model_dump() for tp in result.test_points], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    paths["test_points_json"] = tp_path

    tc_json_path = out_dir / "test_cases.json"
    tc_json_path.write_text(
        json.dumps([tc.model_dump() for tc in result.test_cases], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    paths["test_cases_json"] = tc_json_path

    tc_csv_path = out_dir / "test_cases.csv"
    with tc_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "title",
                "test_point_id",
                "priority",
                "type",
                "preconditions",
                "steps",
                "expected",
                "tags",
            ],
        )
        writer.writeheader()
        for tc in result.test_cases:
            writer.writerow(
                {
                    "id": tc.id,
                    "title": tc.title,
                    "test_point_id": tc.test_point_id,
                    "priority": tc.priority,
                    "type": tc.type,
                    "preconditions": " | ".join(tc.preconditions),
                    "steps": " | ".join(tc.steps),
                    "expected": " | ".join(tc.expected),
                    "tags": " | ".join(tc.tags),
                }
            )
    paths["test_cases_csv"] = tc_csv_path

    meta_path = out_dir / "meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "requirement": result.requirement.model_dump(),
                "counts": {"test_points": len(result.test_points), "test_cases": len(result.test_cases)},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    paths["meta_json"] = meta_path
    return paths
