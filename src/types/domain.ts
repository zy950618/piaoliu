export type QuotaType = 'fish_bottle' | 'throw_bottle' | 'truth' | 'dare' | 'treehole_post'

export type ContentStatus = 'pending' | 'approved' | 'rejected'
export type BottleTargetGender = 'all' | 'female' | 'male'
export type BottleTargetScope = 'all' | 'same_city' | 'nearby'

export interface UserProfile {
  id: string
  nickname: string
  avatarText: string
  avatarUrl?: string
  platform: 'wechat' | 'ios' | 'android' | 'h5'
  isVip: boolean
  vipLevel: 'none' | 'monthly' | 'season' | 'yearly'
  vipExpiresAt?: string
  driftCoins: number
  gender?: 'female' | 'male' | 'unknown'
  ageRange?: string
  city?: string
  faceVerified?: boolean
  genderVerified?: boolean
  charmValue?: number
}

export interface QuotaItem {
  type: QuotaType
  label: string
  base: number
  vipBonus: number
  adBonus: number
  used: number
  remaining: number
}

export interface AdRewardState {
  canWatch: boolean
  cooldownSeconds: number
  cooldownMinutes: number
  rewardPerQuota: number
  activeSessionId?: string
}

export interface CheckinState {
  checkedToday: boolean
  streakDays: number
  weekRewards: number[]
  currentWeekIndex: number
  lastReward?: number
}

export interface MeStatus {
  user: UserProfile
  quotas: Record<QuotaType, QuotaItem>
  adReward: AdRewardState
  checkin: CheckinState
}

export interface UserRecordSummaryItem {
  type: 'bottle' | 'treehole' | 'truth' | 'dare' | 'game' | 'report'
  title: string
  desc: string
  count: number
}

export interface UserActivityRecord {
  id: string
  recordType: 'truth' | 'dare' | 'game'
  title: string
  content: string
  visibility?: string
  sourceType?: string
  sourceId?: string
  createdAt: string
}

export interface MembershipProduct {
  id: string
  name: string
  priceLabel: string
  platform: 'wechat' | 'ios' | 'android' | 'all'
  benefits: string[]
}

export interface Bottle {
  id: string
  authorId: string
  authorName: string
  authorAvatarText?: string
  authorAvatarUrl?: string
  authorVip?: boolean
  authorGender?: 'female' | 'male' | 'unknown'
  authorAgeRange?: string
  authorCity?: string
  authorVerified?: boolean
  content: string
  mood: string
  status: ContentStatus
  replies: number
  targetGender?: BottleTargetGender
  targetScope?: BottleTargetScope
  isFollowing?: boolean
  friendRequested?: boolean
  createdAt: string
}

export interface TreeholePost {
  id: string
  authorId: string
  authorName: string
  authorAvatarText: string
  authorAvatarUrl?: string
  authorGender: 'female' | 'male' | 'unknown'
  authorAgeRange: string
  content: string
  resonanceCount: number
  replyCount: number
  paidPhotoCount?: number
  status: ContentStatus
  createdAt: string
}

export interface TruthQuestion {
  id: string
  category: string
  text: string
}

export interface DareTask {
  id: string
  category: string
  text: string
}

export interface MessageItem {
  id: string
  title: string
  body: string
  createdAt: string
  unread: boolean
  businessType?: string | null
  businessId?: string | null
}

export interface ConversationTurn {
  id: string
  senderName: string
  body: string
  createdAt: string
  fromMe: boolean
  type?: 'text' | 'image' | 'voice' | 'video' | 'flash_image' | 'flash_video' | 'gift' | 'game_room'
  mediaUrl?: string
  mediaDuration?: number
  flashViewed?: boolean
  giftId?: string
  giftName?: string
  giftIconText?: string
  giftPriceCoins?: number
  gameRoomId?: string
  gameRoomMode?: 'truth' | 'dare' | 'mixed'
}

export interface ConversationThread {
  id: string
  bottleId: string
  participantUserId: string
  participantName: string
  participantAvatarText?: string
  participantAvatarUrl?: string
  participantTag: string
  bottlePreview: string
  lastMessage: string
  updatedAt: string
  unreadCount: number
  turns: ConversationTurn[]
}

