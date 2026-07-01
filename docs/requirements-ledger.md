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

## R-007 上下文私聊规则纠偏与接口契约

- 日期：2026-06-29
- 来源：AGENTS.md 与 `docs/enterprise-loop-v2/patches/CODEX_RULE_PATCH_CHAT_PHOTO_V3.md`。
- 优先级：P0
- 状态：后端、admin-web 与用户端入口最小闭环已完成，真实持久化和用户端真实发起链路待接入
- 要求：
  - 禁止无上下文冷启动骚扰陌生人。
  - 允许明确互动上下文内的陌生人私聊。
  - 好友关系不是私聊唯一门槛，只用于长期关系沉淀、更多资料可见性和更低频控限制。
  - 上下文私聊必须保存 `source_type`、`source_id`、双向回应/确认证据、频控、拉黑、举报、风控和审计。
- 接口范围：
  - `POST /chat/context-requests`
  - `POST /chat/context-requests/{id}/accept`
  - `POST /chat/context-requests/{id}/reject`
  - `GET /chat/conversations`
  - `GET /chat/conversations/{id}`
  - `POST /chat/conversations/{id}/messages`
  - `POST /chat/conversations/{id}/report`
  - `POST /chat/conversations/{id}/block`
- 验收口径：
  - 无上下文私聊失败。
  - 漂流瓶回应、广场/树洞评论、游戏/房间/扩列上下文完成双向回应或确认后可创建临时私聊。
  - 拉黑、举报、风控冻结后不可继续发送消息。
  - 管理后台能查看来源和举报证据。
- 已完成证据：
  - [产品规则](product-rules.md) 已写入新规则。
  - [API Contract](api-contract.md) 已写入字段级契约、状态枚举和错误码。
  - [接口与后台搭建计划](backend-interface-admin-plan.md) 已补后台审核入口。
  - 后端已新增 `/chat/context-requests`、`/chat/conversations`、消息、举报、拉黑和管理员查看接口的最小闭环。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 通过，42 passed。
  - 接口冒烟确认无上下文返回 `CHAT_CONTEXT_REQUIRED`，确认后会话 `active`，举报后后台详情 `reported`，拉黑后发消息返回 `CHAT_BLOCKED`。
- 后续待接入：
  - `admin-web/` 审核队列和会话详情已完成最小可视闭环，后续可接真实处置动作和详情路由。
  - 用户端“继续聊/私聊”入口和状态提示已完成最小可视闭环，后续需接入真实 `/chat/context-requests` 发起、确认、拒绝和会话跳转。
  - 后续从内存 store 迁移到真实数据库模型和审计表。

## R-008 私密照片 AI 智能审核规则纠偏与接口契约

- 日期：2026-06-29
- 来源：AGENTS.md 与 `docs/enterprise-loop-v2/patches/CODEX_RULE_PATCH_CHAT_PHOTO_V3.md`。
- 优先级：P0
- 状态：后端、admin-web 与用户端状态反馈最小闭环已完成，真实上传、收益流水和申诉链路待接入
- 要求：
  - 私密照片 AI 智能审核优先，风险分级，人工复核兜底。
  - 低风险、高置信、非露骨、无敏感隐私、无未成年人疑似、无诈骗导流内容可自动通过。
  - 中风险、低置信、边界内容进入人工复核。
  - 高风险内容自动拒绝、冻结或进入更严格复核。
  - 收益只允许来自审核通过且未冻结的内容。
  - 所有审核必须保留模型标签、置信度、风险等级、自动动作、人工复核记录和审计日志。
- 接口范围：
  - `POST /private-photos`
  - `GET /private-photos`
  - `GET /private-photos/{id}`
  - `POST /private-photos/{id}/unlock`
  - `GET /admin/private-photos/reviews`
  - `GET /admin/private-photos/reviews/{id}`
  - `POST /admin/private-photos/reviews/{id}/review`
  - `GET /admin/private-photos/risk-summary`
- 验收口径：
  - 低风险图片自动通过并记录 AI 审核日志。
  - 中风险图片进入人工复核。
  - 高风险图片拒绝或冻结。
  - 审核中、拒绝、冻结、申诉待处理内容不能产生收益。
  - 后台能按风险等级、状态、用户、时间、举报数筛选。
- 已完成证据：
  - [产品规则](product-rules.md) 已写入新规则。
  - [API Contract](api-contract.md) 已写入字段级契约、状态枚举和错误码。
  - [接口与后台搭建计划](backend-interface-admin-plan.md) 已补后台审核入口。
  - 后端已新增 `POST /private-photos`、`GET /private-photos/{id}`、`POST /private-photos/{id}/unlock`、`GET /admin/private-photos/reviews`、`GET /admin/private-photos/reviews/{id}`、`POST /admin/private-photos/reviews/{id}/review`、`GET /admin/private-photos/risk-summary` 的最小闭环。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 通过，46 passed。
  - 接口冒烟确认低风险自动通过并可解锁；中风险进入人工复核且复核放行后可解锁；高风险冻结且不可解锁；后台风险汇总可见。
- 后续待接入：
  - `admin-web/` 私密照片审核列表、复核详情和审计日志已完成最小可视闭环，后续可接真实批量操作和申诉详情。
  - 用户端钱包页已展示上传后审核状态、人工复核、拒绝/冻结和收益状态反馈；后续需接真实上传入口、真实新契约列表和申诉入口。
  - 后续从内存 store 迁移到真实数据库模型、真实审核记录和收益流水。

## R-009 用户端上下文私聊与私密照片状态体验

- 日期：2026-06-29
- 来源：LOOP-5 用户端体验最小闭环。
- 优先级：P1
- 状态：真实接口动作已接入瓶子/广场入口，浏览器端全链路联调受本地 PostgreSQL 缺失限制
- 要求：
  - 漂流瓶回应后提示“基于本次互动继续聊”，等待对方确认后开启临时私聊。
  - 广场留言后提供“继续聊”入口，并说明需发帖人回复或确认。
  - 私密照片上传/展示侧需体现 AI 自动通过、人工复核、冻结/拒绝、收益冻结/不可结算。
  - 底部 tab 固定为 `瓶子 / 广场 / 游戏 / 树洞 / 我的`。
- 已完成证据：
  - `src/pages.json` 第四个 tab 已从 `消息` 纠偏为 `树洞`。
  - `output/playwright/user-bottle-continue-chat.png` 展示瓶子回应后的继续聊说明。
  - `output/playwright/user-plaza-comment-continue-chat.png` 展示广场留言“继续聊”入口。
  - `output/playwright/user-wallet-private-photo-review.png` 展示 AI 自动通过、人工复核、已冻结和收益状态。
  - `output/playwright/user-treehole-tab.png` 展示底部五 tab 为 `瓶子 / 广场 / 游戏 / 树洞 / 我的`。
- 后续待接入：
  - 点击“继续聊”已真实调用 `/chat/context-requests`，并处理 pending、active、expired、blocked、risk_frozen 和失败状态。
  - 后续需在可运行当前后端数据库环境下完成浏览器端“加载页面 -> 点击继续聊 -> pending/active”端到端验证。
  - 私密照片上传页真实调用 `POST /private-photos`，列表统一读取新审核契约，冻结后提供申诉入口。

## R-010 LOOP-6 生产级回归验收

- 日期：2026-06-29
- 来源：LOOP-6 生产级验收与回归。
- 优先级：P1
- 状态：本轮回归通过，生产化遗留项已进入 inbox
- 要求：
  - 旧规则不得残留在业务代码中；补丁文档中旧句只允许作为废弃规则说明。
  - 管理后台不得回到用户端 `src/pages/**` 或用户端 `pages.json`。
  - 用户端底部 tab 必须为 `瓶子 / 广场 / 游戏 / 树洞 / 我的`。
  - 上下文私聊必须能证明无上下文失败、上下文确认 active、举报/拉黑闭环。
  - 私密照片审核必须能证明 AI 自动通过、人工复核、高风险冻结/拒绝和收益状态。
- 已完成证据：
  - 业务代码旧规则残留搜索无命中；`src/pages/nearby/index.vue` 旧 toast 已纠偏。
  - `src/pages.json` 搜索 `admin|后台` 无命中，tabBar 为 `瓶子 / 广场 / 游戏 / 树洞 / 我的`。
  - 接口冒烟覆盖 `CHAT_CONTEXT_REQUIRED`、`active`、`reported`、`blocked`、`CHAT_BLOCKED`。
  - 接口冒烟覆盖照片 `ai_approved/low_risk/eligible`、`manual_required/medium_risk/frozen`、`frozen/high_risk/ineligible`。
  - 全量命令通过：typecheck、frontend tests、H5 build、admin build、backend pytest、compileall。
  - 7 张截图证据均存在且非空。
