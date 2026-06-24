<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">拉新活动</text>
        <text class="muted">邀请好友获得会员奖励</text>
      </view>
    </view>

    <view class="section panel referral-card">
      <text class="muted">我的邀请码</text>
      <text class="invite-code">{{ content.referral?.inviteCode || 'SEA260' }}</text>
      <text class="muted">已邀请 {{ content.referral?.invitedCount || 0 }}/{{ content.referral?.nextRewardNeed || 5 }}</text>
    </view>

    <view class="section button" @tap="claimReferral">领取奖励</view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'

const content = useContentStore()

onLoad(() => content.loadVerification())

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
.referral-card {
  display: grid;
  gap: 12rpx;
}

.invite-code {
  color: #236c72;
  font-size: 52rpx;
  font-weight: 900;
  line-height: 1.2;
}
</style>
