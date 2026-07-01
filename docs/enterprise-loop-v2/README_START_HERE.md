# 漂流瓶企业级 LOOP 优化包 v2

版本：v2.0  
日期：2026-06-29  
用途：把漂流瓶项目从“可运行骨架”推进到“企业级、商业级、可验收、可多 Agent 并行接力”的执行体系。

## 为什么重做 v2

上一版只给了总任务书和基本验收。v2 增加以下关键能力：

1. **AI LOOP 标准解释**：明确 AI 中的 LOOP 不是“反复改”，而是带边界、观察、评估、反思、停止条件和证据链的智能体控制回路。
2. **强约束**：不读文档不准改；无证据不算完成；Mock 不准冒充生产；后台不准回到用户端；失败不准继续宣称完成。
3. **多子 Agent 作业系统**：拆成 10 个子 Agent，每个有输入、输出、文件边界、禁止项、验收项、并行/串行依赖。
4. **生产级验收门禁**：从 G0 到 G14，覆盖架构、RBAC、数据库、API、UI、性能、安全、可访问性、监控、文档、发布和回滚。
5. **可复制 Codex 提示词**：包含短版、完整版、每个 Agent 的子提示词。
6. **SKILL.md 模板**：给 Codex/Agents 放入本地 skills 后可用于 UI、后台、RBAC、测试、SRE、文档接力。
7. **LOOP 运行报告模板**：每轮必须填，避免“我改好了”但没有证据。

## 文件索引

| 文件 | 用途 |
| --- | --- |
| `00_CODEX_MASTER_PROMPT_ENTERPRISE_LOOP_V2.md` | 直接复制给 Codex 的总提示词，最完整。 |
| `CODEX_COPY_PROMPT_SHORT_V2.md` | 一屏短版，可先贴给 Codex。 |
| `01_AI_LOOP_STANDARD_AND_PROJECT_LOOP.md` | 解释 AI LOOP 标准，并映射到本项目。 |
| `02_MULTI_AGENT_OPERATING_SYSTEM.md` | 多 Agent 并行协作、依赖、冲突处理、交接协议。 |
| `03_AGENT_TASK_CARDS.md` | 每个 Agent 的详细任务卡。 |
| `04_PRODUCTION_ACCEPTANCE_GATES.md` | 企业级生产验收门禁。 |
| `05_LOOP_RUN_REPORT_TEMPLATE.md` | 每轮 LOOP 运行报告模板。 |
| `06_ENTERPRISE_BACKEND_ADMIN_ROADMAP.md` | 后台与管理端生产级路线图。 |
| `07_USER_EXPERIENCE_AND_COMMERCIAL_GROWTH_ROADMAP.md` | 用户体验、商业增长、扩列/房间功能路线图。 |
| `08_MONITORING_SLO_SECURITY_ACCESSIBILITY.md` | 监控、SLO、安全、可访问性标准。 |
| `09_SKILLS_REFERENCE_AND_SEARCH_KEYWORDS.md` | 推荐模板、UI 库、搜索关键词与 Skills 建议。 |
| `10_CI_CHECKLIST_AND_COMMANDS.md` | 测试命令、CI 检查、人工验收命令。 |
| `11_APPEND_TO_EXISTING_DOCS.md` | 可追加到项目 docs 的条目。 |
| `SUB_AGENTS/*.md` | 每个子 Agent 的可复制提示词。 |
| `SKILL_TEMPLATES/*.md` | 可转成本地 SKILL.md 的模板。 |
| `TABLES/acceptance_matrix.md` | 分模块验收矩阵。 |

## 使用顺序

1. 先把 `CODEX_COPY_PROMPT_SHORT_V2.md` 贴给 Codex，要求它读取项目。
2. 再把 `00_CODEX_MASTER_PROMPT_ENTERPRISE_LOOP_V2.md` 给 Codex 作为总规则。
3. 如果 Codex 支持多 Agent，把 `SUB_AGENTS/*.md` 分别派发。
4. 每个 Agent 必须用 `05_LOOP_RUN_REPORT_TEMPLATE.md` 写回结果。
5. 合并前必须按 `04_PRODUCTION_ACCEPTANCE_GATES.md` 和 `TABLES/acceptance_matrix.md` 验收。

## 一句话强约束

**没有读取证据、没有测试证据、没有截图/接口响应证据、没有文档同步证据的任务，一律视为未完成。**