- 后续待接入：
  - 用户端“继续聊”真实接口动作。
  - 私密照片新审核契约的真实上传、列表、解锁和申诉入口。
  - 后端内存 store 迁移到数据库和真实审计落库。

## R-011 LOOP-7 用户端继续聊真实接口接入

- 日期：2026-06-29
- 来源：LOOP-7 用户端继续聊真实接口接入。
- 优先级：P1
- 状态：已通过，浏览器端瓶子/广场继续聊 pending 截图已补齐
- 要求：
  - 瓶子回应后发起 `source_type=bottle_reply` 的 `/chat/context-requests`。
  - 广场留言“继续聊”发起 `source_type=plaza_comment` 的 `/chat/context-requests`。
  - 申请状态必须向用户展示 pending、active、blocked、expired、risk_frozen 或失败状态。
  - 无上下文继续聊必须由接口拒绝。
- 已完成证据：
  - `businessApi.createContextChatRequest()` 单元测试通过，验证请求字段和响应映射。
  - `npm run test:frontend` 通过，19 passed。
  - 接口冒烟确认缺少 `source_id` 返回 `CHAT_CONTEXT_REQUIRED`。
  - 接口冒烟确认 `bottle_reply` 和 `plaza_comment` 均可创建 `pending`。
  - 接口冒烟确认 accept 后返回 `active` 和 `conversation_id`。
  - `output/playwright/user-bottle-context-request-pending.png` 展示瓶子回应后 pending 状态。
  - `output/playwright/user-plaza-context-request-pending.png` 展示广场继续聊 pending 状态。
- 后续待接入：
  - 接入消息页跳转和临时会话详情。

## R-012 当前后端 E2E SQLite 环境

- 日期：2026-06-29
- 来源：LOOP-8 当前后端 E2E 环境闭环。
- 优先级：P1
- 状态：已完成
- 要求：
  - 本地没有 PostgreSQL 时，仍能启动当前 FastAPI 供 H5 E2E 使用。
  - 同一后端实例必须同时支持 H5 页面数据和 `/chat/context-requests`。
  - H5 构建产物必须明确指向当前 E2E 后端，避免误连旧 8100 服务。
- 已完成证据：
  - 新增 `scripts/start-e2e-backend.ps1` 使用 SQLite `backend/runtime/e2e.sqlite3`。
  - 新增 `scripts/build-h5-e2e.ps1` 和 `npm run build:h5:e2e`。
  - 8110 实例验证 `/me/status`、`/plaza/posts/plaza_001`、`/plaza/posts/plaza_001/comments`、`/bottles/random`、`/chat/context-requests` 均通过。
  - 浏览器截图已证明瓶子/广场继续聊点击后进入 pending。
- 后续待接入：
  - 为 CI 固化 E2E 启停脚本和自动断言。
## R-013 LOOP-9 会话跳转最小闭环

- 日期：2026-06-29
- 来源：用户要求“accept 后进入消息页/临时会话详情”，并反馈捞瓶弹窗不应显示“原漂流瓶”标签。
- 优先级：P1
- 状态：已完成最小闭环，生产持久化仍待后续 LOOP。
- 要求：
  - 捞到瓶子弹窗默认展示最开始的漂流瓶正文，不额外显示“原漂流瓶”标签。
  - 用户端上下文私聊申请在接口返回 `active + conversation_id` 时，跳转到消息页临时会话详情。
  - 消息页支持通过 `contextConversationId` 读取 `/chat/conversations/{id}` 并展示来源、状态、消息列表和输入区。
  - 临时会话非 active 状态不得继续发送消息，仍保留频控、举报、拉黑、风控、审计提示。
- 已完成证据：
  - `businessApi.acceptContextChatRequest()` 已映射 `confirm_action/evidence_id`。
  - `businessApi.getContextConversation()` 已映射临时会话详情、消息、风控和审计字段。
  - `content.loadContextConversation()` 与 `content.sendContextConversationMessage()` 已接入消息页。
  - `src/pages/messages/chat.vue` 支持 `contextConversationId` 路由。
  - `src/pages/bottle/index.vue` 和 `src/pages/plaza/comments.vue` 在 active 后跳转 `/pages/messages/chat?contextConversationId=...`。
  - `Select-String src/pages/bottle/index.vue -Pattern '原漂流瓶|origin-kicker'` 无命中。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 均通过。
  - 接口冒烟：`pending -> active -> GET conversation active -> send sent`，摘要见 `output/playwright/context-conversation-smoke.json`。
  - 截图：`output/playwright/user-context-conversation-detail.png`。
- 后续待接入：
  - 树洞评论、游戏房间、扩列匹配入口复用本轮临时会话详情。
  - 将 context request/conversation/message 从内存 store 迁移到真实数据库和审计表。

## R-014 LOOP-10 树洞评论继续聊入口

- 日期：2026-06-29
- 来源：LOOP-10 树洞评论继续聊入口最小闭环。
- 优先级：P1
- 状态：已完成最小闭环，生产持久化仍待后续 LOOP。
- 要求：
  - 树洞用户必须先回复一条树洞心情，才能基于 `treehole_comment` 发起上下文继续聊。
  - 请求必须包含 `source_type=treehole_comment`、`source_id`、`reply_id`、`initiator_action=continue_chat`、`evidence_id`。
  - pending 状态必须在当前树洞弹层反馈给用户，不能伪装成普通私信。
  - 如果后续确认返回 `active + conversation_id`，必须复用 `/pages/messages/chat?contextConversationId=...` 临时会话详情。
- 已完成证据：
  - `src/pages/treehole/index.vue` 已在 `replyMood()` 成功后调用 `content.createContextChatRequest()`。
  - `src/services/businessApi.test.ts` 已覆盖 `treehole_comment` 字段映射。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests` 均通过。
  - 接口冒烟：`treehole reply -> context pending -> accept active -> GET conversation treehole_comment -> send sent`，摘要见 `output/playwright/treehole-context-smoke.json`。
  - 截图：`output/playwright/user-treehole-context-request-pending.png`。
- 后续待接入：
  - 游戏房间、扩列匹配入口复用本轮临时会话详情。
  - 将 context request/conversation/message 从内存 store 迁移到真实数据库和审计表。

## R-015 LOOP-11 游戏房间上下文确认入口

- 日期：2026-06-29
- 来源：LOOP-11 游戏房间上下文确认入口最小闭环。
- 优先级：P1
- 状态：已完成最小闭环，生产持久化仍待后续 LOOP。
- 要求：
  - 游戏房间上下文私聊只能来自已有消息会话内的房间创建动作，不能从游戏页冷启动陌生私聊。
  - 请求必须包含 `source_type=game_room`、`source_id=room_id`、`reply_id=thread_id`、`initiator_action=room_confirm`、`evidence_id=game_room:{room_id}`。
  - pending 状态必须在房间面板反馈给用户，不能伪装成普通私信。
  - 如果后续确认返回 `active + conversation_id`，必须复用 `/pages/messages/chat?contextConversationId=...` 临时会话详情。
- 已完成证据：
  - `src/pages/messages/chat.vue` 已在 `createRoom()` 成功后调用 `content.createContextChatRequest()`。
  - `src/services/businessApi.test.ts` 已覆盖 `game_room` + `room_confirm` 字段映射。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests` 均通过。
  - 接口冒烟：`create room -> context pending -> accept active -> GET conversation game_room -> send sent`，摘要见 `output/playwright/game-room-context-smoke.json`。
  - 截图：`output/playwright/user-game-room-context-request-pending.png`。
- 后续待接入：
  - 扩列/附近的人匹配入口必须先证明存在明确匹配或确认动作。
  - 将 context request/conversation/message 从内存 store 迁移到真实数据库和审计表。

## R-016 LOOP-12 附近的人好友规则残留纠偏

- 日期：2026-06-29
- 来源：LOOP-12 附近的人好友规则残留纠偏与扩列入口判定。
- 优先级：P1
- 状态：规则残留已完成纠偏，`match_expand` 入口因缺少匹配/确认动作暂不接入。
- 要求：
  - 好友申请不得表达“好友通过后才打开私信”的旧规则。
  - 好友关系用于长期关系沉淀、资料可见性和更低频控限制，不是上下文私聊唯一门槛。
  - 附近的人页不得出现无上下文陌生私聊入口。
  - `match_expand` 只有在存在双方匹配或确认动作后才允许接入。
