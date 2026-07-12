# Testing Strategy

测试体系分三层：fast、scenario、release。日常开发优先 fast；触及模块时补 scenario；发版或大改再跑 release。

## 三层测试

| 层 | 用途 | 命令 |
|----|------|------|
| `fast` | 日常门禁，无网络优先 | `python tests/run.py --fast` |
| `scenario` | 功能域专项 | 见下表 |
| `release` | 发版前完整验证 | `python tests/run.py --full` + GUI 冒烟 + 外部 API |

## Scenario 命令矩阵

| 场景 | 命令 |
|------|------|
| LLM 阶段 | `pytest tests/unit/test_analyst_team_llm.py tests/unit/test_llm_trade_stages.py tests/unit/test_llm_transport.py -q` |
| 回测 | `pytest tests/unit/test_backtest_engine.py tests/unit/test_backtest_macro.py tests/unit/test_backtest_metrics.py tests/unit/test_backtest_simulator.py -q` |
| MT5 账号/执行边界 | `pytest tests/unit/test_mt5_provider.py -q` |
| 文档/流水线同步 | `pytest tests/regression/test_doc_pipeline_sync.py -q` |
| 报告可信度层 | `pytest tests/unit/test_fact_registry.py tests/unit/test_report_invariants.py tests/unit/test_report_reliability.py tests/unit/test_evidence_provenance.py tests/unit/test_golden_report_benchmark.py -q` |
| 外部数据 | `python tests/run.py --external` |
| 规则一致性 | `python tests/tools/coherence_check.py` |
| GUI 手工冒烟 | `python run_app.py` 后按 `tests/cases/test-plan.md` 的 UIL/FN 清单检查 |

## 输出边界

- `tests/cases/`：用例目录和设计，不放运行输出。
- `tests/reports/`：只保留人工挑选的审计报告和 `.gitkeep`。
- 浏览器 profile、截图、cache、临时运行日志不进入 Git。
- `.codex-remote-attachments/` 一律忽略，截图附件不属于代码仓库。

## 用例维护

- 新增测试先登记 `tests/cases/catalog.yaml`，再补自动化或手工说明。
- 改流水线阶段必须同步 `docs/reference/pipeline-steps.yaml`。
- 改报告字段必须同步 `docs/reference/examples/report-schema.md`。
- 改事实注册/不变量/证据溯源必须同步 [report-trust.md](../architecture/report-trust.md)。
- 每次自动优化默认验收：fast + 本轮专项 + `git diff --check`。
