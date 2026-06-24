# 漂流瓶社交项目

一套面向微信小程序、iOS、Android 的「漂流瓶 + 真心话 + 大冒险 + 树洞」匿名轻社交产品骨架。

## 当前完成内容

- `uni-app + Vue 3 + TypeScript + Pinia` 前端骨架。
- 首页、漂流瓶、真心话、大冒险、树洞、消息、用户中心、会员中心、后台占位页面。
- 今日次数、VIP、广告冷却、签到、漂流币、Mock 内容数据。
- FastAPI 接口草案和 Pydantic schema。
- 产品设计规范与接口文档。

## 前端运行

```bash
npm install
npm run dev:h5
```

微信小程序构建：

```bash
npm run build:mp-weixin
```

## 后端运行

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 设计与产品文档

- `docs/product-rules.md`
- `docs/api-contract.md`
- `docs/design-system.md`
