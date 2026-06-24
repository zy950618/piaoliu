<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">黑名单</text>
        <text class="muted">已屏蔽的用户不会再推荐给你</text>
      </view>
    </view>

    <view class="section panel">
      <view v-for="item in visibleBlacklist" :key="item.id" class="record-row">
        <view>
          <text class="body">{{ item.nickname }}</text>
          <text class="muted">{{ item.reason }}</text>
        </view>
        <text class="tag">已屏蔽</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useContentStore } from '@/stores/content'

const content = useContentStore()
const fallbackBlacklist = [
  { id: 'fake_black_1', nickname: '海岸来信', reason: '频繁广告引流' },
  { id: 'fake_black_2', nickname: '晚风', reason: '不友善互动' }
]

onLoad(() => content.loadBlacklist())

const visibleBlacklist = computed(() => (content.blacklist.length ? content.blacklist : fallbackBlacklist))
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
