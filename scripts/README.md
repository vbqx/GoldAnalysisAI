# 开发脚本

本目录**不再存放测试用例**。测试相关代码已迁移至 [`tests/`](../tests/README.md)。

| 旧脚本 | 新位置 |
|--------|--------|
| `run_pipeline_test.py` | `python tests/run.py --integration` |
| `test_llm_json_fix.py` | `pytest tests/unit/test_llm_json.py` |
| `regression_test.py` | `python tests/run.py --fast` |
| `create_system_test_issues.py` | `tests/tools/github/create_issues.py` |
| `close_fixed_issues.py` | `tests/tools/github/close_issues.py` |
| `chart_compare_test.py` | `tests/tools/chart_compare.py` |

根目录仍保留同名薄封装以便过渡，输出 deprecation 提示。
