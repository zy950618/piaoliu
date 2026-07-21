<template>
  <view class="room-page">
    <view v-if="loading" class="state-card">正在进入房间…</view>
    <view v-else-if="errorText" class="state-card error-state">
      <text class="state-title">暂时无法进入房间</text>
      <text>{{ errorText }}</text>
      <button class="secondary-button" @tap="loadRoom">重新加载</button>
    </view>
    <template v-else-if="room">
      <view class="room-header">
        <view>
          <text class="eyebrow">{{ room.visibility === 'public' ? '广场公开房' : '双人私密房' }}</text>
          <text class="room-title">{{ room.name }}</text>
          <text class="room-subtitle">玩法结果由服务器生成，仅房间成员可见</text>
        </view>
        <text class="status-badge">{{ room.status === 'active' ? '进行中' : '已结束' }}</text>
      </view>

      <view class="members-panel">
        <view v-for="member in room.members" :key="member.userId" class="member-row">
          <view class="member-avatar">{{ member.role === 'owner' ? '主' : '友' }}</view>
          <view class="member-copy">
            <text>{{ member.userId === app.user?.id ? '我' : room.visibility === 'public' ? '房间成员' : '受邀成员' }}</text>
            <text class="member-meta">{{ member.role === 'owner' ? '房主' : '成员' }} · {{ member.status === 'active' ? '已加入' : '等待加入' }}</text>
          </view>
        </view>
        <view v-if="room.visibility === 'private' && room.members.length < room.capacity" class="waiting-member">
          <view class="member-avatar waiting">待</view>
          <view class="member-copy">
            <text>等待对方接受邀请</text>
            <text class="member-meta">对方加入后会实时出现在这里</text>
          </view>
        </view>
      </view>

      <view class="play-section">
        <text class="section-title">今晚玩什么</text>
        <text class="section-hint">每次只开启一轮，结果会保留在本次房间记录中。</text>
        <view class="play-grid">
          <button :disabled="busy || room.status !== 'active'" class="play-button" @tap="play('dice')">
            <text class="play-name">掷骰子</text>
            <text class="play-desc">1–6 点随机结果</text>
          </button>
          <button :disabled="busy || room.status !== 'active'" class="play-button" @tap="play('truth')">
            <text class="play-name">真心话</text>
            <text class="play-desc">{{ room.visibility === 'public' ? '适合房间互动的问题' : '适合两人的问题' }}</text>
          </button>
          <button :disabled="busy || room.status !== 'active'" class="play-button" @tap="play('dare')">
            <text class="play-name">大冒险</text>
            <text class="play-desc">有边界的轻任务</text>
          </button>
        </view>
      </view>

      <view v-if="round" class="result-card">
        <text class="result-label">本轮结果</text>
        <text v-if="round.mode === 'dice'" class="dice-result">{{ round.result.value }}</text>
        <text v-else class="prompt-result">{{ round.promptText }}</text>
        <text class="result-foot">{{ round.mode === 'dice' ? '六面骰 · 服务端随机' : '仅用于轻松互动，任何人都可以跳过' }}</text>
      </view>

      <button v-if="room.ownerId === app.user?.id && room.status === 'active'" class="end-button" @tap="endRoom">
        结束房间
      </button>
    </template>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { businessApi } from '@/services/businessApi'
import { showToast } from '@/services/feedback'
import { connectRoom, type RealtimeConnection } from '@/services/realtime'
import { useAppStore } from '@/stores/app'
import type { SocialGameRound, SocialRoom } from '@/types/domain'

const app = useAppStore()
const roomId = ref('')
const room = ref<SocialRoom>()
const round = ref<SocialGameRound>()
const loading = ref(true)
const busy = ref(false)
const errorText = ref('')
let realtimeConnection: RealtimeConnection | undefined

onLoad((query) => {
  roomId.value = String(query?.roomId || '')
  void initializeRoom()
})

onUnload(() => realtimeConnection?.close())

async function initializeRoom() {
  await Promise.all([app.hydrate(), loadRoom()])
  if (!room.value) return
  realtimeConnection = await connectRoom(room.value.id, (event) => {
    if (event.type === 'room.updated') void loadRoom(false)
    if (event.type === 'room.round.resolved') {
      const value = event.round as Record<string, unknown> | undefined
      if (value) round.value = {
        id: String(value.id || ''),
        roomId: String(value.room_id || room.value?.id || ''),
        initiatorId: String(value.initiator_id || ''),
        mode: value.mode as SocialGameRound['mode'],
        status: value.status as SocialGameRound['status'],
        promptId: value.prompt_id ? String(value.prompt_id) : undefined,
        promptText: value.prompt_text ? String(value.prompt_text) : undefined,
        result: (value.result as Record<string, unknown>) || {},
        createdAt: String(value.created_at || ''),
        resolvedAt: value.resolved_at ? String(value.resolved_at) : undefined
      }
    }
  })
}

