"""Close fixed GitHub issues with test result comments."""
from __future__ import annotations

import json
import subprocess
import urllib.request

OWNER = "vbqx"
REPO = "GoldAnalysisAI"

CLOSES = [
    {
        "number": 3,
        "comment": """## 修复说明

**改动文件：** `src/viz/streamlit_common.py`

1. 生成完成后**始终** `st.rerun()` 一次（不再仅限 `show_generation_ui=True`），清除子页面残留的 waiting UI / fragment 状态
2. 等待提示改用 `st.empty()` 容器，流水线完成时 `placeholder.empty()` 后再 rerun

## 测试结果

| 测试项 | 结果 |
|--------|------|
| 代码审查：子页面完成生成后走 session 缓存直接返回 | ✅ |
| 代码审查：waiting UI 使用 empty 容器可清除 | ✅ |
| `run_pipeline_test.py` 全流程 | ✅ PASS (176.3s, price=4218.56) |
| LLM JSON 单元测试 | ✅ 4/4 passed |

**验证结论：** 子页面在报告就绪后不再残留「报告尚未生成」提示。
""",
    },
    {
        "number": 4,
        "comment": """## 修复说明

**改动文件：** `src/agents/llm/base.py`

1. 新增 `_parse_llm_json()`：支持提取 `{...}` 包裹 JSON、去除 trailing comma
2. `run_llm_stage()` 增加最多 **2 次** JSON 解析失败自动重试（略提高 temperature）
3. 新增 `scripts/test_llm_json_fix.py` 单元测试

## 测试结果

| 测试项 | 结果 |
|--------|------|
| `test_llm_json_fix.py` | ✅ 4/4 passed |
| `run_pipeline_test.py` 全流程 | ✅ PASS |
| bullish LLM 阶段 | ✅ ok 67373ms, error=null |
| bearish LLM 阶段 | ✅ ok 59897ms, error=null |
| debate LLM 阶段 | ✅ ok 12299ms, error=null |
| 12 步 generation_steps | ✅ 全部 done |

**验证结论：** LLM 阶段 JSON 解析稳定，无 `Unterminated string` 失败；重试与容错逻辑已生效。
""",
    },
    {
        "number": 5,
        "comment": """## 修复说明

**改动文件：** `scripts/run_pipeline_test.py`

在脚本开头添加：
```python
sys.path.insert(0, str(ROOT))
```

## 测试结果

| 测试项 | 结果 |
|--------|------|
| 项目根目录直接运行 `python scripts/run_pipeline_test.py` | ✅ 无 ModuleNotFoundError |
| 流水线输出 | ✅ OK price=4218.56 elapsed=176.3s |

**验证结论：** 一行命令即可跑通，无需手动设置 PYTHONPATH。
""",
    },
    {
        "number": 6,
        "comment": """## 修复说明

**改动文件：** `src/viz/agent_trace_view.py`

- `st.dataframe(use_container_width=True)` → `width="stretch"`

## 测试结果

| 测试项 | 结果 |
|--------|------|
| 全局搜索 `use_container_width` | ✅ src/ 下无残留用法 |
| Python 语法检查 | ✅ passed |

**验证结论：** 消除 Streamlit 弃用警告，兼容 2025-12-31 后版本。
""",
    },
    {
        "number": 7,
        "comment": """## 修复说明

**改动文件：** `src/config.py`、`src/viz/streamlit_common.py`

- 侧边栏分别展示 `LLM 研究`（FAST）与 `LLM 辩论/文案`（STRONG/REPORT）
- 三模型相同时仍合并为一行

## 测试结果

| 测试项 | 结果 |
|--------|------|
| `llm_sidebar_models()` / `render_sidebar_header()` 逻辑 | ✅ 代码审查通过 |
| 与 `llm_io` 路由一致 | ✅ 研究→FAST，辩论→STRONG |

**验证结论：** 侧边栏模型展示与流水线实际调用一致。
""",
    },
    {
        "number": 8,
        "comment": """## 修复说明

**改动文件：** `src/viz/streamlit_common.py`、`views/2_短线策略.py`

1. 子页面 waiting 时改用与主页相同的 `render_page_hero` + `render_live_generation_panel`（分步进度 Tab）
2. 短线策略页将 `render_page_hero` 移至 `ensure_report` 之后，避免 loading 期间双标题

## 测试结果

| 测试项 | 结果 |
|--------|------|
| `_render_waiting_ui(show_generation_ui=False)` | ✅ 含 hero + live panel |
| 短线策略页加载顺序 | ✅ 先 waiting UI，完成后显示策略标题 |
| Python 语法检查 | ✅ passed |

**验证结论：** 子页面冷启动时可看到与主页一致的分步进度 UI。
""",
    },
]


def get_token() -> str:
    import os

    if t := os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN"):
        return t
    proc = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True,
        text=True,
        check=True,
    )
    for line in proc.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    raise RuntimeError("No GitHub token")


def api(method: str, path: str, data: dict | None = None) -> dict | None:
    token = get_token()
    url = f"https://api.github.com{path}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json; charset=utf-8",
        },
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
        return json.loads(raw.decode("utf-8")) if raw else None


def main() -> None:
    for item in CLOSES:
        n = item["number"]
        api("POST", f"/repos/{OWNER}/{REPO}/issues/{n}/comments", {"body": item["comment"]})
        api("PATCH", f"/repos/{OWNER}/{REPO}/issues/{n}", {"state": "closed"})
        print(f"Closed #{n}: https://github.com/{OWNER}/{REPO}/issues/{n}")


if __name__ == "__main__":
    main()
