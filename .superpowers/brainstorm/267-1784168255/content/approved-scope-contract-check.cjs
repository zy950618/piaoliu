const fs = require('node:fs');
const path = require('node:path');

const htmlPath = path.join(__dirname, 'chat-message-room-v2.html');
const html = fs.readFileSync(htmlPath, 'utf8');

const toolPanel = html.match(/<div id="chatTools" class="chat-tools">([\s\S]*?)<\/div>\s*<div class="composer">/)?.[1] || '';
const toolLabels = [...toolPanel.matchAll(/<span>([^<]+)<\/span>/g)].map(match => match[1]);
const toolActions = [...toolPanel.matchAll(/<button class="tool(?: room)?" onclick="([^"]+)">/g)].map(match => match[1]);
const expectedLabels = ['图片', '闪照', '视频', '摇骰子', '真心话', '大冒险', '房间', '更多玩法'];
const expectedActions = [
  "requestChatMedia('图片')",
  "requestChatMedia('闪照')",
  "requestChatMedia('视频')",
  'rollDice()',
  "openPlayChoice('truth')",
  "openPlayChoice('dare')",
  'openRoomSheet()',
  "showToast('更多玩法即将开放')"
];

const startReply = html.match(/function startBottleReply\(button,event\)\{([^\n]+)\}/)?.[1] || '';
const closeReply = html.match(/function closeBottleComposer\(\)\{([^\n]+)\}/)?.[1] || '';
const result = {
  groupHeadingCount: (toolPanel.match(/tool-group-label/g) || []).length,
  toolLabels,
  toolActions,
  hasFourByTwoGrid: /grid-template-rows:repeat\(2,76px\)/.test(html),
  hasLegacyFourRowOverride: /grid-template-rows:18px 70px 18px 70px/.test(html),
  hasPrototypeKeyboard: /id="prototypeKeyboard"/.test(html),
  hasKeyboardOpenStyles: /\.bottle-view\.keyboard-open/.test(html),
  focusesBeforeAnimationFrame: startReply.indexOf('input.focus') >= 0
    && (startReply.indexOf('requestAnimationFrame') < 0 || startReply.indexOf('input.focus') < startReply.indexOf('requestAnimationFrame')),
  opensKeyboardState: startReply.includes("classList.add('keyboard-open')"),
  closesKeyboardState: closeReply.includes("classList.remove('keyboard-open')")
};

const valid = result.groupHeadingCount === 0
  && JSON.stringify(result.toolLabels) === JSON.stringify(expectedLabels)
  && JSON.stringify(result.toolActions) === JSON.stringify(expectedActions)
  && result.hasFourByTwoGrid === true
  && result.hasLegacyFourRowOverride === false
  && result.hasPrototypeKeyboard === true
  && result.hasKeyboardOpenStyles === true
  && result.focusesBeforeAnimationFrame === true
  && result.opensKeyboardState === true
  && result.closesKeyboardState === true;

console.log(JSON.stringify(result, null, 2));
if (!valid) process.exitCode = 1;