- 已完成证据：
  - `backend/app/db_business.py` 好友申请通知已改为新规则文案。
  - `src/services/mockApi.ts` mock 好友申请通知已同步新规则文案。
  - `src/pages/nearby/index.vue` 申请好友后展示新规则状态。
  - `backend/tests/test_api_contract.py` 新增通知文案契约测试。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests` 均通过。
  - 旧规则搜索无命中：`通过后才会打开私信|同意后才能聊天|好友申请通过后才|不能直接私聊|陌生人不能直接私聊`。
  - 接口冒烟：`friend-request -> messages notification`，摘要见 `output/playwright/nearby-friend-rule-smoke.json`。
  - 截图：`output/playwright/user-nearby-friend-context-rule.png`。
- 后续待接入：
  - 若产品新增附近的人双方匹配/确认动作，再接入 `source_type=match_expand`。
  - 将 context request/conversation/message 从内存 store 迁移到真实数据库和审计表。

## R-017 LOOP-13 附近的人 VIP/5积分继续聊门槛

- 日期：2026-06-30
- 来源：用户要求“附近的人当前只有关注和申请好友设置为只有VIP，或者消耗5个积分才能聊天”。
- 优先级：P1
- 状态：已完成最小闭环，生产持久化仍待后续 LOOP。
- 要求：
  - 附近的人页面可发起继续聊申请，但不得直接打开陌生私聊。
  - VIP 用户可免费发起附近继续聊申请。
  - 非 VIP 用户必须消耗 5 积分才能发起附近继续聊申请。
  - 发起后必须进入 `pending` 上下文申请，等待对方确认后才允许创建临时会话。
  - 请求必须保留 `source_type=match_expand`、`source_id=nearby:{target_user_id}`、`reply_id`、`initiator_action=continue_chat` 和 `evidence_id`。
- 已完成证据：
  - `backend/app/routes/chat.py` 新增 `POST /chat/match-expand-requests`。
  - `backend/app/db_business.py` 新增 VIP 免费或非 VIP 扣 5 积分的门槛逻辑。
  - `backend/app/schemas.py` 新增 `MatchExpandContextResponse`。
  - `src/services/businessApi.ts`、`src/stores/content.ts`、`src/types/domain.ts` 已接入前端契约和 store 方法。
  - `src/pages/nearby/index.vue` 已新增“继续聊”按钮、VIP/积分提示和 pending 状态反馈。
  - `src/services/businessApi.test.ts` 已覆盖前端请求与响应映射。
  - `backend/tests/test_api_contract.py` 已覆盖 VIP 免费和非 VIP 扣 5 积分。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests` 均通过。
  - 接口冒烟：VIP `cost_coins=0` 且积分不变；非 VIP `cost_coins=5` 且积分从 80 降为 75；两者均返回 `pending + match_expand`，摘要见 `output/playwright/match-expand-gate-smoke.json`。
  - 截图：`output/playwright/user-nearby-match-expand-pending.png`。
- 后续待接入：
  - 将 context request/conversation/message/report/block/audit refs 从内存 store 迁移到真实数据库和审计表。
  - 为积分扣减补幂等键、重复发起频控和审计落库。

## R-018 LOOP-14 附近的人与消息界面压缩优化

- 日期：2026-06-30
- 来源：用户提供附近的人和消息页参考图，要求“参考这个页面设计和样式，注意筛选功能，聊天界面优化，按照给到的图片和压缩”。
- 优先级：P1
- 状态：已完成 UI 最小闭环。
- 要求：
  - 附近的人页面参考深色同城列表样式，保留筛选能力。
  - 附近的人卡片要更紧凑，突出头像、昵称、标签、统计和开聊入口。
  - 消息页参考三入口结构，包含留言消息、精准查找、系统消息。
  - 消息页必须展示真实私聊列表，而不是只有空状态。
  - 聊天详情页需要压缩和深色优化。
- 已完成证据：
  - `src/pages/nearby/index.vue` 已新增筛选图标、搜索栏、深色列表和紧凑卡片。
  - `src/pages/messages/index.vue` 已新增三入口和真实私聊列表。
  - `src/pages/messages/chat.vue` 已优化聊天详情深色布局，并将普通会话来源标签改为“互动来源”。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 均通过。
  - 截图：`output/playwright/user-nearby-redesign-filters.png`、`output/playwright/user-messages-redesign-list.png`、`output/playwright/user-chat-redesign-detail.png`。
- 后续待接入：
  - 附近的人继续聊重复发起需要幂等键、已有 pending 复用和重复扣费保护。
  - 若要完全贴近参考图，可继续替换为真实头像资源和真实省市字段。

## R-019 LOOP-16 删除树洞与消息承接最小闭环

- 日期：2026-06-30
- 来源：用户要求删除树洞功能，并重新设计消息位置和消息邀请卡片。
- 优先级：P0
- 状态：已完成 LOOP-16 最小闭环；消息邀请卡片同意/取消与二次跳转拆入 LOOP-20。
- 要求：
  - 删除用户端树洞功能入口，底部 tab 从 `瓶子 / 广场 / 游戏 / 树洞 / 我的` 改为 `瓶子 / 广场 / 游戏 / 消息 / 我的`。
  - 游戏页不得再出现树洞入口。
  - 消息页承接树洞位置，必须展示后端数据库或测试数据库生成的假消息数据。
  - 消息邀请卡片、同意/取消、同意后二次跳转不纳入 LOOP-16，本项拆入 R-023 / LOOP-20。
  - 历史文档中的树洞完成项保留为历史记录，但新功能不得继续依赖树洞。
- 验收：
  - `src/pages.json` 不再把树洞配置为 tab。
  - 用户端页面不再有树洞入口或树洞跳转。
  - 消息邀请卡片、同意/取消、二次点击跳转由 R-023 / LOOP-20 独立验收。
  - H5 截图覆盖消息 tab 和游戏页无树洞入口。
- LOOP-16 已完成证据：
  - `src/pages.json` 不再注册 `pages/treehole/index`，底部第 4 个 tab 改为 `pages/messages/index`。
  - `src/pages/game/index.vue` 已移除树洞星球入口、`goTreehole()` 和相关样式。
  - `src/pages/messages/index.vue` 将历史 `treehole` 类型承接到消息页，展示层清洗为“留言”。
  - 验证命令通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
  - 路由/接口冒烟：`GET http://127.0.0.1:5175/#/pages/messages/index` 200；`GET http://127.0.0.1:5175/#/pages/game/index` 200；`GET http://127.0.0.1:8110/messages` 200。
  - 截图：`output/playwright/loop16-messages-tab.png`、`output/playwright/loop16-game-no-treehole.png`。

## R-020 LOOP-17 游戏随机匹配入口与筛选

- 日期：2026-06-30
- 来源：用户要求游戏增加随机匹配入口，点击可跳转，并增加性别和年龄筛选，次数与其他次数一致。
- 优先级：P1
- 状态：已完成 LOOP-17 最小闭环；统一城市筛选仍拆入 LOOP-18。
- 要求：
  - 游戏页新增随机匹配入口。
  - 点击随机匹配入口可跳转到匹配页或打开匹配面板。
  - 匹配支持性别筛选和年龄区间筛选。
  - 匹配次数从统一 quota/用户状态读取，不能硬编码。
  - 匹配成功后可进入房间或临时会话；必须保留来源和审计。
- 验收：
  - H5 游戏页有随机匹配入口截图。
  - 随机匹配筛选面板有性别和年龄筛选截图。
  - 接口冒烟覆盖匹配请求、次数扣减/剩余次数、无匹配不扣次数。
  - 前端测试覆盖随机匹配请求参数映射。
- LOOP-17 已完成证据：
  - `src/pages/game/index.vue` 已新增随机匹配入口，点击进入 `pages/game/match`。
  - `src/pages/game/match.vue` 已提供真心话/大冒险次数、性别筛选和年龄区间筛选；结果头像不再显示文字。
  - `POST /game/random-match` 已返回 `game_room` 来源、`room_id/source_id/evidence_id` 和 `next_action=wait_confirm`。
  - 接口冒烟：`output/playwright/game-random-match-smoke.json` 记录真心话次数 `10 -> 9`，无匹配返回 `404` 且大冒险次数 `10 -> 10`。
  - 截图：`output/playwright/loop17-game-random-entry.png`、`output/playwright/loop17-game-random-filter.png`、`output/playwright/loop17-game-random-result.png`。

## R-021 LOOP-18 统一城市筛选与附近的人年龄双端滑条

- 日期：2026-06-30
- 来源：用户要求附近的人年龄筛选使用双端进度条，删除距离筛选，城市筛选统一为全国/热门城市/全部展开。
- 优先级：P1
- 状态：已完成 LOOP-18 最小闭环；其他页面接入同一城市源可按后续 LOOP 扩展。
- 要求：
  - 附近的人年龄筛选改为双端进度条，可两头拉动。
  - 附近的人不再显示距离筛选。
  - 城市筛选默认显示 `全国 / 北京 / 上海 / 广州 / 深圳 / 全部`。
  - 点击“全部”展开全国其他城市或省份；布局按页面空间调整。
  - 所有涉及城市筛选的页面必须复用同一套城市选择规则。
- 验收：
  - 附近的人截图显示双端年龄滑条、城市筛选，不显示距离筛选。
  - 广场/随机匹配等城市筛选页面使用同一套城市组件或同一数据源。
  - H5 构建和前端测试通过。
