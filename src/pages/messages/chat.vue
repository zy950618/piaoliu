<template>
  <view class="page chat-page safe-bottom">
    <view v-if="selectedThread" class="panel chat-panel">
      <view class="chat-head">
        <view class="chat-user-head">
          <image v-if="selectedThread.participantAvatarUrl" class="thread-avatar image-avatar" :src="selectedThread.participantAvatarUrl" mode="aspectFill" />
          <text v-else class="thread-avatar">{{ avatarText(selectedThread) }}</text>
          <view class="chat-title-main">
            <text class="h2">{{ selectedThread.participantName }}</text>
            <text class="muted">{{ selectedThread.participantTag }} · ID {{ participantDisplayId }}</text>
          </view>
          <view class="online-chip">
            <text class="online-dot" />
            <text>在线</text>
          </view>
        </view>
      </view>

      <view class="source-card">
        <text class="source-kicker">原漂流瓶</text>
        <text class="source-text">{{ selectedThread.bottlePreview }}</text>
      </view>

      <view class="message-list" :class="{ 'message-list-expanded': activeTool === 'more' || activeTool === 'room' }">
        <view
          v-for="turn in selectedThread.turns"
          :key="turn.id"
          class="chat-line"
          :class="{ me: turn.fromMe }"
        >
          <text class="chat-name">{{ turn.fromMe ? '我' : turn.senderName }}</text>
          <view class="chat-bubble" :class="[turn.type || 'text', { viewed: turn.flashViewed }]">
            <text v-if="!turn.type || turn.type === 'text'">{{ turn.body }}</text>
            <text v-else-if="turn.type === 'image'">图片消息：{{ turn.body }}</text>
            <text v-else-if="turn.type === 'voice'">语音 {{ turn.mediaDuration || 8 }}s：{{ turn.body }}</text>
            <text v-else-if="turn.type === 'video'">视频消息：{{ turn.body }}</text>
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

      <view class="composer-shell">
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
                <text>{{ avatarText(selectedThread).slice(0, 1) }}</text>
                <text>我</text>
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
                <text>{{ avatarText(selectedThread).slice(0, 1) }}</text>
                <text>我</text>
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
                <text>{{ avatarText(selectedThread).slice(0, 1) }}</text>
                <text>我</text>
              </view>
            <view class="room-countdown">15:00</view>
            </view>
          </view>
        </view>

        <view class="composer-row">
          <view class="plus-button" :class="{ open: activeTool === 'more' || activeTool === 'room' }" @tap="toggleMorePanel">
            <text />
          </view>
          <input v-model="draft" class="chat-input" maxlength="120" placeholder="输入聊天内容" @tap.stop @click.stop />
          <view class="send-button" @tap="sendText">发送</view>
        </view>
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
import { useContentStore } from '@/stores/content'
import type { ConversationThread, ConversationTurn, GiftProduct } from '@/types/domain'

type MediaType = NonNullable<ConversationTurn['type']>
type RoomMode = 'truth' | 'dare' | 'mixed'

const content = useContentStore()
const threadId = ref('')
const activeTool = ref<'' | 'more' | 'gift' | 'room'>('')
const draft = ref('')
const sendingGiftId = ref('')
const celebrationGift = ref<GiftProduct>()
let giftTimer: ReturnType<typeof setTimeout> | undefined

const selectedThread = computed(() => content.conversationThreads.find((thread) => thread.id === threadId.value))
const participantDisplayId = computed(() => selectedThread.value?.participantUserId || '-')

onLoad((query) => {
  threadId.value = String(query?.threadId || '')
  void loadPage()
})

onUnload(() => {
  if (giftTimer) clearTimeout(giftTimer)
})

async function loadPage() {
  await Promise.all([content.loadConversationThreads(), content.loadWallet()])
}

function avatarText(thread: ConversationThread) {
  return thread.participantAvatarText || thread.participantName.slice(0, 1)
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
  if (!text || !selectedThread.value) return
  await content.sendConversationTurn(selectedThread.value.id, { body: text, type: 'text' })
  draft.value = ''
  activeTool.value = ''
}

function toggleMorePanel() {
  activeTool.value = activeTool.value === 'more' ? '' : 'more'
}

async function sendMedia(type: MediaType) {
  if (!selectedThread.value) return
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
  if (activeTool.value === 'gift') {
    activeTool.value = ''
    return
  }
  await content.loadWallet()
  activeTool.value = 'gift'
}

async function sendGift(giftId: string) {
  if (!selectedThread.value || sendingGiftId.value) return
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
  await content.createGameRoom(selectedThread.value.id, mode)
  showToast('游戏房间已创建')
  activeTool.value = ''
}

function goWallet() {
  activeTool.value = ''
  navigateTo('/pages/wallet/index')
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
}

.chat-panel {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 176rpx);
  min-height: calc(100dvh - 176rpx);
  padding: 22rpx;
  border-radius: 16px;
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

