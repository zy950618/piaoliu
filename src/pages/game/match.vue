<template>
  <view class="match-page safe-bottom">
    <view class="match-head">
      <view>
        <text class="kicker">Game Match</text>
        <text class="title">随机匹配</text>
      </view>
      <view class="quota-pill">
        <text>{{ currentQuotaLabel }}</text>
        <text>{{ currentQuotaLeft }}</text>
      </view>
    </view>

    <view class="mode-row">
      <view
        v-for="item in modeOptions"
        :key="item.value"
        class="mode-chip"
        :class="{ active: selectedMode === item.value }"
        @tap="selectedMode = item.value"
      >
        <text>{{ item.label }}</text>
        <text>{{ quotaLeft(item.value) }} 次</text>
      </view>
    </view>

    <view class="filter-panel">
      <view class="filter-block">
        <text class="filter-label">性别</text>
        <view class="chip-row">
          <view
            v-for="item in genderOptions"
            :key="item.value"
            class="filter-chip"
            :class="{ active: selectedGender === item.value }"
            @tap="selectedGender = item.value"
          >
            {{ item.label }}
          </view>
        </view>
      </view>

      <view class="filter-block">
        <text class="filter-label">年龄</text>
        <view class="chip-row">
          <view
            v-for="item in ageOptions"
            :key="item.value"
            class="filter-chip"
            :class="{ active: selectedAgeRange === item.value }"
            @tap="selectedAgeRange = item.value"
          >
            {{ item.label }}
          </view>
        </view>
      </view>
    </view>

    <view class="start-button" :class="{ disabled: matching || currentQuotaLeft <= 0 }" @tap="startMatch">
      {{ matching ? '匹配中' : '开始匹配' }}
    </view>

    <view v-if="matchResult" class="result-card">
      <view class="result-top">
        <view class="avatar" />
        <view class="result-main">
          <text class="name">{{ matchResult.targetUser.nickname }}</text>
          <text class="meta">{{ genderLabel(matchResult.targetUser.gender) }} · {{ matchResult.targetUser.ageRange || '年龄未知' }} · {{ matchResult.targetUser.distanceText }}</text>
        </view>
        <text class="status">已匹配</text>
      </view>
      <view class="source-grid">
        <view>
          <text>房间</text>
          <text>{{ matchResult.roomId }}</text>
        </view>
        <view>
          <text>来源</text>
          <text>{{ matchResult.sourceType }}</text>
        </view>
        <view>
          <text>剩余</text>
          <text>{{ matchResult.quota.remaining }} 次</text>
        </view>
      </view>
      <view class="result-actions">
        <view class="secondary-button" @tap="resetMatch">再匹配</view>
        <view class="primary-button" @tap="openMessages">查看消息</view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { showToast, switchTab } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { BottleTargetGender, GameRandomMatch, GameRandomMatchMode } from '@/types/domain'

const app = useAppStore()
const content = useContentStore()
const selectedMode = ref<GameRandomMatchMode>('truth')
const selectedGender = ref<BottleTargetGender>('all')
const selectedAgeRange = ref('all')
const matching = ref(false)
const matchResult = ref<GameRandomMatch>()

const modeOptions: Array<{ value: GameRandomMatchMode; label: string }> = [
  { value: 'truth', label: '真心话' },
  { value: 'dare', label: '大冒险' }
]

const genderOptions: Array<{ value: BottleTargetGender; label: string }> = [
  { value: 'all', label: '全部' },
  { value: 'female', label: '女生' },
  { value: 'male', label: '男生' }
]

const ageOptions = [
  { value: 'all', label: '全部' },
  { value: '18-24', label: '18-24' },
  { value: '25-30', label: '25-30' },
  { value: '31-36', label: '31-36' },
  { value: '37+', label: '37+' }
]

const currentQuotaLeft = computed(() => quotaLeft(selectedMode.value))
const currentQuotaLabel = computed(() => (selectedMode.value === 'truth' ? '真心话次数' : '大冒险次数'))

onLoad(() => {
  void app.hydrate()
})

function quotaLeft(mode: GameRandomMatchMode) {
  return app.quotas?.[mode]?.remaining ?? 0
}

async function startMatch() {
  if (matching.value) return
  if (currentQuotaLeft.value <= 0) {
    showToast(`${currentQuotaLabel.value}不足`)
    return
  }
  matching.value = true
  try {
    matchResult.value = await content.startGameRandomMatch({
      mode: selectedMode.value,
      gender: selectedGender.value,
      ageRange: selectedAgeRange.value === 'all' ? undefined : selectedAgeRange.value,
      clientMatchId: `h5_${Date.now()}_${Math.random().toString(16).slice(2, 8)}`
    })
    showToast('匹配成功')
  } catch {
    showToast('暂时没有匹配对象')
  } finally {
    matching.value = false
  }
}

function resetMatch() {
  matchResult.value = undefined
}

function openMessages() {
  switchTab('/pages/messages/index')
}

