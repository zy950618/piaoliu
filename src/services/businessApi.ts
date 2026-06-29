import type {
  BlacklistItem,
  Bottle,
  BottleTargetGender,
  BottleTargetScope,
  CheckinState,
  CoinLedgerItem,
  ConversationThread,
  ConversationTurn,
  CreatorProfile,
  DareTask,
  GiftProduct,
  MembershipProduct,
  MessageItem,
  NearbyUser,
  PrivatePhoto,
  ReferralState,
  TreeholePost,
  TruthQuestion,
  UserActivityRecord,
  UserRecordSummaryItem,
  UserProfile,
  VerificationState,
  WalletState
} from '@/types/domain'
import { requestJson } from '@/services/http'

export interface BottleFilterOptions {
  city?: string
  gender?: string
  ageRange?: string
}

type BottleDto = {
  id: string
  author_id: string
  author_name: string
  author_avatar_text?: string
  author_avatar_url?: string
  author_vip?: boolean
  author_gender?: Bottle['authorGender']
  author_age_range?: string
  author_city?: string
  author_verified?: boolean
  content: string
  mood: string
  status: Bottle['status']
  replies: number
  target_gender?: BottleTargetGender
  target_scope?: BottleTargetScope
  is_following?: boolean
  friend_requested?: boolean
  created_at: string
}

type TreeholePostDto = {
  id: string
  author_id: string
  author_name?: string
  author_avatar_text?: string
  author_avatar_url?: string
  author_gender?: TreeholePost['authorGender']
  author_age_range?: string
  content: string
  resonance_count: number
  reply_count: number
  paid_photo_count?: number
  status: TreeholePost['status']
  created_at: string
}

type MessageDto = {
  id: string
  title: string
  body: string
  created_at: string
  unread: boolean
  business_type?: string | null
  business_id?: string | null
}

