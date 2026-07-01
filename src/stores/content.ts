import { ref } from 'vue'
import { defineStore } from 'pinia'
import type {
  Bottle,
  BottleTargetGender,
  BottleTargetScope,
  BlacklistItem,
  CoinLedgerItem,
  ConversationThread,
  ConversationTurn,
  ContextChatConversation,
  ContextChatRequest,
  ContextChatRequestAcceptPayload,
  ContextChatRequestPayload,
  CreatorProfile,
  DareTask,
  GameRandomMatchMode,
  GiftProduct,
  MessageItem,
  NearbyUser,
  PlazaComment,
  PlazaPost,
  PrivatePhoto,
  ReferralState,
  TreeholePost,
  TruthQuestion,
  UserActivityRecord,
  UserProfile,
  UserRecordSummaryItem,
  VerificationState,
  WalletState
} from '@/types/domain'
import { businessApi } from '@/services/businessApi'
import { plazaApi } from '@/services/plazaApi'
import { removeTabBadge, setTabBadge } from '@/services/feedback'
import { useAppStore } from './app'

interface BottleFilterOptions {
  city?: string
  gender?: string
  ageRange?: string
}

interface ThrowBottleOptions {
  targetGender?: BottleTargetGender
  targetScope?: BottleTargetScope
}

function profileAvatarText(profile: UserProfile, fallback: string) {
  return profile.avatarText || profile.nickname.slice(0, 1) || fallback
}

