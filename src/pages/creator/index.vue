<template>
  <view class="page safe-bottom">
    <view class="panel creator-hero">
      <text class="title">人脸认证</text>
      <text class="body intro">完成活体检测、男女识别和人工复核后，才可开启私密照片收益、礼物收益和魅力值提现。</text>
      <view class="button hero-button" @tap="verifyFace">开始认证</view>
    </view>

    <view class="section panel verify-panel">
      <view class="between">
        <view>
          <text class="h2">认证状态</text>
          <text class="muted">活体：{{ content.verification?.livenessPassed ? '通过' : '未通过' }} · 性别：{{ genderText }} · 复核：{{ reviewText }}</text>
        </view>
        <AppIcon name="verify" tone="rose" />
      </view>
    </view>

    <view class="section panel referral-panel">
      <view class="between">
        <view>
          <text class="h2">拉新赠会员</text>
          <text class="muted">邀请码 {{ content.referral?.inviteCode || '-' }} · 已邀请 {{ content.referral?.invitedCount || 0 }}/{{ content.referral?.nextRewardNeed || 0 }}</text>
        </view>
        <view class="button secondary referral-button" @tap="claimReferral">领取</view>
      </view>
    </view>

    <view class="section panel">
      <text class="h2">收益规则</text>
      <view class="rule-row">
        <text class="body">充值金币只能消费，不能提现。</text>
      </view>
      <view class="rule-row">
        <text class="body">照片查看和礼物收益会转为魅力值，达到门槛后申请提现。</text>
      </view>
      <view class="rule-row">
        <text class="body">异常拉新、诱导充值、被举报内容会冻结收益和魅力值。</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import AppIcon from '@/components/AppIcon.vue'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'

const content = useContentStore()

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

onLoad(async () => {
  await content.loadWallet()
  await content.loadVerification()
})

async function verifyFace() {
  await content.submitFaceVerification()
  showToast('已提交人脸识别和性别识别，等待人工复核')
}

async function claimReferral() {
  try {
    await content.claimReferralVip()
    showToast('拉新会员奖励已到账')
  } catch {
    showToast('邀请人数未达标')
  }
}
</script>

<style scoped lang="scss">
.creator-hero {
  background: rgba(255, 255, 255, 0.86);
}

.intro {
  display: block;
  margin: 18rpx 0;
}

.hero-button {
  width: 190rpx;
}

.verify-panel {
  background: rgba(191, 91, 115, 0.08);
}

.referral-panel {
  background: rgba(255, 105, 0, 0.08);
}

.referral-button {
  width: 120rpx;
  min-height: 66rpx;
}

.rule-row {
  padding: 20rpx 0;
  border-bottom: 1px solid rgba(29, 29, 31, 0.08);
}
</style>
