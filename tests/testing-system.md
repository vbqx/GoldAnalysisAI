# 测试系统

默认门禁离线运行：

```powershell
python tests/run.py
```

常用范围：

| 命令 | 范围 |
|---|---|
| `python tests/run.py --unit` | 全部单元测试 |
| `python tests/run.py --regression` | 文档、样例和 ASPICE 回归 |
| `python tests/run.py --financial` | Advice V2 内容与审计测试 |
| `python tests/run.py --integration` | 慢速端到端集成 |
| `python tests/run.py --external` | 真实外部供应商健康检查 |
| `python tests/run.py --full` | 所有测试 |

核心 Advice V2 契约位于 `tests/unit/test_advice_v2.py`。测试要求：最多一个首选方案、WAIT/AVOID 不带方案、几何与证据通过审计、LLM 不改变数字、报告无 V1 顶层键。

ASPICE 证据检查：

```powershell
python scripts/check_aspice_assets.py --check
python scripts/generate_aspice_software_evidence.py --check
python scripts/generate_aspice_readable_docs.py --check
```

真实供应商不可用不等同于软件失败；`--external` 单独记录结果，不污染确定性离线门禁。
