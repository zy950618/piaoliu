<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">我的记录</text>
        <text class="muted">瓶子、消息、游戏和举报记录</text>
      </view>
    </view>

    <view class="section panel">
      <view v-for="item in records" :key="item.title" class="record-row">
        <view>
          <text class="body">{{ item.title }}</text>
          <text class="muted">{{ item.desc }}</text>
        </view>
        <text class="tag">{{ item.count }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useContentStore } from '@/stores/content'

const content = useContentStore()
const records = computed(() => content.userRecords)

onLoad(() => content.loadUserRecords())
</script>

<style scoped lang="scss">
.record-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  padding: 22rpx 0;
  border-bottom: 1px solid rgba(23, 33, 38, 0.08);
}

.record-row:last-child {
  border-bottom: 0;
}

.record-row .body,
.record-row .muted {
  display: block;
}
</style>
