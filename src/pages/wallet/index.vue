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
      <text class="h2">充值金币</text>
      <text class="muted recharge-copy">金币用于聊天送礼、查看付费内容，不可提现。</text>
      <view class="recharge-grid">
        <view v-for="item in rechargeOptions" :key="item" class="recharge-card" :class="{ disabled: paying }" @tap="recharge(item)">
          <text class="recharge-amount">{{ item }}</text>
          <text class="muted">金币</text>
        </view>
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
        <view v-for="gift in content.gifts" :key="gift.id" class="gift-card" :class="[giftTierClass(gift), { premium: isPremiumGift(gift) }]">
          <view class="gift-stage">
            <GiftVisual :gift="gift" size="card" :active="isPremiumGift(gift)" />
          </view>
          <text class="body">{{ gift.name }}</text>
          <text class="gift-desc">{{ giftDescription(gift) }}</text>
          <view class="gift-price-row">
            <text class="coin-dot" />
            <text>{{ gift.priceCoins }}</text>
          </view>
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
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import GiftVisual from '@/components/GiftVisual.vue'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'
import type { GiftProduct } from '@/types/domain'

const content = useContentStore()
const rechargeOptions = [30, 68, 128, 328, 648, 999]
const paying = ref(false)

onLoad(() => content.loadWallet())

async function withdraw() {
  try {
    await content.requestWithdraw(50)
    showToast('提现申请已提交，进入人工审核')
  } catch {
    showToast('可提现收益不足')
  }
}

async function recharge(amount: number) {
  if (paying.value) return
  paying.value = true
  try {
    await content.rechargeCoins(amount)
    showToast(`充值成功，已到账 ${amount} 金币`)
  } catch {
    showToast('支付失败，请稍后再试')
  } finally {
    paying.value = false
  }
}

function isPremiumGift(gift: GiftProduct) {
  return gift.priceCoins >= 520 || /crown|island|whale|plane|flight/i.test(gift.id)
}

function giftTierClass(gift: GiftProduct) {
  if (gift.priceCoins >= 999 || gift.id.includes('crown')) return 'gift-tier-legend'
  if (isPremiumGift(gift)) return 'gift-tier-premium'
  if (gift.priceCoins >= 99) return 'gift-tier-rare'
  return 'gift-tier-basic'
}

function giftDescription(gift: GiftProduct) {
  if (gift.priceCoins >= 999 || gift.id.includes('crown')) return '全屏礼物'
  if (isPremiumGift(gift)) return '进场特效'
  if (gift.priceCoins >= 99) return '动态光效'
  return '轻量心意'
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
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 8px;
  padding: 26rpx;
  box-sizing: border-box;
  box-shadow: 0 14rpx 32rpx rgba(15, 23, 42, 0.06);
}

.recharge {
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(239, 246, 255, 0.94)),
    radial-gradient(circle at 94% 0%, rgba(37, 99, 235, 0.12), transparent 34%);
}

.earned {
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(240, 253, 250, 0.94)),
    radial-gradient(circle at 94% 0%, rgba(20, 184, 166, 0.12), transparent 34%);
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

.recharge-copy {
  display: block;
  margin-top: 8rpx;
}

.recharge-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 20rpx;
}

.recharge-card {
  border: 1px solid rgba(35, 108, 114, 0.12);
  border-radius: 8px;
  padding: 18rpx;
  background: rgba(35, 108, 114, 0.06);
  text-align: center;
}

.recharge-card.disabled {
  opacity: 0.55;
}

.recharge-amount {
  display: block;
  color: #236c72;
  font-size: 34rpx;
  font-weight: 900;
}

.gift-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
  margin-top: 20rpx;
}

.gift-card {
  position: relative;
  overflow: hidden;
  min-height: 210rpx;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 16px;
  padding: 18rpx 12rpx 16rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.92)),
    radial-gradient(circle at 88% 0%, rgba(37, 99, 235, 0.08), transparent 32%);
  box-shadow: 0 12rpx 28rpx rgba(15, 23, 42, 0.06);
  text-align: center;
  transition: transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}

.gift-card:active {
  transform: scale(0.97);
}

.gift-card.premium {
  border-color: rgba(37, 99, 235, 0.22);
  box-shadow: 0 18rpx 42rpx rgba(37, 99, 235, 0.12);
}

.gift-card.premium::before {
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, transparent 0%, rgba(255, 255, 255, 0.62) 42%, transparent 62%);
  transform: translateX(-120%);
  animation: walletGiftSweep 2.8s ease-in-out infinite;
  content: '';
}

.gift-stage {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 104rpx;
  height: 104rpx;
  margin: 0 auto 12rpx;
}

.gift-desc {
  display: block;
  margin-top: 5rpx;
  color: #64748b;
  font-size: 20rpx;
  font-weight: 800;
}

.gift-price-row {
  position: relative;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6rpx;
  margin-top: 8rpx;
  border-radius: 999px;
  padding: 7rpx 12rpx;
  color: #0f172a;
  background: rgba(241, 245, 249, 0.92);
  font-size: 21rpx;
  font-weight: 900;
}

.gift-card > .muted {
  display: none;
}

.coin-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: linear-gradient(145deg, #fde68a, #f59e0b);
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.72), 0 0 10rpx rgba(245, 158, 11, 0.34);
}

@keyframes walletGiftSweep {
  0%,
  46% {
    transform: translateX(-120%);
  }

  74%,
  100% {
    transform: translateX(120%);
  }
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
