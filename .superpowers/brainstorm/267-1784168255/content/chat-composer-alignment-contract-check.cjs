const fs = require('node:fs');
const path = require('node:path');

const htmlPath = path.join(__dirname, 'chat-message-room-v2.html');
const html = fs.readFileSync(htmlPath, 'utf8');

const keyboardStart = html.indexOf('<div id="prototypeKeyboard"');
const keyboardEnd = html.indexOf('</section>', keyboardStart);
const keyboard = html.slice(keyboardStart, keyboardEnd);
const composerStart = html.indexOf('<div class="composer">');
const composerEnd = html.indexOf('</section>', composerStart);
const composer = html.slice(composerStart, composerEnd);
const roomComposerStart = html.indexOf('<div id="roomComposer"');
const roomComposerEnd = html.indexOf('</section>', roomComposerStart);
const roomComposer = html.slice(roomComposerStart, roomComposerEnd);
const roomToolsStart = html.indexOf('<div id="roomTools"');
const roomToolsEnd = html.indexOf('<div id="roomComposer"', roomToolsStart);
const roomTools = roomToolsStart >= 0 ? html.slice(roomToolsStart, roomToolsEnd) : '';
const roomMediaFunction = html.match(/function openRoomMedia\(\)\{([^\n]+)\}/)?.[1] || '';

const expectedNineKeys = ['1', '2 ABC', '3 DEF', '4 GHI', '5 JKL', '6 MNO', '7 PQRS', '8 TUV', '9 WXYZ'];
const roomMediaLabels = [...roomTools.matchAll(/<span>(图片|闪照|视频)<\/span>/g)].map(match => match[1]);
const chatShellStart = composer.indexOf('class="chat-input-shell"');
const micIndex = composer.indexOf('id="micButton"');
const chatInputIndex = composer.indexOf('id="chatInput"');
const chatSendIndex = composer.indexOf('id="chatSendButton"');
const chatMoreIndex = composer.indexOf('id="chatMoreButton"');
const roomInputIndex = roomComposer.indexOf('id="roomInput"');
const roomSendIndex = roomComposer.indexOf('id="roomSend"');
const roomMoreIndex = roomComposer.indexOf('id="roomMediaButton"');

const result = {
  forbiddenSuggestionCount: ['慢慢说', '我在听', '抱抱你'].filter(text => keyboard.includes(text)).length,
  hasQwertyRows: /class="keyboard-key">[QWERTYUIOP]</.test(keyboard),
  hasNineGrid: keyboard.includes('class="nine-key-grid"'),
  nineKeysPresent: expectedNineKeys.every(label => keyboard.includes(label)),
  chatInputShellExists: chatShellStart >= 0,
  micInsideInputShell: chatShellStart >= 0 && micIndex > chatShellStart && micIndex < chatInputIndex,
  chatComposerOrder: chatInputIndex >= 0 && chatInputIndex < chatSendIndex && chatSendIndex < chatMoreIndex,
  micHandlerPreserved: composer.includes('id="micButton"') && composer.includes('onclick="toggleVoiceMode()"'),
  roomComposerOrder: roomInputIndex >= 0 && roomInputIndex < roomSendIndex && roomSendIndex < roomMoreIndex,
  roomMoreUsesSingleStyle: roomComposer.includes('class="room-more-tools"'),
  roomToolsExists: roomToolsStart >= 0,
  roomMediaLabels,
  roomToolsStateStyles: /\.room-view\.tools-open \.room-composer/.test(html) && /\.room-tools\.open/.test(html),
  roomMediaNoLongerModal: roomMediaFunction.length > 0 && !roomMediaFunction.includes('openActionCard')
};

const valid = result.forbiddenSuggestionCount === 0
  && result.hasQwertyRows === false
  && result.hasNineGrid === true
  && result.nineKeysPresent === true
  && result.chatInputShellExists === true
  && result.micInsideInputShell === true
  && result.chatComposerOrder === true
  && result.micHandlerPreserved === true
  && result.roomComposerOrder === true
  && result.roomMoreUsesSingleStyle === true
  && result.roomToolsExists === true
  && JSON.stringify(result.roomMediaLabels) === JSON.stringify(['图片', '闪照', '视频'])
  && result.roomToolsStateStyles === true
  && result.roomMediaNoLongerModal === true;

console.log(JSON.stringify(result, null, 2));
if (!valid) process.exitCode = 1;
