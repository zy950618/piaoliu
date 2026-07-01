import { quotaFullLabels } from '@/constants/product'
import type {
  AdminDashboard,
  AdminRewardConfigDraft,
  AdminSession,
  Bottle,
  BottleTargetGender,
  BottleTargetScope,
  ConversationThread,
  ContentStatus,
  DareTask,
  MeStatus,
  MessageItem,
  QuotaType,
  TreeholePost,
  TruthQuestion
} from '@/types/domain'
import { nowIso } from '@/utils/time'
import {
  addAdRewardToAllQuotas,
  consumeQuota,
  getAdminSummary,
  getMeStatusSnapshot,
  mockState,
  resetAdCooldown,
  tickAdCooldown
} from './mockState'

interface ThrowBottleOptions {
  targetGender?: BottleTargetGender
  targetScope?: BottleTargetScope
}

export interface BottleFilterOptions {
  city?: string
  gender?: string
  ageRange?: string
}

const sensitiveWords = ['站外联系方式', '诱导充值', '加我私下聊', '快速赚金币']

function moderateText(text: string) {
  const matchedKeywords = sensitiveWords.filter((word) => text.includes(word))
  const maskedText = matchedKeywords.reduce((result, word) => result.split(word).join('*'.repeat(word.length)), text)
  return {
    matchedKeywords,
    maskedText,
    shouldReview: matchedKeywords.length > 0
  }
}

function delay<T>(value: T, ms = 160): Promise<T> {
  return new Promise((resolve) => setTimeout(() => resolve(value), ms))
}

function randomPick<T>(items: T[]): T {
  const item = items[Math.floor(Math.random() * items.length)]
  if (!item) {
    throw new Error('EMPTY_LIST')
  }
  return item
}

let lastFishedBottleId = ''

const nearbyCityMap: Record<string, string[]> = {
  杭州: ['杭州', '上海', '宁波', '苏州'],
  上海: ['上海', '杭州', '苏州', '南京'],
  广州: ['广州', '深圳', '佛山'],
  深圳: ['深圳', '广州', '东莞'],
  北京: ['北京', '天津'],
  成都: ['成都', '重庆']
}

function viewerCity() {
  return mockState.user.city || '全国'
}

function isNearbyCity(authorCity?: string, currentCity = viewerCity()) {
  if (!authorCity || !currentCity || currentCity === '全国') return false
  return (nearbyCityMap[currentCity] || [currentCity]).includes(authorCity)
}

function bottleAllowsViewer(item: Bottle) {
  if (item.targetGender && item.targetGender !== 'all' && item.targetGender !== mockState.user.gender) return false
  if (item.targetScope === 'same_city') return item.authorCity === viewerCity()
  if (item.targetScope === 'nearby') return isNearbyCity(item.authorCity)
  return true
}

function matchBottleFilter(item: Bottle, filters: BottleFilterOptions = {}) {
  if (filters.city === '同城' && item.authorCity !== viewerCity()) return false
  if (filters.city === '附近' && !isNearbyCity(item.authorCity)) return false
  if (filters.gender === '女' && item.authorGender !== 'female') return false
  if (filters.gender === '男' && item.authorGender !== 'male') return false
  if (filters.ageRange && filters.ageRange !== '全部' && item.authorAgeRange !== filters.ageRange) return false
  return true
}

function pickBottleForFishing(items: Bottle[], filters: BottleFilterOptions = {}): Bottle {
  const available = items.filter(
    (item) =>
      item.status !== 'rejected' &&
      item.authorId !== mockState.user.id &&
      bottleAllowsViewer(item) &&
      matchBottleFilter(item, filters)
  )
  if (!available.length) {
    throw new Error('NO_MATCHED_BOTTLE')
  }
  const candidates = available.length > 1 ? available.filter((item) => item.id !== lastFishedBottleId) : available
  const bottle = randomPick(candidates.length ? candidates : available)
  lastFishedBottleId = bottle.id
  return bottle
}

function cloneAdminSession(): AdminSession {
  return {
    ...mockState.adminSession,
    permissions: [...mockState.adminSession.permissions]
  }
}

function createAuditLog(action: string, target: string, detail: string) {
  mockState.auditLogs.unshift({
    id: `audit_${Date.now()}`,
    operator: mockState.adminSession.accountId,
    action,
    target,
    detail,
    createdAt: nowIso()
  })
}

