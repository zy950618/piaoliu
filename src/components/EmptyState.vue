<template>
  <view class="empty">
    <text class="empty-title">{{ title }}</text>
    <text class="empty-body">{{ body }}</text>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  body: string
}>()
</script>

<style scoped lang="scss">
.empty {
  border: 1px dashed #d8cdbd;
  border-radius: 8px;
  padding: 38rpx 24rpx;
  text-align: center;
  background: #fffdf8;
}

.empty-title,
.empty-body {
  display: block;
}

.empty-title {
  color: #25323c;
  font-size: 28rpx;
  font-weight: 700;
}

.empty-body {
  margin-top: 10rpx;
  color: #66727a;
  font-size: 24rpx;
  line-height: 1.5;
}
</style>
