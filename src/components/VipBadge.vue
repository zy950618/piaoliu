<template>
  <view class="vip-badge" :class="[variant, { glow }]">
    <text class="vip-gem"></text>
    <text class="vip-text">{{ labelText }}</text>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  variant?: 'mini' | 'standard' | 'premium' | 'ribbon'
  label?: string
  glow?: boolean
}>(), {
  variant: 'standard',
  label: '',
  glow: false
})

const labelText = computed(() => {
  if (props.label) return props.label
  return 'VIP'
})
</script>

<style scoped lang="scss">
.vip-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  flex-shrink: 0;
  overflow: hidden;
  border: 1px solid rgba(154, 97, 10, 0.42);
  border-radius: 999px;
  color: #f7df9e;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.13), rgba(255, 255, 255, 0.03)),
    linear-gradient(135deg, #111827 0%, #1f2937 48%, #07080d 100%);
  box-shadow:
    inset 0 1rpx 0 rgba(255, 255, 255, 0.18),
    inset 0 -1rpx 0 rgba(0, 0, 0, 0.42),
    0 8rpx 18rpx rgba(15, 23, 42, 0.2);
  box-sizing: border-box;
}

.vip-badge::after {
  position: absolute;
  inset: 0;
  background: linear-gradient(105deg, transparent 0%, rgba(255, 255, 255, 0.26) 45%, transparent 68%);
  transform: translateX(-120%);
  content: '';
}

.vip-badge.glow::after,
.premium::after,
.ribbon::after {
  animation: vipShine 2.8s ease-in-out infinite;
}

.vip-gem {
  position: relative;
  z-index: 1;
  display: inline-block;
  width: 13rpx;
  height: 13rpx;
  transform: rotate(45deg);
  border-radius: 3rpx;
  background:
    radial-gradient(circle at 30% 30%, #fff, transparent 34%),
    linear-gradient(135deg, #f8e7ad, #a87418);
  box-shadow: 0 0 12rpx rgba(248, 223, 158, 0.42);
}

.vip-text {
  position: relative;
  z-index: 1;
  letter-spacing: 0;
  line-height: 1;
  font-weight: 900;
  white-space: nowrap;
}

.mini {
  min-height: 32rpx;
  padding: 0 11rpx;
}

.mini .vip-text {
  font-size: 19rpx;
}

.mini .vip-gem {
  display: none;
}

.standard {
  min-height: 46rpx;
  padding: 0 16rpx;
}

.standard .vip-text {
  font-size: 22rpx;
}

.premium {
  min-height: 60rpx;
  padding: 0 22rpx;
  border-color: rgba(247, 223, 158, 0.34);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.03)),
    linear-gradient(135deg, #0f172a 0%, #1f2937 52%, #050506 100%);
}

.premium .vip-text {
  font-size: 26rpx;
}

.premium .vip-gem {
  width: 15rpx;
  height: 15rpx;
}

.ribbon {
  min-height: 62rpx;
  border-radius: 8px;
  padding: 0 24rpx;
  border-color: rgba(247, 223, 158, 0.32);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.03)),
    linear-gradient(135deg, #111827 0%, #283241 50%, #07080d 100%);
  box-shadow:
    inset 0 1rpx 0 rgba(255, 255, 255, 0.16),
    0 12rpx 28rpx rgba(15, 23, 42, 0.2);
}

.ribbon .vip-text {
  font-size: 26rpx;
}

@keyframes vipShine {
  0%,
  42% {
    transform: translateX(-120%);
  }

  72%,
  100% {
    transform: translateX(120%);
  }
}
</style>
