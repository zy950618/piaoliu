<template>
  <view class="page creator-page safe-bottom">
    <view class="account-card">
      <view class="account-row">
        <view class="avatar-shell">
          <image class="avatar-image" :src="resolveAvatarUrl(app.user?.avatarUrl, app.user?.id || 'current-user')" mode="aspectFill" />
        </view>
        <view class="account-main">
          <view class="name-row">
            <text class="account-name">{{ app.user?.nickname || '匿名岛民' }}</text>
            <text class="status-chip" :class="{ verified }">{{ verified ? '已认证' : reviewText }}</text>
          </view>
          <text class="account-copy">{{ verified ? '收益权限已开通，礼物和内容收益会进入收益账户。' : '完成认证后开启礼物收益、内容收益和提现能力。' }}</text>
        </view>
      </view>

      <view class="primary-row">
        <view>
          <text class="primary-label">{{ verified ? '可提现收益' : '认证进度' }}</text>
          <text class="primary-value">{{ verified ? content.wallet?.withdrawableCoins || 0 : `${progressPercent}%` }}</text>
        </view>
        <button v-if="!verified" class="primary-action" hover-class="none" :class="{ disabled: submitting }" @tap="verifyFace">
          {{ submitting ? '提交中' : actionText }}
        </button>
        <view v-else class="done-state">
          <text class="done-dot"></text>
          <text>已完成</text>
        </view>
      </view>
    </view>

    <view v-if="verified" class="metric-grid">
      <view class="metric-card accent">
        <text class="metric-label">礼物收益</text>
        <text class="metric-value">{{ content.wallet?.giftCoins || 0 }}</text>
        <text class="metric-copy">聊天与广场礼物</text>
      </view>
      <view class="metric-card">
        <text class="metric-label">内容收益</text>
        <text class="metric-value">{{ content.wallet?.earnedCoins || 0 }}</text>
        <text class="metric-copy">照片查看等收益</text>
      </view>
      <view class="metric-card">
        <text class="metric-label">魅力值</text>
        <text class="metric-value">{{ content.wallet?.charmValue || 0 }}</text>
        <text class="metric-copy">门槛 {{ content.wallet?.withdrawThresholdCharm || 0 }}</text>
      </view>
      <view class="metric-card">
        <text class="metric-label">冻结中</text>
        <text class="metric-value">{{ content.wallet?.frozenCoins || 0 }}</text>
        <text class="metric-copy">等待风控复核</text>
      </view>
    </view>

    <view v-else class="section-card">
      <view class="section-head">
        <text class="section-title">认证流程</text>
        <text class="section-subtitle">通过后自动隐藏认证入口</text>
      </view>
      <view class="step-list">
        <view class="step-row" :class="{ done: content.verification?.livenessPassed }">
          <view class="step-mark">{{ content.verification?.livenessPassed ? '✓' : '1' }}</view>
          <view class="step-main">
            <text class="step-title">活体检测</text>
            <text class="step-copy">{{ content.verification?.livenessPassed ? '本人检测已通过' : '确认账号由本人使用' }}</text>
          </view>
        </view>
        <view class="step-row" :class="{ done: content.verification?.genderVerified }">
          <view class="step-mark">{{ content.verification?.genderVerified ? '✓' : '2' }}</view>
          <view class="step-main">
            <text class="step-title">资料识别</text>
            <text class="step-copy">当前性别：{{ genderText }}</text>
          </view>
        </view>
        <view class="step-row" :class="{ done: content.verification?.manualReviewStatus === 'approved' }">
          <view class="step-mark">{{ content.verification?.manualReviewStatus === 'approved' ? '✓' : '3' }}</view>
          <view class="step-main">
            <text class="step-title">人工复核</text>
            <text class="step-copy">{{ reviewText }}</text>
          </view>
        </view>
      </view>
    </view>

    <view class="section-card referral-card">
      <view class="section-head">
        <text class="section-title">邀请奖励</text>
        <text class="section-subtitle">邀请码 {{ content.referral?.inviteCode || '-' }}</text>
      </view>
      <view class="invite-progress">
        <view class="invite-copy-row">
          <text class="invite-count">{{ content.referral?.invitedCount || 0 }}/{{ content.referral?.nextRewardNeed || 0 }}</text>
          <text class="invite-desc">达标领取 {{ content.referral?.rewardVipDays || 0 }} 天会员</text>
        </view>
        <button class="secondary-action" hover-class="none" @tap="claimReferral">领取</button>
      </view>
    </view>

    <view class="section-card rules-card">
      <view class="section-head compact">
        <text class="section-title">收益规则</text>
        <text class="section-subtitle">平台风控复核</text>
      </view>
      <view class="rule-row">
        <text class="rule-label">充值币</text>
        <text class="rule-copy">只能消费，不能提现。</text>
      </view>
      <view class="rule-row">
        <text class="rule-label">收益币</text>
        <text class="rule-copy">礼物和内容收益会转为魅力值，达到门槛后申请提现。</text>
      </view>
      <view class="rule-row">
        <text class="rule-label">风控</text>
        <text class="rule-copy">异常拉新、诱导充值、被举报内容会冻结收益。</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import { resolveAvatarUrl } from '@/utils/avatar'

