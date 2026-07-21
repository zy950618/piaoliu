<template>
  <view class="page safe-bottom reward-page">
    <view class="ad-hero">
      <view>
        <text class="eyebrow">{{ ad.provider }}</text>
        <text class="title">{{ ad.title }}</text>
        <text class="muted">{{ ad.description }}</text>
      </view>
      <view class="reward-chip">+{{ ad.rewardPerQuota }} 次</view>
    </view>

    <view class="ad-stage">
      <video
        v-if="ad.displayType === 'video' && ad.mediaUrl"
        class="ad-media"
        :src="ad.mediaUrl"
        :controls="false"
        :autoplay="watching"
        muted
        object-fit="cover"
      />
      <image
        v-else-if="ad.displayType === 'image' && ad.mediaUrl"
        class="ad-media"
        :src="ad.mediaUrl"
        mode="aspectFill"
      />
      <view v-else class="ad-link-panel">
        <text class="ad-link-title">{{ ad.title }}</text>
        <text class="muted">{{ ad.clickUrl || '广告落地页待配置' }}</text>
      </view>
      <view class="countdown-badge">
        {{ watching ? `${remainingSeconds}s` : `${ad.countdownSeconds}s` }}
      </view>
    </view>

    <view class="section panel bridge-panel">
      <view>
        <text class="h2">小程序桥接</text>
        <text class="muted">后续微信小程序接广告联盟时复用同一广告位和路径。</text>
      </view>
      <view class="bridge-row">
        <text>AppID</text>
        <strong>{{ ad.miniProgramAppId || '-' }}</strong>
      </view>
      <view class="bridge-row">
        <text>路径</text>
        <strong>{{ ad.miniProgramPath || '-' }}</strong>
      </view>
      <view class="button secondary" @tap="openMiniProgramBridge">打开小程序入口</view>
    </view>

    <view class="section action-panel">
      <view class="button primary-action" :class="{ disabled: !canStart || watching }" @tap="startReward">
        {{ actionText }}
      </view>
      <view class="button ghost-action" v-if="ad.clickUrl" @tap="openLanding">查看广告落地页</view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'

type NavigateToMiniProgram = (options: { appId: string; path?: string }) => void
type UniMiniProgramBridge = typeof uni & {
  navigateToMiniProgram?: NavigateToMiniProgram
}

const app = useAppStore()
const watching = ref(false)
const settled = ref(false)
const remainingSeconds = ref(0)
let timer: ReturnType<typeof setInterval> | undefined

const ad = computed(() => ({
  canWatch: app.adReward?.canWatch ?? false,
  cooldownText: app.adCountdownText,
  rewardPerQuota: app.adReward?.rewardPerQuota ?? 1,
  displayType: app.adReward?.displayType ?? 'video',
  provider: app.adReward?.provider ?? 'mock_alliance',
  placementId: app.adReward?.placementId ?? 'reward_video_default',
  title: app.adReward?.title ?? '激励视频',
  description: app.adReward?.description ?? '完整观看后可获得次数奖励',
  mediaUrl: app.adReward?.mediaUrl,
  clickUrl: app.adReward?.clickUrl,
  countdownSeconds: app.adReward?.countdownSeconds ?? 5,
  miniProgramAppId: app.adReward?.miniProgramAppId,
  miniProgramPath: app.adReward?.miniProgramPath
}))

const canStart = computed(() => ad.value.canWatch && !settled.value)
const actionText = computed(() => {
  if (watching.value) return `观看中 ${remainingSeconds.value}s`
  if (settled.value) return '奖励已到账'
  if (!ad.value.canWatch) return ad.value.cooldownText
  return '开始观看并领取次数'
})

onLoad(() => {
  void app.hydrate()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

async function startReward() {
  if (!canStart.value || watching.value) {
    showToast(ad.value.cooldownText || '暂不可领取')
    return
  }
  watching.value = true
  const prepared = await app.prepareRewardAd()
  remainingSeconds.value = prepared.countdownSeconds || ad.value.countdownSeconds
  timer = setInterval(async () => {
    remainingSeconds.value -= 1
    if (remainingSeconds.value > 0) return
    if (timer) clearInterval(timer)
    timer = undefined
    try {
      await app.commitRewardAd(prepared.sessionId, true)
      settled.value = true
      showToast(`奖励已到账，所有玩法次数 +${prepared.rewardPerQuota}`)
    } finally {
      watching.value = false
    }
  }, 1000)
}

function openLanding() {
  if (!ad.value.clickUrl) return
  if (typeof window !== 'undefined') {
    window.open(ad.value.clickUrl, '_blank')
    return
  }
  showToast('广告链接已配置')
}

function openMiniProgramBridge() {
  const bridge = typeof uni !== 'undefined' ? (uni as UniMiniProgramBridge).navigateToMiniProgram : undefined
  if (bridge && ad.value.miniProgramAppId) {
    bridge({ appId: ad.value.miniProgramAppId, path: ad.value.miniProgramPath })
    return
  }
  showToast(ad.value.miniProgramPath || '小程序入口待配置')
}
</script>

<style scoped lang="scss">
.reward-page {
  background: #07111f;
  color: #f8fafc;
}

.ad-hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20rpx;
  padding: 30rpx 28rpx 18rpx;
}

.eyebrow,
.title,
.muted {
  display: block;
}

.eyebrow {
  color: #67e8f9;
  font-size: 22rpx;
  font-weight: 800;
}

.title {
  margin-top: 8rpx;
  color: #f8fafc;
  font-size: 38rpx;
  font-weight: 900;
}

.muted {
  margin-top: 8rpx;
  color: rgba(226, 232, 240, 0.72);
  font-size: 24rpx;
  line-height: 1.5;
}

.reward-chip {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 10rpx 18rpx;
  color: #062b2e;
  background: #5eead4;
  font-size: 26rpx;
  font-weight: 900;
}

.ad-stage {
  position: relative;
  overflow: hidden;
  width: calc(100% - 56rpx);
  margin: 16rpx 28rpx 0;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 8px;
  aspect-ratio: 16 / 10;
  background: #0f172a;
}

.ad-media,
.ad-link-panel {
  width: 100%;
  height: 100%;
}

.ad-link-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-sizing: border-box;
  padding: 44rpx;
}

.ad-link-title {
  color: #fff;
  font-size: 34rpx;
  font-weight: 900;
}

.countdown-badge {
  position: absolute;
  right: 18rpx;
  top: 18rpx;
  min-width: 76rpx;
  border-radius: 999px;
  padding: 9rpx 14rpx;
  text-align: center;
  color: #07111f;
  background: #facc15;
  font-size: 25rpx;
  font-weight: 900;
}

.bridge-panel {
  display: grid;
  gap: 14rpx;
  margin: 24rpx 28rpx 0;
  color: #0f172a;
  background: #f8fafc;
}

.bridge-row {
  display: flex;
  justify-content: space-between;
  gap: 18rpx;
  color: #334155;
  font-size: 24rpx;
}

.bridge-row strong {
  max-width: 430rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-panel {
  display: grid;
  gap: 16rpx;
  margin: 24rpx 28rpx 0;
}

.primary-action {
  min-height: 84rpx;
  background: linear-gradient(135deg, #2dd4bf, #38bdf8);
  color: #042f2e;
}

.ghost-action {
  min-height: 76rpx;
  color: #e2e8f0;
  background: rgba(148, 163, 184, 0.16);
}
</style>
