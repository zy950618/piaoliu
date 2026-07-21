import { API_BASE_URL, getAccessToken } from './http'

export interface RealtimeConnection {
  close: () => void
}

export async function connectContextChat(
  conversationId: string,
  onEvent: (event: Record<string, unknown>) => void,
  onDisconnected?: () => void
): Promise<RealtimeConnection | undefined> {
  if (typeof uni === 'undefined' || typeof uni.connectSocket !== 'function') return undefined
  const token = await getAccessToken()
  const wsBase = API_BASE_URL.replace(/^http:/, 'ws:').replace(/^https:/, 'wss:')
  const socket = uni.connectSocket({
    url: `${wsBase}/ws/chat/${encodeURIComponent(conversationId)}?token=${encodeURIComponent(token)}`,
    fail: () => onDisconnected?.()
  })
  socket.onMessage((message) => {
    try {
      const event = JSON.parse(String(message.data)) as Record<string, unknown>
      onEvent(event)
    } catch {
      // Invalid events are ignored; HTTP sync remains the recovery source.
    }
  })
  socket.onError(() => onDisconnected?.())
  socket.onClose(() => onDisconnected?.())
  return { close: () => socket.close({}) }
}

export async function connectRoom(
  roomId: string,
  onEvent: (event: Record<string, unknown>) => void,
  onDisconnected?: () => void
): Promise<RealtimeConnection | undefined> {
  if (typeof uni === 'undefined' || typeof uni.connectSocket !== 'function') return undefined
  const token = await getAccessToken()
  const wsBase = API_BASE_URL.replace(/^http:/, 'ws:').replace(/^https:/, 'wss:')
  const socket = uni.connectSocket({
    url: `${wsBase}/ws/rooms/${encodeURIComponent(roomId)}?token=${encodeURIComponent(token)}`,
    fail: () => onDisconnected?.()
  })
  socket.onMessage((message) => {
    try {
      onEvent(JSON.parse(String(message.data)) as Record<string, unknown>)
    } catch {
      // HTTP reload remains the recovery path for malformed events.
    }
  })
  socket.onError(() => onDisconnected?.())
  socket.onClose(() => onDisconnected?.())
  return { close: () => socket.close({}) }
}
