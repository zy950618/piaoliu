你现在接手这个漂流瓶项目，必须进入“持续 LOOP 企业级执行模式”。

先读取项目内规则包：

docs/enterprise-loop-v2/README_START_HERE.md
docs/enterprise-loop-v2/CODEX_COPY_PROMPT_SHORT_V2.md
docs/enterprise-loop-v2/00_CODEX_MASTER_PROMPT_ENTERPRISE_LOOP_V2.md
docs/enterprise-loop-v2/01_AI_LOOP_STANDARD_AND_PROJECT_LOOP.md
docs/enterprise-loop-v2/02_MULTI_AGENT_OPERATING_SYSTEM.md
docs/enterprise-loop-v2/04_PRODUCTION_ACCEPTANCE_GATES.md
docs/enterprise-loop-v2/ENTERPRISE_LOOP_ACCEPTANCE_CHECKLIST_DETAILED_V2.md

如果存在补丁规则，也必须读取，并以后读到的补丁规则覆盖旧规则：

docs/enterprise-loop-v2/patches/
docs/enterprise-loop-v2/patches/CODEX_RULE_PATCH_CHAT_PHOTO_V3.md
docs/enterprise-loop-v2/patches/CODEX_COPY_PROMPT_RULE_PATCH_SHORT_V3.md
docs/enterprise-loop-v2/patches/ACCEPTANCE_CHAT_PHOTO_V3.md

同时读取项目已有文档：

README.md
docs/product-rules.md
docs/api-contract.md
docs/design-system.md
docs/backend-interface-admin-plan.md
docs/multi-agent-workbench.md
docs/requirements-ledger.md
docs/completed-checklist.md
docs/detail-optimization-inbox.md
docs/work-history.md

## 一、最高强约束

1. 不允许重写已有业务。
2. 不允许把后台放回 src/pages 或用户端 pages.json。
3. 后台只允许在 admin-web/ 中继续优化。
4. 用户端底部导航保持：瓶子 / 广场 / 游戏 / 树洞 / 我的。
5. 不允许无上下文冷启动骚扰陌生人。
6. 私聊规则必须改为：允许明确互动上下文内的陌生人私聊。
7. 好友关系不是私聊唯一门槛，好友用于长期关系沉淀、更多资料可见性和更低频控限制。
8. 漂流瓶场景：B 捞到 A 的瓶子并回应后，A 回复该回应或点击“继续聊/私聊”，双方可开启上下文私聊，无需先加好友。
9. 广场/树洞场景：B 评论 A 的内容后，A 回复该评论或点击“继续聊/私聊”，双方可开启上下文私聊，无需先加好友。
10. 游戏/房间/扩列场景：双方进入同一房间或匹配上下文，并完成明确互动或确认后，可开启临时私聊。
11. 所有上下文私聊必须保留来源、上下文 ID、双向确认/回应证据、频控、拉黑、举报、风控和审计。
12. 私密照片规则必须改为：AI 智能审核优先，风险分级，人工复核兜底。
13. 低风险、高置信、非露骨、无敏感隐私、无未成年人疑似、无诈骗导流内容，可自动通过。
14. 中风险、低置信、边界内容进入人工复核。
15. 高风险内容自动拒绝、冻结或进入更严格复核。
16. 收益只允许来自审核通过且未冻结的内容。
17. 所有审核必须保留模型标签、置信度、风险等级、自动动作、人工复核记录和审计日志。
18. 每一轮必须按 LOOP 执行：READ → PLAN → SPLIT → IMPLEMENT → VERIFY → PREVIEW → REVIEW → RECORD → NEXT。
19. 每个子 Agent 必须有明确产物和验收证据。
20. 没有测试命令、截图、接口响应、日志或文件 diff 证据的“已完成”一律算未完成。
21. 每轮最多处理 1 个 P0 或 2 个 P1，不允许大范围乱改。
22. 每轮必须更新 docs/work-history.md、docs/completed-checklist.md、docs/requirements-ledger.md。
23. 发现文档和代码不一致时，必须先报告差异，再按当前 LOOP 范围修正。
24. 不允许只做文档后停止。规则修正完成后，必须继续进入下一阶段 LOOP，直到所有可安全处理的 P0/P1 完成，或遇到必须人工确认的阻塞。

## 二、持续 LOOP 定义

你不是只做一次分析，而是要持续循环推进。

每一轮 LOOP 必须包含：

### READ

读取本轮相关文档、代码、测试、接口、历史记录和规则补丁。

### PLAN

列出本轮目标、不可变规则、风险点、影响范围、验收门禁。

### SPLIT

拆分多子 Agent 并行任务。至少包含：

* Product Rules Agent：产品规则、上下文私聊、私密照片审核规则。
* API Contract Agent：接口契约、字段、状态机、错误码、分页、筛选。
* Backend Agent：后端 schema、路由、权限、审计、数据库迁移。
* Admin Web Agent：admin-web 页面、审核工作台、配置、批量处理、审计展示。
* User Frontend Agent：H5/小程序用户端体验、入口、弹窗、状态反馈。
* QA Agent：单元测试、接口测试、E2E、回归测试、截图验证。
* Security & Risk Agent：频控、风控、拉黑、举报、隐私、权限边界。
* Docs Agent：work-history、completed-checklist、requirements-ledger、detail-optimization-inbox 同步。

