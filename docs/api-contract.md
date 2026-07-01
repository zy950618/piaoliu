# API Contract

## 用户状态

- `GET /me/status`
- 返回用户资料、VIP、漂流币、今日次数、广告冷却、签到状态、认证状态摘要。

## 次数与奖励

- `GET /quota/today`
- `POST /quota/consume`
- `POST /checkin`
- `GET /checkin/week`
- `GET /ads/reward/status`
- `POST /ads/reward/prepare`
- `POST /ads/reward/commit`

## 内容

- `POST /bottles`
- `GET /bottles/random`
- `POST /bottles/{id}/reply`
- `GET /truth/question/random`
- `GET /dare/task/random`
- 游戏页复用真心话和大冒险接口，前端区分常规/私密模式，后续可扩展 `mode=public|private`。
- `POST /treehole/posts`
- `GET /treehole/feed`
- `POST /treehole/{id}/react`
- `GET /plaza/posts`
- `GET /nearby/users`

列表类接口后续统一支持筛选参数：

- `city`
- `gender`
- `age_range`

## 关系与安全

- `POST /relations/follow`
- `POST /relations/friend-request`
- `POST /reports`
- `POST /blocks`
- `GET /blacklist`

禁止无上下文冷启动私聊。明确互动上下文内的陌生人可以在双向回应/确认后开启带来源的临时私聊；好友关系不是私聊唯一门槛。

### 上下文私聊

#### 来源枚举

- `bottle_reply`
- `plaza_comment`
- `treehole_comment`
- `game_room`
- `private_room`
- `match_expand`
- `friend`

#### 会话状态

- `pending`：已发起，等待对方确认或回应。
- `active`：双方已确认或回应，可发送消息。
- `muted`：用户主动静音或限流。
- `blocked`：任一方拉黑后停止发送。
- `expired`：上下文过期。
- `reported`：会话被举报并进入审核。
- `risk_frozen`：风控冻结，等待处理。

#### `POST /chat/context-requests`

创建上下文私聊申请。

请求字段：

- `target_user_id`：目标用户 ID。
- `source_type`：来源枚举。
- `source_id`：来源对象 ID，例如瓶子回应、帖子评论、房间或匹配 ID。
- `reply_id`：可选，漂流瓶回应或评论回复 ID。
- `initiator_action`：`reply`、`continue_chat`、`private_chat`、`room_confirm`。
- `evidence_id`：双向回应/确认证据 ID。

响应字段：

- `id`：上下文申请 ID。
- `status`：`pending` 或 `active`。
- `conversation_id`：已直接激活时返回。
- `source_summary`：来源卡片摘要。
- `rate_limit`：非好友会话频控摘要。

#### `POST /chat/context-requests/{id}/accept`

确认上下文私聊申请并创建或激活会话。

请求字段：

- `confirm_action`：`reply`、`continue_chat`、`private_chat`、`room_confirm`。
- `evidence_id`：确认动作证据 ID。

响应字段：

- `conversation_id`
- `status=active`
- `source_type`
- `source_id`
- `participants`
- `audit_id`

#### `POST /chat/context-requests/{id}/reject`

拒绝上下文私聊申请。

请求字段：

- `reason`：拒绝原因。

响应字段：

- `id`
- `status=expired`
- `audit_id`

#### `GET /chat/conversations`

查询当前用户会话列表。

查询参数：

- `status`：可选，会话状态。
- `source_type`：可选，来源枚举。
- `page`、`page_size`：分页参数。

响应字段：

- `items[].id`
- `items[].status`
- `items[].source_type`
- `items[].source_id`
- `items[].source_summary`
- `items[].participants`
- `items[].friendship_state`
- `items[].expires_at`
- `items[].last_message`
- `total`

#### `GET /chat/conversations/{id}`

查询会话详情。

响应字段：

- `id`
- `status`
- `source_type`
- `source_id`
- `source_summary`
- `participants`
- `friendship_state`
- `rate_limit`
- `risk_state`
- `report_state`
- `messages`
- `audit_refs`

#### `POST /chat/conversations/{id}/messages`

发送会话消息。

请求字段：

- `content_type`：`text`、`image`、`voice`、`system_source_card`。
- `content`
- `client_message_id`：客户端幂等 ID。

响应字段：

- `message_id`
- `status`：`sent`、`risk_pending`、`blocked`。
- `risk_labels`
- `audit_id`

