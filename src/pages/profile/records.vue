<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">我的记录</text>
        <text class="muted">瓶子、树洞、游戏和举报记录</text>
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
const records = [
  { title: '我的瓶子', desc: '已投递和已捞起的瓶子', count: '12' },
  { title: '我的树洞', desc: '发布、共鸣和回复记录', count: '8' },
  { title: '真心话记录', desc: '公开和私密真心话', count: '6' },
  { title: '大冒险记录', desc: '公开和私密大冒险', count: '5' },
  { title: '举报记录', desc: '安全处理进度', count: '2' }
]
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
