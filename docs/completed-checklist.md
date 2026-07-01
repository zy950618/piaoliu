# 已完成清单

## 文档类

- [x] 产品规则初版：见 [产品规则](product-rules.md)。
- [x] API Contract 初版：见 [API Contract](api-contract.md)。
- [x] 设计规范初版：见 [设计规范](design-system.md)。
- [x] 预览版本记录：见 [预览版本记录](preview-version-log.md)。
- [x] 多 Agent 协作入口：见 [多 Agent 协作入口](multi-agent-workbench.md)。
- [x] 需求台账：见 [需求台账](requirements-ledger.md)。
- [x] 处理历史：见 [处理历史](work-history.md)。
- [x] 接口与后台搭建计划：见 [接口与后台搭建计划](backend-interface-admin-plan.md)。
- [x] 后续细节优化入口：见 [后续细节优化入口](detail-optimization-inbox.md)。

## 产品规则已明确

- [x] 首版功能范围：漂流瓶、游戏、树洞、广场、附近的人、消息中心、会员中心、钱包、认证收益、用户中心和后台看板。
- [x] 底部主导航：瓶子、广场、游戏、树洞、我的。
- [x] 后台为独立管理员入口，不出现在普通用户“我的”页面。
- [x] 规则纠偏完成：禁止无上下文冷启动骚扰，允许明确互动上下文内的陌生人私聊；好友关系不是私聊唯一门槛。
- [x] 充值金币不可提现，收益金币转换为魅力值后按规则提现。
- [x] 规则纠偏完成：私密照片 AI 智能审核优先，低风险自动通过，中风险人工复核，高风险拒绝或冻结，收益只来自审核通过且未冻结内容。

## 漂流瓶阶段成果

- [x] `bottle-v5`：补齐捞/扔入口、角标计数、筛选弹窗和瓶子详情信息。
- [x] `bottle-v6`：修复 H5 预览导航栏和弹窗遮挡问题。
- [x] `bottle-v7`：优化筛选选中态、弹窗居中、瓶子造型和水波视觉。
- [x] `bottle-v8`：修复筛选关闭行为、保存摘要刷新和关系动作角标。

## 验证记录已存在

- [x] 漂流瓶相关版本记录了 `npm run typecheck`。
- [x] 漂流瓶相关版本记录了 `npm run build:h5`。
- [x] 漂流瓶相关版本记录了 `npm run test:frontend`。
- [x] 漂流瓶相关版本记录了后端测试命令。
- [x] `bottle-v8` 记录了 Chrome CDP 真实点击验证。

## 后台接口与后台管理骨架

- [x] 后台接口 P0/P1 骨架实现：用户、内容、举报/拉黑、奖励配置、钱包/提现、认证、订单、广场、附近、审计日志。
- [x] 后端接口契约测试扩展到 12 个，覆盖广告幂等、次数幂等、签到幂等、订单校验幂等、举报/拉黑幂等、树洞共鸣幂等和后台接口存在性。
- [x] 前端后台管理页接入完整 Mock Dashboard。
- [x] 后台管理页展示：概览指标、奖励配置、用户列表/详情摘要、内容审核、举报队列、广告奖励记录、订单记录、提现/钱包风控、审计日志。
- [x] 后台页冒烟截图：`runtime-admin-dashboard-v1.png`。
- [x] 本轮后台骨架验证通过：`npm run typecheck`、`npm run build:h5`、`npm run test:frontend`、`python -m compileall -q backend\app backend\tests`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 继续完成阶段文档同步历史

- [x] 多 Agent 工作台已登记本轮目标：真实鉴权骨架、角色权限、数据库/Alembic 占位、统一错误码、审计日志链路、后台详情/批量操作/高级筛选入口。
- [x] 需求台账已新增 `R-005 后台继续完成阶段补强`。
- [x] 后台接口计划已补继续完成阶段 P0/P1 拆解和验收口径。
- [x] 早期文档同步阶段记录了当时只改 `docs/**`，不声明代码能力已完成。
- [x] 后续优化入口已承接仍需生产化接入的后台补强条目。

## 后台继续完成阶段代码落地

- [x] 后端已增加管理员 Mock 鉴权闭环：登录、退出、当前管理员、未登录拦截和 Bearer token 校验。
- [x] 后端已增加角色权限依赖占位，后台配置保存和内容审核写操作需要管理员身份。
- [x] 后端已增加统一错误响应，未授权、权限不足、HTTP 异常和参数校验错误返回统一 `error.code` / `error.message` 结构。
- [x] 后端已增加审计日志链路，管理员登录、退出、配置变更和审核动作会写入 Mock 审计记录。
- [x] 后端已增加 SQLAlchemy async、Redis、Alembic 目录和初始迁移占位，当前环境未安装依赖时仍可使用 Mock 路径运行。
- [x] 后端契约测试扩展到 15 个，覆盖管理员鉴权、写接口拦截、审计追加和现有业务幂等能力。
- [x] 前端后台页已增加 Mock 管理员登录状态、退出/恢复登录、模块锚点和详情面板。
- [x] 前端后台页已增加奖励配置保存、内容批量通过、内容批量下架和前端审计反馈。
- [x] 后台页冒烟截图：`runtime-admin-dashboard-v2.png`、`runtime-admin-detail-v2.png`。
- [x] 本轮继续完成阶段验证通过：`npm run typecheck`、`npm run build:h5`、`npm run test:frontend`、`python -m compileall -q backend\app backend\tests`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 上下文私聊后端最小闭环

- [x] `/chat/context-requests` 已支持带 `source_type/source_id` 的上下文私聊申请。
- [x] `/chat/context-requests/{id}/accept` 已支持双向确认后创建 `active` 会话。
- [x] `/chat/conversations/{id}/messages` 已支持 active 会话发消息，拉黑后返回 `CHAT_BLOCKED`。
- [x] `/chat/conversations/{id}/report` 已支持举报后会话进入 `reported`，后台详情可见。
- [x] `/admin/chat/context-requests` 和 `/admin/chat/conversations/{id}` 已支持管理员查看最小队列和详情。
- [x] 本轮只声明后端最小闭环完成，不声明 admin-web 页面或用户端入口完成。

## 私密照片 AI 审核后端最小闭环

- [x] `/private-photos` 已支持上传或注册私密照片，并返回 AI 审核风险分级。
- [x] 低风险内容自动进入 `ai_approved`，`revenue_state=eligible`。
- [x] 中风险内容进入 `manual_required`，复核前 `revenue_state=frozen` 且不能解锁。
- [x] 高风险内容进入 `rejected` 或 `frozen`，不能展示、解锁或产生收益。
- [x] `/admin/private-photos/reviews/{id}/review` 已支持人工复核放行、拒绝、冻结、解冻和收益动作。
- [x] `/admin/private-photos/risk-summary` 已支持后台风险汇总。
- [x] 本轮只声明后端最小闭环完成，不声明 admin-web 页面或用户端上传状态 UI 完成。

## admin-web 审核工作台最小可视闭环

- [x] `admin-web/` 已新增“上下文私聊”审核页，展示来源类型、来源 ID、会话状态、频控和详情证据。
- [x] `admin-web/` 已新增“照片审核”页，展示 AI 风险分级、模型标签、置信度、自动动作、收益状态和复核详情。
- [x] `admin-web/` 后台审计页可展示审计日志明细列。
- [x] 本轮只声明 admin-web 最小可视闭环完成，不声明用户端入口完成。

## 管理后台 Web 化纠正

- [x] 后台已从 uni-app 用户端路由剥离，新增独立目录 `admin-web/`。
- [x] 新增 Web Admin 命令：`npm run dev:admin`、`npm run build:admin`。
- [x] `src/pages.json` 已删除 `pages/admin/index`，用户端小程序、iOS、Android、H5 不再包含后台入口。
- [x] 旧的 `src/pages/admin/index.vue` 和未使用的 `src/stores/admin.ts` 已删除。
- [x] 独立 Web Admin 已覆盖总览、奖励配置、用户、内容审核、举报、订单、钱包提现、审计模块。
- [x] Web Admin 截图：`runtime-admin-web-v2.png`。
- [x] 验证通过：`npm run typecheck`、`npm run build:admin`、`npm run build:h5`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 内容审核分类与聊天记录审核

- [x] Web Admin 内容审核增加分类切换：全部、漂流瓶、树洞、私密照片、广场、聊天记录。
- [x] Mock 数据增加聊天审核记录，包含会话双方、来源、关联内容、最近消息、风险等级、状态、原因和完整对话。
- [x] Web Admin 增加聊天记录审核表和聊天详情抽屉。
- [x] 增加直接访问入口：`/#content:chat`、`/#content:chat:chat_review_003`。
- [x] 截图：`runtime-admin-content-chat-v1.png`、`runtime-admin-chat-detail-v2.png`。
- [x] 验证通过：`npm run typecheck`、`npm run build:admin`、`npm run build:h5`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 审核策略、对应用户与违规词自动屏蔽

- [x] 内容审核项已增加对应用户、触发来源、处理策略、命中违规词和自动动作字段。
- [x] 聊天审核项已增加参与用户 ID、触发来源、处理策略、命中违规词和自动动作字段。
- [x] Web Admin 内容审核表已显示对应用户、触发来源和自动动作。
- [x] Web Admin 详情抽屉可查看对应用户详情。
- [x] 明确规则：正常内容自动通过；举报、命中违规词、风控异常、私密照片进入审核。
- [x] 发送侧 Mock 已接入违规词自动屏蔽，覆盖漂流瓶、树洞发布和瓶子回复。
- [x] 截图：`runtime-admin-content-bottle-policy-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run build:admin`、`npm run build:h5`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## H5 用户端整体设计基线

- [x] 全局 H5 视觉基线已统一：背景、卡片、按钮、标签、筛选条、次数卡。
- [x] 广场、树洞、游戏、我的主页面头部已统一为 `page-hero` 风格。
- [x] H5 桌面预览增加居中手机容器和背景。
- [x] 修复窄屏主要操作按钮截断：广场关注/送礼、树洞认证标签、我的签到/认证/领取。
- [x] 截图：`runtime-h5-plaza-design-v3.png`、`runtime-h5-treehole-design-v3.png`、`runtime-h5-profile-design-v4.png`。
- [x] 验证通过：`npm run typecheck`、`npm run build:h5`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## H5 宽屏比例修复

- [x] 桌面 H5 已取消手机壳固定窄屏比例。
- [x] 宽屏下用户端 `.page` 使用最大 1180px 内容宽度并居中，浏览器背景铺满。
- [x] 移动端窄屏适配保留。
- [x] 瓶子页保持全屏动画铺满视口。
- [x] 截图：`runtime-h5-bottle-wide-v1.png`、`runtime-h5-plaza-wide-v1.png`、`runtime-h5-profile-wide-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run build:h5`、`npm run test:frontend`。

