import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import type { AdRewardState, CheckinState, QuotaItem, QuotaType, UserProfile } from '@/types/domain'
import { quotaOrder } from '@/constants/product'
import { meApi } from '@/services/meApi'
import { playRewardVideoAd } from '@/services/rewardVideoAd'
import { formatCountdown } from '@/utils/time'

export const useAppStore = defineStore('app', () => {
  const loading = ref(false)
  const user = ref<UserProfile>()
  const quotas = ref<Record<QuotaType, QuotaItem>>()
  const adReward = ref<AdRewardState>()
  const checkin = ref<CheckinState>()
  const hydrated = ref(false)
  let hydrateTask: Promise<void> | undefined

  const quotaList = computed(() => {
    if (!quotas.value) return []
    return quotaOrder.map((type) => quotas.value![type])
  })

  const adCountdownText = computed(() => {
    if (!adReward.value) return ''
    if (adReward.value.canWatch) return '现在可看广告'
    return `${formatCountdown(adReward.value.cooldownSeconds)} 后可再次观看`
  })

  const nextCheckinReward = computed(() => {
    if (!checkin.value) return 0
    return checkin.value.weekRewards[checkin.value.currentWeekIndex] ?? 0
  })

  async function hydrate() {
    if (hydrated.value) return
    if (hydrateTask) return hydrateTask
    loading.value = true
    hydrateTask = (async () => {
      const status = await loadStatus()
      user.value = status.user
      quotas.value = status.quotas
      adReward.value = status.adReward
      checkin.value = status.checkin
      hydrated.value = true
    })().finally(() => {
      loading.value = false
      hydrateTask = undefined
    })
    return hydrateTask
  }

  async function runCheckin() {
    const result = await meApi.checkin()
    checkin.value = {
      checkedToday: result.checkedToday,
      streakDays: result.streakDays,
      weekRewards: [...result.weekRewards],
      currentWeekIndex: result.currentWeekIndex,
      lastReward: result.lastReward
    }
    user.value = result.user
    hydrated.value = true
    return result
  }

  async function watchRewardAd(completed = true) {
    const prepared = await meApi.prepareAdReward()
    const watched = completed ? await playRewardVideoAd(prepared.countdownSeconds) : false
    const status = await commitRewardAd(prepared.sessionId, watched)
    return status
  }

  async function prepareRewardAd() {
    return meApi.prepareAdReward()
  }

  async function commitRewardAd(sessionId: string, completed: boolean) {
    const status = await meApi.commitAdReward(sessionId, completed)
    user.value = status.user
    quotas.value = status.quotas
    adReward.value = status.adReward
    checkin.value = status.checkin
    hydrated.value = true
    return status
  }

  async function tickAdCooldown(seconds = 1) {
    void seconds
    adReward.value = (await meApi.getStatus()).adReward
  }

  async function refreshStatus() {
    const status = await loadStatus()
    user.value = status.user
    quotas.value = status.quotas
    adReward.value = status.adReward
    checkin.value = status.checkin
    hydrated.value = true
  }

  function updateUserProfile(patch: Partial<Pick<UserProfile, 'avatarText' | 'avatarUrl' | 'nickname'>>) {
    if (!user.value) return
    user.value = {
      ...user.value,
      ...patch
    }
  }

  function applyUserProfile(profile: UserProfile) {
    user.value = profile
    hydrated.value = true
  }

  async function saveUserProfile(patch: Partial<Omit<Pick<UserProfile, 'avatarText' | 'avatarUrl' | 'nickname' | 'gender' | 'city' | 'ageRange'>, 'avatarUrl'>> & { avatarUrl?: string | null }) {
    user.value = await meApi.updateProfile(patch)
    hydrated.value = true
    return user.value
  }

  async function loadStatus() {
    return meApi.getStatus()
  }

  return {
    loading,
    user,
    quotas,
    quotaList,
    adReward,
    checkin,
    adCountdownText,
    nextCheckinReward,
    hydrate,
    refreshStatus,
    updateUserProfile,
    applyUserProfile,
    saveUserProfile,
    runCheckin,
    prepareRewardAd,
    commitRewardAd,
    watchRewardAd,
    tickAdCooldown
  }
})