如果当前工具不支持真实子 Agent，就由主控模拟这些角色逐项审计；不允许省略分工。

### IMPLEMENT

只实现本轮范围内的最小闭环，不做无关重构。

### VERIFY

必须运行对应命令和接口冒烟。

### PREVIEW

涉及 UI 时必须生成或说明截图路径；没有截图不能声明 UI 完成。

### REVIEW

对照验收门禁判断：通过、部分通过、失败、阻塞。

### RECORD

写入 docs/work-history.md、docs/completed-checklist.md、docs/requirements-ledger.md；未完成项写入 docs/detail-optimization-inbox.md。

### NEXT

自动给出下一轮 LOOP 目标，并继续执行下一轮，除非遇到必须人工确认的问题。

## 三、暂停条件

只有以下情况才允许暂停并请求确认：

1. 需要删除大段已有业务。
2. 需要迁移真实数据库且可能破坏现有数据。
3. 需要修改核心商业规则但文档之间存在冲突。
4. 测试环境缺失导致无法验证关键功能。
5. 安全、隐私、合规风险无法由当前信息判断。
6. 当前轮改动会超过 1 个 P0 或 2 个 P1 的范围。

除此之外，不要停在“等待确认”，应继续进入下一阶段 LOOP。

## 四、本轮持续执行路线

### LOOP-0：读取与规则差异分析

目标：

1. 读取所有规则包、补丁规则和现有 docs。
2. 找出旧规则残留：

   * 陌生人不能直接私聊。
   * 好友申请通过后才开放聊天。
   * 私密照片必须先人工审核后展示。
3. 输出旧规则所在文件、行附近内容、应替换的新规则。
4. 不改代码前，先改文档规则。

验收：

* 已列出读取文件。
* 已列出旧规则残留位置。
* 已列出替换规则。
* 已列出影响范围。
* 已列出下一轮要改的文档清单。

完成后自动进入 LOOP-1。

### LOOP-1：文档规则纠偏

目标：

修改以下文档中的旧规则：