## 瓶子页筛选入口优化

- [x] 筛选入口已从头部右侧移到瓶子左上侧、蓝白渐变交接附近。
- [x] 筛选入口已按反馈继续上移约 2-3cm。
- [x] 筛选入口已再次上移，并缩小尺寸、降低阴影和背景存在感。
- [x] 筛选入口已继续上移并贴左边缘，隐藏筛选摘要，仅保留轻量入口。
- [x] 头部恢复为纯标题区，不再和月亮、筛选按钮抢视觉焦点。
- [x] 筛选入口改为浅青白半透明胶囊和 CSS 调节图标。
- [x] 捞瓶详情弹窗空回应不会关闭，弹窗内会显示“请先写一句回应”。
- [x] 捞瓶详情弹窗的关注入口已移动到头像/昵称行右侧。
- [x] 捞瓶详情弹窗已移除“加好友”操作。
- [x] 捞瓶详情弹窗已移除顶部“捞到一只瓶子”、心情标签、关闭按钮和“送礼物”入口。
- [x] 捞瓶详情弹窗底部按钮已调整为左侧“扔回海里”、右侧“回应”。
- [x] 截图：`runtime-h5-bottle-filter-dock-v1.png`、`runtime-h5-bottle-filter-left-v1.png`、`runtime-h5-bottle-filter-up-v1.png`、`runtime-h5-bottle-filter-higher-main-v1.png`、`runtime-h5-bottle-filter-edge-v1.png`、`runtime-h5-bottle-filter-edge-compact-v1.png`、`runtime-h5-bottle-filter-reply-fix-v1.png`、`runtime-h5-bottle-follow-layout-v1.png`、`runtime-h5-bottle-caught-actions-v1.png`。
- [x] 验证通过：`npm run typecheck`。

## 漂流瓶 Mock 用户数据

- [x] 漂流瓶 Mock 数据已扩展到 8 条不同用户样本。
- [x] 用户细节已覆盖昵称、头像字、性别、年龄段、城市、VIP、认证状态、心情和内容。
- [x] 捞瓶随机逻辑已过滤当前登录用户自己的瓶子。
- [x] 捞瓶随机逻辑已避免连续返回同一只瓶子。
- [x] 后端 `BottleOut` 已增加作者头像字、VIP、性别、年龄、城市、认证、目标性别和目标城市字段。
- [x] 后端 `/bottles` 和 `/bottles/random` 已使用后端 Mock 数据源返回多用户瓶子数据。
- [x] 后端 `/relations/follow` 已写入关注状态，并可反映到瓶子数据的 `is_following`。
- [x] SQLAlchemy 模型已增加 `Bottle`、`BottleReply`、`Follow`。
- [x] Alembic 已增加 `0002_bottle_relation_models.py`，创建 `bottles`、`bottle_replies`、`follows` 表。
- [x] 截图：`runtime-h5-bottle-random-users-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、后端相关文件 `py_compile`。

## 捞瓶回应、扔回、举报和拉黑

- [x] 空回应会提示“请先写一句回应”，不会提交，也不会关闭捞瓶详情弹窗。
- [x] 有效回应提交后关闭捞瓶详情弹窗。
- [x] 扔回海里会关闭捞瓶详情弹窗。
- [x] 举报/拉黑入口已改为详情弹窗，不再只是 toast。
- [x] 举报弹窗已包含原因选择、相关瓶子预览、取消、拉黑并扔回、提交举报。
- [x] 提交举报会写入 Mock 后台举报队列，并关闭举报弹窗但保留捞瓶详情。
- [x] 拉黑并扔回会写入 Mock 黑名单，并关闭举报弹窗和捞瓶详情。
- [x] 截图：`runtime-h5-bottle-report-modal-v1.png`、`runtime-h5-bottle-empty-reply-error-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`。

## 捞瓶筛选条件

- [x] 页面捞瓶已传递当前城市、性别、年龄筛选条件。
- [x] 前端 Mock 已按城市、性别、年龄段过滤瓶子。
- [x] 后端 `/bottles/random` 已支持 `city`、`gender`、`age_range` 查询参数。
- [x] 无匹配时提示“没有符合筛选条件的瓶子”，不会返回不符合条件的瓶子。
- [x] 无匹配时不扣捞瓶次数。
- [x] 有匹配时先确认真实瓶子，再扣捞瓶次数。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 扔瓶弹窗文案和性别选项

- [x] 扔瓶弹窗已移除顶部“扔一个瓶子”提示。
- [x] 扔瓶弹窗标题已从“你想让陌生人读到什么？”改为“写下这一刻想留下的话”。
- [x] 扔瓶弹窗已移除“写下这一刻想留下的话”，输入框成为第一视觉。
- [x] “谁可以捞”选项已统一为“默认 / 男 / 女”，不再显示“男士 / 女士”。
- [x] 扔瓶地区选择已从城市列表改为“默认 / 同城 / 附近”的轻量范围选择。
- [x] 扔瓶输入框已上移并增加独立卡片样式，减少标题和选项挤压感。
- [x] 扔瓶提交按钮已从“投进海里”改为“扔出去”。
- [x] 扔瓶弹窗选择“男 / 女”和城市时不再触发弹窗关闭。
- [x] 扔瓶弹窗已取消点击遮罩关闭，只保留“取消”和“扔出去”作为明确动作。
- [x] 全局检查 H5 源码内已无“男士 / 女士 / 投进海里 / 扔一个瓶子 / 你想让陌生人读到什么”残留。
- [x] 验证通过：`npm run typecheck`。

## 扔瓶随机话术和空内容校验

- [x] 扔瓶输入框右下角已增加“随机”入口。
- [x] 随机话术从 Mock 数据池读取，后续可替换为真实数据库查询。
- [x] 话术方向按网上资料提炼为开放式问题、轻松兴趣话题、分享当下和温和情绪价值。
- [x] 点击“随机”会把话术填入输入框，并清除空内容错误。
- [x] 空内容点击“扔出去”会提示“先写一点内容，才能扔出去”，不会关闭弹窗，也不会扣次数。
- [x] 前端 Mock API 已在扣次数前拒绝空内容，避免绕过页面生成空瓶子。
- [x] 后端已增加 `GET /bottles/prompts/random` 接口草案。
- [x] 后端 `POST /bottles` 已在扣次数前拒绝空内容，返回 `EMPTY_BOTTLE_CONTENT`。
- [x] 截图：`runtime-h5-bottle-random-prompt-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 扔瓶范围和捞瓶筛选规则

- [x] 扔瓶不再使用 `targetCity`，改为 `targetScope: all / same_city / nearby`。
- [x] 当前 Mock 用户增加城市 `杭州`，新扔出的瓶子使用发布者所在城市作为 `authorCity`。
- [x] 扔瓶弹窗范围文案改为“默认 / 同城优先 / 附近优先”，不再让用户手选具体城市。
- [x] 捞瓶筛选“城市”改为“范围”，选项为“全国 / 同城 / 附近”。
- [x] 捞瓶同城筛选按当前用户城市匹配，不再按用户手选城市匹配。
- [x] 捞瓶附近筛选按 Mock 城市圈匹配，当前杭州附近包含杭州、上海、宁波、苏州。
- [x] 捞瓶时会同时检查瓶子的目标性别和投放范围，避免男用户捞到“只给女”的瓶子，或异地用户捞到“同城优先”的瓶子。
- [x] 后端 `BottleOut`、`POST /bottles`、`GET /bottles/random` 已同步 `target_scope` 规则。
- [x] SQLAlchemy 模型已将瓶子字段改为 `target_scope`，Alembic 已增加 `0003_bottle_target_scope.py`。
- [x] 截图：`runtime-h5-bottle-scope-filter-v1.png`、`runtime-h5-bottle-target-scope-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 广场发动态和底部导航强化

- [x] 广场页面已增加“发动态”发布卡片。
- [x] 广场动态空内容会提示“先写一点内容，才能发布”，不会发布空动态。
- [x] 前端 Mock 已增加 `publishPlazaPost`，新动态插入广场列表顶部。
- [x] 底部 5 个入口仍为“瓶子 / 广场 / 游戏 / 树洞 / 我的”。
- [x] H5 底部导航已上移，增加独立浮层背景、边框和阴影，与页面内容明显区分。
- [x] 当前页面 tab 已用绿色拱形门高亮，并补充文字小图标识别。
- [x] 普通页面底部留白已增加，避免浮起导航遮挡内容。
- [x] 截图：`runtime-h5-plaza-composer-tabbar-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`。

## 广场独立服务和加号发布

- [x] 广场页面已移除“漂流广场”标题和漂流语境文案。
- [x] 广场主页不再直接显示发动态输入框，主页以浏览和筛选为主。
- [x] 筛选已放到广场页面最上方。
- [x] 页面底部中心已增加 `+` 发布按钮。
- [x] 点击 `+` 会打开发布弹窗，支持文字、图文、声音三种类型选择。
- [x] 广场列表已显示图文/声音标识、浏览量、点赞和留言。
- [x] 附近的人入口改为定位授权语境，提示开启定位后展示同城和附近用户动态。
- [x] 前端 Mock `publishPlazaPost` 已支持 `mediaType`、`mediaCount`、`viewCount`。
- [x] 后端已新增独立 `plaza.py` 路由，承载 `/plaza/posts` 和 `/nearby/users`。
- [x] 后端 `POST /plaza/posts` 已支持发布图文/声音 Mock 动态。
- [x] 截图：`runtime-h5-plaza-plus-composer-v1.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 瓶子页主操作按钮缩小

- [x] 瓶子页底部“捞 / 扔”按钮已缩小。
- [x] 按钮左右边距增加，从页面两侧更内收。
- [x] 按钮高度从 `112rpx` 降为 `92rpx`。
- [x] 主字字号从 `42rpx` 降为 `34rpx`。
- [x] 次数角标从 `42rpx` 降为 `34rpx`。
- [x] 截图：`runtime-h5-bottle-actions-smaller-v1.png`。
- [x] 验证通过：`npm run typecheck`。

## 尚未完成

- [ ] 生产级管理员账号表、密码哈希、token/session 持久化、禁用账号和刷新凭证策略。
- [ ] 完整角色权限矩阵：超级管理员、审核管理员、运营管理员、财务管理员的菜单权限和接口权限。
- [ ] PostgreSQL、Redis、SQLAlchemy async 真实依赖安装、连接配置、迁移执行和种子管理员落地。
- [ ] 审计日志、配置变更、审核动作、批量操作写入真实数据库表，并支持检索和导出。
- [ ] 后台独立 Web Admin 项目或路由拆分、高级筛选、导出、趋势图和更多批量操作。
- [ ] 聊天审核真实接口、真实聊天记录查询权限、敏感词命中证据和审核处理动作落库。
- [ ] H5/小程序端首屏、动效、弹窗、提交防重、慢接口状态和审核反馈继续优化。
- [ ] 举报队列快速处理和私密照片“闪图”聊天入口。