export interface AdminSummary {
  users: number
  activeUsers: number
  pendingContent: number
  reports: number
  adRewardsToday: number
  ordersToday: number
  pendingWithdrawals: number
  riskWallets: number
}

export interface AdminSession {
  accountId: string
  displayName: string
  role: 'super_admin' | 'content_admin' | 'risk_admin'
  permissions: string[]
  signedIn: boolean
  lastLoginAt: string
}

export interface AdminRewardConfig {
  baseQuotas: Record<QuotaType, number>
  adCooldownMinutes: number
  adRewardPerQuota: number
  adReward: string
  checkinRewards: number[]
  quotaNames: Record<QuotaType, string>
}

export interface AdminRewardConfigDraft {
  baseQuotas: Record<QuotaType, number>
  adCooldownMinutes: number
  adRewardPerQuota: number
  checkinRewards: number[]
}

export interface AdminUserSummary {
  id: string
  nickname: string
  avatarText?: string
  avatarUrl?: string
  status: 'active' | 'limited' | 'blocked'
  platform: UserProfile['platform']
  gender: NonNullable<UserProfile['gender']>
  isVip: boolean
  verificationStatus: VerificationState['manualReviewStatus']
  safetyScore: number
  walletRisk: 'normal' | 'watch' | 'blocked'
  driftCoins: number
  charmValue: number
  joinedAt: string
  lastActiveAt: string
  blockedUntil?: string | null
  blockReason?: string | null
}

export interface AdminContentReviewItem {
  id: string
  type: 'bottle' | 'treehole' | 'private_photo' | 'plaza'
  category: 'bottle' | 'treehole' | 'private_photo' | 'plaza'
  authorId: string
  authorName: string
  authorGender?: 'female' | 'male' | 'unknown'
  authorAvatarText?: string
  authorAvatarUrl?: string
  preview: string
  status: ContentStatus
  riskLevel: 'low' | 'medium' | 'high'
  reviewTrigger: 'report' | 'keyword' | 'risk' | 'private_photo' | 'system_sample' | 'new_user'
  handlingPolicy: string
  matchedKeywords?: string[]
  autoAction: 'auto_pass' | 'mask_and_review' | 'reject' | 'manual_review'
  reason: string
  createdAt: string
}

export interface AdminChatReviewItem {
  id: string
  threadId: string
  source: 'bottle' | 'treehole' | 'plaza' | 'game_room'
  reporterName?: string
  participantUserIds: string[]
  participants: string[]
  participantAvatarTexts?: Array<string | null>
  participantAvatarUrls?: Array<string | null>
  relatedContent: string
  lastMessage: string
  riskLevel: 'low' | 'medium' | 'high'
  status: 'pending' | 'reviewing' | 'resolved'
  reviewTrigger: 'report' | 'keyword' | 'risk'
  handlingPolicy: string
  matchedKeywords?: string[]
  autoAction: 'mask_and_review' | 'reject' | 'manual_review'
  reason: string
  messages: ConversationTurn[]
  disciplineStatus: 'clear' | 'watch' | 'violation'
  disciplineSummary: string
  roomMode?: 'truth' | 'dare' | 'mixed' | null
  updatedAt: string
}

export interface AdminReportItem {
  id: string
  reporterName: string
  targetType: 'user' | 'bottle' | 'treehole' | 'reply' | 'chat' | 'plaza' | 'private_photo'
  targetId: string
  targetPreview: string
  targetTypeText?: string
  targetDisplayName?: string
  targetAvatarText?: string
  targetAvatarUrl?: string
  reason: string
  status: 'pending' | 'reviewing' | 'resolved'
  priority: 'normal' | 'high'
  createdAt: string
}

export interface AdminAdRewardRecord {
  id: string
  userId: string
  nickname: string
  sessionId: string
  rewardPerQuota: number
  quotaTypes: QuotaType[]
  status: 'settled' | 'cooldown' | 'blocked'
  createdAt: string
}

export interface AdminOrderRecord {
  id: string
  userId: string
  nickname: string
  productName: string
  amountCoins: number
  payAmount: number
  channel: 'wechat' | 'apple' | 'android'
  status: 'paid' | 'refunding' | 'closed'
  createdAt: string
}

