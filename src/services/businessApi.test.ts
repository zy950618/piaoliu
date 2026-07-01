import { beforeEach, describe, expect, it, vi } from 'vitest'
import { businessApi } from './businessApi'
import { requestJson } from '@/services/http'

vi.mock('@/services/http', () => ({
  requestJson: vi.fn()
}))

const requestJsonMock = vi.mocked(requestJson)

describe('businessApi membership', () => {
  beforeEach(() => {
    requestJsonMock.mockReset()
  })

  it('verifies membership orders and maps the updated user profile', async () => {
    requestJsonMock.mockResolvedValueOnce({
      order: {
        id: 'order_001',
        platform: 'wechat',
        product_id: 'vip_season',
        transaction_id: 'tx_001',
        status: 'mock_verified',
        vip_level: 'season',
        verified_at: '2026-06-29T00:00:00+00:00'
      },
      user: {
        id: '100000000001',
        nickname: 'member_user',
        avatar_text: 'M',
        avatar_url: 'file://member.png',
        platform: 'h5',
        is_vip: true,
        vip_level: 'season',
        vip_expires_at: '2026-09-27T00:00:00+00:00',
        drift_coins: 260,
        gender: 'female',
        age_range: '25-30',
        city: 'Hangzhou',
        face_verified: true,
        gender_verified: true,
        charm_value: 1880
      }
    })

    const result = await businessApi.verifyMembershipOrder({
      platform: 'wechat',
      productId: 'vip_season',
      transactionId: 'tx_001'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/membership/orders/verify', {
      method: 'POST',
      body: JSON.stringify({
        platform: 'wechat',
        product_id: 'vip_season',
        transaction_id: 'tx_001',
        receipt: 'mock_receipt'
      })
    })
    expect(result.order.vipLevel).toBe('season')
    expect(result.user.isVip).toBe(true)
    expect(result.user.vipLevel).toBe('season')
    expect(result.user.vipExpiresAt).toBe('2026-09-27T00:00:00+00:00')
  })

  it('creates context chat requests with source and evidence fields', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'ctx_001',
      status: 'pending',
      conversation_id: null,
      source_type: 'plaza_comment',
      source_id: 'plaza_001:comment_001',
      source_summary: {
        title: '基于本次互动开启',
        source_type: 'plaza_comment',
        source_id: 'plaza_001:comment_001'
      },
      rate_limit: {
        scope: 'none',
        messages_per_minute: 6
      }
    })

    const result = await businessApi.createContextChatRequest({
      targetUserId: 'creator_001',
      sourceType: 'plaza_comment',
      sourceId: 'plaza_001:comment_001',
      replyId: 'comment_001',
      initiatorAction: 'continue_chat',
      evidenceId: 'comment_001'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/chat/context-requests', {
      method: 'POST',
      body: JSON.stringify({
        target_user_id: 'creator_001',
        source_type: 'plaza_comment',
        source_id: 'plaza_001:comment_001',
        reply_id: 'comment_001',
        initiator_action: 'continue_chat',
        evidence_id: 'comment_001'
      })
    })
    expect(result).toMatchObject({
      id: 'ctx_001',
      status: 'pending',
      sourceType: 'plaza_comment',
      sourceId: 'plaza_001:comment_001'
    })
  })

  it('creates treehole context chat requests after replies', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'ctx_tree_001',
      status: 'pending',
      conversation_id: null,
      source_type: 'treehole_comment',
      source_id: 'tree_001',
      source_summary: {
        title: '基于本次互动开启',
        source_type: 'treehole_comment',
        source_id: 'tree_001'
      },
      rate_limit: {
        scope: 'none',
        messages_per_minute: 6
      }
    })

    const result = await businessApi.createContextChatRequest({
      targetUserId: 'tree_author_001',
      sourceType: 'treehole_comment',
      sourceId: 'tree_001',
      replyId: 'tree_reply:tree_001',
      initiatorAction: 'continue_chat',
      evidenceId: 'treehole_reply:tree_001'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/chat/context-requests', {
      method: 'POST',
      body: JSON.stringify({
        target_user_id: 'tree_author_001',
        source_type: 'treehole_comment',
        source_id: 'tree_001',
        reply_id: 'tree_reply:tree_001',
        initiator_action: 'continue_chat',
        evidence_id: 'treehole_reply:tree_001'
      })
    })
    expect(result).toMatchObject({
      id: 'ctx_tree_001',
      status: 'pending',
      sourceType: 'treehole_comment',
      sourceId: 'tree_001'
    })
  })

  it('creates game room context chat requests after room confirmation', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'ctx_room_001',
      status: 'pending',
      conversation_id: null,
      source_type: 'game_room',
      source_id: 'room_001',
      source_summary: {
        title: '基于本次互动开启',
        source_type: 'game_room',
        source_id: 'room_001'
      },
      rate_limit: {
        scope: 'none',
        messages_per_minute: 6
      }
    })

    const result = await businessApi.createContextChatRequest({
      targetUserId: 'room_partner_001',
      sourceType: 'game_room',
      sourceId: 'room_001',
      replyId: 'thread_001',
      initiatorAction: 'room_confirm',
      evidenceId: 'game_room:room_001'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/chat/context-requests', {
      method: 'POST',
      body: JSON.stringify({
        target_user_id: 'room_partner_001',
        source_type: 'game_room',
        source_id: 'room_001',
        reply_id: 'thread_001',
        initiator_action: 'room_confirm',
        evidence_id: 'game_room:room_001'
      })
    })
    expect(result).toMatchObject({
      id: 'ctx_room_001',
      status: 'pending',
      sourceType: 'game_room',
      sourceId: 'room_001'
    })
  })

  it('creates nearby match expand requests with vip or coin gate metadata', async () => {
    requestJsonMock.mockResolvedValueOnce({
      request: {
        id: 'ctx_match_001',
        status: 'pending',
        conversation_id: null,
        source_type: 'match_expand',
        source_id: 'nearby:creator_001',
        source_summary: {
          title: '基于本次互动开启',
          source_type: 'match_expand',
          source_id: 'nearby:creator_001'
        },
        rate_limit: {
          scope: 'none',
          messages_per_minute: 6
        }
      },
      gate: 'drift_coins',
      cost_coins: 5,
      remaining_drift_coins: 75,
      user: {
        id: '100000000001',
        nickname: 'nearby_user',
        avatar_text: 'N',
        platform: 'h5',
        is_vip: false,
        vip_level: 'none',
        drift_coins: 75,
        gender: 'female',
        charm_value: 1880
      }
    })

    const result = await businessApi.createMatchExpandContextRequest('creator_001')

    expect(requestJsonMock).toHaveBeenCalledWith('/chat/match-expand-requests', {
      method: 'POST',
      body: JSON.stringify({
        target_user_id: 'creator_001'
      })
    })
    expect(result).toMatchObject({
      gate: 'drift_coins',
      costCoins: 5,
      remainingDriftCoins: 75,
      request: {
        status: 'pending',
        sourceType: 'match_expand',
        sourceId: 'nearby:creator_001'
      },
      user: {
        driftCoins: 75
      }
    })
  })

  it('loads nearby users with shared city and age filters', async () => {
    requestJsonMock.mockResolvedValueOnce([
      {
        id: 'creator_001',
        nickname: 'nearby_user',
        icon_text: 'N',
        icon_url: '',
        gender: 'female',
        verified: true,
        age_range: '25-30',
        city: '杭州',
        distance_km: 2.2,
        distance_text: '2.2km',
        signature: '礼貌匹配',
        is_vip: true,
        online: true
      }
    ])

    const result = await businessApi.listNearbyUsers({
      city: '杭州',
      gender: '女',
      ageRange: '24-31'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/nearby/users?city=%E6%9D%AD%E5%B7%9E&gender=%E5%A5%B3&age_range=24-31')
    expect(result[0]).toMatchObject({
      id: 'creator_001',
      city: '杭州',
      gender: 'female',
      ageRange: '25-30',
      iconUrl: expect.stringContaining('https://api.dicebear.com/9.x/open-peeps/svg')
    })
  })

  it('starts game random match with filters and maps quota metadata', async () => {
    requestJsonMock.mockResolvedValueOnce({
      match_id: 'match_front_001',
      room_id: 'room_front_001',
      mode: 'truth',
      status: 'matched',
      target_user: {
        id: 'creator_001',
        nickname: 'game_partner',
        icon_text: 'G',
        gender: 'female',
        verified: true,
        age_range: '25-30',
        distance_km: 2.2,
        distance_text: '2.2km',
        signature: '礼貌匹配',
        is_vip: true,
        online: true
      },
      quota: {
        type: 'truth',
        label: '真心话',
        base: 5,
        vip_bonus: 5,
        ad_bonus: 0,
        used: 1,
        remaining: 9
      },
      source_type: 'game_room',
      source_id: 'room_front_001',
      evidence_id: 'game_random_match:room_front_001',
      next_action: 'wait_confirm'
    })

    const result = await businessApi.startGameRandomMatch({
      mode: 'truth',
      gender: 'female',
      ageRange: '25-30',
      clientMatchId: 'front_match_001'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/game/random-match', {
      method: 'POST',
      body: JSON.stringify({
        mode: 'truth',
        gender: 'female',
        age_range: '25-30',
        client_match_id: 'front_match_001'
      })
    })
    expect(result).toMatchObject({
      matchId: 'match_front_001',
      roomId: 'room_front_001',
      mode: 'truth',
      targetUser: {
        id: 'creator_001',
        ageRange: '25-30'
      },
      quota: {
        type: 'truth',
        remaining: 9
      },
      sourceType: 'game_room',
      evidenceId: 'game_random_match:room_front_001'
    })
  })

  it('accepts context chat requests and maps active conversation ids', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'ctx_002',
      status: 'active',
      conversation_id: 'chat_002',
      source_type: 'bottle_reply',
      source_id: 'bottle_002',
      source_summary: {
        title: '基于本次互动开启',
        source_type: 'bottle_reply',
        source_id: 'bottle_002'
      },
      rate_limit: {
        scope: 'none',
        messages_per_minute: 6
      }
    })

    const result = await businessApi.acceptContextChatRequest('ctx_002', {
      confirmAction: 'reply',
      evidenceId: 'author_reply_002'
    })

    expect(requestJsonMock).toHaveBeenCalledWith('/chat/context-requests/ctx_002/accept', {
      method: 'POST',
      body: JSON.stringify({
        confirm_action: 'reply',
        evidence_id: 'author_reply_002'
      })
    })
    expect(result).toMatchObject({
      id: 'ctx_002',
      status: 'active',
      conversationId: 'chat_002',
      sourceType: 'bottle_reply'
    })
  })

  it('lists and rejects context chat invitation cards', async () => {
    requestJsonMock.mockResolvedValueOnce([
      {
        id: 'ctx_invite_001',
        status: 'pending',
        conversation_id: null,
        source_type: 'game_room',
        source_id: 'room_invite_001',
        source_summary: {
          title: '游戏房间邀请',
          source_type: 'game_room',
          source_id: 'room_invite_001'
        },
        rate_limit: {
          scope: 'none',
          messages_per_minute: 6
        }
      }
    ])
    requestJsonMock.mockResolvedValueOnce({
      id: 'ctx_invite_001',
      status: 'expired',
      conversation_id: null,
      source_type: 'game_room',
      source_id: 'room_invite_001',
      source_summary: {
        title: '游戏房间邀请',
        source_type: 'game_room',
        source_id: 'room_invite_001'
      },
      rate_limit: {
        scope: 'none',
        messages_per_minute: 6
      }
    })

    const list = await businessApi.listContextChatRequests()
    const rejected = await businessApi.rejectContextChatRequest('ctx_invite_001', 'user_cancel_from_messages')

    expect(requestJsonMock).toHaveBeenNthCalledWith(1, '/chat/context-requests')
    expect(requestJsonMock).toHaveBeenNthCalledWith(2, '/chat/context-requests/ctx_invite_001/reject', {
      method: 'POST',
      body: JSON.stringify({
        reason: 'user_cancel_from_messages'
      })
    })
    expect(list[0]).toMatchObject({
      id: 'ctx_invite_001',
      status: 'pending',
      sourceType: 'game_room',
      sourceId: 'room_invite_001'
    })
    expect(rejected).toMatchObject({
      id: 'ctx_invite_001',
      status: 'expired'
    })
  })

  it('loads context conversation detail for temporary chat pages', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'chat_002',
      status: 'active',
      source_type: 'bottle_reply',
      source_id: 'bottle_002',
      source_summary: {
        title: '基于本次互动开启',
        source_type: 'bottle_reply',
        source_id: 'bottle_002'
      },
      participants: ['user_demo', 'creator_001'],
      friendship_state: 'none',
      expires_at: '2026-07-06T00:00:00+00:00',
      last_message: 'hello',
      rate_limit: {
        scope: 'none',
        messages_per_minute: 6
      },
      risk_state: 'clear',
      report_state: 'none',
      messages: [
        {
          id: 'msg_001',
          sender_id: 'user_demo',
          content_type: 'text',
          content: 'hello',
          status: 'sent',
          created_at: '2026-06-29T00:00:00+00:00'
        }
      ],
      audit_refs: ['audit_001']
    })

    const result = await businessApi.getContextConversation('chat_002')

    expect(requestJsonMock).toHaveBeenCalledWith('/chat/conversations/chat_002')
    expect(result).toMatchObject({
      id: 'chat_002',
      status: 'active',
      sourceType: 'bottle_reply',
      sourceId: 'bottle_002',
      messages: [
        {
          id: 'msg_001',
          senderId: 'user_demo',
          contentType: 'text',
          content: 'hello'
        }
      ]
    })
  })

  it('marks a conversation thread as read through the backend contract', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'thread_read_001',
      bottle_id: 'bottle_001',
      participant_user_id: 'creator_001',
      participant_name: '北岸',
      participant_avatar_text: null,
      participant_avatar_url: 'https://example.test/avatar.png',
      participant_tag: '广场互动',
      bottle_preview: 'preview',
      last_message: 'latest',
      updated_at: '2026-06-30T00:00:00+00:00',
      unread_count: 0,
      turns: []
    })

    const result = await businessApi.markConversationRead('thread_read_001')

    expect(requestJsonMock).toHaveBeenCalledWith('/conversations/thread_read_001/read', { method: 'POST' })
    expect(result).toMatchObject({
      id: 'thread_read_001',
      unreadCount: 0,
      participantName: '北岸'
    })
  })

  it('marks one message notification as read through the backend contract', async () => {
    requestJsonMock.mockResolvedValueOnce({
      id: 'msg_read_001',
      title: '系统通知',
      body: '单条通知已读',
      created_at: '2026-06-30T00:00:00+00:00',
      unread: false,
      business_type: 'system',
      business_id: 'system_001'
    })

    const result = await businessApi.markMessageRead('msg_read_001')

    expect(requestJsonMock).toHaveBeenCalledWith('/messages/msg_read_001/read', { method: 'POST' })
    expect(result).toMatchObject({
      id: 'msg_read_001',
      unread: false,
      businessType: 'system',
      businessId: 'system_001'
    })
  })
})