async function loadRoom(showLoading = true) {
  if (!roomId.value) {
    loading.value = false
    errorText.value = '缺少房间编号，请从聊天页重新进入。'
    return
  }
  if (showLoading) loading.value = true
  errorText.value = ''
  try {
    room.value = await businessApi.getRoom(roomId.value)
  } catch (error) {
    errorText.value = error instanceof Error ? error.message : '房间加载失败，请检查网络。'
  } finally {
    if (showLoading) loading.value = false
  }
}

async function play(mode: SocialGameRound['mode']) {
  if (busy.value || !room.value) return
  busy.value = true
  try {
    round.value = await businessApi.playRoomRound(room.value.id, mode)
  } catch (error) {
    showToast(error instanceof Error ? error.message : '本轮开启失败，请稍后重试')
  } finally {
    busy.value = false
  }
}

async function endRoom() {
  if (!room.value || busy.value) return
  busy.value = true
  try {
    room.value = await businessApi.endRoom(room.value.id)
    showToast('房间已结束，记录仍会保留')
  } catch (error) {
    showToast(error instanceof Error ? error.message : '房间结束失败，请重试')
  } finally {
    busy.value = false
  }
}
</script>

<style scoped lang="scss">
.room-page { min-height: 100vh; padding: 32rpx; background: #f5f9fb; color: #17252d; box-sizing: border-box; }
.room-header { display: flex; justify-content: space-between; gap: 24rpx; padding: 36rpx; background: #fff; border: 1rpx solid #dce8ed; border-radius: 28rpx; }
.eyebrow { display: block; margin-bottom: 10rpx; color: #358ba9; font-size: 22rpx; font-weight: 600; letter-spacing: 2rpx; }
.room-title { display: block; font-size: 40rpx; line-height: 1.25; font-weight: 700; }
.room-subtitle { display: block; margin-top: 12rpx; color: #627782; font-size: 25rpx; line-height: 1.55; }
.status-badge { align-self: flex-start; padding: 8rpx 16rpx; border-radius: 999rpx; background: #e8f5f8; color: #267a96; font-size: 22rpx; white-space: nowrap; }
.members-panel, .play-section, .result-card, .state-card { margin-top: 24rpx; padding: 30rpx; background: #fff; border: 1rpx solid #dce8ed; border-radius: 24rpx; }
.member-row, .waiting-member { display: flex; align-items: center; gap: 20rpx; padding: 16rpx 0; }
.member-row + .member-row, .member-row + .waiting-member { border-top: 1rpx solid #edf3f5; }
.member-avatar { display: grid; place-items: center; width: 72rpx; height: 72rpx; border-radius: 50%; background: #dceff4; color: #267a96; font-size: 24rpx; font-weight: 700; }
.member-avatar.waiting { background: #f1f3f4; color: #83939b; }
.member-copy { display: flex; flex-direction: column; gap: 6rpx; font-size: 28rpx; }
.member-meta, .section-hint, .result-foot { color: #6c7f89; font-size: 23rpx; line-height: 1.5; }
.section-title { display: block; font-size: 32rpx; font-weight: 700; }
.section-hint { display: block; margin-top: 8rpx; }
.play-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16rpx; margin-top: 24rpx; }
.play-button { min-width: 0; padding: 24rpx 12rpx; border: 1rpx solid #cfe0e6; border-radius: 20rpx; background: #f8fbfc; line-height: 1.2; }
.play-button::after, .secondary-button::after, .end-button::after { border: 0; }
.play-button[disabled] { opacity: .45; }
.play-name, .play-desc { display: block; }
.play-name { color: #1d5669; font-size: 27rpx; font-weight: 650; }
.play-desc { margin-top: 10rpx; color: #71838c; font-size: 20rpx; }
.result-card { text-align: center; border-color: #b9dce7; }
.result-label { display: block; color: #358ba9; font-size: 22rpx; font-weight: 600; }
.dice-result { display: block; margin: 18rpx 0; color: #176f8d; font-size: 104rpx; line-height: 1; font-weight: 750; }
.prompt-result { display: block; margin: 24rpx auto; max-width: 560rpx; font-size: 34rpx; line-height: 1.55; font-weight: 650; }
.end-button, .secondary-button { margin-top: 28rpx; border-radius: 18rpx; font-size: 27rpx; }
.end-button { background: transparent; border: 1rpx solid #d5a5a5; color: #a23d3d; }
.secondary-button { background: #358ba9; color: #fff; }
.error-state { color: #7e3030; }
.state-title { display: block; margin-bottom: 12rpx; font-size: 32rpx; font-weight: 700; }
@media (max-width: 390px) { .play-grid { grid-template-columns: 1fr; } .play-button { text-align: left; } }
</style>
