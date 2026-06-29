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
})
