<template>
  <view class="page profile-page safe-bottom">
    <view class="panel profile-card">
      <view class="vip-ribbon" @tap="go('/pages/membership/index')">
        <text class="vip-mark">VIP</text>
        <text class="vip-copy">会员权益生效中</text>
      </view>

      <view class="row profile-row">
        <view class="avatar" @tap="go('/pages/profile/settings')">{{ app.user?.avatarText || '海' }}</view>
        <view class="profile-main">
          <view class="row name-row">
            <text class="title">{{ app.user?.nickname || '匿名岛民' }}</text>
            <text class="gender-pill">{{ userGenderText }}</text>
          </view>
          <view class="user-id-row" @tap="copyUserId">
            <text class="muted">user_id: {{ app.user?.id || '-' }}</text>
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
      <view class="quick-card" @tap="go('/pages/messages/index')">
        <text class="quick-title">消息中心</text>
        <text class="quick-copy">私信和互动提醒</text>
      </view>
      <view class="quick-card" @tap="go('/pages/creator/index')">
        <text class="quick-title">认证与收益</text>
        <text class="quick-copy">资料、相册、分账</text>
      </view>
    </view>

    <view class="section panel list-panel">
      <view v-for="item in menuItems" :key="item.title" class="menu-row" @tap="go(item.url)">
        <view class="menu-icon">{{ item.icon }}</view>
        <view class="menu-main">
          <text class="menu-title">{{ item.title }}</text>
          <text class="muted">{{ item.desc }}</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { navigateTo, showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'

const app = useAppStore()
const content = useContentStore()

const menuItems = [
  { icon: '设', title: '用户设置', desc: '头像、昵称和个人资料', url: '/pages/profile/settings' },
  { icon: '脸', title: '人脸认证', desc: '活体、性别识别、人工复核', url: '/pages/profile/verification' },
  { icon: '邀', title: '拉新活动', desc: '邀请码、邀请进度、会员奖励', url: '/pages/profile/referral' },
  { icon: '黑', title: '黑名单', desc: '查看已屏蔽的人和原因', url: '/pages/profile/blacklist' },
  { icon: '记', title: '我的记录', desc: '瓶子、树洞、游戏和举报记录', url: '/pages/profile/records' }
]

onLoad(async () => {
  await app.hydrate()
  await content.loadVerification()
  await content.loadBlacklist()
})

const userGenderText = computed(() => {
  const gender = app.user?.gender
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
})

function go(url: string) {
  navigateTo(url)
}

function copyUserId() {
  const userId = app.user?.id
  if (!userId) return
  if (typeof uni !== 'undefined' && uni.setClipboardData) {
    uni.setClipboardData({
      data: userId,
      success: () => showToast('user_id 已复制')
    })
    return
  }
  showToast(userId)
}
</script>

<style scoped lang="scss">
.profile-page {
  padding-top: 30rpx;
}

.profile-card {
  position: relative;
  overflow: hidden;
  padding-top: 72rpx;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(239, 247, 244, 0.88)),
    radial-gradient(circle at 90% 10%, rgba(35, 108, 114, 0.12), transparent 32%);
}

.vip-ribbon {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  display: flex;
  align-items: center;
  gap: 12rpx;
  min-height: 52rpx;
  padding: 0 24rpx;
  color: #fff;
  background: linear-gradient(135deg, #9a6424, #d99b48);
  box-sizing: border-box;
}

.vip-mark {
  font-size: 24rpx;
  font-weight: 900;
  letter-spacing: 0;
}

.vip-copy {
  font-size: 22rpx;
  font-weight: 700;
}

.profile-row {
  gap: 18rpx;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 96rpx;
  height: 96rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.92);
  border-radius: 50%;
  color: #fff;
  background: #236c72;
  box-shadow: 0 12rpx 28rpx rgba(35, 108, 114, 0.18);
  font-size: 36rpx;
  font-weight: 800;
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

.gender-pill,
.edit-pill,
.copy-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 5rpx 13rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
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

.profile-stats {
  margin-top: 24rpx;
}

.stat {
  min-height: 118rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
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
  color: #236c72;
  font-size: 34rpx;
  font-weight: 800;
}

.sign-mini-button {
  flex: 0 0 auto;
  border-radius: 8px;
  padding: 14rpx 18rpx;
  color: #fff;
  background: #236c72;
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
  border-radius: 8px;
  padding: 22rpx;
  background: rgba(255, 255, 255, 0.88);
  box-sizing: border-box;
  box-shadow: 0 14rpx 32rpx rgba(31, 54, 58, 0.06);
}

.quick-card.primary {
  background: linear-gradient(135deg, rgba(35, 108, 114, 0.94), rgba(45, 124, 118, 0.9));
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
}

.menu-row {
  display: flex;
  align-items: center;
  gap: 18rpx;
  min-height: 108rpx;
  border-bottom: 1px solid rgba(23, 33, 38, 0.08);
}

.menu-row:last-child {
  border-bottom: 0;
}

.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 58rpx;
  height: 58rpx;
  border-radius: 50%;
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
  font-size: 23rpx;
  font-weight: 900;
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
