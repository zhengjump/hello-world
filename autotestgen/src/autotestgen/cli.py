from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from autotestgen.generator import generate, write_outputs


app = typer.Typer(add_completion=False, help="根据需求自动抽取测试点、生成脑图测试设计并产出测试用例。")
console = Console()


@app.command("gen")
def gen_cmd(
    requirement: str = typer.Argument(..., help="需求文本，例如：ECU支持AUTOSAR网络管理"),
    out_dir: Path = typer.Option(Path("out"), "--out", "-o", help="输出目录"),
) -> None:
    """
    生成：
    - test_design.md（Mermaid mindmap 脑图）
    - test_points.json
    - test_cases.json / test_cases.csv
    - meta.json
    """
    result = generate(requirement)
    paths = write_outputs(result, out_dir)

    table = Table(title="生成结果")
    table.add_column("项", style="bold")
    table.add_column("值")
    table.add_row("领域识别", result.requirement.domain)
    table.add_row("测试点数", str(len(result.test_points)))
    table.add_row("用例数", str(len(result.test_cases)))
    table.add_row("脑图", str(paths["test_design_md"]))
    table.add_row("用例(CSV)", str(paths["test_cases_csv"]))
    table.add_row("用例(JSON)", str(paths["test_cases_json"]))
    console.print(table)


@app.command("demo")
def demo_cmd(out_dir: Path = typer.Option(Path("out"), "--out", "-o", help="输出目录")) -> None:
    """使用内置示例需求运行一次。"""
    gen_cmd("ECU支持AUTOSAR网络管理", out_dir=out_dir)

