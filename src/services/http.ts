const DEFAULT_API_BASE_URL = 'http://127.0.0.1:8100'

const env = (import.meta as unknown as { env?: Record<string, string | undefined> }).env
export const API_BASE_URL = env?.VITE_API_BASE_URL || DEFAULT_API_BASE_URL

export interface ApiRequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  headers?: Record<string, string>
  body?: unknown
}

const CLIENT_ID_KEY = 'piaoliu_client_id'
const ACCESS_TOKEN_KEY = 'piaoliu_access_token'
let loginPromise: Promise<string> | undefined

function createClientId() {
  const randomPart = Math.floor(Math.random() * 1_000_000).toString().padStart(6, '0')
  return `${Date.now()}${randomPart}`
}

function isNumericClientId(value: unknown): value is string {
  return typeof value === 'string' && /^\d{8,64}$/.test(value)
}

export function getClientId() {
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

function getStoredToken() {
  if (typeof uni !== 'undefined' && typeof uni.getStorageSync === 'function') {
    return String(uni.getStorageSync(ACCESS_TOKEN_KEY) || '')
  }
  if (typeof localStorage !== 'undefined') return localStorage.getItem(ACCESS_TOKEN_KEY) || ''
  return ''
}

function storeToken(token: string) {
  if (typeof uni !== 'undefined' && typeof uni.setStorageSync === 'function') {
    uni.setStorageSync(ACCESS_TOKEN_KEY, token)
    return
  }
  if (typeof localStorage !== 'undefined') localStorage.setItem(ACCESS_TOKEN_KEY, token)
}

async function platformLoginCode() {
  // H5 is a local preview surface; WeChat's uni.login provider is unavailable there.
  if (typeof window !== 'undefined') return `h5-dev-${getClientId()}`
  if (typeof uni !== 'undefined' && typeof uni.login === 'function') {
    return new Promise<string>((resolve, reject) => {
      uni.login({
        provider: 'weixin',
        success: (result) => result.code ? resolve(result.code) : reject(new Error('微信登录未返回有效凭证')),
        fail: () => reject(new Error('微信登录失败，请检查网络后重试'))
      })
    })
  }
  return `h5-dev-${getClientId()}`
}

async function requestUserToken() {
  const code = await platformLoginCode()
  const url = `${API_BASE_URL}/auth/wechat`
  const payload = { code }
  if (typeof uni !== 'undefined' && typeof uni.request === 'function') {
    return new Promise<string>((resolve, reject) => {
      uni.request({
        url,
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        data: payload,
        success: (response) => {
          if ((response.statusCode || 0) < 200 || (response.statusCode || 0) >= 300) {
            reject(new Error('登录状态初始化失败'))
            return
          }
          const token = String((response.data as { access_token?: string })?.access_token || '')
          token ? resolve(token) : reject(new Error('登录响应缺少访问凭证'))
        },
        fail: () => reject(new Error('无法连接登录服务'))
      })
    })
  }
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!response.ok) throw new Error('登录状态初始化失败')
  const body = await response.json() as { access_token?: string }
  if (!body.access_token) throw new Error('登录响应缺少访问凭证')
  return body.access_token
}

export async function getAccessToken(forceRefresh = false) {
  if (!forceRefresh) {
    const stored = getStoredToken()
    if (stored) return stored
  }
  if (!loginPromise) {
    loginPromise = requestUserToken()
      .then((token) => {
        storeToken(token)
        return token
      })
      .finally(() => {
        loginPromise = undefined
      })
  }
  return loginPromise
}

function readableError(data: unknown, statusCode: number) {
  if (typeof data === 'string' && data.trim()) return data
  const payload = data as { error?: { message?: string }; detail?: { message?: string } | string }
  if (payload?.error?.message) return payload.error.message
  if (typeof payload?.detail === 'string') return payload.detail
  if (payload?.detail?.message) return payload.detail.message
  return `请求失败（${statusCode}）`
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
  const accessToken = path === '/auth/wechat' ? '' : await getAccessToken()
  const headers = {
    'Content-Type': 'application/json',
    'X-Client-Id': getClientId(),
    ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
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
            reject(new Error(readableError(response.data, statusCode)))
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
    const text = await response.text()
    let body: unknown = text
    try { body = JSON.parse(text) } catch { /* Keep server text. */ }
    throw new Error(readableError(body, response.status))
  }
  return response.json() as Promise<T>
}