- LOOP-18 已完成证据：
  - `src/constants/product.ts` 已新增 `primaryCityOptions` 和 `expandedCityOptions`，供后续城市筛选页面复用。
  - `GET /nearby/users` 已支持 `city` 查询参数，并返回 `city` 字段；年龄筛选改为区间重叠匹配。
  - `src/pages/nearby/index.vue` 已删除距离筛选，改为城市筛选、性别筛选、双端年龄滑条。
  - 接口冒烟：`output/playwright/nearby-city-age-smoke.json` 验证 `city=杭州&gender=女&age_range=24-31` 返回杭州女性且年龄区间重叠；`city=全国` 返回更大集合。
  - 截图：`output/playwright/loop18-nearby-city-age-filter.png`、`output/playwright/loop18-nearby-city-expanded-age-drag.png`。

## R-022 LOOP-19 头像资源与用户资料同步

- 日期：2026-06-30
- 来源：用户要求所有头像不准显示字体，用户设置头像优先，否则使用网上找的随机头像。
- 优先级：P1
- 状态：LOOP-19 已完成核心 H5 头像最小闭环；历史页面与后台非核心头像清理保留为后续 P2。
- 要求：
  - 所有头像组件不得再显示文字头像。
  - 用户设置了 `avatar_url` 时必须显示用户头像。
  - 用户未设置头像时必须显示系统随机头像，不允许显示昵称首字或文字。
  - 头像池需至少几十张，来源需可商用或免费使用，并保留来源说明。
  - 用户更新资料后，附近的人、消息、匹配和聊天页必须同步最新头像与资料。
- 已选来源：
  - DiceBear HTTP API `open-peeps` 风格，按稳定 seed 生成系统头像；前后端均通过 30 个 `bottle-wave-01..30` seed 做随机兜底。
  - 用户显式 `avatar_url` 优先；没有用户头像时才使用系统头像 URL。
- 验收：
  - 搜索业务代码不再存在文字头像兜底渲染。
  - 至少 30 个系统随机头像 URL 或本地缓存资源可用。
  - H5 截图覆盖附近的人、消息列表、聊天详情都显示图片头像。
  - 用户资料更新后刷新列表能显示新头像。
- LOOP-19 已完成证据：
  - `src/utils/avatar.ts` 新增 30 个系统头像 seed 和 `resolveAvatarUrl()`，统一 `avatar_url` 优先、系统头像兜底。
  - `backend/app/db_business.py` 为当前用户、种子用户、附近的人、消息会话参与者返回 DiceBear 图片头像 URL。
  - `src/pages/nearby/index.vue`、`src/pages/messages/index.vue`、`src/pages/messages/chat.vue` 已移除本轮目标头像文字兜底，改为图片头像或无文字图形占位。
  - `src/stores/content.ts` 在用户资料更新后同步更新当前用户在附近的人列表中的头像、昵称、城市和年龄资料。
  - 接口冒烟：`output/playwright/avatar-url-smoke.json` 验证 `/me/status`、`/nearby/users`、`/conversations` 均返回图片头像，并验证显式 `avatar_url` 更新后被保留。
  - 截图：`output/playwright/loop19-nearby-image-avatars.png`、`output/playwright/loop19-messages-image-avatars.png`、`output/playwright/loop19-chat-image-avatar.png`。
  - UI 断言：`output/playwright/loop19-avatar-ui.json` 记录附近的人 9/9、消息列表 5/5、聊天详情 1/1 均为图片头像且头像节点文本为空。
  - 已通过 `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
## R-023 LOOP-20 消息邀请卡片同意/取消与二次跳转
- 日期：2026-06-30
- 来源：用户要求“消息邀请功能应该是卡片形式，并且可以跳转同意、取消；同意后二次点击此房间直接跳转”。
- 优先级：P1
- 状态：LOOP-20 已完成最小闭环；生产持久化仍按 R-024 / LOOP-21 处理。
- 要求：
  - 消息页以卡片形式展示邀请数据。
  - 邀请卡片支持同意、取消。
  - 同意后生成或绑定房间/会话。
  - 已同意邀请二次点击时直接跳转房间或会话详情。
  - 后端测试数据或测试数据库需要生成可验证邀请数据。
- 验收：
  - 消息页截图显示邀请卡片。
  - 接口冒烟覆盖列表、同意、取消和二次跳转状态。
  - H5 点击同意后可进入房间或临时会话详情。
- LOOP-20 已完成证据：
  - `backend/app/routes/chat.py` 新增 `GET /chat/context-requests` 用户侧邀请列表。
  - `backend/app/chat_store.py` 为当前用户生成稳定测试邀请卡片，并保留同意后 active `conversation_id`，取消后变为 `expired`。
  - `src/services/businessApi.ts`、`src/stores/content.ts` 已接入邀请列表、同意、取消。
  - `src/pages/messages/index.vue` 已以卡片形式展示邀请，pending 状态支持“同意/取消”，active 状态点击卡片直接进入临时会话详情。
  - 接口冒烟：`output/playwright/message-invitation-smoke.json` 覆盖列表、同意、二次读取 active 卡片、会话详情、取消。
  - 截图：`output/playwright/loop20-message-invite-card-pending.png`、`output/playwright/loop20-message-invite-accepted-chat.png`、`output/playwright/loop20-message-invite-card-active.png`。
  - UI 断言：`output/playwright/loop20-message-invite-ui.json` 记录 pending 卡片包含同意/取消，同意后 hash 进入 `contextConversationId`，active 卡片二次点击仍进入同一会话。
  - 已通过 `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。

## R-024 LOOP-21 上下文会话生产持久化
- 日期：2026-06-30
- 来源：LOOP-13/14 后续生产级验证要求。
- 优先级：P1
- 状态：LOOP-21 已完成最小生产持久化闭环。
- 要求：
  - 将 context request / conversation / message / report / block / audit refs 从内存 store 迁移到数据库。
  - 保持现有接口契约不变。
  - 服务重启后仍可读取已创建会话。
- 验收：
  - 后端测试覆盖创建会话、重启或重建 store 后读取会话。
  - 接口冒烟覆盖 pending -> active -> GET conversation -> send message。
  - 文档记录数据库表、迁移和回滚边界。
- LOOP-21 已完成证据：
  - `backend/app/models.py` 新增 `chat_context_requests`、`chat_conversations`、`chat_messages`、`chat_conversation_reports`、`chat_conversation_blocks`。
  - `backend/alembic/versions/0011_context_chat_persistence.py` 新增真实数据库迁移和 downgrade 回滚。
  - `backend/app/chat_store.py` 已从内存 dict 迁移为 SQLAlchemy 数据库读写；保留旧 dict 仅用于重启式测试清空，不再承载状态。
  - `backend/app/routes/chat.py` 已改为基于 `AsyncSession` 的 async 路由，保持现有接口路径和响应契约不变。
  - 后端测试：`test_context_conversation_survives_memory_store_reset` 覆盖创建、确认、发送消息后清空旧内存容器仍可读取会话和消息。
  - 接口冒烟：`output/playwright/context-persistence-smoke.json` 覆盖创建 pending、accept active、send message、真实重启 8110 后 GET detail/list 仍能读到同一会话。
  - 截图：`output/playwright/loop21-persisted-conversation-after-restart.png` 展示真实重启后 H5 仍能打开同一临时会话详情。
  - UI 断言：`output/playwright/loop21-persisted-conversation-ui.json` 记录同一 `contextConversationId` 和页面 hash。
  - 已通过 `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。

## R-025 LOOP-22 附近的人继续聊重复扣费保护

- 日期：2026-06-30
- 来源：LOOP-13/14 后续风险项，附近的人重复发起可能重复扣 5 积分。
- 优先级：P1
- 状态：LOOP-22 已完成最小幂等闭环。
- 要求：
  - 同一发起人、同一目标、同一 `source_type=match_expand`、同一 `source_id=nearby:{target_user_id}`，存在 pending/active 时必须复用已有请求。
  - 非 VIP 首次发起仍扣 5 积分；重复发起不得再次扣积分。
  - 前端重复发起时要展示“复用申请，不重复扣积分”的状态反馈。
- 验收：
  - 后端测试覆盖首次扣 5、第二次不扣、请求 ID 相同。
  - 接口冒烟覆盖积分前后值、请求 ID 复用、第二次 `cost_coins=0`。
  - H5 截图显示复用状态反馈。
- LOOP-22 已完成证据：
  - `backend/app/db_business.py` 在扣费前查询已有 pending/active `match_expand` 请求，存在则直接返回并设置 `cost_coins=0`。
  - `src/pages/nearby/index.vue` 已把 `costCoins=0` 的反馈改为“已复用申请，不重复扣积分”。
  - 后端测试：`test_match_expand_context_request_reuses_existing_pending_without_second_charge` 覆盖请求 ID 复用和二次不扣费。
  - 接口冒烟：`output/playwright/match-expand-idempotency-smoke.json` 记录积分 `70 -> 65 -> 65`，两次请求 ID 相同，第二次 `costCoins=0`。
  - 截图：`output/playwright/loop22-match-expand-idempotency.png`。
  - UI 断言：`output/playwright/loop22-match-expand-idempotency-ui.json` 记录状态文案“已复用申请，不重复扣积分”。
  - 已通过 `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