function adminReviewExtras(): Pick<AdminDashboard, 'chatAppeals' | 'contextChatRequests' | 'privatePhotoReviews' | 'privatePhotoRiskSummary'> {
  const privatePhotoReviews: AdminDashboard['privatePhotoReviews'] = [
    {
      id: 'mock_photo_review_low',
      photoId: 'mock_photo_review_low',
      userId: mockState.user.id,
      reviewStatus: 'ai_approved',
      riskLevel: 'low_risk',
      modelLabels: ['non_explicit', 'no_sensitive_privacy'],
      confidence: 0.93,
      autoAction: 'approve',
      reportCount: 0,
      revenueState: 'eligible',
      assignedAdminId: null,
      updatedAt: nowIso()
    },
    {
      id: 'mock_photo_review_manual',
      photoId: 'mock_photo_review_manual',
      userId: mockState.user.id,
      reviewStatus: 'manual_required',
      riskLevel: 'medium_risk',
      modelLabels: ['low_confidence', 'borderline_content'],
      confidence: 0.62,
      autoAction: 'manual_review',
      reportCount: 1,
      revenueState: 'frozen',
      assignedAdminId: null,
      updatedAt: nowIso()
    },
    {
      id: 'mock_photo_review_frozen',
      photoId: 'mock_photo_review_frozen',
      userId: mockState.user.id,
      reviewStatus: 'frozen',
      riskLevel: 'high_risk',
      modelLabels: ['high_risk', 'safety_violation'],
      confidence: 0.96,
      autoAction: 'freeze',
      reportCount: 3,
      revenueState: 'ineligible',
      assignedAdminId: null,
      updatedAt: nowIso()
    }
  ]
  return {
    chatAppeals: [],
    contextChatRequests: [
      {
        id: 'mock_ctx_bottle_001',
        status: 'reported',
        conversationId: 'mock_chat_bottle_001',
        sourceType: 'bottle_reply',
        sourceId: 'bottle_001',
        sourceTitle: '基于本次互动开启',
        participantSummary: '发瓶人 / 捞瓶回应者',
        rateLimitText: '非好友上下文：6 条/分钟'
      },
      {
        id: 'mock_ctx_plaza_001',
        status: 'active',
        conversationId: 'mock_chat_plaza_001',
        sourceType: 'plaza_comment',
        sourceId: 'plaza_001:comment_001',
        sourceTitle: '广场评论继续聊',
        participantSummary: '动态作者 / 评论用户',
        rateLimitText: '非好友上下文：6 条/分钟'
      }
    ],
    privatePhotoReviews,
    privatePhotoRiskSummary: {
      lowRisk: privatePhotoReviews.filter((item) => item.riskLevel === 'low_risk').length,
      mediumRisk: privatePhotoReviews.filter((item) => item.riskLevel === 'medium_risk').length,
      highRisk: privatePhotoReviews.filter((item) => item.riskLevel === 'high_risk').length,
      manualRequired: privatePhotoReviews.filter((item) => item.reviewStatus === 'manual_required').length,
      frozen: privatePhotoReviews.filter((item) => item.reviewStatus === 'frozen').length
    }
  }
}

function getAdminDashboardSnapshot(): AdminDashboard {
  return {
    adminSession: cloneAdminSession(),
    summary: getAdminSummary(),
    rewardConfig: {
      baseQuotas: Object.fromEntries(Object.entries(mockState.quotas).map(([type, quota]) => [type, quota.base])) as Record<
        QuotaType,
        number
      >,
      adCooldownMinutes: mockState.adReward.cooldownMinutes,
      adRewardPerQuota: mockState.adReward.rewardPerQuota,
      adReward: `所有玩法次数各 +${mockState.adReward.rewardPerQuota}`,
      checkinRewards: [...mockState.checkin.weekRewards],
      adDisplayType: mockState.adReward.displayType,
      adProvider: mockState.adReward.provider,
      adPlacementId: mockState.adReward.placementId,
      adTitle: mockState.adReward.title,
      adDescription: mockState.adReward.description,
      adMediaUrl: mockState.adReward.mediaUrl,
      adClickUrl: mockState.adReward.clickUrl,
      adCountdownSeconds: mockState.adReward.countdownSeconds,
      miniProgramAppId: mockState.adReward.miniProgramAppId,
      miniProgramPath: mockState.adReward.miniProgramPath,
      quotaNames: quotaFullLabels
    },
    users: mockState.adminUsers.map((item) => ({ ...item })),
    contentReviews: mockState.contentReviews.map((item) => ({ ...item })),
    chatReviews: mockState.chatReviews.map((item) => ({
      ...item,
      participants: [...item.participants],
      messages: item.messages.map((message) => ({ ...message }))
    })),
    ...adminReviewExtras(),
    reports: mockState.adminReports.map((item) => ({ ...item })),
    adRewardRecords: mockState.adRewardRecords.map((item) => ({
      ...item,
      quotaTypes: [...item.quotaTypes]
    })),
    orders: mockState.orderRecords.map((item) => ({ ...item })),
    walletRisks: mockState.walletRiskItems.map((item) => ({ ...item })),
    auditLogs: mockState.auditLogs.map((item) => ({ ...item }))
  }
}