## 广场后端假数据库接入和留言弹窗修复

- [x] 广场列表、发布、点赞、留言已从前端本地 Mock 切换到 FastAPI 接口读取和写入。
- [x] 后端已增加 `plaza_comments` 假数据库列表，并提供 `GET /plaza/posts/{post_id}/comments` 评论读取接口。
- [x] `POST /plaza/posts/{post_id}/comments` 会写入后端假数据库、更新 `comment_count` 和 `comment_preview`。
- [x] 广场留言弹窗不再点击遮罩误关闭，提交后保持打开并刷新留言列表。
- [x] 留言提交增加防重复状态，空内容仍保留前端校验提示。
- [x] 广场发布动态已通过 `POST /plaza/posts` 写入后端假数据库，刷新列表后可看到后端返回数据。
- [x] H5 运行时验证通过：留言弹窗打开后可加载数据库评论，提交留言后接口评论数增加并立即显示。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 广场筛选、留言和附近的人公里筛选

- [x] 广场顶部筛选已改为城市筛选，首版覆盖全国、北京、上海、广州、深圳、杭州、成都、厦门，后续可替换为真实全国城市表。
- [x] 广场性别筛选和年龄段筛选已在前端 Mock 列表中真实生效。
- [x] 广场后端 `GET /plaza/posts` 已支持 `city`、`gender`、`age_range` 查询参数，并兼容中文值和英文值。
- [x] 广场动态已增加留言弹窗、空留言校验、Mock 写入和后端 `POST /plaza/posts/{post_id}/comments` 接口。
- [x] 广场底部 `+` 保持为悬浮发布入口，未点击时不遮挡主页内容。
- [x] 附近的人页面已移除女性友好模式展示。
- [x] 附近的人页面只保留性别、年龄、公里数筛选，不再显示城市或范围筛选。
- [x] 附近的人 Mock 数据已补充 `distance_km` 和 `age_range`，用于模拟后续数据库定位结果。
- [x] 附近的人后端 `GET /nearby/users` 已支持 `gender`、`age_range`、`distance_km` 查询参数。
- [x] H5 运行态验证：广场页面显示城市/性别/年龄筛选、留言入口和悬浮加号；附近的人页面显示性别/年龄/距离筛选且不显示女性友好模式。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。
- [x] 后端 8100 已重启，接口冒烟通过：杭州/男/25-30 返回 1 条广场动态，女/25-30/3km 返回 1 个附近用户，留言接口会更新 `comment_count` 和 `comment_preview`。

## 广场榜单入口和媒体筛选

- [x] 广场静态入口已改为可点击：附近动态、礼物榜、新人推荐榜。
- [x] 已移除广场列表卡片上的“已认证”展示，保留性别标签。
- [x] 媒体筛选从静态“图文/声音”改为可点击“图文/声音/视频”，默认三项全部选中。
- [x] 解决 H5 下 `tap` 和 `click` 双触发导致媒体筛选点一次等于切换两次的问题。
- [x] 发布动态弹窗默认媒体类型改为图文，发布类型支持图文、声音、视频。
- [x] 前端和后端 Mock 广场数据已补充一条视频动态。
- [x] 后端 `PlazaPost` 和 `PlazaCreateRequest` 已支持 `media_type=video`。
- [x] H5 运行态验证：点掉“图文”后图文动态消失；继续点掉“声音”后只剩视频动态；页面不再出现“已认证”。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 广场入口精简和互动统计展示

- [x] 广场主界面已取消图文、声音、视频三个媒体筛选入口。
- [x] 广场主界面只保留附近动态、礼物榜、新人推荐榜三个入口。
- [x] 浏览、点赞、留言数量已从一串文字改为独立统计块展示。
- [x] 点赞按钮已接入前端 Mock 更新，点击后点赞数即时增加。
- [x] 修复 H5 下点赞按钮 `tap` 和 `click` 双触发导致一次点击加 2 的问题。
- [x] 后端已增加 `POST /plaza/posts/{post_id}/like` Mock 接口。
- [x] H5 运行态验证：顶部入口只有 3 个；统计标签为浏览、点赞、留言；一次点赞只增加 1。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 广场年龄区间滑动筛选

- [x] 广场年龄筛选已从固定 chips 改为区间滑动条。
- [x] 年龄标签和区间滑动条已放在同一行，并保留间距。
- [x] 年龄区间筛选按区间重叠匹配广场动态年龄段。
- [x] 其他复用 `ExploreFilters` 的页面仍保留原年龄 chips，不受本次广场调整影响。
- [x] H5 运行态验证：年龄行存在、标签为“年龄”、滑动条数量为 2，顶部三个入口仍为等宽三列。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`。

## 广场筛选横向细节优化

- [x] 广场年龄筛选已从双滑条改为单滑条。
- [x] 单滑条用于切换 `全部`、`18-24`、`25-30`、`31-36`、`37+` 区间。
- [x] 广场性别筛选已改为同一横线展示：`性别`、`全部`、`女`、`男`。
- [x] H5 运行态验证：年龄滑条数量为 1；性别行 display 为 flex 且居中对齐。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`。

## 广场年龄双端区间滑块

- [x] 广场年龄筛选不再显示“全部年龄”，默认显示 `18-80岁`。
- [x] 广场年龄最大值已调整为 80 岁。
- [x] 广场年龄筛选已改为一条轨道两个端点滑块：左侧控制起始年龄，右侧控制结束年龄。
- [x] 广场年龄筛选样式改为自定义轨道、选中区间和双滑块，不再使用原生单 slider。
- [x] H5 运行态验证：页面不包含“全部年龄”；年龄值显示 `18-80岁`；`.age-thumb` 数量为 2。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`。

## 广场筛选拖动和数据库结构补强

- [x] 修复 H5 广场年龄双端滑块拖动问题：拖动开始后监听 `window` 的 mouse/touch move 和 end，避免滑块移出轨道后失效。
- [x] 广场列表请求已携带城市、性别、年龄区间参数，由后端执行筛选。
- [x] 后端年龄筛选已从字符串相等改为区间重叠匹配，例如 `24-31` 可匹配 `25-30`。
- [x] 广场帖子数据已增加 `media` 资源列表，媒体记录包含 `post_id`、`owner_id`、`media_type`、`url`、`storage_key`、`mime_type`、大小、时长和宽高。
- [x] 发布广场动态时可写入媒体资源元数据，并与当前用户和帖子关联。
- [x] SQLAlchemy 模型已补齐 `plaza_posts`、`plaza_media`、`plaza_comments`、`plaza_likes`。
- [x] Alembic 已新增 `0004_plaza_posts_media_comments.py`，用于真实 PostgreSQL 阶段建表。
- [x] 后端 8100 已重启，接口冒烟通过：广场返回媒体资源；`杭州 + 男 + 24-31` 返回 `plaza_002`；发布视频动态返回用户关联媒体。
- [x] H5 5173 已重启，`http://localhost:5173/#/pages/plaza/index` 返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 广场年龄滑块双向拖动修复

- [x] 广场年龄滑块左右端点已拆成明确的 `min` / `max` 句柄。
- [x] 左侧滑块只控制起始年龄，右侧滑块只控制结束年龄，避免右侧向左拖动时被误判为左侧滑块。
- [x] 轨道空白区域点击仍保留“选择最近端点”的快速调整能力。
- [x] H5 5173 已重启，`http://localhost:5173/#/pages/plaza/index` 返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。

## 广场真实媒体展示

- [x] 广场种子数据已从 `/uploads/...` 占位媒体换成真实在线图片、语音和视频 URL。
- [x] 图片动态会实际渲染图片墙，不再只显示“图文”标签。
- [x] 视频动态会实际渲染视频播放器，使用远程 MP4。
- [x] 语音动态会显示语音卡片，并通过播放按钮实际播放远程 MP3。
- [x] 后端契约测试已断言广场媒体 URL 为 `https://`，并覆盖 image、voice、video 三类媒体。
- [x] 后端 8100 和 H5 5173 已重启；`GET /plaza/posts` 返回真实在线媒体 URL，`http://localhost:5173/#/pages/plaza/index` 返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 广场点赞和隐藏留言

- [x] 广场点赞改为乐观更新：点击后当前卡片点赞数先 +1，再用后端返回值校准，失败时回滚并提示。
- [x] 留言发送成功后会关闭留言弹窗，不再停留在弹窗内。
- [x] 留言弹窗新增“隐藏，仅主人查看”勾选项。
- [x] 后端 `PlazaCommentRequest` 和 `PlazaCommentOut` 已增加 `hidden_for_owner_only` / `visible_to_owner_only` 字段。
- [x] 后端留言列表按可见性过滤：公开留言可见；隐藏留言只有留言本人和帖子发布者可见。
- [x] 广场卡片新增“查看留言”入口，跳转独立留言页 `pages/plaza/comments`。
- [x] 独立留言页显示当前用户可见留言，并对隐藏留言显示“仅主人可见”标识。
- [x] Alembic 已新增 `0005_plaza_comment_visibility.py`，用于真实数据库阶段给 `plaza_comments` 增加隐藏字段。
- [x] 后端 8100 和 H5 5173 已重启；接口冒烟确认点赞数 +1，隐藏留言可见性符合规则，H5 页面返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。

## 游戏页飞船视觉替换

- [x] 游戏页旧的 CSS 拼接飞船已替换成本地 SVG 飞船资产。
- [x] 新增 `src/static/ships/aurora-cruiser.svg`，用于游戏页远近三艘飞船。
- [x] 保留原有漂移动画和远近层次，同时替换为更完整的飞船造型、渐变机身、舷窗、机翼和尾焰。
- [x] H5 5173 已重启，`http://localhost:5173/#/pages/game/index` 返回 200。
- [x] 新飞船资源 `http://localhost:5173/static/ships/aurora-cruiser.svg` 返回 `200 image/svg+xml`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。

## 广场语音播放按钮图标化

- [x] 广场语音卡片已去掉“播放”文字。
- [x] 未播放状态显示侧向三角形图标。
- [x] 播放中状态显示正方形停止图标。
- [x] 点击播放中的语音按钮会停止播放并恢复三角形。
- [x] 语音播放结束或失败时会自动恢复三角形。
- [x] H5 5173 已重启，验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。

## 广场留言弹窗简化和隐藏勾选修复

- [x] 修复 H5 下“隐藏，仅主人查看”点一下无法勾选的问题：增加点击去重，避免 `tap/click` 双触发抵消状态。
- [x] 广场留言弹窗已移除顶部“留言”标题。
- [x] 广场留言弹窗已移除上方历史留言列表，不再显示作者、昵称或“谁来信”等信息。
- [x] 留言输入框已改为弹窗内顶格显示。
- [x] H5 5173 已重启，`http://localhost:5173/#/pages/plaza/index` 返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 广场点赞、留言关闭和隐藏留言复验修复