## R-026 LOOP-23 可见头像文字兜底清理

- 日期：2026-06-30
- 来源：LOOP-19 后续 P2；用户要求“所有头像不准显示字体，如果用户没有设置，用随机的，如果用户设置了，必须是用户的”。
- 优先级：P2
- 状态：LOOP-23 已完成可见 UI 最小清理。
- 要求：
  - H5 可见页面头像不得在缺少 `avatar_url/icon_url` 时回退为文字。
  - 后台管理端用户、内容、聊天、举报和审计中的头像位不得显示文字 fallback。
  - 保留 `avatar_text/icon_text` 作为后端兼容字段和礼物图标字段，不做破坏性 schema 删除。
- LOOP-23 已完成证据：
  - `src/pages/bottle/index.vue`、`src/pages/plaza/index.vue`、`src/pages/plaza/comments.vue`、`src/pages/home/index.vue`、`src/pages/profile/index.vue`、`src/pages/creator/index.vue`、`src/pages/treehole/index.vue` 可见头像 fallback 已统一调用 `resolveAvatarUrl()`。
  - `admin-web/src/AdminApp.vue` 用户、内容作者、聊天参与者、举报目标、审计操作人头像 fallback 已改为 DiceBear 图片 URL。
  - 接口冒烟：`output/playwright/avatar-url-smoke.json` 验证 `/me/status`、`/nearby/users`、`/conversations` 均返回图片头像 URL，显式 `avatar_url` 更新后保留用户头像。
  - UI 断言：`output/playwright/loop23-avatar-fallbacks-ui.json` 验证广场列表 3/3、广场评论 2/2、我的页 1/1、后台用户页 10/10 均为图片头像且头像节点文本为空。
  - 截图：`output/playwright/loop23-plaza-avatar-fallbacks.png`、`output/playwright/loop23-plaza-comment-avatar-fallbacks.png`、`output/playwright/loop23-profile-avatar-fallback.png`、`output/playwright/loop23-admin-avatar-fallbacks.png`。
  - 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- 后续：
  - `avatar_text/icon_text` 字段仍作为接口兼容和礼物图标字段保留；如要做字段级重命名或 schema 删除，需要单独数据库迁移 LOOP。
## R-027 LOOP-24 自动总验收与剩余队列

- 优先级：P1
- 状态：已完成自动总验收；当前代码门禁通过，剩余生产级大项进入后续 LOOP 队列。
- 范围：
  - 复跑类型检查、前端测试、H5 构建、admin 构建、后端 pytest 与 Python 编译。
  - 复跑上下文私聊、消息邀请、会话持久化、扩列幂等、附近的人筛选、好友申请规则、游戏随机匹配和头像兜底接口冒烟。
  - 复跑消息邀请卡片、持久化会话、扩列幂等、附近的人筛选、头像图片兜底截图。
- 验收证据：
  - `npm run typecheck`：通过。
  - `npm run test:frontend`：4 个测试文件、27 条测试通过。
  - `npm run build:h5:e2e`：通过。
  - `npm run build:admin`：通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：54 passed。
  - `python -m compileall -q backend\app backend\tests`：通过。
  - 接口冒烟：`avatar-url-smoke.cjs`、`message-invitation-smoke.cjs`、`context-persistence-smoke.cjs`、`match-expand-idempotency-smoke.cjs`、`nearby-city-age-smoke.cjs`、`nearby-friend-rule-smoke.cjs`、`game-random-match-smoke.cjs` 均通过。
  - 截图复验：`loop20-message-invite-card-pending.png`、`loop20-message-invite-accepted-chat.png`、`loop20-message-invite-card-active.png`、`loop21-persisted-conversation-after-restart.png`、`loop22-match-expand-idempotency.png`、`loop18-nearby-city-age-filter.png`、`loop18-nearby-city-expanded-age-drag.png`、`loop23-plaza-avatar-fallbacks.png`、`loop23-plaza-comment-avatar-fallbacks.png`、`loop23-profile-avatar-fallback.png`、`loop23-admin-avatar-fallbacks.png`。
- 剩余队列：
  - 生产级管理员真实账号和完整权限矩阵仍是大范围 P0。
  - 真实 PostgreSQL/Alembic/Redis 迁移执行仍是大范围 P0，涉及真实数据库迁移暂停条件。
  - 私密照片真实上传、收益流水、申诉链路仍是 P0/P1 后续项。
  - 字段级错误码、审计链路完善和高级筛选仍是 P1 后续项。
## R-028 LOOP-25 管理员真实账号与权限矩阵最小闭环

- 优先级：P0
- 状态：已完成最小闭环；生产级外部身份源、多因素和完整细粒度权限仍留待后续增强。
- 范围：
  - 后端支持 `ADMIN_ACCOUNTS` 配置多个管理员账号，默认包含 `admin`、`moderator`、`risk`。
  - 登录后返回签名 session token，不再只依赖单一固定 mock token；保留旧 `ADMIN_MOCK_TOKEN` 兼容测试和本地脚本。
  - `/admin/summary`、`/admin/users`、`/admin/content`、`/admin/audit`、`/admin/wallet`、`/admin/verification`、`/admin/reports`、`/admin/chats`、`/admin/referral`、`/admin/nearby`、`/admin/plaza`、`/admin/reward-config` 均要求 bearer token。
  - `moderator` 可读取后台数据，但更新奖励配置必须返回 `ADMIN_FORBIDDEN`。
- 验收证据：
  - `node output\playwright\admin-auth-smoke.cjs`：未登录读取 401、坏 token 401、admin 读取 200、moderator 读取 200、moderator 更新奖励配置 403。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：55 passed。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`python -m compileall -q backend\app backend\tests` 均通过。
  - 后台截图：`output/playwright/loop25-admin-auth-dashboard.png`。
- 后续项：
  - 接企业真实身份源、密码哈希存储、MFA、操作级权限矩阵和审计检索仍为后续 P1/P0，不在本轮扩大。
## R-029 LOOP-26 真实 PostgreSQL/Alembic/Redis 迁移执行验收

- 优先级：P0
- 状态：已解除阻塞并通过；Docker Desktop 启动后已用临时 PostgreSQL/Redis 容器完成真实迁移和接口冒烟。
- 已验证：
  - Alembic 配置存在：`backend/alembic.ini`、`backend/alembic/env.py`。
  - 迁移文件存在至 `0011_context_chat_persistence.py`。
  - PostgreSQL 方言离线 SQL 可生成：`backend/runtime/loop26-postgres-upgrade.sql`，大小 59594 bytes。
  - 真实 PostgreSQL 连接失败：`ConnectionRefusedError: [WinError 1225]`。
  - Redis 连接失败：`TimeoutError: Timeout connecting to server`。
  - Docker daemon 连接失败：`failed to connect to the docker API ... dockerDesktopLinuxEngine`。
  - SQLite 隔离迁移不能替代真实 PG：在 `0002_bottle_relation_models` 的 `create_unique_constraint` 处因 SQLite 不支持 ALTER constraint 失败。
- 阻塞条件：
  - 需要可控测试 PostgreSQL 和 Redis 实例，或允许启动 Docker Desktop 并创建临时容器。
  - 需要明确测试库 URL，避免误连真实生产数据。
- 下一步：
  - 已执行 `python -m alembic -c backend/alembic.ini upgrade head` 到 `0011_context_chat_persistence (head)`。
  - 已启动 `drift-loop26-postgres` 与 `drift-loop26-redis` 临时容器，端口分别为 `55432`、`56379`。
  - 已修复 PostgreSQL 严格外键下种子广场动态父子落库顺序：`backend/app/db_business.py` 中先 flush `PlazaPost` 再插入 `PlazaMedia`。
  - 已通过 `node output\playwright\admin-auth-smoke.cjs` 和 `node output\playwright\context-persistence-postgres-smoke.cjs`。
  - 已通过后端测试、前端测试、H5 构建和 admin 构建。
## R-030 LOOP-27 私密照片真实上传、收益冻结和申诉最小闭环

