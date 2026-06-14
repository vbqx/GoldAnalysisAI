# 测试用例目录

本目录存放**用例定义与测试文档**，与 `tests/unit`、`tests/regression` 等实现代码分离。

| 文件 | 说明 |
|------|------|
| [catalog.yaml](./catalog.yaml) | 用例 ID、优先级、所属套件、是否自动化、关联 Issue |

## 用例 ID 规则

| 前缀 | 含义 |
|------|------|
| `UT-*` | 单元测试 |
| `IT-*` | 集成测试（流水线、外部服务） |
| `RG-*` | 回归测试（Issue 修复项、约定检查） |
| `UI-*` | 手工 / UI 测试（待自动化） |

## 维护流程

1. 在 `catalog.yaml` 新增或更新用例条目
2. 在对应 `tests/<suite>/` 下实现或更新测试代码
3. 本地执行 `python tests/run.py` 验证
4. 关单时在 GitHub Issue 引用用例 ID（如 `RG-03`）