- [x] 先做接口冒烟验证：点赞接口会让 `like_count` 从 329 增加到 330，隐藏留言发布后 `comment_count` 从 44 增加到 45。
- [x] 隐藏留言可见性已复验：当前留言人和帖子作者可见，其他用户不可见，隐藏留言不进入公开 `comment_preview`。
- [x] 广场页点赞、留言、查看留言、发布、隐藏勾选等关键链路已清理同元素 `@tap + @click` 双绑定，降低 H5 双触发导致的无反应、重复触发或状态抵消。
- [x] 留言发布成功后不再等待重新拉取评论列表；先按后端返回更新帖子评论数并关闭留言弹窗，独立留言页再按需加载评论列表。
- [x] H5 浏览器运行验证：点赞数从 330 增加到 331；隐藏留言勾选可选中；发布留言后弹窗关闭，留言数增加到 46。
- [x] H5 浏览器运行验证：点击“查看留言”跳转到 `#/pages/plaza/comments?postId=plaza_001`，独立留言页展示可见留言和“仅主人可见”标识。
- [x] H5 5173 已重启，`http://localhost:5173/#/pages/plaza/index` 和 `http://localhost:5173/#/pages/plaza/comments?postId=plaza_001` 均返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。
## 2026-06-24 广场语音播放和波形动画修复

- [x] 复验问题：点击广场语音按钮后 `.voice-player` 未进入 `playing` 状态，页面看起来没有任何播放反馈。
- [x] 根因处理：语音按钮已移除同元素 `@tap + @click` 双绑定，避免 H5 一次点击触发两次导致播放后立刻停止。
- [x] 播放实现已从 H5 原生 `new Audio()` 改为 uni-app `uni.createInnerAudioContext()`，便于后续小程序和 App 端复用。
- [x] 播放失败时增加提示：`语音播放失败，请稍后再试`，不再静默无效。
- [x] 语音卡片新增播放中波形动画，播放时显示 5 条动态波形，停止后隐藏。
- [x] H5 浏览器运行验证：点击语音后 `.voice-player playing`、`.voice-wave active`，停止方块显示，波形条高度持续变化。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 广场数据持久化和浏览量修复

- [x] 已确认旧问题根因：广场路由直接操作 `app.routes.wallet` 中的 `plaza_posts`、`plaza_comments`、`plaza_media` Python 列表，没有使用 SQLAlchemy/PostgreSQL，也没有任何浏览量写入逻辑。
- [x] 已新增本地持久化仓储 `backend/app/plaza_store.py`，使用 SQLite 文件保存广场帖子、媒体、留言、点赞记录和浏览记录。
- [x] 广场 `GET /plaza/posts` 已从持久化仓储读取，并会为本次返回的帖子写入 `plaza_view_events` 且增加 `view_count`。
- [x] 广场 `POST /plaza/posts/{post_id}/like` 已写入 `plaza_likes`，并同步增加帖子 `like_count`。
- [x] 广场 `POST /plaza/posts/{post_id}/comments` 已写入 `plaza_comments`，并同步增加帖子 `comment_count`；隐藏留言仍不进入公开预览。
- [x] 后端测试已隔离使用 `backend/runtime/test_plaza.sqlite3`，避免污染 H5 正在看的运行数据。
- [x] 新增后端测试直接查询 SQLite 表，验证浏览、点赞、留言不是只改内存变量。
- [x] 运行时冒烟通过：浏览量从 1681 到 1682；点赞记录、留言记录、浏览记录均可从 SQLite 表查到；API 重启后留言和计数仍存在。
- [x] H5 运行验证：广场页面重新读取后显示持久化后的浏览、点赞、留言数量。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 广场点赞切换和大拇指动效

- [x] 广场帖子响应新增 `liked_by_current_user`，前端映射为 `likedByMe`。
- [x] 点赞接口从单纯累加改为当前用户点赞切换：未点赞时写入 `plaza_likes` 并 `like_count +1`；已点赞时删除当前用户点赞记录并 `like_count -1`。
- [x] 前端点赞按钮新增大拇指图标，未点赞显示“点赞”，已点赞显示“已赞”。
- [x] 点赞按钮新增状态样式：已赞为绿色高亮，未赞为浅色按钮。
- [x] 点赞/取消点赞新增浮层动效：点赞显示 `+1`，取消点赞显示 `-1`，大拇指有弹跳动画。
- [x] 后端测试新增点赞切换契约：第一次点赞 `liked_by_current_user=true` 且计数 +1；第二次取消 `liked_by_current_user=false` 且计数恢复，库中当前用户点赞记录清空。
- [x] H5 浏览器验证通过：未点赞按钮第一次点击从 146 到 147 并显示 `+1`，第二次点击从 147 到 146 并显示 `-1`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 广场留言入口纠偏和计数详情页

- [x] 纠正入口理解：广场卡片右侧操作区的“留言”已恢复为留言板弹窗。
- [x] 广场统计区“浏览 / 点赞 / 留言”里的留言计数项已改为详情页入口。
- [x] 页面不再显示单独的“查看留言”按钮。
- [x] 留言详情页顶部展示动态本体，下面展示当前用户可见留言，底部保留留言输入和“隐藏，仅主人查看”。
- [x] 后端新增 `GET /plaza/posts/{post_id}`，详情页刷新时可直接读取动态。
- [x] 评论种子数据补充了不同用户、不同头像、公开留言和隐藏留言。
- [x] H5 浏览器验证：右侧“留言”打开弹窗；统计区留言计数跳转到 `#/pages/plaza/comments?postId=...`；详情页无“查看留言”。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 留言详情页用户资料同步和圆润化

- [x] 评论响应新增留言作者资料：`author_gender`、`author_age_range`、`author_verified`、`author_city`。
- [x] 本地 SQLite `plaza_comments` 自动补齐作者性别、年龄、认证、城市字段，旧运行数据会回填默认资料。
- [x] 新发留言会使用当前用户资料写入头像、昵称、性别、年龄、城市、认证状态。
- [x] 留言详情页顶部动态作者显示性别和年龄标签，和广场卡片数据保持一致。
- [x] 留言列表每条留言显示头像、昵称、认证、性别、年龄、城市。
- [x] 留言详情页视觉圆润化：动态卡片、留言卡片、头像、媒体、输入框和播放器圆角统一放大，减少棱角和硬边框。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
- [x] 运行接口验证：`GET /plaza/posts/plaza_001/comments` 已返回留言作者性别、年龄和城市字段；H5 5173 返回 200。
## 2026-06-24 仅主人可见留言隐私修复

- [x] 修复隐藏留言只是打标签的问题：`hidden_for_owner_only=true` 的留言现在不会返回给普通浏览者。
- [x] “仅主人可见”改为严格只给动态发布者可见，不再默认给留言本人二次查看。
- [x] 动态发布者看到隐藏留言时，留言作者身份会脱敏为“匿名留言 / 匿”。
- [x] 隐藏留言返回给主人时不再暴露留言人的昵称、头像、性别、年龄、城市和认证状态。
- [x] 前端详情页隐藏留言不再显示性别年龄城市标签，只显示匿名身份和“仅主人可见”。
- [x] 后端测试已覆盖：普通用户看不到隐藏留言；动态主人看到匿名化隐藏留言。
- [x] 运行接口验证：`viewer_id=user_mock_001` 隐藏留言数量为 0；`viewer_id=creator_001` 可见隐藏留言但作者为匿名。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 留言详情页输入区和动态卡视觉优化

- [x] 底部留言输入区已从大块面板改为更轻的悬浮圆角胶囊区域。
- [x] 留言输入框高度固定压缩，不再占据过大屏幕空间。
- [x] 发送按钮已从“发送”文字改为横向饱满箭头图形按钮。
- [x] 顶部动态卡增加柔和分割线，作者、正文、媒体、统计之间更有线条层次。
- [x] 顶部动态统计改为三列铺开展示：浏览、点赞、留言。
- [x] 动态卡、语音卡、留言卡继续加大圆角，降低棱角感。
- [x] H5 5173 已重启，`#/pages/plaza/comments?postId=plaza_001` 返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。
## 2026-06-24 留言发送图标替换和同排布局