- 优先级：P0
- 状态：已完成最小闭环。
- 范围：
  - `private_photo_assets` 增加审核、风险、收益、申诉、审计字段，并通过 Alembic `0012_private_photo_reviews` 迁移。
  - `POST /private-photos` 从内存 store 改为数据库持久化，保留 AI mock 风险分级。
  - `GET /private-photos/{id}`、`POST /private-photos/{id}/unlock`、admin review/risk summary 改为数据库读取。
  - 新增 `POST /private-photos/{id}/appeal`：仅 rejected/frozen 可申诉，申诉后 `appeal_pending`，收益保持 `frozen`，审核前不可解锁。
  - 后台内容队列兼容私密照片细分审核状态，映射为通用 pending/approved/rejected。
- 验收证据：
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：56 passed。
  - `python -m compileall -q backend\app backend\tests`：通过。
  - `python -m alembic -c alembic.ini current`：`0012_private_photo_reviews (head)`。
  - `node output\playwright\private-photo-postgres-smoke.cjs`：通过，低风险可解锁，高风险冻结后申诉进入 `appeal_pending`，后台队列可见。
  - PostgreSQL 证据：`private_photo_assets` 最新申诉行 `appeal_pending|frozen|pending:误判申诉，要求人工复核`。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin` 均通过。
  - 截图：`output/playwright/loop27-private-photo-review-admin.png`；断言 JSON：`output/playwright/loop27-private-photo-review-admin.json`。
- 后续：
  - 真实对象存储签名上传、图片二进制扫描、多模型审核和申诉后台操作流仍可作为后续 P1/P0 继续拆分。

## R-031 LOOP-28 字段级错误码与审计链路收口

- 优先级：P1
- 状态：已完成最小闭环，作为当前 P0/P1 LOOP 队列收口。
- 范围：
  - 请求校验错误统一返回 `VALIDATION_ERROR`，并在 `details.field_errors[]` 中提供字段路径、字段级错误码和消息。
  - 保留 `details.raw_errors`，避免破坏依赖 FastAPI/Pydantic 原始错误结构的旧调用方。
  - 私密照片 AI 审核、解锁、申诉、人工复核写入数据库审计表，并让业务行 `audit_refs` 指向同一个审计 ID。
  - 后台 `/admin/audit` 返回数据库审计记录，同时兼容旧内存审计记录。
  - 后台审计页对私密照片动作和目标类型给出明确文案。
- 验收证据：
  - 后端测试：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`，57 passed。
  - 前端测试：`npm run test:frontend`，4 个测试文件、27 条测试通过。
  - 构建：`npm run build:h5:e2e`、`npm run build:admin` 均通过。
  - PostgreSQL：`python -m alembic -c alembic.ini current` 返回 `0012_private_photo_reviews (head)`。
  - 接口冒烟：`output/playwright/loop28-error-audit-smoke.json`。
  - 后台截图：`output/playwright/loop28-admin-audit.png`，断言 `hasAppeal=true`、`hasTarget=true`。
- 高级筛选验收边界：
  - 当前后台已有内容/举报/聊天/照片审核分区和照片审核风险/状态查询能力，满足本轮最小管理验收。
  - 跨模块复合筛选、保存筛选条件、导出和更细权限化筛选不属于当前 P1 门禁，列入 P2 增强。
## R-032 LOOP-29 小程序桥接与广告激励视频配置最小闭环

- 日期：2026-06-30
- 来源：用户要求启动服务并处理界面细节，同时增加更多小程序入口、后续小程序桥接、广告联盟配置、广告展示倒计时，以及看视频获得次数。
- 优先级：P1
- 状态：已完成最小闭环；真实广告联盟 SDK、服务端回调验签和反作弊计费归入后续 P1/P2 增强。
- 范围：
  - 用户端新增 `pages/ad/reward` 激励视频页，展示广告联盟、广告位、倒计时、素材、落地页、小程序 AppID 和路径。
  - 首页和签到页原“看广告拿次数”入口改为进入激励视频页，不再直接发放奖励。
  - 后端新增数据库配置表 `app_configs`，后台可配置广告展示类型、广告联盟、广告位、素材 URL、落地页、倒计时、小程序桥接和奖励次数。
  - `/me/status` 与 `/ads/reward/prepare` 返回后台配置，`/ads/reward/commit` 在倒计时后发放次数。
  - admin-web 新增“广告配置”页，支持配置广告联盟、小程序桥接、倒计时和奖励次数。
- 验收证据：
  - 后端测试：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`，58 passed。
  - 前端测试：`npm run test:frontend`，4 files / 27 tests passed。
  - 构建：`npm run typecheck`、`npm run build:h5:e2e`、`npm run build:admin` 均通过。
  - 接口冒烟：`output/playwright/loop29-ad-bridge-smoke.json`，记录 provider=`loop29_alliance`、placement=`loop29_reward_video`、countdown=3、reward delta=3。
  - UI 截图：`output/playwright/loop29-h5-reward-ad.png`、`output/playwright/loop29-admin-ad-config.png`。
- 后续：
  - 接入微信小程序真实 `wx.navigateToMiniProgram` 和广告联盟激励视频 SDK。
  - 增加广告服务端回调验签、播放完成证明、反作弊、频控、收益报表和投放位 AB 配置。
## R-033 LOOP-30 前台聊天输入状态机与发布弹窗 UI 纠偏

- 日期：2026-06-30
- 来源：用户提供聊天页与发布弹窗截图，并要求按 UI/UX、业务状态机、边界场景持续 LOOP 执行，不能只分析或只写报告。
- 优先级：P1
- 状态：已完成本轮最小闭环；后台证据链详情、未读域拆分、游戏入口重构等保留后续独立 LOOP。
- 范围：
  - 聊天页输入区改为主流 IM 结构：左侧麦克风、中间输入框、右侧发送或加号。
  - 有文本时显示发送按钮；无文本时显示加号按钮。
  - 加号面板移动到输入行下方并压缩高度，避免大面积遮挡聊天内容。
  - 麦克风入口切换语音模式，并关闭加号面板。
  - 发布弹窗移除大块文字式媒体选择，改为图片/视频图标入口，底部仅保留取消和发布。
  - 发布弹窗支持视频选择和预览，取消时清理临时媒体。
- 验收证据：
  - 一键验收：`.\scripts\run-ui-message-admin-loop.ps1` 通过。
  - H5/后台截图：`reports/ui-message-admin-loop/screenshots/`。
  - UI 冒烟：`reports/ui-message-admin-loop/e2e-results.json`，失败用例数 0。
  - 前端测试：`npm run test:frontend`，4 files / 27 tests passed。
  - 后端测试：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`，58 passed。
- 后续：
  - 未读域拆分、头像点击规则、删除/封禁/拉黑/注销边界状态。
  - 后台私密照片审核详情闭环和举报用户证据链搜索。
## R-034 LOOP-31 消息页信息架构纠偏与发现入口移除

- 日期：2026-06-30
- 来源：用户要求按 UI/UX、业务状态机和边界场景持续 LOOP 验收；消息页应承接私聊、留言消息和系统消息，不混入发现/匹配功能。
- 优先级：P1
- 状态：已完成 LOOP-31 最小闭环。
- 范围：
  - 消息页顶部快捷入口从 `留言消息 / 精准查找 / 系统消息` 调整为 `留言消息 / 系统消息`。
  - 移除消息页到附近的人/发现页的 `openNearby` 跳转入口。
  - 一键验收脚本增加结构性断言：quick-action 必须为 2 个，存在 mail/system，不存在 target。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：58 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - UI 冒烟：`reports/ui-message-admin-loop/e2e-results.json` 中 `quickActionCount=2`、`hasDiscoveryEntry=false`。
  - 截图：`reports/ui-message-admin-loop/screenshots/mobile-390-messages.png`。
- 后续：
  - 消息页上下双标题栏、未读域清除规则、邀请卡片与私聊列表分区细节继续拆入后续 LOOP。
## R-035 LOOP-32 消息页标题栏冗余与未读清除状态机

- 日期：2026-06-30
- 来源：LOOP-31 截图目检发现消息页系统标题栏和自绘标题栏叠加；用户要求持续 LOOP 验收失败先修复。
- 优先级：P1
- 状态：已完成 LOOP-32 最小闭环。
- 范围：
  - `pages/messages/index` 改为 `navigationStyle=custom`，保留自绘消息栏，移除 H5 顶部系统标题空隙。
  - 新增 `POST /conversations/{thread_id}/read`，用于进入私聊前持久化清除该会话未读数。
  - 前端 `businessApi.markConversationRead()` 和 `content.markConversationRead()` 接入接口；点击私聊或通知跳转私聊前等待已读落库。
  - UI 冒烟增加等待列表渲染、自绘标题检测和未读清除检测。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 未读 UI 响应：`badge=2 -> badge=0`，`unreadChatHash=#/pages/messages/chat?...`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 28 tests passed。
  - `npm run build:h5:e2e`、`npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：59 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/mobile-390-messages.png`。
- 后续：
  - 留言消息/系统消息单条已读持久化、邀请卡片未读域和 H5/API 端口一致性拆入后续 LOOP。
