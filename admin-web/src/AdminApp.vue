<template>
  <main class="admin-shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-mark">D</span>
        <div>
          <strong>漂流岛管理后台</strong>
          <small>Web Admin</small>
        </div>
      </div>

      <nav class="nav-list">
        <button
          v-for="tab in tabs"
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
        <small>独立 Web 后台</small>
        <span>不进入小程序、iOS、Android 用户端路由。</span>
      </div>
    </aside>

    <section class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">运营 / 审核 / 风控</p>
          <h1>{{ currentTabLabel }}</h1>
        </div>
        <div class="session-card">
          <span class="status-dot" :class="{ off: !dashboard?.adminSession.signedIn }"></span>
          <div>
            <strong>{{ dashboard?.adminSession.displayName || '未登录' }}</strong>
            <small>{{ dashboard?.adminSession.role || 'no_session' }}</small>
          </div>
          <button type="button" class="ghost-button" @click="toggleSession">
            {{ dashboard?.adminSession.signedIn ? '退出' : '模拟登录' }}
          </button>
        </div>
      </header>

      <section v-if="loading" class="panel loading-panel">加载管理数据中...</section>

      <template v-else-if="dashboard">
        <section class="metric-grid">
          <article v-for="metric in metrics" :key="metric.label" class="metric-card">
            <span>{{ metric.label }}</span>
            <strong>{{ metric.value }}</strong>
          </article>
        </section>

        <section v-if="activeTab === 'overview'" class="content-grid">
          <article class="panel span-2">
            <div class="panel-head">
              <div>
                <h2>待办队列</h2>
                <p>内容、举报、提现和广告奖励的当前风险面。</p>
              </div>
            </div>
            <div class="queue-grid">
              <button class="queue-card" type="button" @click="setActiveTab('content')">
                <strong>{{ dashboard.summary.pendingContent }}</strong>
                <span>待审内容</span>
              </button>
              <button class="queue-card" type="button" @click="setActiveTab('reports')">
                <strong>{{ dashboard.summary.reports }}</strong>
                <span>举报待处理</span>
              </button>
              <button class="queue-card" type="button" @click="setActiveTab('wallet')">
                <strong>{{ dashboard.summary.pendingWithdrawals }}</strong>
                <span>提现复核</span>
              </button>
              <button class="queue-card" type="button" @click="setActiveTab('audit')">
                <strong>{{ dashboard.auditLogs.length }}</strong>
                <span>审计记录</span>
              </button>
            </div>
          </article>

          <article class="panel">
            <h2>平台边界</h2>
            <ul class="rule-list">
              <li>后台是独立 Web 管理端。</li>
              <li>用户端只保留瓶子、广场、游戏、树洞、我的。</li>
              <li>真实鉴权和落库后续接 PostgreSQL/Redis。</li>
            </ul>
          </article>
        </section>

        <section v-if="activeTab === 'config'" class="panel">
          <div class="panel-head">
            <div>
              <h2>奖励与次数配置</h2>
              <p>首版仍走 Mock，后续对接 `/admin/reward-config`。</p>
            </div>
            <button type="button" class="primary-button" @click="saveConfig">保存配置</button>
          </div>

          <div class="form-grid">
            <label>
              <span>广告冷却分钟</span>
              <input v-model.number="configDraft.adCooldownMinutes" type="number" min="1" />
            </label>
            <label>
              <span>广告每类次数奖励</span>
              <input v-model.number="configDraft.adRewardPerQuota" type="number" min="1" />
            </label>
            <label class="wide">
              <span>一周签到奖励</span>
              <input v-model="checkinRewardsText" type="text" />
            </label>
          </div>

          <div class="quota-grid">
            <label v-for="quota in quotaEntries" :key="quota.type">
              <span>{{ quota.label }}</span>
              <input v-model.number="configDraft.baseQuotas[quota.type]" type="number" min="0" />
            </label>
          </div>
        </section>

        <section v-if="activeTab === 'users'" class="panel">
          <TableHeader title="用户管理" subtitle="统一查看跨端账号、认证状态、会员、风控和收益。" />
          <table>
            <thead>
              <tr>
                <th>用户</th>
                <th>平台</th>
                <th>性别</th>
                <th>VIP</th>
                <th>认证</th>
                <th>安全分</th>
                <th>钱包风险</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in dashboard.users" :key="user.id">
                <td>
                  <strong>{{ user.nickname }}</strong>
                  <small>{{ user.id }}</small>
                </td>
                <td>{{ user.platform }}</td>
                <td>{{ genderText(user.gender) }}</td>
                <td>{{ user.isVip ? 'VIP' : '-' }}</td>
                <td>{{ user.verificationStatus }}</td>
                <td>{{ user.safetyScore }}</td>
                <td><span class="pill" :class="user.walletRisk">{{ user.walletRisk }}</span></td>
                <td><button type="button" class="text-button" @click="selectDetail('用户详情', user)">查看</button></td>
              </tr>
            </tbody>
          </table>
        </section>

        <section v-if="activeTab === 'content'" class="panel">
          <div class="panel-head">
            <div>
              <h2>内容审核</h2>
              <p>按分类处理漂流瓶、树洞、广场、私密照片和聊天记录。</p>
            </div>
            <div class="action-row">
              <button type="button" class="ghost-button" :disabled="!selectedContentIds.length" @click="batchApprove">
                批量通过
              </button>
              <button type="button" class="danger-button" :disabled="!selectedContentIds.length" @click="batchOffline">
                批量下架
              </button>
            </div>
          </div>

          <div class="category-bar">
            <button
              v-for="category in contentCategories"
              :key="category.key"
              type="button"
              class="category-button"
              :class="{ active: activeContentCategory === category.key }"
              @click="setContentCategory(category.key)"
            >
              <span>{{ category.label }}</span>
              <small>{{ category.count }}</small>
            </button>
          </div>

          <div class="review-policy">
            <strong>审核策略</strong>
            <span>正常内容自动通过，不进入人工；举报、命中违规词、风控异常、私密照片才进入审核。命中违规词时发送侧先自动屏蔽，后台保留命中证据。</span>
          </div>

          <table>
            <thead>
              <tr>
                <th></th>
                <th>内容</th>
                <th>分类</th>
                <th>作者</th>
                <th>触发</th>
                <th>风险</th>
                <th>状态</th>
                <th>动作</th>
                <th>原因</th>
                <th></th>
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
                <td class="preview-cell">{{ item.preview }}</td>
                <td>{{ item.category }}</td>
                <td>
                  <strong>{{ item.authorName }}</strong>
                  <small>{{ item.authorId }}</small>
                  <button type="button" class="inline-link" @click="selectUserById(item.authorId)">用户</button>
                </td>
                <td>{{ triggerText(item.reviewTrigger) }}</td>
                <td><span class="pill" :class="item.riskLevel">{{ item.riskLevel }}</span></td>
                <td>{{ item.status }}</td>
                <td>{{ actionText(item.autoAction) }}</td>
                <td>{{ item.reason }}</td>
                <td><button type="button" class="text-button" @click="selectDetail('内容详情', item)">详情</button></td>
              </tr>
            </tbody>
          </table>

          <div v-if="showChatReviews" class="chat-review-section">
            <div class="panel-head nested">
              <div>
                <h2>聊天记录审核</h2>
                <p>用于举报、骚扰、导流、诱导充值等场景的上下文复核。</p>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th>会话双方</th>
                  <th>来源</th>
                  <th>最近消息</th>
                  <th>触发</th>
                  <th>风险</th>
                  <th>状态</th>
                  <th>动作</th>
                  <th>原因</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chat in dashboard.chatReviews" :key="chat.id">
                  <td>
                    <strong>{{ chat.participants.join(' / ') }}</strong>
                    <small>{{ chat.threadId }}</small>
                  </td>
                  <td>{{ sourceText(chat.source) }}</td>
                  <td class="preview-cell">{{ chat.lastMessage }}</td>
                  <td>{{ triggerText(chat.reviewTrigger) }}</td>
                  <td><span class="pill" :class="chat.riskLevel">{{ chat.riskLevel }}</span></td>
                  <td>{{ chat.status }}</td>
                  <td>{{ actionText(chat.autoAction) }}</td>
                  <td>{{ chat.reason }}</td>
                  <td><button type="button" class="text-button" @click="selectDetail('聊天记录详情', chat)">查看对话</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section v-if="activeTab === 'reports'" class="panel">
          <TableHeader title="举报队列" subtitle="举报、拉黑和人工复核入口。" />
          <DataCards :items="dashboard.reports" title-key="targetPreview" @select="selectDetail('举报详情', $event)" />
        </section>

        <section v-if="activeTab === 'orders'" class="panel">
          <TableHeader title="订单记录" subtitle="会员、金币包、平台支付和退款状态。" />
          <DataCards :items="dashboard.orders" title-key="productName" @select="selectDetail('订单详情', $event)" />
        </section>

        <section v-if="activeTab === 'wallet'" class="panel">
          <TableHeader title="钱包与提现风控" subtitle="区分充值金币、收益金币、魅力值和冻结金额。" />
          <DataCards :items="dashboard.walletRisks" title-key="riskReason" @select="selectDetail('钱包详情', $event)" />
        </section>

        <section v-if="activeTab === 'audit'" class="panel">
          <TableHeader title="审计日志" subtitle="管理员操作、配置变更和审核动作记录。" />
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>操作人</th>
                <th>动作</th>
                <th>对象</th>
                <th>详情</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in dashboard.auditLogs" :key="log.id" @click="selectDetail('审计详情', log)">
                <td>{{ log.createdAt }}</td>
                <td>{{ log.operator }}</td>
                <td>{{ log.action }}</td>
                <td>{{ log.target }}</td>
                <td>{{ log.detail }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </template>
    </section>

    <aside v-if="detail" class="detail-drawer">
      <div class="panel-head">
        <div>
          <p class="eyebrow">详情</p>
          <h2>{{ detail.title }}</h2>
        </div>
        <button type="button" class="ghost-button" @click="detail = null">关闭</button>
      </div>
      <dl>
        <template v-for="[key, value] in detailRows" :key="key">
          <dt>{{ key }}</dt>
          <dd>{{ value }}</dd>
        </template>
      </dl>
      <div v-if="detailRelatedUsers.length" class="related-users">
        <h3>对应用户</h3>
        <button v-for="user in detailRelatedUsers" :key="user.id" type="button" class="related-user" @click="selectDetail('用户详情', user)">
          <strong>{{ user.nickname }}</strong>
          <span>{{ user.id }} · {{ genderText(user.gender) }} · {{ user.isVip ? 'VIP' : '非会员' }} · 安全分 {{ user.safetyScore }}</span>
        </button>
      </div>
      <div v-if="detailChatMessages.length" class="chat-transcript">
        <h3>对话内容</h3>
        <article v-for="message in detailChatMessages" :key="message.id" class="chat-bubble">
          <strong>{{ message.senderName }}</strong>
          <p>{{ message.body }}</p>
          <small>{{ message.createdAt }}</small>
        </article>
      </div>
    </aside>
  </main>
</template>

<script setup lang="ts">
import { computed, defineComponent, h, onMounted, ref, type PropType } from 'vue'
import { mockApi } from '@/services/mockApi'
import type { AdminDashboard, AdminRewardConfigDraft, ContentStatus, ConversationTurn } from '@/types/domain'

type TabKey = 'overview' | 'config' | 'users' | 'content' | 'reports' | 'orders' | 'wallet' | 'audit'
type ContentCategoryKey = 'all' | 'bottle' | 'treehole' | 'private_photo' | 'plaza' | 'chat'

const tabs: { key: TabKey; label: string; badge?: string }[] = [
  { key: 'overview', label: '总览' },
  { key: 'config', label: '奖励配置' },
  { key: 'users', label: '用户' },
  { key: 'content', label: '内容审核', badge: 'P0' },
  { key: 'reports', label: '举报' },
  { key: 'orders', label: '订单' },
  { key: 'wallet', label: '钱包提现' },
  { key: 'audit', label: '审计' }
]

const loading = ref(true)
const dashboard = ref<AdminDashboard>()
const activeTab = ref<TabKey>('overview')
const activeContentCategory = ref<ContentCategoryKey>('all')
const selectedContentIds = ref<string[]>([])
const detail = ref<{ title: string; value: Record<string, unknown> } | null>(null)
const configDraft = ref<AdminRewardConfigDraft>({
  baseQuotas: {
    fish_bottle: 0,
    throw_bottle: 0,
    truth: 0,
    dare: 0,
    treehole_post: 0
  },
  adCooldownMinutes: 30,
  adRewardPerQuota: 1,
  checkinRewards: []
})
const checkinRewardsText = ref('')

const currentTabLabel = computed(() => tabs.find((tab) => tab.key === activeTab.value)?.label || '后台')
const metrics = computed(() => {
  const summary = dashboard.value?.summary
  if (!summary) return []
  return [
    { label: '总用户', value: summary.users },
    { label: '今日活跃', value: summary.activeUsers },
    { label: '待审内容', value: summary.pendingContent },
    { label: '举报待处理', value: summary.reports },
    { label: '广告奖励', value: summary.adRewardsToday },
    { label: '今日订单', value: summary.ordersToday },
    { label: '待提现', value: summary.pendingWithdrawals },
    { label: '钱包风险', value: summary.riskWallets }
  ]
})
const quotaEntries = computed(() => {
  const config = dashboard.value?.rewardConfig
  if (!config) return []
  return Object.entries(config.quotaNames).map(([type, label]) => ({ type: type as keyof AdminRewardConfigDraft['baseQuotas'], label }))
})
const detailRows = computed(() => {
  if (!detail.value) return []
  return Object.entries(detail.value.value)
    .filter(([key]) => key !== 'messages')
    .map(([key, value]) => [key, Array.isArray(value) ? value.join(' / ') : String(value ?? '')])
})
const filteredContentReviews = computed(() => {
  const items = dashboard.value?.contentReviews ?? []
  if (activeContentCategory.value === 'all' || activeContentCategory.value === 'chat') {
    return items
  }
  return items.filter((item) => item.type === activeContentCategory.value)
})
const showChatReviews = computed(() => activeContentCategory.value === 'all' || activeContentCategory.value === 'chat')
const contentCategories = computed(() => {
  const content = dashboard.value?.contentReviews ?? []
  const chats = dashboard.value?.chatReviews ?? []
  const countType = (type: Exclude<ContentCategoryKey, 'all' | 'chat'>) => content.filter((item) => item.type === type).length
  return [
    { key: 'all' as const, label: '全部', count: content.length + chats.length },
    { key: 'bottle' as const, label: '漂流瓶', count: countType('bottle') },
    { key: 'treehole' as const, label: '树洞', count: countType('treehole') },
    { key: 'private_photo' as const, label: '私密照片', count: countType('private_photo') },
    { key: 'plaza' as const, label: '广场', count: countType('plaza') },
    { key: 'chat' as const, label: '聊天记录', count: chats.length }
  ]
})
const detailChatMessages = computed<ConversationTurn[]>(() => {
  const messages = detail.value?.value.messages
  return Array.isArray(messages) ? (messages as ConversationTurn[]) : []
})
const detailRelatedUsers = computed(() => {
  if (!detail.value || !dashboard.value) return []
  const value = detail.value.value
  const ids = new Set<string>()
  if (typeof value.authorId === 'string') ids.add(value.authorId)
  if (Array.isArray(value.participantUserIds)) {
    value.participantUserIds.forEach((id) => {
      if (typeof id === 'string') ids.add(id)
    })
  }
  return dashboard.value.users.filter((user) => ids.has(user.id))
})

async function loadDashboard() {
  loading.value = true
  dashboard.value = await mockApi.listAdminData()
  syncConfigDraft()
  openDetailFromHash()
  loading.value = false
}

function syncConfigDraft() {
  if (!dashboard.value) return
  configDraft.value = {
    baseQuotas: { ...dashboard.value.rewardConfig.baseQuotas },
    adCooldownMinutes: dashboard.value.rewardConfig.adCooldownMinutes,
    adRewardPerQuota: dashboard.value.rewardConfig.adRewardPerQuota,
    checkinRewards: [...dashboard.value.rewardConfig.checkinRewards]
  }
  checkinRewardsText.value = dashboard.value.rewardConfig.checkinRewards.join(' / ')
}

async function toggleSession() {
  if (dashboard.value?.adminSession.signedIn) {
    const session = await mockApi.adminLogout()
    dashboard.value.adminSession = session
    return
  }
  const session = await mockApi.adminLogin('admin_demo')
  if (dashboard.value) dashboard.value.adminSession = session
}

async function saveConfig() {
  configDraft.value.checkinRewards = checkinRewardsText.value
    .split(/[\/,，\s]+/)
    .map((item) => Number(item))
    .filter((item) => Number.isFinite(item))
  dashboard.value = await mockApi.saveAdminRewardConfig(configDraft.value)
  syncConfigDraft()
}

function toggleContent(id: string) {
  selectedContentIds.value = selectedContentIds.value.includes(id)
    ? selectedContentIds.value.filter((item) => item !== id)
    : [...selectedContentIds.value, id]
}

function setContentCategory(category: ContentCategoryKey) {
  activeContentCategory.value = category
  selectedContentIds.value = []
  if (activeTab.value === 'content') {
    window.location.hash = category === 'all' ? 'content' : `content:${category}`
  }
}

function setActiveTab(tab: TabKey) {
  activeTab.value = tab
  window.location.hash = tab === 'content' && activeContentCategory.value !== 'all' ? `content:${activeContentCategory.value}` : tab
}

async function batchApprove() {
  await batchReview('approved')
}

async function batchOffline() {
  if (!selectedContentIds.value.length) return
  dashboard.value = await mockApi.batchOfflineContent(selectedContentIds.value)
  selectedContentIds.value = []
}

async function batchReview(status: ContentStatus) {
  if (!selectedContentIds.value.length) return
  dashboard.value = await mockApi.batchReviewContent(selectedContentIds.value, status)
  selectedContentIds.value = []
}

function selectDetail(title: string, value: unknown) {
  detail.value = { title, value: value as Record<string, unknown> }
  const item = value as { id?: string }
  if (title === '聊天记录详情' && item.id) {
    window.location.hash = `content:chat:${item.id}`
  }
}

function selectUserById(userId: string) {
  const user = dashboard.value?.users.find((item) => item.id === userId)
  if (user) {
    selectDetail('用户详情', user)
  }
}

function genderText(gender: string) {
  const map: Record<string, string> = { female: '女', male: '男', unknown: '未知' }
  return map[gender] || gender
}

function sourceText(source: string) {
  const map: Record<string, string> = { bottle: '漂流瓶', treehole: '树洞', plaza: '广场' }
  return map[source] || source
}

function triggerText(trigger: string) {
  const map: Record<string, string> = {
    report: '举报',
    keyword: '违规词',
    risk: '风控',
    private_photo: '私密照片',
    system_sample: '抽检',
    new_user: '新用户'
  }
  return map[trigger] || trigger
}

function actionText(action: string) {
  const map: Record<string, string> = {
    auto_pass: '自动通过',
    mask_and_review: '屏蔽待审',
    reject: '拒绝',
    manual_review: '人工复核'
  }
  return map[action] || action
}

const TableHeader = defineComponent({
  props: {
    title: { type: String, required: true },
    subtitle: { type: String, required: true }
  },
  setup(props) {
    return () =>
      h('div', { class: 'panel-head' }, [
        h('div', [h('h2', props.title), h('p', props.subtitle)])
      ])
  }
})

const DataCards = defineComponent({
  props: {
    items: { type: Array as PropType<unknown[]>, required: true },
    titleKey: { type: String, required: true }
  },
  emits: ['select'],
  setup(props, { emit }) {
    return () =>
      h(
        'div',
        { class: 'card-list' },
        props.items.map((rawItem) => {
          const item = rawItem as Record<string, unknown>
          return h(
            'button',
            {
              type: 'button',
              class: 'data-card',
              onClick: () => emit('select', item)
            },
            [
              h('strong', String(item[props.titleKey] ?? item.id ?? '详情')),
              h(
                'span',
                Object.entries(item)
                  .slice(0, 4)
                  .map(([key, value]) => `${key}: ${String(value)}`)
                  .join(' · ')
              )
            ]
          )
        })
      )
  }
})

function restoreViewFromHash() {
  const hash = window.location.hash.replace(/^#/, '')
  const [tab, category] = hash.split(':')
  if (tabs.some((item) => item.key === tab)) {
    activeTab.value = tab as TabKey
  }
  if (category && activeTab.value === 'content' && ['all', 'bottle', 'treehole', 'private_photo', 'plaza', 'chat'].includes(category)) {
    activeContentCategory.value = category as ContentCategoryKey
  }
}

function openDetailFromHash() {
  const [, category, itemId] = window.location.hash.replace(/^#/, '').split(':')
  if (activeTab.value !== 'content' || category !== 'chat' || !itemId || !dashboard.value) return
  const chat = dashboard.value.chatReviews.find((item) => item.id === itemId)
  if (chat) {
    detail.value = { title: '聊天记录详情', value: chat as unknown as Record<string, unknown> }
  }
}

onMounted(() => {
  restoreViewFromHash()
  void loadDashboard()
})
</script>