- [x] 已将用户提供的 `icons8-发送-48.png` 放入 `src/static/icons/send-paper-plane.png`。
- [x] 留言详情页底部输入区改为输入框和发送图标同一行。
- [x] 发送按钮使用图片图标，不再使用文字或 CSS 箭头。
- [x] 输入条右侧增加轻分隔和圆角图标按钮，形成更明确的设计层次。
- [x] 隐藏留言勾选项保留下移到第二行，避免和发送图标挤在一起。
- [x] H5 5173 已重启，页面和图标资源均返回 200。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`。

## 2026-06-29 LOOP-5 用户端体验最小闭环

- [x] 规则纠偏完成：用户端底部 tab 已保持 `瓶子 / 广场 / 游戏 / 树洞 / 我的`。
- [x] 入口可视完成：瓶子回应弹窗已展示基于本次瓶子互动继续聊的说明。
- [x] 入口可视完成：广场留言详情已展示“继续聊”入口和需发帖人回复/确认的说明。
- [x] 状态反馈完成：钱包页已展示私密照片 AI 自动通过、人工复核、冻结/拒绝和收益状态。
- [x] 兼容映射完成：`PrivatePhoto` 类型和接口映射支持新审核字段，同时兼容旧响应。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 截图证据：`output/playwright/user-bottle-continue-chat.png`、`output/playwright/user-plaza-comment-continue-chat.png`、`output/playwright/user-wallet-private-photo-review.png`、`output/playwright/user-treehole-tab.png`。
- [ ] 未标记功能完成：点击“继续聊”真实发起接口、私密照片真实上传和申诉入口仍需后续 LOOP。

## 2026-06-29 LOOP-6 生产级回归验收

- [x] 旧规则残留回归：业务代码中旧私聊门槛和旧人工审核规则搜索无残留。
- [x] 旧规则残留修复：`src/pages/nearby/index.vue` 好友申请 toast 已从旧规则已废弃文案“同意后才能聊天”纠偏为“明确互动后也可基于上下文继续聊”。
- [x] 后台隔离回归：`src/pages.json` 搜索 `admin|后台` 无命中。
- [x] 底部 tab 回归：`瓶子 / 广场 / 游戏 / 树洞 / 我的`。
- [x] 接口回归：上下文私聊无来源失败、确认 active、举报 reported、拉黑 blocked、拉黑后发消息 `CHAT_BLOCKED`。
- [x] 接口回归：私密照片低风险自动通过、中风险人工复核、高风险冻结且收益不可结算。
- [x] 截图回归：admin 和用户端 7 张截图均存在且非空。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [ ] 未标记生产完成：真实数据库持久化、真实用户端继续聊接口动作、私密照片真实上传/申诉仍需后续 LOOP。

## 2026-06-29 总结点二次验证

- [x] 二次静态门禁通过：业务代码无旧规则残留；历史记录中的旧句已标注为旧规则已废弃文案。
- [x] 二次后台隔离通过：`src/pages.json` 搜索 `admin|后台` 无命中。
- [x] 二次底部 tab 通过：`瓶子 / 广场 / 游戏 / 树洞 / 我的`。
- [x] 二次命令验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 二次接口冒烟通过：上下文私聊无来源失败、确认 active、举报 reported、拉黑 blocked、拉黑后 `CHAT_BLOCKED`；私密照片低/中/高风险状态均返回预期。
- [x] 二次截图通过：7 张 admin/user 截图已重新生成且目检关键页通过。
- [x] LOOP-7 门禁：允许进入，但本总结点未开始 LOOP-7。

## 2026-06-29 LOOP-7 用户端继续聊真实接口接入

- [x] 前端接口封装完成：`businessApi.createContextChatRequest()` 调用 `/chat/context-requests`。
- [x] Store 接入完成：`content.createContextChatRequest()` 暴露给瓶子和广场页面。
- [x] 瓶子入口完成：回应成功后发起 `bottle_reply` 继续聊申请，并显示状态反馈。
- [x] 广场入口完成：留言“继续聊”发起 `plaza_comment` 继续聊申请，并显示状态反馈。
- [x] 单元测试完成：新增 `businessApi` 请求字段和响应映射测试。
- [x] 接口冒烟完成：无来源失败、瓶子来源 pending、广场来源 pending、accept 后 active。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 浏览器端全链路补验通过：通过 SQLite E2E 当前后端，瓶子回应和广场继续聊点击后均展示 pending 状态。

## 2026-06-29 LOOP-8 当前后端 E2E 环境闭环

- [x] 新增 `scripts/start-e2e-backend.ps1`，使用 SQLite 启动当前 FastAPI E2E 后端。
- [x] 新增 `scripts/build-h5-e2e.ps1` 和 `npm run build:h5:e2e`，H5 构建明确指向 8110 当前后端。
- [x] 接口验证通过：`/me/status`、`/plaza/posts/plaza_001`、`/plaza/posts/plaza_001/comments`、`/bottles/random`、`/chat/context-requests`。
- [x] 浏览器截图通过：`user-bottle-context-request-pending.png`、`user-plaza-context-request-pending.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
## 2026-06-29 LOOP-9 会话跳转最小闭环与捞瓶文案纠偏

- [x] 捞到瓶子弹窗已移除“原漂流瓶”标签，默认直接展示瓶子正文。
- [x] 前端已新增 `acceptContextChatRequest`、`getContextConversation`、`sendContextConversationMessage` 接口封装。
- [x] Store 已新增当前临时会话读取和发送消息方法。
- [x] 消息页已支持 `contextConversationId`，可展示临时会话来源、active 状态、消息列表和输入区。
- [x] 瓶子/广场入口在接口返回 `active + conversationId` 时会跳转到临时会话详情。
- [x] 单元测试已覆盖 accept 请求字段映射和临时会话详情响应映射。
- [x] 接口冒烟通过：`pending -> active -> GET conversation active -> send sent`。
- [x] 截图通过：`output/playwright/user-context-conversation-detail.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。
- [ ] 未标记生产完成：临时会话仍需真实数据库持久化，树洞/游戏/扩列入口仍待后续 LOOP。

## 2026-06-29 LOOP-10 树洞评论继续聊入口最小闭环

- [x] 树洞回复成功后已发起 `source_type=treehole_comment` 的上下文继续聊申请。
- [x] 树洞继续聊申请包含 `source_id`、`reply_id`、`initiator_action`、`evidence_id`。
- [x] pending 状态已在树洞弹层展示“继续聊申请已发出，等待对方确认”。
- [x] active + conversationId 分支已复用临时会话详情跳转。
- [x] 单元测试已覆盖 treehole context request 字段映射。
- [x] 接口冒烟通过：`treehole reply -> context pending -> accept active -> conversation treehole_comment -> send sent`。
- [x] 截图通过：`output/playwright/user-treehole-context-request-pending.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [ ] 未标记生产完成：游戏/扩列入口和上下文会话数据库持久化仍待后续 LOOP。

## 2026-06-29 LOOP-11 游戏房间上下文确认入口最小闭环

- [x] 消息页已有会话内创建游戏房间后，已发起 `source_type=game_room` 的上下文继续聊申请。
- [x] 游戏房间继续聊申请包含 `source_id=room_id`、`reply_id=thread_id`、`initiator_action=room_confirm`、`evidence_id=game_room:{room_id}`。
- [x] pending 状态已在房间面板展示“房间已创建，继续聊申请等待对方确认”。
- [x] active + conversationId 分支已复用临时会话详情跳转。
- [x] 单元测试已覆盖 game room context request 字段映射。
- [x] 接口冒烟通过：`create room -> context pending -> accept active -> conversation game_room -> send sent`。
- [x] 截图通过：`output/playwright/user-game-room-context-request-pending.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [ ] 未标记生产完成：扩列/附近的人匹配入口和上下文会话数据库持久化仍待后续 LOOP。

## 2026-06-29 LOOP-12 附近的人好友规则残留纠偏

- [x] 后端好友申请通知已移除“对方通过后才会打开私信”的旧规则文案。
- [x] 前端 mock 好友申请通知已同步新规则文案。
- [x] 附近的人页申请好友后显示“好友用于长期关系沉淀，明确互动上下文内仍可继续聊”。
- [x] 差异判定完成：附近的人当前没有双方匹配/确认动作，因此未接入 `match_expand`，也未新增私聊入口。
- [x] 后端测试已覆盖好友申请通知不再包含旧门槛。
- [x] 接口冒烟通过：`friend-request -> messages notification`，`old_rule_present=false`。
- [x] 截图通过：`output/playwright/user-nearby-friend-context-rule.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [ ] 未标记生产完成：`match_expand` 仍需产品级匹配/确认动作后才能接入；上下文会话数据库持久化仍待后续 LOOP。

## 2026-06-30 LOOP-13 附近的人 VIP/5积分继续聊门槛

- [x] 附近的人卡片已新增“继续聊”申请入口。
- [x] VIP 用户发起附近继续聊申请免费，接口返回 `gate=vip`、`cost_coins=0`，积分不减少。
- [x] 非 VIP 用户发起附近继续聊申请会消耗 5 积分，接口返回 `gate=drift_coins`、`cost_coins=5`。
- [x] 继续聊申请只创建 `source_type=match_expand` 的 pending 上下文申请，仍需对方确认后才开启临时会话。
- [x] 附近页已展示 VIP/5积分门槛说明和 pending 状态反馈。
- [x] 单元测试已覆盖 `POST /chat/match-expand-requests` 的前端映射。
- [x] 后端测试已覆盖 VIP 免费和非 VIP 扣 5 积分两条主路径。
- [x] 接口冒烟通过：VIP 免费、非 VIP 扣 5 积分、两者均返回 `pending + match_expand`。
- [x] 截图通过：`output/playwright/user-nearby-match-expand-pending.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [ ] 未标记生产完成：上下文会话数据库持久化仍待后续 LOOP。

## 2026-06-30 LOOP-14 附近的人与消息界面压缩优化

- [x] 附近的人页面已按参考图改为深色“同城”列表。
- [x] 附近的人顶部已增加筛选图标、搜索栏和搜索按钮。
- [x] 筛选功能保留性别、年龄、距离，并改为点击筛选图标展开。
- [x] 附近的人卡片已压缩为头像、昵称、年龄/城市/在线标签、关注数、注册天数、开聊按钮。
- [x] 消息页已改为“留言消息 / 精准查找 / 系统消息”三入口。
- [x] 消息页已展示真实私聊列表，点击仍进入聊天详情。
- [x] 聊天详情页已改为深色压缩布局，普通会话来源标签改为“互动来源”。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`。
- [x] 截图通过：`output/playwright/user-nearby-redesign-filters.png`、`output/playwright/user-messages-redesign-list.png`、`output/playwright/user-chat-redesign-detail.png`。
- [ ] 未标记生产完成：附近的人继续聊重复发起仍需幂等和 pending 复用，防止非 VIP 重复扣 5 积分。

## 2026-06-30 LOOP-15 新需求规则更新与实施拆分

- [x] 已把“删除树洞，消息承接第 4 个 tab”写入产品规则。
- [x] 已把游戏随机匹配、性别筛选、年龄筛选和次数一致写入需求账本。
- [x] 已把附近的人双端年龄进度条、删除距离筛选、统一城市筛选写入需求账本。
- [x] 已把头像不再显示文字、用户头像优先、随机头像池兜底写入需求账本。
- [x] 已把消息邀请卡片、同意、取消、同意后二次点击跳转写入需求账本和接口草案。
- [x] 已把后续实现拆为 LOOP-16 到 LOOP-19，避免一次性大改。
- [ ] 未标记功能完成：本轮只完成规则纠偏和实施拆分，代码实现从下一轮开始。

## 2026-06-30 LOOP-16 删除树洞与消息承接最小闭环

- [x] 排队编号已更新：R-019 对应 LOOP-16；游戏随机匹配进入 LOOP-17；统一城市与附近的人年龄双端滑条进入 LOOP-18；头像资源与资料同步进入 LOOP-19；消息邀请卡片进入 LOOP-20；上下文会话生产持久化进入 LOOP-21。
- [x] `src/pages.json` 已移除 `pages/treehole/index` 路由注册，底部第 4 个 tab 已改为 `消息` 并指向 `pages/messages/index`。
- [x] 游戏页已移除树洞入口、`goTreehole()` 和相关样式，不再从游戏页跳转树洞。
- [x] 消息页和聊天详情页已承接历史 `treehole` 类型，展示层统一清洗为“留言”，避免用户端继续看到树洞文案。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 路由/接口冒烟通过：消息页 200、游戏页 200、`GET /messages` 200。
- [x] 截图证据：`output/playwright/loop16-messages-tab.png`、`output/playwright/loop16-game-no-treehole.png`。
- [ ] 未标记功能完成：消息邀请卡片同意/取消与同意后二次跳转已拆入 LOOP-20，本轮只完成删除树洞与消息承接 P0。

## 2026-06-30 LOOP-17 游戏随机匹配入口与筛选

