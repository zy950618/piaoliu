export async function playRewardVideoAd(): Promise<boolean> {
  // Future ad SDK integration point: resolve true only after the rewarded video is completed.
  await new Promise((resolve) => setTimeout(resolve, 450))
  return true
}
