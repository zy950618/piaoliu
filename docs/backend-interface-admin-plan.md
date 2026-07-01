# 接口与后台搭建计划

## 目标

先搭建后台接口、后台管理等完整骨架，让多 Agent 可以按模块并行补齐业务细节。

本计划只定义搭建顺序、接口范围、后台管理模块和验收口径；具体代码实现由后续开发任务处理。

## 总体原则

- 后台能力独立于普通用户端，不出现在普通用户“我的”页面。
- 管理端先有骨架、权限和状态流，再补复杂筛选、批量操作和数据图表。
- 接口先满足列表、详情、状态变更、配置读取/保存四类最小闭环。
- 所有审核类操作必须保留操作人、操作时间、原因和前后状态。
- 多 Agent 分工时，每个模块都要同步更新 [处理历史](work-history.md) 和 [已完成清单](completed-checklist.md)。

## P0 后台基础骨架

### 管理员鉴权

- 接口范围：
  - `POST /admin/auth/login`
  - `POST /admin/auth/logout`
  - `GET /admin/auth/me`
- 后台管理入口：
  - 管理员登录页。
  - 登录后基础布局：侧边栏、顶部当前管理员信息、退出入口。
- 验收：
  - 未登录访问后台接口返回未授权。
  - 登录后能读取当前管理员身份和角色。

### 后台概览

- 接口范围：
  - `GET /admin/summary`
  - `GET /admin/audit-queues/summary`
- 后台管理入口：
  - 数据概览页。
  - 待审核队列概览：内容、认证、提现、举报。
- 验收：
  - 页面能看到核心计数。
  - 每个计数能跳转到对应管理模块。

### 用户管理

- 接口范围：
  - `GET /admin/users`
  - `GET /admin/users/{id}`
  - `PATCH /admin/users/{id}/status`
- 后台管理入口：
  - 用户列表。
  - 用户详情。
  - 封禁、解封、备注、风控状态查看。
- 验收：
  - 支持按昵称、手机号或用户 ID 查询。
  - 用户状态变更写入处理历史。

## P1 审核与业务配置

### 内容审核

- 接口范围：
  - `GET /admin/content`
  - `GET /admin/content/{id}`
  - `POST /admin/moderation/{id}`
- 后台管理入口：
  - 瓶子、树洞、广场、私密照片审核队列。
  - 通过、拒绝、下架、标记风险。
- 验收：
  - 每次审核必须填写或选择原因。
  - 审核结果影响内容展示状态。

### 举报与拉黑

- 接口范围：
  - `GET /admin/reports`
  - `GET /admin/reports/{id}`
  - `POST /admin/reports/{id}/resolve`
  - `GET /admin/blocks`
- 后台管理入口：
  - 举报列表。
  - 举报详情。
  - 处理结论和关联用户/内容入口。
- 验收：
  - 举报能关闭、维持观察或触发内容/用户处罚。

### 上下文私聊审核

- 接口范围：
  - `GET /admin/chat/context-requests`
  - `GET /admin/chat/conversations/{id}`
  - `POST /admin/chat/conversations/{id}/resolve-report`
- 后台管理入口：
  - 上下文私聊审核队列。
  - 举报聊天详情。
  - 会话来源跳转和来源卡片。
- 验收：
  - 会话必须展示 `source_type`、`source_id`、双向回应/确认证据、参与人、状态和风险标签。
  - 举报处理必须填写原因，并写入审计日志。
  - 拉黑、举报、风控冻结后不能继续发送消息。

### 私密照片智能审核

- 接口范围：
  - `GET /admin/private-photos/reviews`
  - `GET /admin/private-photos/reviews/{id}`
  - `POST /admin/private-photos/reviews/{id}/review`
  - `GET /admin/private-photos/risk-summary`
- 后台管理入口：
  - 私密照片 AI 审核结果页。
  - 人工复核工作台。
  - 风险等级筛选和收益冻结/解冻处理。
- 验收：
  - 展示模型标签、置信度、风险等级、自动动作、人工复核记录和审计记录。
  - 低风险高置信内容可自动通过；中风险进入人工复核；高风险拒绝或冻结。
  - 审核中、拒绝、冻结、申诉待处理内容不得产生收益。
  - 每次人工复核必须填写原因，并记录操作人、时间、前后状态和收益动作。

### 奖励配置

- 接口范围：
  - `GET /admin/reward-config`
  - `PATCH /admin/reward-config`
- 后台管理入口：
  - 今日次数配置。
  - 广告冷却配置。
  - 签到奖励配置。
  - 拉新赠会员配置。
- 验收：
  - 配置读取和保存形成闭环。
  - 修改配置必须保留操作记录。

### 认证复核

- 接口范围：
  - `GET /admin/verifications`
  - `GET /admin/verifications/{id}`
  - `POST /admin/verifications/{id}/review`
