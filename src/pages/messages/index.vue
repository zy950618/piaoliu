<template>
  <view class="page messages-page safe-bottom">
    <view class="message-topbar">
      <view class="inbox-glyph" />
      <text class="message-title">消息</text>
      <view class="window-pill">
        <text class="dot-menu">•••</text>
        <text class="mini-line" />
        <text class="circle-mark" />
      </view>
    </view>

    <view class="quick-actions">
      <view class="quick-action mail" @tap="showMessages('all')">
        <view class="quick-icon">
          <text />
        </view>
        <text>留言消息</text>
        <text v-if="noticeUnreadCount" class="action-badge">{{ noticeUnreadCount }}</text>
      </view>
      <view class="quick-action system" @tap="showMessages('system')">
        <view class="quick-icon">
          <text />
        </view>
        <text>系统消息</text>
        <text v-if="systemUnreadCount" class="action-badge">{{ systemUnreadCount }}</text>
      </view>
    </view>

    <view class="chat-list-head">
      <view>
        <text class="list-title">{{ activeTab === 'messages' ? noticeTitle : '私聊列表' }}</text>
        <text class="list-subtitle">{{ activeTab === 'messages' ? '瓶子、广场、系统通知集中在这里' : '真实两个人聊天，点击进入会话' }}</text>
      </view>
      <view v-if="activeTab === 'messages'" class="mark-read" :class="{ disabled: totalUnread === 0 }" @tap="markAllRead">已读</view>
      <view v-else class="mark-read" :class="{ disabled: historyUnreadCount === 0 }">{{ historyUnreadCount || '0' }}</view>
    </view>

    <view v-if="activeTab === 'conversations'" class="thread-list">
      <view
        v-for="thread in content.conversationThreads"
        :key="thread.id"
        class="thread-card"
        :class="{ frozen: thread.status === 'risk_frozen' }"
        @tap="openThread(thread.id)"
      >
        <image class="thread-avatar image-avatar" :src="threadAvatarUrl(thread)" mode="aspectFill" />
        <view class="thread-main">
          <view class="thread-title-row">
            <text class="thread-name">{{ thread.participantName }}</text>
            <text class="thread-time">{{ formatThreadTime(thread.updatedAt) }}</text>
          </view>
          <text class="thread-tag">{{ thread.status === 'risk_frozen' ? '已冻结' : displayText(thread.participantTag) }}</text>
          <text class="thread-last">{{ displayText(thread.lastMessage || thread.bottlePreview) }}</text>
        </view>
        <view class="thread-side">
          <text v-if="thread.unreadCount > 0" class="unread-dot">{{ thread.unreadCount }}</text>
          <text class="thread-arrow">›</text>
        </view>
      </view>
      <EmptyState
        v-if="content.conversationThreads.length === 0"
        title="暂无私聊"
        body="捞到瓶子并回应后，对话会保存在这里。"
      />
    </view>

    <view v-else class="notice-list">
      <view v-if="noticeFilter !== 'system' && roomInvitations.length" class="notice-section-head room-section">
        <text>游戏房间邀请</text>
        <text class="notice-section-badge">{{ roomInvitations.length }}</text>
      </view>
      <view v-for="invitation in noticeFilter === 'system' ? [] : roomInvitations" :key="invitation.id" class="invite-card room-invite-card">
        <view class="invite-head">
          <view>
            <text class="invite-title">收到私密房间邀请</text>
            <text class="invite-subtitle">24 小时内有效 · 仅房间成员可见</text>
          </view>
          <text class="invite-status">待加入</text>
        </view>
        <view class="invite-body">
          <text>同意后进入房间，可以一起玩骰子、真心话和大冒险。</text>
        </view>
        <view class="invite-actions">
          <view class="invite-button primary" @tap.stop="acceptGameRoomInvitation(invitation.id)">同意并进入</view>
        </view>
      </view>
      <view v-if="pendingContextRequests.length" class="notice-section-head">
        <text>待处理邀请</text>
        <text class="notice-section-badge">{{ pendingContextRequests.length }}</text>
      </view>
      <view
        v-for="request in pendingContextRequests"
        :key="request.id"
        class="invite-card"
        :class="request.status"
        @tap="openContextRequest(request)"
      >
        <view class="invite-head">
          <view>
            <text class="invite-title">{{ contextRequestTitle(request) }}</text>
            <text class="invite-subtitle">{{ contextRequestSubtitle(request) }}</text>
          </view>
          <text class="invite-status">{{ contextRequestStatusText(request) }}</text>
        </view>
        <view class="invite-body">
          <text>{{ contextRequestBody(request) }}</text>
        </view>
        <view class="invite-actions">
          <view
            v-if="request.status === 'pending'"
            class="invite-button ghost"
            @tap.stop="rejectInvitation(request)"
          >
            取消
          </view>
          <view
            v-if="request.status === 'pending'"
            class="invite-button primary"
            @tap.stop="acceptInvitation(request)"
          >
            同意
          </view>
          <view v-else-if="request.status === 'active'" class="invite-button primary">
            进入会话
          </view>
          <view v-else class="invite-button disabled">
            已处理
          </view>
        </view>
      </view>
      <view v-if="handledContextRequests.length" class="notice-section-head muted-section">
        <text>已处理邀请</text>
      </view>
      <view
        v-for="request in handledContextRequests"
        :key="request.id"
        class="invite-card"
        :class="request.status"
        @tap="openContextRequest(request)"
      >
        <view class="invite-head">
          <view>
            <text class="invite-title">{{ contextRequestTitle(request) }}</text>
            <text class="invite-subtitle">{{ contextRequestSubtitle(request) }}</text>
          </view>
          <text class="invite-status">{{ contextRequestStatusText(request) }}</text>
        </view>
        <view class="invite-body">
          <text>{{ contextRequestBody(request) }}</text>
        </view>
        <view class="invite-actions">
          <view v-if="request.status === 'active'" class="invite-button primary">
            进入会话
          </view>
          <view v-else class="invite-button disabled">
            已处理
          </view>
        </view>
      </view>
      <view v-if="visibleMessages.length" class="notice-section-head" :class="noticeFilter === 'system' ? 'system-section' : 'mail-section'">
        <text>{{ noticeFilter === 'system' ? '系统通知' : '留言通知' }}</text>
      </view>
      <view v-for="message in visibleMessages" :key="message.id" class="notice-card" @tap="openMessage(message)">
        <view class="notice-head">
          <text class="notice-title">{{ displayText(message.title) }}</text>
          <text v-if="message.unread" class="notice-new">新</text>
        </view>
        <text class="notice-body">{{ displayText(message.body) }}</text>
        <view class="notice-foot">
          <text>{{ message.createdAt }}</text>
          <text>{{ messageActionLabel(message) }} ›</text>
        </view>
      </view>
      <EmptyState v-if="visibleMessages.length === 0 && visibleContextRequests.length === 0 && (noticeFilter === 'system' || roomInvitations.length === 0)" title="暂无消息" body="留言、邀请和系统通知会出现在这里。" />
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import EmptyState from '@/components/EmptyState.vue'
import { businessApi } from '@/services/businessApi'
import { navigateTo, showToast, switchTab } from '@/services/feedback'
import { useContentStore } from '@/stores/content'
import { resolveAvatarUrl } from '@/utils/avatar'
import type { ContextChatRequest, ConversationThread, MessageItem, RoomInvitation } from '@/types/domain'

