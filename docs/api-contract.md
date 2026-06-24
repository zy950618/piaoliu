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

陌生人不能直接私聊。好友申请通过后才可开放聊天。

## 认证、拉新和钱包

- `GET /verification`
- `POST /verification/face`
- `POST /referrals/claim-vip`
- `GET /wallet`
- `GET /creators`
- `GET /private-photos`
- `POST /private-photos/unlock`
- `POST /gifts/send`
- `POST /wallet/withdraw`

重要规则：

- 人脸认证包含活体检测、男女识别、人工复核。
- 充值金币不可提现。
- 照片查看和礼物带来的收益进入收益金币，并转换为魅力值。
- 提现按魅力值门槛和换算比例处理。
- 私密照片只允许审核通过的非露骨内容。

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

详细搭建顺序见 [接口与后台搭建计划](backend-interface-admin-plan.md)。每个后台模块完成后，需要同步更新 [处理历史](work-history.md) 和 [已完成清单](completed-checklist.md)。