- 后台管理入口：
  - 人脸活体、性别识别、人工复核队列。
- 验收：
  - 性别识别结果不能自动最终通过，必须进入人工复核状态。

### 钱包与提现审核

- 接口范围：
  - `GET /admin/wallet/withdrawals`
  - `GET /admin/wallet/withdrawals/{id}`
  - `POST /admin/wallet/withdrawals/{id}/review`
  - `GET /admin/wallet/transactions`
- 后台管理入口：
  - 提现申请列表。
  - 提现详情。
  - 金币、收益金币、魅力值流水查询。
- 验收：
  - 提现审核区分通过、拒绝、风控冻结。
  - 充值金币不可提现规则在后台说明和校验中可见。

## P2 管理效率与细节

- 批量审核和批量下架。
- 操作日志检索。
- 管理员角色和权限管理。
- 数据看板趋势图。
- 高级筛选和导出。
- 风控命中详情。

## 继续完成阶段 P0/P1 拆解

### 管理员真实鉴权骨架

- 接口范围：
  - `POST /admin/auth/login`：校验管理员账号、密码和启用状态，返回访问凭证。
  - `POST /admin/auth/logout`：注销当前凭证或刷新服务端会话状态。
  - `GET /admin/auth/me`：返回当前管理员、角色、权限和可见菜单。
- 后台管理入口：
  - 未登录统一跳转管理员登录页。
  - 顶部展示当前管理员、角色和退出入口。
- 验收：
  - 未登录访问后台接口返回统一未授权错误码。
  - 禁用管理员不能登录。
  - 登录后能读取当前管理员身份、角色和权限列表。

### 角色权限

- 角色占位：
  - `super_admin`：全部后台接口和配置权限。
  - `review_admin`：内容、举报、认证复核审核权限。
  - `ops_admin`：奖励配置、广告奖励、广场/树洞运营权限。
  - `finance_admin`：钱包流水、提现审核和财务风控权限。
- 权限边界：
  - 菜单权限控制后台入口可见性。
  - 接口权限控制实际操作。
  - 危险操作必须二次确认并写审计日志。
- 验收：
  - 无权限访问返回统一无权限错误码。
  - 后台菜单和接口权限使用同一角色权限来源。

### 数据库/Alembic 占位

- 占位范围：
  - PostgreSQL：管理员、角色、权限、审计日志、后台配置、审核记录。
  - Redis：后台会话、短期令牌、频率限制和幂等键。
  - SQLAlchemy async：统一 session 生命周期和 repository 边界。
  - Alembic：迁移目录、初始表结构和种子管理员迁移。
- 验收：
  - 新增表结构先有迁移计划，再接入业务读写。
  - Mock store 向真实数据库迁移时保留接口响应兼容性。

### 统一错误码

- 错误码范围：
  - `AUTH_REQUIRED`：未登录或凭证失效。
  - `FORBIDDEN`：角色或权限不足。
  - `VALIDATION_ERROR`：参数格式或字段校验失败。
  - `NOT_FOUND`：用户、内容、举报、提现等对象不存在。
  - `STATE_CONFLICT`：当前状态不允许执行该操作。
  - `DUPLICATE_OPERATION`：幂等场景下重复提交。
  - `INTERNAL_ERROR`：未预期服务端错误。
- 验收：
  - 后台接口错误响应结构一致。
  - 前端后台管理页能按错误码展示明确反馈。

### 审计日志链路

- 接口范围：
  - `GET /admin/audit-logs`
  - `GET /admin/audit-logs/{id}`
- 记录范围：
  - 登录、退出、权限拒绝。
  - 用户状态变更。
  - 内容审核、举报处理、认证复核、提现审核。
  - 奖励配置、批量操作和导出操作。
- 验收：
  - 每条审计日志包含操作人、角色、模块、对象 ID、动作、原因、前状态、后状态、请求 ID 和时间。
  - 详情页能查看关联审计记录。

### 后台详情、批量操作和高级筛选入口

- 详情入口：
  - 用户详情、内容详情、举报详情、提现详情、认证复核详情、审计日志详情。
- 批量操作入口：
  - 内容批量通过/拒绝/下架。
  - 举报批量关闭或转人工复核。
  - 提现批量风控冻结仅允许财务或超级管理员执行。
- 高级筛选入口：
  - 状态、时间范围、城市、性别、年龄段、风险等级、处理人、金额区间。
- 验收：
  - 批量操作有权限校验、二次确认、结果汇总和审计记录。
  - 高级筛选参数进入接口契约并有默认值和空值语义。

## 多 Agent 分工建议

- Agent A：管理员鉴权、后台布局、概览接口。
- Agent B：用户管理、举报处理、拉黑记录。
- Agent C：内容审核、认证复核、私密照片审核。
- Agent D：奖励配置、钱包流水、提现审核。
- Agent E：文档同步、处理历史、完成清单和后续优化入口。

