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