export const useContentStore = defineStore('content', () => {
  const currentBottle = ref<Bottle>()
  const treeholeFeed = ref<TreeholePost[]>([])
  const currentTruth = ref<TruthQuestion>()
  const currentDare = ref<DareTask>()
  const messages = ref<MessageItem[]>([])
  const conversationThreads = ref<ConversationThread[]>([])
  const contextChatRequests = ref<ContextChatRequest[]>([])
  const currentContextConversation = ref<ContextChatConversation>()
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
  const userRecords = ref<UserRecordSummaryItem[]>([])
  const submitting = ref(false)

  async function throwBottle(content: string, options: ThrowBottleOptions = {}) {
    submitting.value = true
    try {
      const bottle = await businessApi.throwBottle(content, options)
      await useAppStore().refreshStatus()
      currentBottle.value = bottle
      return bottle
    } finally {
      submitting.value = false
    }
  }

  async function getRandomBottlePrompt() {
    return businessApi.getRandomBottlePrompt()
  }

  async function fishBottle(filters: BottleFilterOptions = {}) {
    const bottle = await businessApi.fishBottle(filters)
    await useAppStore().refreshStatus()
    currentBottle.value = bottle
    return bottle
  }

  async function replyBottle(id: string, content: string) {
    await businessApi.replyBottle(id, content)
    await loadMessages()
    await loadConversationThreads()
  }

  async function followUser(userId: string) {
    await businessApi.followUser(userId)
    await loadMessages()
    if (currentBottle.value?.authorId === userId) currentBottle.value.isFollowing = true
  }

  async function requestFriend(userId: string) {
    await businessApi.requestFriend(userId)
    await loadMessages()
    if (currentBottle.value?.authorId === userId) currentBottle.value.friendRequested = true
  }

  async function reportBottle(id: string, reason: string) {
    await businessApi.reportBottle(id, reason)
    await loadMessages()
  }

  async function reportPlazaPost(id: string, reason: string) {
    await businessApi.reportPlazaPost(id, reason)
    await loadMessages()
  }

  async function reportUser(id: string, reason: string) {
    await businessApi.reportUser(id, reason)
    await loadMessages()
  }

  async function blockUser(userId: string, reason: string) {
    void reason
    await businessApi.blockUser(userId)
    await loadMessages()
    await loadBlacklist()
  }

  async function drawTruthQuestion() {
    const question = await businessApi.drawTruthQuestion()
    await useAppStore().refreshStatus()
    currentTruth.value = question
    return question
  }

  async function drawDareTask() {
    const task = await businessApi.drawDareTask()
    await useAppStore().refreshStatus()
    currentDare.value = task
    return task
  }

  async function loadTreeholeFeed() {
    treeholeFeed.value = await businessApi.listTreeholeFeed()
  }

  async function publishTreehole(content: string) {
    submitting.value = true
    try {
      const post = await businessApi.publishTreehole(content)
      await useAppStore().refreshStatus()
      await loadTreeholeFeed()
      return post
    } finally {
      submitting.value = false
    }
  }

  async function resonateTreehole(id: string) {
    await businessApi.resonateTreehole(id)
    await loadTreeholeFeed()
  }

  async function replyTreehole(id: string, replyContent: string) {
    await businessApi.replyTreehole(id, replyContent)
    await loadTreeholeFeed()
  }

  async function loadMessages() {
    messages.value = await businessApi.listMessages()
    syncMessageBadge()
  }

  async function loadConversationThreads() {
    conversationThreads.value = await businessApi.listConversationThreads()
    syncMessageBadge()
  }

  function unreadTotal() {
    return messages.value.filter((item) => item.unread).length + conversationThreads.value.reduce((sum, thread) => sum + thread.unreadCount, 0)
  }

  function syncMessageBadge() {
    const count = unreadTotal()
    if (count > 0) {
      setTabBadge(3, count > 99 ? '99+' : String(count))
      return
    }
    removeTabBadge(3)
  }

  function markAllMessagesRead() {
    messages.value = messages.value.map((item) => ({ ...item, unread: false }))
    conversationThreads.value = conversationThreads.value.map((thread) => ({ ...thread, unreadCount: 0 }))
    void businessApi.markMessagesRead()
    syncMessageBadge()
  }

  async function markMessageRead(messageId: string) {
    messages.value = messages.value.map((item) => (item.id === messageId ? { ...item, unread: false } : item))
    try {
      const updatedMessage = await businessApi.markMessageRead(messageId)
      messages.value = messages.value.map((item) => (item.id === messageId ? updatedMessage : item))
    } catch {
      // Keep local read state when the network request fails; the next refresh will reconcile.
    }
    syncMessageBadge()
  }

  async function markConversationRead(threadId: string) {
    conversationThreads.value = conversationThreads.value.map((thread) => (
      thread.id === threadId ? { ...thread, unreadCount: 0 } : thread
    ))
    try {
      const updatedThread = await businessApi.markConversationRead(threadId)
      const exists = conversationThreads.value.some((thread) => thread.id === threadId)
      conversationThreads.value = exists
        ? conversationThreads.value.map((thread) => (
          thread.id === threadId ? updatedThread : thread
        ))
        : [updatedThread, ...conversationThreads.value]
    } catch {
      // Keep local read state when the network request fails; the next refresh will reconcile.
    }
    syncMessageBadge()
  }

  async function submitChatAppeal(threadId: string, reason: string) {
    const appeal = await businessApi.createChatAppeal(threadId, reason)
    await loadMessages()
    return appeal
  }

  async function sendConversationTurn(
    threadId: string,
    payload: Pick<ConversationTurn, 'body' | 'type' | 'mediaUrl' | 'mediaDuration'>
  ) {
    const thread = await businessApi.sendConversationTurn(threadId, payload)
    conversationThreads.value = conversationThreads.value.map((item) => (item.id === threadId ? thread : item))
    return thread
  }

  async function viewConversationTurn(threadId: string, turnId: string) {
    const thread = await businessApi.viewConversationTurn(threadId, turnId)
    conversationThreads.value = conversationThreads.value.map((item) => (item.id === threadId ? thread : item))
    return thread
  }

  async function createGameRoom(threadId: string, mode: 'truth' | 'dare' | 'mixed') {
    const result = await businessApi.createGameRoom(threadId, mode)
    conversationThreads.value = conversationThreads.value.map((item) => (item.id === threadId ? result.thread : item))
    return result
  }

  async function createContextChatRequest(payload: ContextChatRequestPayload) {
    const result = await businessApi.createContextChatRequest(payload)
    await loadContextChatRequests()
    return result
  }

  async function loadContextChatRequests() {
    contextChatRequests.value = await businessApi.listContextChatRequests()
    return contextChatRequests.value
  }

  async function createMatchExpandContextRequest(targetUserId: string) {
    const result = await businessApi.createMatchExpandContextRequest(targetUserId)
    useAppStore().applyUserProfile(result.user)
    if (result.threadId) {
      await markConversationRead(result.threadId)
    }
    await loadContextChatRequests()
    return result
  }

  async function acceptContextChatRequest(requestId: string, payload: ContextChatRequestAcceptPayload) {
    const result = await businessApi.acceptContextChatRequest(requestId, payload)
    contextChatRequests.value = contextChatRequests.value.map((item) => (item.id === requestId ? result : item))
    return result
  }

  async function rejectContextChatRequest(requestId: string, reason: string) {
    const result = await businessApi.rejectContextChatRequest(requestId, reason)
    contextChatRequests.value = contextChatRequests.value.map((item) => (item.id === requestId ? result : item))
    return result
  }

  async function loadContextConversation(conversationId: string) {
    currentContextConversation.value = await businessApi.getContextConversation(conversationId)
    return currentContextConversation.value
  }

  async function sendContextConversationMessage(conversationId: string, message: string) {
    const result = await businessApi.sendContextConversationMessage(conversationId, message)
    currentContextConversation.value = await businessApi.getContextConversation(conversationId)
    return result
  }

  async function loadWallet() {
    const result = await businessApi.getWallet()
    wallet.value = result.wallet
    ledger.value = result.ledger
    gifts.value = result.gifts
  }

  async function loadVerification() {
    const result = await businessApi.getVerification()
    verification.value = result.verification
    referral.value = result.referral
  }

  async function loadCreators() {
    creators.value = await businessApi.listCreators()
    privatePhotos.value = await businessApi.listPrivatePhotos()
  }

  async function loadPrivatePhotos() {
    privatePhotos.value = await businessApi.listPrivatePhotos()
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

  async function publishPlazaPost(
    content: string,
    options: {
      mediaType?: 'text' | 'image' | 'voice' | 'video'
      mediaCount?: number
      media?: Array<{
        mediaType: 'image' | 'voice' | 'video'
        url: string
        mimeType: string
        storageKey?: string
        sizeBytes?: number
        durationSeconds?: number
        width?: number
        height?: number
      }>
    } = {}
  ) {
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

  async function loadNearbyUsers(filters: BottleFilterOptions & { distanceKm?: number } = {}) {
    nearbyUsers.value = await businessApi.listNearbyUsers(filters)
  }

  async function loadBlacklist() {
    blacklist.value = await businessApi.listBlacklist()
  }

  async function submitFaceVerification() {
    verification.value = await businessApi.submitFaceVerification()
  }

  async function claimReferralVip() {
    const result = await businessApi.claimReferralVip()
    referral.value = result.referral
    await useAppStore().refreshStatus()
  }

  async function unlockPrivatePhoto(photoId: string) {
    const result = await businessApi.unlockPrivatePhoto(photoId)
    wallet.value = result.wallet
    privatePhotos.value = privatePhotos.value.map((photo) => (photo.id === photoId ? result.photo : photo))
    await loadWallet()
  }

  async function sendGift(giftId: string, receiverId: string) {
    const result = await businessApi.sendGift(giftId, receiverId)
    wallet.value = result.wallet
    await loadWallet()
    await loadMessages()
  }

  async function sendConversationGift(threadId: string, giftId: string) {
    const result = await businessApi.sendConversationGift(threadId, giftId)
    wallet.value = result.wallet
    conversationThreads.value = conversationThreads.value.map((item) => (item.id === threadId ? result.thread : item))
    await loadWallet()
    return result
  }

  async function rechargeCoins(amount: number) {
    const result = await businessApi.rechargeCoins(amount)
    wallet.value = result.wallet
    await loadWallet()
    return result
  }

  async function requestWithdraw(amount: number) {
    const result = await businessApi.requestWithdraw(amount)
    wallet.value = result.wallet
    await loadWallet()
  }

  async function loadUserRecords() {
    userRecords.value = await businessApi.listUserRecords()
  }

  async function saveUserActivityRecord(payload: {
    recordType: UserActivityRecord['recordType']
    title: string
    content: string
    visibility?: string
    sourceType?: string
    sourceId?: string
  }) {
    const record = await businessApi.saveUserActivityRecord(payload)
    await loadUserRecords()
    return record
  }

  async function startGameRandomMatch(payload: { mode: GameRandomMatchMode; gender: BottleTargetGender; ageRange?: string; clientMatchId: string }) {
    const result = await businessApi.startGameRandomMatch(payload)
    await useAppStore().refreshStatus()
    await loadMessages()
    return result
  }

  function syncCurrentUserProfile(profile: UserProfile) {
    const avatarText = profileAvatarText(profile, '海')
    const anonymousAvatarText = profileAvatarText(profile, '匿')
    const verified = Boolean(profile.faceVerified && profile.genderVerified)

    if (currentBottle.value?.authorId === profile.id) {
      currentBottle.value = {
        ...currentBottle.value,
        authorName: profile.nickname,
        authorAvatarText: avatarText,
        authorAvatarUrl: profile.avatarUrl,
        authorVip: profile.isVip,
        authorGender: profile.gender || 'unknown',
        authorAgeRange: profile.ageRange,
        authorCity: profile.city,
        authorVerified: verified
      }
    }

    treeholeFeed.value = treeholeFeed.value.map((post) => (
      post.authorId === profile.id
        ? {
            ...post,
            authorName: profile.nickname,
            authorAvatarText: anonymousAvatarText,
            authorAvatarUrl: profile.avatarUrl,
            authorGender: profile.gender || 'unknown',
            authorAgeRange: profile.ageRange || post.authorAgeRange
          }
        : post
    ))

    plazaPosts.value = plazaPosts.value.map((post) => (
      post.authorId === profile.id
        ? {
            ...post,
            authorName: profile.nickname,
            iconText: avatarText,
            iconUrl: profile.avatarUrl,
            gender: profile.gender,
            verified,
            city: profile.city,
            ageRange: profile.ageRange
          }
        : post
    ))

    plazaComments.value = Object.fromEntries(
      Object.entries(plazaComments.value).map(([postId, comments]) => [
        postId,
        comments.map((comment) => (
          comment.authorId === profile.id
            ? {
                ...comment,
                authorName: profile.nickname,
                iconText: anonymousAvatarText,
                iconUrl: profile.avatarUrl,
                authorGender: profile.gender || 'unknown',
                authorAgeRange: profile.ageRange,
                authorVerified: verified,
                authorCity: profile.city
              }
            : comment
        ))
      ])
    )

    conversationThreads.value = conversationThreads.value.map((thread) => ({
      ...thread,
      ...(thread.participantUserId === profile.id
        ? {
            participantName: profile.nickname,
            participantAvatarText: avatarText,
            participantAvatarUrl: profile.avatarUrl
          }
        : {}),
      turns: thread.turns.map((turn) => (
        turn.fromMe ? { ...turn, senderName: profile.nickname } : turn
      ))
    }))

    creators.value = creators.value.map((creator) => (
      creator.userId === profile.id
        ? {
            ...creator,
            displayName: profile.nickname,
            gender: profile.gender || 'unknown',
            verified,
            charmValue: profile.charmValue ?? creator.charmValue
          }
        : creator
    ))

    privatePhotos.value = privatePhotos.value.map((photo) => (
      photo.ownerId === profile.id ? { ...photo, ownerName: profile.nickname } : photo
    ))

    nearbyUsers.value = nearbyUsers.value.map((user) => (
      user.id === profile.id
        ? {
            ...user,
            nickname: profile.nickname,
            iconText: avatarText,
            iconUrl: profile.avatarUrl,
            gender: profile.gender || 'unknown',
            verified,
            ageRange: profile.ageRange,
            isVip: profile.isVip
          }
        : user
    ))

    blacklist.value = blacklist.value.map((item) => (
      item.userId === profile.id ? { ...item, nickname: profile.nickname } : item
    ))
  }

  return {
    currentBottle,
    treeholeFeed,
    currentTruth,
    currentDare,
    messages,
    conversationThreads,
    contextChatRequests,
    currentContextConversation,
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
    userRecords,
    submitting,
    throwBottle,
    getRandomBottlePrompt,
    fishBottle,
    replyBottle,
    followUser,
    requestFriend,
    reportBottle,
    reportPlazaPost,
    reportUser,
    blockUser,
    drawTruthQuestion,
    drawDareTask,
    loadTreeholeFeed,
    publishTreehole,
    resonateTreehole,
    replyTreehole,
    loadMessages,
    loadConversationThreads,
    markAllMessagesRead,
    markMessageRead,
    markConversationRead,
    submitChatAppeal,
    sendConversationTurn,
    viewConversationTurn,
    createGameRoom,
    createContextChatRequest,
    loadContextChatRequests,
    createMatchExpandContextRequest,
    acceptContextChatRequest,
    rejectContextChatRequest,
    loadContextConversation,
    sendContextConversationMessage,
    loadWallet,
    loadVerification,
    loadCreators,
    loadPrivatePhotos,
    loadPlazaPosts,
    loadPlazaPost,
    publishPlazaPost,
    loadPlazaComments,
    commentPlazaPost,
    likePlazaPost,
    loadNearbyUsers,
    loadBlacklist,
    submitFaceVerification,
    claimReferralVip,
    unlockPrivatePhoto,
    sendGift,
    sendConversationGift,
    rechargeCoins,
    requestWithdraw,
    loadUserRecords,
    saveUserActivityRecord,
    startGameRandomMatch,
    syncCurrentUserProfile
  }
})
