<template>
  <view class="page chat-page safe-bottom">
    <view v-if="contextConversationId" class="panel chat-panel">
      <view class="chat-head">
        <view class="chat-user-head">
          <view class="thread-avatar context-avatar" />
          <view class="chat-title-main">
            <text class="h2">临时会话</text>
            <text class="muted">{{ contextStatusText }}</text>
          </view>
          <view class="online-chip">
            <text class="online-dot" />
            <text>{{ contextConversation?.status || 'loading' }}</text>
          </view>
        </view>
      </view>

      <view v-if="contextConversation" class="source-card">
        <text class="source-kicker">{{ contextSourceTitle }}</text>
        <text class="source-text">{{ contextSourceText }}</text>
      </view>

      <view class="message-list">
        <view v-if="!contextConversation?.messages.length" class="context-empty">
          <text>会话已开启，可以基于本次互动继续聊。</text>
        </view>
        <view
          v-for="message in contextConversation?.messages || []"
          :key="message.id"
          class="chat-line"
          :class="{ me: message.senderId === contextCurrentUserId }"
        >
          <text class="chat-name">{{ message.senderId === contextCurrentUserId ? '我' : '对方' }}</text>
          <view class="chat-bubble" :class="[message.contentType, { viewed: message.status === 'risk_pending' }]">
            <text>{{ message.content }}</text>
          </view>
        </view>
      </view>

      <view class="composer-shell">
        <view class="composer-row">
          <view class="plus-button disabled">
            <text />
          </view>
          <input v-model="draft" class="chat-input" maxlength="120" placeholder="基于本次互动继续聊" @tap.stop @click.stop />
          <view class="send-button" @tap="sendText">发送</view>
        </view>
      </view>
    </view>

    <view v-else-if="selectedThread" class="panel chat-panel">
      <view class="chat-head">
        <view class="chat-user-head direct-chat-head">
          <view class="chat-party self-party">
            <image class="thread-avatar image-avatar" :src="currentUserAvatarUrl" mode="aspectFill" />
            <view class="chat-title-main">
              <text class="party-label">我</text>
              <text class="party-name">{{ currentUserName }}</text>
            </view>
          </view>
          <view class="chat-link-mark" />
          <view class="chat-party peer-party">
            <image class="thread-avatar image-avatar" :src="threadAvatarUrl(selectedThread)" mode="aspectFill" />
            <view class="chat-title-main">
              <text class="party-label">{{ displayText(selectedThread.participantTag) }}</text>
              <text class="party-name">{{ selectedThread.participantName }}</text>
              <text class="muted">ID {{ participantDisplayId }}</text>
            </view>
          </view>
          <view class="online-chip">
            <text class="online-dot" />
            <text>在线</text>
          </view>
        </view>
      </view>

      <view class="source-card">
        <text class="source-kicker">互动来源</text>
        <text class="source-text">{{ displayText(selectedThread.bottlePreview) }}</text>
      </view>

      <view v-if="isSelectedThreadFrozen" class="freeze-card">
        <text class="freeze-title">聊天已冻结</text>
        <text class="freeze-text">{{ selectedThreadFrozenNotice }}</text>
        <textarea
          v-model="appealReason"
          class="appeal-input"
          maxlength="120"
          placeholder="补充申诉说明"
          @tap.stop
          @click.stop
        />
        <view class="freeze-action-row">
          <view class="freeze-link" :class="{ disabled: appealSubmitting || appealSubmitted }" @tap="submitFrozenAppeal">
            {{ appealButtonText }}
          </view>
        </view>
      </view>

      <view class="message-list" :class="{ 'message-list-expanded': activeTool === 'more' || activeTool === 'room' || activeTool === 'voice' }">
        <view
          v-for="turn in selectedThread.turns"
          :key="turn.id"
          class="chat-line"
          :class="{ me: turn.fromMe }"
        >
          <text class="chat-name">{{ turn.fromMe ? '我' : turn.senderName }}</text>
          <view class="chat-bubble" :class="[turn.type || 'text', { viewed: turn.flashViewed }]">
            <text v-if="!turn.type || turn.type === 'text'">{{ displayText(turn.body) }}</text>
            <text v-else-if="turn.type === 'image'">图片消息：{{ displayText(turn.body) }}</text>
            <text v-else-if="turn.type === 'voice'">语音 {{ turn.mediaDuration || 8 }}s：{{ displayText(turn.body) }}</text>
            <text v-else-if="turn.type === 'video'">视频消息：{{ displayText(turn.body) }}</text>
            <text v-else-if="turn.type === 'flash_image'" @tap="viewFlash(turn)">闪图：{{ turn.flashViewed ? '已查看' : '点击查看一次' }}</text>
            <text v-else-if="turn.type === 'flash_video'" @tap="viewFlash(turn)">闪视频：{{ turn.flashViewed ? '已查看' : '点击查看一次' }}</text>
            <view v-else-if="turn.type === 'gift'" class="gift-bubble">
              <GiftVisual class="gift-bubble-visual" :gift="turnGift(turn)" size="bubble" active />
              <text>{{ turn.giftName }} · {{ turn.giftPriceCoins }} 金币</text>
            </view>
            <view v-else-if="turn.type === 'game_room'" class="room-bubble">
              <text>{{ turn.body }}</text>
              <text class="room-id">{{ turn.gameRoomId }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-if="!isSelectedThreadFrozen" class="composer-shell" @tap.stop @click.stop>
        <view class="composer-row">
          <view class="voice-button" :class="{ open: activeTool === 'voice' }" @tap="toggleVoiceMode">
            <text />
          </view>
          <input
            v-model="draft"
            class="chat-input"
            maxlength="120"
            placeholder="输入聊天内容"
            @focus="closeTransientPanels"
            @tap.stop
            @click.stop
          />
          <view v-if="canSendText" class="send-button" @tap="sendText">发送</view>
          <view v-else class="plus-button" :class="{ open: activeTool === 'more' || activeTool === 'room' }" @tap="toggleMorePanel">
            <text />
          </view>
        </view>

        <view v-if="activeTool === 'voice'" class="voice-capture-panel">
          <view class="voice-capture-icon" />
          <text>按住说话，松开发送</text>
        </view>

        <view v-if="activeTool === 'more' || activeTool === 'room'" class="composer-panels">
          <view v-if="activeTool === 'more'" class="tool-panel">
            <view class="tool-grid">
              <view class="tool-chip image-tool" @tap="sendMedia('image')">
                <view class="tool-glyph image-glyph" />
                <text class="tool-name">图片</text>
              </view>
              <view class="tool-chip voice-tool" @tap="sendMedia('voice')">
                <view class="tool-glyph voice-glyph" />
                <text class="tool-name">语音</text>
              </view>
              <view class="tool-chip video-tool" @tap="sendMedia('video')">
                <view class="tool-glyph video-glyph" />
                <text class="tool-name">视频</text>
              </view>
              <view class="tool-chip gift-tool highlight" @tap="toggleGiftPanel">
                <view class="tool-glyph gift-glyph" />
                <text class="tool-name">礼物</text>
              </view>
              <view class="tool-chip flash-tool" @tap="sendMedia('flash_image')">
                <view class="tool-glyph flash-glyph" />
                <text class="tool-name">闪图</text>
              </view>
              <view class="tool-chip flash-video-tool" @tap="sendMedia('flash_video')">
                <view class="tool-glyph flash-glyph" />
                <text class="tool-name">闪视频</text>
              </view>
              <view class="tool-chip room-tool" @tap="activeTool = 'room'">
                <view class="tool-glyph room-glyph" />
                <text class="tool-name">房间</text>
              </view>
            </view>
          </view>

          <view v-if="activeTool === 'room'" class="room-panel">
            <view class="room-mode public" @tap="createRoom('truth')">
              <view class="room-mode-head">
                <text>公开房间</text>
                <text class="room-state">公开</text>
              </view>
              <view class="avatar-ring">
                <view class="room-avatar participant" />
                <view class="room-avatar self" />
              </view>
              <view class="room-presence">
                <text class="presence-bar strong" />
                <text class="presence-bar" />
                <text class="presence-bar soft" />
                <text>2 online</text>
              </view>
            </view>
            <view class="room-mode private" @tap="createRoom('dare')">
              <view class="room-mode-head">
                <text>私密房间</text>
                <text class="room-state">私密</text>
              </view>
              <view class="avatar-ring">
                <view class="room-avatar participant" />
                <view class="room-avatar self" />
              </view>
              <view class="room-presence">
                <text class="presence-bar strong" />
                <text class="presence-bar soft" />
                <text>2 online</text>
              </view>
            </view>
            <view class="room-mode temporary primary" @tap="createRoom('mixed')">
              <view class="room-mode-head">
                <text>临时房间</text>
                <text class="room-state">限时</text>
              </view>
              <view class="avatar-ring">
                <view class="room-avatar participant" />
                <view class="room-avatar self" />
              </view>
            <view class="room-countdown">15:00</view>
            </view>
            <text v-if="gameRoomContextStatus" class="room-context-status">{{ gameRoomContextStatus }}</text>
          </view>
        </view>

      </view>
      <view v-else class="composer-shell frozen-composer" @tap="submitFrozenAppeal">
        <text>{{ appealSubmitted ? '申诉已提交，等待后台处理' : '聊天已冻结，点击提交申诉' }}</text>
      </view>
    </view>

    <EmptyState v-else title="会话不存在" body="该聊天已结束或不可访问。" />

    <GiftSheet
      v-if="activeTool === 'gift' && selectedThread"
      :receiver-name="selectedThread.participantName"
      :wallet-balance="content.wallet?.rechargeCoins || 0"
      :gifts="content.gifts"
      :sending-gift-id="sendingGiftId"
      @close="activeTool = ''"
      @recharge="goWallet"
      @select="sendGift"
    />
    <GiftSplash :gift="celebrationGift" />
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import EmptyState from '@/components/EmptyState.vue'
import GiftVisual from '@/components/GiftVisual.vue'
import GiftSheet from '@/components/GiftSheet.vue'
import GiftSplash from '@/components/GiftSplash.vue'
import { navigateTo, showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import { resolveAvatarUrl } from '@/utils/avatar'
import type { ContextChatConversation, ConversationThread, ConversationTurn, GiftProduct } from '@/types/domain'

type MediaType = NonNullable<ConversationTurn['type']>
type RoomMode = 'truth' | 'dare' | 'mixed'

const content = useContentStore()
const app = useAppStore()
const threadId = ref('')
const contextConversationId = ref('')
const activeTool = ref<'' | 'more' | 'gift' | 'room' | 'voice'>('')
const draft = ref('')
const appealReason = ref('我认为本次聊天冻结存在误判，请复核上下文。')
const appealSubmitting = ref(false)
const appealSubmitted = ref(false)
const sendingGiftId = ref('')
const gameRoomContextStatus = ref('')
const celebrationGift = ref<GiftProduct>()
let giftTimer: ReturnType<typeof setTimeout> | undefined

const selectedThread = computed(() => content.conversationThreads.find((thread) => thread.id === threadId.value))
const participantDisplayId = computed(() => selectedThread.value?.participantUserId || '-')
const currentUserName = computed(() => app.user?.nickname || '我')
const currentUserAvatarUrl = computed(() => resolveAvatarUrl(app.user?.avatarUrl, app.user?.id || 'current-user'))
const isSelectedThreadFrozen = computed(() => selectedThread.value?.status === 'risk_frozen')
const selectedThreadFrozenNotice = computed(() => selectedThread.value?.frozenNotice || '该聊天已因举报处置被冻结。若你认为处理有误，可在客服入口提交申诉说明。')
const appealButtonText = computed(() => {
  if (appealSubmitted.value) return '申诉已提交'
  if (appealSubmitting.value) return '提交中'
  return '提交申诉'
})
const contextConversation = computed(() => content.currentContextConversation)
const contextCurrentUserId = computed(() => contextConversation.value?.participants[0] || '')
const canSendText = computed(() => Boolean(draft.value.trim()))
const contextStatusText = computed(() => {
  if (!contextConversation.value) return '正在加载临时会话'
  if (contextConversation.value.status === 'active') return '基于本次互动开启，仍受频控、举报、拉黑和审计保护'
  if (contextConversation.value.status === 'blocked') return '会话已被拉黑，不能继续发送'
  if (contextConversation.value.status === 'reported' || contextConversation.value.status === 'risk_frozen') return '会话已进入风控处理'
  if (contextConversation.value.status === 'expired') return '会话已过期'
  return '等待对方确认'
})
const contextSourceTitle = computed(() => contextConversation.value?.sourceSummary.title || '基于本次互动开启')
const contextSourceText = computed(() => {
  const conversation = contextConversation.value
  if (!conversation) return ''
  const sourceId = conversation.sourceSummary.source_id || conversation.sourceId || '-'
  return `${sourceTypeLabel(conversation.sourceType)} · ${sourceId}`
})

onLoad((query) => {
  threadId.value = String(query?.threadId || '')
  contextConversationId.value = String(query?.contextConversationId || '')
  void loadPage()
})

onUnload(() => {
  if (giftTimer) clearTimeout(giftTimer)
})

async function loadPage() {
  if (contextConversationId.value) {
    await Promise.all([app.hydrate(), content.loadContextConversation(contextConversationId.value)])
    return
  }
  await Promise.all([app.hydrate(), content.loadConversationThreads(), content.loadWallet()])
  if (threadId.value && !selectedThread.value) {
    await content.markConversationRead(threadId.value)
  }
}

function threadAvatarUrl(thread: ConversationThread) {
  return resolveAvatarUrl(thread.participantAvatarUrl, thread.participantUserId || thread.id)
}

function turnGift(turn: ConversationTurn): GiftProduct {
  return {
    id: turn.giftId || 'gift',
    name: turn.giftName || '礼物',
    priceCoins: turn.giftPriceCoins || 0,
    iconText: turn.giftIconText || '',
    category: ''
  }
}

async function sendText() {
  const text = draft.value.trim()
  if (contextConversationId.value) {
    if (!text || !contextConversation.value) return
    if (contextConversation.value.status !== 'active') {
      showToast('当前会话暂不能发送')
      return
    }
    const result = await content.sendContextConversationMessage(contextConversationId.value, text)
    draft.value = ''
    if (result.status === 'risk_pending') showToast('消息已进入风控审核')
    return
  }
  if (!text || !selectedThread.value) return
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  await content.sendConversationTurn(selectedThread.value.id, { body: text, type: 'text' })
  draft.value = ''
  activeTool.value = ''
}

function sourceTypeLabel(sourceType: ContextChatConversation['sourceType']) {
  const labels: Record<ContextChatConversation['sourceType'], string> = {
    bottle_reply: '漂流瓶回应',
    plaza_comment: '广场评论',
    treehole_comment: '历史评论',
    game_room: '游戏房间',
    private_room: '私密房间',
    match_expand: '扩列匹配',
    friend: '好友关系'
  }
  return labels[sourceType]
}

function displayText(value: string) {
  return value.replace(/树洞/g, '留言')
}

function toggleMorePanel() {
  if (activeTool.value === 'room') gameRoomContextStatus.value = ''
  activeTool.value = activeTool.value === 'more' ? '' : 'more'
}

function toggleVoiceMode() {
  gameRoomContextStatus.value = ''
  activeTool.value = activeTool.value === 'voice' ? '' : 'voice'
}

function closeTransientPanels() {
  if (activeTool.value === 'more' || activeTool.value === 'room' || activeTool.value === 'voice') {
    activeTool.value = ''
    gameRoomContextStatus.value = ''
  }
}

async function sendMedia(type: MediaType) {
  if (!selectedThread.value) return
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  activeTool.value = ''
  if (type === 'image' || type === 'flash_image') {
    await chooseImage(type)
    return
  }
  if (type === 'video' || type === 'flash_video') {
    await chooseVideo(type)
    return
  }
  await content.sendConversationTurn(selectedThread.value.id, {
    body: '按住录制的语音',
    type: 'voice',
    mediaDuration: 8
  })
}

async function chooseImage(type: 'image' | 'flash_image') {
  if (!selectedThread.value) return
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  if (typeof uni !== 'undefined' && uni.chooseImage) {
    uni.chooseImage({
      count: 1,
      sourceType: ['album', 'camera'],
      success: async (result) => {
        const filePath = result.tempFilePaths?.[0] || ''
        await content.sendConversationTurn(selectedThread.value!.id, {
          body: type === 'flash_image' ? '发送了一张闪图' : '发送了一张图片',
          type,
          mediaUrl: filePath
        })
      },
      fail: () => showToast('需要相册或相机权限')
    })
    return
  }
  await content.sendConversationTurn(selectedThread.value.id, { body: type === 'flash_image' ? '发送了一张闪图' : '发送了一张图片', type })
}

async function chooseVideo(type: 'video' | 'flash_video') {
  if (!selectedThread.value) return
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  if (typeof uni !== 'undefined' && uni.chooseVideo) {
    uni.chooseVideo({
      sourceType: ['album', 'camera'],
      compressed: true,
      success: async (result) => {
        await content.sendConversationTurn(selectedThread.value!.id, {
          body: type === 'flash_video' ? '发送了一段闪视频' : '发送了一段视频',
          type,
          mediaUrl: result.tempFilePath,
          mediaDuration: result.duration
        })
      },
      fail: () => showToast('需要相册或相机权限')
    })
    return
  }
  await content.sendConversationTurn(selectedThread.value.id, { body: type === 'flash_video' ? '发送了一段闪视频' : '发送了一段视频', type, mediaDuration: 12 })
}

async function viewFlash(turn: ConversationTurn) {
  if (turn.flashViewed || !selectedThread.value) return
  await content.viewConversationTurn(selectedThread.value.id, turn.id)
  showToast('闪内容已查看，仅显示一次')
}

async function toggleGiftPanel() {
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  if (activeTool.value === 'gift') {
    activeTool.value = ''
    return
  }
  await content.loadWallet()
  activeTool.value = 'gift'
}

async function sendGift(giftId: string) {
  if (!selectedThread.value || sendingGiftId.value) return
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  const gift = content.gifts.find((item) => item.id === giftId)
  if (!gift) return
  if ((content.wallet?.rechargeCoins || 0) < gift.priceCoins) {
    showToast('金币不足，请先充值')
    goWallet()
    return
  }
  sendingGiftId.value = giftId
  try {
    await content.sendConversationGift(selectedThread.value.id, giftId)
    activeTool.value = ''
    playGiftCelebration(gift)
    showToast(`已送出 ${gift.name}`)
  } catch {
    showToast('金币不足，请先充值')
    goWallet()
  } finally {
    sendingGiftId.value = ''
  }
}

async function createRoom(mode: RoomMode) {
  if (!selectedThread.value) return
  if (isSelectedThreadFrozen.value) {
    showAppealInfo()
    return
  }
  gameRoomContextStatus.value = ''
  const thread = selectedThread.value
  try {
    const result = await content.createGameRoom(thread.id, mode)
    const contextRequest = await content.createContextChatRequest({
      targetUserId: thread.participantUserId,
      sourceType: 'game_room',
      sourceId: result.roomId,
      replyId: thread.id,
      initiatorAction: 'room_confirm',
      evidenceId: `game_room:${result.roomId}`
    })
    gameRoomContextStatus.value = gameRoomStatusText(contextRequest.status, contextRequest.conversationId)
    showToast(gameRoomContextStatus.value)
    if (contextRequest.status === 'active' && contextRequest.conversationId) {
      activeTool.value = ''
      navigateTo(`/pages/messages/chat?contextConversationId=${contextRequest.conversationId}`)
    }
  } catch {
    gameRoomContextStatus.value = '房间已创建或申请失败，请稍后重试'
    showToast(gameRoomContextStatus.value)
  }
}

function gameRoomStatusText(status: string, conversationId?: string) {
  if (status === 'active') return conversationId ? '房间确认已通过，正在进入临时会话' : '房间确认已通过'
  if (status === 'blocked') return '对方或你已拉黑，无法开启房间继续聊'
  if (status === 'expired') return '房间继续聊申请已过期'
  if (status === 'reported' || status === 'risk_frozen') return '房间继续聊申请已进入风控处理'
  return '房间已创建，继续聊申请等待对方确认'
}

function goWallet() {
  activeTool.value = ''
  navigateTo('/pages/wallet/index')
}

function showAppealInfo() {
  activeTool.value = ''
  void submitFrozenAppeal()
}

async function submitFrozenAppeal() {
  activeTool.value = ''
  if (!selectedThread.value || appealSubmitting.value || appealSubmitted.value) return
  const reason = appealReason.value.trim() || '我认为本次聊天冻结存在误判，请复核上下文。'
  appealSubmitting.value = true
  try {
    await content.submitChatAppeal(selectedThread.value.id, reason)
    appealSubmitted.value = true
    showToast('申诉已提交，等待后台处理')
  } catch {
    showToast('申诉提交失败，请稍后再试')
  } finally {
    appealSubmitting.value = false
  }
}

function playGiftCelebration(gift: GiftProduct) {
  celebrationGift.value = gift
  if (giftTimer) clearTimeout(giftTimer)
  giftTimer = setTimeout(() => {
    celebrationGift.value = undefined
  }, 1300)
}
</script>

<style scoped lang="scss">
.chat-page {
  min-height: 100vh;
  min-height: 100dvh;
  padding: 18rpx 18rpx 116rpx;
  color: #fff;
  background: #071225;
}

.chat-panel {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 176rpx);
  min-height: calc(100dvh - 176rpx);
  border: 0;
  border-radius: 20rpx;
  padding: 18rpx;
  background: #111b39;
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.04);
}

