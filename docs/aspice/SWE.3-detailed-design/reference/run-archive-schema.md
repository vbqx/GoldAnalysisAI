# Advice V2 运行归档与回放契约

每次运行保存在 `.cache/run_archives/<run_id>/`。

| 文件 | 回放作用 |
|---|---|
| `manifest.json` | 归档 schema、状态、配置和制品版本。 |
| `report.json` | Advice V2 报告；新归档必需。 |
| `enriched/{tf}.json` | 指标补全后的多周期数据。 |
| `analyses.json` | 时间周期结构分析。 |
| `fetch.json` | 外部数据和原始抓取摘要。 |

`report_contract_version=2` 对应 `artifact_kind=human_review_advice` 和 `artifact_version=2`。

## 回放规则

1. V2 归档直接加载同一份报告，不重新抓取数据，不调用 LLM。
2. V1 归档不再显示旧 `signals` 或 `agent_trace`；回放器使用已保存的 enriched 数据、analyses 和 external 快照重建 Advice V2。
3. 缺少重建所需市场数据的旧归档返回明确诊断，不把 V1 内容伪装成当前建议。
4. 更高的未知 schema 版本阻止加载；可兼容的缺字段归档以 degraded 状态加载。
5. 新写入先完成制品，再原子写入最终 manifest。

布局或契约变更必须提升对应版本、增加兼容测试并更新本文档。
