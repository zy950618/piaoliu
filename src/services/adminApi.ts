import type { AdminDashboard, AdminRewardConfigDraft, ContentStatus, ConversationTurn } from '@/types/domain'

const API_BASE_URL = 'http://127.0.0.1:8100'
let token = ''

type AdminLoginCredentials = {
  username: string
  password: string
}

type AdminSummaryDto = {
  users: number
  pending_content: number
  reports: number
  ad_rewards_today: number
  orders_today: number
}

type AdminUserDto = {
  id: string
  nickname: string
  avatar_text: string | null
  avatar_url: string | null
  platform: 'wechat' | 'ios' | 'android' | 'h5'
  gender: 'female' | 'male' | 'unknown'
  is_vip: boolean
  drift_coins: number
  status: 'active' | 'limited' | 'blocked'
  face_verified: boolean
  created_at: string
  blocked_until: string | null
  block_reason: string | null
}

type AdminContentDto = {
  id: string
  type: 'bottle' | 'treehole' | 'plaza' | 'private_photo'
  status: ContentStatus
  author_id: string
  author_name: string | null
  author_avatar_text: string | null
  author_avatar_url: string | null
  excerpt: string
  created_at: string
}

type AdminWalletDto = {
  recharge_coins: number
  earned_coins: number
  gift_coins: number
  frozen_coins: number
  pending_withdrawals: number
}

type AdminAuditDto = {
  id: string
  actor: string
  action: string
  target_type: string
  target_id: string
  created_at: string
}

type ReportDto = {
  id: string
  target_type: 'user' | 'bottle' | 'treehole' | 'reply' | 'chat' | 'plaza' | 'private_photo'
  target_id: string
  reason: string
  status: 'queued' | 'reviewing' | 'resolved'
  created_at: string
  target_type_text?: string | null
  target_display_name?: string | null
  target_avatar_text?: string | null
  target_avatar_url?: string | null
  target_preview?: string | null
}

type AdminChatMessageDto = {
  id: string
  sender_name: string
  body: string
  created_at: string
  from_me: boolean
  type?: ConversationTurn['type']
  media_url?: string
  media_duration?: number
  flash_viewed?: boolean
  gift_id?: string
  gift_name?: string
  gift_icon_text?: string
  gift_price_coins?: number
  game_room_id?: string
  game_room_mode?: ConversationTurn['gameRoomMode']
}

type AdminChatDto = {
  id: string
  thread_id: string
  source: 'bottle' | 'treehole' | 'plaza'
  participant_user_ids: string[]
  participants: string[]
  participant_avatar_texts?: (string | null)[]
  participant_avatar_urls?: (string | null)[]
  related_content: string
  last_message: string
  risk_level: 'low' | 'medium' | 'high'
  status: 'pending' | 'reviewing' | 'resolved'
  review_trigger: 'report' | 'keyword' | 'risk'
  handling_policy: string
  matched_keywords?: string[]
  auto_action: 'mask_and_review' | 'reject' | 'manual_review'
  reason: string
  messages: AdminChatMessageDto[]
  updated_at: string
}

function formatTargetTypeLabel(type: ReportDto['target_type']) {
  return (
    {
      user: '用户',
      bottle: '漂流瓶',
      treehole: '树洞',
      reply: '回应',
      chat: '私信聊天',
      plaza: '广场',
      private_photo: '私密照片'
    }[type]
  )
}

function userDisplayName(item: AdminUserDto) {
  return item.nickname || `用户 ${item.id}`
}

function shortId(id: string) {
  return id ? `${id.slice(0, 6)}...${id.slice(-4)}` : '-'
}

function mapAdminActionLabel(action: string) {
  const map: Record<string, string> = {
    admin_login: '管理员登录',
    admin_logout: '管理员登出',
    update_reward_config: '更新奖励配置',
    user_status_active: '用户恢复',
    user_status_limited: '用户限制',
    user_status_blocked: '用户封禁',
    admin_bootstrap: '系统初始化'
  }
  return map[action] || action.replace(/_/g, ' ')
}

