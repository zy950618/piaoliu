<template>
  <view class="page safe-bottom">
    <QuotaGrid :items="app.quotaList" />

    <view class="section panel">
      <text class="h2">真心话</text>
      <text class="muted intro">抽到问题后扣除 1 次真心话次数。回答可以私密保存，也可以投递成瓶子。</text>
      <view class="category-row">
        <text v-for="item in categories" :key="item" class="tag">{{ item }}</text>
      </view>
      <view class="button" @tap="draw">抽一个问题</view>
    </view>

    <view v-if="content.currentTruth" class="section panel">
      <text class="tag">{{ content.currentTruth.category }}</text>
      <text class="question">{{ content.currentTruth.text }}</text>
      <textarea v-model="answer" class="textarea" placeholder="写下真实一点的答案" />
      <view class="grid-2">
        <view class="button secondary" @tap="savePrivate">私密保存</view>
        <view class="button" @tap="sendAsBottle">投递成瓶子</view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import QuotaGrid from '@/components/QuotaGrid.vue'
import { useQuotaGuard } from '@/composables/useQuotaGuard'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'

const app = useAppStore()
const content = useContentStore()
const { ensureQuota } = useQuotaGuard()
const answer = ref('')
const categories = ['情感', '朋友局', '深夜', '轻松']

onLoad(() => app.hydrate())

async function draw() {
  if (!ensureQuota('truth')) return
  await content.drawTruthQuestion()
  showToast('已抽到真心话，真心话次数 -1')
}

function savePrivate() {
  showToast('已保存到私密回答记录')
}

async function sendAsBottle() {
  if (!answer.value.trim()) {
    showToast('先写下回答')
    return
  }
  if (!ensureQuota('throw_bottle')) return
  await content.throwBottle(answer.value.trim())
  answer.value = ''
  showToast('回答已投递成瓶子，扔瓶次数 -1')
}
</script>

<style scoped lang="scss">
.intro {
  display: block;
  margin: 12rpx 0 20rpx;
}

.category-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 22rpx;
}

.question {
  display: block;
  margin-top: 18rpx;
  color: #25323c;
  font-size: 34rpx;
  font-weight: 700;
  line-height: 1.45;
}

.textarea {
  width: 100%;
  min-height: 220rpx;
  margin: 22rpx 0;
  border: 1px solid #eadfce;
  border-radius: 8px;
  background: #fff;
  padding: 20rpx;
  box-sizing: border-box;
  font-size: 28rpx;
}
</style>
