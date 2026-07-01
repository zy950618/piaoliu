export async function playRewardVideoAd(countdownSeconds = 1): Promise<boolean> {
  // Future ad SDK integration point: resolve true only after the rewarded video is completed.
  await new Promise((resolve) => setTimeout(resolve, Math.max(1, countdownSeconds) * 1000))
  return true
}
