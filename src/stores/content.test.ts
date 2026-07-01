import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useContentStore } from './content'
import type { UserProfile } from '@/types/domain'

const updatedProfile: UserProfile = {
  id: 'user_sync_001',
  nickname: 'profile_sync_user',
  avatarText: 'S',
  avatarUrl: 'file://profile_sync.png',
  platform: 'h5',
  isVip: true,
  vipLevel: 'monthly',
  driftCoins: 120,
  gender: 'female',
  ageRange: '25-30',
  city: 'Hangzhou',
  faceVerified: true,
  genderVerified: true,
  charmValue: 88
}

describe('content profile sync', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('updates loaded author snapshots after the current user profile changes', () => {
    const content = useContentStore()
    content.currentBottle = {
      id: 'bottle_sync_001',
      authorId: updatedProfile.id,
      authorName: 'old_name',
      authorAvatarText: 'O',
      content: 'bottle',
      mood: 'drift',
      status: 'approved',
      replies: 0,
      createdAt: '2026-01-01T00:00:00Z'
    }
    content.treeholeFeed = [{
      id: 'tree_sync_001',
      authorId: updatedProfile.id,
      authorName: 'old_name',
      authorAvatarText: 'O',
      authorGender: 'unknown',
      authorAgeRange: 'unknown',
      content: 'tree',
      resonanceCount: 0,
      replyCount: 0,
      status: 'approved',
      createdAt: '2026-01-01T00:00:00Z'
    }]
    content.plazaPosts = [{
      id: 'plaza_sync_001',
      authorId: updatedProfile.id,
      authorName: 'old_name',
      iconText: 'O',
      topic: 'topic',
      content: 'post',
      likeCount: 0,
      commentCount: 1,
      createdAt: '2026-01-01T00:00:00Z'
    }]
    content.plazaComments = {
      plaza_sync_001: [{
        id: 'comment_sync_001',
        postId: 'plaza_sync_001',
        authorId: updatedProfile.id,
        authorName: 'old_name',
        iconText: 'O',
        content: 'comment',
        createdAt: '2026-01-01T00:00:00Z'
      }]
    }
    content.conversationThreads = [{
      id: 'thread_sync_001',
      bottleId: 'bottle_sync_001',
      status: 'active',
      participantUserId: 'other_user',
      participantName: 'other',
      participantTag: 'chat',
      bottlePreview: 'preview',
      lastMessage: 'message',
      updatedAt: '2026-01-01T00:00:00Z',
      unreadCount: 0,
      turns: [{
        id: 'turn_sync_001',
        senderName: 'old_name',
        body: 'message',
        createdAt: '2026-01-01T00:00:00Z',
        fromMe: true
      }]
    }]

    content.syncCurrentUserProfile(updatedProfile)

    expect(content.currentBottle?.authorName).toBe(updatedProfile.nickname)
    expect(content.currentBottle?.authorAvatarUrl).toBe(updatedProfile.avatarUrl)
    expect(content.treeholeFeed[0]?.authorName).toBe(updatedProfile.nickname)
    expect(content.plazaPosts[0]?.iconUrl).toBe(updatedProfile.avatarUrl)
    expect(content.plazaComments.plaza_sync_001?.[0]?.authorName).toBe(updatedProfile.nickname)
    expect(content.conversationThreads[0]?.turns[0]?.senderName).toBe(updatedProfile.nickname)
  })
})
