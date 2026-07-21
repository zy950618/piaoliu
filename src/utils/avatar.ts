export const systemAvatarSeeds = [
  'bottle-wave-01',
  'bottle-wave-02',
  'bottle-wave-03',
  'bottle-wave-04',
  'bottle-wave-05',
  'bottle-wave-06',
  'bottle-wave-07',
  'bottle-wave-08',
  'bottle-wave-09',
  'bottle-wave-10',
  'bottle-wave-11',
  'bottle-wave-12',
  'bottle-wave-13',
  'bottle-wave-14',
  'bottle-wave-15',
  'bottle-wave-16',
  'bottle-wave-17',
  'bottle-wave-18',
  'bottle-wave-19',
  'bottle-wave-20',
  'bottle-wave-21',
  'bottle-wave-22',
  'bottle-wave-23',
  'bottle-wave-24',
  'bottle-wave-25',
  'bottle-wave-26',
  'bottle-wave-27',
  'bottle-wave-28',
  'bottle-wave-29',
  'bottle-wave-30'
]

export function systemAvatarUrl(seed: string) {
  const normalized = stableSeed(seed)
  return `https://api.dicebear.com/9.x/open-peeps/svg?seed=${encodeURIComponent(normalized)}&backgroundColor=b6e3f4,c0aede,d1d4f9`
}

export function resolveAvatarUrl(explicitUrl: string | null | undefined, seed: string) {
  return explicitUrl || systemAvatarUrl(seed)
}

function stableSeed(value: string) {
  const source = value || 'anonymous'
  let hash = 0
  for (const char of source) {
    hash = ((hash << 5) - hash + char.charCodeAt(0)) | 0
  }
  const index = Math.abs(hash) % systemAvatarSeeds.length
  return systemAvatarSeeds[index] || systemAvatarSeeds[0] || 'bottle-wave-01'
}
