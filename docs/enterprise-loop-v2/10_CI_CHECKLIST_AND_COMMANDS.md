# CI、命令、检查清单 v2

日期：2026-06-29

## 1. 基础命令

```bash
npm install
npm run typecheck
npm run test:frontend
npm run build:h5
npm run build:admin
```

后端：

```bash
cd backend
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
python -m compileall -q app tests
$env:PYTHONPATH='.'; python -m pytest tests -q
```

项目根目录下如按既有文档运行：

```bash
python -m compileall -q backendpp backend	ests
$env:PYTHONPATH='backend'; python -m pytest backend	ests -q
```

## 2. 后台启动

```bash
npm run dev:admin
npm run build:admin
```

验收：

- 独立后台可访问。
- 用户端 `src/pages.json` 无后台入口。
- 不同角色菜单不同。

## 3. H5 启动

```bash
npm run dev:h5
npm run build:h5
```

验收页面：

```text
#/pages/bottle/index
#/pages/plaza/index
#/pages/plaza/comments?postId=plaza_001
#/pages/treehole/index
#/pages/game/index
#/pages/profile/index
#/pages/nearby/index
```

## 4. 接口冒烟模板

管理员：

```bash
curl -i http://127.0.0.1:8100/admin/auth/me
curl -X POST http://127.0.0.1:8100/admin/auth/login -H "Content-Type: application/json" -d "{...}"
curl -H "Authorization: Bearer <token>" http://127.0.0.1:8100/admin/auth/me
```

广场：

```bash
curl http://127.0.0.1:8100/plaza/posts
curl http://127.0.0.1:8100/plaza/posts/plaza_001
curl http://127.0.0.1:8100/plaza/posts/plaza_001/comments
```

权限：

```bash
# review_admin 不能处理财务提现
# finance_admin 不能修改内容审核策略
# read_only_admin 不能执行任何写操作
```

## 5. 搜索检查

```bash
# 后台不得进用户端
grep -R "pages/admin\|后台管理\|admin-web" src/pages.json src/pages || true

# H5 双触发风险
grep -R "@tap=.*@click\|@click=.*@tap" src admin-web || true

# 明文密码风险
grep -R "password.*=.*['"]" backend/app || true

# token 泄露风险
grep -R "console.log.*token\|print.*token" backend src admin-web || true
```

## 6. Playwright 验收建议

关键路径：

- 管理员登录。
- 不同角色菜单。
- 内容审核通过/拒绝。
- 批量下架。
- 提现审核。
- 审计日志详情。
- 漂流瓶捞/扔。
- 广场点赞 toggle。
- 广场隐藏留言。
- 留言详情页隐私。

## 7. 失败处理

如果任意命令失败：

1. 不允许声明完成。
2. 记录失败命令和摘要。
3. 定位到 Agent。
4. 修复后重跑相关命令。
5. 如果修复影响其他模块，进入下一轮 LOOP。