const content = useContentStore()
const roomInvitations = ref<RoomInvitation[]>([])
const pendingInvitationCount = computed(() => content.contextChatRequests.filter((item) => item.status === 'pending').length)
const systemMessageTypes = new Set(['system', 'membership', 'payment', 'verification', 'checkin', 'ad_reward', 'chat_freeze', 'chat_restore'])
const systemUnreadCount = computed(() => content.messages.filter((item) => item.unread && isSystemMessage(item)).length)
const noticeUnreadCount = computed(() => content.messages.filter((item) => item.unread && !isSystemMessage(item)).length + pendingInvitationCount.value + roomInvitations.value.length)
const unreadCount = computed(() => noticeUnreadCount.value + systemUnreadCount.value)
const historyUnreadCount = computed(() => content.conversationThreads.reduce((sum, thread) => sum + thread.unreadCount, 0))
const totalUnread = computed(() => unreadCount.value + historyUnreadCount.value)
const activeTab = ref<'conversations' | 'messages'>('conversations')
const noticeFilter = ref<'all' | 'system'>('all')
const tabPages = new Set(['/pages/bottle/index', '/pages/plaza/index', '/pages/game/index', '/pages/messages/index', '/pages/profile/index'])
type MessageTarget = {
  page: string
  threadId?: string
  useTab?: boolean
}

