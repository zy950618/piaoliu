<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">签到</text>
        <text class="muted">连续签到 {{ app.checkin?.streakDays || 0 }} 天，签到奖励玩法次数</text>
      </view>
    </view>

    <view class="section panel">
      <view class="checkin-head">
        <view>
          <text class="h2">一周签到</text>
          <text class="muted">下一次奖励所有玩法次数 +{{ app.nextCheckinReward }}</text>
        </view>
        <view class="button secondary sign-button" :class="{ disabled: app.checkin?.checkedToday }" @tap="checkin">
          {{ app.checkin?.checkedToday ? '已签到' : '立即签到' }}
        </view>
      </view>
      <CheckinStrip
        class="checkin"
        :rewards="app.checkin?.weekRewards || []"
        :active-count="app.checkin?.streakDays || 0"
        :current-index="app.checkin?.currentWeekIndex || 0"
      />
    </view>

    <view class="section panel video-panel">
      <view class="video-copy">
        <text class="h2">看视频领取次数</text>
        <text class="muted">完整看完一次，金币 +1，所有玩法次数各 +{{ app.adReward?.rewardPerQuota || 10 }}</text>
      </view>
      <view class="reward-status">{{ app.adCountdownText }}</view>
      <view class="button video-button" :class="{ disabled: !app.adReward?.canWatch || adWatching }" @tap="watchVideoAd">
        {{ adWatching ? '加载视频中' : app.adReward?.canWatch ? '看视频领取' : app.adCountdownText }}
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import CheckinStrip from '@/components/CheckinStrip.vue'
import { navigateTo, showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'

const app = useAppStore()
const adWatching = ref(false)

onLoad(() => app.hydrate())

async function checkin() {
  if (app.checkin?.checkedToday) return
  const result = await app.runCheckin()
  showToast(`连续签到第 ${result.streakDays} 天，所有玩法次数 +${result.lastReward}`)
}

async function watchVideoAd() {
  if (adWatching.value) return
  if (!app.adReward?.canWatch) {
    showToast(app.adCountdownText)
    return
  }
  navigateTo('/pages/ad/reward')
}
</script>

<style scoped lang="scss">
.checkin-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
}

.sign-button {
  width: 168rpx;
  min-height: 70rpx;
  flex: 0 0 auto;
}

.checkin {
  margin-top: 24rpx;
}

.video-panel {
  display: grid;
  gap: 18rpx;
}

.video-copy .h2,
.video-copy .muted {
  display: block;
}

.video-copy .muted {
  margin-top: 8rpx;
}

.reward-status {
  display: inline-flex;
  justify-self: start;
  border-radius: 999px;
  padding: 7rpx 16rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
  font-size: 23rpx;
  font-weight: 800;
  line-height: 1.2;
}

.video-button {
  min-height: 78rpx;
}
</style>
