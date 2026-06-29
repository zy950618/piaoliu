const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8100'

const env = (import.meta as unknown as { env?: Record<string, string | undefined> }).env
export const API_BASE_URL = env?.VITE_API_BASE_URL || DEFAULT_API_BASE_URL

export interface ApiRequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  headers?: Record<string, string>
  body?: unknown
}

const CLIENT_ID_KEY = 'piaoliu_client_id'

function createClientId() {
  const randomPart = Math.floor(Math.random() * 1_000_000).toString().padStart(6, '0')
  return `${Date.now()}${randomPart}`
}

function isNumericClientId(value: unknown): value is string {
  return typeof value === 'string' && /^\d{8,64}$/.test(value)
}

function getClientId() {
  if (typeof uni !== 'undefined' && typeof uni.getStorageSync === 'function') {
    const stored = uni.getStorageSync(CLIENT_ID_KEY)
    if (isNumericClientId(stored)) return stored
    const next = createClientId()
    uni.setStorageSync(CLIENT_ID_KEY, next)
    return next
  }
  if (typeof localStorage !== 'undefined') {
    const stored = localStorage.getItem(CLIENT_ID_KEY)
    if (isNumericClientId(stored)) return stored
    const next = createClientId()
    localStorage.setItem(CLIENT_ID_KEY, next)
    return next
  }
  return createClientId()
}

function normalizeBody(body: unknown) {
  if (typeof body !== 'string') return body
  try {
    return JSON.parse(body)
  } catch {
    return body
  }
}

export async function requestJson<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const headers = {
    'Content-Type': 'application/json',
    'X-Client-Id': getClientId(),
    ...(options.headers || {})
  }
  const url = `${API_BASE_URL}${path}`

  if (typeof uni !== 'undefined' && typeof uni.request === 'function') {
    return new Promise<T>((resolve, reject) => {
      uni.request({
        url,
        method: options.method || 'GET',
        header: headers,
        data: normalizeBody(options.body),
        success: (response) => {
          const statusCode = response.statusCode || 0
          if (statusCode < 200 || statusCode >= 300) {
            reject(new Error(typeof response.data === 'string' ? response.data : `HTTP_${statusCode}`))
            return
          }
          resolve(response.data as T)
        },
        fail: (error) => reject(error)
      })
    })
  }

  const response = await fetch(url, {
    headers,
    method: options.method,
    body: typeof options.body === 'string' ? options.body : options.body == null ? undefined : JSON.stringify(options.body)
  })
  if (!response.ok) {
    const body = await response.text()
    throw new Error(body || `HTTP_${response.status}`)
  }
  return response.json() as Promise<T>
}