const noticeTitle = computed(() => (noticeFilter.value === 'system' ? '系统消息' : '留言消息'))
const visibleMessages = computed(() => {
  if (noticeFilter.value === 'system') {
    return content.messages.filter(isSystemMessage)
  }
  return content.messages.filter((message) => !isSystemMessage(message))
})
const visibleContextRequests = computed(() => {
  if (noticeFilter.value === 'system') return []
  return content.contextChatRequests
})
const pendingContextRequests = computed(() => visibleContextRequests.value.filter((request) => request.status === 'pending'))
const handledContextRequests = computed(() => visibleContextRequests.value.filter((request) => request.status !== 'pending'))

function isSystemMessage(message: MessageItem) {
  const type = message.businessType?.toLowerCase() || ''
  return systemMessageTypes.has(type)
}

onLoad(() => {
  void loadPage()
})

async function loadPage() {
  const [, , , invitations] = await Promise.all([
    content.loadMessages(),
    content.loadConversationThreads(),
    content.loadContextChatRequests(),
    businessApi.listRoomInvitations()
  ])
  roomInvitations.value = invitations
}

async function acceptGameRoomInvitation(invitationId: string) {
  try {
    const room = await businessApi.acceptRoomInvitation(invitationId)
    roomInvitations.value = roomInvitations.value.filter((item) => item.id !== invitationId)
    showToast('已加入房间')
    navigateTo(`/pages/game/room?roomId=${room.id}`)
  } catch (error) {
    showToast(error instanceof Error ? error.message : '加入房间失败，请稍后重试')
  }
}

function showMessages(filter: 'all' | 'system') {
  noticeFilter.value = filter
  activeTab.value = 'messages'
}

async function openThread(threadId: string) {
  await content.markConversationRead(threadId)
  navigateTo(`/pages/messages/chat?threadId=${threadId}`)
}

function openContextRequest(request: ContextChatRequest) {
  if (request.status === 'active' && request.conversationId) {
    navigateTo(`/pages/messages/chat?contextConversationId=${request.conversationId}`)
    return
  }
  if (request.status === 'pending') {
    showToast('请先同意或取消邀请')
    return
  }
  showToast('邀请已处理')
}

async function acceptInvitation(request: ContextChatRequest) {
  const result = await content.acceptContextChatRequest(request.id, {
    confirmAction: confirmActionForSource(request.sourceType),
    evidenceId: `message_invite_accept:${request.id}`
  })
  showToast(result.conversationId ? '已同意，正在进入会话' : '已同意')
  if (result.conversationId) {
    navigateTo(`/pages/messages/chat?contextConversationId=${result.conversationId}`)
  }
}

async function rejectInvitation(request: ContextChatRequest) {
  await content.rejectContextChatRequest(request.id, 'user_cancel_from_messages')
  showToast('已取消邀请')
}