.chat-head {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 18rpx;
}

.chat-user-head {
  display: flex;
  align-items: center;
  gap: 12rpx;
  flex: 1;
  min-width: 0;
}

.direct-chat-head {
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) 34rpx minmax(0, 1fr) auto;
  gap: 10rpx;
}

.chat-party {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 10rpx;
}

.chat-link-mark {
  position: relative;
  width: 34rpx;
  height: 2rpx;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.48);
}

.chat-link-mark::before,
.chat-link-mark::after {
  position: absolute;
  top: 50%;
  width: 8rpx;
  height: 8rpx;
  border-radius: 50%;
  content: '';
  background: #2dd4bf;
  transform: translateY(-50%);
}

.chat-link-mark::before {
  left: -2rpx;
}

.chat-link-mark::after {
  right: -2rpx;
}

.thread-avatar {
  flex: 0 0 auto;
  width: 74rpx;
  height: 74rpx;
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(180deg, #38bdf8, #2563eb);
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 12rpx 24rpx rgba(37, 99, 235, 0.18);
}

.context-avatar {
  position: relative;
  overflow: hidden;
}

.context-avatar::before,
.context-avatar::after {
  position: absolute;
  content: '';
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.88);
}

.context-avatar::before {
  top: 17rpx;
  left: 50%;
  width: 22rpx;
  height: 22rpx;
  transform: translateX(-50%);
}

