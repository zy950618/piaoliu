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
- [x] 陌生人不能直接私聊，好友申请通过后才开放聊天。
- [x] 充值金币不可提现，收益金币转换为魅力值后按规则提现。
- [x] 私密照片必须先审后展，只允许审核通过的非露骨内容。

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