async function openMessage(message: MessageItem) {
  await content.markMessageRead(message.id)
  const target = messageTarget(message)
  if (target.threadId) {
    await content.markConversationRead(target.threadId)
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
    if (businessType === 'chat' || businessType === 'chat_freeze' || businessType === 'chat_restore') {
      if (businessId) {
        const thread = content.conversationThreads.find((item) => item.id === businessId)
        return { page: '/pages/messages/index', useTab: true, threadId: thread?.id || businessId }
      }
      return { page: '/pages/messages/index', useTab: true }
    }
    if (businessType === 'bottle') {
      if (businessId) {
        const thread = content.conversationThreads.find((item) => item.id === businessId || item.bottleId === businessId)
        if (thread) return { page: '/pages/messages/index', threadId: thread.id }
      }
      return { page: '/pages/messages/index', useTab: true }
    }
    if (businessType === 'treehole') return { page: '/pages/messages/index', useTab: true }
    if (businessType === 'plaza') return { page: '/pages/plaza/index' }
    if (businessType === 'payment' || businessType === 'ad_reward') return { page: '/pages/wallet/index' }
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
  if (/瓶子|回应|回复|聊天|好友|关注|消息/.test(text)) return { page: '/pages/messages/index', useTab: true }
  return { page: '/pages/profile/records' }
}

function threadAvatarUrl(thread: ConversationThread) {
  return resolveAvatarUrl(thread.participantAvatarUrl, thread.participantUserId || thread.id)
}

function contextRequestTitle(request: ContextChatRequest) {
  return request.sourceSummary.title || `${sourceTypeLabel(request.sourceType)}邀请`
}

function contextRequestSubtitle(request: ContextChatRequest) {
  return `${sourceTypeLabel(request.sourceType)} · ${request.sourceId || '本次互动'}`
}

function contextRequestBody(request: ContextChatRequest) {
  if (request.status === 'active') return '已同意邀请，再次点击卡片可直接进入临时会话。'
  if (request.status === 'pending') return '对方已发起基于明确互动的继续聊邀请，同意后开启临时会话。'
  return '该邀请已取消或过期，不会开启会话。'
}

function contextRequestStatusText(request: ContextChatRequest) {
  if (request.status === 'pending') return '待处理'
  if (request.status === 'active') return '已同意'
  if (request.status === 'blocked') return '已拉黑'
  if (request.status === 'reported' || request.status === 'risk_frozen') return '风控中'
  return '已取消'
}

function confirmActionForSource(sourceType: ContextChatRequest['sourceType']) {
  if (sourceType === 'game_room' || sourceType === 'private_room') return 'room_confirm'
  if (sourceType === 'bottle_reply' || sourceType === 'plaza_comment' || sourceType === 'treehole_comment') return 'reply'
  return 'continue_chat'
}

function sourceTypeLabel(sourceType: ContextChatRequest['sourceType']) {
  const labels: Record<ContextChatRequest['sourceType'], string> = {
    bottle_reply: '漂流瓶',
    plaza_comment: '留言',
    treehole_comment: '历史留言',
    game_room: '游戏房间',
    private_room: '私密房间',
    match_expand: '附近的人',
    friend: '好友'
  }
  return labels[sourceType]
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

function displayText(value: string) {
  return value.replace(/树洞/g, '留言')
}
</script>

<style scoped lang="scss">
.messages-page {
  min-height: 100vh;
  min-height: 100dvh;
  padding: 22rpx 22rpx 128rpx;
  color: #fff;
  background: #071225;
}

.message-topbar {
  position: sticky;
  top: 0;
  z-index: 8;
  display: grid;
  grid-template-columns: 76rpx 1fr 164rpx;
  align-items: center;
  gap: 12rpx;
  margin: -4rpx -4rpx 22rpx;
  padding: 10rpx 4rpx 8rpx;
  background: rgba(7, 18, 37, 0.94);
  backdrop-filter: blur(12px);
}

.message-title {
  font-size: 34rpx;
  font-weight: 900;
  text-align: center;
}

.inbox-glyph {
  position: relative;
  width: 64rpx;
  height: 64rpx;
}

.inbox-glyph::before,
.inbox-glyph::after {
  position: absolute;
  content: '';
  box-sizing: border-box;
}

.inbox-glyph::before {
  left: 12rpx;
  top: 20rpx;
  width: 40rpx;
  height: 34rpx;
  border: 5rpx solid #fff;
  border-radius: 5rpx;
}

.inbox-glyph::after {
  left: 18rpx;
  top: 11rpx;
  width: 28rpx;
  height: 18rpx;
  border: 5rpx solid #fff;
  border-bottom: 0;
  border-radius: 5rpx 5rpx 0 0;
}

.window-pill {
  display: grid;
  grid-template-columns: 1fr 1rpx 34rpx;
  align-items: center;
  gap: 18rpx;
  min-height: 64rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.28);
  border-radius: 999px;
  padding: 0 18rpx;
  color: #fff;
  background: rgba(17, 27, 56, 0.86);
  box-sizing: border-box;
}

.dot-menu {
  font-size: 30rpx;
  line-height: 1;
}

.mini-line {
  width: 1rpx;
  height: 32rpx;
  background: rgba(148, 163, 184, 0.4);
}

.circle-mark {
  width: 20rpx;
  height: 20rpx;
  border: 4rpx solid #fff;
  border-radius: 50%;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18rpx;
  margin-bottom: 42rpx;
}

.quick-action {
  position: relative;
  display: grid;
  justify-items: center;
  gap: 14rpx;
  min-height: 152rpx;
  color: #fff;
  font-size: 25rpx;
  font-weight: 900;
}

.quick-icon {
  position: relative;
  width: 86rpx;
  height: 86rpx;
  border-radius: 50%;
  box-shadow: 0 18rpx 34rpx rgba(0, 0, 0, 0.26);
}

.quick-icon text,
.quick-icon::before,
.quick-icon::after {
  position: absolute;
  content: '';
  box-sizing: border-box;
}

.mail .quick-icon {
  background: linear-gradient(145deg, #ff43c7, #ff70aa);
}

.mail .quick-icon::before {
  inset: 24rpx 22rpx;
  border-radius: 10rpx;
  background: #fff;
}

.mail .quick-icon::after {
  left: 31rpx;
  top: 35rpx;
  width: 24rpx;
  height: 14rpx;
  border-left: 5rpx solid #ff5cb6;
  border-bottom: 5rpx solid #ff5cb6;
  transform: rotate(-45deg);
}

.system .quick-icon {
  background: linear-gradient(145deg, #ff8e2b, #ff6d2f);
}

.system .quick-icon::before {
  left: 28rpx;
  top: 23rpx;
  width: 26rpx;
  height: 38rpx;
  border-radius: 9rpx;
  background: #fff;
}

.system .quick-icon::after {
  left: 22rpx;
  top: 31rpx;
  width: 15rpx;
  height: 22rpx;
  border-radius: 10rpx 0 0 10rpx;
  background: #fff;
}

.action-badge {
  position: absolute;
  right: 14rpx;
  top: 4rpx;
  min-width: 30rpx;
  border-radius: 999px;
  padding: 5rpx 8rpx;
  color: #fff;
  background: #ef4444;
  font-size: 18rpx;
  line-height: 1;
  text-align: center;
}

.chat-list-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  margin-bottom: 18rpx;
}

.list-title,
.list-subtitle {
  display: block;
}

.list-title {
  color: #fff;
  font-size: 30rpx;
  font-weight: 900;
}

.list-subtitle {
  margin-top: 6rpx;
  color: #7786aa;
  font-size: 22rpx;
}

.mark-read {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 10rpx 18rpx;
  color: #071225;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
  font-size: 22rpx;
  font-weight: 900;
}

.mark-read.disabled {
  opacity: 0.56;
}

.thread-list,
.notice-list {
  display: grid;
  gap: 18rpx;
}

.notice-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
  margin-top: 4rpx;
  color: #e5eefc;
  font-size: 24rpx;
  font-weight: 900;
}

.notice-section-head.muted-section {
  color: #8792b1;
}

.notice-section-badge {
  min-width: 30rpx;
  border-radius: 999px;
  padding: 5rpx 10rpx;
  color: #071225;
  background: #2dd4bf;
  font-size: 18rpx;
  line-height: 1;
  text-align: center;
}

.thread-card,
.notice-card {
  border-radius: 20rpx;
  background: #151e3e;
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.04);
}

