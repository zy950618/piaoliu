<template>
  <view class="page safe-bottom">
    <QuotaGrid :items="app.quotaList" />

    <view class="section panel">
      <text class="h2">真心话</text>
      <text class="muted intro">先选择投递对象，再决定捞一个问题或把当前真心话扔出去。</text>
      <view class="gender-row">
        <view
          v-for="item in genderOptions"
          :key="item.value"
          class="gender-chip"
          :class="[item.value, { active: targetGender === item.value }]"
          @tap="targetGender = item.value"
        >
          <text class="gender-mark">{{ item.mark }}</text>
          <text>{{ item.label }}</text>
        </view>
      </view>
      <view class="category-row">
        <text v-for="item in categories" :key="item" class="tag">{{ item }}</text>
      </view>
      <view class="grid-2 truth-actions">
        <view class="button secondary" @tap="draw">捞一个</view>
        <view class="button" @tap="sendAsBottle">扔出去</view>
      </view>
    </view>

    <view v-if="content.currentTruth" class="section panel">
      <text class="tag">{{ content.currentTruth.category }}</text>
      <text class="question">{{ content.currentTruth.text }}</text>
      <textarea v-model="answer" class="textarea" placeholder="写下真实一点的答案" />
      <view class="grid-2">
        <view class="button secondary" @tap="draw">继续捞</view>
        <view class="button" @tap="sendAsBottle">扔这个</view>
      </view>
      <view class="save-link" @tap="savePrivate">私密保存</view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import QuotaGrid from '@/components/QuotaGrid.vue'
import { useQuotaGuard } from '@/composables/useQuotaGuard'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { BottleTargetGender } from '@/types/domain'

type TruthTargetGender = Exclude<BottleTargetGender, 'all'>

const app = useAppStore()
const content = useContentStore()
const { ensureQuota } = useQuotaGuard()
const answer = ref('')
const targetGender = ref<TruthTargetGender>('female')
const categories = ['情感', '朋友局', '深夜', '轻松']
const genderOptions: Array<{ value: TruthTargetGender; label: string; mark: string }> = [
  { value: 'female', label: '女生', mark: '♀' },
  { value: 'male', label: '男生', mark: '♂' }
]
const targetGenderLabel = computed(() => genderOptions.find((item) => item.value === targetGender.value)?.label || '对方')

onLoad(() => app.hydrate())

async function draw() {
  if (!ensureQuota('truth')) return
  await content.drawTruthQuestion()
  answer.value = ''
  showToast(`已为${targetGenderLabel.value}捞到真心话，真心话次数 -1`)
}

async function savePrivate() {
  if (!content.currentTruth) {
    showToast('先抽一个问题')
    return
  }
  const trimmed = answer.value.trim()
  await content.saveUserActivityRecord({
    recordType: 'truth',
    title: content.currentTruth.category,
    content: trimmed ? `${content.currentTruth.text}\n${trimmed}` : content.currentTruth.text,
    visibility: 'private',
    sourceType: 'truth',
    sourceId: content.currentTruth.id
  })
  showToast('已保存到私密回答记录')
}

async function sendAsBottle() {
  if (!content.currentTruth) {
    showToast('先捞一个真心话')
    return
  }
  if (!ensureQuota('throw_bottle')) return
  await content.throwBottle(truthBottleContent(), { targetGender: targetGender.value })
  answer.value = ''
  showToast(`已扔给${targetGenderLabel.value}，扔瓶次数 -1`)
}

function truthBottleContent() {
  const question = content.currentTruth?.text || ''
  const trimmed = answer.value.trim()
  return trimmed ? `${question}\n${trimmed}` : question
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

.gender-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14rpx;
  margin: 18rpx 0;
}

.gender-chip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  min-height: 82rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 14px;
  color: #334155;
  background: linear-gradient(180deg, #fff, #f8fafc);
  font-size: 26rpx;
  font-weight: 900;
  box-shadow: 0 10rpx 24rpx rgba(15, 23, 42, 0.05);
}

.gender-chip.active {
  color: #fff;
  border-color: transparent;
  box-shadow: 0 18rpx 34rpx rgba(37, 99, 235, 0.18);
}

.gender-chip.female.active {
  background: linear-gradient(145deg, #f472b6, #db2777);
}

.gender-chip.male.active {
  background: linear-gradient(145deg, #38bdf8, #2563eb);
}

.gender-mark {
  font-size: 32rpx;
  line-height: 1;
}

.truth-actions {
  margin-top: 6rpx;
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

.save-link {
  margin-top: 18rpx;
  color: #64748b;
  font-size: 24rpx;
  font-weight: 800;
  text-align: center;
}
</style>
