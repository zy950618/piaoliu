<template>
  <view class="checkin-strip">
    <view v-for="(reward, index) in rewards" :key="`${reward}-${index}`" class="day" :class="{ active: index < activeCount, current: index === currentIndex }">
      <text class="day-label">D{{ index + 1 }}</text>
      <text class="day-reward">{{ reward }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
defineProps<{
  rewards: number[]
  activeCount: number
  currentIndex: number
}>()
</script>

<style scoped lang="scss">
.checkin-strip {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 8rpx;
}

.day {
  min-height: 88rpx;
  border: 1px solid #eadfce;
  border-radius: 8px;
  background: #fffdf8;
  text-align: center;
  padding-top: 12rpx;
  box-sizing: border-box;
}

.day.active {
  background: #e3f1ee;
  border-color: #b9d9d4;
}

.day.current {
  border-color: #d9895b;
}

.day-label,
.day-reward {
  display: block;
  line-height: 1.3;
}

.day-label {
  color: #66727a;
  font-size: 20rpx;
}

.day-reward {
  margin-top: 4rpx;
  color: #25323c;
  font-size: 24rpx;
  font-weight: 700;
}
</style>
