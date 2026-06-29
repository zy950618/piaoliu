<template>
  <view class="page messages-page safe-bottom">
    <view class="message-toolbar">
      <view class="toolbar-tabs">
        <view class="segment-pill" :class="{ active: activeTab === 'conversations' }" @tap="activeTab = 'conversations'">
          <text class="segment-icon icon-chat" />
          聊天
          <text v-if="historyUnreadCount" class="inline-badge">{{ historyUnreadCount }}</text>
        </view>
        <view class="segment-pill" :class="{ active: activeTab === 'messages' }" @tap="activeTab = 'messages'">
          <text class="segment-icon icon-bell" />
          通知
          <text v-if="unreadCount" class="inline-badge">{{ unreadCount }}</text>
        </view>
      </view>
      <view class="read-all-button" :class="{ disabled: totalUnread === 0 }" @tap="markAllRead">一键已读</view>
    </view>

    <view v-if="activeTab === 'conversations'" class="chat-layout">
      <view class="thread-list">
        <view class="thread-section-head">
          <view>
            <text class="h2">消息</text>
            <text class="muted">按用户归档对话，点击进入聊天页。</text>
          </view>
        </view>
        <view
          v-for="thread in content.conversationThreads"
          :key="thread.id"
          class="thread-chip"
          @tap="openThread(thread.id)"
        >
          <image v-if="thread.participantAvatarUrl" class="thread-avatar image-avatar" :src="thread.participantAvatarUrl" mode="aspectFill" />
          <text v-else class="thread-avatar">{{ avatarText(thread) }}</text>
          <view class="thread-main">
            <view class="thread-title-row">
              <text class="thread-name">{{ thread.participantName }}</text>
              <text class="thread-time">{{ formatThreadTime(thread.updatedAt) }}</text>
            </view>
            <text class="thread-tag">{{ thread.participantTag }}</text>
            <text class="thread-last">{{ thread.lastMessage || thread.bottlePreview }}</text>
          </view>
          <view class="thread-side">
            <text v-if="thread.unreadCount > 0" class="unread-dot">{{ thread.unreadCount }}</text>
            <text class="thread-arrow">›</text>
          </view>
        </view>
      </view>

      <EmptyState
        v-if="content.conversationThreads.length === 0"
        title="暂无聊天"
        body="捞到瓶子并回应后，对话会保存在这里。"
      />
    </view>

    <view v-else class="section">
      <view v-for="message in content.messages" :key="message.id" class="panel message-card" @tap="openMessage(message)">
        <view class="between">
          <text class="h2">{{ message.title }}</text>
          <text v-if="message.unread" class="tag">新</text>
        </view>
        <text class="body message-body">{{ message.body }}</text>
        <view class="message-foot">
          <text class="muted">{{ message.createdAt }}</text>
          <view class="message-action">
            <text>{{ messageActionLabel(message) }}</text>
            <text class="message-arrow">›</text>
          </view>
        </view>
      </view>
      <EmptyState v-if="content.messages.length === 0" title="暂无消息" body="瓶子回复、树洞回应和系统通知会出现在这里。" />
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import EmptyState from '@/components/EmptyState.vue'
import { navigateTo, showToast, switchTab } from '@/services/feedback'
import { useContentStore } from '@/stores/content'
import type { ConversationThread, MessageItem } from '@/types/domain'

const content = useContentStore()
const unreadCount = computed(() => content.messages.filter((item) => item.unread).length)
const historyUnreadCount = computed(() => content.conversationThreads.reduce((sum, thread) => sum + thread.unreadCount, 0))
const totalUnread = computed(() => unreadCount.value + historyUnreadCount.value)
const activeTab = ref<'conversations' | 'messages'>('conversations')
const tabPages = new Set(['/pages/bottle/index', '/pages/plaza/index', '/pages/game/index', '/pages/messages/index', '/pages/profile/index'])
type MessageTarget = {
  page: string
  threadId?: string
  useTab?: boolean
}

onLoad(() => {
  void loadPage()
})

async function loadPage() {
  await Promise.all([content.loadMessages(), content.loadConversationThreads()])
}

function openThread(threadId: string) {
  navigateTo(`/pages/messages/chat?threadId=${threadId}`)
}

function openMessage(message: MessageItem) {
  const target = messageTarget(message)
  if (target.threadId) {
    navigateTo(`/pages/messages/chat?threadId=${target.threadId}`)
    return
  }
  if (target.page === '/pages/messages/index' && target.useTab) {
    activeTab.value = 'conversations'
    return
  }
  if (tabPages.has(target.page)) {
    switchTab(target.page)
    return
  }
  navigateTo(target.page)
}