.thread-card {
  display: flex;
  align-items: center;
  gap: 18rpx;
  min-height: 126rpx;
  padding: 18rpx;
}

.thread-card.frozen {
  border: 1rpx solid rgba(251, 191, 36, 0.22);
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.12), #151e3e 44%);
}

.thread-card.frozen .thread-tag {
  color: #fbbf24;
}

.thread-avatar {
  flex: 0 0 auto;
  width: 76rpx;
  height: 76rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.88);
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(145deg, #22d3ee, #2563eb);
}

.image-avatar {
  display: block;
  background: rgba(255, 255, 255, 0.08);
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
  color: #fff;
  font-size: 27rpx;
  font-weight: 900;
}

.thread-time,
.thread-last,
.notice-foot {
  color: #8792b1;
  font-size: 21rpx;
}

.thread-tag {
  margin-top: 6rpx;
  color: #2dd4bf;
  font-size: 21rpx;
  font-weight: 900;
}

.thread-last {
  margin-top: 7rpx;
}

.thread-side {
  display: grid;
  justify-items: end;
  gap: 8rpx;
}

.unread-dot,
.notice-new {
  min-width: 30rpx;
  border-radius: 999px;
  padding: 5rpx 8rpx;
  color: #fff;
  background: #ef4444;
  font-size: 18rpx;
  line-height: 1;
  text-align: center;
}

