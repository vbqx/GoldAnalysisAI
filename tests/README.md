# GoldAnalysisAI 测试体系

测试代码、用例目录与开发工具与业务代码 (`src/`) 分离，统一放在 `tests/` 下。

## 目录结构

```
tests/
├── README.md                 # 本文件
├── run.py                    # 统一入口：自动测试脚本
├── dashboard.py              # Streamlit 测试面板 UI
├── runner.py                 # 测试运行引擎（CLI + UI 共用）
├── conftest.py               # pytest 配置
├── _bootstrap.py             # 路径 / .env 引导
├── cases/
│   ├── README.md             # 用例维护说明
│   ├── test-plan.md          # 分层测试设计（UI→指标→功能→性能）
│   └── catalog.yaml          # 用例目录（ID、优先级、是否自动化）
├── unit/                     # 单元测试（无网络，秒级）
├── integration/              # 集成测试（完整流水线，~2–3 分钟）
├── regression/               # 回归测试（Issue 修复项、约定检查）
├── tools/                    # 开发辅助（非 pytest 用例）
│   ├── chart_compare.py      # 生成对比用 HTML
│   └── github/               # Issue 批量创建/关单
└── reports/                  # 测试输出（gitignore）
```

## 快速开始

```bash
# 安装开发依赖（含 pytest）
pip install -r requirements-dev.txt

# 快速测试：单元 + 回归（默认，无网络，约 61 项）
python tests/run.py

# 金融 Review 单测（FIN-*）
python tests/run.py --financial

# 外部 API 冒烟（DXY / 新闻 / TE 日历 / TV 社媒，需网络）
python tests/run.py --external

# 完整测试：含流水线集成（需 TradingView + .env）
python tests/run.py --full

# 仅单元 / 仅回归 / 仅集成
python tests/run.py --unit
python tests/run.py --regression
python tests/run.py --integration
```

等价 pytest 命令：

```bash
pytest tests/unit tests/regression -q          # 快速（含外部源 + Analyst LLM + 信号去重 + TV 重试）
pytest tests/unit/test_external_sources.py -v
pytest tests/unit/test_signal_dedup.py -v
pytest tests/unit/test_analyst_team_llm.py -v
pytest tests/unit/test_tradingview_retry.py -v
pytest tests/unit/test_financial_review.py -m financial -v
pytest tests/integration -m integration -q   # slow
```

## 测试面板 UI

浏览器中实时查看 pytest 进度、通过/失败统计与流水线日志：

```bash
streamlit run tests/dashboard.py --server.port 8502
```

打开 http://localhost:8502 ，选择套件后点击「开始」。支持 **快速**、**金融 Review（FIN-*）**、**集成** 等套件；界面约 1 秒刷新。

## 用例维护

1. 在 [`cases/test-plan.md`](cases/test-plan.md) 设计场景，在 [`cases/catalog.yaml`](cases/catalog.yaml) 登记用例（`UIL-*` / `IND-*` / `FN-*` / `FIN-*` / `PERF-*` / `UT-*` / `IT-*` / `RG-*`）
2. 在对应子目录实现测试代码
3. 本地 `python tests/run.py` 验证
4. 关 Issue 时在评论中引用用例 ID（如 `RG-03`）

## 开发工具

| 命令 | 说明 |
|------|------|
| `streamlit run tests/dashboard.py --server.port 8502` | **测试面板 UI**（实时进度与日志） |
| `python tests/tools/chart_compare.py` | 跑流水线并输出 `_chart_test.html` |
| `python tests/tools/github/create_issues.py` | 从系统测试报告批量创建 GitHub Issue |
| `python tests/tools/github/close_issues.py` | 关单并附评论（维护用） |

## 与 `scripts/` 的关系

`scripts/` 仅保留向后兼容的薄封装，新测试请一律放入 `tests/`。

| 旧命令 | 新命令 |
|--------|--------|
| `python scripts/run_pipeline_test.py` | `python tests/run.py --integration` |
| `python scripts/test_live_fetch.py` | 外部数据源手动冒烟（或 `python tests/run.py --external`） |
| `python scripts/test_llm_json_fix.py` | `pytest tests/unit/test_llm_json.py` |
| `python scripts/regression_test.py` | `python tests/run.py --fast` |
