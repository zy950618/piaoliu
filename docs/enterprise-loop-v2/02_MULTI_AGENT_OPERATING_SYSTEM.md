# 多子 Agent 作业系统 v2

日期：2026-06-29

## 1. 总原则

多 Agent 不是“每个人随便改一块”，而是带有依赖、权限、输入输出和验收证据的并行工程系统。

本项目多 Agent 采用：

```text
A0 Orchestrator 控制总 LOOP
A1-A7 功能实现 Agent 并行/串行处理
A8 QA Agent 负责阻断不合格合并
A9 SRE/Security Agent 负责生产风险
A10 Docs Keeper 负责接力文档
```

## 2. RACI

| 模块 | Responsible | Accountable | Consulted | Informed |
| --- | --- | --- | --- | --- |
| 生产级管理员鉴权 | A1 | A0 | A2/A9 | A3/A8/A10 |
| RBAC 权限矩阵 | A1 | A0 | A3/A9 | A8/A10 |
| PostgreSQL/Redis/Alembic | A2 | A0 | A1/A9 | A8/A10 |
| 审计日志真实落库 | A2/A9 | A0 | A1/A3/A4/A5 | A8/A10 |
| Web Admin 布局与菜单 | A3 | A0 | A1/A6 | A8/A10 |
| 审核工作台 | A3/A4 | A0 | A1/A2/A9 | A8/A10 |
| 钱包提现与财务风控 | A5 | A0 | A1/A2/A9 | A8/A10 |
| 用户端体验 | A6 | A0 | A7/A8 | A10 |
| 扩列/房间/增长 | A7 | A0 | A4/A5/A6/A9 | A8/A10 |
| 自动化测试和截图 | A8 | A0 | 所有 Agent | A10 |
| 文档同步 | A10 | A0 | 所有 Agent | 所有 Agent |

## 3. 并行批次

### Batch 0：准备与冻结

A0 + A10：

- 读取文档和代码。
- 输出不可变规则。
- 输出当前能力边界。
- 输出任务优先级。
- 冻结本轮允许修改范围。

通过条件：

- 文档读取清单完整。
- 明确 Mock/生产边界。
- 明确不改范围。

### Batch 1：生产底座

A1 + A2 + A9 并行：

- A1：管理员、RBAC、会话。
- A2：数据库、迁移、仓储。
- A9：request_id、日志、trace、错误码、安全基线。

依赖：

- A1 依赖 A2 的管理员表。
- A9 需要和 A1/A2 共同定义 audit fields。

通过条件：

- seed 管理员可登录。
- token/session 可持久化和失效。
- 权限矩阵生效。
- 审计真实落库。

### Batch 2：后台效率

A3 + A4 + A5 并行：

- A3：后台框架、菜单、表格、筛选、批量。
- A4：审核/举报/聊天/私密照片。
- A5：钱包/提现/财务风控。

通过条件：

- 员工处理高频任务路径短。
- 每个写操作有二次确认、原因、审计。
- 不同角色看到不同菜单和按钮。

### Batch 3：用户端体验与增长

A6 + A7 并行：

- A6：用户端状态、动效、失败恢复、视觉统一。
- A7：扩列、普通房间、私密房间、增长策略。

通过条件：

- 不破坏现有业务。
- 新功能先有规则、接口、风控、审核链路。
- 用户端不出现后台式复杂表格。

### Batch 4：验证与文档

A8 + A9 + A10：

- A8：测试、截图、E2E、回归。
- A9：安全、SLO、监控验证。
- A10：文档同步。

通过条件：

- 全部门禁通过。
- 失败项明确。
- 文档同步完整。

## 4. Agent 文件边界

| Agent | 优先文件 | 禁止项 |
| --- | --- | --- |
| A1 | `backend/app/core/security.py`, `backend/app/models/admin.py`, `backend/app/routes/admin_auth.py`, tests | 不得改用户端 UI；不得硬编码明文密码 |
| A2 | `backend/app/db/**`, `backend/app/repositories/**`, `backend/alembic/**` | 不得绕过 migration 直接改生产表 |
| A3 | `admin-web/**` | 不得改 `src/pages.json` 加后台路由 |
| A4 | `backend/app/routes/moderation*`, `admin-web/**` 审核页 | 不得放宽私密照片/聊天审核规则 |
| A5 | wallet/withdrawal models/routes/admin-web finance | 不得允许充值金币提现 |
| A6 | `src/pages/**`, `src/components/**`, `src/styles/**` | 不得改后台；不得改变底部 Tab |
| A7 | docs/product rules, api contract, new module drafts | 不得先写代码再补规则 |
| A8 | tests, playwright, screenshots, reports | 不得修改业务逻辑来让测试过 |
| A9 | logging, telemetry, error handling, security tests | 不得关闭安全校验换取通过 |
| A10 | docs | 不得删除历史记录 |

## 5. 子 Agent 输出协议

每个 Agent 结束必须输出：

```text
Agent 名称：
本轮目标：
读取文件：
修改文件：
新增/修改接口：
新增/修改数据表：
验证命令：
证据：
失败项：
风险项：
需要其他 Agent 接力：
是否允许进入合并：YES/NO
```

## 6. 主线程合并协议

A0 合并前检查：

1. 是否违反不可变业务规则。
2. 是否有两个 Agent 修改同一文件冲突。
3. 是否有接口字段变化未通知前端/测试/文档。
4. 是否有数据库迁移未执行或未测试。
5. 是否有安全门禁未通过。
6. 是否有截图/接口证据缺失。
7. 是否文档未同步。

## 7. 并发效率规则

为提高效率：

- A1/A2/A9 可并行做设计，但实现时以迁移和模型为先。
- A3 可先做 UI 骨架，但必须用接口契约 mock，不能写死字段。
- A4/A5 可先定义状态机和接口，不阻塞 A3 页面结构。
- A8 可提前写失败测试，推动 A1-A7 按标准实现。
- A10 每轮都同步，避免最后补文档丢上下文。

## 8. 不允许的多 Agent 错误

- 每个 Agent 都改全局样式导致 UI 混乱。
- 多个 Agent 都改 `mockState`，结果互相覆盖。
- Backend 改接口不改前端映射。
- 前端为了显示方便新增假字段但不进 API Contract。
- QA 只跑测试不看业务规则。
- Docs 只记录“已完成”，不写证据。
