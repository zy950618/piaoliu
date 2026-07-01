# 可追加到现有 docs 的条目 v2

日期：2026-06-29

## 1. 建议追加到 `multi-agent-workbench.md`

```md
## 企业级 LOOP v2 补充

后续所有 Agent 必须按 RPP-AOEVRR-D 执行：Read → Protect → Plan → Act → Observe → Evaluate → Verify → Reflect → Record → Decide。

没有读取证据、测试证据、接口/截图证据、文档同步证据的任务，不得标记完成。

多 Agent 必须拆分为：Orchestrator、Backend Identity/RBAC、Database/Persistence、Admin Web UX、Moderation/Safety、Wallet/Finance、User Frontend UX、Growth/Product、QA/E2E/Visual、Observability/SRE/Security、Docs Keeper。
```

## 2. 建议追加到 `requirements-ledger.md`

```md
## R-007 企业级 LOOP 与生产级验收补强

- 日期：2026-06-29
- 优先级：P0
- 状态：待处理
- 要求：在现有后台骨架和用户端体验基础上，引入企业级 LOOP、多 Agent 分工、生产级验收门禁、强约束和证据链。
- 验收：每轮任务必须有 LOOP START/RESULT；必须按 G0-G14 门禁验收；必须更新处理历史、完成清单和接口/设计文档。
```

## 3. 建议追加到 `completed-checklist.md`

```md
## 企业级 LOOP v2 待完成

- [ ] 生产级管理员账号、密码哈希、token/session 持久化。
- [ ] 完整 RBAC 权限矩阵和按钮/接口双重权限。
- [ ] PostgreSQL/Redis 真实连接与 Alembic 执行。
- [ ] 审计日志真实落库、检索和导出。
- [ ] Web Admin 高级筛选、批量、详情、导出、趋势图、队列 SLA。
- [ ] 用户端加载/空态/错误/慢接口/防重复/隐私提示统一。
- [ ] 扩列、普通房间、私密房间产品规则与接口契约。
- [ ] OpenTelemetry、SLO、告警、性能和可访问性验收。
```

## 4. 建议追加到 `work-history.md` 的模板

```md
## YYYY-MM-DD 企业级 LOOP 第 N 轮

- Agent：
- 目标：
- 读取文件：
- 不可变规则：
- 修改文件：
- 处理动作：
- 验证命令：
- 接口/截图证据：
- 失败项：
- 风险项：
- 文档同步：
- 是否可合并：YES/NO
- 后续入口：
```
