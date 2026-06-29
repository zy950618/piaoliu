<template>
  <view class="page profile-page safe-bottom">
    <view class="panel profile-card" :class="{ 'vip-active': app.user?.isVip }">
      <view v-if="app.user?.isVip" class="vip-plate" @tap="go('/pages/membership/index')">
        <view class="vip-plate-main">
          <VipBadge variant="ribbon" label="BLACK" glow />
          <view class="vip-ribbon-copy">
            <text class="vip-eyebrow">DRIFT BLACK</text>
            <text class="vip-copy">尊享会员</text>
            <text class="vip-expire">{{ vipExpireText }}</text>
          </view>
        </view>
        <text class="vip-plate-arrow">›</text>
      </view>

      <view class="row profile-row">
        <view class="avatar" @tap="go('/pages/profile/settings')">
          <image v-if="app.user?.avatarUrl" class="avatar-image" :src="app.user.avatarUrl" mode="aspectFill" />
          <text v-else>{{ app.user?.avatarText || '海' }}</text>
        </view>
        <view class="profile-main">
          <view class="row name-row">
            <text class="title">{{ app.user?.nickname || '匿名岛民' }}</text>
            <VipBadge v-if="app.user?.isVip" class="inline-vip" variant="mini" glow />
            <text class="gender-pill">{{ userGenderText }}</text>
          </view>
          <view class="user-id-row" @tap="copyUserId">
            <text class="muted">ID {{ displayUserId }}</text>
            <text class="copy-pill">复制</text>
          </view>
        </view>
        <view class="edit-pill" @tap="go('/pages/profile/settings')">编辑</view>
      </view>

      <view class="grid-2 profile-stats">
        <view class="stat">
          <text class="stat-value">{{ app.user?.driftCoins || 0 }}</text>
          <text class="muted">漂流币</text>
        </view>
        <view class="stat sign-stat">
          <view>
            <text class="stat-value">{{ app.checkin?.streakDays || 0 }}</text>
            <text class="muted">连续签到</text>
          </view>
          <view class="sign-mini-button" @tap="go('/pages/profile/checkin')">去签到</view>
        </view>
      </view>
    </view>

    <view class="section quick-grid">
      <view class="quick-card primary" @tap="go('/pages/membership/index')">
        <text class="quick-title">会员中心</text>
        <text class="quick-copy">权益、次数加成</text>
      </view>
      <view class="quick-card" @tap="go('/pages/wallet/index')">
        <text class="quick-title">金币钱包</text>
        <text class="quick-copy">余额、流水、提现</text>
      </view>
      <view class="quick-card" @tap="go('/pages/creator/index')">
        <text class="quick-title">{{ verified ? '收益中心' : '认证与收益' }}</text>
        <text class="quick-copy">{{ verified ? '礼物收益、魅力值、提现' : '认证后开启收益能力' }}</text>
      </view>
    </view>

    <view class="section panel list-panel">
      <view v-for="item in menuItems" :key="item.title" class="menu-row" @tap="go(item.url)">
        <view class="menu-icon" :class="`menu-icon-${item.icon}`" aria-hidden="true" />
        <view class="menu-main">
          <text class="menu-title">{{ item.title }}</text>
          <text class="muted">{{ item.desc }}</text>
        </view>
        <text v-if="item.badge" class="menu-badge">{{ item.badge }}</text>
        <text class="menu-arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import VipBadge from '@/components/VipBadge.vue'
