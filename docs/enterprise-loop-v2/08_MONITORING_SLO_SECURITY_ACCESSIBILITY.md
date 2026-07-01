# 监控、SLO、安全、可访问性标准 v2

日期：2026-06-29

## 1. 监控目标

企业级不是“本地能跑”，而是出问题能发现、能定位、能追责、能恢复。

必须覆盖：

```text
logs 日志
metrics 指标
traces 链路
errors 错误
business events 业务事件
audit logs 审计
```

## 2. request_id 标准

每个请求必须：

- 生成或接收 `X-Request-ID`。
- 响应返回 `request_id`。
- 错误响应包含 `request_id`。
- 后端日志包含 `request_id`。
- 审计日志包含 `request_id`。

错误响应建议：

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "当前角色无权执行该操作",
    "request_id": "req_...",
    "details": {}
  }
}
```

## 3. SLI/SLO 建议

| 服务 | SLI | SLO |
| --- | --- | --- |
| 用户端核心 API | 成功率 | 99.5% / 30 天 |
| 后台核心 API | 成功率 | 99.5% / 30 天 |
| 用户端核心读 API | P95 延迟 | ≤ 800ms |
| 后台列表 API | P95 延迟 | ≤ 1000ms |
| 后台写操作 | P95 延迟 | ≤ 1500ms |
| 审核队列 | 高风险内容待处理时长 | P95 ≤ 30 分钟 |
| 提现审核 | 提现待处理时长 | P95 ≤ 1 工作日 |
| 错误告警 | P0 错误发现时间 | ≤ 5 分钟 |

## 4. 指标清单

### 4.1 技术指标

```text
http_requests_total
http_request_duration_seconds
http_errors_total
admin_auth_failures_total
permission_denied_total
db_query_duration_seconds
redis_errors_total
job_failures_total
```

### 4.2 业务指标

```text
bottle_fish_success_total
bottle_throw_success_total
plaza_post_created_total
plaza_like_total
plaza_comment_total
treehole_post_total
verification_pending_total
verification_pass_rate
report_pending_total
moderation_queue_size
withdrawal_pending_total
withdrawal_rejected_total
```

### 4.3 风控指标

```text
sensitive_word_hit_total
blocked_user_action_total
hidden_comment_created_total
private_photo_rejected_total
risk_freeze_total
abnormal_withdrawal_total
```

## 5. 日志标准

禁止记录：

- 明文密码。
- 完整 token。
- 精确定位。
- 私密照片 URL 原始敏感信息。
- 完整支付账户明文。

建议结构：

```json
{
  "level": "INFO",
  "time": "2026-06-29T00:00:00Z",
  "request_id": "req_...",
  "trace_id": "trace_...",
  "module": "admin.moderation",
  "action": "approve_content",
  "operator_id": "admin_...",
  "object_id": "content_...",
  "result": "success",
  "duration_ms": 123
}
```

## 6. 安全基线

### 6.1 后台安全

- 登录失败频率限制。
- 强密码策略或最小密码复杂度。
- token 过期。
- 退出失效。
- CSRF/XSS 防护视部署形态处理。
- 管理后台只允许 HTTPS。
- 高危操作二次确认。
- 操作审计不可篡改。

### 6.2 权限安全

- 菜单权限不是安全边界。
- 每个接口必须校验权限。
- 批量操作逐项校验。
- 导出需要单独权限。
- 财务、风控、超级管理员权限分离。

### 6.3 隐私安全

- 附近的人不返回精确经纬度。
- 隐藏留言普通人不可见。
- 隐藏留言给主人匿名化作者。
- 私密照片只有 AI 自动通过或人工复核通过后可展示；审核中、拒绝、冻结内容不得展示或产生收益。
- 聊天审核只能给有权限管理员查看。

## 7. 可访问性标准

至少按 WCAG 2.2 AA 思路检查：

- 颜色对比度。
- 键盘可操作。
- 焦点可见。
- 表单错误有文本。
- 图标按钮有可理解文本或 aria-label。
- 触控目标不要过小。
- 弹窗打开后焦点进入弹窗，关闭后回到触发元素。

## 8. 性能标准

### 用户端

- 首屏：LCP ≤ 2.5s。
- 交互：INP ≤ 200ms。
- 稳定：CLS ≤ 0.1。
- 大媒体懒加载。
- 音频/视频失败有兜底。

### 后台

- 表格分页。
- 复杂筛选走后端。
- 大导出异步任务。
- 图表按时间范围请求。
- 详情抽屉按需加载。

## 9. 告警建议

| 告警 | 条件 | 处理人 |
| --- | --- | --- |
| 后台登录失败激增 | 5 分钟内失败超过阈值 | 安全/运维 |
| 审核积压 | 高风险队列 P95 超过 30 分钟 | 审核负责人 |
| 提现积压 | 待处理超过 1 工作日 | 财务负责人 |
| 5xx 错误 | 5 分钟错误率超过 1% | 后端负责人 |
| DB 慢查询 | P95 超过阈值 | 后端/DB |
| 隐私异常 | 普通用户看到隐藏留言/私密内容 | P0 立即阻断 |
