import type { QuotaType } from '@/types/domain'

export const quotaLabels: Record<QuotaType, string> = {
  fish_bottle: '捞瓶',
  throw_bottle: '扔瓶',
  truth: '真心话',
  dare: '大冒险',
  treehole_post: '历史留言'
}

export const quotaFullLabels: Record<QuotaType, string> = {
  fish_bottle: '捞瓶子',
  throw_bottle: '扔瓶子',
  truth: '真心话',
  dare: '大冒险',
  treehole_post: '历史留言'
}

export const defaultBaseQuotas: Record<QuotaType, number> = {
  fish_bottle: 5,
  throw_bottle: 3,
  truth: 3,
  dare: 3,
  treehole_post: 2
}

export const defaultVipBonus: Record<QuotaType, number> = {
  fish_bottle: 5,
  throw_bottle: 3,
  truth: 3,
  dare: 3,
  treehole_post: 2
}

export const weeklyCheckinRewards = [10, 10, 30, 10, 10, 30, 100]

export const quotaOrder: QuotaType[] = [
  'fish_bottle',
  'throw_bottle',
  'truth',
  'dare',
  'treehole_post'
]

export const primaryCityOptions = ['全国', '北京', '上海', '广州', '深圳', '全部']

export const expandedCityOptions = [
  '杭州',
  '成都',
  '重庆',
  '武汉',
  '南京',
  '苏州',
  '西安',
  '厦门',
  '三亚',
  '长沙',
  '郑州',
  '天津',
  '青岛',
  '宁波',
  '福州',
  '合肥'
]
