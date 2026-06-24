import type { QuotaType } from '@/types/domain'
import { quotaFullLabels } from '@/constants/product'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'

export function useQuotaGuard() {
  const app = useAppStore()

  function ensureQuota(type: QuotaType): boolean {
    const quota = app.quotas?.[type]
    if (!quota || quota.remaining <= 0) {
      const label = quotaFullLabels[type]
      showToast(`${label}次数不足，可看广告、签到或开通 VIP`)
      return false
    }
    return true
  }

  return { ensureQuota }
}
