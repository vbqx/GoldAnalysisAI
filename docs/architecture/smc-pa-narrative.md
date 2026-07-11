# SMC + PA 叙事组合

> Lux SMC 定结构方向与执行区；DGT 量价定价值区与成交阻力支撑。  
> 文案、LLM 与主图分层消费，见 [technical-analysis.md](./technical-analysis.md)。

---

## 1. 原则

**按场景区分主次**（与 `field_glossary.PA_SMC_PRIORITY` 一致，不得混用）：

| 场景 | 主 | 辅 |
|------|----|----|
| 报告五块叙事 | PA（POC/VAH/VAL、量价 S/R） | SMC 仅 `allowed_levels` 引用 |
| 交易计划 | PA 定入场/止损/目标区 | SMC 后台过滤，不进文案 |
| 技术 Analyst / 多空研究 | SMC（趋势/BOS/OB/FVG/流动性） | PA 确认共振、拒绝、扫过收回 |

| 层级 | 负责模块 | 回答的问题 |
|------|----------|------------|
| **SMC** | `luxalgo_smc` → `ict_pa` | 趋势、BOS/CHoCH、OB/FVG、Swing 流动性、研究侧结构方向 |
| **PA** | `dgt_price_action` | POC/VAH/VAL、量价 S/R、放量/高波动、叙事主干与计划定区 |
| **组合** | `narrative_combine` → `narrative_sections` | 同一面板内合并叙述，共振时分别点明来源 |

**不替换**：叙事与计划以 PA 为主干；研究/技术 Analyst 以 SMC 定结构，PA 不取代 SMC 方向判断。

---

## 2. 各面板组合逻辑

### 市场总览

| 行 | SMC | PA |
|----|-----|-----|
| 状态 | 4H/1H/15m 趋势众数 → 主方向 | 现价相对 5m POC/VA 位置 |
| 结构 | 多周期一致/分歧 | — |
| 价位① | 日内已走区间（1d H/L） | 同条附带 POC、VAH、VAL |
| 价位② | 主信号入场区（FVG/OB） | 检测与 VAH/VAL/量价 S/R 共振（±8 点） |

### 关键流动性

| 侧 | SMC | PA |
|----|-----|-----|
| 上方 | `report.liquidity` Swing/Strong 高点 | `price_action.5m.sr_levels` 阻力（连续/放量/高波动） |
| 下方 | 同上低点 | 同上支撑 |

合并格式：`上方：结构 4134 / 4138；量价 4136(连续量价阻力) / 4140(放量阻力)。`

### 4H / 1H / 15M 结构

| 字段 | SMC | PA |
|------|-----|-----|
| context | 溢价折价、BOS、CHoCH | 该周期 POC/VA（1h/15m 含现价区位） |
| levels | OB/FVG 或 Swing 压力支撑 | 与 SMC 区间共振时追加「与量价位共振」 |
| 15m 补充 | — | 无 SMC 压力时列近端 PA 阻力 |

---

## 3. 共振规则

实现：`src/analysis/narrative_combine.py`

```
RESONANCE_TOLERANCE = 8.0  # XAUUSD 点
```

当 SMC 区间中点与 PA 价位（VAH/VAL/POC/S/R）相差 ≤ 8 点时，文案标注共振，不合并为单一指标名。

---

## 3.1 交易计划（PA 主 + SMC 过滤）

实现：`src/analysis/plan_signals.py` → `report_engine.generate_trading_signals()`

| 方案 | PA 定什么 | SMC 仅过滤 |
|------|-----------|------------|
| A 激进反抽做空 | 最近上方量价阻力 | BOS/CHoCH 同向 +8，反向 -10；OB/FVG 共振 +6，未对齐 -4 |
| B 保守反抽做空 | VAH 拒绝区（无 VAH 则次近阻力） | 同上 |
| C 右侧扫低做多 | VAL 扫低收回（无 VAL 则量价支撑） | CHoCH 转强确认触发；结构过滤同上 |

- **不阻断**：SMC 未对齐仍输出计划，只降低 `score_total`。
- **回退**：DGT 量价不足时，用规则 PA 价位锚点（日内高低、摆动、近期极值）合成 5m PA，不再回退 SMC FVG/OB。

---

## 4. 数据流

```
build_report()
  ├─ timeframes      ← Lux SMC
  ├─ liquidity       ← Lux Swing
  ├─ price_action    ← DGT 全量计算
  ├─ signals         ← PA 主计划 + SMC 过滤评分
  └─ narrative_sections ← build_rule_narrative_sections()  # SMC+PA 组合

build_technical_context()
  └─ price_action    ← 分析师 / 技术 LLM

build_llm_context()
  ├─ technical_context（含 price_action）
  ├─ price_action（报告副本）
  └─ narrative_facts
        ├─ price_action（完整）
        ├─ price_action_summary（紧凑）
        ├─ combination_rules
        └─ allowed_levels（SMC + PA 价位白名单）
```

---

## 5. 主图 vs 文案

| 输出 | SMC | PA |
|------|-----|-----|
| 5m 主图 | OB/FVG 色块 | 仅 S/R 水平线 |
| 报告五块文案 | 主干 | 嵌入 context/levels |
| LLM | `timeframes` + `lux_timeframe_panels` | `price_action` + `price_action_summary` |

---

## 6. Volume 不可用

`price_action.volume_ok == false` 时：

- PA Profile 为空或跳过
- 连续 S/R 回退 **Price 模式**（Pine 同名逻辑）
- 文案仅保留 SMC 主干，不编造 POC

---

## 7. 相关代码

| 文件 | 职责 |
|------|------|
| `narrative_combine.py` | 组合规则常量、共振、LLM 摘要 |
| `plan_signals.py` | PA 主交易计划几何 + SMC 过滤评分 |
| `narrative_sections.py` | 规则文案五块 |
| `llm/prompts.py` | 叙事 LLM 系统提示 |
| `llm/context.py` | 叙事 LLM payload |
| `technical_context.py` | 分析师/技术阶段 `price_action` |

---

## 8. 相关文档

- [technical-analysis.md](./technical-analysis.md)
- [chart-layers.md](./chart-layers.md)
- [analyst-context.md](./analyst-context.md)
