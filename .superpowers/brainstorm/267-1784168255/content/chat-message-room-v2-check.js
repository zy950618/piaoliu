import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const runCheck = async (page) => {
  const consoleErrors = [];
  page.on('console', message => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  await page.goto(process.env.CHECK_URL || 'http://127.0.0.1:8772/.superpowers/brainstorm/267-1784168255/content/chat-message-room-v2.html');
  await page.setViewportSize({ width: 390, height: 844 });

  if (process.env.CHECK_SCOPE === 'play-voice') {
    const resetPrototypeScroll = async () => page.evaluate(() => {
      document.querySelector('.phone').scrollTo(0, 0);
      document.querySelector('.screen').scrollTo(0, 0);
      window.scrollTo(0, 0);
    });
    const openDirectTool = async label => {
      await page.getByRole('button', { name: '更多功能', exact: true }).click();
      await page.waitForFunction(() => document.getElementById('chatTools').classList.contains('open') && getComputedStyle(document.getElementById('chatTools')).transform === 'none');
      await page.locator('#chatTools .tool').filter({ hasText: label }).click();
      await page.waitForFunction(() => document.getElementById('actionCard').classList.contains('open'));
    };

    await page.locator('.swipe-row[data-name="小雨"] .row-content').click();
    await page.waitForFunction(() => getComputedStyle(document.getElementById('chatView')).transform === 'none');

    await openDirectTool('真心话');
    const playPromptLayout = await page.evaluate(() => {
      const input = document.getElementById('playPrompt').getBoundingClientRect();
      const random = document.querySelector('.play-random').getBoundingClientRect();
      return {
        randomInsideInput: random.left >= input.right - 46 && random.right <= input.right + 1,
        randomTouchWidth: parseFloat(getComputedStyle(document.querySelector('.play-random')).width),
        defaultMode: document.querySelector('.play-mode-switch .active')?.dataset.mode
      };
    });
    await page.getByRole('button', { name: '随机题目', exact: true }).click();
    const randomTruthPrompt = await page.locator('#playPrompt').inputValue();
    await page.locator('.play-mode-switch').getByRole('button', { name: '私密', exact: true }).click();
    await page.locator('#playPrompt').fill('如果可以重新认识一个人，你最想先了解什么？');
    await page.locator('#playPrompt').evaluate(input => input.blur());
    await page.waitForTimeout(240);
    await resetPrototypeScroll();
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-truth-play-modal.png' });
    await page.locator('#actionCard').getByRole('button', { name: '发送邀请', exact: true }).click();
    const playMessage = page.locator('.chat-body .play-message').last();
    const playMessageText = await playMessage.textContent();

    await openDirectTool('大冒险');
    await page.getByRole('button', { name: '随机题目', exact: true }).click();
    const randomDarePrompt = await page.locator('#playPrompt').inputValue();
    await page.locator('#actionCard').getByRole('button', { name: '取消', exact: true }).click();

    await openDirectTool('摇骰子');
    const diceRollingObserved = await page.locator('#diceFace.rolling').count() === 1;
    await page.waitForFunction(() => {
      const send = document.getElementById('diceSend');
      return send && !send.disabled;
    });
    const firstDiceValue = Number(await page.locator('#diceFace').getAttribute('data-value'));
    const diceResultText = (await page.locator('#diceFace').textContent()).trim();
    await page.waitForFunction(() => !document.getElementById('toast').classList.contains('show') && getComputedStyle(document.getElementById('toast')).opacity === '0');
    await resetPrototypeScroll();
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-dice-result-modal.png' });
    await page.locator('#actionCard').getByRole('button', { name: '再摇一次', exact: true }).click();
    await page.waitForFunction(() => document.getElementById('diceFace').classList.contains('rolling'));
    await page.waitForFunction(() => !document.getElementById('diceSend').disabled);
    const secondDiceValue = Number(await page.locator('#diceFace').getAttribute('data-value'));
    const diceRollCount = Number(await page.locator('#diceFace').getAttribute('data-roll-count'));
    await page.locator('#actionCard').getByRole('button', { name: '发送', exact: true }).click();
    const sentDice = page.locator('.chat-body .dice-message .dice-face').last();
    const sentDiceValue = Number(await sentDice.getAttribute('data-value'));
    const diceBubbleText = (await page.locator('.chat-body .dice-message').last().textContent()).trim();

    await page.waitForFunction(() => !document.getElementById('toast').classList.contains('show') && getComputedStyle(document.getElementById('toast')).opacity === '0');
    await page.getByRole('button', { name: '语音', exact: true }).click();
    const directHold = page.locator('#chatVoiceHold');
    const directBox = await directHold.boundingBox();
    if (!directBox) throw new Error('单聊按住说话区域不可见');
    await page.mouse.move(directBox.x + directBox.width / 2, directBox.y + directBox.height / 2);
    await page.mouse.down();
    await page.waitForTimeout(720);
    const directRecordingState = await page.evaluate(() => ({
      shellRecording: document.getElementById('chatInputShell').classList.contains('recording'),
      feedbackOpacity: getComputedStyle(document.querySelector('#chatInputShell .voice-feedback')).opacity,
      duration: document.getElementById('chatVoiceDuration').textContent,
      holdText: document.getElementById('chatVoiceHold').textContent
    }));
    await resetPrototypeScroll();
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-direct-voice-waveform.png' });
    await page.mouse.up();
    await page.waitForFunction(() => document.querySelectorAll('.chat-body .voice-message').length > 0);
    const directVoiceDuration = await page.locator('.chat-body .voice-message time').last().textContent();

    await page.getByRole('region', { name: '个人聊天' }).getByLabel('返回').click();
    await page.locator('.quick-item').filter({ hasText: '邀请与申请' }).click();
    await page.locator('.notice-item[data-action="invite-room"]').click();
    await page.getByRole('button', { name: '接受邀请', exact: true }).click();
    await page.getByRole('region', { name: '通知列表' }).getByLabel('返回').click();
    await page.locator('#invitedRoomRow .row-content').click();
    await page.waitForFunction(() => getComputedStyle(document.getElementById('roomView')).transform === 'none');
    await page.waitForFunction(() => !document.getElementById('toast').classList.contains('show') && getComputedStyle(document.getElementById('toast')).opacity === '0');
    await page.getByRole('region', { name: '私密房间' }).getByRole('button', { name: '语音', exact: true }).click();
    const roomHold = page.locator('#roomVoiceHold');
    const roomBox = await roomHold.boundingBox();
    if (!roomBox) throw new Error('房间按住说话区域不可见');
    await page.mouse.move(roomBox.x + roomBox.width / 2, roomBox.y + roomBox.height / 2);
    await page.mouse.down();
    await page.waitForTimeout(720);
    const roomRecordingState = await page.evaluate(() => ({
      shellRecording: document.getElementById('roomInputShell').classList.contains('recording'),
      feedbackOpacity: getComputedStyle(document.querySelector('#roomInputShell .voice-feedback')).opacity,
      duration: document.getElementById('roomVoiceDuration').textContent,
      holdText: document.getElementById('roomVoiceHold').textContent
    }));
    await resetPrototypeScroll();
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-room-voice-waveform.png' });
    await page.mouse.up();
    await page.waitForFunction(() => document.querySelectorAll('#roomChat .voice-message').length > 0);
    const roomVoiceDuration = await page.locator('#roomChat .voice-message time').last().textContent();
    await page.getByRole('region', { name: '私密房间' }).getByLabel('更多功能').click();
    await page.waitForFunction(() => document.getElementById('roomTools').classList.contains('open'));
    const roomToolLabels = await page.locator('#roomTools .room-tool span').allTextContents();

    const result = {
      playPromptLayout,
      randomTruthPrompt,
      playMessageText,
      randomDarePrompt,
      diceRollingObserved,
      firstDiceValue,
      secondDiceValue,
      diceRollCount,
      sentDiceValue,
      diceResultText,
      diceBubbleText,
      directRecordingState,
      directVoiceDuration,
      roomRecordingState,
      roomVoiceDuration,
      roomToolLabels,
      consoleErrors
    };
    const valid = result.playPromptLayout.randomInsideInput
      && result.playPromptLayout.randomTouchWidth >= 44
      && result.playPromptLayout.defaultMode === '普通'
      && result.randomTruthPrompt.length > 0
      && result.playMessageText.includes('真心话')
      && result.playMessageText.includes('私密')
      && result.playMessageText.includes('如果可以重新认识一个人')
      && result.playMessageText.includes('等待回应')
      && result.randomDarePrompt.length > 0
      && result.diceRollCount >= 2
      && result.firstDiceValue >= 1 && result.firstDiceValue <= 6
      && result.secondDiceValue >= 1 && result.secondDiceValue <= 6
      && result.sentDiceValue === result.secondDiceValue
      && result.diceResultText === ''
      && result.diceBubbleText === ''
      && result.directRecordingState.shellRecording
      && result.directRecordingState.feedbackOpacity === '1'
      && result.directRecordingState.holdText === '松开发送'
      && Number.parseFloat(result.directRecordingState.duration) >= 0.6
      && result.directVoiceDuration.endsWith('″')
      && result.roomRecordingState.shellRecording
      && result.roomRecordingState.feedbackOpacity === '1'
      && result.roomRecordingState.holdText === '松开发送'
      && Number.parseFloat(result.roomRecordingState.duration) >= 0.6
      && result.roomVoiceDuration.endsWith('″')
      && JSON.stringify(result.roomToolLabels) === JSON.stringify(['图片', '闪照', '视频'])
      && result.consoleErrors.length === 0;
    if (!valid) throw new Error(`玩法与语音检查失败：${JSON.stringify(result)}`);
    return result;
  }

  if (process.env.CHECK_SCOPE === 'composer-alignment') {
    await page.locator('.swipe-row[data-name="小雨"] .row-content').click();
    await page.waitForFunction(() => getComputedStyle(document.getElementById('chatView')).transform === 'none');
    const chatInputLayout = await page.evaluate(() => {
      const shell = document.querySelector('.chat-input-shell');
      const mic = document.getElementById('micButton');
      const input = document.getElementById('chatInput');
      const send = document.getElementById('chatSendButton');
      const more = document.getElementById('chatMoreButton');
      const shellRect = shell.getBoundingClientRect();
      const micRect = mic.getBoundingClientRect();
      const inputRect = input.getBoundingClientRect();
      return {
        micInsideShell: mic.parentElement === shell,
        micWithinInput: micRect.left >= inputRect.left && micRect.right <= inputRect.right,
        micTouchWidth: micRect.width,
        order: inputRect.left < send.getBoundingClientRect().left && send.getBoundingClientRect().left < more.getBoundingClientRect().left,
        shellWidth: shellRect.width,
        screenX: document.querySelector('.screen').getBoundingClientRect().x
      };
    });
    await page.getByRole('button', { name: '语音', exact: true }).click();
    const voiceState = {
      active: await page.locator('#micButton.active').count() === 1,
      inputValue: await page.locator('#chatInput').inputValue(),
      readOnly: await page.locator('#chatInput').getAttribute('readonly') !== null,
      holdVisible: await page.locator('#chatVoiceHold').evaluate(hold => getComputedStyle(hold).display !== 'none'),
      holdText: await page.locator('#chatVoiceHold').textContent()
    };
    await page.getByRole('button', { name: '语音', exact: true }).click();
    const textState = {
      active: await page.locator('#micButton.active').count() === 1,
      inputValue: await page.locator('#chatInput').inputValue(),
      readOnly: await page.locator('#chatInput').getAttribute('readonly') !== null
    };
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-chat-inline-mic.png' });

    await page.getByRole('region', { name: '个人聊天' }).getByLabel('返回').click();
    await page.waitForFunction(() => !document.getElementById('chatView').classList.contains('open'));
    await page.locator('.quick-item').filter({ hasText: '邀请与申请' }).click();
    await page.locator('.notice-item[data-action="invite-room"]').click();
    await page.getByRole('button', { name: '接受邀请', exact: true }).click();
    await page.getByRole('region', { name: '通知列表' }).getByLabel('返回').click();
    await page.locator('#invitedRoomRow .row-content').click();
    await page.waitForFunction(() => getComputedStyle(document.getElementById('roomView')).transform === 'none');
    const roomToolsHiddenInitially = await page.locator('#roomTools.open').count() === 0;
    const roomComposerOrder = await page.evaluate(() => {
      const input = document.getElementById('roomInput').getBoundingClientRect();
      const send = document.getElementById('roomSend').getBoundingClientRect();
      const more = document.getElementById('roomMediaButton').getBoundingClientRect();
      return {
        correct: input.left < send.left && send.left < more.left,
        moreWidth: more.width
      };
    });
    await page.getByRole('region', { name: '私密房间' }).getByLabel('更多功能').click();
    await page.waitForFunction(() => {
      const view = document.getElementById('roomView');
      const composer = document.getElementById('roomComposer').getBoundingClientRect();
      const tools = document.getElementById('roomTools').getBoundingClientRect();
      const viewRect = view.getBoundingClientRect();
      return view.classList.contains('tools-open')
        && Math.abs(composer.bottom - tools.top) < 1
        && Math.abs(tools.bottom - viewRect.bottom) < 1;
    });
    await page.waitForFunction(() => getComputedStyle(document.getElementById('toast')).opacity === '0');
    const roomToolLabels = await page.locator('#roomTools .room-tool span').allTextContents();
    const roomToolsLayout = await page.locator('#roomTools').evaluate(tools => {
      const style = getComputedStyle(tools);
      const rect = tools.getBoundingClientRect();
      return {
        height: rect.height,
        columns: style.gridTemplateColumns.split(' ').filter(Boolean).length,
        screenX: document.querySelector('.screen').getBoundingClientRect().x,
        actionCardOpen: document.getElementById('actionCard').classList.contains('open')
      };
    });
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-room-media-tools.png' });
    await page.locator('#roomTools').getByRole('button', { name: '图片', exact: true }).click();
    const roomToolsClosedAfterChoice = await page.locator('#roomTools.open').count() === 0;
    const roomChoiceToast = await page.locator('#toast').textContent();
    await page.getByRole('region', { name: '私密房间' }).getByLabel('返回').click();

    await page.locator('.quick-item').filter({ hasText: '互动通知' }).click();
    await page.locator('.notice-item[data-action="bottle-reply"]').click();
    const rainGroup = page.locator('[data-thread-id="thread-rain"]');
    await rainGroup.getByRole('button', { name: '回复', exact: true }).click();
    await page.waitForFunction(() => {
      const view = document.getElementById('bottleView').getBoundingClientRect();
      const keyboard = document.getElementById('prototypeKeyboard').getBoundingClientRect();
      return Math.abs(keyboard.bottom - view.bottom) < 1;
    });
    await page.waitForFunction(() => getComputedStyle(document.getElementById('toast')).opacity === '0');
    const keyboardState = await page.evaluate(() => {
      const keyboard = document.getElementById('prototypeKeyboard');
      return {
        nineKeyCount: keyboard.querySelectorAll('.nine-key').length,
        labels: [...keyboard.querySelectorAll('.nine-key')].map(key => key.getAttribute('aria-label')),
        forbiddenSuggestions: ['慢慢说', '我在听', '抱抱你'].filter(text => keyboard.textContent.includes(text)),
        qwertyKeyCount: keyboard.querySelectorAll('.keyboard-key').length,
        inputFocused: document.activeElement === document.getElementById('bottleReplyInput')
      };
    });
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-nine-grid-keyboard.png' });
    await page.locator('#bottleReplyInput').fill('测试九宫格收起');
    await page.locator('#bottleComposer .send-reply').click();
    await page.waitForTimeout(300);
    const keyboardClosedAfterSend = await page.locator('#bottleView.keyboard-open').count() === 0
      && await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).visibility) === 'hidden';

    const result = {
      chatInputLayout,
      voiceState,
      textState,
      roomToolsHiddenInitially,
      roomComposerOrder,
      roomToolLabels,
      roomToolsLayout,
      roomToolsClosedAfterChoice,
      roomChoiceToast,
      keyboardState,
      keyboardClosedAfterSend,
      consoleErrors
    };
    const valid = result.chatInputLayout.micInsideShell
      && result.chatInputLayout.micWithinInput
      && result.chatInputLayout.micTouchWidth >= 44
      && result.chatInputLayout.order
      && result.chatInputLayout.screenX === 0
      && result.voiceState.active
      && result.voiceState.inputValue === ''
      && result.voiceState.readOnly
      && result.voiceState.holdVisible
      && result.voiceState.holdText === '按住说话'
      && result.textState.active === false
      && result.textState.inputValue === ''
      && result.textState.readOnly === false
      && result.roomToolsHiddenInitially
      && result.roomComposerOrder.correct
      && result.roomComposerOrder.moreWidth >= 44
      && JSON.stringify(result.roomToolLabels) === JSON.stringify(['图片', '闪照', '视频'])
      && result.roomToolsLayout.height === 112
      && result.roomToolsLayout.columns === 3
      && result.roomToolsLayout.screenX === 0
      && result.roomToolsLayout.actionCardOpen === false
      && result.roomToolsClosedAfterChoice
      && result.roomChoiceToast === '选择图片'
      && result.keyboardState.nineKeyCount === 9
      && result.keyboardState.labels[1] === '2 ABC'
      && result.keyboardState.labels[8] === '9 WXYZ'
      && result.keyboardState.forbiddenSuggestions.length === 0
      && result.keyboardState.qwertyKeyCount === 0
      && result.keyboardState.inputFocused
      && result.keyboardClosedAfterSend
      && result.consoleErrors.length === 0;
    if (!valid) throw new Error(`输入栏对齐检查失败：${JSON.stringify(result)}`);
    return result;
  }

  if (process.env.CHECK_SCOPE === 'approved-scope') {
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
    await page.locator('.swipe-row[data-name="小雨"] .row-content').click();
    await page.waitForFunction(() => getComputedStyle(document.getElementById('chatView')).transform === 'none');
    const toolsHiddenInitially = await page.locator('#chatTools.open').count() === 0;
    await page.getByRole('button', { name: '更多功能', exact: true }).click();
    const toolPanel = page.locator('#chatTools');
    await page.waitForFunction(() => {
      const chat = document.getElementById('chatView');
      const tools = document.getElementById('chatTools');
      return getComputedStyle(chat).transform === 'none'
        && getComputedStyle(tools).transform === 'none';
    });
    const toolLayout = await toolPanel.evaluate(panel => {
      const style = getComputedStyle(panel);
      return {
        height: panel.getBoundingClientRect().height,
        columns: style.gridTemplateColumns.split(' ').filter(Boolean).length,
        rows: style.gridTemplateRows.split(' ').filter(Boolean).length
      };
    });
    const toolLabels = await toolPanel.locator('.tool span').allTextContents();
    const toolActions = await toolPanel.locator('.tool').evaluateAll(buttons => buttons.map(button => button.getAttribute('onclick')));
    const toolGroupHeadingCount = await toolPanel.locator('.tool-group-label').count();
    const toolGeometry = await page.evaluate(() => {
      const snapshot = element => {
        const rect = element.getBoundingClientRect();
        const style = getComputedStyle(element);
        return { x: rect.x, width: rect.width, transform: style.transform, opacity: style.opacity };
      };
      return {
        phone: snapshot(document.querySelector('.phone')),
        screen: snapshot(document.querySelector('.screen')),
        chat: snapshot(document.getElementById('chatView'))
      };
    });
    await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-chat-tools.png' });

    await page.getByRole('region', { name: '个人聊天' }).getByLabel('返回').click();
    await page.locator('.quick-item').filter({ hasText: '互动通知' }).click();
    await page.locator('.notice-item[data-action="bottle-reply"]').click();
    const rainGroup = page.locator('[data-thread-id="thread-rain"]');
    await rainGroup.getByRole('button', { name: '回复', exact: true }).click();
    await page.waitForFunction(() => {
      const view = document.getElementById('bottleView');
      const composer = document.getElementById('bottleComposer');
      const keyboard = document.getElementById('prototypeKeyboard');
      if (!view || !composer || !keyboard) return false;
      const keyboardRect = keyboard.getBoundingClientRect();
      const composerRect = composer.getBoundingClientRect();
      const viewRect = view.getBoundingClientRect();
      return Math.abs(keyboardRect.bottom - viewRect.bottom) < 1
        && Math.abs(composerRect.bottom - keyboardRect.top) < 1;
    });
    const keyboardState = await page.evaluate(() => {
      const view = document.getElementById('bottleView');
      const body = document.getElementById('bottleBody');
      const composer = document.getElementById('bottleComposer');
      const keyboard = document.getElementById('prototypeKeyboard');
      const input = document.getElementById('bottleReplyInput');
      const bodyRect = body.getBoundingClientRect();
      const composerRect = composer.getBoundingClientRect();
      const keyboardRect = keyboard.getBoundingClientRect();
      return {
        replying: view.classList.contains('replying'),
        keyboardOpen: view.classList.contains('keyboard-open'),
        inputFocused: document.activeElement === input,
        keyboardVisible: keyboardRect.top < view.getBoundingClientRect().bottom,
        composerTouchesKeyboard: Math.abs(composerRect.bottom - keyboardRect.top) < 1,
        bodyAboveComposer: bodyRect.bottom <= composerRect.top + 1,
        bodyBottom: bodyRect.bottom,
        composerTop: composerRect.top,
        outerScroll: { x: window.scrollX, y: window.scrollY }
      };
    });
    await page.locator('.phone').screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/approved-bottle-keyboard-open.png' });
    await page.locator('#bottleReplyInput').fill('测试标准键盘收起');
    await page.locator('#bottleComposer .send-reply').click();
    await page.waitForTimeout(300);
    const afterSend = await page.evaluate(() => {
      const view = document.getElementById('bottleView');
      const body = document.getElementById('bottleBody');
      const composer = document.getElementById('bottleComposer');
      const keyboard = document.getElementById('prototypeKeyboard');
      return {
        replying: view.classList.contains('replying'),
        keyboardOpen: view.classList.contains('keyboard-open'),
        composerVisibility: getComputedStyle(composer).visibility,
        keyboardTop: keyboard.getBoundingClientRect().top,
        viewBottom: view.getBoundingClientRect().bottom,
        bodyBottomPadding: parseFloat(getComputedStyle(body).paddingBottom),
        outerScroll: { x: window.scrollX, y: window.scrollY }
      };
    });
    const newReplyVisible = await rainGroup.locator('.thread-message.mine').last().evaluate(message => {
      const bodyRect = document.getElementById('bottleBody').getBoundingClientRect();
      const messageRect = message.getBoundingClientRect();
      return messageRect.top >= bodyRect.top && messageRect.bottom <= bodyRect.bottom;
    });

    const result = {
      toolsHiddenInitially,
      toolGroupHeadingCount,
      toolLabels,
      toolActions,
      toolLayout,
      toolGeometry,
      keyboardState,
      afterSend,
      newReplyVisible,
      consoleErrors
    };
    const valid = result.toolsHiddenInitially
      && result.toolGroupHeadingCount === 0
      && JSON.stringify(result.toolLabels) === JSON.stringify(expectedLabels)
      && JSON.stringify(result.toolActions) === JSON.stringify(expectedActions)
      && result.toolLayout.height === 184
      && result.toolLayout.columns === 4
      && result.toolLayout.rows === 2
      && result.toolGeometry.screen.x === 0
      && result.toolGeometry.chat.x === 0
      && result.keyboardState.replying
      && result.keyboardState.keyboardOpen
      && result.keyboardState.inputFocused
      && result.keyboardState.keyboardVisible
      && result.keyboardState.composerTouchesKeyboard
      && result.keyboardState.bodyAboveComposer
      && result.keyboardState.outerScroll.x === 0
      && result.keyboardState.outerScroll.y === 0
      && result.afterSend.replying === false
      && result.afterSend.keyboardOpen === false
      && result.afterSend.composerVisibility === 'hidden'
      && result.afterSend.keyboardTop >= result.afterSend.viewBottom
      && result.afterSend.bodyBottomPadding === 28
      && result.afterSend.outerScroll.x === 0
      && result.afterSend.outerScroll.y === 0
      && result.newReplyVisible
      && result.consoleErrors.length === 0;
    if (!valid) throw new Error(`批准范围检查失败：${JSON.stringify(result)}`);
    return result;
  }

  if (process.env.CHECK_SCOPE === 'reply-collapse') {
    await page.locator('.quick-item').filter({ hasText: '互动通知' }).click();
    await page.locator('.notice-item[data-action="bottle-reply"]').click();
    const rainGroup = page.locator('[data-thread-id="thread-rain"]');
    const closeReplyButtonCount = await page.locator('#bottleComposer .close-reply').count();
    await rainGroup.getByRole('button', { name: '回复', exact: true }).click();
    await page.locator('#bottleReplyInput').fill('测试收起输入框');
    await page.locator('#bottleComposer .send-reply').click();
    await page.waitForTimeout(300);
    const result = {
      closeReplyButtonCount,
      composerOpenAfterSend: await page.locator('#bottleView.replying').count(),
      composerVisibilityAfterSend: await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).visibility),
      composerOpacityAfterSend: await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).opacity),
      composerPointerEventsAfterSend: await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).pointerEvents),
      bottleViewOverflowAfterSend: await page.locator('#bottleView').evaluate(view => getComputedStyle(view).overflow),
      replyInputFocusedAfterSend: await page.locator('#bottleReplyInput').evaluate(input => document.activeElement === input),
      bottleBodyBottomPaddingAfterSend: await page.locator('#bottleBody').evaluate(body => parseFloat(getComputedStyle(body).paddingBottom)),
      newReplyVisibleAfterSend: await rainGroup.locator('.thread-message.mine').last().evaluate(message => {
        const body = document.getElementById('bottleBody');
        const bodyRect = body.getBoundingClientRect();
        const messageRect = message.getBoundingClientRect();
        return messageRect.top >= bodyRect.top && messageRect.bottom <= bodyRect.bottom;
      }),
      outerScroll: await page.evaluate(() => ({ x: window.scrollX, y: window.scrollY })),
      consoleErrors
    };
    const valid = result.closeReplyButtonCount === 0
      && result.composerOpenAfterSend === 0
      && result.composerVisibilityAfterSend === 'hidden'
      && result.composerOpacityAfterSend === '0'
      && result.composerPointerEventsAfterSend === 'none'
      && result.bottleViewOverflowAfterSend === 'hidden'
      && result.replyInputFocusedAfterSend === false
      && result.bottleBodyBottomPaddingAfterSend === 28
      && result.newReplyVisibleAfterSend === true
      && result.outerScroll.x === 0
      && result.outerScroll.y === 0
      && result.consoleErrors.length === 0;
    if (!valid) throw new Error(`回复收起检查失败：${JSON.stringify(result)}`);
    return result;
  }

  const invitedRoomVisibleBeforeAccept = await page.locator('#invitedRoomRow:visible').count();

  await page.locator('.swipe-row[data-name="小雨"] .row-content').click();
  await page.getByRole('button', { name: '聊天设置', exact: true }).click();
  const flatLabels = await page.locator('#chatSettingsView .flat-setting-row').allTextContents();
  const groupHeadings = await page.locator('#chatSettingsView .settings-section-title').count();

  await page.evaluate(() => {
    const state = directConversations.get('小雨');
    state.unread = 2;
    updateDirectRow('小雨');
  });
  await page.getByRole('button', { name: '消息免打扰', exact: true }).click();
  const muteIndicatorVisible = await page.locator('.swipe-row[data-name="小雨"] .mute-indicator').count();
  const muteIndicatorLabel = await page.locator('.swipe-row[data-name="小雨"] .mute-indicator').getAttribute('aria-label');
  const unreadAfterMute = await page.locator('.swipe-row[data-name="小雨"] .unread').textContent();
  await page.getByRole('button', { name: '消息免打扰', exact: true }).click();
  const muteIndicatorAfterDisable = await page.locator('.swipe-row[data-name="小雨"] .mute-indicator').count();
  await page.getByRole('button', { name: '消息免打扰', exact: true }).click();

  const confirmations = [];
  for (const label of ['清空聊天记录', '删除会话', '拉黑用户']) {
    await page.getByRole('button', { name: new RegExp(label) }).click();
    confirmations.push(await page.locator('#dialogTitle').textContent());
    await page.getByRole('button', { name: '取消', exact: true }).click();
  }

  await page.getByRole('button', { name: '返回聊天', exact: true }).click();
  await page.getByRole('region', { name: '个人聊天' }).getByLabel('返回').click();
  await page.waitForTimeout(350);
  await page.locator('.phone').screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/message-mute-indicator-final.png' });
  await page.locator('.quick-item').filter({ hasText: '互动通知' }).click();
  await page.locator('.notice-item[data-action="bottle-reply"]').click();
  await page.waitForTimeout(50);
  const bottleOpen = await page.locator('#bottleView.open').count();
  const chatOpenFromBottle = await page.locator('#chatView.open').count();
  const targetHighlighted = await page.locator('[data-reply-id="reply-rain"].targeted').count();
  const rainGroup = page.locator('[data-thread-id="thread-rain"]');
  const unreadVisibleInitially = await rainGroup.locator('.reply-unread-dot:not([hidden])').count();
  const rainMessagesBefore = await rainGroup.locator('.thread-message').count();
  const ownerRepliesBefore = await rainGroup.locator('.thread-message.mine').count();
  const closeReplyButtonCount = await page.locator('#bottleComposer .close-reply').count();
  const outerScroll = await page.evaluate(() => ({ x: window.scrollX, y: window.scrollY }));
  await page.screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/bottle-reply-threads-final.png' });
  await page.waitForTimeout(1300);
  const unreadVisibleAfterView = await rainGroup.locator('.reply-unread-dot:not([hidden])').count();
  const replyActionLabels = await page.locator('.reply-thread-action').allTextContents();
  await rainGroup.getByRole('button', { name: '回复', exact: true }).click();
  const composerOpen = await page.locator('#bottleView.replying').count();
  const replyPlaceholder = await page.locator('#bottleReplyInput').getAttribute('placeholder');
  await page.locator('#bottleReplyInput').fill('我现在好一点了，谢谢你。');
  await page.locator('#bottleComposer .send-reply').click();
  const replySuccessText = await page.locator('#toast').textContent();
  await page.waitForTimeout(300);
  const composerOpenAfterSend = await page.locator('#bottleView.replying').count();
  const composerVisibilityAfterSend = await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).visibility);
  const composerOpacityAfterSend = await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).opacity);
  const composerPointerEventsAfterSend = await page.locator('#bottleComposer').evaluate(composer => getComputedStyle(composer).pointerEvents);
  const bottleViewOverflowAfterSend = await page.locator('#bottleView').evaluate(view => getComputedStyle(view).overflow);
  const replyInputFocusedAfterSend = await page.locator('#bottleReplyInput').evaluate(input => document.activeElement === input);
  const bottleBodyBottomPaddingAfterSend = await page.locator('#bottleBody').evaluate(body => parseFloat(getComputedStyle(body).paddingBottom));
  const newReplyVisibleAfterSend = await rainGroup.locator('.thread-message.mine').last().evaluate(message => {
    const body = document.getElementById('bottleBody');
    const bodyRect = body.getBoundingClientRect();
    const messageRect = message.getBoundingClientRect();
    return messageRect.top >= bodyRect.top && messageRect.bottom <= bodyRect.bottom;
  });
  const rainMessagesAfter = await rainGroup.locator('.thread-message').count();
  const ownerRepliesAfter = await rainGroup.locator('.thread-message.mine').count();
  const echoMessagesAfter = await page.locator('[data-thread-id="thread-echo"] .thread-message').count();
  const replyInputAfterSend = await page.locator('#bottleReplyInput').inputValue();

  await page.getByLabel('返回互动通知').click();
  await page.locator('.notice-item[data-action="bottle-reply"]').click();
  await page.waitForTimeout(50);
  const unreadVisibleAfterReopen = await page.locator('[data-thread-id="thread-rain"] .reply-unread-dot:not([hidden])').count();
  await page.getByLabel('返回互动通知').click();
  await page.getByRole('region', { name: '通知列表' }).getByLabel('返回').click();
  await page.locator('.quick-item').filter({ hasText: '邀请与申请' }).click();
  await page.waitForTimeout(300);
  await page.locator('.notice-item[data-action="invite-room"]').click();
  await page.getByRole('button', { name: '接受邀请', exact: true }).click();
  const invitedRoomVisibleAfterAccept = await page.locator('#invitedRoomRow:visible').count();
  const invitedRoomRows = await page.locator('#list .swipe-row[data-name="深夜故事"]').count();
  const firstVisibleConversationId = await page.locator('#list .swipe-row:visible').first().getAttribute('id');
  const inviteNoticeAfterAccept = await page.locator('.notice-item[data-action="invite-room"]').count();

  await page.getByRole('region', { name: '通知列表' }).getByLabel('返回').click();
  await page.locator('.phone').screenshot({ path: 'E:/ai_project/漂流瓶项目/.superpowers/brainstorm/267-1784168255/content/room-accepted-list-final.png' });
  await page.locator('#invitedRoomRow .row-content').click();
  const acceptedRoomOpen = await page.locator('#roomView.open').count();
  const acceptedRoomTitle = await page.locator('#roomTitle').textContent();
  await page.getByRole('region', { name: '私密房间' }).getByLabel('返回').click();
  await page.locator('.quick-item').filter({ hasText: '邀请与申请' }).click();
  await page.waitForTimeout(300);

  await page.locator('.notice-swipe-row .notice-item').first().click();
  const decisionOpenedOnTap = await page.locator('#actionCard.open').count();
  await page.locator('#actionMask').click({ position: { x: 5, y: 5 } });
  const firstRow = page.locator('.notice-swipe-row').first();
  const firstContent = firstRow.locator('.notice-item');
  const box = await firstContent.boundingBox();
  if (!box) throw new Error('邀请通知不可见');
  await page.mouse.move(box.x + box.width - 20, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width - 120, box.y + box.height / 2, { steps: 6 });
  await page.mouse.up();
  await page.waitForTimeout(300);
  const swipeOffset = Number(await firstRow.getAttribute('data-offset'));
  await firstRow.locator('.notice-delete').click();
  await page.waitForTimeout(300);
  const invitationRowsAfterDelete = await page.locator('.notice-swipe-row').count();
  const decisionOpenedByDelete = await page.locator('#actionCard.open').count();

  await page.reload();
  await page.locator('.quick-item').filter({ hasText: '邀请与申请' }).click();
  await page.locator('.notice-item[data-action="invite-room"]').click();
  await page.getByRole('button', { name: '拒绝', exact: true }).click();
  const invitedRoomVisibleAfterReject = await page.locator('#invitedRoomRow:visible').count();
  const inviteNoticeAfterReject = await page.locator('.notice-item[data-action="invite-room"]').count();

  const result = {
    flatLabels: flatLabels.map(value => value.replace('›', '').trim()),
    groupHeadings,
    invitedRoomVisibleBeforeAccept,
    muteIndicatorVisible,
    muteIndicatorLabel,
    unreadAfterMute,
    muteIndicatorAfterDisable,
    confirmations,
    bottleOpen,
    chatOpenFromBottle,
    targetHighlighted,
    unreadVisibleInitially,
    unreadVisibleAfterView,
    replyActionLabels,
    closeReplyButtonCount,
    rainMessagesBefore,
    rainMessagesAfter,
    ownerRepliesBefore,
    ownerRepliesAfter,
    echoMessagesAfter,
    composerOpen,
    replyPlaceholder,
    replySuccessText,
    composerOpenAfterSend,
    composerVisibilityAfterSend,
    composerOpacityAfterSend,
    composerPointerEventsAfterSend,
    bottleViewOverflowAfterSend,
    replyInputFocusedAfterSend,
    bottleBodyBottomPaddingAfterSend,
    newReplyVisibleAfterSend,
    replyInputAfterSend,
    unreadVisibleAfterReopen,
    outerScroll,
    swipeOffset,
    invitedRoomVisibleAfterAccept,
    invitedRoomRows,
    firstVisibleConversationId,
    inviteNoticeAfterAccept,
    acceptedRoomOpen,
    acceptedRoomTitle,
    invitationRowsAfterDelete,
    decisionOpenedByDelete,
    decisionOpenedOnTap,
    invitedRoomVisibleAfterReject,
    inviteNoticeAfterReject,
    consoleErrors
  };

  const valid = result.flatLabels.length === 5
    && result.groupHeadings === 0
    && result.invitedRoomVisibleBeforeAccept === 0
    && result.muteIndicatorVisible === 1
    && result.muteIndicatorLabel === '消息免打扰已开启'
    && result.unreadAfterMute === '2'
    && result.muteIndicatorAfterDisable === 0
    && result.confirmations.every(Boolean)
    && result.bottleOpen === 1
    && result.chatOpenFromBottle === 0
    && result.targetHighlighted === 1
    && result.unreadVisibleInitially === 1
    && result.unreadVisibleAfterView === 0
    && result.replyActionLabels.length === 4
    && result.replyActionLabels.every(label => label.trim() === '回复')
    && result.closeReplyButtonCount === 0
    && result.rainMessagesBefore === 2
    && result.rainMessagesAfter === 3
    && result.ownerRepliesBefore === 1
    && result.ownerRepliesAfter === 2
    && result.echoMessagesAfter === 0
    && result.composerOpen === 1
    && result.replyPlaceholder === '写下回复…'
    && result.replySuccessText === '已回复'
    && result.composerOpenAfterSend === 0
    && result.composerVisibilityAfterSend === 'hidden'
    && result.composerOpacityAfterSend === '0'
    && result.composerPointerEventsAfterSend === 'none'
    && result.bottleViewOverflowAfterSend === 'hidden'
    && result.replyInputFocusedAfterSend === false
    && result.bottleBodyBottomPaddingAfterSend === 28
    && result.newReplyVisibleAfterSend === true
    && result.replyInputAfterSend === ''
    && result.unreadVisibleAfterReopen === 0
    && result.outerScroll.x === 0
    && result.outerScroll.y === 0
    && result.swipeOffset === -76
    && result.invitedRoomVisibleAfterAccept === 1
    && result.invitedRoomRows === 1
    && result.firstVisibleConversationId === 'invitedRoomRow'
    && result.inviteNoticeAfterAccept === 0
    && result.acceptedRoomOpen === 1
    && result.acceptedRoomTitle === '深夜故事'
    && result.invitationRowsAfterDelete === 0
    && result.decisionOpenedByDelete === 0
    && result.decisionOpenedOnTap === 1
    && result.invitedRoomVisibleAfterReject === 0
    && result.inviteNoticeAfterReject === 0
    && result.consoleErrors.length === 0;

  if (!valid) throw new Error(`交互检查失败：${JSON.stringify(result)}`);
  return result;
};

const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.PLAYWRIGHT_CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
});
const page = await browser.newPage();
page.setDefaultTimeout(5000);
page.setDefaultNavigationTimeout(15000);
try {
  console.log(JSON.stringify(await runCheck(page), null, 2));
} catch (error) {
  console.error(error.stack || error);
  process.exitCode = 1;
} finally {
  await browser.close();
}
