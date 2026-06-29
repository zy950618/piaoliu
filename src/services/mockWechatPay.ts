export interface MockWechatPayOrder {
  orderId: string
  channel: 'wechat'
  amountCoins: number
  amountCents: number
  status: 'created' | 'paid'
  prepayId: string
}

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export async function createMockWechatPayOrder(amountCoins: number): Promise<MockWechatPayOrder> {
  if (amountCoins <= 0) throw new Error('INVALID_PAY_AMOUNT')
  await delay(180)
  const suffix = `${Date.now()}_${Math.random().toString(16).slice(2, 8)}`
  return {
    orderId: `wx_order_${suffix}`,
    channel: 'wechat',
    amountCoins,
    amountCents: amountCoins,
    status: 'created',
    prepayId: `mock_prepay_${suffix}`
  }
}

export async function waitMockWechatPayCallback(order: MockWechatPayOrder): Promise<MockWechatPayOrder> {
  await delay(260)
  return {
    ...order,
    status: 'paid'
  }
}