.context-avatar::after {
  right: 16rpx;
  bottom: 11rpx;
  left: 16rpx;
  height: 28rpx;
}

.image-avatar {
  display: block;
  background: rgba(35, 108, 114, 0.08);
}

.chat-title-main {
  flex: 1;
  min-width: 0;
}

.party-label,
.party-name {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.party-label {
  color: #9aa6c3;
  font-size: 20rpx;
  font-weight: 800;
}

.party-name {
  color: #fff;
  font-size: 26rpx;
  font-weight: 900;
}

.online-chip {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 8rpx 12rpx;
  color: #99f6e4;
  background: rgba(13, 148, 136, 0.22);
  font-size: 20rpx;
  font-weight: 900;
}

.online-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  background: #35b47f;
  box-shadow: 0 0 0 6rpx rgba(53, 180, 127, 0.16);
}

.chat-title-main .h2,
.chat-title-main .muted {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-title-main .h2 {
  color: #fff;
}

.chat-title-main .muted {
  color: #9aa6c3;
}

.source-card {
  margin-top: 16rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.16);
  border-radius: 16rpx;
  padding: 14rpx 16rpx;
  background: rgba(7, 18, 37, 0.72);
}

.source-kicker,
.source-text {
  display: block;
}

.source-kicker {
  color: #2dd4bf;
  font-size: 21rpx;
  font-weight: 900;
}

