<template>
  <view class="page safe-bottom">
    <view class="hero panel glass">
      <view class="between">
        <view class="row user-row">
          <view class="avatar">
            <image class="avatar-image" :src="resolveAvatarUrl(app.user?.avatarUrl, app.user?.id || 'current-user')" :alt="`${app.user?.nickname || '当前用户'}的头像`" mode="aspectFill" />
          </view>
          <view>
            <view class="row name-row">
              <text class="title">{{ app.user?.nickname || '匿名岛民' }}</text>
              <VipBadge v-if="app.user?.isVip" variant="standard" glow />
            </view>
            <text class="muted">微信小程序 / iOS / Android 数据互通</text>
          </view>
        </view>
        <view class="coin-box">
          <text class="muted">漂流币</text>
          <text class="coin">{{ app.user?.driftCoins ?? 0 }}</text>
        </view>
      </view>
    </view>

    <view class="section insight-card">
      <view class="insight-main">
        <text class="insight-kicker">今晚推荐</text>
        <text class="insight-title">先捞一只瓶子，再决定要不要关注。</text>
      </view>
      <button class="button insight-button" hover-class="none" @tap="go('/pages/bottle/index')">去捞瓶</button>
    </view>

    <view class="section">
      <view class="between section-head">
        <text class="h2">今日次数</text>
        <text class="muted">完成动作才扣除</text>
      </view>
      <QuotaGrid :items="app.quotaList" />
    </view>

    <view class="section panel reward-panel">
      <view class="between">
        <view>
          <text class="h2">广告加次数</text>
          <text class="muted reward-copy">看完一次，五种玩法各 +1</text>
        </view>
        <view class="tag">{{ app.adCountdownText }}</view>
      </view>
      <button class="button semantic-button" hover-class="none" :class="{ disabled: !app.adReward?.canWatch }" @tap="watchAd">
        {{ app.adReward?.canWatch ? '观看广告领取' : app.adCountdownText }}
      </button>
    </view>

    <view class="section">
      <text class="h2">开始漂流</text>
      <view class="grid-2 action-grid">
        <button class="entry bottle" hover-class="none" @tap="go('/pages/bottle/index')">
          <text class="entry-title">漂流瓶</text>
          <text class="entry-copy">扔出秘密，捞回回应</text>
          <view class="entry-badges">
            <text class="entry-badge">捞 +{{ quotaLeft('fish_bottle') }}</text>
            <text class="entry-badge">发 +{{ quotaLeft('throw_bottle') }}</text>
          </view>
        </button>
        <button class="entry truth" hover-class="none" @tap="go('/pages/truth/index')">
          <text class="entry-title">游戏</text>
          <text class="entry-copy">快速开始一轮真心话</text>
          <view class="entry-badges">
            <text class="entry-badge">真心话 +{{ quotaLeft('truth') }}</text>
            <text class="entry-badge">私密真心话 +{{ quotaLeft('truth') }}</text>
            <text class="entry-badge">大冒险 +{{ quotaLeft('dare') }}</text>
          </view>
        </button>
        <button class="entry tree" hover-class="none" @tap="go('/pages/game/index')">
          <text class="entry-title">游戏星系</text>
          <text class="entry-copy">随机匹配、真心话和大冒险</text>
          <view class="entry-badges">
            <text class="entry-badge">匹配入口</text>
          </view>
        </button>
        <button class="entry plaza" hover-class="none" @tap="go('/pages/plaza/index')">
          <text class="entry-title">广场</text>
          <text class="entry-copy">看公开动态和热门话题</text>
        </button>
        <button class="entry nearby" hover-class="none" @tap="go('/pages/nearby/index')">
          <text class="entry-title">附近的人</text>
          <text class="entry-copy">粗略距离，安全互动</text>
        </button>
      </view>
    </view>

    <view class="section grid-2">
      <button class="mini-entry panel" hover-class="none" @tap="go('/pages/creator/index')">
        <text class="mini-title">女性认证</text>
        <text class="muted">安全展示、收益分账、提现规则</text>
      </button>
      <button class="mini-entry panel" hover-class="none" @tap="go('/pages/wallet/index')">
        <text class="mini-title">金币钱包</text>
        <text class="muted">充值币不可提现，收益币可提现</text>
      </button>
      <button class="mini-entry panel" hover-class="none" @tap="go('/pages/profile/index')">
        <text class="mini-title">我的中心</text>
        <text class="muted">签到、黑名单、会员和记录</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
import QuotaGrid from '@/components/QuotaGrid.vue'
import VipBadge from '@/components/VipBadge.vue'
import { navigateTo, showToast, switchTab } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { resolveAvatarUrl } from '@/utils/avatar'
import type { QuotaType } from '@/types/domain'