- [x] 游戏页已新增随机匹配入口，并跳转到 `pages/game/match`。
- [x] 随机匹配页已提供真心话/大冒险次数、性别筛选和年龄区间筛选。
- [x] 后端已新增 `POST /game/random-match`，返回 `game_room` 来源、房间 ID、证据 ID 和 `wait_confirm` 下一步。
- [x] 匹配次数已复用现有 `truth/dare` quota，成功匹配扣对应次数，无匹配不扣次数。
- [x] 新增随机匹配前端参数映射测试和后端接口契约测试。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 接口冒烟通过：`output/playwright/game-random-match-smoke.json`。
- [x] 截图证据：`output/playwright/loop17-game-random-entry.png`、`output/playwright/loop17-game-random-filter.png`、`output/playwright/loop17-game-random-result.png`。
- [ ] 未标记生产完成：城市筛选仍按 LOOP-18 统一处理；随机匹配后进入真实房间/邀请卡片的完整交互仍需后续 LOOP 承接。

## 2026-06-30 LOOP-18 统一城市筛选与附近的人年龄双端滑条

- [x] 附近的人筛选已删除距离选项，不再显示选择距离。
- [x] 附近的人筛选已增加城市筛选，默认显示 `全国 / 北京 / 上海 / 广州 / 深圳 / 全部`。
- [x] 点击城市 `全部` 可展开更多城市：杭州、成都、重庆、武汉、南京、苏州等。
- [x] 附近的人年龄筛选已改为双端年龄滑条，可通过两端滑块调整区间。
- [x] 附近的人列表城市已从接口 `city` 字段读取，不再在页面内随机派生。
- [x] 后端 `GET /nearby/users` 已支持 `city` 参数，并对动态年龄区间做重叠匹配。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 接口冒烟通过：`output/playwright/nearby-city-age-smoke.json`。
- [x] 截图证据：`output/playwright/loop18-nearby-city-age-filter.png`、`output/playwright/loop18-nearby-city-expanded-age-drag.png`。
- [ ] 未标记全站完成：随机匹配和广场后续仍可继续接入同一城市数据源；全站图片头像池仍在 LOOP-19。

## 2026-06-30 LOOP-19 头像资源与用户资料同步

- [x] 已新增系统头像池：`src/utils/avatar.ts` 提供 30 个 `bottle-wave-01..30` seed，并通过 DiceBear `open-peeps` HTTP API 生成图片头像。
- [x] 已统一头像优先级：用户显式 `avatar_url` 优先；没有用户头像时使用系统随机头像 URL。
- [x] 后端附近的人、消息会话参与者、当前用户资料均返回图片头像 URL。
- [x] 附近的人、消息列表、聊天详情三个核心 H5 链路已移除头像文字兜底，截图断言头像节点文本为空。
- [x] 用户资料更新后会同步刷新当前用户在附近的人列表中的头像、昵称、城市和年龄资料。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 接口冒烟通过：`output/playwright/avatar-url-smoke.json`。
- [x] 截图证据：`output/playwright/loop19-nearby-image-avatars.png`、`output/playwright/loop19-messages-image-avatars.png`、`output/playwright/loop19-chat-image-avatar.png`。
- [x] UI 断言：`output/playwright/loop19-avatar-ui.json`。
- [ ] 未标记全站完成：历史未注册页面、后台管理页和旧 mock 命名中的 `avatarText/iconText` 仍需按后续 P2 清理，避免未来误用回文字头像。

## 2026-06-30 LOOP-20 消息邀请卡片同意/取消与二次跳转

- [x] 后端已新增用户侧 `GET /chat/context-requests` 邀请列表，并为当前用户生成稳定测试邀请卡片。
- [x] 邀请卡片 pending 状态支持同意和取消：同意后生成 active 临时会话，取消后状态变为 `expired`。
- [x] 消息页已以卡片形式展示邀请数据，pending 卡片显示“同意/取消”，active 卡片显示“进入会话”。
- [x] 同意后会跳转 `/pages/messages/chat?contextConversationId=...`，回到消息页二次点击 active 卡片仍直接进入同一会话。
- [x] 前端 API 与 store 已接入邀请列表、同意、取消。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 接口冒烟通过：`output/playwright/message-invitation-smoke.json`。
- [x] 截图证据：`output/playwright/loop20-message-invite-card-pending.png`、`output/playwright/loop20-message-invite-accepted-chat.png`、`output/playwright/loop20-message-invite-card-active.png`。
- [x] UI 断言：`output/playwright/loop20-message-invite-ui.json`。
- [x] 后续承接已完成：上下文会话生产持久化已由 LOOP-21 完成；重复扣费最小幂等保护已由 LOOP-22 完成。

## 2026-06-30 LOOP-21 上下文会话生产持久化

- [x] `chat_context_requests`、`chat_conversations`、`chat_messages`、`chat_conversation_reports`、`chat_conversation_blocks` 已加入 SQLAlchemy 模型。
- [x] 已新增 Alembic 迁移 `backend/alembic/versions/0011_context_chat_persistence.py`，包含 upgrade 和 downgrade。
- [x] `chat_store` 已从内存 dict 迁移为数据库读写，旧 dict 仅保留给重启式测试清空，不再承载状态。
- [x] `/chat/context-requests`、accept/reject、`/chat/conversations`、messages、report、block、admin chat routes 均保持原接口路径并改为 `AsyncSession`。
- [x] 后端测试已覆盖创建、确认、发送消息后清空旧内存容器仍可读取会话和消息。
- [x] 真实接口冒烟已覆盖 pending -> active -> send message -> 重启 8110 -> GET conversation/list 仍可读取。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 接口冒烟通过：`output/playwright/context-persistence-smoke.json`。
- [x] 截图证据：`output/playwright/loop21-persisted-conversation-after-restart.png`。
- [x] UI 断言：`output/playwright/loop21-persisted-conversation-ui.json`。
- [x] 后续承接已完成：附近的人重复扣费幂等与 pending/active 复用已由 LOOP-22 完成；更细短期频控保留 P2。

## 2026-06-30 LOOP-22 附近的人继续聊重复扣费保护

- [x] 后端已在扣费前按 `initiator_id + target_user_id + source_type=match_expand + source_id` 查找 pending/active 请求。
- [x] 已存在 pending/active 时复用同一请求 ID，返回 `cost_coins=0`，不再次扣 5 积分。
- [x] 非 VIP 首次发起仍扣 5 积分，保持原门槛。
- [x] 前端重复发起时展示“已复用申请，不重复扣积分，继续聊申请已发出，等待对方确认”。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 接口冒烟通过：`output/playwright/match-expand-idempotency-smoke.json`。
- [x] 截图证据：`output/playwright/loop22-match-expand-idempotency.png`。
- [x] UI 断言：`output/playwright/loop22-match-expand-idempotency-ui.json`。
- [ ] 未标记全量完成：更细的短期频控和客户端按钮持久禁用可后续 P2 优化。
## 2026-06-30 LOOP-23 可见头像文字兜底清理

- [x] H5 瓶子、广场、广场评论、首页、我的、创作者页、历史树洞页可见头像 fallback 已改为图片 URL。
- [x] admin-web 用户、内容作者、聊天参与者、举报目标、审计操作人头像 fallback 已改为图片 URL。
- [x] 保留 `avatar_text/icon_text` 作为接口兼容字段和礼物图标字段，未做破坏性 schema 删除。
- [x] 可见模板残留扫描通过：本轮目标文件无 `<text v-else>` / `<span v-else class="avatar">` 头像文字 fallback。
- [x] 接口冒烟通过：`output/playwright/avatar-url-smoke.json`。
- [x] UI 断言通过：`output/playwright/loop23-avatar-fallbacks-ui.json`，广场列表 3/3、广场评论 2/2、我的页 1/1、后台用户页 10/10 均为图片头像且文本为空。
- [x] 截图证据：`output/playwright/loop23-plaza-avatar-fallbacks.png`、`output/playwright/loop23-plaza-comment-avatar-fallbacks.png`、`output/playwright/loop23-profile-avatar-fallback.png`、`output/playwright/loop23-admin-avatar-fallbacks.png`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [ ] 未标记 schema 清理完成：字段级 `avatar_text/icon_text` 重命名或删除需要单独数据库迁移 LOOP。
## 2026-06-30 LOOP-24 自动总验收

- [x] 复跑 `npm run typecheck`，通过。
- [x] 复跑 `npm run test:frontend`，4 个测试文件、27 条测试通过。
- [x] 复跑 `npm run build:h5:e2e`，通过。
- [x] 复跑 `npm run build:admin`，通过。
- [x] 复跑 `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`，54 passed。
- [x] 复跑 `python -m compileall -q backend\app backend\tests`，通过。
- [x] 接口冒烟通过：头像兜底、消息邀请、会话持久化、扩列幂等、附近的人筛选、好友申请规则、游戏随机匹配。
- [x] 截图复验通过：消息邀请卡片、持久化会话详情、扩列幂等、附近的人筛选、头像图片兜底。
- [x] 旧规则扫描完成：代码侧无旧规则命中，文档命中均为旧规则废弃/补丁覆盖/验收上下文。
- [x] 后台隔离扫描完成：`src/pages.json` 无后台或树洞页面路由。
- [x] 剩余 P0/P1 已写入 `docs/detail-optimization-inbox.md`，未在本轮混做。
## 2026-06-30 LOOP-25 管理员真实账号与权限矩阵最小闭环

- [x] 后端支持 `ADMIN_ACCOUNTS` 多账号配置，默认包含 admin / moderator / risk。
- [x] 管理员登录返回签名 session token，并能通过 `/admin/auth/me` 读取角色。
- [x] 后台读取接口已挂 bearer token 和角色校验。
- [x] moderator 可读取后台摘要，但更新奖励配置返回 403 `ADMIN_FORBIDDEN`。
- [x] 接口冒烟 `node output\playwright\admin-auth-smoke.cjs` 通过。
- [x] 后端测试 `$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`：55 passed。
- [x] 前端门禁 `npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin` 均通过。
- [x] 后台截图：`output/playwright/loop25-admin-auth-dashboard.png`。
- [x] 后续真实身份源、密码哈希、MFA 和细粒度权限已写入 `docs/detail-optimization-inbox.md`。
## 2026-06-30 LOOP-26 真实 PostgreSQL/Alembic/Redis 迁移执行验收

- [x] 已读取 Alembic 配置和迁移文件。
- [x] 已探测本机 PostgreSQL/Redis/Docker 环境。
- [x] 已生成 PostgreSQL 方言离线升级 SQL：`backend/runtime/loop26-postgres-upgrade.sql`。
- [x] 已记录 PostgreSQL 连接失败、Redis 连接失败、Docker daemon 未运行证据。
- [x] 已完成真实 PostgreSQL 迁移执行：临时容器 `drift-loop26-postgres`，版本到 `0011_context_chat_persistence (head)`。
- [x] 已完成 Redis 冒烟：临时容器 `drift-loop26-redis`，`PING` 返回 `PONG`。
- [x] 已修复 PostgreSQL 外键顺序问题：种子 `PlazaPost` 先 flush，再插入 `PlazaMedia`。
- [x] 已通过 admin auth 冒烟和 PostgreSQL 重启持久化会话冒烟。
- [x] LOOP-26 解除阻塞后结论更新为通过。
## 2026-06-30 LOOP-27 私密照片真实上传、收益冻结和申诉最小闭环

