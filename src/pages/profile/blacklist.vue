<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">黑名单</text>
        <text class="muted">已屏蔽的用户不会再推荐给你</text>
      </view>
    </view>

    <view v-if="content.blacklist.length" class="section panel">
      <view v-for="item in content.blacklist" :key="item.id" class="record-row">
        <view>
          <text class="body">{{ item.nickname }}</text>
          <text class="muted">{{ item.reason }}</text>
        </view>
        <text class="tag">已屏蔽</text>
      </view>
    </view>

    <EmptyState v-else title="暂无黑名单" body="被你屏蔽的用户会显示在这里。" />
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
import EmptyState from '@/components/EmptyState.vue'
import { useContentStore } from '@/stores/content'

const content = useContentStore()

onLoad(() => content.loadBlacklist())
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
