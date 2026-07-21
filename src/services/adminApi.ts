import type { AdminDashboard, AdminRewardConfigDraft, ContentStatus, ConversationTurn } from '@/types/domain'
import { API_BASE_URL } from '@/services/http'

let token = ''
let currentAdmin: { username: string; roles: string[] } | undefined

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

type AdminRewardConfigDto = {
  base_quotas: Record<string, number>
  vip_bonus: Record<string, number>
  ad_cooldown_minutes: number
  ad_reward_per_quota: number
  checkin_rewards: number[]
  reject_refund_enabled: boolean
  ad_display_type: 'video' | 'image' | 'link'
  ad_provider: string
  ad_placement_id: string
  ad_title: string
  ad_description: string
  ad_media_url?: string | null
  ad_click_url?: string | null
  ad_countdown_seconds: number
  mini_program_app_id?: string | null
  mini_program_path?: string | null
}

type AdminAuditDto = {
  id: string
  actor: string
  action: string
  target_type: string
  target_id: string
  detail?: string | null
  created_at: string
}

type ReportDto = {
  id: string
  reporter_id?: string | null
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
  evidence_refs?: string[]
  audit_refs?: string[]
}

type ReportResolveDto = {
  report_id: string
  before_status: 'queued' | 'reviewing' | 'resolved'
  after_status: 'queued' | 'reviewing' | 'resolved'
  reason: string
  audit_id: string
  resolved_at: string
  penalty_action: 'none' | 'limit_user' | 'freeze_chat' | 'offline_content'
  penalty_target_user_id?: string | null
  penalty_target_thread_id?: string | null
  penalty_target_content_id?: string | null
  penalty_target_content_type?: string | null
  penalty_audit_id?: string | null
}

type ReportRestoreDto = {
  report_id: string
  thread_id: string
  before_thread_status: 'active' | 'risk_frozen'
  after_thread_status: 'active' | 'risk_frozen'
  reason: string
  audit_id: string
  restored_at: string
}

type ChatAppealDto = {
  id: string
  thread_id: string
  user_id: string
  user_name?: string | null
  participant_name?: string | null
  reason: string
  status: AdminDashboard['chatAppeals'][number]['status']
  admin_reason?: string | null
  audit_refs: string[]
  created_at: string
  updated_at: string
}

type ChatAppealReviewDto = {
  appeal_id: string
  thread_id: string
  before_status: AdminDashboard['chatAppeals'][number]['status']
  after_status: AdminDashboard['chatAppeals'][number]['status']
  thread_status: 'active' | 'risk_frozen'
  audit_id: string
  reviewed_at: string
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
  source: 'bottle' | 'treehole' | 'plaza' | 'game_room'
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
  discipline_status?: 'clear' | 'watch' | 'violation'
  discipline_summary?: string
  room_mode?: ConversationTurn['gameRoomMode'] | null
  updated_at: string
}

type AdminContextChatRequestDto = {
  id: string
  status: 'pending' | 'active' | 'muted' | 'blocked' | 'expired' | 'reported' | 'risk_frozen'
  conversation_id?: string | null
  source_type: AdminDashboard['contextChatRequests'][number]['sourceType']
  source_id?: string | null
  source_summary: { title?: string; source_type?: string; source_id?: string }
  rate_limit: { scope?: string; messages_per_minute?: number }
}

type AdminPrivatePhotoReviewDto = {
  id: string
  photo_id: string
  user_id: string
  review_status: AdminDashboard['privatePhotoReviews'][number]['reviewStatus']
  risk_level: AdminDashboard['privatePhotoReviews'][number]['riskLevel']
  model_labels: string[]
  confidence: number
  auto_action: AdminDashboard['privatePhotoReviews'][number]['autoAction']
  report_count: number
  revenue_state: AdminDashboard['privatePhotoReviews'][number]['revenueState']
  assigned_admin_id?: string | null
  updated_at: string
}

type AdminPrivatePhotoRiskSummaryDto = {
  low_risk: number
  medium_risk: number
  high_risk: number
  manual_required: number
  frozen: number
}

function formatTargetTypeLabel(type: ReportDto['target_type']) {
  return (
    {
      user: '用户',
      bottle: '漂流瓶',
      treehole: '历史留言',
      reply: '回应',
      chat: '私信聊天',
      plaza: '广场',
      private_photo: '私密照片'
    }[type]
  )
}

function userDisplayName(item: AdminUserDto) {
  return item.nickname || `用户 ${businessCode(item.id)}`
}