function mapAdminTargetTypeLabel(targetType: string) {
  const map: Record<string, string> = {
    system: '系统',
    admin_session: '管理员会话',
    user: '用户',
    content: '内容',
    moderation_job: '审核任务',
    reward_config: '奖励配置',
    admin_session_action: '管理员会话'
  }
  return map[targetType] || targetType
}

function mapAdminAuditTarget(item: AdminAuditDto) {
  const readableType = mapAdminTargetTypeLabel(item.target_type)
  return `${readableType} · ${shortId(item.target_id)}`
}

function truncateText(value: string | null | undefined, maxLength: number) {
  const text = value?.trim() || ''
  return text.length > maxLength ? `${text.slice(0, maxLength - 1)}…` : text
}

function reportMeta(item: ReportDto) {
  const targetTypeText = item.target_type_text?.trim() || formatTargetTypeLabel(item.target_type)
  const targetDisplayName = item.target_display_name?.trim() || `${targetTypeText} #${shortId(item.target_id)}`
  const targetAvatarText = item.target_avatar_text || targetDisplayName.slice(0, 1) || '目'
  const preview = truncateText(item.target_preview || item.reason, 120)

  return {
    targetTypeText,
    targetDisplayName,
    targetAvatarText,
    targetAvatarUrl: item.target_avatar_url || undefined,
    targetPreview: preview
  }
}

async function requestJson<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {})
    },
    ...options
  })
  if (!response.ok) {
    const body = await response.text()
    throw new Error(body || `HTTP_${response.status}`)
  }
  return response.json() as Promise<T>
}

function buildSession(signedIn = true, admin?: { username: string; roles: string[] }): AdminDashboard['adminSession'] {
  const role = !signedIn ? 'super_admin' : admin?.roles.includes('admin') ? 'super_admin' : admin?.roles.includes('moderator') ? 'content_admin' : 'risk_admin'
  return {
    accountId: admin?.username || 'admin',
    displayName: signedIn ? admin?.username || 'admin' : '未登录',
    role,
    permissions: ['content', 'risk', 'config'],
    signedIn,
    lastLoginAt: new Date().toISOString()
  }
}