## R-036 LOOP-33 H5/API E2E 服务端口一致性与一键验收脚本自愈

- 日期：2026-06-30
- 来源：LOOP-32 未读清除验收中发现 H5 dev server 默认连接 8100，而 H5 构建使用 8110，旧后端进程会造成假失败。
- 优先级：P1
- 状态：已完成 LOOP-33 最小闭环。
- 范围：
  - `scripts/run-ui-message-admin-loop.ps1` 新增 `BackendPort` 和 `BackendDatabasePath` 参数。
  - 一键验收开始时自动停止并重启 `BackendPort` 上的 E2E 后端，等待 `/me/status` 可用。
  - 一键验收自动停止并重启 H5 dev server，并注入同一个 `VITE_API_BASE_URL`。
  - H5 构建改为显式调用 `scripts/build-h5-e2e.ps1 -Port $BackendPort`。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - UI 冒烟仍验证消息页入口隔离、自绘标题、未读清除、聊天输入区、发布弹窗和后台截图。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：59 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
- 后续：
  - PostgreSQL/Redis 容器健康检查和端口自动选择可作为后续 P2 增强。
## R-037 LOOP-34 留言消息/系统消息单条已读持久化与邀请卡片未读分区

- 日期：2026-06-30
- 来源：用户指定下一轮进入 LOOP-34：留言消息/系统消息单条已读持久化与邀请卡片未读分区。
- 优先级：P1
- 状态：已完成 LOOP-34 最小闭环。
- 范围：
  - 后端新增 `POST /messages/{message_id}/read`，只把当前用户指定留言或系统通知标记为已读。
  - 前端 `businessApi.markMessageRead()` 和 `content.markMessageRead()` 接入后端已读接口，保留本地即时反馈并由接口结果回填。
  - 消息页把快捷入口角标拆为留言消息未读数和系统消息未读数。
  - 留言消息分区展示待处理邀请、已处理邀请和留言通知；系统消息分区不展示邀请卡片。
  - UI 冒烟补接口直接调用和分区结构断言，并修复从系统通知返回私聊列表的状态复位。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`POST /messages/{id}/read` 返回 `unread=false`，列表复查同一条仍为 `false`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：60 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/mobile-390-message-notices.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-system-notices.png`。
- 后续：
  - 后台消息通知审计查询、通知类型后台配置和更细的邀请未读统计可拆入后续 P2。
## R-038 LOOP-35 后台举报证据链检索与详情可视化

- 日期：2026-06-30
- 来源：LOOP-30/31 后续项保留“后台证据链详情”，用户要求进入 LOOP-35。
- 优先级：P1
- 状态：已完成 LOOP-35 最小闭环。
- 范围：
  - `GET /admin/reports` 增加 `status`、`target_type`、`q` 查询参数。
  - 举报响应新增 `reporter_id`、`evidence_refs`、`audit_refs`，用于后台展示证据链。
  - 聊天举报证据链包含 `report`、`chat`、`reporter`、`conversation`、`thread_status` 引用。
  - 后台举报处置页新增关键词搜索、选中行和证据链详情面板。
  - 一键 UI 冒烟新增后台举报页断言和截图。
  - 一键验收脚本改为每次使用唯一隔离 SQLite，避免旧 E2E 数据库 schema 造成假失败。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`GET /admin/reports?target_type=chat&q=thread` 返回 2 条，第一条含 5 个 `evidence_refs`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：61 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`。
- 后续：
  - 举报处置动作、处罚联动、批量关闭和审计详情页可拆入后续 LOOP。

## R-039 LOOP-36 举报处置动作与审计落库最小闭环

- 日期：2026-06-30
- 来源：用户指定下一轮进入 LOOP-36：举报处置动作与审计落库最小闭环。
- 优先级：P1
- 状态：已完成 LOOP-36 最小闭环。
- 范围：
  - 新增 `POST /admin/reports/{id}/resolve`，要求后台管理员或审核员提交处理原因。
  - 举报处置返回 `before_status`、`after_status`、`reason`、`audit_id` 和 `resolved_at`。
  - 后端把举报状态更新为 `resolved`，并写入 `AdminAuditLog(action=report_resolve,target_type=report)`。
  - `GET /admin/reports` 复查时返回新的 `audit_refs`，后台详情面板展示审计引用。
  - 后台举报处置页新增处理原因输入和“标记已处理”按钮。
  - UI 冒烟补“后台举报处置写入已处理状态和审计引用”断言，并修复 CDP 点击前未滚动导致的按钮假失败。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`POST /admin/reports/{id}/resolve` 返回 200，`after_status=resolved`，`audit_id=audit_...`，列表复查该举报 `audit_refs` 包含该审计 ID。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：62 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`。
- 后续：
  - 举报处置联动内容下线、用户限制、聊天冻结、收益冻结、批量关闭和审计详情页继续拆入后续 LOOP。

## R-040 LOOP-37 举报处罚联动和审计详情页最小闭环

- 日期：2026-06-30
- 来源：用户指定 LOOP-37：举报处罚联动和审计详情页最小闭环，范围仍控制为 1 个 P1。
- 优先级：P1
- 状态：已完成 LOOP-37 最小闭环。
- 范围：
  - `POST /admin/reports/{id}/resolve` 新增可选 `penalty_action`。
  - 当前仅实现 `penalty_action=limit_user`，并且只支持聊天举报。
  - 后端根据聊天举报 `reporter_id` 和 `ConversationThread` 双方关系，限制非举报人的被举报用户。
  - 处罚联动把目标用户状态写为 `limited`，并写入 `AdminUserRestriction`。
  - 审计新增 `report_penalty_limit_user`，同时 `report_resolve` 审计 detail 写入 `penalty_action` 和 `penalty_target_user_id`。
  - `GET /admin/audit` 返回 `detail`。
  - 后台举报详情新增处置动作选择，后台审计页新增审计详情面板。
  - UI 冒烟新增“后台审计详情展示举报处罚联动记录”断言和审计详情截图。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`POST /admin/reports/{id}/resolve` 携带 `penalty_action=limit_user` 返回 200，目标用户 `status=limited`，审计 detail 包含 `penalty_action=limit_user`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：63 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-detail.png`。
- 后续：
  - 内容下线、聊天冻结、收益冻结、批量关闭、二次确认和用户端处罚通知继续拆入后续 LOOP。

## R-041 LOOP-38 举报冻结聊天最小闭环

- 日期：2026-06-30
- 来源：用户要求将 LOOP-38 全部执行完毕；承接 LOOP-37 下一轮建议。
- 优先级：P1
- 状态：已完成 LOOP-38 最小闭环。
- 范围：
  - `POST /admin/reports/{id}/resolve` 新增 `penalty_action=freeze_chat`。
  - 当前 `freeze_chat` 只支持聊天举报，非聊天举报不允许触发。
  - 后端把目标 `ConversationThread.status` 写为 `risk_frozen`。
  - 冻结后 `POST /conversations/{thread_id}/turns` 返回 `403`，错误码 `CHAT_RISK_FROZEN`。
  - 审计新增 `report_penalty_freeze_chat`，`report_resolve` 的 detail 写入 `penalty_action=freeze_chat` 和 `penalty_target_thread_id`。
  - 后台举报处置动作下拉新增“冻结聊天”，并默认走本轮冻结聊天验收路径。
  - UI 冒烟新增“后台审计详情展示举报冻结聊天记录”断言和截图。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`penalty_action=freeze_chat` 返回 200，证据链包含 `thread_status:risk_frozen`，冻结后发消息返回 `CHAT_RISK_FROZEN`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：64 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-detail.png`。
- 后续：
  - 内容下线、收益冻结、批量处置、二次确认、处罚撤销和用户端通知/申诉继续拆入后续 LOOP。

## R-042 LOOP-39 处罚后用户端通知与冻结提示最小闭环

- 日期：2026-06-30
- 来源：用户要求 LOOP-39 验证通过后自动进入下一轮；承接 LOOP-38 的用户端通知/申诉剩余项。
- 优先级：P1
- 状态：已完成 LOOP-39 最小闭环。
- 范围：
  - `penalty_action=freeze_chat` 处置成功后，为举报人生成 `business_type=chat_freeze`、`business_id={thread_id}` 的系统通知。
  - `GET /conversations` 和 `POST /conversations/{thread_id}/read` 继续返回 `risk_frozen` 会话，新增 `frozen_notice`。
  - 消息页把 `chat_freeze` 归入系统消息，点击通知可直达被冻结的聊天详情。
  - 聊天页展示“聊天已冻结”、冻结说明和申诉说明入口。
  - 冻结聊天页禁用输入、媒体、礼物和房间入口；后端继续以 `CHAT_RISK_FROZEN` 拦截发送。
  - UI 冒烟新增“用户端系统通知可进入冻结聊天说明”断言和截图。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`GET /messages` 返回 `chat_freeze` 通知，`POST /conversations/{thread_id}/read` 返回 `status=risk_frozen` 和 `frozen_notice`，发消息返回 `403 / CHAT_RISK_FROZEN`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：64 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/mobile-390-chat-frozen.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-detail.png`。