function messageActionLabel(message: MessageItem) {
  const target = messageTarget(message)
  if (target.threadId || target.page === '/pages/messages/index') return '去聊天'
  if (target.page.includes('/wallet/')) return '去钱包'
  if (target.page.includes('/membership/')) return '去会员'
  if (target.page.includes('/verification')) return '去认证'
  if (target.page.includes('/blacklist')) return '去黑名单'
  return '查看'
}

function messageTarget(message: MessageItem): MessageTarget {
  const text = `${message.title} ${message.body}`
  if (message.businessType) {
    const businessType = message.businessType.toLowerCase()
    const businessId = message.businessId?.trim()
    if (businessType === 'chat') {
      if (businessId) {
        const thread = content.conversationThreads.find((item) => item.id === businessId)
        if (thread) {
          return { page: '/pages/messages/index', useTab: true, threadId: thread.id }
        }
      }
      return { page: '/pages/messages/index', useTab: true, threadId: undefined }
    }
    if (businessType === 'bottle') {
      if (businessId) {
        const thread = content.conversationThreads.find((item) => item.id === businessId || item.bottleId === businessId)
        if (thread) {
          return { page: '/pages/messages/index', threadId: thread.id }
        }
      }
      return { page: '/pages/messages/index', useTab: true }
    }
    if (businessType === 'treehole') return { page: '/pages/treehole/index', threadId: undefined }
    if (businessType === 'plaza') return { page: '/pages/plaza/index', threadId: undefined }
    if (businessType === 'payment' || businessType === 'ad_reward') return { page: '/pages/wallet/index', threadId: undefined }
    if (businessType === 'membership') return { page: '/pages/membership/index' }
    if (businessType === 'verification') return { page: '/pages/profile/verification' }
    if (businessType === 'checkin') return { page: '/pages/profile/checkin' }
    if (businessType === 'friend' || businessType === 'follow') return { page: '/pages/messages/index', useTab: true }
    if (businessType === 'block') return { page: '/pages/profile/blacklist' }
    if (businessType === 'friendship' || businessType === 'request') return { page: '/pages/messages/index', useTab: true }
    if (businessType === 'report') return { page: '/pages/messages/index', useTab: true }
  }

  if (/会员|VIP|vip/.test(text)) return { page: '/pages/membership/index' }
  if (/充值|金币|礼物|钱包|提现/.test(text)) return { page: '/pages/wallet/index' }
  if (/实名|认证|验证|人脸/.test(text)) return { page: '/pages/profile/verification' }
  if (/黑名单|拉黑|屏蔽/.test(text)) return { page: '/pages/profile/blacklist' }
  if (/签到/.test(text)) return { page: '/pages/profile/checkin' }
  if (/视频奖励|奖励已到账|次数/.test(text)) return { page: '/pages/profile/index' }
  if (/树洞/.test(text)) return { page: '/pages/treehole/index' }
  if (/瓶子|回应|回复|聊天|好友|关注|消息/.test(text)) return { page: '/pages/messages/index', useTab: true }
  return { page: '/pages/profile/records' }
}

function avatarText(thread: ConversationThread) {
  return thread.participantAvatarText || thread.participantName.slice(0, 1)
}