.thread-arrow {
  color: #6f7da1;
  font-size: 40rpx;
  line-height: 1;
}

.notice-card {
  padding: 20rpx;
}

.invite-card {
  border: 1rpx solid rgba(45, 212, 191, 0.2);
  border-radius: 20rpx;
  padding: 20rpx;
  background: linear-gradient(135deg, rgba(31, 41, 86, 0.98), rgba(16, 31, 67, 0.98));
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.05);
}

.invite-card.active {
  border-color: rgba(45, 212, 191, 0.55);
}

.invite-card.expired {
  opacity: 0.72;
}

.invite-head,
.invite-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
}

.invite-title,
.invite-subtitle {
  display: block;
}

.invite-title {
  color: #fff;
  font-size: 28rpx;
  font-weight: 900;
}

.invite-subtitle,
.invite-body {
  color: #91a0c4;
  font-size: 22rpx;
}

.invite-subtitle {
  margin-top: 6rpx;
}

.invite-status {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 8rpx 14rpx;
  color: #071225;
  background: #2dd4bf;
  font-size: 20rpx;
  font-weight: 900;
}

.invite-body {
  margin: 16rpx 0;
  line-height: 1.45;
}

.invite-button {
  min-width: 132rpx;
  border-radius: 999px;
  padding: 13rpx 20rpx;
  font-size: 23rpx;
  font-weight: 900;
  text-align: center;
  box-sizing: border-box;
}

.invite-button.primary {
  color: #071225;
  background: linear-gradient(135deg, #2af0b6, #22a7ff);
}

.invite-button.ghost {
  color: #b8c2dc;
  background: rgba(148, 163, 184, 0.16);
}

.invite-button.disabled {
  color: #8792b1;
  background: rgba(148, 163, 184, 0.12);
}

.notice-head,
.notice-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14rpx;
}

.notice-title {
  overflow: hidden;
  color: #fff;
  font-size: 27rpx;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-body {
  display: block;
  margin: 12rpx 0;
  color: #b8c2dc;
  font-size: 24rpx;
  line-height: 1.45;
}
</style>