export const adminApi = {
  async login(credentials: AdminLoginCredentials = { username: 'admin', password: 'admin_mock_password' }) {
    const response = await requestJson<{ access_token: string; admin: { username: string; roles: string[] } }>('/admin/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
    token = response.access_token
    return buildSession(true, response.admin)
  },

  async logout() {
    if (token) await requestJson('/admin/auth/logout', { method: 'POST' })
    token = ''
    return buildSession(false)
  },

  async listAdminData(options: { autoLogin?: boolean } = { autoLogin: true }): Promise<AdminDashboard> {
    if (!token) {
      if (options.autoLogin === false) throw new Error('ADMIN_NOT_SIGNED_IN')
      await this.login()
    }

    const [summary, users, content, wallet, audit, rewardConfig, reports, chats] = await Promise.all([
      requestJson<AdminSummaryDto>('/admin/summary'),
      requestJson<AdminUserDto[]>('/admin/users'),
      requestJson<AdminContentDto[]>('/admin/content'),
      requestJson<AdminWalletDto>('/admin/wallet'),
      requestJson<AdminAuditDto[]>('/admin/audit'),
      requestJson<{
        base_quotas: Record<string, number>
        ad_cooldown_minutes: number
        ad_reward_per_quota: number
        checkin_rewards: number[]
      }>('/admin/reward-config'),
      requestJson<ReportDto[]>('/admin/reports'),
      requestJson<AdminChatDto[]>('/admin/chats')
    ])

    const reportStatus = (status: ReportDto['status']) => (status === 'queued' ? 'pending' : status)

    return {
      adminSession: buildSession(true),
      summary: {
        users: summary.users,
        activeUsers: users.filter((item) => item.status === 'active').length,
        pendingContent: summary.pending_content,
        reports: summary.reports,
        adRewardsToday: summary.ad_rewards_today,
        ordersToday: summary.orders_today,
        pendingWithdrawals: wallet.pending_withdrawals,
        riskWallets: wallet.frozen_coins > 0 ? 1 : 0
      },
      rewardConfig: {
        baseQuotas: rewardConfig.base_quotas as AdminDashboard['rewardConfig']['baseQuotas'],
        adCooldownMinutes: rewardConfig.ad_cooldown_minutes,
        adRewardPerQuota: rewardConfig.ad_reward_per_quota,
        adReward: `每次+${rewardConfig.ad_reward_per_quota}金币`,
        checkinRewards: rewardConfig.checkin_rewards,
        quotaNames: {
          fish_bottle: '捞瓶',
          throw_bottle: '扔瓶',
          truth: '真心话',
          dare: '大冒险',
          treehole_post: '树洞投稿'
        }
      },
      users: users.map((item) => ({
        id: item.id,
        nickname: userDisplayName(item),
        avatarText: item.avatar_text || '用',
        avatarUrl: item.avatar_url || undefined,
        status: item.status,
        platform: item.platform,
        gender: item.gender,
        isVip: item.is_vip,
        verificationStatus: item.face_verified ? 'approved' : 'not_submitted',
        safetyScore: item.status === 'active' ? 96 : item.status === 'limited' ? 72 : 32,
        walletRisk: item.status === 'blocked' ? 'blocked' : item.status === 'limited' ? 'watch' : 'normal',
        driftCoins: item.drift_coins,
        charmValue: 100,
        joinedAt: item.created_at,
        lastActiveAt: item.created_at,
        blockedUntil: item.blocked_until,
        blockReason: item.block_reason
      })),
      contentReviews: content.map((item) => ({
        id: item.id,
        type: item.type,
        category: item.type,
        authorId: item.author_id,
        authorName: item.author_name || (users.find((user) => user.id === item.author_id)?.nickname || item.author_id),
        authorAvatarText: item.author_avatar_text || undefined,
        authorAvatarUrl: item.author_avatar_url || undefined,
        preview: item.excerpt,
        status: item.status,
        riskLevel: item.status === 'pending' ? 'medium' : item.status === 'rejected' ? 'high' : 'low',
        reviewTrigger: 'system_sample',
        handlingPolicy: '系统采样内容监控',
        autoAction: item.status === 'approved' ? 'auto_pass' : 'manual_review',
        reason: item.status === 'rejected' ? '审核未通过' : '待确认',
        createdAt: item.created_at
      })),
      chatReviews: chats.map((item) => ({
        id: item.id,
        threadId: item.thread_id,
        source: item.source,
        participantUserIds: item.participant_user_ids,
        participants: item.participants,
        participantAvatarTexts: item.participant_avatar_texts || [],
        participantAvatarUrls: item.participant_avatar_urls || [],
        relatedContent: item.related_content,
        lastMessage: item.last_message,
        riskLevel: item.risk_level,
        status: item.status,
        reviewTrigger: item.review_trigger,
        handlingPolicy: item.handling_policy,
        matchedKeywords: item.matched_keywords || [],
        autoAction: item.auto_action,
        reason: item.reason,
        messages: item.messages.map((message) => ({
          id: message.id,
          senderName: message.sender_name,
          body: message.body,
          createdAt: message.created_at,
          fromMe: message.from_me,
          type: message.type,
          mediaUrl: message.media_url,
          mediaDuration: message.media_duration,
          flashViewed: message.flash_viewed,
          giftId: message.gift_id,
          giftName: message.gift_name,
          giftIconText: message.gift_icon_text,
          giftPriceCoins: message.gift_price_coins,
          gameRoomId: message.game_room_id,
          gameRoomMode: message.game_room_mode
        })),
        updatedAt: item.updated_at
      })),
      reports: reports.map((item) => {
        const target = reportMeta(item)
        return {
          id: item.id,
          reporterName: '系统工单',
          targetType: item.target_type,
          targetTypeText: target.targetTypeText,
          targetId: item.target_id,
          targetDisplayName: target.targetDisplayName,
          targetAvatarText: target.targetAvatarText,
          targetAvatarUrl: target.targetAvatarUrl,
          targetPreview: target.targetPreview,
          reason: item.reason,
          status: reportStatus(item.status),
          priority: item.target_type === 'chat' || item.target_type === 'reply' ? 'high' : 'normal',
          createdAt: item.created_at
        }
      }),
      adRewardRecords: [],
      orders: [],
      walletRisks: wallet.pending_withdrawals
        ? [
            {
              id: 'wallet_review_001',
              userId: users[0]?.id ?? '100000000001',
              nickname: users[0]?.nickname ?? '风险用户',
              type: 'withdraw',
              amountCoins: wallet.frozen_coins,
              charmValue: 0,
              status: 'pending',
              riskReason: '异常提现审核',
              createdAt: new Date().toISOString()
            }
          ]
        : [],
      auditLogs: audit.map((item) => ({
        id: item.id,
        operator: item.actor,
        action: mapAdminActionLabel(item.action),
        target: mapAdminAuditTarget(item),
        detail: item.target_id ? `关联标识：${shortId(item.target_id)}` : '-',
        createdAt: item.created_at
      }))
    }
  },

  async saveAdminRewardConfig(config: AdminRewardConfigDraft) {
    await requestJson('/admin/reward-config', {
      method: 'PATCH',
      body: JSON.stringify({
        base_quotas: config.baseQuotas,
        vip_bonus: {
          fish_bottle: 5,
          throw_bottle: 5,
          truth: 5,
          dare: 5,
          treehole_post: 5
        },
        ad_cooldown_minutes: config.adCooldownMinutes,
        ad_reward_per_quota: config.adRewardPerQuota,
        checkin_rewards: config.checkinRewards,
        reject_refund_enabled: false
      })
    })
    return this.listAdminData()
  },

  async setUserStatus(userId: string, status: 'active' | 'limited' | 'blocked', options?: { reason?: string; blockDays?: number; blockedUntil?: string }) {
    await requestJson(`/admin/users/${userId}/status`, {
      method: 'POST',
      body: JSON.stringify({
        status,
        reason: options?.reason,
        block_days: options?.blockDays,
        blocked_until: options?.blockedUntil
      })
    })
    return this.listAdminData()
  },

  async setUserStatuses(
    userIds: string[],
    status: 'active' | 'limited' | 'blocked',
    options?: { reason?: string; blockDays?: number; blockedUntil?: string }
  ) {
    await Promise.all(
      userIds.map((userId) =>
        requestJson(`/admin/users/${userId}/status`, {
          method: 'POST',
          body: JSON.stringify({
            status,
            reason: options?.reason,
            block_days: options?.blockDays,
            blocked_until: options?.blockedUntil
          })
        })
      )
    )
    return this.listAdminData()
  },

  async batchReviewContent(ids: string[], status: ContentStatus) {
    await Promise.all(
      ids.map((id) =>
        requestJson(`/admin/moderation/${id}`, {
          method: 'POST',
          body: JSON.stringify({ action: status === 'approved' ? 'approve' : 'reject', reason: 'batch_review' })
        })
      )
    )
    return this.listAdminData()
  },

  async batchOfflineContent(ids: string[]) {
    await Promise.all(
      ids.map((id) =>
        requestJson(`/admin/moderation/${id}`, {
          method: 'POST',
          body: JSON.stringify({ action: 'reject', reason: 'offline' })
        })
      )
    )
    return this.listAdminData()
  },

  async reviewVerification(userId: string, action: 'approve' | 'reject', reason?: string) {
    return requestJson('/admin/verification/' + userId + '/review', {
      method: 'POST',
      body: JSON.stringify({ action, reason })
    })
  }
}