type ConversationTurnDto = {
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

type ConversationThreadDto = {
  id: string
  bottle_id?: string
  participant_user_id: string
  participant_name: string
  participant_avatar_text?: string
  participant_avatar_url?: string
  participant_tag: string
  bottle_preview?: string
  last_message?: string
  updated_at: string
  unread_count: number
  turns: ConversationTurnDto[]
}

type WalletDto = {
  recharge_coins: number
  earned_coins: number
  gift_coins: number
  withdrawable_coins: number
  frozen_coins: number
  charm_value: number
  withdraw_threshold_charm: number
  charm_exchange_rate: number
}

type LedgerDto = {
  id: string
  title: string
  amount: number
  coin_bucket: CoinLedgerItem['coinBucket']
  withdrawable: boolean
  created_at: string
}

type GiftDto = {
  id: string
  name: string
  price_coins: number
  icon_text: string
  category?: string
}

type VerificationDto = {
  face_verified: boolean
  gender_verified: boolean
  detected_gender: VerificationState['detectedGender']
  liveness_passed: boolean
  manual_review_status: VerificationState['manualReviewStatus']
}

type ReferralDto = {
  invite_code: string
  invited_count: number
  reward_vip_days: number
  next_reward_need: number
}

type CreatorDto = {
  user_id: string
  display_name: string
  gender: CreatorProfile['gender']
  verified: boolean
  safety_score: number
  follower_count: number
  album_count: number
  earned_coins: number
  charm_value: number
}

type PrivatePhotoDto = {
  id: string
  owner_id: string
  owner_name: string
  title: string
  cover_tone?: string
  price_coins: number
  blurred?: boolean
  status: PrivatePhoto['status']
  purchased: boolean
}

type NearbyUserDto = {
  id: string
  nickname: string
  icon_text: string
  gender: NearbyUser['gender']
  verified: boolean
  age_range?: string
  distance_km?: number
  distance_text: string
  signature: string
  is_vip: boolean
  online: boolean
}

type BlacklistDto = {
  id: string
  user_id: string
  nickname: string
  reason: string
  blocked_at: string
}

type UserRecordSummaryDto = {
  type: UserRecordSummaryItem['type']
  title: string
  desc: string
  count: number
}

type UserActivityRecordDto = {
  id: string
  record_type: UserActivityRecord['recordType']
  title: string
  content: string
  visibility?: string
  source_type?: string
  source_id?: string
  created_at: string
}

type GamePromptDto = {
  id: string
  mode: 'truth_public' | 'truth_private' | 'dare_public' | 'dare_private'
  text: string
  meaning: string
  visibility: string
}

type MembershipProductDto = {
  id: string
  name: string
  price_label: string
  platform: MembershipProduct['platform']
  benefits: string[]
}

type UserProfileDto = {
  id: string
  nickname: string
  avatar_text: string
  avatar_url?: string
  platform: UserProfile['platform']
  is_vip: boolean
  vip_level: UserProfile['vipLevel']
  vip_expires_at?: string
  drift_coins: number
  gender?: UserProfile['gender']
  age_range?: string
  city?: string
  face_verified?: boolean
  gender_verified?: boolean
  charm_value?: number
}

type MembershipOrderDto = {
  id: string
  platform: 'wechat' | 'ios' | 'android'
  product_id: string
  transaction_id: string
  status: 'mock_verified' | 'duplicate_verified'
  vip_level: 'monthly' | 'season' | 'yearly'
  verified_at: string
}

type MembershipOrderVerifyDto = {
  order: MembershipOrderDto
  user: UserProfileDto
}

export type MembershipPaymentPlatform = MembershipOrderDto['platform']

function toBottle(dto: BottleDto): Bottle {
  return {
    id: dto.id,
    authorId: dto.author_id,
    authorName: dto.author_name,
    authorAvatarText: dto.author_avatar_text,
    authorAvatarUrl: dto.author_avatar_url,
    authorVip: dto.author_vip,
    authorGender: dto.author_gender,
    authorAgeRange: dto.author_age_range,
    authorCity: dto.author_city,
    authorVerified: dto.author_verified,
    content: dto.content,
    mood: dto.mood,
    status: dto.status,
    replies: dto.replies,
    targetGender: dto.target_gender,
    targetScope: dto.target_scope,
    isFollowing: dto.is_following,
    friendRequested: dto.friend_requested,
    createdAt: dto.created_at
  }
}

function toTreeholePost(dto: TreeholePostDto): TreeholePost {
  return {
    id: dto.id,
    authorId: dto.author_id,
    authorName: dto.author_name || '匿名树洞',
    authorAvatarText: dto.author_avatar_text || '匿',
    authorAvatarUrl: dto.author_avatar_url,
    authorGender: dto.author_gender || 'unknown',
    authorAgeRange: dto.author_age_range || '未知',
    content: dto.content,
    resonanceCount: dto.resonance_count,
    replyCount: dto.reply_count,
    paidPhotoCount: dto.paid_photo_count,
    status: dto.status,
    createdAt: dto.created_at
  }
}

function toTurn(dto: ConversationTurnDto): ConversationTurn {
  return {
    id: dto.id,
    senderName: dto.sender_name,
    body: dto.body,
    createdAt: dto.created_at,
    fromMe: dto.from_me,
    type: dto.type,
    mediaUrl: dto.media_url,
    mediaDuration: dto.media_duration,
    flashViewed: dto.flash_viewed,
    giftId: dto.gift_id,
    giftName: dto.gift_name,
    giftIconText: dto.gift_icon_text,
    giftPriceCoins: dto.gift_price_coins,
    gameRoomId: dto.game_room_id,
    gameRoomMode: dto.game_room_mode
  }
}

function toThread(dto: ConversationThreadDto): ConversationThread {
  return {
    id: dto.id,
    bottleId: dto.bottle_id || '',
    participantUserId: dto.participant_user_id,
    participantName: dto.participant_name,
    participantAvatarText: dto.participant_avatar_text,
    participantAvatarUrl: dto.participant_avatar_url,
    participantTag: dto.participant_tag,
    bottlePreview: dto.bottle_preview || '',
    lastMessage: dto.last_message || '',
    updatedAt: dto.updated_at,
    unreadCount: dto.unread_count,
    turns: dto.turns.map(toTurn)
  }
}

function toWallet(dto: WalletDto): WalletState {
  return {
    rechargeCoins: dto.recharge_coins,
    earnedCoins: dto.earned_coins,
    giftCoins: dto.gift_coins,
    withdrawableCoins: dto.withdrawable_coins,
    frozenCoins: dto.frozen_coins,
    charmValue: dto.charm_value,
    withdrawThresholdCharm: dto.withdraw_threshold_charm,
    charmExchangeRate: dto.charm_exchange_rate
  }
}

function toVerification(dto: VerificationDto): VerificationState {
  return {
    faceVerified: dto.face_verified,
    genderVerified: dto.gender_verified,
    detectedGender: dto.detected_gender,
    livenessPassed: dto.liveness_passed,
    manualReviewStatus: dto.manual_review_status
  }
}

function toUserProfile(dto: UserProfileDto): UserProfile {
  return {
    id: dto.id,
    nickname: dto.nickname,
    avatarText: dto.avatar_text,
    avatarUrl: dto.avatar_url,
    platform: dto.platform,
    isVip: dto.is_vip,
    vipLevel: dto.vip_level,
    vipExpiresAt: dto.vip_expires_at,
    driftCoins: dto.drift_coins,
    gender: dto.gender,
    ageRange: dto.age_range,
    city: dto.city,
    faceVerified: dto.face_verified,
    genderVerified: dto.gender_verified,
    charmValue: dto.charm_value
  }
}

function toReferral(dto: ReferralDto): ReferralState {
  return {
    inviteCode: dto.invite_code,
    invitedCount: dto.invited_count,
    rewardVipDays: dto.reward_vip_days,
    nextRewardNeed: dto.next_reward_need
  }
}

export const businessApi = {
  async throwBottle(content: string, options: { targetGender?: BottleTargetGender; targetScope?: BottleTargetScope } = {}) {
    return toBottle(await requestJson<BottleDto>('/bottles', {
      method: 'POST',
      body: JSON.stringify({
        content,
        target_gender: options.targetGender || 'all',
        target_scope: options.targetScope || 'all'
      })
    }))
  },

  async getRandomBottlePrompt() {
    const result = await requestJson<{ content: string }>('/bottles/prompts/random')
    return result.content
  },

  async fishBottle(filters: BottleFilterOptions = {}) {
    const params = new URLSearchParams()
    if (filters.city) params.set('city', filters.city)
    if (filters.gender) params.set('gender', filters.gender)
    if (filters.ageRange) params.set('age_range', filters.ageRange)
    const query = params.toString()
    return toBottle(await requestJson<BottleDto>(`/bottles/random${query ? `?${query}` : ''}`))
  },

  async replyBottle(id: string, content: string) {
    return requestJson<{ status: string }>(`/bottles/${id}/reply`, {
      method: 'POST',
      body: JSON.stringify({ content })
    })
  },

  async followUser(userId: string) {
    return requestJson<{ status: string }>(`/relations/follow`, {
      method: 'POST',
      body: JSON.stringify({ target_user_id: userId })
    })
  },

  async requestFriend(userId: string) {
    return requestJson<{ status: string }>(`/relations/friend-request`, {
      method: 'POST',
      body: JSON.stringify({ target_user_id: userId })
    })
  },

  async reportBottle(id: string, reason: string) {
    return requestJson<{ id: string }>(`/reports`, {
      method: 'POST',
      body: JSON.stringify({ target_type: 'bottle', target_id: id, reason })
    })
  },

  async blockUser(userId: string) {
    return requestJson<{ id: string }>(`/blocks`, {
      method: 'POST',
      body: JSON.stringify({ blocked_user_id: userId })
    })
  },

  async drawTruthQuestion() {
    return requestJson<TruthQuestion>('/truth/question/random')
  },

  async drawDareTask() {
    return requestJson<DareTask>('/dare/task/random')
  },

  async listTreeholeFeed() {
    const rows = await requestJson<TreeholePostDto[]>('/treehole/feed')
    return rows.map(toTreeholePost)
  },

  async publishTreehole(content: string) {
    return toTreeholePost(await requestJson<TreeholePostDto>('/treehole/posts', {
      method: 'POST',
      body: JSON.stringify({ content })
    }))
  },

  async resonateTreehole(id: string) {
    return requestJson<{ status: string; post: TreeholePostDto }>(`/treehole/${id}/react`, { method: 'POST' })
  },

  async replyTreehole(id: string, content: string) {
    return requestJson<{ status: string; post: TreeholePostDto }>(`/treehole/${id}/reply`, {
      method: 'POST',
      body: JSON.stringify({ content })
    })
  },

  async listMessages(): Promise<MessageItem[]> {
    const rows = await requestJson<MessageDto[]>('/messages')
    return rows.map((item) => ({
      id: item.id,
      title: item.title,
      body: item.body,
      createdAt: item.created_at,
      unread: item.unread,
      businessType: item.business_type,
      businessId: item.business_id
    }))
  },

  async markMessagesRead() {
    return requestJson<{ status: string }>('/messages/read-all', { method: 'POST' })
  },

  async listConversationThreads() {
    const rows = await requestJson<ConversationThreadDto[]>('/conversations')
    return rows.map(toThread)
  },

  async sendConversationTurn(threadId: string, payload: Pick<ConversationTurn, 'body' | 'type' | 'mediaUrl' | 'mediaDuration'>) {
    return toThread(await requestJson<ConversationThreadDto>(`/conversations/${threadId}/turns`, {
      method: 'POST',
      body: JSON.stringify({
        body: payload.body,
        type: payload.type || 'text',
        media_url: payload.mediaUrl,
        media_duration: payload.mediaDuration
      })
    }))
  },

  async viewConversationTurn(threadId: string, turnId: string) {
    return toThread(await requestJson<ConversationThreadDto>(`/conversations/${threadId}/turns/${turnId}/view`, { method: 'POST' }))
  },

  async createGameRoom(threadId: string, mode: 'truth' | 'dare' | 'mixed') {
    const result = await requestJson<{ room_id: string; thread: ConversationThreadDto }>(`/conversations/${threadId}/rooms`, {
      method: 'POST',
      body: JSON.stringify({ mode })
    })
    return { roomId: result.room_id, thread: toThread(result.thread) }
  },

  async getWallet() {
    const result = await requestJson<{ wallet: WalletDto; ledger: LedgerDto[]; gifts: GiftDto[] }>('/wallet')
    return {
      wallet: toWallet(result.wallet),
      ledger: result.ledger.map((item) => ({
        id: item.id,
        title: item.title,
        amount: item.amount,
        coinBucket: item.coin_bucket,
        withdrawable: item.withdrawable,
        createdAt: item.created_at
      })),
      gifts: result.gifts.map((item) => ({ id: item.id, name: item.name, priceCoins: item.price_coins, iconText: item.icon_text, category: item.category }))
    }
  },

  async rechargeCoins(amount: number) {
    const result = await requestJson<{ order_id: string; wallet: WalletDto }>('/wallet/recharge', {
      method: 'POST',
      body: JSON.stringify({ amount, channel: 'mock' })
    })
    return { orderId: result.order_id, wallet: toWallet(result.wallet) }
  },

  async getVerification() {
    const result = await requestJson<{ verification: VerificationDto; referral: ReferralDto }>('/verification')
    return { verification: toVerification(result.verification), referral: toReferral(result.referral) }
  },

  async submitFaceVerification() {
    return toVerification(await requestJson<VerificationDto>('/verification/face', { method: 'POST' }))
  },

  async claimReferralVip() {
    const result = await requestJson<{ status: 'claimed' | 'not_enough'; referral: ReferralDto }>('/referrals/claim-vip', { method: 'POST' })
    return { status: result.status, referral: toReferral(result.referral) }
  },

  async listCreators() {
    const rows = await requestJson<CreatorDto[]>('/creators')
    return rows.map((item) => ({
      userId: item.user_id,
      displayName: item.display_name,
      gender: item.gender,
      verified: item.verified,
      safetyScore: item.safety_score,
      followerCount: item.follower_count,
      albumCount: item.album_count,
      earnedCoins: item.earned_coins,
      charmValue: item.charm_value
    }))
  },

  async listPrivatePhotos() {
    const rows = await requestJson<PrivatePhotoDto[]>('/private-photos')
    return rows.map((item) => ({
      id: item.id,
      ownerId: item.owner_id,
      ownerName: item.owner_name,
      title: item.title,
      coverTone: item.cover_tone || 'mint',
      priceCoins: item.price_coins,
      blurred: item.blurred ?? !item.purchased,
      status: item.status,
      purchased: item.purchased
    }))
  },

  async unlockPrivatePhoto(photoId: string) {
    const result = await requestJson<{ photo: PrivatePhotoDto; wallet: WalletDto }>('/private-photos/unlock', {
      method: 'POST',
      body: JSON.stringify({ photo_id: photoId })
    })
    return {
      photo: {
        id: result.photo.id,
        ownerId: result.photo.owner_id,
        ownerName: result.photo.owner_name,
        title: result.photo.title,
        coverTone: result.photo.cover_tone || 'mint',
        priceCoins: result.photo.price_coins,
        blurred: result.photo.blurred ?? !result.photo.purchased,
        status: result.photo.status,
        purchased: result.photo.purchased
      },
      wallet: toWallet(result.wallet)
    }
  },

  async sendGift(giftId: string, receiverId: string) {
    const result = await requestJson<{ status: 'sent'; receiver_id: string; wallet: WalletDto }>('/gifts/send', {
      method: 'POST',
      body: JSON.stringify({ gift_id: giftId, receiver_id: receiverId })
    })
    return { status: result.status, receiverId: result.receiver_id, wallet: toWallet(result.wallet) }
  },

  async sendConversationGift(threadId: string, giftId: string) {
    const result = await requestJson<{ wallet: WalletDto; thread: ConversationThreadDto }>(`/conversations/${threadId}/gifts`, {
      method: 'POST',
      body: JSON.stringify({ gift_id: giftId })
    })
    return { wallet: toWallet(result.wallet), thread: toThread(result.thread) }
  },

  async requestWithdraw(amount: number) {
    const result = await requestJson<{ status: string; wallet: WalletDto }>('/wallet/withdraw', {
      method: 'POST',
      body: JSON.stringify({ amount })
    })
    return { status: result.status, wallet: toWallet(result.wallet) }
  },

  async listUserRecords() {
    const rows = await requestJson<UserRecordSummaryDto[]>('/me/records')
    return rows.map((item) => ({ type: item.type, title: item.title, desc: item.desc, count: item.count }))
  },

  async saveUserActivityRecord(payload: {
    recordType: UserActivityRecord['recordType']
    title: string
    content: string
    visibility?: string
    sourceType?: string
    sourceId?: string
  }) {
    const row = await requestJson<UserActivityRecordDto>('/me/records', {
      method: 'POST',
      body: JSON.stringify({
        record_type: payload.recordType,
        title: payload.title,
        content: payload.content,
        visibility: payload.visibility,
        source_type: payload.sourceType,
        source_id: payload.sourceId
      })
    })
    return {
      id: row.id,
      recordType: row.record_type,
      title: row.title,
      content: row.content,
      visibility: row.visibility,
      sourceType: row.source_type,
      sourceId: row.source_id,
      createdAt: row.created_at
    }
  },

  async getGamePrompt(mode: GamePromptDto['mode']) {
    const params = new URLSearchParams({ mode })
    const row = await requestJson<GamePromptDto>(`/game/prompts/random?${params.toString()}`)
    return {
      id: row.id,
      mode: row.mode,
      text: row.text,
      meaning: row.meaning,
      visibility: row.visibility
    }
  },

  async listMembershipProducts() {
    const rows = await requestJson<MembershipProductDto[]>('/membership/products')
    return rows.map((item) => ({
      id: item.id,
      name: item.name,
      priceLabel: item.price_label,
      platform: item.platform,
      benefits: item.benefits
    }))
  },

  async verifyMembershipOrder(payload: { platform: MembershipPaymentPlatform; productId: string; transactionId: string; receipt?: string }) {
    const result = await requestJson<MembershipOrderVerifyDto>('/membership/orders/verify', {
      method: 'POST',
      body: JSON.stringify({
        platform: payload.platform,
        product_id: payload.productId,
        transaction_id: payload.transactionId,
        receipt: payload.receipt || 'mock_receipt'
      })
    })
    return {
      order: {
        id: result.order.id,
        platform: result.order.platform,
        productId: result.order.product_id,
        transactionId: result.order.transaction_id,
        status: result.order.status,
        vipLevel: result.order.vip_level,
        verifiedAt: result.order.verified_at
      },
      user: toUserProfile(result.user)
    }
  },

  async listNearbyUsers(filters: BottleFilterOptions & { distanceKm?: number } = {}) {
    const params = new URLSearchParams()
    if (filters.gender) params.set('gender', filters.gender)
    if (filters.ageRange) params.set('age_range', filters.ageRange)
    if (filters.distanceKm) params.set('distance_km', String(filters.distanceKm))
    const query = params.toString()
    const rows = await requestJson<NearbyUserDto[]>(`/nearby/users${query ? `?${query}` : ''}`)
    return rows.map((item) => ({
      id: item.id,
      nickname: item.nickname,
      iconText: item.icon_text,
      gender: item.gender,
      verified: item.verified,
      ageRange: item.age_range,
      distanceKm: item.distance_km,
      distanceText: item.distance_text,
      signature: item.signature,
      isVip: item.is_vip,
      online: item.online
    }))
  },

  async listBlacklist() {
    const rows = await requestJson<BlacklistDto[]>('/blacklist')
    return rows.map((item) => ({ id: item.id, userId: item.user_id, nickname: item.nickname, reason: item.reason, blockedAt: item.blocked_at }))
  }
}
