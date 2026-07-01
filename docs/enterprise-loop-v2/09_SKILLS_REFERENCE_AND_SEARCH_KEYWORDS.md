# 推荐 Skills、模板、UI 库与搜索关键词 v2

日期：2026-06-29

## 1. 后台 UI 参考

### 1.1 Vue Vben Admin

用途：独立 `admin-web/` 的中后台结构参考。

可参考：

- 布局。
- 菜单。
- 权限。
- 主题。
- 页签。
- 表格和表单。

禁止：

- 不评估直接整体替换。
- 不破坏现有业务。

### 1.2 SoybeanAdmin

用途：Vue3 + Vite + TypeScript + Pinia + Naive UI/UnoCSS 视觉和工程参考。

可参考：

- 高颜值后台风格。
- 主题配置。
- 文件路由。
- 组件结构。

### 1.3 Ant Design Pro

用途：企业级中后台信息架构参考。

注意：项目是 Vue，不复制 React 代码，只参考中后台模式。

### 1.4 Naive UI

用途：如果 `admin-web` 需要组件库，可优先评估 Naive UI：Vue3、TypeScript、主题可定制、组件较完整。

### 1.5 Varlet UI / Vant 4

用途：移动端用户端参考。

- Vant 4：成熟移动端组件，但风格偏工具型，需要二次设计。
- Varlet UI：移动端 Material 风格，可参考组件体验。
- 不建议把移动组件库直接用于 Web Admin。

## 2. 建议本地 Skills

下面这些可以作为 Codex/Agents 的本地 `SKILL.md` 方向。

| Skill | 用途 |
| --- | --- |
| `enterprise-loop-orchestrator` | 控制 Read/Plan/Act/Verify/Record LOOP。 |
| `vue3-admin-ux-review` | 检查 admin-web 布局、表格、筛选、详情、批量。 |
| `mobile-social-ux-review` | 检查用户端真实人类体验、触控、文案、动效。 |
| `fastapi-rbac-production` | 生产级管理员、RBAC、session、错误码。 |
| `sqlalchemy-alembic-migration` | PostgreSQL/Redis/Alembic 迁移和仓储。 |
| `moderation-safety-audit` | 审核、举报、聊天记录、隐私、违规词。 |
| `wallet-finance-risk` | 钱包、收益、提现、财务风控。 |
| `playwright-visual-regression` | 页面截图、交互、H5 双触发验证。 |
| `observability-slo-otel` | request_id、logs、metrics、traces、SLO。 |
| `docs-handoff-ledger` | 需求台账、处理历史、完成清单同步。 |

## 3. GitHub 搜索关键词

```text
vue3 admin template vite typescript rbac
vue vben admin permission menu button auth
soybean admin naive ui vue3 vite typescript
naive ui admin dashboard vue3
vue3 vite admin template rbac permission
pinia permission routes admin vue3
fastapi rbac sqlalchemy alembic async redis jwt
fastapi admin auth session redis sqlalchemy alembic
open telemetry fastapi sqlalchemy redis traces metrics
playwright vue visual regression h5 mobile
vant4 mobile social app ui vue3
varlet ui mobile vue3 material
```

## 4. 选择 UI 库强约束

引入任何 UI 库前必须写评估：

```text
库名：
用途：
影响端：admin-web / H5 / 小程序 / App
包体影响：
样式污染风险：
TypeScript 兼容：
主题能力：
替换范围：
回滚方案：
为什么不是只参考设计：
```

## 5. UI 库建议

| 场景 | 推荐 |
| --- | --- |
| 独立 Web Admin | Naive UI / Ant Design Vue / Element Plus / Vben/Soybean 参考 |
| H5/小程序用户端 | Vant 4 / Varlet UI 参考，但谨慎整体引入 |
| 图标 | SVG/iconfont，本地化，不依赖不稳定外链 |
| 图表 | ECharts，后台趋势图和运营看板 |
| 表格 | 后台大表格可用组件库表格，用户端不要表格化 |

## 6. 生产验收相关工具

| 工具 | 用途 |
| --- | --- |
| Playwright | E2E、截图、真实点击验证 |
| Lighthouse | Core Web Vitals/Lighthouse 分数 |
| axe-core | 可访问性自动检查 |
| pytest | 后端契约/权限/幂等测试 |
| Vitest | 前端逻辑测试 |
| OpenTelemetry | traces/metrics/logs |
| Alembic | 数据库迁移 |
| Redis | session、rate limit、idempotency |

## 7. 不建议

- 不建议直接用整套模板覆盖现有项目。
- 不建议 admin-web 和用户端共用一套 UI 风格。
- 不建议为了好看删除审计/权限/风控字段。
- 不建议把移动端组件库用于后台复杂表格。
- 不建议长期依赖 Mock 数据完成验收。