function formatThreadTime(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value.slice(0, 10)
  const now = new Date()
  const sameDay = date.toDateString() === now.toDateString()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  if (sameDay) return `${hours}:${minutes}`
  return `${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

function markAllRead() {
  content.markAllMessagesRead()
  showToast('已全部标为已读')
}
</script>

<style scoped lang="scss">
.message-toolbar {
  position: sticky;
  top: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
  margin: -4rpx -4rpx 18rpx;
  padding: 8rpx 4rpx 14rpx;
  border-radius: 16px;
  border: 1px solid rgba(15, 23, 42, 0.06);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
}

.toolbar-tabs {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: center;
  gap: 8rpx;
  flex: 1;
  min-width: 0;
  border: 1px solid rgba(15, 23, 42, 0.1);
  border-radius: 18px;
  padding: 6rpx;
  background: #f8fafc;
}

.segment-pill,
.read-all-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 58rpx;
  border-radius: 12px;
  padding: 0 20rpx;
  box-sizing: border-box;
  font-size: 25rpx;
  font-weight: 900;
}

.segment-pill {
  position: relative;
  gap: 10rpx;
  min-width: 0;
  border: 1px solid transparent;
  color: #475569;
  background: rgba(255, 255, 255, 0.78);
  transition: color 160ms ease, background 160ms ease, box-shadow 160ms ease;
}

.segment-pill.active {
  color: #fff;
  border-color: rgba(37, 99, 235, 0.24);
  background: linear-gradient(180deg, #3b82f6, #2563eb);
  box-shadow: 0 12rpx 26rpx rgba(37, 99, 235, 0.2);
}

.segment-icon {
  position: relative;
  width: 28rpx;
  height: 28rpx;
  flex: 0 0 auto;
  color: inherit;
}

.segment-icon::before,
.segment-icon::after {
  position: absolute;
  content: '';
  box-sizing: border-box;
}

.icon-chat::before {
  inset: 4rpx 2rpx 6rpx;
  border: 3rpx solid currentColor;
  border-radius: 8rpx;
}

.icon-chat::after {
  left: 8rpx;
  bottom: 2rpx;
  width: 9rpx;
  height: 9rpx;
  border-left: 3rpx solid currentColor;
  border-bottom: 3rpx solid currentColor;
  transform: rotate(-18deg);
}

.icon-bell::before {
  left: 6rpx;
  top: 4rpx;
  width: 16rpx;
  height: 18rpx;
  border: 3rpx solid currentColor;
  border-radius: 12rpx 12rpx 8rpx 8rpx;
}

.icon-bell::after {
  left: 10rpx;
  bottom: 1rpx;
  width: 8rpx;
  height: 5rpx;
  border-radius: 999px;
  background: currentColor;
}

.read-all-button {
  flex: 0 0 auto;
  min-width: 118rpx;
  border: 1px solid rgba(37, 99, 235, 0.16);
  color: #2563eb;
  background: rgba(255, 255, 255, 0.92);
}

.read-all-button.disabled {
  opacity: 0.48;
}

.inline-badge,
.unread-dot {
  min-width: 30rpx;
  border-radius: 999px;
  padding: 4rpx 8rpx;
  color: #fff;
  background: #ef3e36;
  font-size: 19rpx;
  line-height: 1;
  text-align: center;
}

.chat-layout,
.thread-list {
  display: grid;
  gap: 16rpx;
  margin-top: 18rpx;
}

.thread-section-head {
  padding: 4rpx 2rpx 2rpx;
}

.thread-chip {
  display: flex;
  align-items: center;
  gap: 16rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 16px;
  padding: 18rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.9)),
    radial-gradient(circle at 96% 12%, rgba(37, 99, 235, 0.06), transparent 28%);
  box-shadow: 0 12rpx 30rpx rgba(15, 23, 42, 0.06);
  transition: transform 160ms ease, box-shadow 160ms ease;
}

.thread-chip:hover {
  transform: translateY(-3rpx);
  box-shadow: 0 22rpx 48rpx rgba(3, 12, 18, 0.16);
}

.thread-avatar {
  flex: 0 0 auto;
  width: 68rpx;
  height: 68rpx;
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(180deg, #38bdf8, #2563eb);
  font-size: 26rpx;
  font-weight: 900;
  line-height: 68rpx;
  text-align: center;
  box-shadow: 0 10rpx 22rpx rgba(37, 99, 235, 0.14);
}

.image-avatar {
  display: block;
  background: rgba(35, 108, 114, 0.08);
}

.thread-main {
  flex: 1;
  min-width: 0;
}

.thread-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
  min-width: 0;
}

.thread-name,
.thread-tag,
.thread-last {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.thread-name {
  color: #172126;
  font-size: 27rpx;
  font-weight: 900;
}

.thread-time {
  flex: 0 0 auto;
  max-width: 180rpx;
  overflow: hidden;
  color: #8a969b;
  font-size: 20rpx;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.thread-tag {
  margin-top: 5rpx;
  color: #236c72;
  font-size: 21rpx;
  font-weight: 800;
}

.thread-last {
  margin-top: 6rpx;
  color: #65757b;
  font-size: 23rpx;
}

.thread-side {
  display: grid;
  justify-items: end;
  gap: 8rpx;
}

.thread-arrow {
  color: #9aa5aa;
  font-size: 38rpx;
  line-height: 1;
}

.message-card {
  position: relative;
  margin-bottom: 16rpx;
  transition: transform 160ms ease, box-shadow 160ms ease;
}

.message-card:active {
  transform: scale(0.99);
}

.message-body {
  display: block;
  margin: 14rpx 0;
}

.message-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
}

.message-action {
  display: inline-flex;
  align-items: center;
  gap: 6rpx;
  flex: 0 0 auto;
  color: #2563eb;
  font-size: 23rpx;
  font-weight: 900;
}

.message-arrow {
  font-size: 30rpx;
  line-height: 1;
}
</style>