.source-text {
  margin-top: 6rpx;
  overflow: hidden;
  color: #cbd5e1;
  font-size: 23rpx;
  line-height: 1.45;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.freeze-card {
  display: grid;
  gap: 8rpx;
  margin-top: 14rpx;
  border: 1rpx solid rgba(251, 191, 36, 0.24);
  border-radius: 16rpx;
  padding: 16rpx;
  color: #fde68a;
  background: rgba(113, 63, 18, 0.24);
}

.freeze-title,
.freeze-link {
  font-size: 24rpx;
  font-weight: 900;
}

.freeze-text {
  color: #f8e7b4;
  font-size: 22rpx;
  line-height: 1.5;
}

.freeze-link {
  color: #67e8f9;
}

.freeze-link.disabled {
  color: #94a3b8;
}

.appeal-input {
  box-sizing: border-box;
  width: 100%;
  min-height: 92rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.22);
  border-radius: 14rpx;
  padding: 14rpx 16rpx;
  color: #e5f7ff;
  background: rgba(15, 23, 42, 0.72);
  font-size: 24rpx;
  line-height: 1.4;
}

.freeze-action-row {
  display: flex;
  justify-content: flex-start;
}

.send-button,
.room-mode {
  display: flex;
  gap: 8rpx;
  align-items: center;
  justify-content: center;
  border-radius: 14rpx;
  color: #fff;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
  font-weight: 900;
}

