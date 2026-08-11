# Advice V2 测试计划

## 分层

- SWE.4：数据、指标、结构、建议、审计、LLM 边界、归档和界面 helper 单元测试。
- SWE.5：冻结上下文跨组件契约，以及可选 live supplier smoke。
- SWE.6：样例、流水线文档、ASPICE 追溯和完整回归。

## 发布门禁

```powershell
python tests/run.py
python -m compileall -q src app.py run_app.py scripts
python scripts/check_aspice_assets.py --check
python scripts/generate_aspice_software_evidence.py --check
python scripts/generate_aspice_readable_docs.py --check
```

`python tests/run.py --full` 包含 live/slow 集成范围，可能依赖外部供应商；供应商不可用与软件失败分开记录。

## 高风险优先级

1. Advice V2 只能有一个方向和一个首选方案。
2. 陈旧、冲突或证据不足必须降级为 WAIT/AVOID。
3. 关注区、失效位、目标和证据引用必须通过确定性审计。
4. LLM 不得修改方向或数字。
5. 回放不得重新抓取数据或调用 LLM，也不得把 V1 建议直接显示为当前建议。
