export type AppIconName =
  | 'bottle'
  | 'treehole'
  | 'plaza'
  | 'nearby'
  | 'wallet'
  | 'verify'
  | 'gift'
  | 'blacklist'
  | 'vip'
  | 'message'
  | 'follow'
  | 'friend'

export const appIconText: Record<AppIconName, string> = {
  bottle: '瓶',
  treehole: '留',
  plaza: '广',
  nearby: '近',
  wallet: '金',
  verify: '证',
  gift: '礼',
  blacklist: '黑',
  vip: '会',
  message: '信',
  follow: '关',
  friend: '友'
}