.message-list {
  display: grid;
  align-content: start;
  gap: 16rpx;
  flex: 1;
  min-height: 360rpx;
  margin-top: 18rpx;
  overflow-y: auto;
  padding: 4rpx 2rpx 24rpx;
}

.context-empty {
  border-radius: 14rpx;
  padding: 28rpx 20rpx;
  color: #99f6e4;
  background: rgba(20, 184, 166, 0.12);
  font-size: 24rpx;
  font-weight: 800;
  line-height: 1.5;
  text-align: center;
}

.message-list-expanded {
  padding-bottom: 220rpx;
}

.chat-line {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  animation: message-slide 180ms ease-out both;
}

.chat-line.me {
  align-items: flex-end;
}

.chat-name {
  margin-bottom: 8rpx;
  color: #8190b8;
  font-size: 22rpx;
}

.chat-bubble {
  max-width: 84%;
  border-radius: 22rpx 22rpx 22rpx 8rpx;
  padding: 16rpx 20rpx;
  color: #e2e8f0;
  background: #1a2549;
  font-size: 26rpx;
  line-height: 1.45;
  box-shadow: 0 10rpx 24rpx rgba(0, 0, 0, 0.18);
}

.chat-line.me .chat-bubble {
  color: #061225;
  border-radius: 22rpx 22rpx 8rpx 22rpx;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
}

