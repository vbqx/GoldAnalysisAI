"""Extended dashboard components — institutional + strategy map (white theme)."""

from __future__ import annotations

import html
from typing import Any

from src.analysis.report_engine import parse_risk_events_calendar
from src.config import GITHUB_REPO, PROJECT_NAME
from src.viz.display_labels import NARRATIVE_SOURCE_CN, conclusion_display_lines, execution_banner, format_report_branding, humanize_narrative_fallback, infer_trade_theme, label_action
from src.viz.source_labels import render_source_badge, stage_source

_SOURCE_LABELS = {
    "jin10_flash": "金十快讯",
    "jin10_news": "金十资讯",
    "jin10_calendar": "金十财经日历",
    "tradingview_social": "TV Ideas/Minds",
    "tradingview_dxy": "TV DXY",
    "placeholder": "占位/回退",
}


def _is_placeholder_source(src: str) -> bool:
    return src == "placeholder" or src.endswith("_placeholder") or "placeholder" in src.lower()

DASHBOARD_CSS = """
<style>
/* ── Streamlit 全局（各页面共用） ── */
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1440px; }
[data-testid="stSidebar"] { background: #f8fafc; }
[data-testid="stSidebar"] .block-container { padding-top: 1.25rem; }
iframe { border: none; display: block; }

/* ── 页面标题区 ── */
.page-hero {
  background: linear-gradient(135deg, #fff7ed 0%, #ffffff 55%);
  border: 1px solid #fed7aa;
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 16px;
}
.page-hero h1 { font-size: 1.45rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0; }
.page-hero p { font-size: 0.88rem; color: #64748b; margin: 0; line-height: 1.5; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: transparent; border-bottom: 1px solid #e2e8f0; }
.stTabs [data-baseweb="tab"] {
  height: 40px; padding: 0 16px; border-radius: 8px 8px 0 0;
  font-size: 0.92rem; font-weight: 600; color: #64748b;
}
.stTabs [aria-selected="true"] { color: #0f172a; background: #fff7ed; border: 1px solid #fed7aa; border-bottom-color: #fff7ed; }

/* ── 卡片分区 ── */
.section-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px 18px;
  margin-bottom: 16px;
}
.section-card h3 { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin: 0 0 12px 0; }

.report-title { font-size: 1.35rem; font-weight: 700; color: #0f172a; margin: 0 0 4px 0; }
.report-title.center { color: #0f172a; text-align: center; font-size: 1.5rem; }
.report-subtitle { text-align: center; color: #64748b; font-size: 0.9rem; margin: 0 0 12px; line-height: 1.5; }
.report-meta { font-size: 0.8rem; color: #64748b; margin-bottom: 12px; line-height: 1.35; }
.report-hint { font-size: 0.68rem; color: #94a3b8; margin: 0 0 4px 0; }

/* ── 机构报告顶栏 / 底栏（专用 class，不影响短线策略页） ── */
.header-metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;
  margin-bottom: 6px;
}
.top-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;
  margin-bottom: 6px;
}
.bottom-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr 1fr 1fr;
  gap: 6px;
  margin-top: 6px;
  margin-bottom: 4px;
}
@media (max-width: 1100px) {
  .header-metrics, .top-grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .bottom-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

.hbox {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 6px 8px;
  min-height: 0;
  box-shadow: 0 1px 2px rgba(15,23,42,0.04);
}
.hbox.panel { min-height: 0; overflow: auto; }
.hbox.panel.top-cell {
  height: 170px;
  min-height: 170px;
  max-height: 170px;
  overflow-y: auto;
  box-sizing: border-box;
  margin: 0;
}
.hbox.panel.top-cell .lbl { font-size: 0.78rem; color: #475569; margin: 0 0 4px 0; font-weight: 700; flex-shrink: 0; }
.hbox.panel.top-cell .bullet-list { font-size: 0.78rem; line-height: 1.48; color: #1e293b; margin: 0; }
.hbox.panel.top-cell .bullet-list li { margin-bottom: 3px; }
.hbox.panel.top-cell .bullet-list b { font-size: 0.82rem; color: #0f172a; }
.report-top-row-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) [data-testid="stVerticalBlockBorderWrapper"] {
  min-height: 170px;
  box-sizing: border-box;
}
.report-top-row-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(4) .stPlotlyChart {
  margin-top: 0 !important;
}
.hbox.panel .lbl { font-size: 0.78rem; color: #475569; margin: 0 0 4px 0; font-weight: 700; }
.hbox.panel .bullet-list { font-size: 0.78rem; line-height: 1.48; color: #1e293b; }
.hbox.panel .bullet-list li { margin-bottom: 3px; }
.hbox.panel .bullet-list b { font-size: 0.82rem; color: #0f172a; }
.hbox .lbl { font-size: 10px; color: #64748b; margin: 0 0 2px 0; font-weight: 600; }
.hbox .val { font-size: 1rem; font-weight: 700; margin: 0; line-height: 1.2; color: #0f172a; }
.hbox .val.sm { font-size: 0.75rem; font-weight: 500; line-height: 1.45; color: #334155; word-break: break-word; }
.hbox .bear { color: #dc2626; }
.hbox .bull { color: #16a34a; }

.panel-box {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 8px;
  font-size: 12px;
  color: #334155;
  line-height: 1.55;
}
.panel-box h4 { margin: 0 0 8px; font-size: 13px; color: #0f172a; display: flex; align-items: center; gap: 8px; }
.panel-box.compact {
  padding: 6px 8px;
  margin-bottom: 0;
  font-size: 0.72rem;
  line-height: 1.45;
  border-radius: 6px;
  max-height: 118px;
  overflow: auto;
}
.panel-box.compact h4 { margin: 0 0 4px; font-size: 0.78rem; gap: 6px; }
.panel-box.span-2 { grid-column: 1 / -1; }
.num-badge { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; background: #0f172a; color: #fff; font-weight: 700; font-size: 12px; border-radius: 4px; flex-shrink: 0; }

.level-ladder { display: flex; flex-direction: column; gap: 6px; }
.level-item { border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 10px; text-align: center; background: #fff; }
.level-item.resistance { border-color: #fca5a5; background: #fff5f5; }
.level-item.support { border-color: #86efac; background: #f0fdf4; }
.level-item .price { font-size: 1.25rem; font-weight: 700; color: #0f172a; }
.level-item .lbl { font-size: 11px; color: #64748b; margin-top: 2px; }

.tf-panel {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 5px;
  padding: 5px 7px;
  margin-bottom: 4px;
  font-size: 0.68rem;
  line-height: 1.4;
  color: #334155;
}
.tf-panel h4 { margin: 0 0 3px; font-size: 0.72rem; color: #0f172a; }
.tf-stack { display: flex; flex-direction: column; gap: 4px; }
.tf-multi-section-h { margin: 0 0 2px !important; }
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] {
  gap: 0.35rem !important;
  align-items: stretch;
  margin-bottom: 2px;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="stVerticalBlockBorderWrapper"] {
  padding: 0 !important;
  gap: 0 !important;
  overflow: hidden;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"] {
  gap: 0 !important;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="element-container"],
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"],
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="stMarkdown"] {
  margin: 0 !important;
  padding: 0 !important;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="stMarkdown"] p {
  margin: 0 !important;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] [data-testid="stIframe"] {
  margin: 0 !important;
  padding: 0 !important;
  min-height: 0 !important;
}
.tf-main-row-anchor + div[data-testid="stHorizontalBlock"] {
  gap: 0.5rem !important;
  margin-top: 0 !important;
}
.tf-main-row-anchor + div[data-testid="stHorizontalBlock"] .section-h.tight {
  margin-top: 0 !important;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] iframe {
  display: block;
  margin: 0 !important;
  padding: 0 !important;
  line-height: 0;
  vertical-align: top;
  min-height: 0 !important;
}
.tf-col-label {
  margin: 0;
  padding: 3px 8px;
  font-size: 0.68rem;
  font-weight: 700;
  color: #475569;
  line-height: 1.15;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] .tf-panel {
  margin: 0;
  border: none;
  border-top: 1px solid #e2e8f0;
  border-radius: 0;
  padding: 3px 8px 4px;
  font-size: 0.65rem;
  line-height: 1.28;
  background: #fff;
}
.tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] .tf-panel h4 {
  margin: 0 0 2px;
  font-size: 0.68rem;
}
.tf-mini-block { margin-bottom: 2px; }
.tf-mini-block .chart-box-title { margin-bottom: 0; padding: 3px 6px; font-size: 0.7rem; }
.tf-mini-block .tf-panel { margin-top: 2px; margin-bottom: 0; padding: 4px 6px; font-size: 0.66rem; }

.plan-stack { display: flex; flex-direction: column; gap: 5px; }
.plan-stack-note {
  border: 1px dashed #cbd5e1;
  border-radius: 6px;
  padding: 7px 9px;
  color: #64748b;
  font-size: 0.7rem;
  line-height: 1.45;
  background: #f8fafc;
}
.plan-stack-note.warn {
  border-color: #fcd34d;
  background: #fffbeb;
  color: #92400e;
}
.plan-card.unauthorized { opacity: 0.92; }
.plan-card.unauthorized .head { filter: saturate(0.75); }
.plan-card { border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden; font-size: 0.68rem; background: #fff; }
.plan-card.short.is-primary { border-color: #dc2626; box-shadow: 0 0 0 1px rgba(220,38,38,0.18); }
.plan-card.long.is-primary { border-color: #16a34a; box-shadow: 0 0 0 1px rgba(22,163,74,0.18); }
.plan-card.invalid { opacity: 0.78; }
.plan-card .head {
  display: flex; align-items: center; justify-content: space-between; gap: 6px;
  padding: 5px 8px; font-weight: 700; color: #fff; font-size: 0.7rem; line-height: 1.25;
}
.plan-card .head-title { flex: 1; min-width: 0; text-align: left; }
.plan-card .head-badges { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }
.plan-card .body { padding: 6px 8px; background: #fff; line-height: 1.45; }
.plan-card .body b { color: #475569; font-weight: 600; }
.plan-card .plan-grid {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px 8px; margin-bottom: 5px;
}
.plan-card .plan-grid .k { color: #64748b; font-size: 0.62rem; font-weight: 700; }
.plan-card .plan-grid .v { color: #0f172a; font-size: 0.72rem; font-weight: 700; word-break: break-word; }
.plan-card.short .plan-grid .direction-v { color: #dc2626; }
.plan-card.long .plan-grid .direction-v { color: #16a34a; }
.plan-card .plan-meta { color: #64748b; font-size: 0.66rem; line-height: 1.4; }
.plan-card .confidence-pill {
  display: inline-flex; align-items: center; border-radius: 999px;
  padding: 1px 7px; font-size: 0.62rem; font-weight: 800; color: #0f172a; background: rgba(255,255,255,0.92);
}
.plan-card.short .head { background: linear-gradient(135deg, #dc2626, #b91c1c); }
.plan-card.short.alt .head { background: linear-gradient(135deg, #991b1b, #7f1d1d); }
.plan-card.long .head { background: linear-gradient(135deg, #16a34a, #15803d); }
.plan-card.long.alt .head { background: linear-gradient(135deg, #166534, #14532d); }
.decision-summary {
  display: grid;
  grid-template-columns: 1.05fr 1.3fr 1.25fr 1.4fr;
  gap: 8px;
  margin-bottom: 10px;
}
.final-decision-banner {
  border-radius: 8px;
  padding: 10px 12px;
  margin: 0 0 10px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
}
.final-decision-banner.execute {
  border-color: #86efac;
  background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
}
.final-decision-banner.reduce {
  border-color: #fcd34d;
  background: linear-gradient(135deg, #fffbeb, #fefce8);
}
.final-decision-banner.wait {
  border-color: #cbd5e1;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}
.final-decision-banner .fd-title {
  margin: 0;
  color: #0f172a;
  font-size: 0.92rem;
  font-weight: 800;
  line-height: 1.35;
}
.final-decision-banner .fd-verdict {
  font-size: 1rem;
}
.final-decision-banner.execute .fd-verdict { color: #15803d; }
.final-decision-banner.reduce .fd-verdict { color: #b45309; }
.final-decision-banner.wait .fd-verdict { color: #475569; }
.final-decision-banner .fd-sub {
  margin: 5px 0 0;
  color: #64748b;
  font-size: 0.72rem;
  line-height: 1.45;
}
.decision-cell {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  padding: 9px 11px;
  min-width: 0;
  box-shadow: 0 1px 2px rgba(15,23,42,0.04);
}
.decision-cell .k { margin: 0 0 3px; color: #64748b; font-size: 0.66rem; font-weight: 700; text-transform: uppercase; }
.decision-cell .v { margin: 0; color: #0f172a; font-size: 0.95rem; font-weight: 800; line-height: 1.22; word-break: break-word; }
.decision-cell .s { margin: 4px 0 0; color: #64748b; font-size: 0.7rem; line-height: 1.35; }
.decision-cell.direction-short { border-left: 4px solid #dc2626; }
.decision-cell.direction-long { border-left: 4px solid #16a34a; }
.decision-cell.direction-short .v { color: #dc2626; }
.decision-cell.direction-long .v { color: #16a34a; }
.decision-cell.direction-neutral { border-left: 4px solid #64748b; }
.status-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 0.66rem;
  font-weight: 800;
  line-height: 1.35;
  color: #fff;
}
.status-pill.active { background: #16a34a; }
.status-pill.watch { background: #d97706; }
.status-pill.candidate { background: #64748b; }
.status-pill.invalid { background: #94a3b8; }
.signal-mini-badge {
  font-size: 10px;
  margin-left: 6px;
}
.signal-mini-badge.alt { color: #64748b; }
.signal-mini-badge.primary { color: #0ea5e9; }
.signal-mini-badge.llm { color: #7c3aed; }
.primary-plan-focus {
  border: 1px solid #e2e8f0;
  border-left: 4px solid #64748b;
  border-radius: 7px;
  background: #fff;
  padding: 10px 12px;
  margin: 0 0 10px;
  box-shadow: 0 1px 2px rgba(15,23,42,0.04);
}
.primary-plan-focus.short { border-left-color: #dc2626; }
.primary-plan-focus.long { border-left-color: #16a34a; }
.primary-plan-focus.invalid { opacity: 0.78; background: #f8fafc; }
.primary-plan-focus .focus-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
.primary-plan-focus .focus-title { margin: 0; color: #0f172a; font-size: 0.95rem; font-weight: 800; line-height: 1.25; }
.primary-plan-focus .focus-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px; }
.primary-plan-focus .focus-item { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px; min-width: 0; }
.primary-plan-focus .focus-item .k { margin: 0 0 2px; color: #64748b; font-size: 0.62rem; font-weight: 700; }
.primary-plan-focus .focus-item .v { margin: 0; color: #0f172a; font-size: 0.76rem; font-weight: 700; line-height: 1.28; word-break: break-word; }
.primary-plan-focus .focus-note { color: #475569; font-size: 0.72rem; line-height: 1.45; margin: 8px 0 0; }
.run-mode-guide {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin: 0 0 12px;
}
.run-mode-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  padding: 10px 12px;
  min-width: 0;
}
.run-mode-card .name { margin: 0 0 4px; color: #0f172a; font-size: 0.88rem; font-weight: 800; }
.run-mode-card .desc { margin: 0; color: #64748b; font-size: 0.74rem; line-height: 1.45; }
.run-mode-card.recommended { border-left: 4px solid #0ea5e9; }
.run-mode-card.fast { border-left: 4px solid #64748b; }
.run-mode-card.deep { border-left: 4px solid #7c3aed; }
.agent-stage-summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
  margin: 8px 0 14px;
}
.agent-stage-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 7px;
  padding: 9px 11px;
  min-width: 0;
  box-shadow: 0 1px 2px rgba(15,23,42,0.04);
}
.agent-stage-card.llm { border-left: 4px solid #7c3aed; }
.agent-stage-card.rule { border-left: 4px solid #64748b; }
.agent-stage-card .stage-title { display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-bottom: 5px; }
.agent-stage-card .stage-title b { color: #0f172a; font-size: 0.78rem; line-height: 1.25; }
.agent-stage-card .stage-main { color: #0f172a; font-size: 0.82rem; font-weight: 800; line-height: 1.3; margin: 0 0 4px; word-break: break-word; }
.agent-stage-card .stage-sub { color: #64748b; font-size: 0.68rem; line-height: 1.4; margin: 0; word-break: break-word; }
@media (max-width: 1100px) {
  .decision-summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .primary-plan-focus .focus-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .run-mode-guide { grid-template-columns: 1fr; }
  .agent-stage-summary { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 720px) {
  .block-container { padding: 0.75rem 0.85rem 1.5rem; }
  .page-hero { padding: 10px 12px; margin-bottom: 10px; border-radius: 7px; }
  .page-hero h1 { font-size: 1.15rem; line-height: 1.25; }
  .page-hero p { font-size: 0.78rem; }
  .stTabs [data-baseweb="tab-list"] {
    overflow-x: auto;
    flex-wrap: nowrap;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    height: 36px;
    padding: 0 10px;
    white-space: nowrap;
    font-size: 0.82rem;
  }
  .header-metrics, .top-grid-4, .bottom-grid { grid-template-columns: 1fr; }
  .decision-summary, .primary-plan-focus .focus-grid { grid-template-columns: 1fr; }
  .agent-stage-summary { grid-template-columns: 1fr; }
  .primary-plan-focus .focus-head { align-items: flex-start; flex-direction: column; }
  .hbox.panel.top-cell {
    height: auto;
    min-height: 0;
    max-height: none;
  }
  .panel-box.compact {
    max-height: none;
  }
  .report-top-row-anchor + div[data-testid="stHorizontalBlock"],
  .tf-multi-row-anchor + div[data-testid="stHorizontalBlock"],
  .tf-main-row-anchor + div[data-testid="stHorizontalBlock"],
  .strategy-layout-anchor + div[data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    gap: 0.55rem !important;
  }
  .report-top-row-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
  .tf-multi-row-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
  .tf-main-row-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
  .strategy-layout-anchor + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    width: 100% !important;
    flex: 1 1 auto !important;
  }
  .tf-main-row-anchor + div[data-testid="stHorizontalBlock"] .stIframe,
  .strategy-layout-anchor + div[data-testid="stHorizontalBlock"] .stIframe {
    max-width: 100%;
  }
}
.tf-panel .bear { color: #dc2626; font-weight: 600; }
.tf-panel .bull { color: #16a34a; font-weight: 600; }
.narrative-section { position: relative; padding-top: 2px; font-size: .72rem; line-height: 1.42; }
.narrative-line { margin: 2px 0; color: #334155; }
.narrative-line b { color: #0f172a; }
.narrative-价位 b { color: #b45309; }
.narrative-条件 b { color: #0369a1; }
.narrative-失效 b { color: #b91c1c; }
.narrative-source { float: right; margin-left: 6px; padding: 1px 5px; border-radius: 999px; font-size: .58rem; color: #64748b; background: #f1f5f9; }
.narrative-source.llm { color: #166534; background: #dcfce7; }
.narrative-source.fallback { color: #92400e; background: #fef3c7; }
.tf-structure-text {
  margin-top: 4px;
  font-size: 0.68rem;
  line-height: 1.45;
  color: #475569;
}
.star-list li::before { content: "★ "; color: #eab308; }
.cal-item { font-size: 0.72rem; padding: 4px 0; border-bottom: 1px dashed #e2e8f0; line-height: 1.45; }

.llm-narrative-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 14px 16px;
  font-size: 0.9rem;
  line-height: 1.7;
  color: #334155;
  margin-top: 8px;
}
.llm-narrative-box p { margin: 0 0 8px; }
.llm-narrative-box p:last-child { margin-bottom: 0; }
.llm-narrative-box ul { margin: 4px 0 8px; padding-left: 20px; }
.llm-narrative-box li { margin-bottom: 6px; }
.llm-narrative-box b { color: #0f172a; }

.path-card {
  border-left: 3px solid #94a3b8;
  padding: 4px 6px;
  margin-bottom: 4px;
  font-size: 0.68rem;
  line-height: 1.4;
  background: #fafafa;
  border-radius: 0 4px 4px 0;
}
.path-card .summary { color: #64748b; margin-top: 2px; display: block; font-size: 0.65rem; }

.section-h { font-size: 14px; font-weight: 700; color: #0f172a; margin: 8px 0 6px; border-left: 3px solid #dc2626; padding-left: 8px; }
.section-h.tight { font-size: 0.78rem; margin: 0 0 3px; padding-left: 6px; }
.liq-list, .bullet-list { font-size: 12px; line-height: 1.55; color: #334155; margin: 0; padding-left: 18px; }
.liq-list li, .bullet-list li { margin-bottom: 4px; }
.mini-table { width: 100%; border-collapse: collapse; font-size: 0.68rem; }
.mini-table th, .mini-table td { border: 1px solid #e2e8f0; padding: 2px 4px; text-align: left; }
.footer-bar { background: linear-gradient(90deg, #dc2626, #b91c1c); color: #fff; padding: 8px 14px; border-radius: 6px; font-size: 12px; line-height: 1.5; margin-top: 10px; }
.footer-brand { text-align: center; margin-top: 10px; padding-top: 8px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; font-weight: 600; }
.star-list { font-size: 0.68rem; line-height: 1.45; color: #334155; margin: 0; padding-left: 0; list-style: none; }
.star-list li { margin-bottom: 3px; }
.chart-box-title { font-size: 12px; font-weight: 700; color: #0f172a; margin: 0 0 4px; padding: 6px 10px; border: 1px solid #e2e8f0; border-bottom: none; border-radius: 6px 6px 0 0; background: #f8fafc; }

.agent-source-bar { display: flex; flex-wrap: wrap; gap: 4px; align-items: center; margin-bottom: 4px; padding: 4px 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; font-size: 0.65rem; line-height: 1.35; }
.agent-mode-tag { color: #64748b; font-weight: 600; margin-right: 4px; }
.stage-chip { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; background: #fff; border: 1px solid #e2e8f0; border-radius: 4px; color: #334155; }
.src-badge { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 10px; font-weight: 700; line-height: 1.4; }
.src-badge.sm { font-size: 9px; padding: 0 5px; }
.src-badge.rule { background: #e2e8f0; color: #475569; }
.src-badge.llm { background: #ede9fe; color: #6d28d9; }
.stage-model { font-size: 10px; color: #64748b; margin-left: 4px; }
.val-with-badge { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 8px; line-height: 1.65; }

/* ── 外部数据：宽面板优先 ── */
.ext-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
@media (max-width: 900px) {
  .ext-grid { grid-template-columns: 1fr; }
}
.ext-src-chip { display: inline-block; margin-left: 6px; padding: 2px 8px; border-radius: 999px; background: #fff7ed; border: 1px solid #fed7aa; font-size: 10px; font-weight: 600; color: #9a3412; }
.ext-src-placeholder { background: #ffedd5; border-color: #fb923c; color: #c2410c; }
.ext-kind { font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; }
.external-feed h3 { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }

.trace-block:last-child { border-bottom: none; }
.step-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 8px 16px; font-size: 0.92rem; }

/* ── LLM I/O 文本区 ── */
.llm-io-block { margin-bottom: 16px; }
.llm-io-block .io-label { font-size: 0.9rem; font-weight: 600; color: #0f172a; margin: 0 0 6px 0; }
</style>
"""