#### `POST /chat/conversations/{id}/report`

举报会话。

请求字段：

- `reason`
- `message_ids`
- `description`

响应字段：

- `report_id`
- `conversation_status=reported`
- `audit_id`

#### `POST /chat/conversations/{id}/block`

拉黑会话参与人。

请求字段：

- `target_user_id`
- `reason`

响应字段：

- `block_id`
- `conversation_status=blocked`
- `audit_id`

#### 上下文私聊错误码

- `CHAT_CONTEXT_REQUIRED`：缺少合法互动上下文。
- `CHAT_NOT_CONFIRMED`：未完成双向回应或确认。
- `CHAT_BLOCKED`：双方存在拉黑关系。
- `CHAT_RATE_LIMITED`：非好友或风险用户触发频控。
- `CHAT_SOURCE_NOT_FOUND`：来源不存在。
- `CHAT_SOURCE_EXPIRED`：上下文已过期。
- `CHAT_RISK_REVIEW_REQUIRED`：命中聊天风控。
- `CHAT_CONVERSATION_NOT_ACTIVE`：会话不是 active 状态。

## 认证、拉新和钱包

- `GET /verification`
- `POST /verification/face`
- `POST /referrals/claim-vip`
- `GET /wallet`
- `GET /creators`
- `POST /private-photos`
- `GET /private-photos`
- `GET /private-photos/{id}`
- `POST /private-photos/{id}/unlock`
- `POST /gifts/send`
- `POST /wallet/withdraw`

重要规则：

- 人脸认证包含活体检测、男女识别、人工复核。
- 充值金币不可提现。
- 照片查看和礼物带来的收益进入收益金币，并转换为魅力值。
- 提现按魅力值门槛和换算比例处理。
- 私密照片 AI 审核优先，按风险等级进入自动通过、人工复核、自动拒绝或冻结。
- 收益只允许来自审核通过且未冻结的私密照片。

### 私密照片智能审核

#### 审核状态

- `ai_pending`
- `ai_approved`
- `manual_required`
- `manual_approved`
- `rejected`
- `frozen`
- `appeal_pending`

#### 风险等级

- `low_risk`
- `medium_risk`
- `high_risk`

#### `POST /private-photos`

上传或注册私密照片。

请求字段：

- `file_id` 或 `upload_token`
- `visibility`：`private`
- `caption`
- `client_upload_id`：客户端幂等 ID。

响应字段：

- `id`
- `review_status`
- `risk_level`
- `model_labels`
- `confidence`
- `auto_action`
- `revenue_state`：`frozen`、`eligible`、`ineligible`。
- `audit_id`

#### `GET /private-photos`

查询当前用户私密照片列表。

查询参数：

- `review_status`
- `risk_level`
- `page`
- `page_size`

响应字段：

- `items[].id`
- `items[].review_status`
- `items[].risk_level`
- `items[].user_visible_message`
- `items[].revenue_state`
- `items[].created_at`
- `total`

#### `GET /private-photos/{id}`

查询单张私密照片详情。

响应字段：

- `id`
- `review_status`
- `risk_level`
- `model_labels`
- `confidence`
- `auto_action`
- `manual_review`
- `revenue_state`
- `appeal_state`
- `audit_refs`

#### `POST /private-photos/{id}/unlock`

解锁审核通过且未冻结的私密照片。

请求字段：

- `payment_currency`：`coin`
- `client_order_id`

响应字段：

- `unlock_id`
- `photo_id`
- `charged_amount`
- `creator_revenue_state`
- `audit_id`

错误码：

- `PHOTO_REVIEW_PENDING`
- `PHOTO_REJECTED`
- `PHOTO_FROZEN`
- `PHOTO_REVENUE_FROZEN`
- `PHOTO_ALREADY_UNLOCKED`

#### 后台私密照片审核接口

- `GET /admin/private-photos/reviews`
- `GET /admin/private-photos/reviews/{id}`
- `POST /admin/private-photos/reviews/{id}/review`
- `GET /admin/private-photos/risk-summary`

`GET /admin/private-photos/reviews` 查询参数：

- `review_status`
- `risk_level`
- `user_id`
- `date_from`
- `date_to`
- `report_count_min`
- `page`
- `page_size`

审核列表响应字段：

