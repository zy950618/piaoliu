import { describe, expect, it } from 'vitest'
import { createMockWechatPayOrder, waitMockWechatPayCallback } from './mockWechatPay'

describe('mockWechatPay', () => {
  it('creates a wechat order and settles it through callback', async () => {
    const order = await createMockWechatPayOrder(68)
    expect(order.channel).toBe('wechat')
    expect(order.amountCoins).toBe(68)
    expect(order.status).toBe('created')

    const paidOrder = await waitMockWechatPayCallback(order)
    expect(paidOrder.orderId).toBe(order.orderId)
    expect(paidOrder.status).toBe('paid')
  })
})
