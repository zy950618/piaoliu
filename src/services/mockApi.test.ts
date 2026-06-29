import { describe, expect, it } from 'vitest'
import { mockApi } from './mockApi'

describe('mockApi product rules', () => {
  it('returns weekly checkin rewards', async () => {
    const status = await mockApi.getMeStatus()
    expect(status.checkin.weekRewards).toEqual([10, 10, 30, 10, 10, 30, 100])
  })

  it('adds video reward coins and quota to all quota types after completed ad', async () => {
    const before = await mockApi.getMeStatus()
    const beforeWallet = await mockApi.getWallet()
    const prepared = await mockApi.prepareAdReward()
    const after = await mockApi.commitAdReward(prepared.sessionId, true)
    const afterWallet = await mockApi.getWallet()
    expect(after.quotas.fish_bottle.remaining).toBe(before.quotas.fish_bottle.remaining + prepared.rewardPerQuota)
    expect(after.quotas.throw_bottle.remaining).toBe(before.quotas.throw_bottle.remaining + prepared.rewardPerQuota)
    expect(after.quotas.truth.remaining).toBe(before.quotas.truth.remaining + prepared.rewardPerQuota)
    expect(after.quotas.dare.remaining).toBe(before.quotas.dare.remaining + prepared.rewardPerQuota)
    expect(after.quotas.treehole_post.remaining).toBe(before.quotas.treehole_post.remaining + prepared.rewardPerQuota)
    expect(afterWallet.wallet.rechargeCoins).toBe(beforeWallet.wallet.rechargeCoins + 1)
  })

  it('keeps recharge coins separate from withdrawable earned coins', async () => {
    const result = await mockApi.getWallet()
    expect(result.wallet.rechargeCoins).toBeGreaterThan(0)
    expect(result.wallet.withdrawableCoins).toBeLessThanOrEqual(result.wallet.earnedCoins)
    expect(result.wallet.charmValue).toBeGreaterThanOrEqual(result.wallet.withdrawThresholdCharm)
  })

  it('exposes plaza, nearby, and verification mock contracts', async () => {
    const verification = await mockApi.getVerification()
    const plaza = await mockApi.listPlazaPosts()
    const nearby = await mockApi.listNearbyUsers()
    expect(verification.verification.genderVerified).toBe(true)
    expect(plaza.length).toBeGreaterThan(0)
    expect(nearby.length).toBeGreaterThan(0)
  })

  it('publishes plaza posts to the top and rejects empty content', async () => {
    const before = await mockApi.listPlazaPosts()
    await expect(mockApi.publishPlazaPost('   ')).rejects.toThrow('EMPTY_PLAZA_CONTENT')
    const plainPost = await mockApi.publishPlazaPost('今天只发布一条纯文字动态。')
    expect(plainPost.mediaType).toBe('text')
    expect(plainPost.mediaCount).toBe(0)
    const post = await mockApi.publishPlazaPost('今天在广场留一条新的动态。', { mediaType: 'image', mediaCount: 2 })
    const after = await mockApi.listPlazaPosts()
    expect(post.content).toBe('今天在广场留一条新的动态。')
    expect(post.mediaType).toBe('image')
    expect(post.mediaCount).toBe(2)
    expect(post.viewCount).toBe(0)
    expect(after[0]?.id).toBe(post.id)
    expect(after[1]?.id).toBe(plainPost.id)
    expect(after.length).toBe(before.length + 2)
  })

  it('supports video plaza posts in mock contracts', async () => {
    const posts = await mockApi.listPlazaPosts()
    expect(posts.some((post) => post.mediaType === 'video')).toBe(true)
    const post = await mockApi.publishPlazaPost('发布一条视频动态。', { mediaType: 'video', mediaCount: 1 })
    expect(post.mediaType).toBe('video')
    expect(post.mediaCount).toBe(1)
  })

  it('comments plaza posts through the mock interface', async () => {
    const posts = await mockApi.listPlazaPosts()
    const before = posts[0]
    expect(before).toBeTruthy()
    if (!before) return
    const after = await mockApi.commentPlazaPost(before.id, '这条动态我也有同感。')
    expect(after.commentCount).toBe(before.commentCount + 1)
    expect(after.commentPreview).toBe('这条动态我也有同感。')
    await expect(mockApi.commentPlazaPost(before.id, '   ')).rejects.toThrow('EMPTY_PLAZA_COMMENT')
  })

  it('likes plaza posts through the mock interface', async () => {
    const posts = await mockApi.listPlazaPosts()
    const before = posts[0]
    expect(before).toBeTruthy()
    if (!before) return
    const after = await mockApi.likePlazaPost(before.id)
    expect(after.likeCount).toBe(before.likeCount + 1)
  })

  it('exposes nearby age and distance fields for filters', async () => {
    const nearby = await mockApi.listNearbyUsers()
    expect(nearby[0]?.ageRange).toBeTruthy()
    expect(nearby[0]?.distanceKm).toBeGreaterThan(0)
  })

  it('keeps bottle replies in conversation history', async () => {
    const before = await mockApi.listConversationThreads()
    await mockApi.replyBottle('bottle_001', '今晚的海风收到了。')
    const after = await mockApi.listConversationThreads()
    const thread = after.find((item) => item.bottleId === 'bottle_001')
    const lastTurn = thread?.turns[thread.turns.length - 1]
    expect(before.length).toBeGreaterThan(0)
    expect(thread?.lastMessage).toBe('今晚的海风收到了。')
    expect(lastTurn?.body).toBe('今晚的海风收到了。')
  })

  it('filters fished bottles by current user city gender and age', async () => {
    const bottle = await mockApi.fishBottle({ city: '同城', gender: '女', ageRange: '18-24' })
    expect(bottle.authorCity).toBe('杭州')
    expect(bottle.authorGender).toBe('female')
    expect(bottle.authorAgeRange).toBe('18-24')
  })

  it('does not consume fish quota when no bottle matches filters', async () => {
    const before = await mockApi.getMeStatus()
    await expect(mockApi.fishBottle({ city: '同城', gender: '女', ageRange: '37+' })).rejects.toThrow('NO_MATCHED_BOTTLE')
    const after = await mockApi.getMeStatus()
    expect(after.quotas.fish_bottle.remaining).toBe(before.quotas.fish_bottle.remaining)
  })

  it('stores throw scope instead of manual target city', async () => {
    const bottle = await mockApi.throwBottle('今晚把这句话交给同城的人。', {
      targetGender: 'female',
      targetScope: 'same_city'
    })
    expect(bottle.authorCity).toBe('杭州')
    expect(bottle.targetGender).toBe('female')
    expect(bottle.targetScope).toBe('same_city')
  })

  it('returns a random bottle prompt from the mock prompt pool', async () => {
    const prompt = await mockApi.getRandomBottlePrompt()
    expect(prompt.trim().length).toBeGreaterThan(0)
  })

  it('does not consume throw quota for empty bottle content', async () => {
    const before = await mockApi.getMeStatus()
    await expect(mockApi.throwBottle('   ')).rejects.toThrow('EMPTY_BOTTLE_CONTENT')
    const after = await mockApi.getMeStatus()
    expect(after.quotas.throw_bottle.remaining).toBe(before.quotas.throw_bottle.remaining)
  })
})
