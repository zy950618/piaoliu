const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');

const htmlPath = path.join(__dirname, 'chat-message-room-v2.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const runtimeErrors = [];
const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  url: 'http://127.0.0.1/chat-message-room-v2.html',
  beforeParse(window) {
    window.matchMedia = () => ({ matches: true, addListener() {}, removeListener() {} });
    window.scrollTo = () => {};
    window.HTMLElement.prototype.scrollTo = function scrollTo(options) {
      this.scrollTop = typeof options === 'object' ? options.top || 0 : 0;
    };
  }
});

dom.window.addEventListener('error', event => runtimeErrors.push(event.error?.message || event.message));

(async () => {
  await new Promise(resolve => setTimeout(resolve, 20));
  const { document } = dom.window;
  dom.window.openBottleReply('bottle-night-001', 'reply-rain');
  await new Promise(resolve => setTimeout(resolve, 20));

  const rainGroup = document.querySelector('[data-thread-id="thread-rain"]');
  const echoGroup = document.querySelector('[data-thread-id="thread-echo"]');
  const closeReplyButtonCount = document.querySelectorAll('#bottleComposer .close-reply').length;
  const rainMessagesBefore = rainGroup.querySelectorAll('.thread-message').length;
  const echoMessagesBefore = echoGroup.querySelectorAll('.thread-message').length;

  rainGroup.querySelector('.reply-thread-action').click();
  await new Promise(resolve => setTimeout(resolve, 20));
  const input = document.getElementById('bottleReplyInput');
  input.value = '测试收起输入框';
  dom.window.sendBottleThreadReply();
  await new Promise(resolve => setTimeout(resolve, 30));

  const result = {
    closeReplyButtonCount,
    composerOpenAfterSend: document.getElementById('bottleView').classList.contains('replying'),
    composerVisibilityAfterSend: dom.window.getComputedStyle(document.getElementById('bottleComposer')).visibility,
    composerOpacityAfterSend: dom.window.getComputedStyle(document.getElementById('bottleComposer')).opacity,
    composerPointerEventsAfterSend: dom.window.getComputedStyle(document.getElementById('bottleComposer')).pointerEvents,
    bottleViewOverflowAfterSend: dom.window.getComputedStyle(document.getElementById('bottleView')).overflow,
    replyInputFocusedAfterSend: document.activeElement === input,
    bottleBodyBottomPaddingAfterSend: parseFloat(dom.window.getComputedStyle(document.getElementById('bottleBody')).paddingBottom),
    replyInputAfterSend: input.value,
    rainMessagesBefore,
    rainMessagesAfter: rainGroup.querySelectorAll('.thread-message').length,
    echoMessagesBefore,
    echoMessagesAfter: echoGroup.querySelectorAll('.thread-message').length,
    runtimeErrors
  };

  const valid = result.closeReplyButtonCount === 0
    && result.composerOpenAfterSend === false
    && result.composerVisibilityAfterSend === 'hidden'
    && result.composerOpacityAfterSend === '0'
    && result.composerPointerEventsAfterSend === 'none'
    && result.bottleViewOverflowAfterSend === 'hidden'
    && result.replyInputFocusedAfterSend === false
    && result.bottleBodyBottomPaddingAfterSend === 28
    && result.replyInputAfterSend === ''
    && result.rainMessagesAfter === result.rainMessagesBefore + 1
    && result.echoMessagesAfter === result.echoMessagesBefore
    && result.runtimeErrors.length === 0;

  console.log(JSON.stringify(result, null, 2));
  if (!valid) throw new Error('回复输入框 DOM 检查失败');
  dom.window.close();
})().catch(error => {
  console.error(error.stack || error);
  dom.window.close();
  process.exitCode = 1;
});
