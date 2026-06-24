<template>
  <view class="page safe-bottom">
    <QuotaGrid :items="app.quotaList" />

    <view class="section panel">
      <text class="h2">大冒险</text>
      <text class="muted intro">任务偏轻量，不强迫社交暴露。抽到任务后扣除 1 次大冒险次数。</text>
      <view class="category-row">
        <text v-for="item in categories" :key="item" class="tag">{{ item }}</text>
      </view>
      <view class="button" @tap="draw">抽一个任务</view>
    </view>

    <view v-if="content.currentDare" class="section panel">
      <text class="tag">{{ content.currentDare.category }}</text>
      <text class="question">{{ content.currentDare.text }}</text>
      <view class="grid-2 action-row">
        <view class="button secondary" @tap="finish">标记完成</view>
        <view class="button ghost" @tap="skip">换一个想法</view>
      </view>
      <text class="muted note">上传凭证、审核展示会在后端接入后开放。</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
import QuotaGrid from '@/components/QuotaGrid.vue'
import { useQuotaGuard } from '@/composables/useQuotaGuard'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'

const app = useAppStore()
const content = useContentStore()
const { ensureQuota } = useQuotaGuard()
const categories = ['轻松', '社交', '拍照', '文字挑战']

onLoad(() => app.hydrate())

async function draw() {
  if (!ensureQuota('dare')) return
  await content.drawDareTask()
  showToast('已抽到大冒险，大冒险次数 -1')
}

function finish() {
  showToast('完成记录已保存')
}

function skip() {
  showToast('换任务需要再次抽取并扣次数')
}
</script>

<style scoped lang="scss">
.intro,
.note {
  display: block;
  margin-top: 12rpx;
}

.category-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin: 20rpx 0 22rpx;
}

.question {
  display: block;
  margin-top: 18rpx;
  color: #25323c;
  font-size: 34rpx;
  font-weight: 700;
  line-height: 1.45;
}

.action-row {
  margin-top: 26rpx;
}
</style>