export const mockApi = {
  async adminLogin(accountId: string): Promise<AdminSession> {
    mockState.adminSession.accountId = accountId || 'admin_demo'
    mockState.adminSession.displayName = accountId ? `${accountId} 管理员` : '内容运营管理员'
    mockState.adminSession.signedIn = true
    mockState.adminSession.lastLoginAt = nowIso()
    createAuditLog('管理员登录', mockState.adminSession.accountId, 'Mock 登录态已更新')
    return delay(cloneAdminSession())
  },

  async adminLogout(): Promise<AdminSession> {
    createAuditLog('管理员退出', mockState.adminSession.accountId, 'Mock 登录态已清空')
    mockState.adminSession.signedIn = false
    return delay(cloneAdminSession())
  },

  async getMeStatus(): Promise<MeStatus> {
    return delay(getMeStatusSnapshot())
  },

  async tickAdCooldown(seconds = 1) {
    return delay(tickAdCooldown(seconds), 0)
  },

  async checkin() {
    if (mockState.checkin.checkedToday) {
      return delay({ ...mockState.checkin, user: { ...mockState.user } })
    }
    const reward = mockState.checkin.weekRewards[mockState.checkin.currentWeekIndex] ?? 0
    mockState.user.driftCoins += reward
    mockState.checkin.checkedToday = true
    mockState.checkin.streakDays += 1
    mockState.checkin.lastReward = reward
    mockState.checkin.currentWeekIndex = mockState.checkin.streakDays % mockState.checkin.weekRewards.length
    return delay({ ...mockState.checkin, user: { ...mockState.user } })
  },

  async prepareAdReward() {
    if (!mockState.adReward.canWatch) {
      throw new Error('AD_COOLDOWN')
    }
    const sessionId = `ad_${Date.now()}_${Math.random().toString(16).slice(2)}`
    mockState.adReward.activeSessionId = sessionId
    return delay({ sessionId, rewardPerQuota: mockState.adReward.rewardPerQuota })
  },

  async commitAdReward(sessionId: string, completed: boolean) {
    if (!completed) {
      throw new Error('AD_NOT_COMPLETED')
    }
    if (mockState.settledAdSessions.has(sessionId)) {
      return delay(getMeStatusSnapshot())
    }
    mockState.settledAdSessions.add(sessionId)
    addAdRewardToAllQuotas()
    mockState.wallet.rechargeCoins += 1
    mockState.ledger.unshift({
      id: `ledger_ad_${Date.now()}`,
      title: '看视频奖励金币',
      amount: 1,
      coinBucket: 'recharge',
      withdrawable: false,
      createdAt: nowIso()
    })
    resetAdCooldown()
    return delay(getMeStatusSnapshot())
  },

  async getRandomBottlePrompt(): Promise<string> {
    const index = Math.floor(Math.random() * mockState.bottlePromptTemplates.length)
    return delay(mockState.bottlePromptTemplates[index] || '今天有什么小事让你觉得还不错？')
  },

  async throwBottle(content: string, options: ThrowBottleOptions = {}): Promise<Bottle> {
    const trimmedContent = content.trim()
    if (!trimmedContent) {
      throw new Error('EMPTY_BOTTLE_CONTENT')
    }
    consumeQuota('throw_bottle')
    const moderation = moderateText(trimmedContent)
    const bottle: Bottle = {
      id: `bottle_${Date.now()}`,
      authorId: mockState.user.id,
      authorName: mockState.user.nickname,
      authorAvatarText: mockState.user.avatarText,
      authorVip: mockState.user.isVip,
      authorGender: mockState.user.gender,
      authorAgeRange: '25-30',
      authorCity: mockState.user.city || '全国',
      authorVerified: Boolean(mockState.user.faceVerified && mockState.user.genderVerified),
      content: moderation.maskedText,
      mood: moderation.shouldReview ? '待审核' : '已投递',
      status: moderation.shouldReview ? 'pending' : 'approved',
      replies: 0,
      targetGender: options.targetGender || 'all',
      targetScope: options.targetScope || 'all',
      createdAt: nowIso()
    }
    mockState.bottles.unshift(bottle)
    if (moderation.shouldReview) {
      mockState.contentReviews.unshift({
        id: `review_${bottle.id}`,
        type: 'bottle',
        category: 'bottle',
        authorId: mockState.user.id,
        authorName: mockState.user.nickname,
        preview: moderation.maskedText,
        status: 'pending',
        riskLevel: 'high',
        reviewTrigger: 'keyword',
        handlingPolicy: '发送侧已自动屏蔽违规词，后台保留审核记录。',
        matchedKeywords: moderation.matchedKeywords,
        autoAction: 'mask_and_review',
        reason: `命中违规词：${moderation.matchedKeywords.join(' / ')}`,
        createdAt: nowIso()
      })
    }
    return delay({ ...bottle })
  },

  async fishBottle(filters: BottleFilterOptions = {}): Promise<Bottle> {
    const bottle = pickBottleForFishing(mockState.bottles, filters)
    consumeQuota('fish_bottle')
    return delay({ ...bottle })
  },

  async replyBottle(id: string, content: string) {
    const bottle = mockState.bottles.find((item) => item.id === id)
    const moderation = moderateText(content)
    if (bottle) {
      bottle.replies += 1
      const turn = {
        id: `turn_${Date.now()}`,
        senderName: mockState.user.nickname,
        body: moderation.maskedText,
        createdAt: nowIso(),
        fromMe: true
      }
      const thread = mockState.conversationThreads.find((item) => item.bottleId === id)
      if (thread) {
        thread.turns.push(turn)
        thread.lastMessage = moderation.maskedText
        thread.updatedAt = turn.createdAt
        thread.unreadCount = 0
      } else {
        mockState.conversationThreads.unshift({
          id: `thread_${id}`,
          bottleId: id,
          status: 'active',
          participantUserId: bottle.authorId,
          participantName: bottle.authorName,
          participantTag: '漂流瓶回应',
          bottlePreview: bottle.content,
          lastMessage: moderation.maskedText,
          updatedAt: turn.createdAt,
          unreadCount: 0,
          turns: [
            {
              id: `turn_origin_${id}`,
              senderName: bottle.authorName,
              body: bottle.content,
              createdAt: bottle.createdAt,
              fromMe: false
            },
            turn
          ]
        })
      }
    }
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '回复已送达',
      body: `你回复了瓶子：${moderation.maskedText}`,
      createdAt: nowIso(),
      unread: true
    })
    if (moderation.shouldReview) {
      mockState.chatReviews.unshift({
        id: `chat_review_${Date.now()}`,
        threadId: `thread_${id}`,
        source: 'bottle',
        reporterName: '系统风控',
        participantUserIds: [mockState.user.id, bottle?.authorId || 'unknown'],
        participants: [mockState.user.nickname, bottle?.authorName || '未知用户'],
        relatedContent: `漂流瓶：${bottle?.content || id}`,
        lastMessage: moderation.maskedText,
        riskLevel: 'high',
        status: 'pending',
        reviewTrigger: 'keyword',
        handlingPolicy: '聊天发送侧已自动屏蔽违规词，后台保留上下文复核。',
        matchedKeywords: moderation.matchedKeywords,
        autoAction: 'mask_and_review',
        reason: `聊天命中违规词：${moderation.matchedKeywords.join(' / ')}`,
        messages: [
          {
            id: `risk_turn_${Date.now()}`,
            senderName: mockState.user.nickname,
            body: moderation.maskedText,
            createdAt: nowIso(),
            fromMe: true
          }
        ],
        disciplineStatus: 'violation',
        disciplineSummary: `命中聊天安全关键词：${moderation.matchedKeywords.join('、')}。`,
        updatedAt: nowIso()
      })
    }
    return delay({ ok: true })
  },

  async followUser(userId: string) {
    mockState.followingUserIds.add(userId)
    mockState.bottles.forEach((bottle) => {
      if (bottle.authorId === userId) bottle.isFollowing = true
    })
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '关注成功',
      body: '你可以在后续版本的关注列表里继续看到对方动态。',
      createdAt: nowIso(),
      unread: true
    })
    return delay({ ok: true })
  },

  async requestFriend(userId: string) {
    mockState.friendRequestedUserIds.add(userId)
    mockState.bottles.forEach((bottle) => {
      if (bottle.authorId === userId) bottle.friendRequested = true
    })
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '好友申请已发送',
      body: '好友用于长期关系沉淀；明确互动上下文内仍可按规则继续聊。',
      createdAt: nowIso(),
      unread: true
    })
    return delay({ ok: true })
  },

  async reportBottle(bottleId: string, reason: string) {
    const bottle = mockState.bottles.find((item) => item.id === bottleId)
    const reportId = `report_${Date.now()}`
    mockState.adminReports.unshift({
      id: reportId,
      reporterName: mockState.user.nickname,
      targetType: 'bottle',
      targetId: bottleId,
      targetPreview: bottle?.content || '未知漂流瓶',
      reason,
      status: 'pending',
      priority: reason.includes('骚扰') || reason.includes('违规') ? 'high' : 'normal',
      createdAt: nowIso(),
      evidenceRefs: [`report:${reportId}`, `bottle:${bottleId}`, `reporter:${mockState.user.id}`],
      auditRefs: []
    })
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '举报已提交',
      body: '内容已进入审核队列，审核员会结合上下文处理。',
      createdAt: nowIso(),
      unread: true
    })
    return delay({ ok: true })
  },

  async resolveAdminReport(reportId: string, reason: string, penaltyAction: 'none' | 'limit_user' | 'freeze_chat' = 'none') {
    const report = mockState.adminReports.find((item) => item.id === reportId)
    if (!report) throw new Error('REPORT_NOT_FOUND')
    const beforeStatus = report.status
    const auditId = `audit_${Date.now()}`
    const penaltyAuditId = penaltyAction !== 'none' ? `audit_penalty_${Date.now()}` : undefined
    report.status = 'resolved'
    report.auditRefs = penaltyAuditId ? [...report.auditRefs, penaltyAuditId, auditId] : [...report.auditRefs, auditId]
    if (penaltyAction === 'limit_user') {
      const targetUser = mockState.adminUsers.find((item) => item.nickname === report.targetDisplayName)
      if (targetUser) targetUser.status = 'limited'
      mockState.auditLogs.unshift({
        id: penaltyAuditId || `audit_penalty_${Date.now()}`,
        operator: '系统管理员',
        action: '举报限制用户',
        target: targetUser?.id || report.targetId,
        detail: `report=${reportId};reason=${reason}`,
        createdAt: nowIso()
      })
    } else if (penaltyAction === 'freeze_chat') {
      mockState.auditLogs.unshift({
        id: penaltyAuditId || `audit_penalty_${Date.now()}`,
        operator: '系统管理员',
        action: '举报冻结聊天',
        target: report.targetId,
        detail: `report=${reportId};after_status=risk_frozen;reason=${reason}`,
        createdAt: nowIso()
      })
    }
    mockState.auditLogs.unshift({
      id: auditId,
      operator: '系统管理员',
      action: '举报处置',
      target: reportId,
      detail: `before=${beforeStatus};after=resolved;reason=${reason};penalty_action=${penaltyAction}`,
      createdAt: nowIso()
    })
    return delay({
      reportId,
      beforeStatus,
      afterStatus: 'resolved' as const,
      reason,
      auditId,
      resolvedAt: nowIso(),
      penaltyAction,
      penaltyTargetUserId: undefined,
      penaltyTargetThreadId: penaltyAction === 'freeze_chat' ? report.targetId : undefined,
      penaltyAuditId
    })
  },

  async blockUser(userId: string, reason: string) {
    const bottle = mockState.bottles.find((item) => item.authorId === userId)
    const exists = mockState.blacklist.some((item) => item.userId === userId)
    if (!exists) {
      mockState.blacklist.unshift({
        id: `block_${Date.now()}`,
        userId,
        nickname: bottle?.authorName || '未知用户',
        reason,
        blockedAt: nowIso()
      })
    }
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '已加入黑名单',
      body: `${bottle?.authorName || '该用户'}后续不会再出现在你的漂流瓶推荐里。`,
      createdAt: nowIso(),
      unread: true
    })
    return delay({ ok: true })
  },

  async drawTruthQuestion(): Promise<TruthQuestion> {
    consumeQuota('truth')
    return delay({ ...randomPick(mockState.truthQuestions) })
  },

  async drawDareTask(): Promise<DareTask> {
    consumeQuota('dare')
    return delay({ ...randomPick(mockState.dareTasks) })
  },

  async listTreeholeFeed(): Promise<TreeholePost[]> {
    return delay(mockState.treeholes.map((item) => ({ ...item })))
  },

  async publishTreehole(content: string): Promise<TreeholePost> {
    consumeQuota('treehole_post')
    const moderation = moderateText(content)
    const post: TreeholePost = {
      id: `tree_${Date.now()}`,
      authorId: mockState.user.id,
      authorName: mockState.user.nickname,
      authorAvatarText: mockState.user.avatarText,
      authorAvatarUrl: mockState.user.avatarUrl,
      authorGender: mockState.user.gender || 'unknown',
      authorAgeRange: mockState.user.ageRange || '未知',
      content: moderation.maskedText,
      resonanceCount: 0,
      replyCount: 0,
      paidPhotoCount: 0,
      status: moderation.shouldReview ? 'pending' : 'approved',
      createdAt: nowIso()
    }
    mockState.treeholes.unshift(post)
    if (moderation.shouldReview) {
      mockState.contentReviews.unshift({
        id: `review_${post.id}`,
        type: 'treehole',
        category: 'treehole',
        authorId: mockState.user.id,
        authorName: mockState.user.nickname,
        preview: moderation.maskedText,
        status: 'pending',
        riskLevel: 'high',
        reviewTrigger: 'keyword',
        handlingPolicy: '发送侧已自动屏蔽违规词，后台保留审核记录。',
        matchedKeywords: moderation.matchedKeywords,
        autoAction: 'mask_and_review',
        reason: `命中违规词：${moderation.matchedKeywords.join(' / ')}`,
        createdAt: nowIso()
      })
    }
    return delay({ ...post })
  },

  async resonateTreehole(id: string) {
    const post = mockState.treeholes.find((item) => item.id === id)
    if (post) {
      post.resonanceCount += 1
    }
    return delay({ ok: true })
  },

  async replyTreehole(id: string, content: string) {
    const trimmedContent = content.trim()
    if (!trimmedContent) {
      throw new Error('EMPTY_TREEHOLE_REPLY')
    }
    const post = mockState.treeholes.find((item) => item.id === id)
    if (post) {
      post.replyCount += 1
    }
    return delay({ ok: true })
  },

  async listMessages(): Promise<MessageItem[]> {
    return delay(mockState.messages.map((item) => ({ ...item })))
  },

  async listConversationThreads(): Promise<ConversationThread[]> {
    return delay(
      mockState.conversationThreads.map((thread) => ({
        ...thread,
        turns: thread.turns.map((turn) => ({ ...turn }))
      }))
    )
  },

  async getWallet() {
    return delay({
      wallet: { ...mockState.wallet },
      ledger: mockState.ledger.map((item) => ({ ...item })),
      gifts: mockState.gifts.map((item) => ({ ...item }))
    })
  },

  async getVerification() {
    return delay({
      verification: { ...mockState.verification },
      referral: { ...mockState.referral }
    })
  },

  async listCreators() {
    return delay(mockState.creators.map((item) => ({ ...item })))
  },

  async listPrivatePhotos(ownerId?: string) {
    const photos = ownerId ? mockState.privatePhotos.filter((photo) => photo.ownerId === ownerId) : mockState.privatePhotos
    return delay(photos.map((item) => ({ ...item })))
  },

  async listPlazaPosts() {
    return delay(mockState.plazaPosts.map((item) => ({ ...item })))
  },

  async publishPlazaPost(content: string, options: { mediaType?: 'text' | 'image' | 'voice' | 'video'; mediaCount?: number } = {}) {
    const trimmedContent = content.trim()
    if (!trimmedContent) {
      throw new Error('EMPTY_PLAZA_CONTENT')
    }
    const post = {
      id: `plaza_${Date.now()}`,
      authorId: mockState.user.id,
      authorName: mockState.user.nickname,
      iconText: mockState.user.avatarText,
      topic: '今日动态',
      content: trimmedContent,
      mediaType: options.mediaType || 'text',
      mediaCount: options.mediaCount || 0,
      gender: mockState.user.gender,
      verified: Boolean(mockState.user.faceVerified && mockState.user.genderVerified),
      city: mockState.user.city || '杭州',
      ageRange: '25-30',
      viewCount: 0,
      likeCount: 0,
      commentCount: 0,
      commentPreview: '',
      distanceText: '刚刚',
      createdAt: nowIso()
    }
    mockState.plazaPosts.unshift(post)
    return delay({ ...post })
  },

  async commentPlazaPost(postId: string, content: string) {
    const trimmedContent = content.trim()
    if (!trimmedContent) {
      throw new Error('EMPTY_PLAZA_COMMENT')
    }
    const post = mockState.plazaPosts.find((item) => item.id === postId)
    if (!post) {
      throw new Error('PLAZA_POST_NOT_FOUND')
    }
    post.commentCount += 1
    post.commentPreview = trimmedContent
    return delay({ ...post })
  },

  async likePlazaPost(postId: string) {
    const post = mockState.plazaPosts.find((item) => item.id === postId)
    if (!post) {
      throw new Error('PLAZA_POST_NOT_FOUND')
    }
    post.likeCount += 1
    return delay({ ...post })
  },

  async listNearbyUsers() {
    return delay(mockState.nearbyUsers.map((item) => ({ ...item })))
  },

  async listBlacklist() {
    return delay(mockState.blacklist.map((item) => ({ ...item })))
  },

  async submitFaceVerification() {
    mockState.verification.livenessPassed = true
    mockState.verification.faceVerified = true
    mockState.verification.genderVerified = true
    mockState.verification.detectedGender = 'female'
    mockState.verification.manualReviewStatus = 'pending'
    return delay({ ...mockState.verification })
  },

  async claimReferralVip() {
    if (mockState.referral.invitedCount < mockState.referral.nextRewardNeed) {
      throw new Error('REFERRAL_NOT_ENOUGH')
    }
    mockState.user.isVip = true
    mockState.user.vipLevel = 'monthly'
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '拉新会员奖励到账',
      body: `已获得 ${mockState.referral.rewardVipDays} 天会员体验。`,
      createdAt: nowIso(),
      unread: true
    })
    return delay({ user: { ...mockState.user }, referral: { ...mockState.referral } })
  },

  async unlockPrivatePhoto(photoId: string) {
    const photo = mockState.privatePhotos.find((item) => item.id === photoId)
    if (!photo) throw new Error('PHOTO_NOT_FOUND')
    if (photo.purchased) return delay({ photo: { ...photo }, wallet: { ...mockState.wallet } })
    if (mockState.wallet.rechargeCoins < photo.priceCoins) throw new Error('COIN_NOT_ENOUGH')
    mockState.wallet.rechargeCoins -= photo.priceCoins
    photo.purchased = true
    photo.blurred = false
    mockState.ledger.unshift({
      id: `ledger_${Date.now()}`,
      title: `查看 ${photo.ownerName} 的私密照片`,
      amount: -photo.priceCoins,
      coinBucket: 'recharge',
      withdrawable: false,
      createdAt: nowIso()
    })
    mockState.ledger.unshift({
      id: `ledger_income_${Date.now()}`,
      title: `${photo.ownerName} 获得照片查看收益`,
      amount: photo.priceCoins,
      coinBucket: 'earned',
      withdrawable: true,
      createdAt: nowIso()
    })
    return delay({ photo: { ...photo }, wallet: { ...mockState.wallet } })
  },

  async sendGift(giftId: string, receiverId: string) {
    const gift = mockState.gifts.find((item) => item.id === giftId)
    if (!gift) throw new Error('GIFT_NOT_FOUND')
    if (mockState.wallet.rechargeCoins < gift.priceCoins) throw new Error('COIN_NOT_ENOUGH')
    mockState.wallet.rechargeCoins -= gift.priceCoins
    mockState.ledger.unshift({
      id: `ledger_${Date.now()}`,
      title: `送出礼物：${gift.name}`,
      amount: -gift.priceCoins,
      coinBucket: 'recharge',
      withdrawable: false,
      createdAt: nowIso()
    })
    mockState.messages.unshift({
      id: `msg_${Date.now()}`,
      title: '礼物已送达',
      body: `礼物已送给 ${receiverId}，对方收到的是可提现收益币。`,
      createdAt: nowIso(),
      unread: true
    })
    return delay({ ok: true, wallet: { ...mockState.wallet } })
  },

  async requestWithdraw(amount: number) {
    const requiredCharm = amount * mockState.wallet.charmExchangeRate
    if (requiredCharm > mockState.wallet.charmValue) throw new Error('CHARM_LIMIT')
    if (mockState.wallet.charmValue < mockState.wallet.withdrawThresholdCharm) throw new Error('CHARM_THRESHOLD')
    mockState.wallet.withdrawableCoins -= amount
    mockState.wallet.charmValue -= requiredCharm
    mockState.wallet.frozenCoins += amount
    mockState.ledger.unshift({
      id: `ledger_${Date.now()}`,
      title: '魅力值提现申请',
      amount: -amount,
      coinBucket: 'earned',
      withdrawable: true,
      createdAt: nowIso()
    })
    return delay({ wallet: { ...mockState.wallet } })
  },

  async saveAdminRewardConfig(config: AdminRewardConfigDraft): Promise<AdminDashboard> {
    Object.entries(config.baseQuotas).forEach(([type, base]) => {
      const quota = mockState.quotas[type as QuotaType]
      if (quota) {
        quota.base = Number(base)
      }
    })
    mockState.adReward.cooldownMinutes = Number(config.adCooldownMinutes)
    mockState.adReward.rewardPerQuota = Number(config.adRewardPerQuota)
    mockState.adReward.displayType = config.adDisplayType
    mockState.adReward.provider = config.adProvider
    mockState.adReward.placementId = config.adPlacementId
    mockState.adReward.title = config.adTitle
    mockState.adReward.description = config.adDescription
    mockState.adReward.mediaUrl = config.adMediaUrl
    mockState.adReward.clickUrl = config.adClickUrl
    mockState.adReward.countdownSeconds = Number(config.adCountdownSeconds)
    mockState.adReward.miniProgramAppId = config.miniProgramAppId
    mockState.adReward.miniProgramPath = config.miniProgramPath
    mockState.checkin.weekRewards = config.checkinRewards.map((item) => Number(item))
    createAuditLog('保存奖励配置', 'reward_config', '更新玩法基础次数、广告奖励与签到奖励')
    return delay(getAdminDashboardSnapshot())
  },

  async batchReviewContent(ids: string[], status: ContentStatus): Promise<AdminDashboard> {
    mockState.contentReviews.forEach((item) => {
      if (ids.includes(item.id)) {
        item.status = status
      }
    })
    createAuditLog('批量审核内容', ids.join(','), `状态更新为 ${status}`)
    return delay(getAdminDashboardSnapshot())
  },

  async batchOfflineContent(ids: string[]): Promise<AdminDashboard> {
    mockState.contentReviews.forEach((item) => {
      if (ids.includes(item.id)) {
        item.status = 'rejected'
        item.reason = `${item.reason} / 管理员批量下架`
      }
    })
    createAuditLog('批量下架内容', ids.join(','), '内容状态更新为 rejected')
    return delay(getAdminDashboardSnapshot())
  },

  async listAdminData(): Promise<AdminDashboard> {
    return delay({
      adminSession: cloneAdminSession(),
      summary: getAdminSummary(),
      rewardConfig: {
        baseQuotas: Object.fromEntries(Object.entries(mockState.quotas).map(([type, quota]) => [type, quota.base])) as Record<
          QuotaType,
          number
        >,
        adCooldownMinutes: mockState.adReward.cooldownMinutes,
        adRewardPerQuota: mockState.adReward.rewardPerQuota,
        adReward: `所有玩法次数各 +${mockState.adReward.rewardPerQuota}`,
        checkinRewards: mockState.checkin.weekRewards,
        adDisplayType: mockState.adReward.displayType,
        adProvider: mockState.adReward.provider,
        adPlacementId: mockState.adReward.placementId,
        adTitle: mockState.adReward.title,
        adDescription: mockState.adReward.description,
        adMediaUrl: mockState.adReward.mediaUrl,
        adClickUrl: mockState.adReward.clickUrl,
        adCountdownSeconds: mockState.adReward.countdownSeconds,
        miniProgramAppId: mockState.adReward.miniProgramAppId,
        miniProgramPath: mockState.adReward.miniProgramPath,
        quotaNames: quotaFullLabels
      },
      users: mockState.adminUsers.map((item) => ({ ...item })),
      contentReviews: mockState.contentReviews.map((item) => ({ ...item })),
      chatReviews: mockState.chatReviews.map((item) => ({
        ...item,
        participants: [...item.participants],
        messages: item.messages.map((message) => ({ ...message }))
      })),
      ...adminReviewExtras(),
      reports: mockState.adminReports.map((item) => ({ ...item })),
      adRewardRecords: mockState.adRewardRecords.map((item) => ({
        ...item,
        quotaTypes: [...item.quotaTypes]
      })),
      orders: mockState.orderRecords.map((item) => ({ ...item })),
      walletRisks: mockState.walletRiskItems.map((item) => ({ ...item })),
      auditLogs: mockState.auditLogs.map((item) => ({ ...item })),
      recentReports: [
        { id: 'report_001', target: '树洞内容', reason: '疑似骚扰', status: '待处理' },
        { id: 'report_002', target: '漂流瓶回复', reason: '低俗内容', status: '复核中' }
      ]
    })
  }
}
