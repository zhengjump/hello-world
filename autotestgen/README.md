## autotestgen（最小系统）

输入一段需求文本，自动：

- 提取测试点（基于最小规则 + 内置领域知识库）
- 生成测试设计脑图（Mermaid mindmap，写入 `test_design.md`）
- 生成测试用例（`test_cases.csv` / `test_cases.json`）

### 安装

在本仓库目录下：

```bash
cd /workspace/autotestgen
/home/ubuntu/.local/bin/poetry install
```

### 快速体验（示例需求）

```bash
cd /workspace/autotestgen
/home/ubuntu/.local/bin/poetry run autotestgen demo --out out
```

输出文件：

- `out/test_design.md`：测试设计脑图（Mermaid mindmap）
- `out/test_points.json`：测试点清单
- `out/test_cases.csv` / `out/test_cases.json`：测试用例
- `out/meta.json`：元信息

### 自定义需求输入

```bash
cd /workspace/autotestgen
/home/ubuntu/.local/bin/poetry run autotestgen gen "ECU支持AUTOSAR网络管理" --out out
```

### 如何查看脑图

将 `out/test_design.md` 放到支持 Mermaid 的 Markdown 渲染器中（例如 GitHub/多数编辑器插件）即可看到脑图。
