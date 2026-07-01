# 企业级后台与独立 Web Admin 路线图 v2

日期：2026-06-29

## 1. 当前基线

从现有文档看，后台已经完成过阶段性骨架：Mock 鉴权、角色依赖占位、统一错误响应、审计链路、数据库/Alembic 占位和后台详情/批量入口。但生产级账号、真实会话、真实数据库、真实审计落库、完整权限矩阵仍未完成。

## 2. P0：生产级身份与权限

### 2.1 数据模型

```text
admins
roles
permissions
admin_roles
role_permissions
admin_sessions
admin_login_events
audit_logs
```

### 2.2 接口

```text
POST /admin/auth/login
POST /admin/auth/logout
POST /admin/auth/refresh
GET  /admin/auth/me
GET  /admin/roles
GET  /admin/permissions
POST /admin/admins
PATCH /admin/admins/{id}/status
PATCH /admin/admins/{id}/roles
```

### 2.3 验收

- 密码哈希。
- 禁用账号不能登录。
- 失败登录不泄露账号存在。
- token 可刷新/可失效。
- session 可在 Redis 或 DB 中校验。
- 权限从后端返回，前端菜单按权限渲染。
- 接口权限独立校验。

## 3. P0：数据库生产化

### 3.1 技术要求

- PostgreSQL 为主业务库。
- Redis 用于会话、幂等、频率限制、短期令牌。
- SQLAlchemy async 管理 DB session。
- Alembic 管理迁移。
- `.env.example` 完整列出 DATABASE_URL、REDIS_URL、JWT_SECRET、SESSION_TTL 等。

### 3.2 迁移顺序

```text
0001 base users/admins
0002 roles permissions
0003 admin sessions login events
0004 audit logs
0005 moderation records
0006 wallet withdrawals finance risk
0007 verification reviews
0008 content report chat review
0009 operation configs
0010 indexes and constraints
```

### 3.3 索引建议

```text
audit_logs(operator_id, created_at)
audit_logs(module, object_id)
admin_sessions(admin_id, expires_at)
moderation_records(status, risk_level, created_at)
reports(status, created_at)
withdrawals(status, amount, created_at)
users(status, city, gender, created_at)
```

## 4. P1：Web Admin 信息架构

### 4.1 Dashboard

模块：

- 今日新增用户。
- DAU/WAU/MAU。
- 待审核内容。
- 待处理举报。
- 待复核认证。
- 待提现。
- 高风险用户。
- 接口错误率。
- 审核超时队列。

验收：

- 每个数字能跳转对应列表。
- 每个卡片有更新时间。
- 无权限角色不显示无关数据。

### 4.2 审核工作台

分类：

- 漂流瓶。
- 树洞。
- 广场。
- 聊天记录。
- 私密照片。
- 认证复核。

字段：

```text
id, category, source, author, city, gender, risk_level, status,
trigger_reason, matched_words, auto_action, created_at, assigned_to,
last_audit_result
```

操作：

- 通过。
- 拒绝。
- 下架。
- 标记风险。
- 转人工。
- 封禁用户。
- 拉黑/限制互动。

验收：

- 每次操作必须原因。
- 操作后写审计。
- 详情展示关联用户、关联内容、关联举报、历史操作。

### 4.3 财务提现工作台

字段：

```text
withdrawal_id, user_id, amount, charm_value, income_coin,
recharge_coin, risk_score, status, payment_account,
created_at, reviewed_by, reviewed_at
```

操作：

- 通过。
- 拒绝。
- 冻结。
- 补充材料。
- 导出。

强规则：

- 充值金币不可提现。
- 异常收益冻结。
- 财务和超级管理员才能处理。

## 5. P1：员工效率设计

### 5.1 列表页统一结构

```text
顶部 KPI
快速筛选
高级筛选抽屉
表格
批量操作栏
分页
详情抽屉
审计侧栏
```

### 5.2 详情页统一结构

```text
对象摘要
风险状态
原始内容/资料
关联记录
历史操作
可执行动作
审计记录
```

### 5.3 操作反馈

- 成功：明确结果和下一步。
- 失败：展示错误码、人类文案、request_id。
- 批量：展示成功数量、失败数量、失败明细。
- 慢操作：显示进度或进入异步任务列表。

## 6. P2：数据分析和运营配置

### 6.1 数据看板

- 用户增长。
- 留存。
- 发瓶/捞瓶转化。
- 广场发布/点赞/留言。
- 树洞发布/共鸣。
- 认证转化。
- 充值和收益。
- 举报率和审核通过率。

### 6.2 运营配置

- 今日次数。
- 广告冷却。
- 签到奖励。
- 拉新会员。
- 随机话术。
- 礼物配置。
- 会员配置。
- 风控阈值。

所有配置修改必须：

- 二次确认。
- 记录前后值。
- 写审计。
- 支持回滚或版本记录。

## 7. 不合格后台示例

以下情况不算企业级：

- 只有 Dashboard，没有真实权限。
- 只有按钮隐藏，没有接口权限。
- 只有 Mock token，没有会话持久化。
- 只有页面表格，没有批量、筛选、详情、审计。
- 只展示错误 toast，没有 request_id 和错误码。
- 审核操作不能追溯操作人和原因。
- 财务提现没有风控和冻结。
- 改配置没有前后值记录。
