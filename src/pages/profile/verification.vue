<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">人脸认证</text>
        <text class="muted">活体检测、性别识别和人工复核状态</text>
      </view>
      <text v-if="verified" class="verified-badge">已认证</text>
    </view>

    <view class="section panel">
      <view class="status-row">
        <text class="label">活体检测</text>
        <text class="tag">{{ content.verification?.livenessPassed ? '通过' : '未通过' }}</text>
      </view>
      <view class="status-row">
        <text class="label">识别性别</text>
        <text class="tag">{{ genderText }}</text>
      </view>
      <view class="status-row">
        <text class="label">人工复核</text>
        <text class="tag">{{ reviewText }}</text>
      </view>
    </view>

    <view v-if="verified" class="section completed-panel">
      <text class="completed-title">认证已生效</text>
      <text class="completed-copy">你的资料会展示已认证标识，认证入口不再重复出现。</text>
    </view>
    <view v-else class="section button" @tap="verifyFace">提交认证</view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'

const content = useContentStore()

onLoad(() => content.loadVerification())

const verified = computed(() => {
  const state = content.verification
  return Boolean(state?.faceVerified && state.genderVerified && state.livenessPassed && state.manualReviewStatus === 'approved')
})

const genderText = computed(() => {
  const gender = content.verification?.detectedGender
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
})

const reviewText = computed(() => {
  const status = content.verification?.manualReviewStatus
  if (status === 'approved') return '通过'
  if (status === 'pending') return '审核中'
  if (status === 'rejected') return '拒绝'
  return '未提交'
})

async function verifyFace() {
  if (verified.value) {
    showToast('认证已完成')
    return
  }
  await content.submitFaceVerification()
  showToast('已提交认证，等待人工复核')
}
</script>

<style scoped lang="scss">
.page-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
}

.verified-badge {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 10rpx 16rpx;
  color: #fff;
  background: #ef3e36;
  font-size: 23rpx;
  font-weight: 900;
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  padding: 22rpx 0;
  border-bottom: 1px solid rgba(23, 33, 38, 0.08);
}

.status-row:last-child {
  border-bottom: 0;
}

.label {
  color: #172126;
  font-size: 28rpx;
  font-weight: 800;
}

.completed-panel {
  border: 1px solid rgba(35, 108, 114, 0.1);
  border-radius: 8px;
  padding: 24rpx;
  background: rgba(35, 108, 114, 0.08);
}

.completed-title,
.completed-copy {
  display: block;
}

.completed-title {
  color: #236c72;
  font-size: 30rpx;
  font-weight: 900;
}

.completed-copy {
  margin-top: 8rpx;
  color: #65757b;
  font-size: 24rpx;
  line-height: 1.45;
}
</style>
