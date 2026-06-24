<template>
  <view class="page safe-bottom">
    <text class="title">金币钱包</text>
    <text class="muted subtitle">充值金币只能消费；收益会转为魅力值，达到门槛后可申请提现。</text>

    <view class="section wallet-hero">
      <view class="wallet-card recharge">
        <text class="wallet-label">充值金币</text>
        <text class="wallet-value">{{ content.wallet?.rechargeCoins || 0 }}</text>
        <text class="wallet-copy">用于看照片、送礼物，不可提现</text>
      </view>
      <view class="wallet-card earned">
        <text class="wallet-label">魅力值</text>
        <text class="wallet-value">{{ content.wallet?.charmValue || 0 }}</text>
        <text class="wallet-copy">{{ content.wallet?.withdrawThresholdCharm || 0 }} 起可申请提现</text>
      </view>
    </view>

    <view class="section panel">
      <view class="between">
        <view>
          <text class="h2">提现规则</text>
          <text class="muted">提现按魅力值换算，{{ content.wallet?.charmExchangeRate || 100 }} 魅力值 = 1 元，人工审核后到账。</text>
        </view>
        <view class="button secondary withdraw-button" @tap="withdraw">申请提现</view>
      </view>
      <view class="soft-divider" />
      <text class="muted">冻结中：{{ content.wallet?.frozenCoins || 0 }} · 收益金币：{{ content.wallet?.earnedCoins || 0 }} · 礼物收益：{{ content.wallet?.giftCoins || 0 }}</text>
    </view>

    <view class="section panel">
      <text class="h2">礼物</text>
      <view class="gift-grid">
        <view v-for="gift in content.gifts" :key="gift.id" class="gift-card">
          <text class="gift-icon">{{ gift.iconText }}</text>
          <text class="body">{{ gift.name }}</text>
          <text class="muted">{{ gift.priceCoins }} 金币</text>
        </view>
      </view>
    </view>

    <view class="section panel">
      <text class="h2">流水</text>
      <view v-for="item in content.ledger" :key="item.id" class="ledger-row">
        <view>
          <text class="body">{{ item.title }}</text>
          <text class="muted">{{ item.withdrawable ? '可提现收益' : '不可提现充值币' }}</text>
        </view>
        <text class="ledger-amount" :class="{ negative: item.amount < 0 }">{{ item.amount > 0 ? '+' : '' }}{{ item.amount }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'

const content = useContentStore()

onLoad(() => content.loadWallet())

async function withdraw() {
  try {
    await content.requestWithdraw(50)
    showToast('提现申请已提交，进入人工审核')
  } catch {
    showToast('可提现收益不足')
  }
}
</script>

<style scoped lang="scss">
.subtitle {
  display: block;
  margin-top: 10rpx;
}

.wallet-hero {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
}

.wallet-card {
  min-height: 210rpx;
  border-radius: 8px;
  padding: 26rpx;
  box-sizing: border-box;
}

.recharge {
  background: linear-gradient(135deg, #f6dfb6, #fff5df);
}

.earned {
  background: linear-gradient(135deg, #dbeeed, #eef9f5);
}

.wallet-label,
.wallet-value,
.wallet-copy {
  display: block;
}

.wallet-label {
  color: #66727a;
  font-size: 24rpx;
}

.wallet-value {
  margin-top: 18rpx;
  color: #25323c;
  font-size: 46rpx;
  font-weight: 900;
}

.wallet-copy {
  margin-top: 12rpx;
  color: #66727a;
  font-size: 22rpx;
  line-height: 1.45;
}

.withdraw-button {
  width: 150rpx;
  min-height: 68rpx;
}

.gift-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 20rpx;
}

.gift-card {
  border: 1px solid #eadfce;
  border-radius: 8px;
  padding: 18rpx;
  text-align: center;
}

.gift-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 58rpx;
  height: 58rpx;
  margin: 0 auto 10rpx;
  border-radius: 50%;
  color: #fff;
  background: #d9895b;
  font-weight: 800;
}

.ledger-row {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  padding: 22rpx 0;
  border-bottom: 1px solid #eadfce;
}

.ledger-row .body,
.ledger-row .muted {
  display: block;
}

.ledger-amount {
  color: #2d6c73;
  font-size: 30rpx;
  font-weight: 800;
}

.ledger-amount.negative {
  color: #b94747;
}
</style>