.chat-bubble.flash_image,
.chat-bubble.flash_video {
  border: 1px dashed rgba(255, 59, 48, 0.34);
  color: #b94747;
  background: rgba(255, 59, 48, 0.08);
}

.chat-bubble.viewed {
  opacity: 0.56;
}

.gift-bubble,
.room-bubble {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.gift-bubble-visual {
  flex: 0 0 auto;
  margin: 0;
}

.room-id {
  opacity: 0.72;
  font-size: 21rpx;
}

.composer-shell {
  position: sticky;
  bottom: 0;
  z-index: 6;
  margin-top: 14rpx;
  padding: 12rpx 0 8rpx;
  background: linear-gradient(180deg, rgba(7, 18, 37, 0), rgba(7, 18, 37, 0.98) 26%, rgba(7, 18, 37, 0.98));
  display: grid;
  gap: 12rpx;
}

.frozen-composer {
  border: 1rpx solid rgba(251, 191, 36, 0.2);
  border-radius: 16rpx;
  padding: 20rpx;
  color: #fde68a;
  background: rgba(15, 23, 42, 0.96);
  font-size: 24rpx;
  font-weight: 900;
  text-align: center;
}

.composer-panels {
  animation: toolPanelIn 160ms ease-out both;
}

.tool-panel,
.room-panel {
  pointer-events: auto;
  border: 1rpx solid rgba(148, 163, 184, 0.16);
  border-radius: 18rpx;
  padding: 12rpx;
  background: #111b39;
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.04), 0 14rpx 32rpx rgba(0, 0, 0, 0.2);
}

