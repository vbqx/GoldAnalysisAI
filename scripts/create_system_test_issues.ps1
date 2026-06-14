# Create GitHub Issues from 2026-06-14 system test report.
# Usage: .\scripts\create_system_test_issues.ps1
# Auth: gh auth login, or git credential with repo scope

$ErrorActionPreference = "Stop"
$Owner = "vbqx"
$RepoName = "GoldAnalysisAI"
$Repo = "$Owner/$RepoName"

function Get-GitHubToken {
    if ($env:GH_TOKEN) { return $env:GH_TOKEN }
    if ($env:GITHUB_TOKEN) { return $env:GITHUB_TOKEN }
    $cred = @"
protocol=https
host=github.com

"@ | git credential fill
    $line = $cred | Select-String "^password="
    if (-not $line) { throw "No GitHub token found. Run: gh auth login" }
    return ($line.Line -replace '^password=','')
}

$Token = Get-GitHubToken
$Headers = @{
    Authorization = "Bearer $Token"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

function New-GhIssue {
    param(
        [string]$Title,
        [string]$Body,
        [string[]]$Labels = @()
    )
    $payload = @{ title = $Title; body = $Body; labels = $Labels }
    $r = Invoke-RestMethod -Method Post `
        -Uri "https://api.github.com/repos/$Owner/$RepoName/issues" `
        -Headers $Headers `
        -Body ($payload | ConvertTo-Json -Depth 5) `
        -ContentType "application/json; charset=utf-8"
    Write-Host "Created #$($r.number): $($r.html_url)" -ForegroundColor Green
    return $r
}

function Ensure-Label {
    param([string]$Name, [string]$Color, [string]$Description)
    try {
        Invoke-RestMethod -Method Post `
            -Uri "https://api.github.com/repos/$Owner/$RepoName/labels" `
            -Headers $Headers `
            -Body (@{ name = $Name; color = $Color; description = $Description } | ConvertTo-Json) `
            -ContentType "application/json" | Out-Null
    } catch { }
}

$labelDefs = @(
    @{ name = "bug"; color = "d73a4a"; description = "Something isn't working" },
    @{ name = "enhancement"; color = "a2eeef"; description = "New feature or request" },
    @{ name = "testing"; color = "0075ca"; description = "Testing related" },
    @{ name = "priority: high"; color = "b60205"; description = "High priority" },
    @{ name = "priority: low"; color = "0e8a16"; description = "Low priority" }
)
foreach ($ld in $labelDefs) {
    Ensure-Label $ld.name $ld.color $ld.description
}

Write-Host "Creating system test issues for $Repo ..." -ForegroundColor Cyan

New-GhIssue -Title "[Bug] 子页面残留「报告尚未生成」提示" -Labels @("bug", "testing", "priority: high") -Body @'
## 测试场景

- **测试日期：** 2026-06-14
- **环境：** Windows · Streamlit `http://localhost:8501` · `AGENT_MODE=hybrid`
- **步骤：**
  1. 首次访问「机构报告」页，等待流水线完成（约 2–3 分钟）
  2. 确认报告已正常显示（现价、图表、LLM 结论均可见）
  3. 切换到「短线策略」或「LLM决策链」页
  4. 观察页面顶部/侧边栏是否仍显示加载提示

## 发现的问题

报告已在 Session 中缓存且内容完整渲染，但子页面仍残留蓝色 info 条：

> 报告尚未生成，正在跑流水线…请稍候（约 2–3 分钟）。

- 复现页面：`pages/2_短线策略.py`、`pages/3_LLM决策链.py`
- 根因：`ensure_report(show_generation_ui=False)` 在缓存未就绪时调用 `st.info(...)`，rerun 后该 info 未被清除
- 相关代码：`src/viz/streamlit_common.py` 第 142–143 行
- **优先级：** P1 — 用户误以为仍在加载，影响体验

## 建议修复方案

1. **方案 A（推荐）：** 仅在报告确实未就绪时显示 loading，缓存命中后不再调用 `st.info`
   - 在 `ensure_report` 中，若 `REPORT_SESSION_KEY` 已有数据则跳过 info/spinner
   - 或将 loading 状态放入 `st.empty()` 容器，完成后 `.empty()` 清除

2. **方案 B：** 子页面首次访问若主页面尚未生成，redirect 或共用主页面 loading UI（`show_generation_ui=True`）

3. **验收标准：**
   - 报告生成完毕后，切换至「短线策略」「LLM决策链」不再出现「报告尚未生成」提示
   - 首次冷启动（无缓存）时 loading 提示仍正常显示
'@

New-GhIssue -Title "[Bug] LLM 阶段 JSON 解析偶发失败，hybrid 模式回退规则引擎" -Labels @("bug", "testing", "priority: high") -Body @'
## 测试场景

- **测试日期：** 2026-06-14
- **环境：** `AGENT_MODE=hybrid` · `LLM_STAGE_RESEARCH=true` · `LLM_STAGE_DEBATE=true`
- **步骤：**
  1. 启动 Streamlit，首次加载触发完整流水线
  2. 观察服务端日志中 LLM 阶段输出
  3. 在「LLM决策链」页查看阶段来源与 I/O 记录

## 发现的问题

首次 Streamlit 启动时，看多研究（bullish）阶段 LLM 调用失败：

```
WARNING | src.agents.llm.base | llm stage bullish failed: Unterminated string starting at: line 456 column 3 (char 6875)
```

- hybrid 模式自动回退到规则引擎，流水线不中断（容错正常）
- 但 LLM 研究阶段的价值降低，且 I/O 页可能记录截断/ malformed JSON
- 后续 CLI 复跑时 bullish 阶段成功（89s），说明问题具有**间歇性**
- **优先级：** P1 — 影响 hybrid 模式核心能力

## 建议修复方案

1. **增强 JSON 解析容错**（`src/agents/llm/base.py`）：
   - 对 `json.loads` 失败尝试修复常见截断（补全括号、去除 trailing comma）
   - 或使用 `json_repair` 等库做二次解析

2. **流式响应完整性校验：**
   - 在 `_stream_json_response` 结束处检查 JSON 是否闭合
   - 不完整则自动重试（最多 1–2 次，指数退避）

3. **Prompt 约束：**
   - 在 system prompt 中强调「返回紧凑 JSON，避免过长字符串」
   - 对 items 数组设置 max 条数限制

4. **可观测性：**
   - 解析失败时将原始响应写入 `llm_io` 的 error 字段（便于排查）
   - 在 UI 阶段来源 Banner 明确标注「LLM 失败 · 已回退规则」

5. **验收标准：**
   - 连续 5 次流水线运行，bullish/bearish/debate 阶段 JSON 解析成功率 ≥ 95%
   - 失败时 UI 与日志有明确回退原因
'@

New-GhIssue -Title "[Improvement] run_pipeline_test.py 直接运行报 ModuleNotFoundError" -Labels @("enhancement", "testing", "priority: low") -Body @'
## 测试场景

- **测试日期：** 2026-06-14
- **步骤：**
  1. 在项目根目录执行：`python scripts/run_pipeline_test.py`
  2. 不设置 `PYTHONPATH` 或 `cd` 到特定目录

## 发现的问题

脚本直接运行失败：

```
ModuleNotFoundError: No module named 'src'
```

- README 文档中测试命令为 `python scripts/run_pipeline_test.py`，未说明需设置模块路径
- 设置 `$env:PYTHONPATH="项目根目录"` 后可正常运行

## 建议修复方案

1. **方案 A（推荐）：** 在脚本开头添加路径引导：
   ```python
   ROOT = Path(__file__).resolve().parents[1]
   sys.path.insert(0, str(ROOT))
   ```

2. **方案 B：** 改为可安装包入口：`python -m scripts.run_pipeline_test`

3. **同步更新 README** 测试章节，确保一行命令即可跑通

4. **验收标准：**
   - 在项目根目录直接 `python scripts/run_pipeline_test.py` 无 ModuleNotFoundError
'@

New-GhIssue -Title "[Improvement] Streamlit use_container_width 弃用警告" -Labels @("enhancement", "testing", "priority: low") -Body @'
## 测试场景

- **测试日期：** 2026-06-14
- **步骤：**
  1. 启动 Streamlit 应用
  2. 在机构报告页切换页面、渲染 Plotly 图表
  3. 查看终端控制台输出

## 发现的问题

控制台反复出现 Streamlit 弃用警告：

```
Please replace `use_container_width` with `width`.
use_container_width will be removed after 2025-12-31.
For use_container_width=True, use width='stretch'.
```

- 不影响功能，但污染日志，且 2025-12-31 后将不兼容

## 建议修复方案

1. 全局搜索 `use_container_width=True`，替换为 `width="stretch"`
2. 搜索 `use_container_width=False`，替换为 `width="content"`
3. 重点检查 `src/viz/report_views.py`、`src/viz/dashboard_components.py` 等 viz 模块

4. **验收标准：**
   - 启动应用并浏览三页，控制台无 `use_container_width` 弃用警告
'@

New-GhIssue -Title "[Improvement] 侧边栏仅显示 STRONG 模型，与研究阶段 FAST 模型不一致" -Labels @("enhancement", "testing", "priority: low") -Body @'
## 测试场景

- **测试日期：** 2026-06-14
- **环境：** `LLM_MODEL_FAST` 与 `LLM_MODEL_STRONG` 可能配置不同模型
- **步骤：**
  1. 查看侧边栏 LLM 模型显示
  2. 在「LLM决策链 → LLM 输入/输出」查看各阶段实际调用模型

## 发现的问题

- 侧边栏 caption 仅显示 `LLM_MODEL_STRONG`（如 DeepSeek-V4-Pro）
- 研究阶段（bullish/bearish）实际使用 `LLM_MODEL_FAST`（如 Qwen/Qwen2.5-7B-Instruct）
- 用户易误解全部 LLM 调用均使用同一模型

## 建议修复方案

1. 侧边栏改为双行显示：
   ```
   LLM 快模型: Qwen2.5-7B
   LLM 强模型: DeepSeek-V4-Pro
   ```

2. 或在 `render_sidebar_header()` 中根据 `AGENT_MODE` 动态展示路由策略

3. **验收标准：**
   - 侧边栏展示的模型与 `llm_io` 记录中各阶段实际 model 字段一致
'@

New-GhIssue -Title "[Improvement] 子页面首次加载缺少流水线进度 UI" -Labels @("enhancement", "testing", "priority: low") -Body @'
## 测试场景

- **测试日期：** 2026-06-14
- **步骤：**
  1. 清除 Session / 首次冷启动
  2. 直接访问「短线策略」或「LLM决策链」（跳过机构报告主页）
  3. 观察等待期间的 UI 反馈

## 发现的问题

- 首次加载约 2–3 分钟，LLM 研究阶段单步可达 90s+
- 主页面（机构报告）有 spinner + hero「正在生成报告…」
- 子页面仅显示简单 `st.info` 文案，无分步进度（拉取行情 / ICT / 研究 / 辩论等）
- 用户无法感知当前执行到哪一步

## 建议修复方案

1. 抽取 `render_pipeline_progress()` 为共享组件，子页面 loading 时也展示 `generation_steps` 实时进度

2. 或在子页面 loading 期间 redirect 到主页 progress UI，完成后再跳回

3. 复用 `src/viz/pipeline_progress.py` 已有组件

4. **验收标准：**
   - 冷启动直接访问子页面时，可见与主页一致的分步进度
   - 进度步骤与 `meta.generation_steps` 最终记录一致
'@

New-GhIssue -Title "[Testing] 系统测试报告 2026-06-14 — GoldAnalysisAI 全功能测试" -Labels @("testing") -Body @'
## 测试概要

| 项目 | 内容 |
|------|------|
| **测试日期** | 2026-06-14 |
| **测试类型** | 全功能系统测试（非代码审查） |
| **环境** | Windows · Python 3.12 · Streamlit `:8501` |
| **配置** | `AGENT_MODE=hybrid` · `LLM_ENABLED=true` · TradingView OANDA:XAUUSD |
| **结论** | 核心功能可用，28/30 通过，建议修复 P1 缺陷后发布 |

---

## 测试场景

### 后端流水线
- 执行 `scripts/run_pipeline_test.py`（完整 pipeline）
- 验证多周期数据、ICT 分析、报告 Schema、智能体链、LLM 文案

### UI 三页面
- **机构报告** (`app.py`)：指标卡、多周期图、日线主图、Fibonacci、交易计划
- **短线策略** (`pages/2_短线策略.py`)：15m/5m 图、关键价位、策略文字
- **LLM决策链** (`pages/3_LLM决策链.py`)：4 个 Tab（决策/文案/步骤/I/O）

### 缓存与导航
- 三页切换不重新跑流水线
- 侧边栏「指标校验」展开
- HTTP 三页均 200

---

## 测试结果

### 通过项 ✅
- 流水线 12 步全部 `done`，现价 4218.56
- 5 周期数据齐全（5m=5000 … 1d=365）
- 3 条交易信号、LLM 文案、4 条 I/O 记录
- Session 缓存：切换页面时间戳不变，日志无新 pipeline
- 图表 HTML 生成正常

### 未覆盖 ⬜
- 「刷新报告」按钮（避免 3 分钟重跑）
- `AGENT_MODE=rule` / `LLM_ENABLED=false` 纯规则模式
- 网络断开 / API Key 无效等异常场景

---

## 发现的问题

| ID | 优先级 | 描述 | 关联 Issue |
|----|--------|------|-----------|
| BUG-01 | P1 | LLM JSON 解析偶发失败 | 见独立 Issue |
| BUG-02 | P1 | 子页面残留「报告尚未生成」提示 | 见独立 Issue |
| WARN-01 | P2 | run_pipeline_test.py 缺 PYTHONPATH | 见独立 Issue |
| WARN-02 | P2 | use_container_width 弃用警告 | 见独立 Issue |
| WARN-03 | P2 | 侧边栏模型显示不完整 | 见独立 Issue |
| WARN-04 | P2 | 子页面缺少进度 UI | 见独立 Issue |

---

## 建议修复优先级

1. **P1：** BUG-02（UI 误导）→ BUG-01（LLM 稳定性）
2. **P2：** WARN-01 ~ WARN-04 可在下一迭代处理
3. **回归测试：** 修复后复测三页切换、LLM hybrid 回退、CLI 测试脚本

---

## 非功能指标

| 指标 | 结果 |
|------|------|
| 首次加载 | ~182s |
| CLI 复跑 | ~142–231s |
| 容错 | LLM 失败自动回退规则，流水线不中断 |
| 数据一致性 | 三页现价/指标一致 |
'@

Write-Host "`nDone. Created 7 issues in $Repo" -ForegroundColor Green
