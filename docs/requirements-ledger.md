# 需求台账

## 状态说明

- `待处理`：已有明确要求，但尚未开始。
- `处理中`：已有 Agent 接手，仍需继续。
- `已完成`：已有文档、代码或验证记录支撑。
- `待确认`：要求存在歧义，需要用户或负责人确认。

## R-001 后台接口与后台管理完整骨架优先

- 日期：2026-06-23
- 来源：用户最新要求。
- 优先级：P0
- 状态：已完成阶段性骨架，管理员鉴权和真实数据库待后续接入
- 要求：先搭建后台接口、后台管理等完整骨架。
- 范围：
  - 后台接口基础路由、权限边界、管理员鉴权。
  - 用户管理、内容审核、举报/拉黑、奖励配置、提现审核、认证复核、看板统计。
  - 后台管理页面或管理端骨架，至少能承载各模块入口和基础状态。
  - 每一步都要写入要求、处理历史和已经处理的事项，便于多 Agent 共同处理。
- 验收口径：
  - 后台接口清单有明确优先级和路由分组。
  - 后台管理骨架有模块分区和页面入口规划。
  - 每个模块有最小可验证动作，例如列表读取、详情查看、状态变更或配置保存。
  - 处理记录能让下一个 Agent 继续工作，不需要重新推断上下文。
- 关联文档：
  - [接口与后台搭建计划](backend-interface-admin-plan.md)
  - [API Contract](api-contract.md)
  - [处理历史](work-history.md)
- 已完成证据：
  - 后端接口骨架已补齐到后台、用户、内容、举报、钱包、认证、订单、广场、附近、审计等模块。
  - 前端后台管理页已接入完整 Mock Dashboard。
  - `npm run typecheck`、`npm run build:h5`、`npm run test:frontend`、`python -m compileall -q backend\app backend\tests`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 均通过。
  - 后台页面截图：`runtime-admin-dashboard-v1.png`。

## R-002 漂流瓶核心体验

- 日期：2026-06-23
- 来源：现有产品规则和预览版本记录。
- 优先级：P1
- 状态：已完成阶段性版本，后续细节继续优化
- 要求：
  - 漂流瓶页保留“捞 / 扔”双入口并显示剩余次数角标。
  - 筛选弹窗居中展示，保存只应用当前页面状态，不写入持久偏好。
  - 捞到瓶子后展示作者头像、昵称、VIP、认证、性别、年龄段、城市，并支持回应、关注、加好友、送礼物。
- 已有证据：
  - [预览版本记录](preview-version-log.md) 中 `bottle-v5` 到 `bottle-v8`。
- 后续入口：
  - [后续细节优化入口](detail-optimization-inbox.md)

## R-003 产品规则基础盘

- 日期：2026-06-23
- 来源：现有产品规则文档。
- 优先级：P1
- 状态：已完成文档初版
- 要求：
  - 首版包含漂流瓶、游戏、树洞、广场、附近的人、消息中心、会员中心、钱包、认证收益、用户中心和后台看板。
  - 底部主导航固定为瓶子、广场、游戏、树洞、我的。
  - 后台为独立管理员入口，不出现在普通用户“我的”页面。
- 关联文档：
  - [产品规则](product-rules.md)

## R-004 接口契约持续维护

- 日期：2026-06-23
- 来源：现有 API Contract。
- 优先级：P1
- 状态：处理中
- 要求：
  - 用户状态、次数奖励、内容、关系安全、认证拉新钱包、后台接口统一进入接口契约。
  - 列表筛选字段后续统一支持 `city`、`gender`、`age_range`。
- 后续动作：
  - 按后台骨架计划补齐管理员鉴权、审核、提现、认证复核和看板接口细节。

## R-005 后台继续完成阶段补强

- 日期：2026-06-23
- 来源：本轮继续完成阶段文档同步要求。
- 优先级：P0
- 状态：已完成阶段性代码骨架，生产级持久化、真实会话和完整权限矩阵待后续接入
- 要求：在已完成阶段性 Mock 骨架后，继续补齐后台可进入真实运行前必须具备的鉴权、权限、持久化、错误、审计和管理效率入口。
- 范围：
  - 管理员真实鉴权骨架：登录、退出、当前管理员、未登录拦截、token/session 处理和测试占位。
  - 角色权限：超级管理员、审核管理员、运营管理员、财务管理员的接口权限、菜单权限和操作权限。
  - 数据库/Alembic 占位：PostgreSQL、Redis、SQLAlchemy async、Alembic 迁移目录、种子管理员和配置表规划。
  - 统一错误码：未登录、无权限、参数错误、对象不存在、状态冲突、重复操作、系统错误等响应口径。
  - 审计日志链路：管理员操作、审核动作、配置变更、状态变更、批量操作和失败原因记录。
  - 后台详情/批量操作/高级筛选入口：用户、内容、举报、提现、认证复核、审计日志等模块的管理效率入口。
- 验收口径：
  - 每个目标在 [接口与后台搭建计划](backend-interface-admin-plan.md) 中有明确模块、接口范围和验收描述。
  - 未实现项在 [后续细节优化入口](detail-optimization-inbox.md) 中有可接力条目。
  - [处理历史](work-history.md) 记录本轮代码落地、验证命令、接口冒烟和页面截图。
- 已完成证据：
  - 后端已增加管理员 Mock 鉴权、Bearer token 拦截、角色依赖、统一错误响应、审计记录、SQLAlchemy/Redis/Alembic 占位。
  - 前端后台页已增加管理员登录状态、模块锚点、详情面板、奖励配置保存和内容批量操作。
  - `npm run typecheck`、`npm run build:h5`、`npm run test:frontend`、`python -m compileall -q backend\app backend\tests`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 均通过。
  - 后台鉴权冒烟和 Chrome CDP 页面冒烟通过，截图为 `runtime-admin-dashboard-v2.png`、`runtime-admin-detail-v2.png`。
- 后续待接入：
  - 生产级管理员账号、密码哈希、token/session 持久化和禁用账号策略。
  - PostgreSQL/Redis 真实连接、迁移执行、真实审计落库和导出。
  - 完整角色权限矩阵、独立 Web Admin 拆分、高级筛选和更完整批量操作。

## R-006 管理后台必须为独立 Web

- 日期：2026-06-23
- 来源：用户纠正“后台肯定是 Web，不可能是 H5”。
- 优先级：P0
- 状态：已完成阶段性纠正，生产级后台能力继续接入
- 要求：
  - 管理后台必须是独立 Web Admin，不属于小程序、iOS、Android 或 H5 用户端页面。
  - 用户端 `pages.json` 不能挂后台页面，普通用户端不能出现后台入口。
  - Web Admin 后续通过 FastAPI 管理接口读写数据，当前可先复用 Mock API。
- 已完成证据：
  - 新增 `admin-web/` 独立 Vite + Vue 管理后台。
  - 新增 `npm run dev:admin`、`npm run build:admin`。
  - 删除 `src/pages.json` 中的 `pages/admin/index`。
  - 删除旧 `src/pages/admin/index.vue` 和 `src/stores/admin.ts`。
  - `src/pages.json` 检索 `admin` / `后台` 无命中。
  - `npm run typecheck`、`npm run build:admin`、`npm run build:h5`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 均通过。
- 后续待接入：
  - Web Admin 接真实管理员登录、真实权限、真实 FastAPI HTTP、真实数据库和审计落库。
