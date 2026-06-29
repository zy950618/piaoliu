import type { MeStatus, QuotaType, UserProfile } from '@/types/domain'
import { requestJson } from '@/services/http'

type UserProfileDto = {
  id: string
  nickname: string
  avatar_text: string
  avatar_url?: string
  platform: 'wechat' | 'ios' | 'android' | 'h5'
  is_vip: boolean
  vip_level: 'none' | 'monthly' | 'season' | 'yearly'
  vip_expires_at?: string
  drift_coins: number
  gender?: 'female' | 'male' | 'unknown'
  age_range?: string
  city?: string
  face_verified?: boolean
  gender_verified?: boolean
  charm_value?: number
}

type QuotaItemDto = {
  type: QuotaType
  label: string
  base: number
  vip_bonus: number
  ad_bonus: number
  used: number
  remaining: number
}

type MeStatusDto = {
  user: UserProfileDto
  quotas: Record<QuotaType, QuotaItemDto>
  ad_reward: {
    can_watch: boolean
    cooldown_seconds: number
    cooldown_minutes: number
    reward_per_quota: number
    active_session_id?: string
  }
  checkin: {
    checked_today: boolean
    streak_days: number
    week_rewards: number[]
    current_week_index: number
    last_reward?: number
  }
}

function toMeStatus(dto: MeStatusDto): MeStatus {
  const quotas = Object.fromEntries(
    Object.entries(dto.quotas).map(([key, quota]) => [
      key,
      {
        type: quota.type,
        label: quota.label,
        base: quota.base,
        vipBonus: quota.vip_bonus,
        adBonus: quota.ad_bonus,
        used: quota.used,
        remaining: quota.remaining
      }
    ])
  ) as MeStatus['quotas']

  return {
    user: {
      id: dto.user.id,
      nickname: dto.user.nickname,
      avatarText: dto.user.avatar_text,
      avatarUrl: dto.user.avatar_url,
      platform: dto.user.platform,
      isVip: dto.user.is_vip,
      vipLevel: dto.user.vip_level,
      vipExpiresAt: dto.user.vip_expires_at,
      driftCoins: dto.user.drift_coins,
      gender: dto.user.gender,
      ageRange: dto.user.age_range,
      city: dto.user.city,
      faceVerified: dto.user.face_verified,
      genderVerified: dto.user.gender_verified,
      charmValue: dto.user.charm_value
    },
    quotas,
    adReward: {
      canWatch: dto.ad_reward.can_watch,
      cooldownSeconds: dto.ad_reward.cooldown_seconds,
      cooldownMinutes: dto.ad_reward.cooldown_minutes,
      rewardPerQuota: dto.ad_reward.reward_per_quota,
      activeSessionId: dto.ad_reward.active_session_id
    },
    checkin: {
      checkedToday: dto.checkin.checked_today,
      streakDays: dto.checkin.streak_days,
      weekRewards: dto.checkin.week_rewards,
      currentWeekIndex: dto.checkin.current_week_index,
      lastReward: dto.checkin.last_reward
    }
  }
}

function toUserProfile(dto: UserProfileDto): UserProfile {
  return {
    id: dto.id,
    nickname: dto.nickname,
    avatarText: dto.avatar_text,
    avatarUrl: dto.avatar_url,
    platform: dto.platform,
    isVip: dto.is_vip,
    vipLevel: dto.vip_level,
    vipExpiresAt: dto.vip_expires_at,
    driftCoins: dto.drift_coins,
    gender: dto.gender,
    ageRange: dto.age_range,
    city: dto.city,
    faceVerified: dto.face_verified,
    genderVerified: dto.gender_verified,
    charmValue: dto.charm_value
  }
}

export const meApi = {
  async getStatus() {
    return toMeStatus(await requestJson<MeStatusDto>('/me/status'))
  },

  async updateProfile(patch: Partial<Omit<Pick<UserProfile, 'avatarText' | 'avatarUrl' | 'nickname' | 'gender' | 'city' | 'ageRange'>, 'avatarUrl'>> & { avatarUrl?: string | null }) {
    return toUserProfile(await requestJson<UserProfileDto>('/me/profile', {
      method: 'POST',
      body: JSON.stringify({
        nickname: patch.nickname,
        avatar_text: patch.avatarText,
        avatar_url: patch.avatarUrl,
        gender: patch.gender,
        city: patch.city,
        age_range: patch.ageRange
      })
    }))
  },

  async checkin() {
    const result = await requestJson<MeStatusDto['checkin']>('/checkin', { method: 'POST' })
    const status = await this.getStatus()
    return {
      ...result,
      checkedToday: result.checked_today,
      streakDays: result.streak_days,
      weekRewards: result.week_rewards,
      currentWeekIndex: result.current_week_index,
      lastReward: result.last_reward,
      user: status.user
    }
  },

  async prepareAdReward() {
    const result = await requestJson<{ reward_session_id: string; reward_per_quota: number }>('/ads/reward/prepare', { method: 'POST' })
    return { sessionId: result.reward_session_id, rewardPerQuota: result.reward_per_quota }
  },

  async commitAdReward(sessionId: string, completed: boolean) {
    return toMeStatus(await requestJson<MeStatusDto>('/ads/reward/commit', {
      method: 'POST',
      body: JSON.stringify({ reward_session_id: sessionId, completed })
    }))
  }
}