## 骨架完成定义

后台骨架完成必须同时满足：

- P0 接口均有路由和基础响应契约。
- 后台管理端有登录后布局和 P0/P1 模块入口。
- 每个 P1 模块至少有列表页、详情页规划和一个状态变更动作。
- 需求台账、处理历史、已完成清单同步更新。
- 测试或验证命令记录在对应处理历史中。

## 2026-06-23 阶段性实现状态

- 已完成：
  - 后端 Mock 接口骨架覆盖后台概览、用户、内容、举报、拉黑、奖励配置、钱包/提现、认证、订单、广场、附近、审计日志。
  - 前端后台管理页已接入完整 Mock Dashboard，可展示 P0/P1 模块数据。
  - 后端契约测试已扩展到 12 个。
  - 处理历史、需求台账、已完成清单已同步。
- 未完成：
  - 管理员真实鉴权和角色权限。
  - 后台独立 Web Admin 的多页面详情和批量操作。
  - PostgreSQL/Redis/SQLAlchemy async/Alembic 持久化。
  - 操作日志真实落库和统一错误码。
- 继续完成阶段已登记入口：
  - 管理员真实鉴权骨架和角色权限拆解见“继续完成阶段 P0/P1 拆解”。
  - 数据库/Alembic、统一错误码、审计日志链路、后台详情/批量操作/高级筛选均已有接力验收口径。
- 验证证据：
  - 见 [处理历史](work-history.md) 的“后台接口与后台管理骨架”。
  - 后台截图：`runtime-admin-dashboard-v1.png`。

## 2026-06-23 继续完成阶段代码落地状态

- 已完成：
  - 管理员 Mock 鉴权闭环已落地：登录、退出、当前管理员、未登录拦截和 Bearer token 校验。
  - 后台写操作已接入管理员依赖：奖励配置保存、内容审核动作会校验管理员身份并写入审计日志。
  - 统一错误响应已接入：未授权、无权限、HTTP 异常和参数校验错误统一返回 `error.code`、`error.message`。
  - 数据库基础占位已落地：SQLAlchemy async session、Redis client、Alembic 配置、初始迁移和模型规划文件已存在；当前无依赖环境仍使用 Mock store。
  - 前端后台管理页已补齐登录状态、模块锚点、详情面板、内容批量通过、批量下架和奖励配置保存。
- 当前边界：
  - 当前鉴权为 Mock token，不是生产级账号系统。
  - 当前数据库/Alembic 是迁移占位和接口兼容骨架，尚未执行真实 PostgreSQL/Redis 落库。
  - 当前审计写入 Mock 数据，尚未进入真实审计表。
  - 当前后台仍是 uni-app 内部管理页，不是独立 Web Admin 项目。
- 后续接力顺序：
  1. 安装并锁定后端依赖，接入 PostgreSQL/Redis 真实连接和 Alembic 迁移执行。
  2. 增加管理员表、密码哈希、token/session 持久化、禁用账号和刷新策略。
  3. 将审计日志、配置变更、审核动作、批量操作从 Mock store 迁移到真实表。
  4. 把角色权限矩阵落到菜单权限和接口权限，并补充无权限测试。
  5. 拆分独立 Web Admin 或独立路由，继续补高级筛选、导出、趋势图和更完整批量操作。
- 验证证据：
  - `npm run typecheck`、`npm run build:h5`、`npm run test:frontend` 通过。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 通过，15 个测试通过。
  - 后台鉴权冒烟通过，后台页面截图：`runtime-admin-dashboard-v2.png`、`runtime-admin-detail-v2.png`。

## 2026-06-23 管理后台 Web 化纠正状态

- 已完成：
  - 后台管理端已从 uni-app 用户端剥离，新增独立 `admin-web/`。
  - 用户端 `src/pages.json` 已移除 `pages/admin/index`，后台不再进入小程序、iOS、Android、H5 用户端路由。
  - 独立 Web Admin 使用 Vite + Vue，可单独开发和构建。
  - Web Admin 当前复用 Mock API，后续按同一接口契约替换为 FastAPI HTTP。
- 命令：
  - `npm run dev:admin`：启动 Web 管理后台。
  - `npm run build:admin`：构建 Web 管理后台到 `dist-admin/`。
- 当前边界：
  - Web Admin 已经是独立管理后台，但仍未接真实管理员账号、真实 token/session、真实 PostgreSQL/Redis 和真实审计落库。
  - 旧 H5 后台截图仅保留为历史记录，不再代表当前后台交付形态。
- 验证证据：
  - `npm run typecheck`、`npm run build:admin`、`npm run build:h5`、`npm run test:frontend` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 通过，15 个测试通过。
  - `src/pages.json` 检索 `admin` / `后台` 无命中。
  - 当前 Web Admin 预览地址：`http://127.0.0.1:5180/`；截图：`runtime-admin-web-v2.png`。
