import { beforeEach, describe, expect, it, vi } from 'vitest'
import { meApi } from './meApi'
import { requestJson } from '@/services/http'

vi.mock('@/services/http', () => ({
  requestJson: vi.fn()
}))

const requestJsonMock = vi.mocked(requestJson)

describe('meApi status fallback', () => {
  beforeEach(() => {
    requestJsonMock.mockReset()
  })

  it('falls back to mock status in development when status request fails', async () => {
    requestJsonMock.mockRejectedValueOnce(new Error('request:fail'))

    const status = await meApi.getStatus()

    expect(requestJsonMock).toHaveBeenCalledWith('/me/status')
    expect(status.user.id).toBeTruthy()
    expect(status.quotas.fish_bottle.remaining).toBeGreaterThanOrEqual(0)
  })
})
