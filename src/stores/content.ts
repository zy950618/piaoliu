import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  AdminDashboard,
  AdminRewardConfigDraft,
  AdminSession,
  Bottle,
  BottleTargetGender,
  BottleTargetScope,
  BlacklistItem,
  CoinLedgerItem,
  ConversationThread,
  ContentStatus,
  CreatorProfile,
  DareTask,
  GiftProduct,
  MessageItem,
  NearbyUser,
  PlazaComment,
  PlazaPost,
  PrivatePhoto,
  ReferralState,
  TreeholePost,
  TruthQuestion,
  VerificationState,
  WalletState
} from '@/types/domain'
import { mockApi } from '@/services/mockApi'
import { plazaApi } from '@/services/plazaApi'
import type { BottleFilterOptions } from '@/services/mockApi'
import { useAppStore } from './app'

interface ThrowBottleOptions {
  targetGender?: BottleTargetGender
  targetScope?: BottleTargetScope
}

export const useContentStore = defineStore('content', () => {
  const currentBottle = ref<Bottle>()
  const treeholeFeed = ref<TreeholePost[]>([])
  const currentTruth = ref<TruthQuestion>()
  const currentDare = ref<DareTask>()
  const messages = ref<MessageItem[]>([])
  const conversationThreads = ref<ConversationThread[]>([])
  const wallet = ref<WalletState>()
  const ledger = ref<CoinLedgerItem[]>([])
  const creators = ref<CreatorProfile[]>([])
  const privatePhotos = ref<PrivatePhoto[]>([])
  const gifts = ref<GiftProduct[]>([])
  const verification = ref<VerificationState>()
  const referral = ref<ReferralState>()
  const plazaPosts = ref<PlazaPost[]>([])
  const plazaComments = ref<Record<string, PlazaComment[]>>({})
  const nearbyUsers = ref<NearbyUser[]>([])
  const blacklist = ref<BlacklistItem[]>([])
  const adminDashboard = ref<AdminDashboard>()
  const adminSession = ref<AdminSession>()
  const submitting = ref(false)

  async function throwBottle(content: string, options: ThrowBottleOptions = {}) {
    submitting.value = true
    try {
      const bottle = await mockApi.throwBottle(content, options)
      await useAppStore().refreshStatus()
      currentBottle.value = bottle
      return bottle
    } finally {
      submitting.value = false
    }
  }

  async function getRandomBottlePrompt() {
    return mockApi.getRandomBottlePrompt()
  }

  async function fishBottle(filters: BottleFilterOptions = {}) {
    const bottle = await mockApi.fishBottle(filters)
    await useAppStore().refreshStatus()
    currentBottle.value = bottle
    return bottle
  }

  async function replyBottle(id: string, content: string) {
    await mockApi.replyBottle(id, content)
    await loadMessages()
    await loadConversationThreads()
  }

  async function followUser(userId: string) {
    await mockApi.followUser(userId)
    await loadMessages()
    if (currentBottle.value?.authorId === userId) currentBottle.value.isFollowing = true
  }

  async function requestFriend(userId: string) {
    await mockApi.requestFriend(userId)
    await loadMessages()
    if (currentBottle.value?.authorId === userId) currentBottle.value.friendRequested = true
  }

  async function reportBottle(id: string, reason: string) {
    await mockApi.reportBottle(id, reason)
    await loadMessages()
    if (adminDashboard.value) await loadAdminDashboard()
  }

  async function blockUser(userId: string, reason: string) {
    await mockApi.blockUser(userId, reason)
    await loadMessages()
    await loadBlacklist()
  }

  async function drawTruthQuestion() {
    const question = await mockApi.drawTruthQuestion()
    await useAppStore().refreshStatus()
    currentTruth.value = question
    return question
  }

  async function drawDareTask() {
    const task = await mockApi.drawDareTask()
    await useAppStore().refreshStatus()
    currentDare.value = task
    return task
  }

  async function loadTreeholeFeed() {
    treeholeFeed.value = await mockApi.listTreeholeFeed()
  }

  async function publishTreehole(content: string) {
    submitting.value = true
    try {
      const post = await mockApi.publishTreehole(content)
      await useAppStore().refreshStatus()
      await loadTreeholeFeed()
      return post
    } finally {
      submitting.value = false
    }
  }

  async function resonateTreehole(id: string) {
    await mockApi.resonateTreehole(id)
    await loadTreeholeFeed()
  }

  async function replyTreehole(id: string, replyContent: string) {
    await mockApi.replyTreehole(id, replyContent)
    await loadTreeholeFeed()
  }

  async function loadMessages() {
    messages.value = await mockApi.listMessages()
  }

  async function loadConversationThreads() {
    conversationThreads.value = await mockApi.listConversationThreads()
  }

  async function loadWallet() {
    const result = await mockApi.getWallet()
    wallet.value = result.wallet
    ledger.value = result.ledger
    gifts.value = result.gifts
  }

  async function loadVerification() {
    const result = await mockApi.getVerification()
    verification.value = result.verification
    referral.value = result.referral
  }

  async function loadCreators() {
    creators.value = await mockApi.listCreators()
    privatePhotos.value = await mockApi.listPrivatePhotos()
  }

  async function loadPlazaPosts(filters: { city?: string; gender?: string; ageRange?: string } = {}) {
    plazaPosts.value = await plazaApi.listPosts(filters)
  }

  async function loadPlazaPost(postId: string) {
    const post = await plazaApi.getPost(postId)
    const exists = plazaPosts.value.some((item) => item.id === postId)
    plazaPosts.value = exists
      ? plazaPosts.value.map((item) => (item.id === postId ? post : item))
      : [post, ...plazaPosts.value]
    return post
  }

  async function publishPlazaPost(content: string, options: { mediaType?: 'text' | 'image' | 'voice' | 'video'; mediaCount?: number } = {}) {
    submitting.value = true
    try {
      const post = await plazaApi.publishPost(content, options)
      plazaPosts.value = [post, ...plazaPosts.value]
      return post
    } finally {
      submitting.value = false
    }
  }

  async function loadPlazaComments(postId: string) {
    const comments = await plazaApi.listComments(postId)
    plazaComments.value = {
      ...plazaComments.value,
      [postId]: comments
    }
    return comments
  }

  async function commentPlazaPost(postId: string, content: string, options: { hiddenForOwnerOnly?: boolean } = {}) {
    const post = await plazaApi.commentPost(postId, content, options)
    plazaPosts.value = plazaPosts.value.map((item) => (item.id === postId ? post : item))
    return post
  }

  async function likePlazaPost(postId: string) {
    const previous = plazaPosts.value
    plazaPosts.value = plazaPosts.value.map((item) => {
      if (item.id !== postId) return item
      const likedByMe = !item.likedByMe
      const likeCount = Math.max(item.likeCount + (likedByMe ? 1 : -1), 0)
      return { ...item, likedByMe, likeCount }
    })
    try {
      const post = await plazaApi.likePost(postId)
      plazaPosts.value = plazaPosts.value.map((item) => (item.id === postId ? post : item))
      return post
    } catch (error) {
      plazaPosts.value = previous
      throw error
    }
  }

  async function loadNearbyUsers() {
    nearbyUsers.value = await mockApi.listNearbyUsers()
  }

  async function loadBlacklist() {
    blacklist.value = await mockApi.listBlacklist()
  }

  async function loadAdminDashboard() {
    adminDashboard.value = await mockApi.listAdminData()
    adminSession.value = adminDashboard.value.adminSession
  }

  async function adminLogin(accountId: string) {
    adminSession.value = await mockApi.adminLogin(accountId)
    await loadAdminDashboard()
  }

  async function adminLogout() {
    adminSession.value = await mockApi.adminLogout()
    if (adminDashboard.value) {
      adminDashboard.value.adminSession = adminSession.value
    }
  }

  async function saveAdminRewardConfig(config: AdminRewardConfigDraft) {
    adminDashboard.value = await mockApi.saveAdminRewardConfig(config)
    adminSession.value = adminDashboard.value.adminSession
  }

  async function batchReviewContent(ids: string[], status: ContentStatus) {
    adminDashboard.value = await mockApi.batchReviewContent(ids, status)
    adminSession.value = adminDashboard.value.adminSession
  }

  async function batchOfflineContent(ids: string[]) {
    adminDashboard.value = await mockApi.batchOfflineContent(ids)
    adminSession.value = adminDashboard.value.adminSession
  }

  async function submitFaceVerification() {
    verification.value = await mockApi.submitFaceVerification()
  }

  async function claimReferralVip() {
    const result = await mockApi.claimReferralVip()
    referral.value = result.referral
    await useAppStore().refreshStatus()
  }

  async function unlockPrivatePhoto(photoId: string) {
    const result = await mockApi.unlockPrivatePhoto(photoId)
    wallet.value = result.wallet
    privatePhotos.value = privatePhotos.value.map((photo) => (photo.id === photoId ? result.photo : photo))
    await loadWallet()
  }

  async function sendGift(giftId: string, receiverId: string) {
    const result = await mockApi.sendGift(giftId, receiverId)
    wallet.value = result.wallet
    await loadWallet()
    await loadMessages()
  }

  async function requestWithdraw(amount: number) {
    const result = await mockApi.requestWithdraw(amount)
    wallet.value = result.wallet
    await loadWallet()
  }

  return {
    currentBottle,
    treeholeFeed,
    currentTruth,
    currentDare,
    messages,
    conversationThreads,
    wallet,
    ledger,
    creators,
    privatePhotos,
    gifts,
    verification,
    referral,
    plazaPosts,
    plazaComments,
    nearbyUsers,
    blacklist,
    adminDashboard,
    adminSession,
    submitting,
    throwBottle,
    getRandomBottlePrompt,
    fishBottle,
    replyBottle,
    followUser,
    requestFriend,
    reportBottle,
    blockUser,
    drawTruthQuestion,
    drawDareTask,
    loadTreeholeFeed,
    publishTreehole,
    resonateTreehole,
    replyTreehole,
    loadMessages,
    loadConversationThreads,
    loadWallet,
    loadVerification,
    loadCreators,
    loadPlazaPosts,
    loadPlazaPost,
    publishPlazaPost,
    loadPlazaComments,
    commentPlazaPost,
    likePlazaPost,
    loadNearbyUsers,
    loadBlacklist,
    loadAdminDashboard,
    adminLogin,
    adminLogout,
    saveAdminRewardConfig,
    batchReviewContent,
    batchOfflineContent,
    submitFaceVerification,
    claimReferralVip,
    unlockPrivatePhoto,
    sendGift,
    requestWithdraw
  }
})