- `items[].id`
- `items[].photo_id`
- `items[].user_id`
- `items[].review_status`
- `items[].risk_level`
- `items[].model_labels`
- `items[].confidence`
- `items[].auto_action`
- `items[].report_count`
- `items[].revenue_state`
- `items[].assigned_admin_id`
- `items[].updated_at`
- `total`

`POST /admin/private-photos/reviews/{id}/review` 请求字段：

- `action`：`approve`、`reject`、`freeze`、`unfreeze`、`request_more_review`。
- `reason`
- `manual_labels`
- `revenue_action`：`keep_frozen`、`release`、`forfeit`。

响应字段：

- `review_id`
- `before_status`
- `after_status`
- `before_revenue_state`
- `after_revenue_state`
- `audit_id`

私密照片错误码：

- `PHOTO_REVIEW_NOT_FOUND`
- `PHOTO_STATE_CONFLICT`
- `PHOTO_MANUAL_REASON_REQUIRED`
- `PHOTO_REVENUE_NOT_ELIGIBLE`
- `PHOTO_RISK_ACTION_REQUIRED`

## 后台

- `GET /admin/reward-config`
- `PATCH /admin/reward-config`
- `GET /admin/users`
- `GET /admin/content`
- `POST /admin/moderation/{id}`
- `GET /admin/summary`

## 后台优先搭建说明

最新优先级：先搭建后台接口、后台管理等完整骨架，再继续展开前台细节优化。

后台接口首轮按以下分组补齐：

- 管理员鉴权：`POST /admin/auth/login`、`POST /admin/auth/logout`、`GET /admin/auth/me`。
- 后台概览：`GET /admin/summary`、`GET /admin/audit-queues/summary`。
- 用户管理：`GET /admin/users`、`GET /admin/users/{id}`、`PATCH /admin/users/{id}/status`。
- 内容审核：`GET /admin/content`、`GET /admin/content/{id}`、`POST /admin/moderation/{id}`。
- 举报处理：`GET /admin/reports`、`GET /admin/reports/{id}`、`POST /admin/reports/{id}/resolve`。
- 奖励配置：`GET /admin/reward-config`、`PATCH /admin/reward-config`。
- 认证复核：`GET /admin/verifications`、`GET /admin/verifications/{id}`、`POST /admin/verifications/{id}/review`。
- 钱包提现：`GET /admin/wallet/withdrawals`、`GET /admin/wallet/withdrawals/{id}`、`POST /admin/wallet/withdrawals/{id}/review`、`GET /admin/wallet/transactions`。
- 上下文私聊审核：`GET /admin/chat/context-requests`、`GET /admin/chat/conversations/{id}`、`POST /admin/chat/conversations/{id}/resolve-report`。
- 私密照片审核：`GET /admin/private-photos/reviews`、`GET /admin/private-photos/reviews/{id}`、`POST /admin/private-photos/reviews/{id}/review`、`GET /admin/private-photos/risk-summary`。

详细搭建顺序见 [接口与后台搭建计划](backend-interface-admin-plan.md)。每个后台模块完成后，需要同步更新 [处理历史](work-history.md) 和 [已完成清单](completed-checklist.md)。

### 后台举报证据链检索

- `GET /admin/reports`
  - 查询参数：
    - `status`：`queued`、`reviewing`、`resolved`、`all`。
    - `target_type`：`user`、`bottle`、`treehole`、`reply`、`chat`、`plaza`、`private_photo`、`all`。
    - `q`：按举报编号、举报人、目标 ID、原因、目标摘要、证据引用和审计引用做关键词检索。
  - 响应字段：
    - `id`
    - `reporter_id`
    - `target_type`
    - `target_id`
    - `reason`
    - `status`
    - `created_at`
    - `target_type_text`
    - `target_display_name`
    - `target_avatar_url`
    - `target_preview`
    - `evidence_refs`
    - `audit_refs`
  - 证据要求：
    - 聊天举报至少返回 `report:{id}`、`chat:{thread_id}`、`reporter:{user_id}`、`conversation:{thread_id}`、`thread_status:{status}`。
    - 私密照片举报应附带照片审核链路中已有 `audit_refs`。
    - 未处置举报允许 `audit_refs=[]`，后台需明确显示“待处置后生成”。

### 后台举报处置落库

