<template>
  <view v-if="gift" class="gift-splash">
    <view class="streak streak-one"></view>
    <view class="streak streak-two"></view>
    <view class="streak streak-three"></view>
    <view class="splash-card" :class="giftVisualClass(gift)">
      <view class="splash-light"></view>
      <GiftVisual :gift="gift" size="splash" active />
      <text class="splash-name">{{ gift.name }}</text>
      <text class="splash-price">{{ gift.priceCoins }} 金币</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import GiftVisual from '@/components/GiftVisual.vue'
import type { GiftProduct } from '@/types/domain'

defineProps<{
  gift?: GiftProduct
}>()

function giftVisualClass(gift: GiftProduct) {
  if (gift.id.includes('crown')) return 'gift-luxury'
  if (gift.id.includes('island') || gift.id.includes('whale')) return 'gift-rare'
  if (gift.category === '浪漫') return 'gift-romance'
  if (gift.category === '漂流') return 'gift-drift'
  return 'gift-basic'
}

</script>

<style scoped lang="scss">
.gift-splash {
  position: fixed;
  inset: 0;
  z-index: 180;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(5, 7, 12, 0.2);
  animation: splashFade 1.28s ease both;
}

.splash-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 250rpx;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 8px;
  padding: 32rpx 34rpx 28rpx;
  overflow: hidden;
  background: rgba(20, 24, 31, 0.9);
  box-shadow: 0 30rpx 76rpx rgba(0, 0, 0, 0.32);
  animation: giftLaunch 1.18s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.splash-card::before,
.splash-card::after {
  position: absolute;
  width: 190rpx;
  height: 190rpx;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  content: '';
  animation: ringPulse 1.18s ease-out both;
}

.splash-card::after {
  animation-delay: 0.12s;
}

.splash-light {
  position: absolute;
  inset: -40rpx;
  opacity: 0.7;
  transform: rotate(18deg);
}

.gift-basic .splash-light {
  background: linear-gradient(120deg, rgba(65, 214, 195, 0.36), transparent 52%, rgba(38, 114, 255, 0.34));
}

.gift-romance .splash-light {
  background: linear-gradient(120deg, rgba(255, 71, 126, 0.38), transparent 48%, rgba(255, 177, 61, 0.32));
}

.gift-drift .splash-light {
  background: linear-gradient(120deg, rgba(50, 197, 255, 0.38), transparent 48%, rgba(125, 92, 255, 0.32));
}

.gift-rare .splash-light {
  background: linear-gradient(120deg, rgba(143, 124, 255, 0.36), transparent 48%, rgba(54, 226, 160, 0.32));
}

.gift-luxury .splash-light {
  background: linear-gradient(120deg, rgba(255, 212, 90, 0.42), transparent 48%, rgba(123, 92, 255, 0.36));
}

.splash-name,
.splash-price {
  position: relative;
  z-index: 1;
  display: block;
  max-width: 300rpx;
  overflow: hidden;
  color: #fff;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.splash-name {
  margin-top: 18rpx;
  font-size: 31rpx;
  font-weight: 900;
}

.splash-price {
  margin-top: 7rpx;
  color: rgba(255, 255, 255, 0.72);
  font-size: 22rpx;
  font-weight: 800;
}

.streak {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 180rpx;
  height: 4rpx;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, rgba(255, 226, 120, 0.92), transparent);
  transform-origin: 0 50%;
  animation: streakFly 0.88s ease-out both;
}

.streak-one {
  transform: rotate(-28deg);
}

.streak-two {
  transform: rotate(18deg);
  animation-delay: 0.08s;
}

.streak-three {
  transform: rotate(56deg);
  animation-delay: 0.16s;
}

@keyframes giftLaunch {
  0% {
    transform: translateY(120rpx) scale(0.64);
    opacity: 0;
  }

  34% {
    transform: translateY(0) scale(1.08);
    opacity: 1;
  }

  72% {
    transform: translateY(-8rpx) scale(1);
    opacity: 1;
  }

  100% {
    transform: translateY(-28rpx) scale(0.92);
    opacity: 0;
  }
}

@keyframes ringPulse {
  from {
    transform: scale(0.48);
    opacity: 0.72;
  }

  to {
    transform: scale(1.38);
    opacity: 0;
  }
}

@keyframes streakFly {
  from {
    opacity: 0;
    width: 0;
  }

  30% {
    opacity: 1;
  }

  to {
    opacity: 0;
    width: 260rpx;
  }
}

@keyframes splashFade {
  0%,
  80% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}

</style>
