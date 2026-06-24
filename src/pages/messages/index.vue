<template>
  <view class="page messages-page safe-bottom">
    <view class="between">
      <view>
        <text class="title">消息中心</text>
        <text class="muted subtitle">漂流瓶回应、好友进展和系统通知</text>
      </view>
      <text class="tag">{{ totalUnread }} 未读</text>
    </view>

    <view class="panel summary-panel">
      <view>
        <text class="summary-number">{{ content.conversationThreads.length }}</text>
        <text class="muted">历史对话</text>
      </view>
      <view class="summary-divider" />
      <view>
        <text class="summary-number">{{ content.messages.length }}</text>
        <text class="muted">通知记录</text>
      </view>
    </view>

    <view class="segment-control">
      <view class="segment-item" :class="{ active: activeTab === 'conversations' }" @tap="activeTab = 'conversations'">
        历史对话
      </view>
      <view class="segment-item" :class="{ active: activeTab === 'messages' }" @tap="activeTab = 'messages'">
        通知
      </view>
    </view>

    <view v-if="activeTab === 'conversations'" class="section">
      <view
        v-for="thread in content.conversationThreads"
        :key="thread.id"
        class="panel conversation-card"
        :class="{ selected: selectedThreadId === thread.id }"
        @tap="toggleThread(thread.id)"
      >
        <view class="conversation-top">
          <view class="avatar">{{ thread.participantName.slice(0, 1) }}</view>
          <view class="conversation-main">
            <view class="between">
              <text class="h2">{{ thread.participantName }}</text>
              <text v-if="thread.unreadCount > 0" class="tag">{{ thread.unreadCount }} 新</text>
            </view>
            <text class="muted">{{ thread.participantTag }} · {{ thread.updatedAt }}</text>
          </view>
        </view>

        <text class="bottle-preview">“{{ thread.bottlePreview }}”</text>
        <text class="body message-body">{{ thread.lastMessage }}</text>

        <view v-if="selectedThreadId === thread.id" class="thread-preview">
          <view
            v-for="turn in thread.turns.slice(-2)"
            :key="turn.id"
            class="chat-line"
            :class="{ me: turn.fromMe }"
          >
            <text class="chat-name">{{ turn.fromMe ? '我' : turn.senderName }}</text>
            <text class="chat-bubble">{{ turn.body }}</text>
          </view>
        </view>
      </view>
      <EmptyState
        v-if="content.conversationThreads.length === 0"
        title="暂无历史对话"
        body="捞到瓶子并回应后，对话会保存在这里。"
      />
    </view>

    <view v-else class="section">
      <view v-for="message in content.messages" :key="message.id" class="panel message-card">
        <view class="between">
          <text class="h2">{{ message.title }}</text>
          <text v-if="message.unread" class="tag">新</text>
        </view>
        <text class="body message-body">{{ message.body }}</text>
        <text class="muted">{{ message.createdAt }}</text>
      </view>
      <EmptyState v-if="content.messages.length === 0" title="暂无消息" body="瓶子回复、树洞回应和系统通知会出现在这里。" />
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import EmptyState from '@/components/EmptyState.vue'
import { useContentStore } from '@/stores/content'

const content = useContentStore()
const unreadCount = computed(() => content.messages.filter((item) => item.unread).length)
const historyUnreadCount = computed(() => content.conversationThreads.reduce((sum, thread) => sum + thread.unreadCount, 0))
const totalUnread = computed(() => unreadCount.value + historyUnreadCount.value)
const activeTab = ref<'conversations' | 'messages'>('conversations')
const selectedThreadId = ref('')

onLoad(() => {
  void loadPage()
})

async function loadPage() {
  await Promise.all([content.loadMessages(), content.loadConversationThreads()])
  selectedThreadId.value = content.conversationThreads[0]?.id || ''
}

function toggleThread(threadId: string) {
  selectedThreadId.value = selectedThreadId.value === threadId ? '' : threadId
}
</script>

<style scoped lang="scss">
.subtitle {
  display: block;
  margin-top: 8rpx;
}

.summary-panel {
  display: grid;
  grid-template-columns: 1fr 1px 1fr;
  align-items: center;
  margin-top: 24rpx;
  text-align: center;
}

.summary-number {
  display: block;
  color: #1d1d1f;
  font-size: 42rpx;
  font-weight: 800;
  line-height: 1.2;
}

.summary-divider {
  height: 72rpx;
  background: rgba(29, 29, 31, 0.09);
}

.segment-control {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8rpx;
  margin-top: 22rpx;
  border: 1px solid rgba(29, 29, 31, 0.08);
  border-radius: 14px;
  padding: 8rpx;
  background: rgba(255, 255, 255, 0.72);
}

.segment-item {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 64rpx;
  border-radius: 10px;
  color: #6e6e73;
  font-size: 26rpx;
  font-weight: 700;
}

.segment-item.active {
  color: #1d1d1f;
  background: #ffffff;
  box-shadow: 0 10rpx 24rpx rgba(0, 0, 0, 0.06);
}

.conversation-card,
.message-card {
  margin-bottom: 16rpx;
}

.conversation-card.selected {
  border-color: rgba(0, 113, 227, 0.2);
  background: rgba(255, 255, 255, 0.96);
}

.conversation-top {
  display: flex;
  align-items: center;
  gap: 18rpx;
}

.avatar {
  flex: 0 0 auto;
  width: 76rpx;
  height: 76rpx;
  border-radius: 50%;
  background: #2d6c73;
  color: #fff;
  font-size: 30rpx;
  font-weight: 800;
  line-height: 76rpx;
  text-align: center;
}

.conversation-main {
  min-width: 0;
  flex: 1;
}

.conversation-main .h2,
.conversation-main .muted {
  display: block;
}

.bottle-preview {
  display: block;
  margin-top: 22rpx;
  border-left: 6rpx solid rgba(95, 159, 143, 0.45);
  padding-left: 18rpx;
  color: #6e6e73;
  font-size: 25rpx;
  line-height: 1.5;
}

.message-body {
  display: block;
  margin: 14rpx 0;
}

.thread-preview {
  margin-top: 20rpx;
  padding-top: 18rpx;
  border-top: 1px solid rgba(29, 29, 31, 0.08);
}

.chat-line {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 14rpx;
}

.chat-line.me {
  align-items: flex-end;
}

.chat-name {
  margin-bottom: 8rpx;
  color: #6e6e73;
  font-size: 22rpx;
}

.chat-bubble {
  max-width: 82%;
  border-radius: 14px;
  padding: 16rpx 18rpx;
  background: #f5f5f7;
  color: #1d1d1f;
  font-size: 26rpx;
  line-height: 1.45;
}

.chat-line.me .chat-bubble {
  background: rgba(0, 113, 227, 0.1);
  color: #064f9f;
}
</style>