- `POST /admin/reports/{id}/resolve`
  - 用途：管理员或审核员对单条举报做最小闭环处置，把举报状态写为 `resolved`，并生成审计记录。
  - 权限：`admin`、`moderator`。
  - 路径字段：
    - `id`：举报编号。
  - 请求字段：
    - `action`：固定为 `resolve`。
    - `reason`：必填，1-200 字，作为处置原因写入审计详情。
    - `penalty_action`：可选，`none`、`limit_user` 或 `freeze_chat`；默认 `none`。`limit_user` 当前只支持聊天举报，会限制被举报会话中非举报人的用户。`freeze_chat` 当前只支持聊天举报，会把对应聊天线程冻结。
  - 响应字段：
    - `report_id`
    - `before_status`
    - `after_status`
    - `reason`
    - `audit_id`
    - `resolved_at`
    - `penalty_action`
    - `penalty_target_user_id`
    - `penalty_target_thread_id`
    - `penalty_audit_id`
  - 状态要求：
    - `before_status` 返回处置前状态。
    - `after_status` 必须为 `resolved`。
    - 再次通过 `GET /admin/reports?q={report_id}` 查询时，该举报 `status=resolved` 且 `audit_refs` 包含本次 `audit_id`。
  - 审计要求：
    - 写入 `AdminAuditLog`。
    - `action=report_resolve`。
    - `target_type=report`。
    - `target_id={report_id}`。
    - 审计详情需包含前后状态和处理原因。
    - 当 `penalty_action=limit_user` 时，需额外写入 `report_penalty_limit_user` 审计，`target_type=user`，`target_id={penalty_target_user_id}`。
    - 当 `penalty_action=freeze_chat` 时，需额外写入 `report_penalty_freeze_chat` 审计，`target_type=chat`，`target_id={penalty_target_thread_id}`。
  - 冻结聊天要求：
    - 目标聊天线程状态写为 `risk_frozen`。
    - `GET /admin/reports?q={report_id}` 的证据引用需显示 `thread_status:risk_frozen`。
    - 冻结后继续调用 `POST /conversations/{thread_id}/turns` 必须失败，错误码为 `CHAT_RISK_FROZEN`。
    - 处置成功后必须为举报人生成系统通知，`business_type=chat_freeze`，`business_id={thread_id}`，通知正文包含处置原因和申诉说明。
    - `GET /messages` 需返回该通知，用户端系统消息分区点击后进入 `/pages/messages/chat?threadId={thread_id}`。
    - `GET /conversations` 和 `POST /conversations/{thread_id}/read` 需继续返回被冻结会话，字段 `status=risk_frozen`，`frozen_notice` 为用户端冻结原因和申诉说明。
    - 用户端聊天页读取 `frozen_notice` 后必须展示冻结提示，隐藏或禁用输入、图片、语音、视频、礼物和房间入口。
  - 错误码：
    - `REPORT_NOT_FOUND`：举报不存在。
    - `REPORT_TARGET_NOT_FOUND`：处罚联动目标不存在。
    - `REPORT_TARGET_USER_NOT_FOUND`：被处罚用户不存在。
    - `REPORT_PENALTY_UNSUPPORTED`：当前举报类型不支持所选处罚动作。
    - `ADMIN_UNAUTHORIZED`：缺少后台 bearer token。
    - `ADMIN_FORBIDDEN`：角色无处置权限。

- `GET /admin/audit`
  - 响应字段新增：
    - `detail`：后台审计详情原文，用于展示前后状态、处置原因、处罚动作和关联对象。
  - 后台要求：
    - 审计列表支持选中单条记录。
    - 审计详情面板必须展示审计编号、操作者、动作、目标、记录时间和 `detail`。

- `POST /admin/reports/{id}/restore`
  - 用途：恢复由举报处置冻结的聊天线程。
  - 权限：`admin` 或 `moderator`。
  - 请求字段：
    - `reason`：恢复原因，1-200 字。
  - 响应字段：
    - `report_id`
    - `thread_id`
    - `before_thread_status`
    - `after_thread_status`
    - `reason`
    - `audit_id`
    - `restored_at`
  - 状态要求：
    - 仅支持 `target_type=chat` 的举报。
    - 仅当目标聊天线程 `status=risk_frozen` 时可恢复。
    - 恢复后目标聊天线程 `status=active`。
    - 恢复后 `POST /conversations/{thread_id}/turns` 可正常发送。
  - 审计要求：
    - 写入 `AdminAuditLog(action=report_restore_chat,target_type=chat,target_id={thread_id})`。
    - 审计详情需包含举报 ID、恢复前状态、恢复后状态和恢复原因。
  - 通知要求：
    - 为举报人生成系统通知，`business_type=chat_restore`，`business_id={thread_id}`。
  - 错误码：
    - `REPORT_NOT_FOUND`：举报不存在。
    - `REPORT_TARGET_NOT_FOUND`：聊天线程不存在。
    - `REPORT_PENALTY_UNSUPPORTED`：非聊天举报不支持恢复聊天。
    - `REPORT_CHAT_NOT_FROZEN`：目标聊天未处于冻结状态。