function businessCode(id: string) {
  return id ? id.slice(-8) : '-'
}

function businessTargetText(id: string) {
  const map: Record<string, string> = {
    admin: '系统管理员',
    backend: '后端服务',
    global: '全局配置'
  }
  return map[id] || `编号 ${businessCode(id)}`
}

function adminDisplayName(username?: string) {
  const map: Record<string, string> = {
    admin: '系统管理员',
    moderator: '内容管理员'
  }
  return username ? map[username] || '运营管理员' : '运营管理员'
}

function mapAdminActionLabel(action: string) {
  const map: Record<string, string> = {
    admin_login: '管理员登录',
    admin_logout: '管理员登出',
    update_reward_config: '更新奖励配置',
    user_status_active: '用户恢复',
    user_status_limited: '用户限制',
    user_status_blocked: '用户封禁',
    moderation_approve: '内容通过',
    moderation_reject: '内容下线',
    moderation_manual_review: '人工复核',
    private_photo_ai_approve: '私密照片 AI 通过',
    private_photo_ai_reject: '私密照片 AI 拒绝',
    private_photo_ai_freeze: '私密照片 AI 冻结',
    private_photo_ai_manual_review: '私密照片转人工',
    private_photo_unlock: '私密照片解锁',
    private_photo_appeal: '私密照片申诉',
    private_photo_review_approve: '私密照片复核通过',
    private_photo_review_reject: '私密照片复核拒绝',
    private_photo_review_freeze: '私密照片复核冻结',
    private_photo_review_unfreeze: '私密照片解冻',
    report_resolve: '举报处置',
    report_penalty_limit_user: '举报限制用户',
    report_penalty_freeze_chat: '举报冻结聊天',
    report_penalty_offline_content: '举报下线内容',
    report_restore_chat: '举报恢复聊天',
    chat_appeal_submit: '聊天申诉提交',
    chat_appeal_approve: '聊天申诉通过',
    chat_appeal_reject: '聊天申诉驳回',
    admin_bootstrap: '系统初始化',
    mock_bootstrap: '测试数据初始化'
  }
  return map[action] || '后台操作'
}

function mapAdminTargetTypeLabel(targetType: string) {
  const map: Record<string, string> = {
    system: '系统',
    admin_session: '管理员会话',
    user: '用户',
    content: '内容',
    moderation_job: '审核任务',
    report: '举报工单',
    chat_appeal: '聊天申诉',
    reward_config: '奖励配置',
    private_photo: '私密照片',
    admin_session_action: '管理员会话'
  }
  return map[targetType] || '业务对象'
}

function mapAdminAuditTarget(item: AdminAuditDto) {
  const readableType = mapAdminTargetTypeLabel(item.target_type)
  return `${readableType} · ${businessTargetText(item.target_id)}`
}

function truncateText(value: string | null | undefined, maxLength: number) {
  const text = value?.trim() || ''
  return text.length > maxLength ? `${text.slice(0, maxLength - 1)}…` : text
}

function reportMeta(item: ReportDto) {
  const targetTypeText = item.target_type_text?.trim() || formatTargetTypeLabel(item.target_type)
  const targetDisplayName = item.target_display_name?.trim() || `${targetTypeText} · 编号 ${businessCode(item.target_id)}`
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
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {})
      },
      ...options
    })
  } catch {
    throw new Error('无法连接后台服务，请确认 API 已启动后重试')
  }
  if (!response.ok) {
    const body = await response.text()
    throw new Error(readableError(body, response.status))
  }
  return response.json() as Promise<T>
}

function readableError(body: string, status: number) {
  const statusMap: Record<number, string> = {
    401: '登录已失效，请重新登录',
    403: '当前账号没有权限',
    404: '记录不存在',
    409: '当前状态已变化，请刷新后重试',
    422: '提交内容不符合要求',
    503: '后台服务暂不可用，请稍后重试'
  }
  try {
    const parsed = JSON.parse(body) as {
      error?: { code?: string; message?: string }
      detail?: string | { code?: string; message?: string }
    }
    if (parsed.error?.message) return parsed.error.message
    const detail = parsed.detail
    const code = typeof detail === 'object' ? detail.code : undefined
    if (code === 'ADMIN_LOGIN_FAILED') return '管理员账号或密码不正确'
    if (typeof detail === 'string' && detail) return statusMap[status] || detail
  } catch {
    // Fall back to status text below.
  }
  return statusMap[status] || '请求失败，请稍后重试'
}