- 后续：
  - 内容下线、收益冻结、批量处置、二次确认、处罚撤销和真实申诉工单继续拆入后续 LOOP。

## R-043 LOOP-40 冻结聊天恢复与审计最小闭环

- 日期：2026-06-30
- 来源：LOOP-39 验收通过后自动进入下一轮，承接处罚撤销/恢复剩余项。
- 优先级：P1
- 状态：已完成 LOOP-40 最小闭环。
- 范围：
  - 新增 `POST /admin/reports/{id}/restore`。
  - 仅支持 `target_type=chat` 且目标线程 `status=risk_frozen` 的举报恢复。
  - 恢复后目标聊天线程状态写回 `active`。
  - 恢复后生成 `business_type=chat_restore` 的系统通知。
  - 恢复后写入 `AdminAuditLog(action=report_restore_chat,target_type=chat)`。
  - 后台举报详情在已处理且证据链显示 `thread_status:risk_frozen` 时展示“恢复聊天”按钮。
  - UI 冒烟覆盖后台恢复、恢复审计和用户端输入区重新开放。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：冻结后恢复返回 `before_thread_status=risk_frozen`、`after_thread_status=active`，恢复后发送消息成功，存在 `chat_restore` 通知和 `report_restore_chat` 审计。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：65 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - 截图：`reports/ui-message-admin-loop/screenshots/admin-1366-reports-restored.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-restore.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-restored.png`。
- 后续：
  - 真实申诉工单、内容下线、私密照片收益冻结、批量处置和二次确认继续拆入后续 LOOP。

## R-044 LOOP-41 用户端私聊位置、附近开聊和留言即时反馈纠偏

- 日期：2026-06-30
- 来源：用户反馈私聊位置/边界不对、广场帖子留言延迟、附近的人开聊不需要同意且聊天页需要显示双方头像和昵称。
- 优先级：P1
- 状态：已完成 LOOP-41 最小闭环。
- 范围：
  - 附近的人“开聊”不再进入待同意申请，改为 VIP 免费或非 VIP 首次消耗 5 积分后直接创建/复用私聊线程。
  - `POST /chat/match-expand-requests` 成功后返回 `thread_id`，且 `request.status=active`、`request.conversation_id=thread_id`。
  - 用户端附近的人点击“开聊”后直接跳转 `/pages/messages/chat?threadId=...`。
  - 聊天页普通私聊头部展示“我”和对方两侧头像、昵称、来源标签与在线状态，并约束边界避免挤压错位。
  - 广场留言提交成功后先在本页即时追加留言，再异步刷新后端列表。
  - 广场留言时间把后端无时区 UTC ISO 按 UTC 解析，刚提交或 2 分钟内显示“刚刚”。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：`POST /chat/match-expand-requests` 返回 `request_status=active`、`thread_id=thread_88cc44b20ee34011a84ebcc2ba2676a0`、`cost_coins=0`；`POST /conversations/{thread_id}/read` 返回 `conversation_status=active`、`participant_name=海岛来信`、`participant_avatar_url=https://api.dicebear.com/...`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：65 passed。
  - 重点截图：`reports/ui-message-admin-loop/screenshots/mobile-390-nearby-direct-chat.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-plaza-comment-immediate.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-plus-panel.png`。
- 后续：
  - 真实申诉工单仍按 O-044 继续后续独立 LOOP。
  - 广场继续聊仍保持上下文确认规则，本轮只调整附近的人直接开聊规则。

## R-045 LOOP-42 冻结聊天真实申诉工单最小闭环

- 日期：2026-07-01
- 来源：LOOP-41 后续建议，用户要求 LOOP-42 自动自行执行。
- 优先级：P1
- 状态：已完成 LOOP-42 最小闭环。
- 范围：
  - 新增 `chat_appeals` 持久化表和 Alembic 迁移 `0014_chat_appeals.py`。
  - 用户端新增 `POST /conversations/{thread_id}/appeal`，只能对本人 `risk_frozen` 聊天提交申诉。
  - 同一用户同一冻结聊天已有 `pending` 申诉时复用，不重复生成工单。
  - 后台新增 `GET /admin/chat-appeals` 和 `POST /admin/chat-appeals/{id}/review`。
  - 后台通过申诉会把聊天恢复为 `active`，驳回则保持 `risk_frozen`。
  - 申诉提交、通过、驳回均写入审计并生成用户系统通知。
  - 用户端冻结聊天卡片从“客服入口说明”升级为内联申诉输入和提交按钮。
  - 后台举报处置页新增聊天申诉工单列表、申诉详情、通过/驳回按钮。
- 验收证据：
  - `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
  - 接口冒烟：冻结聊天后提交 `appeal_9796fc6bb4a64b5c8f571f2639001c45`，后台列表可见，通过后 `review_after_status=approved`、`review_thread_status=active`、用户通知 `chat_appeal_approved=true`、审计动作为 `chat_appeal_approve`。
  - `npm run typecheck` 通过。
  - `npm run test:frontend`：4 files / 29 tests passed。
  - `npm run build:h5` 和 `npm run build:admin` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：66 passed。
  - `python -m compileall -q backend\app backend\tests` 通过。
  - Alembic：`python -m alembic -c alembic.ini heads` 返回 `0014_chat_appeals (head)`，`upgrade head --sql` 包含 `CREATE TABLE chat_appeals`。
  - 重点截图：`reports/ui-message-admin-loop/screenshots/mobile-390-chat-appeal-submitted.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-chat-appeal-rejected.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-restored.png`。
- 后续：
  - 内容下线、私密照片收益冻结/解冻和批量处置二次确认继续拆入后续独立 LOOP。
## R-047 举报处置内容下线联动

- 来源：LOOP-43。
- 优先级：P1。
- 状态：已完成最小闭环。
- 需求：
  - 后台举报处置支持 `offline_content` 动作。
  - 下线动作覆盖瓶子、广场帖子、广场留言，目标内容从用户端可见列表移除。
  - 下线动作必须写入处罚审计和举报处理审计，保留前后状态、原因、目标内容 ID 和内容类型。
  - 后台举报证据链必须能显示下线后的 `content_status:rejected`。
  - 内容所有者必须收到内容下线通知。
- 验收：
  - 后端契约测试覆盖瓶子、广场帖子、广场留言。
  - 接口冒烟写入 `reports/loop43/api-smoke.json`。
  - 后台 UI 冒烟截图覆盖举报处置和审计详情。
- 后续：
  - 私密照片收益冻结、内容恢复申诉、批量下线和二次确认另拆 LOOP。
## R-048 LOOP-44 举报目标边界与用户信息名片入口

- 日期：2026-07-01
- 来源：用户纠偏“私密照片不需要举报，所有举报都是用户级别，或者用户发布的帖子和漂流瓶，其他类型没有举报”。
- 优先级：P1
- 状态：已完成 LOOP-44 最小闭环，后端旧类型强拒绝另登记为 O-048。
- 需求：
  - 用户端普通举报只允许 `user`、`bottle`、`plaza` 三类目标。
  - 私密照片不提供普通举报入口，继续走 AI 审核、人工复核、申诉、收益冻结/解冻链路。
  - 聊天不提供普通举报入口，继续走上下文风控、拉黑、冻结、聊天申诉链路。
  - 评论不单独举报；如有问题，举报评论作者用户，或举报承载该互动的帖子/漂流瓶。
  - 点击用户头像弹出用户信息名片，名片左上角固定提供“举报”入口。
  - 帖子/漂流瓶内容卡片允许提供内容举报入口。
- 验收：
  - 前端新建举报 API 类型收窄为 `user|bottle|plaza`。
  - 广场帖子卡片提供帖子举报入口。
  - 广场头像点击打开用户信息名片，左上角可举报用户。
  - 不在私密照片、聊天工具区和评论项新增普通举报按钮。
  - 文档明确后台历史旧类型工单只为兼容展示，不代表新用户端入口。
- 已完成证据：
  - `ReportableTargetType` 已收窄为 `user | bottle | plaza`，content store 只暴露用户、广场帖子、漂流瓶三类普通举报入口。
  - `POST /reports` 冒烟：`user`、`plaza`、`bottle` 三类均返回 `queued`，证据 `reports/loop44/api-smoke.json`。
  - 截图：`reports/loop44/screenshots/mobile-390-plaza-report-post-entry.png`、`mobile-390-plaza-user-card-report.png`、`mobile-390-plaza-user-report-modal.png`。
  - 门禁：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`、`python -m pytest backend\tests -q`、`scripts\run-ui-message-admin-loop.ps1` 均通过。