## 2026-06-30 新增契约草案：消息、匹配、城市和头像

### 用户头像

- 所有用户卡片响应应优先返回 `avatar_url`。
- 如果用户未设置头像，后端应返回系统分配的 `fallback_avatar_url`，前端不得用文字头像兜底。
- 推荐字段：
  - `avatar_url: string | null`
  - `fallback_avatar_url: string`
  - `avatar_source: user_uploaded | system_pool`
  - `profile_updated_at: string`

### 城市筛选

- 所有列表型城市筛选统一参数：
  - `city_scope: nationwide | city | expanded`
  - `city: string | null`
  - `province: string | null`
- 默认快捷项：`全国 / 北京 / 上海 / 广州 / 深圳 / 全部`。
- 点击“全部”后前端可请求或使用后端返回的城市/省份列表：
  - `GET /geo/city-options`
  - 响应字段：`hot_cities[]`、`provinces[]`、`cities_by_province{}`

### 附近的人

- `GET /nearby/users` 后续需要支持：
  - `gender: all | female | male`
  - `min_age: number`
  - `max_age: number`
  - `city_scope: nationwide | city | expanded`
  - `city?: string`
  - `province?: string`
- 不再暴露距离筛选为主要用户入口。
- 响应字段补充：
  - `avatar_url`
  - `fallback_avatar_url`
  - `city`
  - `province`
  - `follower_count`
  - `registered_days`

- `POST /chat/match-expand-requests`
  - 用途：附近的人“开聊”入口，不走对方同意队列；校验 VIP 或积分后直接创建/复用私聊线程。
  - 请求字段：`target_user_id`。
  - 响应字段：`request`、`thread_id`、`conversation_id`、`cost_coins`、`current_user`。
  - 状态：成功后 `request.status=active`，`request.conversation_id=thread_id`。
  - 扣费：VIP 用户 `cost_coins=0`；非 VIP 首次开聊消耗 5 积分；复用已存在会话不重复扣费。
  - 会话读取：`POST /conversations/{thread_id}/read` 必须返回对方 `participant_name`、`participant_avatar_url` 和当前会话 `status=active`。
  - 失败：非 VIP 且积分不足返回 `MATCH_EXPAND_INSUFFICIENT_COINS`。

### 游戏随机匹配

- `GET /game/random-match/options`
  - 返回性别、年龄、城市、剩余次数和可用状态。
- `POST /game/random-match`
  - 请求字段：`gender`、`min_age`、`max_age`、`city_scope`、`city`、`province`。
  - 响应字段：`match_id`、`status`、`quota_remaining`、`target_user`、`room_id?`。
- 状态枚举：
  - `idle`
  - `matching`
  - `matched`
  - `no_result`
  - `quota_exhausted`
  - `risk_limited`

### 消息邀请卡片

- 消息页新增邀请卡片接口：
  - `GET /messages/invitations`
  - `POST /messages/invitations/{id}/accept`
  - `POST /messages/invitations/{id}/cancel`
- 邀请状态：
  - `pending`
  - `accepted`
  - `cancelled`
  - `expired`
  - `room_ready`
- `accepted` 或 `room_ready` 状态下再次点击邀请卡片，前端应直接跳转 `room_id` 或 `conversation_id`。

### 消息通知单条已读

- `GET /messages`
  - 用途：读取留言通知、系统通知和业务通知列表。
  - 响应字段：`id`、`title`、`body`、`created_at`、`unread`、`business_type`、`business_id`。
  - `business_type` 属于系统类时进入系统消息分区；其他留言、邀请、互动通知进入留言消息分区。