function genderLabel(gender: BottleTargetGender | 'unknown') {
  if (gender === 'female') return '女生'
  if (gender === 'male') return '男生'
  return '不限'
}
</script>

<style scoped lang="scss">
.match-page {
  min-height: 100vh;
  min-height: 100dvh;
  padding: 28rpx 24rpx 128rpx;
  box-sizing: border-box;
  color: #fff;
  background:
    radial-gradient(circle at 18% 12%, rgba(34, 211, 238, 0.25), transparent 28%),
    radial-gradient(circle at 84% 18%, rgba(244, 114, 182, 0.22), transparent 28%),
    linear-gradient(180deg, #07111f 0%, #101a35 52%, #071225 100%);
}

.match-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
}

.kicker,
.title,
.quota-pill text,
.filter-label,
.name,
.meta,
.status {
  display: block;
}

.kicker {
  color: #22d3ee;
  font-size: 22rpx;
  font-weight: 900;
}

.title {
  margin-top: 6rpx;
  color: #f8fbff;
  font-size: 42rpx;
  font-weight: 900;
}

.quota-pill {
  flex: 0 0 auto;
  min-width: 138rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.14);
  border-radius: 18rpx;
  padding: 14rpx 18rpx;
  background: rgba(255, 255, 255, 0.08);
  text-align: center;
}

.quota-pill text:first-child {
  color: rgba(255, 255, 255, 0.62);
  font-size: 20rpx;
}

.quota-pill text:last-child {
  margin-top: 4rpx;
  color: #2dd4bf;
  font-size: 32rpx;
  font-weight: 900;
}

.mode-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
  margin-top: 30rpx;
}

.mode-chip,
.filter-panel,
.result-card {
  border: 1rpx solid rgba(255, 255, 255, 0.12);
  background: rgba(16, 25, 52, 0.82);
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.05);
}

.mode-chip {
  border-radius: 18rpx;
  padding: 20rpx;
}

.mode-chip.active {
  border-color: rgba(45, 212, 191, 0.55);
  background: linear-gradient(135deg, rgba(45, 212, 191, 0.28), rgba(37, 99, 235, 0.18));
}

.mode-chip text:first-child {
  display: block;
  font-size: 28rpx;
  font-weight: 900;
}

.mode-chip text:last-child {
  display: block;
  margin-top: 8rpx;
  color: #93a4c7;
  font-size: 22rpx;
}

.filter-panel {
  display: grid;
  gap: 24rpx;
  margin-top: 22rpx;
  border-radius: 20rpx;
  padding: 22rpx;
}

.filter-label {
  margin-bottom: 14rpx;
  color: #93a4c7;
  font-size: 23rpx;
  font-weight: 900;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.filter-chip {
  min-width: 104rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.12);
  border-radius: 999px;
  padding: 13rpx 18rpx;
  color: #dbeafe;
  background: rgba(255, 255, 255, 0.07);
  font-size: 23rpx;
  font-weight: 900;
  text-align: center;
  box-sizing: border-box;
}

.filter-chip.active {
  color: #071225;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
}

.start-button,
.primary-button,
.secondary-button {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 82rpx;
  border-radius: 999px;
  font-size: 27rpx;
  font-weight: 900;
}

.start-button {
  margin-top: 26rpx;
  color: #071225;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
}

.start-button.disabled {
  opacity: 0.55;
}

.result-card {
  margin-top: 26rpx;
  border-radius: 22rpx;
  padding: 22rpx;
}

.result-top {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.avatar {
  position: relative;
  overflow: hidden;
  width: 78rpx;
  height: 78rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.82);
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 34%, rgba(255, 255, 255, 0.88) 0 11rpx, transparent 12rpx),
    radial-gradient(circle at 50% 82%, rgba(255, 255, 255, 0.78) 0 24rpx, transparent 25rpx),
    linear-gradient(145deg, #22d3ee, #2563eb);
}

.result-main {
  min-width: 0;
  flex: 1;
}

.name {
  overflow: hidden;
  font-size: 30rpx;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta {
  margin-top: 6rpx;
  color: #93a4c7;
  font-size: 22rpx;
}

.status {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 8rpx 14rpx;
  color: #071225;
  background: #2dd4bf;
  font-size: 21rpx;
  font-weight: 900;
}

.source-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10rpx;
  margin-top: 20rpx;
}

.source-grid view {
  min-width: 0;
  border-radius: 14rpx;
  padding: 12rpx;
  background: rgba(255, 255, 255, 0.07);
}

.source-grid text {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.source-grid text:first-child {
  color: #93a4c7;
  font-size: 20rpx;
}

.source-grid text:last-child {
  margin-top: 5rpx;
  font-size: 22rpx;
  font-weight: 900;
}

.result-actions {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 14rpx;
  margin-top: 22rpx;
}

.secondary-button {
  color: #dbeafe;
  background: rgba(255, 255, 255, 0.09);
}

.primary-button {
  color: #071225;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
}
</style>
