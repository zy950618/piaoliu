---
name: "漂流瓶社交"
description: "从海边情绪内容自然进入清晰关系任务的微信小程序设计系统"
colors:
  primary-sea: "#358BA9"
  action-blue: "#0071E3"
  shell-white: "#F7FAFC"
  surface-white: "#FFFFFF"
  ink: "#172536"
  muted: "#7D8DA0"
  divider: "#E7EDF2"
  private-purple: "#775B9F"
  unread-coral: "#EF6467"
  success-teal: "#5F9F8F"
typography:
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "25px"
    fontWeight: 800
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "17px"
    fontWeight: 750
    lineHeight: 1.35
    letterSpacing: "normal"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, Segoe UI, PingFang SC, Microsoft YaHei, sans-serif"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "normal"
rounded:
  xs: "6px"
  sm: "10px"
  md: "12px"
  sheet: "18px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
components:
  button-primary:
    backgroundColor: "{colors.action-blue}"
    textColor: "{colors.surface-white}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "10px 18px"
  button-secondary:
    backgroundColor: "{colors.shell-white}"
    textColor: "{colors.primary-sea}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "10px 18px"
  chip-public:
    backgroundColor: "#E5F1FF"
    textColor: "#1D67A9"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "3px 7px"
  chip-private:
    backgroundColor: "#F0EAFB"
    textColor: "{colors.private-purple}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "3px 7px"
  navigation-bottom:
    backgroundColor: "{colors.surface-white}"
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    rounded: "{rounded.sheet}"
    height: "66px"
---

# Design System: 漂流瓶社交

## Overview

**Creative North Star: “潮汐白页”**

情绪内容像海面：遇见页、漂流瓶和闪照可以使用真实海景、自然光线与连续缓慢的动态。任务界面像白页：消息、好友、房间设置和后台必须回到清晰、稳定、可长期阅读的白色产品壳。两者通过同一套海蓝品牌色、白色底部导航和一致的交互节奏连接，而不是把每个页面都做成海景。

系统必须保持清透、克制和有吸引力。拒绝杂乱功能方格、夸张渐变、广告感背景、过度圆角、悬浮白块和为了“高级感”添加的水波特效。用户进入任何页面都应立即知道当前关系类型、下一步动作和退出方式。

**Key Characteristics:**

- 情绪内容沉浸，任务界面清楚。
- 白色产品壳跨页面保持稳定。
- 主操作蓝、关系海蓝、私密紫、未读珊瑚各司其职。
- 列表优先使用分隔和留白，不默认包进卡片。
- 动效只解释页面、层级和状态变化。

## Colors

配色以真实海岸的清透感为依据，但不把蓝色铺满任务页面。

### Primary

- **关系海蓝 `primary-sea`：** 用于在线、关系来源、次级图标和非危险状态，是品牌的情绪颜色。
- **操作蓝 `action-blue`：** 仅用于当前导航、创建、发送、同意等主要操作。

### Secondary

- **私密紫 `private-purple`：** 只表示私密房及相关状态，禁止成为通用装饰色。
- **未读珊瑚 `unread-coral`：** 只表示未读、需要处理或风险提醒，禁止大面积使用。
- **成功青绿 `success-teal`：** 表示通过、保存成功和可用状态。

### Neutral

- **产品白 `shell-white`：** 页面基础背景。
- **表面白 `surface-white`：** 导航、输入区和需要与背景区分的操作表面。
- **深墨文字 `ink`：** 主要文字和重要标题。
- **海雾灰 `muted`：** 次要信息、时间和说明。
- **浅岸分隔 `divider`：** 列表分隔和结构边界。

**The White Shell Rule.** 消息、好友、房间设置和后台页面必须以白色产品壳为基础；深色或图片背景只属于情绪内容。

**The One Action Blue Rule.** 一个视图中只允许一个主要操作族使用操作蓝。未选中图标和装饰不得抢用该颜色。

## Typography

**Display Font:** 系统无衬线字体栈
**Body Font:** 系统无衬线字体栈