# Re-export helpers from original module patterns
TF_LABELS = {
    "1h": "1H周期（大结构）",
    "4h": "4H周期（大结构）",
    "15m": "15min周期（中间结构）",
}
TREND_CN = {"bearish": ("空头", "bear"), "bullish": ("多头", "bull"), "ranging": ("震荡", "")}


def _chg_class(change: float) -> str:
    return "bear" if change < 0 else "bull"


def _truncate(text: str, n: int) -> str:
    text = str(text or "—")
    return text if len(text) <= n else text[: n - 1] + "…"


def _source_tags(sources: list[str]) -> str:
    if not sources:
        return ""
    chips = []
    for src in sources:
        if _is_placeholder_source(src):
            chips.append('<span class="ext-src-chip ext-src-placeholder">占位/回退</span>')
            continue
        label = _SOURCE_LABELS.get(src, src)
        chips.append(f'<span class="ext-src-chip">{html.escape(label)}</span>')
    return "".join(chips)


def render_external_data_panel(ext: dict[str, Any]) -> str:
    """Live external feed: DXY, headlines, calendar, TV social."""
    if not ext:
        return ""

    sources = ext.get("sources") or []
    src_html = _source_tags(sources if isinstance(sources, list) else [])

    headlines = ext.get("news_headlines") or []
    if not isinstance(headlines, list):
        headlines = []
    headline_html = "".join(
        f"<li>{html.escape(str(h))}</li>" for h in headlines[:10]
    ) or "<li>暂无匹配头条</li>"

    risk = str(ext.get("risk_events") or "—")
    if risk != "—":
        cal_rows = "".join(
            f'<div class="cal-item">{html.escape(str(e.get("time", "")))} '
            f'{e.get("flag", "")} {html.escape(str(e.get("event", "")))}</div>'
            for e in parse_risk_events_calendar(risk)
        )
        if not cal_rows:
            cal_rows = f'<div class="cal-item">{html.escape(risk[:280])}</div>'
    else:
        cal_rows = '<div class="cal-item">—</div>'

    social = html.escape(str(ext.get("social_sentiment") or "—"))
    posts = ext.get("social_posts") or []
    if not isinstance(posts, list):
        posts = []
    social_html = "".join(
        f'<li><span class="ext-kind">{html.escape(str(p.get("kind", "ideas")))}</span> '
        f'{html.escape(str(p.get("author") or "—"))}: '
        f'{html.escape(str(p.get("title") or "")[:100])}'
        f'{" · 👍" + str(p.get("likes")) if p.get("likes") else ""}</li>'
        for p in posts[:6]
    ) or "<li>暂无 TV 社区样本</li>"

    dxy = html.escape(str(ext.get("dxy_impact") or "—"))

    errors = ext.get("fetch_errors") or []
    err_html = ""
    if isinstance(errors, list) and errors:
        err_html = (
            '<p class="lbl" style="color:#b45309;margin-top:8px">拉取提示：'
            + html.escape("；".join(str(e) for e in errors[:3]))
            + "</p>"
        )

    return f"""
<div class="section-card external-feed">
  <h3>外部数据 · 实时拉取 {src_html}</h3>
  <div class="ext-grid">
    <div class="panel-box"><h4>美元指数 DXY</h4><p>{dxy}</p></div>
    <div class="panel-box"><h4>TV 社区情绪</h4><p>{social}</p><ul class="bullet-list">{social_html}</ul></div>
    <div class="panel-box span-2"><h4>新闻头条</h4><ul class="bullet-list">{headline_html}</ul></div>
    <div class="panel-box span-2"><h4>经济日历 / 事件风险</h4>{cal_rows}</div>
  </div>
  {err_html}
</div>
"""


