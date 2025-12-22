## workspace

本仓库包含一个最小可运行的“需求 → 测试点 → 测试设计（脑图）→ 测试用例”生成工具：

- 代码位置：`/workspace/autotestgen`
- 使用 Poetry 管理依赖

快速运行：

```bash
cd /workspace/autotestgen
/home/ubuntu/.local/bin/poetry install
/home/ubuntu/.local/bin/poetry run autotestgen demo --out out
```