* docs/product-rules.md
* docs/api-contract.md
* docs/backend-interface-admin-plan.md
* docs/multi-agent-workbench.md
* docs/requirements-ledger.md
* docs/detail-optimization-inbox.md
* docs/work-history.md
* docs/completed-checklist.md
* docs/enterprise-loop-v2/*.md
* docs/enterprise-loop-v2/patches/*.md

必须写入新规则：

1. 上下文私聊。
2. 聊天来源 source_type/source_id。
3. 双向回应/确认。
4. 临时私聊状态。
5. 好友升级。
6. 频控、举报、拉黑、审计。
7. AI 图片审核风险分级。
8. 自动通过/人工复核/自动拒绝/冻结。
9. 审核模型证据和人工复核证据。
10. 收益冻结与解冻规则。

验收：

* 全项目搜索旧规则无残留，除非在历史记录中明确标记“旧规则已废弃”。
* docs/work-history.md 追加本轮记录。
* docs/requirements-ledger.md 新增或更新需求项。
* docs/completed-checklist.md 只能写“规则纠偏完成”，不能写“功能完成”。
* docs/detail-optimization-inbox.md 写入后续代码实现入口。

完成后自动进入 LOOP-2。

### LOOP-2：接口契约与状态机设计

目标：

基于新规则补接口契约，不急着写完整业务代码。

需要设计或补充：

#### 上下文私聊接口

* POST /chat/context-requests
* POST /chat/context-requests/{id}/accept
* POST /chat/context-requests/{id}/reject
* GET /chat/conversations
* GET /chat/conversations/{id}
* POST /chat/conversations/{id}/messages
* POST /chat/conversations/{id}/report
* POST /chat/conversations/{id}/block

#### 上下文来源

* bottle_reply
* plaza_comment
* treehole_comment
* game_room
* private_room
* match_expand
* friend

#### 会话状态

* pending
* active
* muted
* blocked
* expired
* reported
* risk_frozen

#### 私密照片审核接口

* POST /private-photos
* GET /private-photos
* GET /private-photos/{id}
* POST /private-photos/{id}/unlock
* GET /admin/private-photos/reviews
* GET /admin/private-photos/reviews/{id}
* POST /admin/private-photos/reviews/{id}/review
* GET /admin/private-photos/risk-summary

#### 审核状态

* ai_pending
* ai_approved
* manual_required
* manual_approved
* rejected
* frozen
* appeal_pending

验收：

* docs/api-contract.md 有字段级契约。
* 状态枚举完整。
* 错误码完整。
* 管理后台入口明确。
* 用户端入口明确。
* 后续代码实现拆入 P0/P1/P2。

完成后自动进入 LOOP-3。

### LOOP-3：后端最小闭环实现

目标：

只做最小可验证闭环，不一次性做完整复杂系统。

优先实现：

1. 上下文私聊数据模型或 mock store。
2. 会话来源 source_type/source_id。
3. 双向回应/确认后创建 active conversation。
4. 无上下文发起私聊返回错误。
5. 拉黑后不可继续发消息。
6. 举报后进入后台审核队列。
7. 私密照片 AI 审核 mock 风险分级。
8. 低风险自动通过。
9. 中风险进入人工复核。
10. 高风险拒绝或冻结。
11. 审计日志写入。
12. 后端测试覆盖主状态流。

验收命令：

npm run typecheck
npm run test:frontend
npm run build:h5
npm run build:admin
$env:PYTHONPATH='backend'; python -m pytest backend\tests -q

必须补接口冒烟：

* 无上下文私聊失败。
* 瓶子回应后可申请继续聊。
* 发帖人确认后会话 active。
* 拉黑后发消息失败。
* 低风险照片 AI 自动通过。
* 中风险照片进入人工复核。
* 高风险照片拒绝或冻结。

完成后自动进入 LOOP-4。

### LOOP-4：admin-web 后台管理实现

目标：

在 admin-web/ 中补管理后台，不允许写回用户端 src/pages/admin。

需要补：

1. 上下文私聊审核队列。
2. 举报聊天详情。
3. 会话来源跳转。
4. 私密照片 AI 审核结果页。
5. 人工复核工作台。
6. 风险等级筛选。
7. 批量处理。
8. 审计日志详情。
9. 操作人、时间、原因、前后状态。
10. 管理员权限控制。

验收：

* npm run build:admin 通过。
* 页面有真实数据或 mock 数据闭环。
* 每个审核操作有原因。
* 每个状态变化有审计记录。
* 截图至少包含：

  * 聊天审核列表。
  * 聊天详情。
  * 私密照片审核列表。
  * 私密照片复核详情。
  * 审计日志详情。

完成后自动进入 LOOP-5。

### LOOP-5：用户端体验实现

目标：

在不破坏现有业务的前提下，补用户感知路径。

需要补：

1. 漂流瓶回应后“继续聊”入口。
2. 发瓶人收到回应后的“回复/继续聊”入口。
3. 广场评论后，发帖人可“继续聊”。
4. 树洞评论后，发布者可“继续聊”。
5. 私聊开启前说明“基于本次互动开启”。
6. 临时会话到期或被拒绝时有明确提示。
7. 拉黑/举报入口明显。
8. 私密照片上传后展示 AI 审核状态。
9. 自动通过、人工复核、拒绝、冻结都有不同用户反馈。
10. 审核中不能产生收益。
11. 冻结后展示申诉或说明入口。

验收：

* H5 build 通过。
* 前端测试通过。
* 至少截图：

  * 瓶子回应后的继续聊入口。
  * 发帖评论后的继续聊入口。
  * 临时会话页面。
  * 私密照片上传审核状态。
  * 私密照片拒绝/复核状态。
* 不允许影响底部 5 个 tab。

完成后自动进入 LOOP-6。

### LOOP-6：生产级验收与回归

目标：

对照企业级验收门禁做最终回归。

必须检查：

1. 旧规则是否残留。
2. 接口是否有契约测试。
3. 后台是否独立 admin-web。
4. 用户端是否无后台入口。
5. 上下文私聊是否防骚扰。
6. 私密照片审核是否风险分级。
7. 拉黑/举报/审计是否闭环。
8. 权限是否隔离。
9. 错误码是否统一。
10. 空状态、加载态、失败态是否存在。
11. UI 是否有截图证据。
12. 测试命令是否完整通过。
13. 文档是否同步。
14. 未完成项是否进入 detail-optimization-inbox。

完成后输出最终 LOOP 报告。

## 五、每轮输出格式

每轮结束必须输出：

### LOOP 编号

例如 LOOP-1 文档规则纠偏。

### 本轮目标

说明本轮处理什么，不处理什么。

### 已读取文件

列出文件路径。

### 多子 Agent 分工

列出每个 Agent 的任务、产物、证据。

### 修改文件

列出所有 diff 文件。

### 验证命令

列出命令和结果。

### 接口冒烟

列出接口、请求、响应摘要。

### 截图证据

列出截图文件名；没有 UI 改动则说明不需要。

### 风险与回滚

说明是否有破坏性风险。

### 文档回写

说明写入了哪些 docs。

### 本轮结论

只能写：

* 通过
* 部分通过
* 失败
* 阻塞

### 下一轮 LOOP

明确下一轮编号、目标和范围，并继续执行。

## 六、立即开始

现在开始 LOOP-0。

先读取规则包、补丁规则和项目 docs，找出旧规则残留位置，输出差异分析。
LOOP-0 完成后不要停止，继续进入 LOOP-1 做文档规则纠偏。
LOOP-1 完成后继续 LOOP-2。
除非遇到暂停条件，否则持续推进。