- [x] 私密照片审核从内存 store 迁移到数据库 `private_photo_assets`。
- [x] 新增 Alembic 迁移 `0012_private_photo_reviews` 并在 Docker PostgreSQL 测试库升级到 head。
- [x] 低风险照片 AI 自动通过，收益 `eligible`，可解锁。
- [x] 高风险照片冻结/不可收益，申诉后进入 `appeal_pending`，收益保持 `frozen`，不可解锁。
- [x] 后台照片审核队列可看到申诉中和冻结状态。
- [x] 接口冒烟：`node output\playwright\private-photo-postgres-smoke.cjs` 通过。
- [x] 截图：`output/playwright/loop27-private-photo-review-admin.png`。
- [x] 后端测试 56 passed，前端测试 27 passed，H5/admin 构建通过。

## 2026-06-30 LOOP-28 字段级错误码与审计链路收口

- [x] `VALIDATION_ERROR` 响应新增 `details.field_errors[]`，包含 `field/code/message`，并保留 `raw_errors` 兼容旧调用方。
- [x] 私密照片创建、解锁、申诉、人工复核审计 ID 已同步写入 `private_photo_assets.audit_refs` 和 `admin_audit_logs`。
- [x] `/admin/audit` 已读取数据库审计记录，并兼容合并旧内存审计记录。
- [x] 后台审计动作已补私密照片相关中文标签，截图可见“私密照片申诉”和目标编号。
- [x] 接口冒烟通过：`output/playwright/loop28-error-audit-smoke.json`。
- [x] 截图通过：`output/playwright/loop28-admin-audit.png`。
- [x] 验证通过：`python -m compileall -q backend\app backend\tests`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、PostgreSQL Alembic current。
- [x] 当前 P0/P1 LOOP 队列已完成到 LOOP-28；后续仅保留 P2/生产增强项。
## 2026-06-30 LOOP-29 小程序桥接与广告激励视频配置

- [x] 后端新增 `app_configs` 持久化配置表，并通过 Alembic `0013_app_configs_ad_reward` 升级到 head。
- [x] 后台 `/admin/reward-config` 已支持广告联盟、广告位、展示类型、倒计时、素材 URL、落地页、小程序 AppID/路径和奖励次数配置。
- [x] 用户端新增 `pages/ad/reward` 激励视频页，展示倒计时、小程序桥接和广告落地页入口。
- [x] 首页和签到页广告入口已改为进入激励视频页，避免旧的即时奖励体验。
- [x] `/me/status`、`/ads/reward/prepare`、`/ads/reward/commit` 已打通配置读取、准备会话和倒计时后发奖闭环。
- [x] 后台新增“广告配置”页，可直接配置广告与小程序桥接参数。
- [x] 修复 H5 激励视频页深色背景下标题对比度偏低的细节问题。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`。
- [x] 接口冒烟通过：`output/playwright/loop29-ad-bridge-smoke.json`。
- [x] 截图证据：`output/playwright/loop29-h5-reward-ad.png`、`output/playwright/loop29-admin-ad-config.png`。
- [ ] 真实广告联盟 SDK、微信小程序真实跳转、广告回调验签和反作弊计费仍需后续独立 LOOP。
## 2026-06-30 LOOP-30 前台聊天输入状态机与发布弹窗 UI 纠偏

- [x] 聊天输入区已改为麦克风、输入框、发送/加号的 IM 结构。
- [x] 无文本时显示加号，有文本时显示发送，避免空发送按钮常驻。
- [x] 加号面板已移到输入行下方，并压缩为较低高度的图标网格。
- [x] 麦克风按钮可切换语音模式，并自动关闭加号面板。
- [x] 聊天背景连续点击 20 次位移为 0，未出现页面抖动。
- [x] 发布弹窗顶部只保留必要标题，媒体入口改为图片/视频图标按钮。
- [x] 发布弹窗底部只保留取消和发布按钮。
- [x] 发布弹窗支持视频选择、预览和取消清理。
- [x] 新增一键验收脚本 `scripts/run-ui-message-admin-loop.ps1`。
- [x] 新增 UI 冒烟脚本 `scripts/ui-message-admin-loop-smoke.cjs`。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`python -m compileall -q backend\app backend\tests`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-chat-plus-panel.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-voice.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-publish-modal.png`。
- [ ] 后台私密照片审核详情、举报用户证据链搜索、未读消息域拆分仍需后续独立 LOOP。
## 2026-06-30 LOOP-31 消息页信息架构纠偏与发现入口移除

- [x] 消息页快捷入口已从 3 个收敛为 2 个，仅保留留言消息和系统消息。
- [x] 已移除消息页 `精准查找` 入口和 `openNearby()` 跳转逻辑。
- [x] 已清理本轮删除产生的 `.target .quick-icon` 孤儿样式。
- [x] UI 冒烟脚本已新增消息页结构断言：`quickActionCount=2`、`hasMailEntry=true`、`hasSystemEntry=true`、`hasDiscoveryEntry=false`。
- [x] 一键验收 `.\scripts\run-ui-message-admin-loop.ps1` 通过，失败用例 0。
- [x] 前端门禁通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`。
- [x] 后端回归通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 58 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-messages.png`。
- [ ] 未标记全量完成：消息页双标题栏、未读清除状态机、后台证据链详情仍需后续独立 LOOP。
## 2026-06-30 LOOP-32 消息页标题栏冗余与未读清除状态机

- [x] `pages/messages/index` 已改为 `navigationStyle=custom`，消息页不再出现系统标题栏和自绘标题栏双层冗余。
- [x] 后端新增 `POST /conversations/{thread_id}/read`，只允许清除当前用户自己的会话未读数。
- [x] 前端 API 已新增 `businessApi.markConversationRead()`，并映射 `unread_count -> unreadCount`。
- [x] Store 已新增可等待的 `markConversationRead()`，本地先清零，再等待接口落库并刷新 thread。
- [x] 消息页点击私聊卡片、通知跳转私聊前会等待对应会话已读落库。
- [x] UI 冒烟新增自绘标题栏断言和未读清除断言，实际验证 `badge 2 -> 0`。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5:e2e`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 59 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-messages.png`。
- [ ] 未标记全量完成：留言消息/系统消息单条已读持久化、邀请卡片未读分区和验收脚本端口一致性仍需后续 LOOP。
## 2026-06-30 LOOP-33 H5/API E2E 服务端口一致性与一键验收脚本自愈

- [x] `scripts/run-ui-message-admin-loop.ps1` 已新增 `BackendPort` 和 `BackendDatabasePath` 参数。
- [x] 一键验收会停止并重启 `BackendPort` 上的 E2E 后端，避免旧后端进程吞掉新增接口。
- [x] 一键验收会等待 `$backendBaseUrl/me/status` 可用后再继续。
- [x] 一键验收会停止并重启 H5 dev server，并注入同一个 `VITE_API_BASE_URL`。
- [x] H5 构建已改为 `scripts/build-h5-e2e.ps1 -Port $BackendPort`，与运行态 API base 对齐。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 59 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [ ] 未标记全量完成：PostgreSQL/Redis 容器健康检查、端口自动选择和长期 CI 编排仍可后续增强。
## 2026-06-30 LOOP-34 留言消息/系统消息单条已读持久化与邀请卡片未读分区

- [x] 后端新增 `POST /messages/{message_id}/read`，只允许清除当前用户自己的单条消息通知未读状态。
- [x] 前端 API 和 store 已接入单条消息通知已读接口，保留本地即时已读反馈并由接口结果回填。
- [x] 消息页快捷入口角标已拆分为留言消息未读数和系统消息未读数。
- [x] 留言消息分区已展示待处理邀请、已处理邀请和留言通知。
- [x] 系统消息分区已排除邀请卡片，避免邀请和系统通知混杂。
- [x] UI 冒烟新增 `POST /messages/{id}/read` 接口断言、邀请分区断言和系统分区断言。
- [x] 修复 UI 冒烟从系统消息分区返回私聊列表的状态复位问题，后续聊天面板断言不再跑在错误页面。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 60 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：目标消息 `beforeUnread=true`，`markedUnread=false`，`afterUnread=false`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-message-notices.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-system-notices.png`。
- [ ] 未标记全量完成：后台通知类型配置、通知审计筛选和更细粒度邀请未读统计可后续拆分。
## 2026-06-30 LOOP-35 后台举报证据链检索与详情可视化

- [x] `GET /admin/reports` 已支持 `status`、`target_type`、`q` 查询参数。
- [x] 举报响应已新增 `reporter_id`、`evidence_refs`、`audit_refs`。
- [x] 聊天举报证据链已返回 report、chat、reporter、conversation、thread_status 引用。
- [x] 后台举报处置页已新增关键词搜索和选中举报详情。
- [x] 后台举报详情已展示举报编号、举报人、目标对象、原因、摘要、证据引用和审计引用。
- [x] UI 冒烟新增“后台举报页展示可检索证据链详情”断言。
- [x] 一键验收脚本已改为唯一隔离 E2E SQLite，避免旧测试库 schema 造成后台假失败。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 61 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：`GET /admin/reports?target_type=chat&q=thread` 返回 2 条，第一条 `evidence_refs` 为 5 个。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`。
- [ ] 未标记全量完成：举报处置动作、处罚联动、批量关闭和独立审计日志详情页仍需后续独立 LOOP。

## 2026-06-30 LOOP-36 举报处置动作与审计落库最小闭环