import { navigateTo, showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'

const app = useAppStore()
const content = useContentStore()

onLoad(async () => {
  await app.refreshStatus()
  await Promise.all([content.loadVerification(), content.loadBlacklist()])
})

const verified = computed(() => {
  const state = content.verification
  return Boolean(state?.faceVerified && state.genderVerified && state.livenessPassed && state.manualReviewStatus === 'approved')
})

const menuItems = computed(() => {
  const items = [
    { icon: 'settings', title: '用户设置', desc: '头像、昵称和个人资料', url: '/pages/profile/settings', badge: '' },
    { icon: 'invite', title: '拉新活动', desc: '邀请码、邀请进度、会员奖励', url: '/pages/profile/referral', badge: '' },
    { icon: 'block', title: '黑名单', desc: '查看已屏蔽的人和原因', url: '/pages/profile/blacklist', badge: '' },
    { icon: 'records', title: '我的记录', desc: '瓶子、树洞、游戏和举报记录', url: '/pages/profile/records', badge: '' }
  ]
  if (!verified.value) {
    items.splice(1, 0, {
      icon: 'verify',
      title: '人脸认证',
      desc: '活体、性别识别、人工复核',
      url: '/pages/profile/verification',
      badge: ''
    })
  }
  return items
})

const userGenderText = computed(() => {
  const gender = app.user?.gender
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
})

const vipExpireText = computed(() => {
  if (!app.user?.vipExpiresAt) return '有效期未同步'
  return `有效期至 ${formatDate(app.user.vipExpiresAt)}`
})

const displayUserId = computed(() => app.user?.id || '-')

function formatDate(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value.slice(0, 10)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${date.getFullYear()}.${month}.${day}`
}

function go(url: string) {
  navigateTo(url)
}

function copyUserId() {
  const userId = app.user?.id
  if (!userId) return
  if (typeof uni !== 'undefined' && uni.setClipboardData) {
    uni.setClipboardData({
      data: userId,
      success: () => showToast('用户 ID 已复制')
    })
    return
  }
  showToast(userId)
}
</script>

<style scoped lang="scss">
.profile-page {
  padding-top: 30rpx;
  background:
    radial-gradient(circle at 18% -8%, rgba(37, 99, 235, 0.06), transparent 30%),
    radial-gradient(circle at 90% 4%, rgba(15, 118, 110, 0.06), transparent 28%),
    linear-gradient(180deg, #ffffff, #f8fafc 58%, #f1f5f9);
}

.profile-card {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.9)),
    radial-gradient(circle at 90% 10%, rgba(37, 99, 235, 0.05), transparent 32%);
}

.profile-card.vip-active {
  padding-top: 22rpx;
  border-color: rgba(15, 23, 42, 0.1);
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.99), rgba(248, 250, 252, 0.94)),
    radial-gradient(circle at 88% 10%, rgba(15, 23, 42, 0.05), transparent 30%);
  box-shadow: 0 22rpx 52rpx rgba(15, 23, 42, 0.08);
}

.profile-card.vip-active::before {
  position: absolute;
  top: 0;
  left: 28rpx;
  right: 28rpx;
  height: 5rpx;
  border-radius: 0 0 999px 999px;
  background: linear-gradient(90deg, #111827, #d8b76a, #111827);
  content: '';
}

.profile-card.vip-active .title,
.profile-card.vip-active .muted {
  color: #0f172a;
}

.profile-card.vip-active .stat {
  border-color: rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.82);
}

.profile-card.vip-active .stat-value {
  color: #111827;
}

.vip-plate {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
  min-height: 88rpx;
  margin-bottom: 24rpx;
  border: 1px solid rgba(230, 184, 92, 0.34);
  border-radius: 16px;
  padding: 14rpx 18rpx;
  color: #f8e8b0;
  background:
    radial-gradient(circle at 12% 0%, rgba(248, 223, 158, 0.24), transparent 36%),
    radial-gradient(circle at 94% 12%, rgba(148, 163, 184, 0.14), transparent 36%),
    linear-gradient(135deg, #07080d 0%, #171d27 52%, #050506 100%);
  box-sizing: border-box;
  box-shadow:
    inset 0 1rpx 0 rgba(255, 255, 255, 0.16),
    0 18rpx 42rpx rgba(15, 23, 42, 0.18);
}

.vip-plate::after {
  position: absolute;
  inset: 0;
  background: linear-gradient(112deg, transparent 0%, rgba(248, 223, 158, 0.16) 44%, transparent 62%);
  transform: translateX(-120%);
  animation: vipSweep 3.2s ease-in-out infinite;
  content: '';
}

.vip-plate-main {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 14rpx;
  min-width: 0;
}

.vip-active .avatar {
  color: #fff;
  background:
    radial-gradient(circle at 32% 24%, rgba(255, 255, 255, 0.35), transparent 30%),
    linear-gradient(145deg, #38bdf8, #2563eb);
  box-shadow: 0 14rpx 32rpx rgba(37, 99, 235, 0.2);
}

.vip-eyebrow,
.vip-copy {
  display: block;
}

.vip-eyebrow {
  color: rgba(248, 223, 158, 0.64);
  font-size: 17rpx;
  font-weight: 900;
  line-height: 1;
}

.vip-copy {
  margin-top: 4rpx;
  color: #fff4cf;
  font-size: 26rpx;
  font-weight: 900;
  line-height: 1.05;
}

.vip-ribbon-copy {
  min-width: 0;
  flex: 1;
}

.vip-expire {
  display: block;
  margin-top: 4rpx;
  overflow: hidden;
  color: rgba(248, 223, 158, 0.72);
  font-size: 19rpx;
  font-weight: 800;
  line-height: 1.15;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vip-plate-arrow {
  position: relative;
  z-index: 1;
  flex: 0 0 auto;
  color: #f8d37b;
  font-size: 40rpx;
  font-weight: 800;
  line-height: 1;
}

.profile-row {
  gap: 18rpx;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex: 0 0 auto;
  width: 96rpx;
  height: 96rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.92);
  border-radius: 50%;
  color: #fff;
  background: #2563eb;
  box-shadow: 0 12rpx 28rpx rgba(37, 99, 235, 0.18);
  font-size: 36rpx;
  font-weight: 800;
}

.avatar-image {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.profile-main {
  flex: 1;
  min-width: 0;
}

.name-row {
  gap: 10rpx;
  min-width: 0;
}

.title {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.inline-vip {
  margin-left: 2rpx;
}

.gender-pill,
.edit-pill,
.copy-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 5rpx 13rpx;
  color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
  font-size: 21rpx;
  font-weight: 800;
  line-height: 1.2;
}

.edit-pill {
  align-self: flex-start;
  margin-top: 8rpx;
}

.user-id-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
  margin-top: 8rpx;
}

.user-id-row .muted {
  min-width: 0;
  max-width: 210rpx;
  overflow: hidden;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  color: #475569;
  font-size: 21rpx;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@keyframes vipSweep {
  0%,
  48% {
    transform: translateX(-120%);
  }

  72%,
  100% {
    transform: translateX(120%);
  }
}

.profile-stats {
  margin-top: 24rpx;
}

.stat {
  min-height: 118rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.72);
  padding: 22rpx;
  box-sizing: border-box;
}

.sign-stat {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
}

.stat-value {
  display: block;
  color: #2563eb;
  font-size: 34rpx;
  font-weight: 800;
}

.sign-mini-button {
  flex: 0 0 auto;
  border-radius: 12px;
  padding: 14rpx 18rpx;
  color: #fff;
  background: #2563eb;
  font-size: 23rpx;
  font-weight: 900;
  line-height: 1;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
}

.quick-card {
  min-height: 132rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 16px;
  padding: 22rpx;
  background: rgba(255, 255, 255, 0.88);
  box-sizing: border-box;
  box-shadow: 0 14rpx 32rpx rgba(15, 23, 42, 0.06);
  transition: transform 160ms ease, box-shadow 160ms ease;
}

.quick-card:active {
  transform: scale(0.985);
}

.quick-card:hover {
  transform: translateY(-3rpx);
  box-shadow: 0 22rpx 48rpx rgba(15, 23, 42, 0.12);
}

.quick-card.primary {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.quick-card.primary .quick-title,
.quick-card.primary .quick-copy {
  color: #fff;
}

.quick-title,
.quick-copy {
  display: block;
}

.quick-title {
  color: #172126;
  font-size: 28rpx;
  font-weight: 900;
}

.quick-copy {
  margin-top: 10rpx;
  color: #65757b;
  font-size: 23rpx;
  line-height: 1.35;
}

.list-panel {
  padding: 6rpx 24rpx;
  border-radius: 16px;
}

.menu-badge {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 7rpx 13rpx;
  color: #fff;
  background: #ef3e36;
  font-size: 21rpx;
  font-weight: 900;
  line-height: 1.2;
}

.menu-row {
  display: flex;
  align-items: center;
  gap: 18rpx;
  min-height: 108rpx;
  border-bottom: 1px solid rgba(23, 33, 38, 0.08);
  transition: transform 150ms ease, background 150ms ease;
}

.menu-row:active {
  transform: scale(0.992);
}

.menu-row:last-child {
  border-bottom: 0;
}

.menu-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 64rpx;
  height: 64rpx;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 18rpx;
  color: #2563eb;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.92));
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.9), 0 8rpx 18rpx rgba(15, 23, 42, 0.06);
}

.menu-icon::before,
.menu-icon::after {
  position: absolute;
  content: '';
  box-sizing: border-box;
}

.menu-icon-settings::before {
  width: 30rpx;
  height: 30rpx;
  border: 5rpx solid currentColor;
  border-radius: 50%;
  box-shadow: 0 -16rpx 0 -10rpx currentColor, 0 16rpx 0 -10rpx currentColor, 16rpx 0 0 -10rpx currentColor, -16rpx 0 0 -10rpx currentColor;
}

.menu-icon-settings::after {
  width: 10rpx;
  height: 10rpx;
  border-radius: 50%;
  background: currentColor;
}

.menu-icon-verify::before {
  width: 32rpx;
  height: 36rpx;
  border: 4rpx solid currentColor;
  border-radius: 18rpx 18rpx 14rpx 14rpx;
}

.menu-icon-verify::after {
  width: 18rpx;
  height: 10rpx;
  border-left: 4rpx solid currentColor;
  border-bottom: 4rpx solid currentColor;
  transform: rotate(-45deg);
}

.menu-icon-invite::before {
  width: 34rpx;
  height: 24rpx;
  border: 4rpx solid currentColor;
  border-radius: 8rpx;
}

.menu-icon-invite::after {
  width: 20rpx;
  height: 20rpx;
  border-top: 4rpx solid currentColor;
  border-right: 4rpx solid currentColor;
  transform: rotate(45deg);
}

.menu-icon-block::before {
  width: 34rpx;
  height: 34rpx;
  border: 4rpx solid currentColor;
  border-radius: 50%;
}

.menu-icon-block::after {
  width: 30rpx;
  height: 4rpx;
  border-radius: 999px;
  background: currentColor;
  transform: rotate(-35deg);
}

.menu-icon-records::before {
  width: 30rpx;
  height: 36rpx;
  border: 4rpx solid currentColor;
  border-radius: 8rpx;
}

.menu-icon-records::after {
  width: 16rpx;
  height: 14rpx;
  border-top: 4rpx solid currentColor;
  border-bottom: 4rpx solid currentColor;
}

.menu-main {
  flex: 1;
  min-width: 0;
}

.menu-title {
  display: block;
  color: #172126;
  font-size: 28rpx;
  font-weight: 900;
  line-height: 1.25;
}

.menu-arrow {
  flex: 0 0 auto;
  color: #8b949b;
  font-size: 38rpx;
  line-height: 1;
}
</style>
