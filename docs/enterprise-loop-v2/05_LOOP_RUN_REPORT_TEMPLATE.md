# LOOP 运行报告模板 v2

> 每轮任务必须复制本模板填写。未填写完整不得声明完成。

## 1. LOOP START

```text
日期：
执行人/Agent：
本轮目标：
优先级：P0 / P1 / P2
本轮类型：Micro / Feature / Release / Product / Safety
```

## 2. Read：读取证据

```text
已读取文档：
已读取代码：
已读取测试：
已读取历史记录：
```

## 3. Protect：不可变规则

```text
本轮涉及的不可变业务规则：
本轮禁止修改的目录/文件：
本轮需要人工审批的动作：
```

## 4. Plan：执行计划

```text
子 Agent 分工：
修改范围：
接口变化预期：
数据库变化预期：
前端页面影响：
后台页面影响：
测试计划：
回滚计划：
```

## 5. Act：执行记录

```text
实际修改文件：
新增文件：
删除文件：
新增/修改接口：
新增/修改迁移：
配置变更：
```

## 6. Observe：运行观察

```text
本地启动命令：
后端接口冒烟：
前端页面路径：
后台页面路径：
日志观察：
截图/录屏：
```

## 7. Evaluate：对照验收

| 门禁 | 结果 | 证据 | 失败原因 |
| --- | --- | --- | --- |
| G0 读取 | PASS/FAIL | | |
| G1 架构 | PASS/FAIL | | |
| G2 业务规则 | PASS/FAIL | | |
| G3 RBAC | PASS/FAIL/NA | | |
| G4 DB | PASS/FAIL/NA | | |
| G5 API | PASS/FAIL/NA | | |
| G6 Admin UX | PASS/FAIL/NA | | |
| G7 User UX | PASS/FAIL/NA | | |
| G8 性能 | PASS/FAIL/NA | | |
| G9 安全 | PASS/FAIL/NA | | |
| G10 可访问性 | PASS/FAIL/NA | | |
| G11 监控 | PASS/FAIL/NA | | |
| G12 测试 | PASS/FAIL | | |
| G13 文档 | PASS/FAIL | | |
| G14 发布 | PASS/FAIL/NA | | |

## 8. Verify：命令结果

```bash
npm run typecheck
npm run test:frontend
npm run build:h5
npm run build:admin
python -m compileall -q backendpp backend	ests
$env:PYTHONPATH='backend'; python -m pytest backend	ests -q
```

实际输出摘要：

```text

```

## 9. Reflect：反思

```text
做对了什么：
发现的问题：
没完成的原因：
潜在风险：
下次 LOOP 需要更改的策略：
```

## 10. Record：文档同步

```text
requirements-ledger.md：
work-history.md：
completed-checklist.md：
api-contract.md：
backend-interface-admin-plan.md：
detail-optimization-inbox.md：
design-system.md：
```

## 11. Decide：决策

```text
是否允许合并：YES / NO
如果 NO，阻塞项：
如果 YES，下一轮任务：
需要哪个 Agent 接力：
```