- [x] 已新增 `POST /admin/reports/{id}/resolve`。
- [x] 请求已要求 `reason`，处置原因会写入审计详情。
- [x] 响应已返回举报处置前状态、处置后状态、原因、审计 ID 和处置时间。
- [x] 后端已把目标举报状态更新为 `resolved`。
- [x] 后端已写入 `AdminAuditLog`，动作名为 `report_resolve`。
- [x] `GET /admin/reports` 复查时已能返回新增 `audit_refs`。
- [x] 后台举报详情已新增处理原因输入和“标记已处理”按钮。
- [x] UI 冒烟新增“后台举报处置写入已处理状态和审计引用”断言。
- [x] 已修复 UI 冒烟点击辅助函数，点击前先滚动到可视区域，避免面板底部按钮假失败。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 62 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：`POST /admin/reports/{id}/resolve` 返回 200，`after_status=resolved`，列表复查 `audit_refs` 包含本次 `audit_id`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`。
- [ ] 未标记全量完成：举报处罚联动、批量关闭、审计详情页和冻结收益仍需后续独立 LOOP。

## 2026-06-30 LOOP-37 举报处罚联动和审计详情页最小闭环

- [x] `POST /admin/reports/{id}/resolve` 已新增 `penalty_action`。
- [x] 已实现单个处罚动作：`limit_user`。
- [x] `limit_user` 当前只支持聊天举报，非聊天举报会返回不支持处罚动作。
- [x] 后端已根据聊天举报的举报人和会话双方解析被举报用户。
- [x] 被举报用户已被联动写为 `limited`。
- [x] 用户限制原因已写入 `AdminUserRestriction`。
- [x] 举报处置审计 detail 已写入 `penalty_action=limit_user` 和 `penalty_target_user_id`。
- [x] 已新增 `report_penalty_limit_user` 审计记录。
- [x] `GET /admin/audit` 已返回 `detail`。
- [x] 后台举报详情已新增处置动作选择。
- [x] 后台审计页已新增审计详情面板。
- [x] UI 冒烟新增“后台审计详情展示举报处罚联动记录”断言。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 63 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：`penalty_action=limit_user` 返回 200，目标用户 `status=limited`，审计 detail 包含处罚动作。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-detail.png`。
- [ ] 未标记全量完成：内容下线、聊天冻结、收益冻结、批量处置、二次确认和用户端通知仍需后续独立 LOOP。

## 2026-06-30 LOOP-38 举报冻结聊天最小闭环

- [x] `POST /admin/reports/{id}/resolve` 已新增 `penalty_action=freeze_chat`。
- [x] `freeze_chat` 当前只支持聊天举报，避免非聊天举报误冻结。
- [x] 目标聊天线程状态已可写为 `risk_frozen`。
- [x] 冻结后举报证据链已展示 `thread_status:risk_frozen`。
- [x] 冻结后继续发送聊天消息会返回 `403 / CHAT_RISK_FROZEN`。
- [x] 已新增 `report_penalty_freeze_chat` 审计。
- [x] `report_resolve` 审计 detail 已写入 `penalty_action=freeze_chat` 和 `penalty_target_thread_id`。
- [x] 后台举报处置动作下拉已新增“冻结聊天”。
- [x] UI 冒烟新增“后台审计详情展示举报冻结聊天记录”断言。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 64 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：`penalty_action=freeze_chat` 返回 200，`evidence_refs` 包含 `thread_status:risk_frozen`，发消息返回 `CHAT_RISK_FROZEN`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/admin-1366-reports.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-detail.png`。
- [ ] 未标记全量完成：内容下线、收益冻结、批量处置、二次确认、处罚撤销、用户端通知和申诉仍需后续独立 LOOP。

## 2026-06-30 LOOP-39 处罚后用户端通知与冻结提示最小闭环

- [x] `freeze_chat` 处置后已生成 `business_type=chat_freeze` 的系统通知。
- [x] `ConversationThread` 已新增 `status` 和 `frozenNotice/frozen_notice` 用户端字段。
- [x] 冻结会话已可继续出现在私聊列表，并可通过系统通知直达聊天详情。
- [x] 聊天详情已展示“聊天已冻结”、冻结说明和申诉说明入口。
- [x] 冻结聊天页已禁用输入、媒体、礼物和房间入口。
- [x] 后端仍以 `403 / CHAT_RISK_FROZEN` 拦截冻结会话发送。
- [x] UI 冒烟新增“用户端系统通知可进入冻结聊天说明”断言。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 64 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：`chat_freeze` 通知存在，冻结会话 `status=risk_frozen`，发消息返回 `CHAT_RISK_FROZEN`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-chat-frozen.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-detail.png`。
- [ ] 未标记全量完成：真实申诉工单、处罚撤销/恢复、内容下线、收益冻结和批量处置仍需后续独立 LOOP。

## 2026-06-30 LOOP-40 冻结聊天恢复与审计最小闭环

- [x] 已新增 `POST /admin/reports/{id}/restore`。
- [x] 恢复接口仅允许聊天举报且目标线程为 `risk_frozen`。
- [x] 恢复后目标聊天线程状态回到 `active`。
- [x] 恢复后可正常发送聊天消息。
- [x] 恢复后已生成 `business_type=chat_restore` 系统通知。
- [x] 恢复后已写入 `report_restore_chat` 审计。
- [x] 后台举报详情已在冻结聊天证据链下展示“恢复聊天”按钮。
- [x] UI 冒烟新增后台恢复、恢复审计、用户端恢复输入区断言。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 65 passed，`python -m compileall -q backend\app backend\tests` 通过。
- [x] 接口冒烟：恢复前 `risk_frozen`，恢复后 `active`，恢复后发消息成功，通知为 `chat_restore`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/admin-1366-reports-restored.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-audit-restore.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-restored.png`。
- [ ] 未标记全量完成：真实申诉工单、内容下线、收益冻结、批量处置和二次确认仍需后续独立 LOOP。

## 2026-06-30 LOOP-41 用户端私聊位置、附近开聊和留言即时反馈纠偏

- [x] 附近的人“开聊”已改为直接创建/复用 active 私聊线程，不再等待对方同意。
- [x] VIP 开聊免费，非 VIP 首次开聊消耗 5 积分，复用已有会话不重复扣费。
- [x] 附近的人开聊接口已返回 `thread_id`，前端点击后直接跳转聊天页。
- [x] 聊天页普通私聊头部已展示双方头像和昵称，并压缩边界避免错位。
- [x] 广场帖子留言提交后本页即时追加显示，再异步刷新后端列表。
- [x] 留言时间已修复无时区 UTC 解析，刚提交内容显示“刚刚”。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 65 passed。
- [x] 验证通过：附近的人契约定向测试 3 passed。
- [x] 接口冒烟：附近的人开聊返回 `request_status=active`、`thread_id`、`cost_coins=0`，读取会话返回对方昵称和头像 URL。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-nearby-direct-chat.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-plaza-comment-immediate.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-plus-panel.png`。
- [ ] 未标记全量完成：真实申诉工单、内容下线、收益冻结、批量处置和二次确认仍需后续独立 LOOP。

## 2026-07-01 LOOP-42 冻结聊天真实申诉工单最小闭环

- [x] 已新增 `chat_appeals` 持久化表。
- [x] 已新增 Alembic 迁移 `backend/alembic/versions/0014_chat_appeals.py`。
- [x] 用户端已新增 `POST /conversations/{thread_id}/appeal`。
- [x] 非冻结聊天不能提交冻结申诉。
- [x] 同一用户同一冻结聊天 pending 申诉会复用，不重复生成。
- [x] 后台已新增 `GET /admin/chat-appeals`。
- [x] 后台已新增 `POST /admin/chat-appeals/{appeal_id}/review`。
- [x] 后台通过申诉后聊天恢复为 `active`，并通知用户 `chat_appeal_approved`。
- [x] 后台驳回申诉后聊天保持 `risk_frozen`，并通知用户 `chat_appeal_rejected`。
- [x] 申诉提交、通过和驳回均写入 `AdminAuditLog`。
- [x] 用户端冻结聊天页已展示申诉输入框和提交按钮。
- [x] 后台举报处置页已展示聊天申诉工单列表、详情、通过/驳回按钮。
- [x] 验证通过：`.\scripts\run-ui-message-admin-loop.ps1`，失败用例 0。
- [x] 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`。
- [x] 验证通过：`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q` 为 66 passed。
- [x] 验证通过：`python -m compileall -q backend\app backend\tests`。
- [x] 验证通过：Alembic head 为 `0014_chat_appeals`，离线 SQL 包含 `CREATE TABLE chat_appeals`。
- [x] 接口冒烟：申诉提交为 `pending`，后台列表可见，通过后线程 `active`、通知存在、审计动作为 `chat_appeal_approve`。
- [x] 截图证据：`reports/ui-message-admin-loop/screenshots/mobile-390-chat-appeal-submitted.png`、`reports/ui-message-admin-loop/screenshots/admin-1366-chat-appeal-rejected.png`、`reports/ui-message-admin-loop/screenshots/mobile-390-chat-restored.png`。
- [ ] 未标记全量完成：内容下线、私密照片收益冻结/解冻、批量处置和二次确认仍需后续独立 LOOP。
- [ ] 未标记全量完成：真实申诉工单、内容下线、收益冻结、批量处置和二次确认仍需后续独立 LOOP。

## 2026-07-01 LOOP-43 内容下线处罚联动最小闭环

- [x] 举报处置新增 `offline_content` 处罚动作。
- [x] `offline_content` 支持瓶子、广场帖子、广场留言下线，目标状态改为 `rejected`。
- [x] 举报列表证据链展示 `content_status:rejected`，广场留言额外展示 `content_type:plaza_comment`。
- [x] 内容下线写入 `report_penalty_offline_content` 审计，举报处理审计记录 `penalty_target_content_id/type`。
- [x] 内容所有者收到 `content_offline` 系统通知。
- [x] 后台举报处置 UI 可选择“下线目标内容”，审计页可查看“举报下线内容”。
- [x] 后端测试、接口冒烟、H5/admin 构建、UI 冒烟截图和文档回写完成。
## 2026-07-01 LOOP-44 举报目标边界与用户信息名片入口

- [x] 已纠偏 LOOP-44：私密照片不进入普通举报处置。
- [x] 用户端普通举报目标已限定为用户、漂流瓶、广场帖子。
- [x] `businessApi` 新建举报入口已收窄为 `ReportableTargetType = 'user' | 'bottle' | 'plaza'`。
- [x] content store 已新增 `reportUser` 和 `reportPlazaPost`，保留 `reportBottle`。
- [x] 广场帖子卡片已新增帖子举报入口。
- [x] 广场作者头像点击已打开用户信息名片，名片左上角提供“举报”入口。
- [x] 文档已明确私密照片、聊天、评论、树洞历史内容不得展示普通举报按钮。
- [x] LOOP-44 验证通过：`npm run typecheck`、`npm run test:frontend`、`npm run build:h5`、`npm run build:admin`、`$env:PYTHONPATH='backend'; python -m pytest backend\tests -q`、`scripts\run-ui-message-admin-loop.ps1`。
- [x] LOOP-44 接口冒烟通过：`POST /reports` 的 `user`、`plaza`、`bottle` 三类目标均返回 `queued`，证据 `reports/loop44/api-smoke.json`。
- [x] LOOP-44 截图已生成：`reports/loop44/screenshots/mobile-390-plaza-report-post-entry.png`、`mobile-390-plaza-user-card-report.png`、`mobile-390-plaza-user-report-modal.png`。
- [x] 后台 `/reports` 历史 target_type 兼容读取仍保留；如需强制 API 拒绝旧类型，已登记到 `O-048` 作为独立后续 LOOP。