- `POST /messages/{message_id}/read`
  - 用途：只把当前用户名下指定留言或系统通知标记为已读。
  - 路径字段：`message_id`。
  - 权限：只能操作当前用户自己的消息通知。
  - 响应字段：同 `GET /messages` 单项，且目标项 `unread=false`。
  - 错误码：`MESSAGE_NOT_FOUND` 表示消息不存在或不属于当前用户。
- 邀请卡片未读分区：
  - `pending` 邀请在留言消息分区顶部展示为待处理邀请。
  - `accepted`、`cancelled`、`expired`、`room_ready` 邀请进入已处理邀请分区。
  - 系统消息分区不得混入邀请卡片。

### 冻结聊天申诉

- `POST /conversations/{thread_id}/appeal`
  - 用途：用户对 `risk_frozen` 普通私聊提交真实申诉工单。
  - 路径字段：`thread_id`。
  - 请求字段：`reason`，1-240 字。
  - 权限：只能申诉当前用户自己的冻结聊天。
  - 幂等：同一用户、同一线程已有 `pending` 申诉时返回原申诉，不重复生成。
  - 响应字段：`id`、`thread_id`、`user_id`、`user_name`、`participant_name`、`reason`、`status`、`admin_reason`、`audit_refs`、`created_at`、`updated_at`。
  - 成功副作用：写入 `chat_appeals`，写入 `AdminAuditLog(action=chat_appeal_submit,target_type=chat_appeal)`，生成 `business_type=chat_appeal` 系统通知。
  - 失败：非冻结聊天返回 `CHAT_APPEAL_THREAD_NOT_FROZEN`，非本人聊天返回 `THREAD_NOT_FOUND`。

- `GET /admin/chat-appeals`
  - 用途：后台查看聊天申诉工单。
  - 查询参数：`status=all|pending|approved|rejected`。
  - 权限：`admin`、`moderator` 可读。
  - 响应字段：同用户申诉响应，包含申诉用户昵称、聊天对方和审计引用。

- `POST /admin/chat-appeals/{appeal_id}/review`
  - 用途：后台通过或驳回聊天申诉。
  - 请求字段：`action=approve|reject`、`reason`。
  - 通过：申诉状态变为 `approved`，目标聊天线程恢复为 `active`，通知用户 `chat_appeal_approved`，写入 `chat_appeal_approve` 审计。
  - 驳回：申诉状态变为 `rejected`，目标聊天线程保持 `risk_frozen`，通知用户 `chat_appeal_rejected`，写入 `chat_appeal_reject` 审计。
  - 响应字段：`appeal_id`、`thread_id`、`before_status`、`after_status`、`thread_status`、`audit_id`、`reviewed_at`。
  - 失败：不存在返回 `CHAT_APPEAL_NOT_FOUND`，已处理返回 `CHAT_APPEAL_ALREADY_REVIEWED`。
## 2026-07-01 LOOP-44 举报目标边界纠偏

### 普通举报目标

`POST /reports` 面向用户端普通举报入口时，只允许以下目标：

- `target_type=user`：点击用户头像打开用户信息名片后，由名片左上角“举报”发起。
- `target_type=bottle`：在漂流瓶内容卡片内发起。
- `target_type=plaza`：在广场帖子卡片内发起。

以下对象不再作为用户端普通举报目标：`private_photo`、`chat`、`reply`、`treehole`。私密照片走 AI 审核、人工复核、申诉和收益冻结链路；聊天走上下文风控、拉黑、冻结和聊天申诉链路；评论不单独举报，需举报发布该评论的用户或承载该评论的帖子/瓶子。

### UI 约束

- 用户头像点击必须先弹出用户信息名片，举报入口固定在名片左上角。
- 帖子和漂流瓶可以在内容卡片内提供举报入口。
- 私密照片卡片、聊天工具区、评论项、树洞历史内容不得展示普通举报按钮。
- 后台 `GET /admin/reports` 可以继续兼容展示历史旧类型工单，但新用户端入口不得再创建这些旧类型。

### LOOP-44 验证证据

- `POST /reports` 冒烟：`user`、`plaza`、`bottle` 三类目标均返回 `queued`，详见 `reports/loop44/api-smoke.json`。
- UI 证据：广场帖子举报入口、头像名片左上角举报入口和用户举报弹窗截图位于 `reports/loop44/screenshots/`。
- 后续边界：后端旧类型 `chat`、`reply`、`private_photo`、`treehole` 的强拒绝与历史工单迁移不在 LOOP-44 范围，登记到 `O-048`。
