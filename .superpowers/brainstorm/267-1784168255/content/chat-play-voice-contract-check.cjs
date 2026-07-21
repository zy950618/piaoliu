const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(path.join(__dirname, 'chat-message-room-v2.html'), 'utf8');
const renderChat = html.match(/function renderCurrentChat\(\)\{([^\n]+)\}/)?.[1] || '';
const openPlay = html.match(/function openPlayChoice\(kind\)\{([^\n]+)\}/)?.[1] || '';
const rollDice = html.match(/function rollDice\(\)\{([^\n]+)\}/)?.[1] || '';
const result = {
  rendersPlayMessage: renderChat.includes("message.type==='play'") || html.includes("case 'play'"),
  rendersDiceMessage: renderChat.includes("message.type==='dice'") || html.includes("case 'dice'"),
  rendersVoiceMessage: renderChat.includes("message.type==='voice'") || html.includes("case 'voice'"),
  playUsesPromptInput: openPlay.includes('playPrompt') && html.includes('class="play-prompt-shell"'),
  randomInsidePrompt: html.includes('class="play-random"') && html.includes('randomizePlayPrompt()'),
  playHasModeState: html.includes('setPlayMode(') && html.includes('sendPlayInvite()'),
  diceOpensModal: rollDice.includes('openActionCard') && html.includes('startDiceRoll('),
  diceHasVisualPips: html.includes('class="dice-face"') && html.includes('class="dice-pip"'),
  diceNoTextFallback: !html.includes('appendMyBubble(`摇到了 ${value} 点`)'),
  diceSendsRichMessage: html.includes("type:'dice'") && html.includes('sendDiceResult()'),
  directVoiceHoldExists: html.includes('id="chatVoiceHold"') && html.includes("startVoiceRecording('direct'"),
  roomVoiceHoldExists: html.includes('id="roomVoiceHold"') && html.includes("startVoiceRecording('room'"),
  roomMicExists: html.includes('id="roomMicButton"') && html.includes('toggleRoomVoiceMode()'),
  waveformExists: html.includes('class="voice-wave"') && (html.match(/class="voice-bar"/g) || []).length >= 14,
  recordingLifecycleExists: html.includes('function startVoiceRecording(') && html.includes('function finishVoiceRecording(') && html.includes('cancelActiveRecording('),
  voiceSendsRichMessage: html.includes("type:'voice'") && html.includes('duration'),
  roomToolsRemainMediaOnly: ['图片', '闪照', '视频'].every(label => html.includes(`<span>${label}</span>`))
};

const valid = Object.values(result).every(Boolean);
console.log(JSON.stringify(result, null, 2));
if (!valid) process.exitCode = 1;