def render_header(report: dict[str, Any]) -> str:
    m = report["metrics"]
    c = report["conclusion"]
    cls = _chg_class(m["daily_change"])

    metric_boxes = [
        ("当前价格", f"{m['current_price']:.2f}", cls),
        ("日涨跌", f"{m['daily_change']:+.2f} ({m['daily_change_pct']:+.2f}%)", cls),
        ("日高 / 日低", f"{m['daily_high']:.2f} / {m['daily_low']:.2f}", ""),
        ("市场情绪", c["market_sentiment"], cls),
    ]
    metric_html = ['<div class="header-metrics">']
    for label, val, vcls in metric_boxes:
        vc = f" {vcls}" if vcls in ("bear", "bull") else ""
        metric_html.append(f'<div class="hbox"><p class="lbl">{label}</p><p class="val{vc}">{val}</p></div>')
    metric_html.append("</div>")

    conclusion_html = ""
    return "".join(metric_html) + conclusion_html


_PLAN_LABELS = ("方案 A（主策略）", "方案 B（备选）", "方案 C（逆势）")


def _fmt_price(value: Any) -> str:
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "—"


def _primary_signal(signals: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not signals:
        return None
    for sig in signals:
        if sig.get("signal_role") == "primary":
            return sig
    return signals[0]


def _status_meta(status: str) -> tuple[str, str]:
    status_map = {
        "active": ("已触发", "active"),
        "watch": ("等待触发", "watch"),
        "candidate": ("候选区", "candidate"),
        "invalid": ("已失效", "invalid"),
    }
    return status_map.get(status, status_map["candidate"])


def _direction_class(signal: dict[str, Any] | None, conclusion: dict[str, Any]) -> str:
    if signal:
        theme = infer_trade_theme(
            theme=str(signal.get("theme") or ""),
            direction=str(signal.get("direction") or ""),
            direction_cn=str(signal.get("direction_cn") or ""),
        )
        return f"direction-{theme}"
    raw = str(conclusion.get("market_sentiment") or "").lower()
    if raw in ("short", "bear", "bearish") or "空" in raw or "跌" in raw:
        return "direction-short"
    if raw in ("long", "bull", "bullish") or "多" in raw or "涨" in raw:
        return "direction-long"
    return "direction-neutral"


def _signal_zone(sig: dict[str, Any]) -> str:
    return f"{_fmt_price(sig.get('entry_low'))} - {_fmt_price(sig.get('entry_high'))}"


def _signal_targets(sig: dict[str, Any]) -> str:
    targets = sig.get("take_profits") or []
    if not targets:
        return "—"
    return " / ".join(_fmt_price(x) for x in targets[:3])


def _first_text(items: list[Any], fallback: str = "—") -> str:
    for item in items:
        text = str(item or "").strip()
        if text:
            return text
    return fallback


def render_final_decision_banner(report: dict[str, Any]) -> str:
    """Prominent one-line verdict: execute / reduce / wait."""
    meta = report.get("meta") or {}
    final = meta.get("final_decision")
    if not final and meta.get("manager_decision"):
        from src.analysis.report_engine import build_final_decision_meta

        final = build_final_decision_meta(report)
    if not final:
        return ""

    authorized = bool(final.get("execution_authorized"))
    action = str(final.get("action") or "wait").lower()
    css = "execute" if action == "execute" else "reduce" if action == "reduce" else "wait"
    verdict = html.escape(str(final.get("verdict_cn") or label_action(action)))

    if authorized:
        plan = final.get("primary_plan") or {}
        direction = html.escape(str(plan.get("direction_cn") or "—"))
        zone = html.escape(str(plan.get("zone") or "—"))
        detail = f"{direction} · 入场 {zone}"
        pos = str(plan.get("position_size") or "").strip()
        if pos:
            detail += f" · {html.escape(pos)}"
        sub = "以下为授权主方案；计划卡与叙述与之对应，可按触发条件执行。"
    else:
        detail = "不执行交易"
        summary = str(final.get("summary") or "").strip()
        sub = summary or "候选方案与结构叙述仅供观察，不可当作下单依据。"
        if final.get("observation_mode"):
            sub = f"快照观察模式 · {sub}"

    return f"""
<div class="final-decision-banner {css}">
  <p class="fd-title"><span class="fd-verdict">{verdict}</span> · {detail}</p>
  <p class="fd-sub">{html.escape(sub)}</p>
</div>
"""


def render_decision_summary(report: dict[str, Any]) -> str:
    """First-screen decision strip: price, bias, executable state, and main risk."""
    metrics = report.get("metrics", {})
    conclusion = report.get("conclusion", {})
    meta = report.get("meta") or {}
    signals = report.get("signals") or []
    execution_authorized = bool(meta.get("execution_authorized"))
    primary = _primary_signal(signals) if execution_authorized else None
    status = str((primary or {}).get("status") or "candidate")
    status_label, status_cls = _status_meta(status)
    if not execution_authorized:
        status_label, status_cls = "未授权", "invalid"
    direction_cls = _direction_class(primary, conclusion)
    price = _fmt_price(metrics.get("current_price"))
    change = (
        f"{float(metrics.get('daily_change', 0)):+.2f} ({float(metrics.get('daily_change_pct', 0)):+.2f}%)"
        if metrics
        else "—"
    )
    direction = html.escape(
        str((primary or {}).get("direction_cn") or conclusion.get("market_sentiment") or "—")
    )
    plan_name = html.escape(
        str((primary or {}).get("name") or label_action(meta.get("manager_decision", {}).get("action", "wait")))
    )
    trigger = html.escape(
        str((primary or {}).get("trigger_note") or execution_banner(meta) or "等待交易假设确认")
    )
    risk_items = list(report.get("invalidation", []) or []) + list(
        report.get("risk_control", []) or []
    )
    risk_text = html.escape(
        _first_text(
            risk_items,
            "暂无明确失效条件",
        )
    )
    debate_badge = render_source_badge(stage_source(report, "debate"), small=True)
    manager_badge = render_source_badge(stage_source(report, "manager"), small=True)

    return f"""
<div class="decision-summary">
  <div class="decision-cell">
    <p class="k">XAUUSD</p>
    <p class="v">{price}</p>
    <p class="s">日内 {html.escape(change)}</p>
  </div>
  <div class="decision-cell {direction_cls}">
    <p class="k">方向判断 {debate_badge}</p>
    <p class="v">{direction}</p>
    <p class="s">{html.escape(str(conclusion.get("direction_summary", "—")))}</p>
  </div>
  <div class="decision-cell">
    <p class="k">主计划状态 {manager_badge}</p>
    <p class="v">{plan_name} <span class="status-pill {status_cls}">{status_label}</span></p>
    <p class="s">{trigger}</p>
  </div>
  <div class="decision-cell">
    <p class="k">失效/风险</p>
    <p class="v">{risk_text}</p>
    <p class="s">先确认状态，再看入场区和止损。</p>
  </div>
</div>
"""


def _display_plan_signals(signals: list[dict[str, Any]], *, limit: int = 3) -> list[dict[str, Any]]:
    """Up to three plans for UI; invalid plans sink to the end but still show when needed."""
    eligible = [sig for sig in signals if sig.get("status") != "invalid"]
    rest = [sig for sig in signals if sig.get("status") == "invalid"]
    return (eligible + rest)[:limit]


def _confidence_text(sig: dict[str, Any]) -> str:
    score = sig.get("score_total")
    grade = sig.get("score_grade")
    if score is None and not grade:
        return "—"
    score_txt = f"{float(score):.0f}分" if score is not None else "—"
    grade_txt = str(grade) if grade else "—"
    return f"{score_txt} · {grade_txt}级"


def _render_plan_card(
    sig: dict[str, Any],
    *,
    plan_label: str,
    is_primary: bool = False,
    unauthorized: bool = False,
) -> str:
    role = sig.get("signal_role", "primary")
    css_theme = infer_trade_theme(
        theme=str(sig.get("theme") or ""),
        direction=str(sig.get("direction") or ""),
        direction_cn=str(sig.get("direction_cn") or ""),
    )
    alt = " alt" if role == "alternate" and not unauthorized else ""
    status = str(sig.get("status") or "candidate")
    status_label, status_cls = _status_meta(status)
    invalid_cls = " invalid" if status == "invalid" else ""
    primary_cls = " is-primary" if is_primary and not unauthorized else ""
    unauth_cls = " unauthorized" if unauthorized else ""
    weight = html.escape(str(sig.get("sentiment_bias_pct", sig.get("win_rate", "—"))))
    trigger_note = html.escape(str(sig.get("trigger_note") or "等待触发确认"))
    reasons = sig.get("score_reasons") or []
    reason_text = "；".join(html.escape(str(x)) for x in reasons[:2])
    source_badge = (
        '<span class="signal-mini-badge llm">LLM</span>'
        if str(sig.get("setup_type", "")).startswith("llm_")
        else ""
    )
    role_badge = ""
    if unauthorized:
        role_badge = '<span class="signal-mini-badge alt">未授权</span>'
    elif is_primary:
        role_badge = '<span class="signal-mini-badge primary">主</span>'
    elif role == "alternate":
        role_badge = '<span class="signal-mini-badge alt">备</span>'
    title = html.escape(str(sig.get("name") or plan_label))
    plan_name = html.escape(plan_label)
    direction = html.escape(str(sig.get("direction_cn") or sig.get("direction") or "—"))
    confidence = html.escape(_confidence_text(sig))
    note = html.escape(str(sig.get("note") or ""))

    return f"""
<div class="plan-card {css_theme}{alt}{invalid_cls}{primary_cls}{unauth_cls}">
  <div class="head">
    <div class="head-title">{plan_name} · {title}</div>
    <div class="head-badges">
      <span class="confidence-pill">置信 {confidence}</span>
      {role_badge}{source_badge}
      <span class="status-pill {status_cls}">{status_label}</span>
    </div>
  </div>
  <div class="body">
    <div class="plan-grid">
      <div><div class="k">方向</div><div class="v direction-v">{direction}</div></div>
      <div><div class="k">入场区</div><div class="v">{_signal_zone(sig)}</div></div>
      <div><div class="k">止损</div><div class="v">{_fmt_price(sig.get('stop_loss'))}</div></div>
      <div><div class="k">目标</div><div class="v">{_signal_targets(sig)}</div></div>
    </div>
    <div class="plan-meta"><b>盈亏比：</b>{html.escape(str(sig.get('risk_reward', '—')))} · <b>结构权重：</b>{weight}</div>
    <div class="plan-meta"><b>触发：</b>{trigger_note}{(' · ' + note) if note else ''}</div>
    {f'<div class="plan-meta">{reason_text}</div>' if reason_text else ''}
  </div>
</div>"""


def render_primary_plan_focus(report: dict[str, Any]) -> str:
    """Backward-compatible wrapper: first plan card only."""
    signals = _display_plan_signals(report.get("signals") or [])
    if not signals:
        return '<div class="plan-stack"><p>暂无交易计划</p></div>'
    primary_idx = next(
        (i for i, sig in enumerate(signals) if sig.get("signal_role") == "primary"),
        0,
    )
    label = _PLAN_LABELS[primary_idx] if primary_idx < len(_PLAN_LABELS) else _PLAN_LABELS[0]
    return f'<div class="plan-stack">{_render_plan_card(signals[primary_idx], plan_label=label, is_primary=True)}</div>'


def render_top_overview_row(report: dict[str, Any]) -> str:
    """Top row: overview | (donut slot) | liquidity | today — 4 columns, 3 HTML panels."""
    overview = report.get("market_overview", [])
    liq = report.get("liquidity", [])[:5]
    c = report["conclusion"]
    debate_src = stage_source(report, "debate")
    debate_badge = render_source_badge(debate_src, small=True)
    conclusion_items = "".join(
        f"<li>{html.escape(line)}</li>" for line in conclusion_display_lines(c)
    )

    ov_html = "".join(f"<li>{html.escape(str(x))}</li>" for x in overview[:5])
    liq_html = "".join(
        f"<li>[{html.escape(str(item['timeframe']))}] <b>{item['price']:.0f}</b> {html.escape(str(item['label'])[:18])}</li>"
        for item in liq
    )

    return f"""
<div class="top-grid-4">
  <div class="hbox panel"><p class="lbl">📊 市场总览</p><ul class="bullet-list">{ov_html or "<li>—</li>"}</ul></div>
  <div class="hbox panel donut-slot"><p class="lbl">📈 多空结构权重</p><p class="val sm" style="color:#94a3b8">← 右侧图表</p></div>
  <div class="hbox panel"><p class="lbl">💧 关键流动性</p><ul class="bullet-list">{liq_html or "<li>—</li>"}</ul></div>
  <div class="hbox panel"><p class="lbl">⚡ 结论与要点 {debate_badge}</p><ul class="bullet-list">
    {conclusion_items}
  </ul></div>
</div>
"""


def render_tf_stack(report: dict[str, Any]) -> str:
    panels = "".join(
        render_tf_panel(tf, report["timeframes"][tf], compact=True)
        for tf in ("4h", "1h", "15m")
    )
    return f'<div class="tf-stack">{panels}</div>'


def render_bottom_row(report: dict[str, Any], conclusion: dict[str, Any]) -> str:
    fib = report.get("fibonacci", [])
    fib_head = "".join(f"<th>{html.escape(str(h))}</th>" for h in ("比例", "价位", "含义"))
    fib_body = "".join(
        f"<tr><td>{f['ratio']:.3f}</td><td>{f['price']}</td><td>{html.escape(str(f['significance']))}</td></tr>"
        for f in fib[:5]
    )
    paths = report.get("path_summary", [])
    path_html = "".join(
        f'<div class="path-card" style="border-color:{p["color"]}">'
        f'<b>{p["id"]} · 结构权重 {p["probability"]}%</b> {html.escape(str(p["name"]))}'
        f'<span class="summary">{html.escape(str(p.get("summary", "")))}</span></div>'
        for p in paths[:3]
    )
    risk_items = list(report.get("risk_control", [])) + list(report.get("invalidation", []))
    risk_html = "".join(f"<li>{html.escape(str(r))}</li>" for r in risk_items[:5])
    stars = "".join(f"<li>{html.escape(str(s))}</li>" for s in conclusion.get("starred", [])[:4])

    return f"""
<div class="bottom-grid">
  <div class="panel-box compact"><h4>Fib 回调参考 <span style="font-size:10px;color:#94a3b8;font-weight:normal">（展示权重非统计概率）</span></h4>
    <table class="mini-table"><thead><tr>{fib_head}</tr></thead><tbody>{fib_body}</tbody></table>
  </div>
  <div class="panel-box compact"><h4>未来走势推演</h4>{path_html or "<p>—</p>"}</div>
  <div class="panel-box compact"><h4>风控与失效</h4><ul class="bullet-list">{risk_html or "<li>—</li>"}</ul></div>
  <div class="panel-box compact"><h4>最终结论</h4><ul class="star-list">{stars or "<li>—</li>"}</ul></div>
</div>
"""


def _fmt_zone(items: list[dict], direction: str | None = None, *, limit: int = 5) -> str:
    filtered = [i for i in items if not direction or i.get("direction") == direction]
    if not filtered:
        return "—"
    return " / ".join(f"{i['low']:.0f}-{i['high']:.0f}" for i in filtered[:limit])


def _fmt_event_list(items: list[dict]) -> str:
    if not items:
        return "—"
    return " / ".join(i.get("label", f"@{i.get('price', 0):.0f}") for i in items)


def _fmt_prices(prices: list[float]) -> str:
    if not prices:
        return "—"
    return " / ".join(f"{p:.0f}" for p in prices)


def _fmt_strong_weak(info: dict[str, Any]) -> str:
    parts: list[str] = []
    if info.get("strong_high") is not None:
        parts.append(f"Strong H {info['strong_high']:.0f}")
    if info.get("weak_high") is not None:
        parts.append(f"Weak H {info['weak_high']:.0f}")
    if info.get("strong_low") is not None:
        parts.append(f"Strong L {info['strong_low']:.0f}")
    if info.get("weak_low") is not None:
        parts.append(f"Weak L {info['weak_low']:.0f}")
    return " · ".join(parts) if parts else "—"


def render_tf_panel(tf: str, info: dict[str, Any], *, compact: bool = False) -> str:
    label = TF_LABELS.get(tf, tf)
    trend_cn, trend_cls = TREND_CN.get(info["trend"], ("—", ""))
    pd_map = {"premium": "溢价", "discount": "折价", "equilibrium": "均衡", "unknown": "—"}
    pd_txt = pd_map.get(info.get("premium_discount", ""), "—")
    swing_txt = "—"
    if info.get("swing_low") is not None and info.get("swing_high") is not None:
        swing_txt = f"H {info['swing_high']:.0f} · L {info['swing_low']:.0f}"

    bos_line = _fmt_event_list(info.get("bos_list", []))
    choch_line = _fmt_event_list(info.get("choch_list", []))
    ob_line = _fmt_zone(info.get("order_blocks", []), limit=5)
    fvg_line = _fmt_zone(info.get("fvgs", []), limit=5)
    eqh_line = _fmt_prices(info.get("equal_highs", []))
    eql_line = _fmt_prices(info.get("equal_lows", []))
    hl_line = _fmt_strong_weak(info)

    if compact:
        return (
            f'<div class="tf-panel"><h4>{label} · <span class="{trend_cls}">{trend_cn}</span></h4>'
            f"<div>区位 {pd_txt} · Swing {swing_txt}</div>"
            f"<div>BOS {bos_line}</div>"
            f"<div>CHoCH {choch_line}</div>"
            f"<div>OB {ob_line}</div>"
            f"<div>FVG {fvg_line}</div>"
            f"<div>EQH {eqh_line} · EQL {eql_line}</div>"
            f"<div>{hl_line}</div></div>"
        )
    ema = info.get("ema_relation", {})
    ema_txt = " / ".join(f"{k}{v}" for k, v in ema.items())
    pd_map = {"premium": "溢价区", "discount": "折价区", "equilibrium": "均衡", "unknown": "—"}
    pd_txt = pd_map.get(info.get("premium_discount", ""), "—")
    ob_bear = _fmt_zone(info.get("order_blocks", []), "bearish")
    ob_bull = _fmt_zone(info.get("order_blocks", []), "bullish")
    fvg_bear = _fmt_zone(info.get("fvgs", []), "bearish")
    extra = "<div><b>执行逻辑：</b>关注反弹中位与扫流动性节点</div>" if tf == "15m" else ""
    return f"""
<div class="tf-panel">
  <h4>【{label}】</h4>
  <div>方向：<span class="{trend_cls}">{trend_cn}</span></div>
  <div>BOS：{info.get('bos', '无')} | CHoCH：{info.get('choch', '无')}</div>
  <div>聪明钱：{pd_txt} | 成交量：{info.get('volume_signal', 'N/A')}</div>
  <div>看跌 OB：{ob_bear} | FVG：{fvg_bear}</div>
  {f'<div>看涨 OB：{ob_bull}</div>' if ob_bull != '—' else ''}
  {extra}
</div>
"""


def render_narrative_section(section: dict[str, Any] | None) -> str:
    """Render one compact institutional-copy block from the shared contract."""
    section = section or {}
    source = str(section.get("source") or "rule")
    source_text = NARRATIVE_SOURCE_CN.get(source, "规则")
    source_cls = "llm" if source == "llm" else ("fallback" if source == "fallback" else "rule")
    rows: list[tuple[str, str]] = []
    if summary := str(section.get("summary") or "").strip():
        rows.append(("状态", summary))
    for value in section.get("context") or []:
        if text := str(value).strip():
            rows.append(("结构", text))
    for value in section.get("levels") or []:
        if text := str(value).strip():
            rows.append(("价位", text))
    for value in section.get("conditions") or []:
        if text := str(value).strip():
            rows.append(("条件", text))
    if invalidation := str(section.get("invalidation") or "").strip():
        rows.append(("失效", invalidation))
    body = "".join(
        f'<div class="narrative-line narrative-{html.escape(kind)}"><b>{html.escape(kind)}：</b>{html.escape(text)}</div>'
        for kind, text in rows[:6]
    )
    return (
        f'<div class="narrative-section"><span class="narrative-source {source_cls}">{source_text}</span>'
        f'{body or "<div class=\"narrative-line\">数据不足，等待确认。</div>"}'
        f'{_narrative_fallback_hint(section)}</div>'
    )


def _narrative_fallback_hint(section: dict[str, Any]) -> str:
    if str(section.get("source") or "") != "fallback":
        return ""
    reason = humanize_narrative_fallback(str(section.get("fallback_reason") or "").strip())
    if not reason:
        return ""
    return f'<div class="plan-stack-note" style="margin-top:4px">兜底原因：{html.escape(reason[:120])}</div>'


def render_key_levels(levels: list[dict]) -> str:
    items = []
    for lv in levels:
        kind = lv.get("kind", "neutral")
        css = kind if kind in ("resistance", "support") else ""
        if "price_low" in lv:
            price_txt = f"{lv['price_low']:.0f}-{lv['price_high']:.0f}"
        else:
            price_txt = f"{lv['price']:.0f}"
        items.append(
            f'<div class="level-item {css}"><div class="price">{price_txt}</div>'
            f'<div class="lbl">{lv["label"]}</div></div>'
        )
    return f'<div class="level-ladder">{"".join(items)}</div>'


def render_strategy_sections(report: dict[str, Any]) -> str:
    c = report["conclusion"]
    sections = [
        ("1 主方向", f"<p>{c['direction_summary']}。{c['action']}</p>"),
        ("2 关键压力", "<ul class='bullet-list'>" + "".join(f"<li>{x}</li>" for x in report.get("resistance_levels", [])) + "</ul>"),
        ("3 关键支撑", "<ul class='bullet-list'>" + "".join(f"<li>{x}</li>" for x in report.get("support_levels", [])) + "</ul>"),
        ("4 交易计划", render_trading_plans(report.get("signals") or [], meta=report.get("meta"))),
        ("5 关键提醒", "<ul class='bullet-list'>" + "".join(f"<li>{x}</li>" for x in report.get("risk_control", [])) + "</ul>"),
    ]
    parts = []
    for title, body in sections:
        num, label = title.split(" ", 1)
        parts.append(f'<div class="panel-box"><h4><span class="num-badge">{num}</span>{label}</h4>{body}</div>')
    return "".join(parts)



def render_path_cards(paths: list[dict]) -> str:
    return "".join(
        f'<div class="path-card" style="border-color:{p["color"]}">'
        f'<b>{p["id"]} · 结构权重 {p["probability"]}%</b> {p["name"]}</div>'
        for p in paths
    )


def render_calendar(events: list[dict]) -> str:
    if not events:
        return ""
    rows = "".join(
        f'<div class="cal-item">{html.escape(str(e.get("time", "")))} {e.get("flag", "")} {html.escape(str(e.get("event", "")))}</div>'
        for e in events
    )
    return f'<div class="panel-box"><h4>📅 宏观日历</h4>{rows}</div>'


def render_trading_plans(
    signals: list[dict],
    *,
    meta: dict | None = None,
    include_primary: bool = True,
) -> str:
    """Unified A/B/C plan cards; separates authorized vs rule-only candidates."""
    del include_primary
    meta = meta or {}
    execution_authorized = bool(meta.get("execution_authorized"))
    if execution_authorized:
        display_signals = [
            s
            for s in signals
            if s.get("signal_role") in ("primary", "alternate") and s.get("status") != "invalid"
        ][:3]
        unauthorized = False
    else:
        display_signals = _display_plan_signals(signals)
        unauthorized = True
    if not display_signals:
        return '<div class="plan-stack"><p>暂无交易计划</p></div>'
    banner = ""
    if unauthorized:
        note = html.escape(execution_banner(meta))
        banner = f'<div class="plan-stack-note warn">⚠ {note}</div>'
    cards = []
    for idx, sig in enumerate(display_signals):
        label = _PLAN_LABELS[idx] if idx < len(_PLAN_LABELS) else f"方案 {idx + 1}"
        is_primary = (not unauthorized) and sig.get("signal_role") == "primary"
        cards.append(
            _render_plan_card(sig, plan_label=label, is_primary=is_primary, unauthorized=unauthorized)
        )
    return f'<div class="plan-stack">{banner}{"".join(cards)}</div>'


def render_liquidity(items: list[dict]) -> str:
    label_map = {
        "Equal Highs / Sell-side Liquidity": "Equal Highs / 卖方流动性",
        "Equal Lows / Buy-side Liquidity": "Equal Lows / 买方流动性",
        "Stop Hunt Above Highs": "高点上方 Stop Hunt",
        "Stop Hunt Below Lows": "低点下方 Stop Hunt",
    }
    lines = []
    for item in items[:6]:
        lbl = label_map.get(item["label"], item["label"])
        lines.append(f"<li>[{item['timeframe']}] {lbl}: <b>{item['price']:.2f}</b></li>")
    return f'<ul class="liq-list">{"".join(lines)}</ul>'


def render_footer(report: dict[str, Any]) -> str:
    reminders = report.get("footer_reminders", [])
    txt = " | ".join(reminders) if reminders else "注意美盘流动性与数据波动"
    return f"""
<div class="footer-bar">📌 今日重要提醒：{txt}</div>
<div class="footer-brand">{PROJECT_NAME} · {GITHUB_REPO}</div>
"""
