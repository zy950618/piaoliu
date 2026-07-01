# Codex 短版提示词 v2：漂流瓶企业级 LOOP 优化

你接手的是已有漂流瓶项目，不是重写项目。先读取 README、docs、admin-web、src、backend、backend/alembic、package.json。读取后先输出已读文件、已完成能力、Mock/占位能力、不可变业务规则、Agent 拆分和本轮禁止范围。

最高约束：后台必须保持独立 `admin-web/`，不得挂回用户端；用户端底部 Tab 固定为 瓶子/广场/游戏/树洞/我的；禁止无上下文冷启动骚扰，允许明确互动上下文内的陌生人私聊，好友不是私聊唯一门槛；关注不等于好友；充值金币不可提现；私密照片 AI 审核优先、风险分级、人工复核兜底；认证必须人工复核；附近的人只展示粗略距离；隐藏留言只给主人可见且匿名化作者；后台审核、提现、配置、封禁、批量动作必须写审计。

执行 LOOP：Read → Protect → Plan → Act → Observe → Evaluate → Verify → Reflect → Record → Decide。每轮最多处理 1 个 P0 或 2 个 P1。每轮开始必须写目标、读取文件、不可变规则、允许修改、禁止修改、子 Agent、验证方式、人工门禁、回滚方案。每轮结束必须写修改文件、接口变化、数据库变化、测试命令、接口冒烟、截图/视觉证据、失败项、风险项、文档同步和是否允许合并。

必须按多子 Agent 分工：A0 Orchestrator，A1 Backend Identity/RBAC，A2 Database/Persistence，A3 Admin Web UX，A4 Moderation/Safety，A5 Wallet/Finance，A6 User Frontend UX，A7 Growth/Product，A8 QA/E2E/Visual，A9 Observability/SRE/Security，A10 Docs Keeper。即使只有一个 Codex，也要分段执行并输出每个 Agent 的结果。

第一阶段只做生产级后台底座：真实管理员账号、密码哈希、token/session、RBAC、PostgreSQL/Redis、Alembic、审计真实落库、统一错误码、admin-web 角色菜单和按钮权限。Mock 不能冒充生产完成。

必须通过门禁：读取、架构、业务规则、RBAC、数据库、API 契约、Web Admin、用户端体验、性能、安全/隐私、可访问性、监控/SLO、测试回归、文档接力、发布回滚。没有证据不算完成。
