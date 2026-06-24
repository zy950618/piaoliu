<template>
  <view class="quota-grid">
    <view v-for="quota in items" :key="quota.type" class="quota-card">
      <view class="quota-layer"></view>
      <text class="quota-label">{{ quota.label }}</text>
      <text class="quota-badge">+{{ quota.remaining }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import type { QuotaItem } from '@/types/domain'

defineProps<{
  items: QuotaItem[]
}>()
</script>

<style scoped lang="scss">
.quota-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14rpx;
}

.quota-card {
  position: relative;
  min-height: 104rpx;
  overflow: hidden;
  border: 1px solid rgba(23, 33, 38, 0.06);
  border-radius: 8px;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.96), rgba(245, 249, 247, 0.82)),
    #fff;
  padding: 18rpx 18rpx 16rpx;
  box-sizing: border-box;
  box-shadow: 0 14rpx 28rpx rgba(31, 54, 58, 0.05);
}

.quota-layer {
  position: absolute;
  right: -22rpx;
  bottom: -28rpx;
  width: 94rpx;
  height: 94rpx;
  border-radius: 50%;
  background: rgba(185, 71, 71, 0.08);
  pointer-events: none;
}

.quota-label {
  display: block;
  position: relative;
  z-index: 1;
  color: #25323c;
  font-size: 24rpx;
  font-weight: 800;
  line-height: 1.3;
}

.quota-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  min-width: 58rpx;
  margin-top: 16rpx;
  border-radius: 999px;
  padding: 7rpx 16rpx;
  color: #fff;
  background: #ff3b30;
  box-shadow: 0 10rpx 22rpx rgba(255, 59, 48, 0.24);
  font-size: 24rpx;
  font-weight: 900;
  line-height: 1;
  box-sizing: border-box;
}

@media (min-width: 720px) {
  .quota-grid {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }
}
</style>