const app = useAppStore()
const content = useContentStore()
const submitting = ref(false)

const verified = computed(() => {
  const state = content.verification
  return Boolean(state?.faceVerified && state.genderVerified && state.livenessPassed && state.manualReviewStatus === 'approved')
})

const progressPercent = computed(() => {
  const state = content.verification
  if (!state) return 0
  const passed = [state.livenessPassed, state.genderVerified, state.manualReviewStatus === 'approved'].filter(Boolean).length
  return Math.round((passed / 3) * 100)
})

const actionText = computed(() => {
  const status = content.verification?.manualReviewStatus
  if (status === 'pending') return '重新提交'
  if (status === 'rejected') return '再次认证'
  return '开始认证'
})

const genderText = computed(() => {
  const gender = content.verification?.detectedGender
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
})

const reviewText = computed(() => {
  const status = content.verification?.manualReviewStatus
  if (status === 'approved') return '审核通过'
  if (status === 'pending') return '审核中'
  if (status === 'rejected') return '审核未通过'
  return '未提交'
})

onLoad(async () => {
  await Promise.all([app.hydrate(), content.loadWallet(), content.loadVerification()])
})

async function verifyFace() {
  if (verified.value || submitting.value) return
  submitting.value = true
  try {
    await content.submitFaceVerification()
    showToast('已提交认证，等待人工复核')
  } finally {
    submitting.value = false
  }
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
.creator-page {
  min-height: 100vh;
  padding-top: 24rpx;
  padding-bottom: 48rpx;
  background: linear-gradient(180deg, #f7faf8 0%, #eef4f1 100%);
}

.account-card,
.section-card,
.metric-card {
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 12rpx 28rpx rgba(31, 54, 58, 0.055);
}

.account-card {
  padding: 26rpx;
}

.account-row {
  display: grid;
  grid-template-columns: 88rpx minmax(0, 1fr);
  gap: 18rpx;
  align-items: center;
}

.avatar-shell {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(145deg, #236c72, #6f8f72);
  font-size: 32rpx;
  font-weight: 900;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
}

.account-main {
  min-width: 0;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
  min-width: 0;
}

.account-name,
.account-copy,
.primary-label,
.primary-value,
.metric-label,
.metric-value,
.metric-copy,
.section-title,
.section-subtitle,
.step-title,
.step-copy,
.invite-count,
.invite-desc {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-name {
  min-width: 0;
  color: #172126;
  font-size: 31rpx;
  font-weight: 900;
}

.status-chip {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 7rpx 12rpx;
  color: #8a5a10;
  background: rgba(194, 122, 53, 0.13);
  font-size: 20rpx;
  font-weight: 900;
  line-height: 1.1;
}

.status-chip.verified {
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
}

.account-copy {
  margin-top: 8rpx;
  color: #65757b;
  font-size: 23rpx;
  line-height: 1.35;
  white-space: normal;
}

.primary-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 18rpx;
  margin-top: 28rpx;
  border-top: 1px solid rgba(23, 33, 38, 0.07);
  padding-top: 22rpx;
}

.primary-label {
  color: #65757b;
  font-size: 22rpx;
  font-weight: 800;
}

.primary-value {
  margin-top: 7rpx;
  color: #172126;
  font-size: 48rpx;
  font-weight: 900;
  line-height: 1;
}

.primary-action,
.secondary-action {
  margin: 0;
  border: 0;
  border-radius: 8px;
  box-sizing: border-box;
  font-weight: 900;
}

.primary-action::after,
.secondary-action::after {
  display: none;
}

.primary-action {
  flex: 0 0 auto;
  min-width: 168rpx;
  height: 68rpx;
  padding: 0 20rpx;
  color: #fff;
  background: #236c72;
  font-size: 25rpx;
  line-height: 68rpx;
}

.primary-action.disabled {
  color: #8d989e;
  background: #dbe4e0;
}

.done-state {
  display: inline-flex;
  align-items: center;
  gap: 9rpx;
  min-height: 46rpx;
  border-radius: 999px;
  padding: 0 14rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.08);
  font-size: 22rpx;
  font-weight: 900;
}

.done-dot {
  width: 13rpx;
  height: 13rpx;
  border-radius: 50%;
  background: #236c72;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 16rpx;
}

.metric-card {
  min-height: 136rpx;
  padding: 20rpx;
}

.metric-card.accent {
  border-color: rgba(35, 108, 114, 0.16);
  background: linear-gradient(180deg, rgba(238, 248, 244, 0.98), rgba(255, 255, 255, 0.96));
}

.metric-label {
  color: #65757b;
  font-size: 21rpx;
  font-weight: 800;
}

.metric-value {
  margin-top: 8rpx;
  color: #172126;
  font-size: 38rpx;
  font-weight: 900;
  line-height: 1;
}

.accent .metric-value {
  color: #236c72;
}

.metric-copy {
  margin-top: 7rpx;
  color: #8a969b;
  font-size: 20rpx;
}

.section-card {
  margin-top: 16rpx;
  padding: 24rpx;
}

.section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18rpx;
  margin-bottom: 18rpx;
}

.section-head.compact {
  margin-bottom: 8rpx;
}

.section-title {
  color: #172126;
  font-size: 29rpx;
  font-weight: 900;
}

.section-subtitle {
  max-width: 330rpx;
  color: #65757b;
  font-size: 21rpx;
  font-weight: 700;
  text-align: right;
}

.step-list {
  display: grid;
  gap: 4rpx;
}

.step-row {
  display: grid;
  grid-template-columns: 54rpx minmax(0, 1fr);
  gap: 14rpx;
  align-items: center;
  padding: 13rpx 0;
}

.step-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46rpx;
  height: 46rpx;
  border-radius: 50%;
  color: #65757b;
  background: rgba(23, 33, 38, 0.07);
  font-size: 21rpx;
  font-weight: 900;
}