.tool-grid,
.room-panel {
  display: grid;
  animation: toolPanelIn 160ms ease-out both;
}

.tool-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10rpx;
}

.tool-chip {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6rpx;
  min-height: 92rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.14);
  border-radius: 16rpx;
  padding: 10rpx 6rpx;
  color: #e2e8f0;
  background: #172142;
  font-size: 20rpx;
  font-weight: 900;
  box-shadow: 0 8rpx 18rpx rgba(15, 23, 42, 0.05);
}

.tool-chip.highlight {
  color: #0f172a;
  border-color: rgba(245, 158, 11, 0.2);
  background: linear-gradient(180deg, #fffbeb, #fff7ed);
}

.tool-name {
  display: block;
  line-height: 1;
}

.tool-glyph {
  position: relative;
  width: 48rpx;
  height: 48rpx;
  border-radius: 14px;
  box-shadow: inset 0 0 0 2rpx rgba(255, 255, 255, 0.35);
}

.tool-glyph::before {
  content: '';
  position: absolute;
  inset: 10rpx;
  border: 3rpx solid rgba(255, 255, 255, 0.88);
  border-radius: 10rpx;
}

.tool-glyph::after {
  content: '';
  position: absolute;
  width: 13rpx;
  height: 13rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.92);
  right: 11rpx;
  bottom: 11rpx;
}