const app = useAppStore()

onLoad(() => {
  app.hydrate()
})

function go(url: string) {
  if (url === '/pages/home/index' || url === '/pages/plaza/index' || url === '/pages/game/index' || url === '/pages/messages/index' || url === '/pages/profile/index') {
    switchTab(url)
    return
  }
  navigateTo(url)
}

function quotaLeft(type: QuotaType) {
  return app.quotas?.[type]?.remaining ?? 0
}

async function watchAd() {
  if (!app.adReward?.canWatch) {
    showToast(app.adCountdownText)
    return
  }
  navigateTo('/pages/ad/reward')
}
</script>

<style scoped lang="scss">
.hero {
  background:
    linear-gradient(135deg, rgba(255, 250, 240, 0.94), rgba(219, 238, 237, 0.86)),
    #fffaf0;
}

.user-row {
  min-width: 0;
  gap: 18rpx;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  width: 86rpx;
  height: 86rpx;
  border-radius: 50%;
  color: #fff;
  background: #2d6c73;
  font-size: 34rpx;
  font-weight: 700;
}

.avatar-image {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.name-row {
  gap: 12rpx;
}

.coin-box {
  min-width: 108rpx;
  text-align: right;
}

.coin {
  display: block;
  color: #d9895b;
  font-size: 34rpx;
  font-weight: 800;
  line-height: 1.2;
}

.section-head {
  margin-bottom: 14rpx;
}

button.entry,
button.mini-entry,
button.insight-button,
.semantic-button {
  width: 100%;
  margin: 0;
  border: 0;
  color: inherit;
  font: inherit;
  line-height: inherit;
  text-align: left;
}

button.mini-entry::after,
button.insight-button::after,
.semantic-button::after {
  display: none;
}

.insight-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  border-radius: 8px;
  padding: 26rpx;
  background: linear-gradient(135deg, #234b5d, #2d6c73);
  box-shadow: 0 18rpx 38rpx rgba(35, 75, 93, 0.16);
}

.insight-main {
  min-width: 0;
}

.insight-kicker,
.insight-title {
  display: block;
  color: #fff;
}

.insight-kicker {
  opacity: 0.78;
  font-size: 22rpx;
}

.insight-title {
  margin-top: 8rpx;
  font-size: 30rpx;
  font-weight: 800;
  line-height: 1.35;
}

.insight-button {
  width: 168rpx;
  min-height: 66rpx;
  color: #234b5d;
  background: #fffdf8;
  flex-shrink: 0;
  padding: 0 16rpx;
  font-size: 26rpx;
  box-sizing: border-box;
  text-align: center;
}

.reward-panel {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.reward-copy {
  display: block;
  margin-top: 6rpx;
}

.mini-button {
  width: 138rpx;
  min-height: 64rpx;
  font-size: 24rpx;
}

.checkin {
  margin-top: 20rpx;
}

.action-grid {
  margin-top: 16rpx;
}

.entry {
  position: relative;
  overflow: hidden;
  min-height: 190rpx;
  border-radius: 8px;
  padding: 26rpx;
  box-sizing: border-box;
  box-shadow: 0 16rpx 34rpx rgba(31, 54, 58, 0.08);
}

.entry::after {
  content: '';
  position: absolute;
  right: -38rpx;
  bottom: -42rpx;
  width: 158rpx;
  height: 158rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

.entry-title,
.entry-copy {
  display: block;
}

.entry-title {
  color: #25323c;
  font-size: 34rpx;
  font-weight: 800;
}

.entry-copy {
  margin-top: 14rpx;
  color: #4f5c64;
  font-size: 25rpx;
  line-height: 1.5;
}

.entry-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  position: relative;
  z-index: 1;
  margin-top: 20rpx;
}

.entry-badge {
  border-radius: 999px;
  padding: 7rpx 14rpx;
  color: #fff;
  background: #ff3b30;
  box-shadow: 0 9rpx 20rpx rgba(255, 59, 48, 0.22);
  font-size: 21rpx;
  font-weight: 900;
  line-height: 1;
}

.bottle {
  background: #dbeeed;
}

.truth {
  background: #f6dfb6;
}

.dare {
  background: #e6d8f0;
}

.tree {
  background: #dfe8d8;
}

.plaza {
  background: #fff3f5;
}

.nearby {
  background: #eef7ed;
}

.mini-entry {
  min-height: 148rpx;
}

.mini-title {
  display: block;
  margin-bottom: 10rpx;
  color: #25323c;
  font-size: 28rpx;
  font-weight: 800;
}
</style>
