# 预览版本记录

## 2026-06-23 bottle-v8

- 页面：`/pages/bottle/index`
- 目标：修复预览未刷新、筛选关闭行为、主页动态感和关系动作小角标。
- 调整：
  - 重启 H5 dev 服务到 `http://127.0.0.1:5173/`，避免继续访问旧进程缓存。
  - 筛选弹窗点击选项只更新蓝底选中态，不关闭弹窗；只能通过“取消 / 保存”关闭。
  - 保存筛选后主屏筛选摘要立即刷新。
  - 主页保留原蓝绿月光配色，新增天空和海面的柔和过渡、雾化层和流动水流，弱化背景硬分割。
  - 捞到瓶子的关系动作改为“回应 + 关注 / 加好友 / 送礼物”，关注、好友、礼物均带右上角小角标。
- 验证：
  - `npm run typecheck` 通过。
  - `npm run build:h5` 通过。
  - `npm run test:frontend` 通过，5 个测试通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend/tests -q` 通过，6 个测试通过。
  - Chrome CDP 真实点击验证：选择筛选项后弹窗仍打开，点击保存后弹窗关闭，摘要变为 `北京 · 全部 · 全部`。
- 截图：
  - `runtime-bottle-fullscreen-v8.png`
  - `runtime-bottle-filter-selected-v8.png`
  - `runtime-bottle-filter-save-real-v8.png`
  - `runtime-bottle-caught-v8.png`

## 2026-06-23 bottle-v7

- 页面：`/pages/bottle/index`
- 目标：按最新反馈修正筛选选中态、弹窗位置和瓶子/水波视觉。
- 调整：
  - 筛选弹窗改为 chip 选择模式，已选择项显示蓝底白字。
  - 扔瓶弹窗和捞到瓶子弹窗都改为页面居中展示。
  - 保留原蓝绿月光配色，只优化瓶子造型、玻璃高光、瓶塞细节。
  - 水波纹从粗横向色块改为柔和细弧线，降低背景割裂感。
- 验证：
  - `npm run typecheck` 通过。
  - `npm run build:h5` 通过。
  - `npm run test:frontend` 通过，5 个测试通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend/tests -q` 通过，6 个测试通过。
- 截图：
  - `runtime-bottle-fullscreen-v7.png`
  - `runtime-bottle-filter-v7.png`
  - `runtime-bottle-throw-v7.png`
  - `runtime-bottle-caught-v7.png`

## 2026-06-23 bottle-v6

- 页面：`/pages/bottle/index`
- 目标：修复瓶子页预览时主体未显示、弹窗按钮被 TabBar 遮挡的问题。
- 问题：
  - Headless 首次截图过早，只看到系统导航和 TabBar；稳定后确认 DOM 已挂载。
  - H5 默认导航栏占用顶部，和“瓶子页全屏动画”目标不一致。
  - 扔瓶弹窗底部操作区会被底部 TabBar 覆盖。
- 调整：
  - 瓶子页改为 `navigationStyle: custom`，去掉系统顶部导航。
  - 主界面筛选入口直接展示当前筛选摘要。
  - 弹窗层级提高到 `z-index: 10000`，卡片限制最大高度并允许滚动。
  - 重新截取主屏、筛选、扔瓶、捞到瓶子四个状态。
- 验证：
  - `npm run typecheck` 通过。
  - `npm run build:h5` 通过。
  - `npm run test:frontend` 通过，5 个测试通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend/tests -q` 通过，6 个测试通过。
- 截图：
  - `runtime-bottle-fullscreen-v6.png`
  - `runtime-bottle-filter-v6.png`
  - `runtime-bottle-throw-v6.png`
  - `runtime-bottle-caught-v6.png`

## 2026-06-23 bottle-v5

- 页面：`/pages/bottle/index`
- 目标：补齐捞/扔、角标计数、筛选弹窗和瓶子详情信息。
- 调整：
  - 保留全屏动画主界面下的“捞 / 扔”双动作，并继续用角标显示对应剩余次数。
  - 筛选弹窗改为页面居中，包含“取消 / 保存”，保存只应用当前页面状态，不做持久记录。
  - 捞到瓶子弹窗补作者头像、昵称、VIP、认证、性别、年龄段和城市标签。
  - 扔瓶弹窗补“谁可以捞”和地区选择，关闭或发布后重置为默认。
- 验证：
  - `npm run typecheck` 通过。
  - `npm run build:h5` 通过。
  - `npm run test:frontend` 通过，5 个测试通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend/tests -q` 通过，6 个测试通过。
- 截图：
  - 当前浏览器预览工具被现有 Chrome profile 占用，截图待工具恢复后补采集。
  - 预期文件名：`runtime-bottle-fullscreen-v5.png`、`runtime-bottle-filter-v5.png`、`runtime-bottle-caught-v5.png`。

## 2026-06-23 bottle-v4

- 页面：`/pages/bottle/index`
- 目标：根据最新代码继续优化瓶子页视觉。
- 调整：
  - 背景从深海改为柔和月光蓝绿海面。
  - 筛选入口和筛选项增加“筛 / 城 / 性 / 龄”识别图标。
  - 瓶子重画为包含瓶塞、瓶口、瓶颈、玻璃高光、纸条和标签的玻璃瓶。
  - 保持全屏动画和捞/扔弹窗流程。
- 验证：
  - `npm run typecheck` 通过。
  - `npm run build:h5` 通过。
  - `npm run test:frontend` 通过。
  - `$env:PYTHONPATH='backend'; python -m pytest backend/tests -q` 通过。
- 截图：
  - 本次浏览器预览工具被现有 Chrome profile 占用，截图待工具恢复后补采集。
  - 预期文件名：`runtime-bottle-fullscreen-v4.png`、`runtime-bottle-modal-v4.png`。