.image-tool .tool-glyph {
  background: linear-gradient(145deg, #60a5fa, #2563eb);
}

.voice-tool .tool-glyph {
  background: linear-gradient(145deg, #34d399, #0f766e);
}

.video-tool .tool-glyph {
  background: linear-gradient(145deg, #818cf8, #4f46e5);
}

.gift-tool .tool-glyph {
  background: linear-gradient(145deg, #fbbf24, #f97316);
}

.flash-tool .tool-glyph,
.flash-video-tool .tool-glyph {
  background: linear-gradient(145deg, #fb7185, #e11d48);
}

.room-tool .tool-glyph {
  background: linear-gradient(145deg, #14b8a6, #0f766e);
}

.room-panel {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12rpx;
  border: 1rpx solid rgba(47, 127, 109, 0.18);
  border-radius: 16rpx;
  padding: 16rpx;
  background: #111b39;
}

.room-mode {
  display: grid;
  gap: 14rpx;
  min-height: 176rpx;
  padding: 16rpx;
  color: #99f6e4;
  background: rgba(20, 184, 166, 0.12);
  font-size: 22rpx;
  text-align: left;
}

.room-mode-head,
.room-presence {
  display: flex;
  align-items: center;
}

.room-mode-head {
  justify-content: space-between;
  gap: 8rpx;
  color: #fff;
  font-weight: 900;
}

.room-state {
  border-radius: 999px;
  padding: 4rpx 8rpx;
  color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
  font-size: 18rpx;
}

.avatar-ring {
  display: flex;
  align-items: center;
  min-height: 44rpx;
}

.room-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44rpx;
  height: 44rpx;
  margin-right: -10rpx;
  border: 3rpx solid rgba(255, 255, 255, 0.92);
  border-radius: 50%;
  background: linear-gradient(180deg, #38bdf8, #2563eb);
}

.room-avatar.self {
  background: linear-gradient(180deg, #2af0b6, #0f766e);
}

.room-presence {
  gap: 5rpx;
  color: #65757b;
  font-size: 18rpx;
}

.presence-bar {
  width: 8rpx;
  height: 20rpx;
  border-radius: 999px;
  background: #7bc7a7;
}

.presence-bar.strong {
  height: 30rpx;
  background: #2563eb;
}

.presence-bar.soft {
  height: 14rpx;
  opacity: 0.56;
}

.room-countdown {
  justify-self: start;
  border-radius: 999px;
  padding: 8rpx 14rpx;
  color: #fff;
  background: rgba(255, 255, 255, 0.16);
  font-size: 24rpx;
  font-weight: 900;
}

.room-mode.primary {
  color: #fff;
  background: linear-gradient(180deg, #3b82f6, #2563eb);
}

.room-mode.primary .room-mode-head,
.room-mode.primary .room-state {
  color: #fff;
}

.room-context-status {
  grid-column: 1 / -1;
  display: block;
  border-radius: 12rpx;
  padding: 14rpx 16rpx;
  color: #99f6e4;
  background: rgba(20, 184, 166, 0.12);
  font-size: 22rpx;
  font-weight: 900;
  line-height: 1.45;
}

.composer-row {
  display: grid;
  grid-template-columns: 64rpx minmax(0, 1fr) 104rpx;
  gap: 10rpx;
}

.plus-button,
.voice-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 68rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.16);
  border-radius: 16rpx;
  color: #2dd4bf;
  background: #172142;
  box-shadow: 0 8rpx 18rpx rgba(0, 0, 0, 0.18);
}

.plus-button text,
.plus-button::after {
  position: absolute;
  width: 28rpx;
  height: 4rpx;
  border-radius: 999px;
  background: currentColor;
  content: '';
  transition: transform 160ms ease;
}

.plus-button::after {
  transform: rotate(90deg);
}

.plus-button.open text {
  transform: rotate(45deg);
}

.plus-button.open::after {
  transform: rotate(135deg);
}

.plus-button.disabled {
  opacity: 0.38;
}

.voice-button {
  color: #67e8f9;
}

.voice-button::before {
  content: '';
  width: 24rpx;
  height: 34rpx;
  border: 4rpx solid currentColor;
  border-radius: 999px;
  box-sizing: border-box;
}

.voice-button::after {
  position: absolute;
  bottom: 16rpx;
  width: 28rpx;
  height: 14rpx;
  border-right: 4rpx solid currentColor;
  border-bottom: 4rpx solid currentColor;
  border-left: 4rpx solid currentColor;
  border-radius: 0 0 14rpx 14rpx;
  content: '';
}

.voice-button.open {
  color: #111b39;
  background: #67e8f9;
}

.voice-capture-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14rpx;
  min-height: 112rpx;
  border: 1rpx solid rgba(103, 232, 249, 0.2);
  border-radius: 18rpx;
  color: #bfdbfe;
  background: rgba(15, 23, 42, 0.58);
  font-size: 24rpx;
  font-weight: 900;
}

.voice-capture-icon {
  width: 34rpx;
  height: 34rpx;
  border-radius: 50%;
  background: #67e8f9;
  box-shadow: 0 0 0 10rpx rgba(103, 232, 249, 0.12);
}

.chat-input {
  min-height: 68rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.16);
  border-radius: 16rpx;
  padding: 0 18rpx;
  color: #e2e8f0;
  background: #172142;
  box-sizing: border-box;
  font-size: 26rpx;
}

.send-button {
  min-height: 68rpx;
  font-size: 24rpx;
}

@keyframes message-slide {
  from {
    opacity: 0;
    transform: translateY(10rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes toolPanelIn {
  from {
    opacity: 0;
    transform: translateY(12rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 420px) {
  .room-panel {
    grid-template-columns: 1fr;
  }

  .online-chip {
    padding: 7rpx 10rpx;
    font-size: 19rpx;
  }
}
</style>