.thread-avatar {
  flex: 0 0 auto;
  width: 68rpx;
  height: 68rpx;
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(180deg, #38bdf8, #2563eb);
  font-size: 26rpx;
  font-weight: 900;
  line-height: 68rpx;
  text-align: center;
  border: 3rpx solid rgba(255, 255, 255, 0.9);
  box-shadow: 0 0 0 5rpx rgba(37, 99, 235, 0.12), 0 10rpx 22rpx rgba(37, 99, 235, 0.14);
}

.image-avatar {
  display: block;
  background: rgba(35, 108, 114, 0.08);
}

.chat-title-main {
  flex: 1;
  min-width: 0;
}

.online-chip {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 8rpx 12rpx;
  color: #0f766e;
  background: rgba(15, 118, 110, 0.1);
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

.source-card {
  margin-top: 18rpx;
  border: 1px solid rgba(37, 99, 235, 0.1);
  border-radius: 14px;
  padding: 16rpx 18rpx;
  background:
    linear-gradient(180deg, rgba(248, 250, 252, 0.96), rgba(255, 255, 255, 0.92)),
    radial-gradient(circle at 98% 0%, rgba(37, 99, 235, 0.08), transparent 34%);
}

.source-kicker,
.source-text {
  display: block;
}

.source-kicker {
  color: #2563eb;
  font-size: 21rpx;
  font-weight: 900;
}

.source-text {
  margin-top: 6rpx;
  overflow: hidden;
  color: #334155;
  font-size: 24rpx;
  line-height: 1.45;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.send-button,
.room-mode {
  display: flex;
  gap: 8rpx;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  color: #fff;
  background: linear-gradient(180deg, #3b82f6, #2563eb);
  font-weight: 900;
}

.message-list {
  display: grid;
  align-content: start;
  gap: 18rpx;
  flex: 1;
  min-height: 320rpx;
  margin-top: 22rpx;
  overflow-y: auto;
  padding: 4rpx 2rpx 24rpx;
}

.message-list-expanded {
  padding-bottom: 292rpx;
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
  color: #65757b;
  font-size: 22rpx;
}

.chat-bubble {
  max-width: 84%;
  border-radius: 20px 20px 20px 6px;
  padding: 17rpx 20rpx;
  color: #172126;
  background: rgba(255, 255, 255, 0.92);
  font-size: 26rpx;
  line-height: 1.45;
  box-shadow: 0 10rpx 24rpx rgba(3, 12, 18, 0.08);
}

.chat-line.me .chat-bubble {
  color: #fff;
  border-radius: 20px 20px 6px 20px;
  background: linear-gradient(180deg, #3b82f6, #2563eb);
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
  background: linear-gradient(180deg, rgba(255, 255, 255, 0), rgba(248, 250, 252, 0.98) 26%, rgba(248, 250, 252, 0.98));
  display: grid;
  gap: 12rpx;
}

.composer-panels {
  animation: toolPanelIn 160ms ease-out both;
}

.tool-panel,
.room-panel {
  pointer-events: auto;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 18px;
  padding: 16rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.96)),
    radial-gradient(circle at 12% 0%, rgba(37, 99, 235, 0.06), transparent 32%);
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.88), 0 14rpx 32rpx rgba(15, 23, 42, 0.08);
}

.tool-grid,
.room-panel {
  display: grid;
  animation: toolPanelIn 160ms ease-out both;
}

.tool-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14rpx 10rpx;
}

.tool-chip {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  min-height: 112rpx;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  padding: 12rpx 6rpx;
  color: #0f172a;
  background: linear-gradient(180deg, #fff, #f8fafc);
  font-size: 21rpx;
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
  width: 58rpx;
  height: 58rpx;
  border-radius: 18px;
  box-shadow: inset 0 0 0 2rpx rgba(255, 255, 255, 0.35);
}

.tool-glyph::before {
  content: '';
  position: absolute;
  inset: 12rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.88);
  border-radius: 12rpx;
}

.tool-glyph::after {
  content: '';
  position: absolute;
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.92);
  right: 13rpx;
  bottom: 13rpx;
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
  border: 1px solid rgba(47, 127, 109, 0.12);
  border-radius: 16px;
  padding: 16rpx;
  background: rgba(248, 250, 252, 0.96);
}

.room-mode {
  display: grid;
  gap: 14rpx;
  min-height: 176rpx;
  padding: 16rpx;
  color: #236c72;
  background: rgba(37, 99, 235, 0.08);
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
  color: #172126;
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

.avatar-ring text {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44rpx;
  height: 44rpx;
  margin-right: -10rpx;
  border: 3rpx solid rgba(255, 255, 255, 0.92);
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(180deg, #38bdf8, #2563eb);
  font-size: 18rpx;
  font-weight: 900;
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

.composer-row {
  display: grid;
  grid-template-columns: 64rpx minmax(0, 1fr) 104rpx;
  gap: 10rpx;
}

.plus-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 68rpx;
  border: 1px solid rgba(37, 99, 235, 0.14);
  border-radius: 16px;
  color: #2563eb;
  background: #fff;
  box-shadow: 0 8rpx 18rpx rgba(15, 23, 42, 0.06);
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

.chat-input {
  min-height: 68rpx;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 16px;
  padding: 0 18rpx;
  background: #fff;
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
