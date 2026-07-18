# Codex 自动优化目标模板

以后你可以少对话、多给目标。默认边界是：Codex 可以分析、修改、测试、分批提交，但不自动推送远端。

## 推荐目标格式

```text
目标：
范围：
禁止事项：
验收命令：
提交策略：
停止条件：
```

## 示例

```text
目标：整理测试体系，让日常开发、场景专项、发版测试更清楚。
范围：tests/、docs/aspice/governance/verification-strategy.md、README 测试入口。
禁止事项：不改业务逻辑，不删除人工审计报告。
验收命令：python tests/run.py --fast；pytest tests/regression/test_doc_pipeline_sync.py -q；git diff --check。
提交策略：按 docs、tests、cleanup 分批提交。
停止条件：fast 全绿，工作区只剩我明确允许的未提交文件。
```

## 默认工作规则

- 先读现状，再动文件。
- 自然边界分批提交，不把代码、文档、测试输出混成一包。
- 每轮至少跑 `python tests/run.py --fast`，再加触及模块专项测试。
- 发现高风险行为时先降级为计划，例如实盘下单、删除历史审计、重写核心决策逻辑。
- 最终汇报必须包含：改了什么、验证结果、剩余风险、下一步建议。

## 适合长期目标的写法

- “持续优化文档，直到新人能按 docs/documentation-center.md 跑通项目。”
- “持续降低测试噪音，直到 git status 不再出现生成物。”
- “持续推进 LLM replay，直到能区分规则 baseline 与 LLM 决策表现。”
- “持续整理执行链，直到 shadow -> paper_mt5 -> live_mt5 的边界可审计。”