function buildSession(signedIn = true, admin?: { username: string; roles: string[] }): AdminDashboard['adminSession'] {
  const activeAdmin = admin || currentAdmin
  const role = !signedIn
    ? 'super_admin'
    : activeAdmin?.roles.some((item) => item === 'super_admin' || item === 'admin')
      ? 'super_admin'
      : activeAdmin?.roles.includes('moderator')
        ? 'content_admin'
        : 'risk_admin'
  return {
    accountId: activeAdmin?.username || 'admin',
    displayName: signedIn ? adminDisplayName(activeAdmin?.username || 'admin') : '未登录',
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
    currentAdmin = response.admin
    return buildSession(true, response.admin)
  },

  async logout() {
    if (token) await requestJson('/admin/auth/logout', { method: 'POST' })
    token = ''
    currentAdmin = undefined
    return buildSession(false)
  },

  async listAdminData(options: { autoLogin?: boolean } = { autoLogin: true }): Promise<AdminDashboard> {
    if (!token) {
      if (options.autoLogin === false) throw new Error('管理员未登录')
      await this.login()
    }

    const [
      summary,
      users,
      content,
      wallet,
      audit,
      rewardConfig,
      reports,
      chatAppeals,
      chats,
      contextChatRequests,
      privatePhotoReviews,
      privatePhotoRiskSummary
    ] = await Promise.all([
      requestJson<AdminSummaryDto>('/admin/summary'),
      requestJson<AdminUserDto[]>('/admin/users'),
      requestJson<AdminContentDto[]>('/admin/content'),
      requestJson<AdminWalletDto>('/admin/wallet'),
      requestJson<AdminAuditDto[]>('/admin/audit'),
      requestJson<AdminRewardConfigDto>('/admin/reward-config'),
      requestJson<ReportDto[]>('/admin/reports'),
      requestJson<ChatAppealDto[]>('/admin/chat-appeals'),
      requestJson<AdminChatDto[]>('/admin/chats'),
      requestJson<AdminContextChatRequestDto[]>('/admin/chat/context-requests'),
      requestJson<AdminPrivatePhotoReviewDto[]>('/admin/private-photos/reviews'),
      requestJson<AdminPrivatePhotoRiskSummaryDto>('/admin/private-photos/risk-summary')
    ])

    const reportStatus = (status: ReportDto['status']) => (status === 'queued' ? 'pending' : status)
    const usersById = new Map(users.map((user) => [user.id, user]))

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
        adReward: `所有玩法各 +${rewardConfig.ad_reward_per_quota} 次`,
        checkinRewards: rewardConfig.checkin_rewards,
        adDisplayType: rewardConfig.ad_display_type,
        adProvider: rewardConfig.ad_provider,
        adPlacementId: rewardConfig.ad_placement_id,
        adTitle: rewardConfig.ad_title,
        adDescription: rewardConfig.ad_description,
        adMediaUrl: rewardConfig.ad_media_url || undefined,
        adClickUrl: rewardConfig.ad_click_url || undefined,
        adCountdownSeconds: rewardConfig.ad_countdown_seconds,
        miniProgramAppId: rewardConfig.mini_program_app_id || undefined,
        miniProgramPath: rewardConfig.mini_program_path || undefined,
        quotaNames: {
          fish_bottle: '捞瓶',
          throw_bottle: '扔瓶',
          truth: '真心话',
          dare: '大冒险',
          treehole_post: '历史留言'
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
        authorGender: usersById.get(item.author_id)?.gender || 'unknown',
        authorAvatarText: item.author_avatar_text || undefined,
        authorAvatarUrl: item.author_avatar_url || undefined,
        preview: item.excerpt,
        status: item.status,
        riskLevel: item.status === 'pending' ? 'medium' : item.status === 'rejected' ? 'high' : 'low',
        reviewTrigger: 'system_sample',
        handlingPolicy: '系统采样内容监控',
        autoAction: item.status === 'approved' ? 'auto_pass' : 'manual_review',
        reason: item.status === 'rejected' ? '审核未通过' : '待人工确认',
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
        disciplineStatus: item.discipline_status || 'clear',
        disciplineSummary: item.discipline_summary || '未发现需要处置的聊天纪律问题。',
        roomMode: item.room_mode,
        updatedAt: item.updated_at
      })),
      contextChatRequests: contextChatRequests.map((item) => ({
            id: item.id,
            status: item.status,
            conversationId: item.conversation_id,
            sourceType: item.source_type,
            sourceId: item.source_id,
            sourceTitle: item.source_summary?.title || '基于本次互动开启',
            participantSummary: item.source_type === 'friend' ? '好友关系' : '上下文双方',
            rateLimitText: `${item.rate_limit?.scope || 'none'}：${item.rate_limit?.messages_per_minute || 6} 条/分钟`
          })),
      privatePhotoReviews: privatePhotoReviews.map((item) => ({
            id: item.id,
            photoId: item.photo_id,
            userId: item.user_id,
            reviewStatus: item.review_status,
            riskLevel: item.risk_level,
            modelLabels: item.model_labels,
            confidence: item.confidence,
            autoAction: item.auto_action,
            reportCount: item.report_count,
            revenueState: item.revenue_state,
            assignedAdminId: item.assigned_admin_id,
            updatedAt: item.updated_at
          })),
      privatePhotoRiskSummary: {
        lowRisk: privatePhotoRiskSummary.low_risk,
        mediumRisk: privatePhotoRiskSummary.medium_risk,
        highRisk: privatePhotoRiskSummary.high_risk,
        manualRequired: privatePhotoRiskSummary.manual_required,
        frozen: privatePhotoRiskSummary.frozen
      },
      reports: reports.map((item) => {
        const target = reportMeta(item)
        return {
          id: item.id,
          reporterId: item.reporter_id || undefined,
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
          createdAt: item.created_at,
          evidenceRefs: item.evidence_refs || [],
          auditRefs: item.audit_refs || []
        }
      }),
      chatAppeals: chatAppeals.map((item) => ({
        id: item.id,
        threadId: item.thread_id,
        userId: item.user_id,
        userName: item.user_name,
        participantName: item.participant_name,
        reason: item.reason,
        status: item.status,
        adminReason: item.admin_reason,
        auditRefs: item.audit_refs || [],
        createdAt: item.created_at,
        updatedAt: item.updated_at
      })),
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
              riskReason: '提现金额进入复核队列',
              createdAt: new Date().toISOString()
            }
          ]
        : [],
      auditLogs: audit.map((item) => ({
        id: item.id,
        operator: adminDisplayName(item.actor),
        action: mapAdminActionLabel(item.action),
        target: mapAdminAuditTarget(item),
        detail: item.detail || (item.target_id ? `关联对象：${businessTargetText(item.target_id)}` : '-'),
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
        reject_refund_enabled: false,
        ad_display_type: config.adDisplayType,
        ad_provider: config.adProvider,
        ad_placement_id: config.adPlacementId,
        ad_title: config.adTitle,
        ad_description: config.adDescription,
        ad_media_url: config.adMediaUrl || null,
        ad_click_url: config.adClickUrl || null,
        ad_countdown_seconds: config.adCountdownSeconds,
        mini_program_app_id: config.miniProgramAppId || null,
        mini_program_path: config.miniProgramPath || null
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
          body: JSON.stringify({ action: status === 'approved' ? 'approve' : 'reject', reason: '批量审核' })
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
          body: JSON.stringify({ action: 'reject', reason: '运营下线' })
        })
      )
    )
    return this.listAdminData()
  },

  async resolveReport(
    reportId: string,
    reason: string,
    penaltyAction: 'none' | 'limit_user' | 'freeze_chat' | 'offline_content' = 'none'
  ): Promise<ReportResolveDto> {
    return requestJson<ReportResolveDto>(`/admin/reports/${reportId}/resolve`, {
      method: 'POST',
      body: JSON.stringify({ action: 'resolve', reason, penalty_action: penaltyAction })
    })
  },

  async restoreReport(reportId: string, reason: string): Promise<ReportRestoreDto> {
    return requestJson<ReportRestoreDto>(`/admin/reports/${reportId}/restore`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    })
  },

  async reviewChatAppeal(appealId: string, action: 'approve' | 'reject', reason: string): Promise<ChatAppealReviewDto> {
    return requestJson<ChatAppealReviewDto>(`/admin/chat-appeals/${appealId}/review`, {
      method: 'POST',
      body: JSON.stringify({ action, reason })
    })
  },

  async reviewVerification(userId: string, action: 'approve' | 'reject', reason?: string) {
    return requestJson('/admin/verification/' + userId + '/review', {
      method: 'POST',
      body: JSON.stringify({ action, reason })
    })
  }
}
