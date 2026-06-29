<template>
  <main class="admin-shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">管</div>
        <div>
          <strong>后台监控</strong>
          <small>运营管理中心</small>
        </div>
      </div>

      <nav class="nav-list">
        <button
          v-for="tab in tabsForRender"
          :key="tab.key"
          class="nav-item"
          :class="{ active: activeTab === tab.key }"
          type="button"
          @click="setActiveTab(tab.key)"
        >
          <span>{{ tab.label }}</span>
          <small v-if="tab.badge">{{ tab.badge }}</small>
        </button>
      </nav>

      <div class="sidebar-note">
        <small>运行提示</small>
        <span>按业务模块、昵称和头像查看记录；技术字段只在后台请求中使用。</span>
      </div>
    </aside>

    <section class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">项目运营 / 内容治理 / 会员钱包</p>
          <h1>{{ pageTitle }}</h1>
        </div>
        <div class="session-card">
          <span class="status-dot" :class="{ off: !dashboard.adminSession.signedIn }"></span>
          <div>
            <strong>{{ dashboard.adminSession.displayName }}</strong>
            <small>{{ sessionRoleText(dashboard.adminSession.role) }} · {{ formatDateTime(dashboard.adminSession.lastLoginAt) }}</small>
          </div>
          <button type="button" class="ghost-button" :disabled="operationBusy" @click="toggleSession">{{ dashboard.adminSession.signedIn ? '退出登录' : '登录' }}</button>
        </div>
      </header>

        <section v-if="loading" class="panel loading-panel">加载中...</section>
        <section v-else-if="loadingError" class="panel loading-panel text-error">{{ loadingError }}</section>

      <template v-else>
        <section v-if="operationMessage" class="panel operation-panel" :class="{ 'text-error': operationMessage.includes('失败') }">{{ operationMessage }}</section>

        <section class="metric-grid">
          <article v-for="metric in metrics" :key="metric.label" class="metric-card">
            <span>{{ metric.label }}</span>
            <strong>{{ metric.value }}</strong>
          </article>
        </section>

        <section class="panel" v-if="activeTab === 'overview'">
          <div class="panel-head">
            <div>
              <h2>任务面板</h2>
              <p>按优先级和类型快速确认待处理项</p>
            </div>
            <button type="button" class="text-button" @click="openTab('content')">进入内容中心</button>
          </div>
          <div class="content-grid">
            <article
              v-for="item in taskBoard"
              :key="item.label"
              class="task-card"
              :class="item.theme"
              @click="openTask(item.tab, item.risk, item.category)"
            >
              <strong>{{ item.count }}</strong>
              <span>{{ item.label }}</span>
              <small>{{ item.remark }}</small>
            </article>
            <article class="task-card">
              <strong>{{ dashboard.summary.pendingContent }}</strong>
              <span>待审核内容总量</span>
              <small>含瓶子 / 树洞 / 广场 / 私密照</small>
            </article>
          </div>
        </section>

        <section v-if="activeTab === 'users'" class="panel">
          <div class="panel-head users-head">
            <div>
              <h2>用户与认证</h2>
              <p>按昵称、账号编号和实名状态处理用户风险</p>
            </div>
            <div class="action-row">
              <button type="button" class="ghost-button" :disabled="operationBusy" @click="setBatchStatus('active')">批量恢复</button>
              <button type="button" class="ghost-button" :disabled="operationBusy" @click="setBatchStatus('limited')">批量限制</button>
              <button type="button" class="danger-button" :disabled="operationBusy" @click="setBatchStatus('blocked')">批量封禁</button>
            </div>
          </div>

          <div class="users-toolbar">
            <input v-model="userKeyword" type="search" placeholder="搜索昵称 / 账号编号" />
            <select v-model="userStatusFilter">
              <option value="">全部状态</option>
              <option value="active">正常</option>
              <option value="limited">受限</option>
              <option value="blocked">封禁</option>
            </select>
            <select v-model="userVerifyFilter">
              <option value="">全部认证</option>
              <option value="approved">已认证</option>
              <option value="pending">待审核</option>
              <option value="rejected">不通过</option>
              <option value="not_submitted">未提交</option>
            </select>
            <input
              v-model.number="userBatchDays"
              type="number"
              class="ban-days"
              min="1"
              max="365"
              placeholder="封禁天数"
            />
            <input v-model="userBatchReason" type="text" class="ban-reason" placeholder="封禁原因（可选）" />
            <button type="button" class="ghost-button" @click="clearUserFilters">重置</button>
          </div>

          <table>
            <thead>
              <tr>
                <th style="width: 40px">
                  <input
                    type="checkbox"
                    :checked="allUsersChecked"
                    @change="toggleAllUsers"
                  />
                </th>
                <th>用户</th>
                <th>平台</th>
                <th>性别</th>
                <th>状态</th>
                <th>会员</th>
                <th>封禁到期</th>
                <th>封禁原因</th>
                <th>风控</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>
                  <input
                    type="checkbox"
                    :checked="selectedUserIds.includes(user.id)"
                    @change="toggleUser(user.id)"
                  />
                </td>
                <td>
                  <div class="user-cell">
                    <img v-if="user.avatarUrl" class="avatar-img" :src="user.avatarUrl" :alt="user.nickname" />
                    <span v-else class="avatar">{{ userAvatarText(user.nickname, user.avatarText) }}</span>
                    <div>
                      <strong>{{ user.nickname }}</strong>
                  <small>{{ visibleCode(user.id, '账号编号') }}</small>
                    </div>
                  </div>
                </td>
                <td>{{ platformText(user.platform) }}</td>
                <td>{{ genderText(user.gender) }}</td>
                <td><span class="pill" :class="user.status">{{ userStatusText(user.status) }}</span></td>
                <td>{{ user.isVip ? '会员' : '-' }}</td>
                <td>{{ formatDateTime(user.blockedUntil) || '-' }}</td>
                <td>{{ user.blockReason || '-' }}</td>
                <td><span class="pill" :class="user.walletRisk">{{ walletRiskText(user.walletRisk) }}</span></td>
                <td class="inline-actions">
                  <button type="button" class="text-button" :disabled="operationBusy" @click="setUserStatus(user.id, 'active')">恢复</button>
                  <button type="button" class="text-button" :disabled="operationBusy" @click="setUserStatus(user.id, 'limited')">限制</button>
                  <button type="button" class="danger-button" :disabled="operationBusy" @click="setUserStatus(user.id, 'blocked', userBatchReason, userBatchDays)">封禁</button>
                </td>
              </tr>
            </tbody>
          </table>
        </section>

        <section v-if="activeTab === 'content'" class="panel">
          <div class="panel-head">
            <div>
              <h2>内容池治理</h2>
              <p>按列表筛选、风险等级和审核状态处理内容</p>
            </div>
            <div class="action-row">
              <button type="button" class="ghost-button" :disabled="operationBusy || !selectedContentIds.length" @click="batchReview('approved')">批量通过</button>
              <button type="button" class="danger-button" :disabled="operationBusy || !selectedContentIds.length" @click="batchReview('rejected')">批量下线</button>
            </div>
          </div>

          <div class="list-filterbar">
            <label>
              内容类型
              <select v-model="activeContentCategory">
                <option v-for="category in contentCategories" :key="category.key" :value="category.key">
                  {{ category.label }}（{{ category.count }}）
                </option>
              </select>
            </label>
            <label>
              风险等级
              <select v-model="contentRiskFilter">
                <option v-for="filter in riskFilters" :key="filter.value" :value="filter.value">
                  {{ filter.label }}
                </option>
              </select>
            </label>
            <label>
              审核状态
              <select v-model="contentStatusFilter">
                <option v-for="filter in contentStatusFilters" :key="filter.value" :value="filter.value">
                  {{ filter.label }}（{{ filter.count }}）
                </option>
              </select>
            </label>
            <span class="filter-summary">当前 {{ filteredContentReviews.length }} 条</span>
          </div>

          <table>
            <thead>
              <tr>
                <th style="width: 36px"></th>
                <th>类别</th>
                <th>作者</th>
                <th>性别</th>
                <th>内容</th>
                <th>状态</th>
                <th>风险</th>
                <th>触发</th>
                <th>动作</th>
                <th>原因</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredContentReviews" :key="item.id">
                <td>
                  <input
                    type="checkbox"
                    :checked="selectedContentIds.includes(item.id)"
                    @change="toggleContent(item.id)"
                  />
                </td>
                <td>{{ categoryLabel(item.category) }}</td>
                <td>
                  <div class="user-cell">
                    <img
                      v-if="item.authorAvatarUrl"
                      class="avatar-img avatar-small"
                      :src="item.authorAvatarUrl"
                      :alt="item.authorName"
                    />
                    <span v-else class="avatar avatar-small">{{ userAvatarText(item.authorName, item.authorAvatarText) }}</span>
                    <div>
                      <strong>{{ item.authorName }}</strong>
                      <small>{{ categoryLabel(item.category) }}作者</small>
                    </div>
                  </div>
                </td>
                <td>{{ genderText(contentAuthorGender(item)) }}</td>
                <td class="preview-cell">{{ item.preview }}</td>
                <td><span class="pill" :class="item.status">{{ contentStatusText(item.status) }}</span></td>
                <td><span class="pill" :class="item.riskLevel">{{ riskText(item.riskLevel) }}</span></td>
                <td>{{ triggerText(item.reviewTrigger) }}</td>
                <td>{{ actionText(item.autoAction) }}</td>
                <td>{{ item.reason }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section v-if="activeTab === 'chats'" class="panel">
          <div class="panel-head">
            <div>
              <h2>聊天与互动安全</h2>
              <p>按会话窗口查看上下文、纪律状态和处理策略</p>
            </div>
          </div>

          <div class="chat-console">
            <aside class="chat-session-list">
              <div class="list-filterbar compact">
                <label>
                  来源
                  <select v-model="activeChatSourceFilter">
                    <option v-for="filter in chatSourceFilters" :key="filter.value" :value="filter.value">
                      {{ filter.label }}（{{ filter.count }}）
                    </option>
                  </select>
                </label>
                <label>
                  风险
                  <select v-model="activeChatRiskFilter">
                    <option v-for="filter in riskFilters" :key="`chat-risk-${filter.value}`" :value="filter.value">
                      {{ filter.label }}（{{ chatRiskCount(filter.value) }}）
                    </option>
                  </select>
                </label>
              </div>

              <button
                v-for="chat in filteredChats"
                :key="chat.id"
                type="button"
                class="chat-session-item"
                :class="{ selected: selectedChat?.id === chat.id }"
                @click="selectedChatId = chat.id"
              >
                <span class="chat-session-main">
                  <strong>{{ chat.participants.join(' / ') }}</strong>
                  <span class="pill" :class="chat.disciplineStatus">{{ disciplineStatusText(chat.disciplineStatus) }}</span>
                </span>
                <span class="chat-session-meta">
                  {{ contentTypeLabel(chat.source) }} · {{ chat.messages.length }} 条 · {{ formatDateTime(chat.updatedAt) }}
                </span>
                <span class="chat-session-last">{{ chat.lastMessage }}</span>
              </button>
            </aside>

            <section v-if="selectedChat" class="chat-window">
              <header class="chat-window-head">
                <div class="chips">
                  <span
                    class="chip profile-chip"
                    v-for="(participant, index) in selectedChat.participants"
                    :key="`${selectedChat.id}-${participant}-${index}`"
                  >
                    <img
                      v-if="selectedChat.participantAvatarUrls?.[index]"
                      class="avatar avatar-small"
                      :src="selectedChat.participantAvatarUrls[index] || ''"
                      :alt="participant"
                    />
                    <span v-else class="avatar avatar-small">
                      {{ userAvatarText(participant, selectedChat.participantAvatarTexts?.[index] || undefined) }}
                    </span>
                    {{ participant }}
                  </span>
                </div>
                <div class="chat-window-meta">
                  <span>{{ contentTypeLabel(selectedChat.source) }}</span>
                  <span>{{ chatStatusText(selectedChat.status) }}</span>
                  <span>{{ riskText(selectedChat.riskLevel) }}风险</span>
                </div>
              </header>

              <div class="chat-message-list">
                <article
                  v-for="message in selectedChat.messages"
                  :key="message.id"
                  class="chat-message"
                  :class="{ mine: message.fromMe, room: message.type === 'game_room' }"
                >
                  <small>{{ message.senderName }} · {{ turnTypeText(message.type) }} · {{ formatDateTime(message.createdAt) }}</small>
                  <p>{{ message.body }}</p>
                  <small v-for="line in messageExtraLines(message)" :key="`${message.id}-${line}`">{{ line }}</small>
                </article>
              </div>
            </section>

            <aside v-if="selectedChat" class="discipline-window">
              <div class="discipline-head">
                <span>聊天纪律</span>
                <strong>{{ disciplineStatusText(selectedChat.disciplineStatus) }}</strong>
              </div>
              <dl class="chat-review-meta">
                <dt>处理分区</dt>
                <dd>{{ sourceTreatmentText(selectedChat.source) }}</dd>
                <dt>纪律摘要</dt>
                <dd>{{ selectedChat.disciplineSummary }}</dd>
                <dt>处理策略</dt>
                <dd>{{ selectedChat.handlingPolicy }}</dd>
                <dt>关联内容</dt>
                <dd>{{ selectedChat.relatedContent || '无关联内容' }}</dd>
                <dt v-if="selectedChat.roomMode">房间模式</dt>
                <dd v-if="selectedChat.roomMode">{{ gameRoomModeText(selectedChat.roomMode) }}</dd>
              </dl>

              <div v-if="selectedChat.matchedKeywords?.length" class="discipline-keywords">
                <span>命中关键词</span>
                <div class="chips">
                  <span v-for="word in selectedChat.matchedKeywords" :key="word" class="chip">{{ word }}</span>
                </div>
              </div>

              <div class="discipline-users">
                <span>关联用户</span>
                <strong
                  v-for="participant in selectedChat.participants"
                  :key="`${selectedChat.id}-user-${participant}`"
                >
                  {{ participant }}
                </strong>
              </div>
            </aside>

            <section v-else class="chat-empty">
              <span>没有符合筛选条件的会话</span>
            </section>
          </div>
        </section>

        <section v-if="activeTab === 'reports'" class="panel">
          <h2>举报处置台</h2>
          <div class="toolbar-actions">
            <button
              v-for="filter in reportStatusFilters"
              :key="`report-status-${filter.value}`"
              type="button"
              class="ghost-button"
              :class="{ active: activeReportStatusFilter === filter.value }"
              @click="activeReportStatusFilter = filter.value"
            >
              {{ filter.label }}（{{ filter.count }}）
            </button>
          </div>
          <div class="toolbar-actions">
            <button
              v-for="filter in reportCategoryFilters"
              :key="`report-type-${filter.value}`"
              type="button"
              class="ghost-button"
              :class="{ active: activeReportTypeFilter === filter.value }"
              @click="activeReportTypeFilter = filter.value"
            >
              {{ filter.label }}（{{ filter.count }}）
            </button>
          </div>
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>目标类型</th>
                <th>目标对象</th>
                <th>原因</th>
                <th>状态</th>
                <th>等级</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredReports" :key="item.id">
                <td>{{ formatDateTime(item.createdAt) }}</td>
                <td>{{ item.targetTypeText || formatReportTypeLabel(item.targetType) }}</td>
                <td>
                  <div class="user-cell">
                    <img
                      v-if="item.targetAvatarUrl"
                      class="avatar-img avatar-small"
                      :src="item.targetAvatarUrl"
                      :alt="item.targetDisplayName || '目标'"
                    />
                    <span v-else class="avatar avatar-small">{{ userAvatarText(item.targetDisplayName || item.targetType, item.targetAvatarText) }}</span>
                    <div>
                      <strong>{{ item.targetDisplayName || '未命名目标' }}</strong>
                      <small>{{ visibleCode(item.targetId, '对象编号') }}</small>
                    </div>
                  </div>
                </td>
                <td class="preview-cell">
                  <p>{{ item.targetPreview || item.reason }}</p>
                </td>
                <td>
                  <span class="pill" :class="item.status">{{ reportStatusLabel(item.status) }}</span>
                </td>
                <td>{{ priorityText(item.priority) }}</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section v-if="activeTab === 'wallet'" class="panel">
          <h2>会员与钱包风控</h2>
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>用户</th>
                <th>类型</th>
                <th>说明</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in dashboard.walletRisks" :key="item.id">
                <td>{{ formatDateTime(item.createdAt) }}</td>
                <td>{{ item.nickname }}</td>
                <td>{{ walletRiskTypeText(item.type) }}</td>
                <td>{{ item.riskReason }}</td>
                <td><span class="pill" :class="item.status">{{ walletRiskStatusText(item.status) }}</span></td>
              </tr>
            </tbody>
          </table>
        </section>

        <section v-if="activeTab === 'audit'" class="panel">
          <h2>后台审计</h2>
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>操作者</th>
                <th>动作</th>
                <th>目标</th>
                <th>说明</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in dashboard.auditLogs" :key="item.id">
                <td>{{ formatDateTime(item.createdAt) }}</td>
                <td>
                  <div class="user-cell">
                    <span class="avatar">{{ userAvatarText(item.operator) }}</span>
                    <div>
                      <strong>{{ item.operator }}</strong>
                      <small>管理员</small>
                    </div>
                  </div>
                </td>
                <td>{{ item.action }}</td>
                <td>{{ item.target }}</td>
                <td>{{ item.detail }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </template>
    </section>
  </main>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { adminApi } from '@/services/adminApi'
import type {
  AdminDashboard,
  AdminSummary,
  AdminUserSummary,
  AdminContentReviewItem,
  AdminChatReviewItem,
  AdminReportItem,
  ConversationTurn,
  ContentStatus,
  AdminContentReviewItem as ContentReviewItemAlias
} from '@/types/domain'

type TabKey = 'overview' | 'users' | 'content' | 'chats' | 'reports' | 'wallet' | 'audit'
type UserStatus = AdminUserSummary['status']
type WalletRisk = AdminUserSummary['walletRisk']
type ContentCategory = 'all' | ContentReviewItemAlias['category']
type RiskLevel = 'all' | 'low' | 'medium' | 'high'
type ContentStatusFilter = 'all' | ContentStatus
type UserStatusFilter = '' | UserStatus
type ReportCategory = 'all' | AdminReportItem['targetType']
type ReportStatusFilter = 'all' | AdminReportItem['status']
type ChatSourceFilter = 'all' | AdminChatReviewItem['source']

type DashTab = { key: TabKey; label: string; badge?: number }

const initialDashboard: AdminDashboard = {
  adminSession: {
    accountId: 'admin',
    displayName: 'admin',
    role: 'super_admin',
    permissions: ['content', 'risk', 'config'],
    signedIn: true,
    lastLoginAt: new Date().toISOString()
  },
  summary: {
    users: 0,
    activeUsers: 0,
    pendingContent: 0,
    reports: 0,
    adRewardsToday: 0,
    ordersToday: 0,
    pendingWithdrawals: 0,
    riskWallets: 0
  },
  rewardConfig: {
    baseQuotas: {
      fish_bottle: 0,
      throw_bottle: 0,
      truth: 0,
      dare: 0,
      treehole_post: 0
    },
    adCooldownMinutes: 15,
    adRewardPerQuota: 10,
    adReward: '每次+10金币',
    checkinRewards: [],
    quotaNames: {
      fish_bottle: '捞瓶',
      throw_bottle: '扔瓶',
      truth: '真心话',
      dare: '大冒险',
      treehole_post: '树洞投稿'
    }
  },
  users: [],
  contentReviews: [],
  chatReviews: [],
  reports: [],
  adRewardRecords: [],
  orders: [],
  walletRisks: [],
  auditLogs: []
}

const tabs: DashTab[] = [
  { key: 'overview', label: '运营总览' },
  { key: 'users', label: '用户与认证' },
  { key: 'content', label: '内容池治理' },
  { key: 'chats', label: '聊天互动' },
  { key: 'reports', label: '举报处置' },
  { key: 'wallet', label: '会员钱包' },
  { key: 'audit', label: '后台审计' }
]

const dashboard = ref<AdminDashboard>(initialDashboard)
const loading = ref(true)
const operationBusy = ref(false)
const operationMessage = ref('')
const activeTab = ref<TabKey>('overview')

const userKeyword = ref('')
const userStatusFilter = ref<UserStatusFilter>('')
const userVerifyFilter = ref<'' | 'approved' | 'pending' | 'rejected' | 'not_submitted'>('')
const userBatchDays = ref(7)
const userBatchReason = ref('')

const selectedUserIds = ref<string[]>([])
const selectedContentIds = ref<string[]>([])
const selectedChatId = ref('')

const activeContentCategory = ref<ContentCategory>('all')
const contentRiskFilter = ref<RiskLevel>('all')
const contentStatusFilter = ref<ContentStatusFilter>('all')
const activeChatSourceFilter = ref<ChatSourceFilter>('all')
const activeChatRiskFilter = ref<RiskLevel>('all')
const activeReportTypeFilter = ref<ReportCategory>('all')
const activeReportStatusFilter = ref<ReportStatusFilter>('all')

const loadingError = ref('')

const tabsWithCounts = computed(() =>
  tabs.map((tab) => {
    if (tab.key === 'users') {
      return { ...tab, badge: dashboard.value.users.length }
    }
    if (tab.key === 'content') {
      return { ...tab, badge: dashboard.value.contentReviews.length }
    }
    if (tab.key === 'chats') {
      return { ...tab, badge: dashboard.value.chatReviews.length }
    }
    if (tab.key === 'reports') {
      return { ...tab, badge: dashboard.value.reports.length }
    }
    return tab
  })
)

const metrics = computed(() => {
  const summary = dashboard.value.summary
  return [
    { label: '总用户', value: summary.users },
    { label: '活跃用户', value: summary.activeUsers },
    { label: '待审内容', value: summary.pendingContent },
    { label: '待处理举报', value: summary.reports },
    { label: '今日奖励发放', value: summary.adRewardsToday },
    { label: '今日订单', value: summary.ordersToday },
    { label: '待处理提现', value: summary.pendingWithdrawals },
    { label: '钱包风险', value: summary.riskWallets }
  ]
})

const riskFilters = [
  { label: '全部', value: 'all' as const },
  { label: '高风险', value: 'high' as const },
  { label: '中风险', value: 'medium' as const },
  { label: '低风险', value: 'low' as const }
]

const riskMap: Record<NonNullable<AdminContentReviewItem['riskLevel']>, string> = {
  high: '高',
  medium: '中',
  low: '低'
}

const reportTypeMap: Record<AdminReportItem['targetType'], string> = {
  user: '用户',
  bottle: '漂流瓶',
  treehole: '树洞',
  reply: '回应',
  chat: '私信聊天',
  plaza: '广场',
  private_photo: '私密照片'
}

const userStatusTextMap: Record<UserStatus, string> = {
  active: '正常',
  limited: '受限',
  blocked: '封禁'
}

const walletRiskTextMap: Record<WalletRisk, string> = {
  normal: '正常',
  watch: '观察',
  blocked: '封禁'
}

const categoryLabelMap: Record<ContentCategory, string> = {
  all: '全部',
  bottle: '漂流瓶',
  treehole: '树洞',
  plaza: '广场',
  private_photo: '私密照片'
}

const contentTypeLabelMap: Record<AdminChatReviewItem['source'], string> = {
  bottle: '漂流瓶',
  treehole: '树洞',
  plaza: '广场',
  game_room: '游戏房间'
}

const reportStatusLabelMap: Record<AdminReportItem['status'], string> = {
  pending: '待处理',
  reviewing: '审核中',
  resolved: '已处理'
}

const contentCategories = computed(() => {
  const content = dashboard.value.contentReviews
  const countType = (type: Exclude<ContentCategory, 'all'>) => content.filter((item) => item.type === type).length
  return [
    { key: 'all' as const, label: '全部', count: content.length },
    { key: 'bottle' as const, label: '漂流瓶', count: countType('bottle') },
    { key: 'treehole' as const, label: '树洞', count: countType('treehole') },
    { key: 'private_photo' as const, label: '私密照片', count: countType('private_photo') },
    { key: 'plaza' as const, label: '广场', count: countType('plaza') }
  ]
})

const chatSourceFilters = computed(() => {
  const rows = dashboard.value.chatReviews
  const countSource = (source: Exclude<ChatSourceFilter, 'all'>) => rows.filter((item) => item.source === source).length
  return [
    { value: 'all' as const, label: '全部会话', count: rows.length },
    { value: 'bottle' as const, label: '漂流瓶', count: countSource('bottle') },
    { value: 'treehole' as const, label: '树洞', count: countSource('treehole') },
    { value: 'plaza' as const, label: '广场', count: countSource('plaza') },
    { value: 'game_room' as const, label: '游戏房间', count: countSource('game_room') }
  ]
})

const reportCategoryFilters = computed(() => {
  const rows = dashboard.value.reports
  const countType = (type: Exclude<ReportCategory, 'all'>) => rows.filter((item) => item.targetType === type).length
  return [
    { value: 'all' as const, label: '全部类型', count: rows.length },
    { value: 'user' as const, label: '用户', count: countType('user') },
    { value: 'bottle' as const, label: '漂流瓶', count: countType('bottle') },
    { value: 'treehole' as const, label: '树洞', count: countType('treehole') },
    { value: 'reply' as const, label: '回应', count: countType('reply') },
    { value: 'chat' as const, label: '私信', count: countType('chat') },
    { value: 'plaza' as const, label: '广场', count: countType('plaza') },
    { value: 'private_photo' as const, label: '私密照', count: countType('private_photo') }
  ]
})

const reportStatusFilters = computed(() => {
  const rows = dashboard.value.reports
  const countStatus = (status: Exclude<ReportStatusFilter, 'all'>) => rows.filter((item) => item.status === status).length
  return [
    { value: 'all' as const, label: '全部状态', count: rows.length },
    { value: 'pending' as const, label: '待处理', count: countStatus('pending') },
    { value: 'reviewing' as const, label: '审核中', count: countStatus('reviewing') },
    { value: 'resolved' as const, label: '已处理', count: countStatus('resolved') }
  ]
})

const contentStatusFilters = computed(() => {
  const rows = dashboard.value.contentReviews
  const countStatus = (status: ContentStatus) => rows.filter((item) => item.status === status).length
  return [
    { value: 'all' as const, label: '全部状态', count: rows.length },
    { value: 'pending' as const, label: '待审', count: countStatus('pending') },
    { value: 'approved' as const, label: '已通过', count: countStatus('approved') },
    { value: 'rejected' as const, label: '已下线', count: countStatus('rejected') }
  ]
})

const filteredUsers = computed(() =>
  dashboard.value.users.filter((user) => {
    const key = userKeyword.value.trim().toLowerCase()
    const byKeyword = !key || user.nickname.toLowerCase().includes(key) || user.id.includes(key)
    const byStatus = !userStatusFilter.value || user.status === userStatusFilter.value
    const byVerify = !userVerifyFilter.value || user.verificationStatus === userVerifyFilter.value
    return byKeyword && byStatus && byVerify
  })
)

const filteredContentReviews = computed(() => {
  let rows = dashboard.value.contentReviews
  if (contentRiskFilter.value !== 'all') {
    rows = rows.filter((item) => item.riskLevel === contentRiskFilter.value)
  }
  if (activeContentCategory.value !== 'all') {
    rows = rows.filter((item) => item.category === activeContentCategory.value)
  }
  if (contentStatusFilter.value !== 'all') {
    rows = rows.filter((item) => item.status === contentStatusFilter.value)
  }
  return rows
})

const filteredChats = computed(() => {
  let rows = dashboard.value.chatReviews
  if (activeChatSourceFilter.value !== 'all') {
    rows = rows.filter((item) => item.source === activeChatSourceFilter.value)
  }
  if (activeChatRiskFilter.value !== 'all') {
    rows = rows.filter((item) => item.riskLevel === activeChatRiskFilter.value)
  }
  return rows
})

const selectedChat = computed(() => {
  if (!filteredChats.value.length) return undefined
  return filteredChats.value.find((item) => item.id === selectedChatId.value) || filteredChats.value[0]
})

const chatRisksBySource = computed(() => {
  let rows = dashboard.value.chatReviews
  if (activeChatSourceFilter.value !== 'all') {
    rows = rows.filter((item) => item.source === activeChatSourceFilter.value)
  }
  return {
    countAll: rows.length,
    countHigh: rows.filter((item) => item.riskLevel === 'high').length,
    countMedium: rows.filter((item) => item.riskLevel === 'medium').length,
    countLow: rows.filter((item) => item.riskLevel === 'low').length
  }
})

const filteredReports = computed(() => {
  let rows = dashboard.value.reports
  if (activeReportTypeFilter.value !== 'all') {
    rows = rows.filter((item) => item.targetType === activeReportTypeFilter.value)
  }
  if (activeReportStatusFilter.value !== 'all') {
    rows = rows.filter((item) => item.status === activeReportStatusFilter.value)
  }
  return rows
})

const allUsersChecked = computed(
  () => filteredUsers.value.length > 0 && filteredUsers.value.every((item) => selectedUserIds.value.includes(item.id))
)

const taskBoard = computed(() => {
  const content = dashboard.value.contentReviews
  const chats = dashboard.value.chatReviews
  const high = [...content, ...chats].filter((item) => item.riskLevel === 'high' && ('status' in item ? item.status !== 'resolved' : true))
  const medium = [...content, ...chats].filter((item) => item.riskLevel === 'medium' && ('status' in item ? item.status !== 'resolved' : true))
  const low = [...content, ...chats].filter((item) => item.riskLevel === 'low' && ('status' in item ? item.status !== 'resolved' : true))
  return [
    {
      label: '高风险',
      remark: '建议优先处理',
      count: high.length,
      risk: 'high' as const,
      tab: 'content' as const,
      category: 'all' as const,
      theme: 'risk-high'
    },
    {
      label: '中风险',
      remark: '建议核验来源',
      count: medium.length,
      risk: 'medium' as const,
      tab: 'content' as const,
      category: 'all' as const,
      theme: 'risk-mid'
    },
    {
      label: '低风险',
      remark: '自动流转',
      count: low.length,
      risk: 'low' as const,
      tab: 'content' as const,
      category: 'all' as const,
      theme: 'risk-low'
    },
    {
      label: '待处理',
      remark: `共 ${dashboard.value.summary.pendingContent} 条`,
      count: dashboard.value.summary.pendingContent,
      risk: 'all' as const,
      tab: 'content' as const,
      category: 'all' as const,
      theme: 'risk-all'
    }
  ]
})

function platformText(platform: AdminUserSummary['platform']) {
  const map: Record<AdminUserSummary['platform'], string> = {
    h5: '网页端',
    wechat: '微信小程序',
    ios: '苹果端',
    android: '安卓端'
  }
  return map[platform]
}

function categoryLabel(type: ContentCategory) {
  return categoryLabelMap[type]
}

function formatReportTypeLabel(type: AdminReportItem['targetType']) {
  return reportTypeMap[type]
}

function contentTypeLabel(type: AdminChatReviewItem['source']) {
  return contentTypeLabelMap[type]
}

function sourceTreatmentText(source: AdminChatReviewItem['source']) {
  const map: Record<AdminChatReviewItem['source'], string> = {
    bottle: '漂流瓶回信复核',
    treehole: '树洞倾诉保护',
    plaza: '广场互动治理',
    game_room: '游戏房间纪律观察'
  }
  return map[source]
}

function disciplineStatusText(status: AdminChatReviewItem['disciplineStatus']) {
  const map: Record<AdminChatReviewItem['disciplineStatus'], string> = {
    clear: '正常',
    watch: '观察',
    violation: '违规'
  }
  return map[status]
}

function gameRoomModeText(mode: NonNullable<ConversationTurn['gameRoomMode']>) {
  const map: Record<NonNullable<ConversationTurn['gameRoomMode']>, string> = {
    truth: '真心话',
    dare: '大冒险',
    mixed: '真心话大冒险'
  }
  return map[mode]
}

function turnTypeText(type: ConversationTurn['type'] = 'text') {
  const map: Record<NonNullable<ConversationTurn['type']>, string> = {
    text: '文字',
    image: '图片',
    voice: '语音',
    video: '视频',
    flash_image: '闪照',
    flash_video: '闪视频',
    gift: '礼物',
    game_room: '游戏房间'
  }
  return map[type]
}

function messageExtraLines(message: ConversationTurn) {
  const lines: string[] = []
  if (message.gameRoomMode) {
    lines.push(`房间模式：${gameRoomModeText(message.gameRoomMode)}`)
  }
  if (message.giftName) {
    lines.push(`礼物：${message.giftIconText || ''}${message.giftName}（${message.giftPriceCoins || 0} 金币）`)
  }
  if (message.mediaUrl) {
    lines.push(`媒体内容：${turnTypeText(message.type)}${message.mediaDuration ? `，${message.mediaDuration} 秒` : ''}`)
  }
  if (message.flashViewed !== undefined && (message.type === 'flash_image' || message.type === 'flash_video')) {
    lines.push(`闪照状态：${message.flashViewed ? '已查看' : '未查看'}`)
  }
  return lines
}

function reportStatusLabel(status: AdminReportItem['status']) {
  return reportStatusLabelMap[status]
}

function genderText(gender: AdminUserSummary['gender']) {
  return gender === 'male' ? '男' : gender === 'female' ? '女' : '未知'
}

function contentAuthorGender(item: AdminContentReviewItem) {
  return item.authorGender || dashboard.value.users.find((user) => user.id === item.authorId)?.gender || 'unknown'
}

function userStatusText(status: UserStatus) {
  return userStatusTextMap[status]
}

function walletRiskText(risk: WalletRisk) {
  return walletRiskTextMap[risk]
}

function riskText(level: 'low' | 'medium' | 'high') {
  return riskMap[level]
}

function contentStatusText(status: ContentStatus) {
  return status === 'approved' ? '已通过' : status === 'rejected' ? '已下线' : '待审'
}

function chatStatusText(status: 'pending' | 'reviewing' | 'resolved') {
  return status === 'resolved' ? '完成' : status === 'reviewing' ? '处理中' : '待处理'
}

function triggerText(trigger: string) {
  const map: Record<string, string> = {
    report: '举报',
    keyword: '关键词',
    risk: '风险',
    private_photo: '私密照',
    system_sample: '系统抽检',
    new_user: '新人'
  }
  return map[trigger] || trigger
}

function actionText(action: string) {
  const map: Record<string, string> = {
    auto_pass: '自动通过',
    mask_and_review: '遮蔽复核',
    reject: '拦截',
    manual_review: '手工复审'
  }
  return map[action] || action
}

function walletRiskTypeText(type: 'withdraw' | 'freeze' | 'charm_review') {
  return type === 'withdraw' ? '提现' : type === 'freeze' ? '冻结' : '魅力审核'
}

function walletRiskStatusText(status: 'pending' | 'reviewing' | 'approved' | 'rejected') {
  const map: Record<typeof status, string> = {
    pending: '待处理',
    reviewing: '复核中',
    approved: '已通过',
    rejected: '已驳回'
  }
  return map[status]
}

function priorityText(priority: AdminReportItem['priority']) {
  return priority === 'high' ? '高优先级' : '普通'
}

function sessionRoleText(role: AdminDashboard['adminSession']['role']) {
  const map: Record<typeof role, string> = {
    super_admin: '超级管理员',
    content_admin: '内容管理员',
    risk_admin: '风控管理员'
  }
  return map[role]
}

function setActiveTab(tab: TabKey) {
  activeTab.value = tab
}

function openTab(tab: Exclude<TabKey, 'overview'>) {
  activeTab.value = tab
}

function openTask(tab: 'content', risk: RiskLevel, category: ContentCategory) {
  activeTab.value = tab
  if (risk !== 'all') {
    contentRiskFilter.value = risk
  }
  activeContentCategory.value = category
}

function toggleUser(id: string) {
  selectedUserIds.value = selectedUserIds.value.includes(id)
    ? selectedUserIds.value.filter((item) => item !== id)
    : [...selectedUserIds.value, id]
}

function toggleContent(id: string) {
  selectedContentIds.value = selectedContentIds.value.includes(id)
    ? selectedContentIds.value.filter((item) => item !== id)
    : [...selectedContentIds.value, id]
}

function toggleAllUsers() {
  if (allUsersChecked.value) {
    selectedUserIds.value = []
    return
  }
  selectedUserIds.value = filteredUsers.value.map((item) => item.id)
}

function clearUserFilters() {
  userKeyword.value = ''
  userStatusFilter.value = ''
  userVerifyFilter.value = ''
}

function visibleCode(id: string, label: string) {
  const shortId = id ? id.slice(-8) : ''
  return shortId ? `${label} ${shortId}` : `${label} -`
}

function formatDateTime(value?: string | null) {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

function userAvatarText(name: string, avatarText?: string) {
  return (avatarText || name || '').trim().slice(0, 1) || '用'
}

function getBlockOptions() {
  return {
    reason: userBatchReason.value.trim() || undefined,
    blockDays: userBatchDays.value || undefined,
    blockedUntil: undefined
  }
}

function formatOperationError(err: unknown) {
  if (!(err instanceof Error)) return '未知错误'
  const map: Record<string, string> = {
    ADMIN_NOT_SIGNED_IN: '管理员未登录',
    ADMIN_LOGIN_FAILED: '管理员账号或密码不正确',
    HTTP_401: '登录已失效，请重新登录',
    HTTP_403: '当前账号没有权限',
    HTTP_404: '记录不存在',
    HTTP_422: '提交内容不符合要求',
    UNKNOWN_ERROR: '未知错误'
  }
  return map[err.message] || err.message
}

async function runAdminOperation(successMessage: string, action: () => Promise<void>) {
  if (operationBusy.value) return
  operationBusy.value = true
  operationMessage.value = ''
  try {
    await action()
    operationMessage.value = successMessage
  } catch (err) {
    operationMessage.value = `操作失败：${formatOperationError(err)}`
  } finally {
    operationBusy.value = false
  }
}

async function setUserStatus(userId: string, status: UserStatus, reason?: string, blockDays?: number) {
  await runAdminOperation('用户状态已更新', async () => {
    const options = status === 'blocked' ? { reason, blockDays, blockedUntil: undefined } : undefined
    dashboard.value = await adminApi.setUserStatus(userId, status, {
      reason: options?.reason,
      blockDays: options?.blockDays,
      blockedUntil: options?.blockedUntil
    })
  })
}

async function setBatchStatus(status: UserStatus) {
  if (!selectedUserIds.value.length) return
  await runAdminOperation('批量用户状态已更新', async () => {
    const options = status === 'blocked'
      ? {
          reason: userBatchReason.value.trim() || undefined,
          blockDays: userBatchDays.value || undefined,
          blockedUntil: undefined
        }
      : undefined
    dashboard.value = await adminApi.setUserStatuses(selectedUserIds.value, status, options)
    selectedUserIds.value = []
  })
}

async function batchReview(status: ContentStatus) {
  if (!selectedContentIds.value.length) return
  await runAdminOperation(status === 'approved' ? '内容已批量通过' : '内容已批量下线', async () => {
    dashboard.value = await adminApi.batchReviewContent(selectedContentIds.value, status)
    selectedContentIds.value = []
  })
}

async function refresh(options: { autoLogin?: boolean } = { autoLogin: true }) {
  loading.value = true
  loadingError.value = ''
  try {
    dashboard.value = await adminApi.listAdminData(options)
  } catch (err) {
    loadingError.value = (err as Error).message
  } finally {
    loading.value = false
  }
}

async function toggleSession() {
  await runAdminOperation(dashboard.value.adminSession.signedIn ? '已退出登录' : '登录成功', async () => {
    if (dashboard.value.adminSession.signedIn) {
      dashboard.value.adminSession = await adminApi.logout()
      selectedUserIds.value = []
      selectedContentIds.value = []
      return
    }
    dashboard.value.adminSession = await adminApi.login()
    await refresh({ autoLogin: false })
  })
}

onMounted(() => {
  void refresh()
})

const pageTitle = computed(() => {
  const title: Record<TabKey, string> = {
    overview: '运营总览',
    users: '用户与认证',
    content: '内容池治理',
    chats: '聊天互动安全',
    reports: '举报处置',
    wallet: '会员钱包风控',
    audit: '后台审计'
  }
  return title[activeTab.value]
})

function chatRiskCount(value: RiskLevel) {
  if (value === 'all') return chatRisksBySource.value.countAll
  if (value === 'high') return chatRisksBySource.value.countHigh
  if (value === 'medium') return chatRisksBySource.value.countMedium
  return chatRisksBySource.value.countLow
}

const tabsForRender = computed(() => {
  return tabsWithCounts.value
})

</script>
