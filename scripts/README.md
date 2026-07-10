# 开发脚本

本目录**不再存放测试用例**。测试相关代码已迁移至 [`tests/`](../tests/README.md)。项目文档见 [`docs/README.md`](../docs/README.md)。

| 脚本 | 说明 |
|------|------|
| `export_sample_report.py` | 生成 `docs/examples/sample-report.json`（无网络） |
| `dev-env.ps1` | Windows 开发终端初始化：UTF-8 控制台、Python UTF-8 输出、OpenBLAS 单线程 |
| `show_utf8.py` | 按 UTF-8 显式读取并带行号输出文本文件，适合中文文档/源码补丁上下文 |

| 旧脚本 | 新位置 |
|--------|--------|
| `run_pipeline_test.py` | `python tests/run.py --integration` |
| `test_llm_json_fix.py` | `pytest tests/unit/test_llm_json.py` |
| `regression_test.py` | `python tests/run.py --fast` |
| `create_system_test_issues.py` | `tests/tools/github/create_issues.py` |
| `close_fixed_issues.py` | `tests/tools/github/close_issues.py` |
| `chart_compare_test.py` | `tests/tools/chart_compare.py` |

根目录仍保留同名薄封装以便过渡，输出 deprecation 提示。

---

## Windows 终端编码

在 PowerShell 中开发或运行测试前，建议先执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\scripts\dev-env.ps1
```

该脚本会切换控制台到 UTF-8，设置 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`，并默认限制 `OPENBLAS_NUM_THREADS=1`，减少中文日志/文档输出乱码和本地测试时的 OpenBLAS 线程问题。`Set-ExecutionPolicy -Scope Process` 只影响当前 PowerShell 窗口。

读取含中文的源码或文档时，优先使用：

```powershell
python scripts/show_utf8.py docs/domain/financial-review.md --start 520 --count 40
```

如果只需要临时用 PowerShell 读取文件，先显式设置输出编码：

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Get-Content -Encoding UTF8 docs/reference/pipeline-steps.yaml
```

不要用未初始化编码环境下的 `Get-Content` 作为补丁上下文来源；它可能把 UTF-8 无 BOM 文件按系统 ANSI 解码，导致看到的文本与磁盘真实内容不一致。