export interface AdminWalletRiskItem {
  id: string
  userId: string
  nickname: string
  type: 'withdraw' | 'freeze' | 'charm_review'
  amountCoins: number
  charmValue: number
  status: 'pending' | 'reviewing' | 'approved' | 'rejected'
  riskReason: string
  createdAt: string
}

export interface AdminAuditLogItem {
  id: string
  operator: string
  action: string
  target: string
  detail: string
  createdAt: string
}

export interface AdminDashboard {
  adminSession: AdminSession
  summary: AdminSummary
  rewardConfig: AdminRewardConfig
  users: AdminUserSummary[]
  contentReviews: AdminContentReviewItem[]
  chatReviews: AdminChatReviewItem[]
  reports: AdminReportItem[]
  adRewardRecords: AdminAdRewardRecord[]
  orders: AdminOrderRecord[]
  walletRisks: AdminWalletRiskItem[]
  auditLogs: AdminAuditLogItem[]
}

export interface WalletState {
  rechargeCoins: number
  earnedCoins: number
  giftCoins: number
  withdrawableCoins: number
  frozenCoins: number
  charmValue: number
  withdrawThresholdCharm: number
  charmExchangeRate: number
}

export interface CoinLedgerItem {
  id: string
  title: string
  amount: number
  coinBucket: 'recharge' | 'earned' | 'gift'
  withdrawable: boolean
  createdAt: string
}

export interface CreatorProfile {
  userId: string
  displayName: string
  gender: 'female' | 'male' | 'unknown'
  verified: boolean
  safetyScore: number
  followerCount: number
  albumCount: number
  earnedCoins: number
  charmValue: number
}

export interface PrivatePhoto {
  id: string
  ownerId: string
  ownerName: string
  title: string
  coverTone: string
  priceCoins: number
  blurred: boolean
  status: ContentStatus
  purchased: boolean
}

export interface GiftProduct {
  id: string
  name: string
  priceCoins: number
  iconText: string
  category?: string
}

export interface VerificationState {
  faceVerified: boolean
  genderVerified: boolean
  detectedGender: 'female' | 'male' | 'unknown'
  livenessPassed: boolean
  manualReviewStatus: 'not_submitted' | 'pending' | 'approved' | 'rejected'
}

export interface ReferralState {
  inviteCode: string
  invitedCount: number
  rewardVipDays: number
  nextRewardNeed: number
}

export interface BlacklistItem {
  id: string
  userId: string
  nickname: string
  reason: string
  blockedAt: string
}

export interface PlazaPost {
  id: string
  authorId: string
  authorName: string
  iconText: string
  iconUrl?: string
  topic: string
  content: string
  mediaType?: 'text' | 'image' | 'voice' | 'video'
  mediaCount?: number
  gender?: 'female' | 'male' | 'unknown'
  verified?: boolean
  city?: string
  ageRange?: string
  viewCount?: number
  likeCount: number
  likedByMe?: boolean
  commentCount: number
  commentPreview?: string
  media?: PlazaMedia[]
  distanceText?: string
  createdAt: string
}

export interface PlazaMedia {
  id: string
  postId: string
  ownerId: string
  mediaType: 'image' | 'voice' | 'video'
  url: string
  storageKey?: string
  mimeType: string
  sizeBytes?: number
  durationSeconds?: number
  width?: number
  height?: number
  createdAt: string
}

export interface PlazaComment {
  id: string
  postId: string
  authorId: string
  authorName: string
  iconText: string
  iconUrl?: string
  authorGender?: 'female' | 'male' | 'unknown'
  authorAgeRange?: string
  authorVerified?: boolean
  authorCity?: string
  content: string
  hiddenForOwnerOnly?: boolean
  visibleToOwnerOnly?: boolean
  createdAt: string
}

export interface NearbyUser {
  id: string
  nickname: string
  iconText: string
  gender: 'female' | 'male' | 'unknown'
  verified: boolean
  ageRange?: string
  distanceKm?: number
  distanceText: string
  signature: string
  isVip: boolean
  online: boolean
}