.step-row.done .step-mark {
  color: #fff;
  background: #236c72;
}

.step-main {
  min-width: 0;
}

.step-title {
  color: #172126;
  font-size: 25rpx;
  font-weight: 900;
}

.step-copy {
  margin-top: 5rpx;
  color: #65757b;
  font-size: 21rpx;
}

.invite-progress {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 118rpx;
  gap: 16rpx;
  align-items: center;
}

.invite-copy-row {
  min-width: 0;
}

.invite-count {
  color: #172126;
  font-size: 32rpx;
  font-weight: 900;
}

.invite-desc {
  margin-top: 5rpx;
  color: #65757b;
  font-size: 22rpx;
}

.secondary-action {
  width: 118rpx;
  height: 60rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
  font-size: 23rpx;
  line-height: 60rpx;
}

.rule-row {
  display: grid;
  grid-template-columns: 110rpx minmax(0, 1fr);
  gap: 14rpx;
  padding: 17rpx 0;
  border-bottom: 1px solid rgba(23, 33, 38, 0.07);
}

.rule-row:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}

.rule-label {
  color: #236c72;
  font-size: 23rpx;
  font-weight: 900;
}

.rule-copy {
  color: #334348;
  font-size: 23rpx;
  line-height: 1.45;
}
</style>