**Character:** 熟悉、耐读、不炫技。微信小程序中的关系任务需要优先保证中文清晰度和系统字体渲染稳定性，不使用展示型字体制造“情绪感”。

### Hierarchy

- **Headline：** 页面标题，紧凑但不压迫。
- **Title：** 会话名、弹层标题和重要分组标题。
- **Body：** 消息预览、说明和正文，长文控制在约70个中文字符的可读宽度内。
- **Label：** 导航、标签、时间和按钮，禁止使用全大写英文眉题。

**The One-Family Rule.** 前后台统一使用系统无衬线字体栈；层级只通过字号、字重、颜色和间距建立。

## Elevation

系统采用“平面优先、结构分层”的方式。列表依赖背景、分隔线和留白建立层级；阴影仅用于悬浮弹层、底部导航和按下反馈，不用于每一张列表项或卡片。

### Shadow Vocabulary

- **自然轻投影：** 小范围中性黑透明投影，用于悬浮按钮和底部弹层。
- **遮罩层：** 使用低透明深墨遮罩表达模态关系，不添加彩色光晕。

**The No Glow Rule.** 禁止彩色外发光、霓虹阴影和大面积模糊玻璃。若控件像漂浮的广告素材，说明投影过重。

## Components

### Buttons

- **Shape:** 主要操作使用完整胶囊；图标按钮使用圆形；常规按钮不使用超大圆角矩形。
- **Primary:** 操作蓝背景、白色文字，只服务当前主要动作。
- **Hover / Focus:** H5 使用清晰焦点环；按压缩小至约0.94，时长100–150ms。
- **Secondary / Ghost:** 产品白或浅海蓝背景，文字使用关系海蓝或深墨色。

### Chips

- **Style:** 公开房采用浅蓝底，私密房采用浅紫底；均为小型标签，不作为大按钮。
- **State:** 标签只表达实体属性，不表达可点击操作。

### Cards / Containers

- **Corner Style:** 常规容器控制在10–12px；底部弹层顶部为18px。
- **Background:** 任务表面使用产品白或表面白。
- **Shadow Strategy:** 静止列表无阴影；弹层使用自然轻投影。
- **Border:** 列表优先使用浅岸分隔线，不使用彩色侧边条。
- **Internal Padding:** 主要使用12px、16px和24px三个层级。

### Inputs / Fields

- **Style:** 浅灰或白色表面，胶囊输入仅用于聊天输入框；设置表单使用10–12px圆角。
- **Focus:** 边界转为操作蓝并出现可见焦点，不使用发光效果。
- **Error / Disabled:** 错误使用未读珊瑚；禁用降低对比但仍保持文字可读。

### Navigation

底部导航始终使用白色产品壳，位置和图标体系跨页面不变。选中项使用操作蓝和浅蓝底，切换过渡200–240ms。进入二级会话或申请页面时，底栏向下退出，返回后恢复。

### Conversation Rows

个人会话使用单头像；房间会话使用组合头像、公开/私密标签和人数。常态无卡片背景，通过分隔线保持扫描效率；未读角标只出现在右侧时间下方。

## Do's and Don'ts

### Do:

- **Do** 让遇见页承担海景和自然动态，让消息、好友和设置回到白色产品壳。
- **Do** 使用操作蓝表示唯一主操作，使用关系海蓝表示关系和状态。
- **Do** 用分隔线和留白组织消息列表，而不是把每一行做成卡片。
- **Do** 为所有按钮提供默认、按下、禁用、加载、成功和错误状态。
- **Do** 提供减少动态效果时的静态或淡入替代。

### Don't:

- **Don't** 使用杂乱的功能方格和没有层级的图标堆叠。
- **Don't** 使用过大的圆角卡片、明显悬浮的白色控件或嵌套卡片。
- **Don't** 使用廉价霓虹渐变、渐变文字、彩色光晕或装饰性玻璃效果。
- **Don't** 使用广告感视频背景或为了动效而增加明显水波和光效。
- **Don't** 使用机械、直男式或把系统规则直接写在主界面的文案。
- **Don't** 把普通聊天、房间和玩法混成同一个入口或同一个数据类型。
