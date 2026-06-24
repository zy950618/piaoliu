<template>
  <view class="page plaza-page safe-bottom">
    <view class="top-filter">
      <ExploreFilters v-model="filters" mode="chips" city-label="城市" :city-options="cityOptions" age-mode="range" />
    </view>

    <view class="section topic-row">
      <view
        v-for="tab in feedTabs"
        :key="tab.value"
        class="topic-pill"
        :class="{ active: activeFeed === tab.value }"
        @tap="activeFeed = tab.value"
      >
        {{ tab.label }}
      </view>
    </view>

    <view class="section location-card">
      <view>
        <text class="h2">附近的人</text>
        <text class="muted">开启定位后展示同城和附近用户动态。</text>
      </view>
      <view class="button secondary location-button" @tap="go('/pages/nearby/index')">开启</view>
    </view>

    <view class="section">
      <view v-for="post in filteredPosts" :key="post.id" class="panel plaza-card">
        <view class="between">
          <view class="row author-row">
            <view class="author-icon">{{ post.iconText }}</view>
            <view>
              <text class="h2">{{ post.authorName }}</text>
              <text class="muted">{{ post.topic }} · {{ post.city }} · {{ post.ageRange }} · {{ post.distanceText }}</text>
            </view>
          </view>
          <view class="row tag-row">
            <text class="tag vip-tag">{{ post.gender === 'female' ? '女' : post.gender === 'male' ? '男' : '未知' }}</text>
          </view>
        </view>
        <text class="body post-content">{{ post.content }}</text>
        <view v-if="post.media?.length" class="media-preview" :class="`media-${post.mediaType || 'text'}`">
          <template v-if="post.mediaType === 'image'">
            <view class="media-grid" :class="imageGridClass(post.media?.length || 0)">
              <image
                v-for="media in post.media.slice(0, 9)"
                :key="media.id"
                class="media-image"
                :src="media.url"
                mode="aspectFill"
              />
            </view>
          </template>
          <template v-else-if="post.mediaType === 'video'">
            <video
              v-for="media in post.media.slice(0, 1)"
              :key="media.id"
              class="media-video"
              :src="media.url"
              controls
            />
          </template>
          <template v-else-if="post.mediaType === 'voice'">
            <view v-for="media in post.media.slice(0, 1)" :key="media.id" class="voice-card">
              <view class="voice-icon">声</view>
              <view class="voice-body">
                <text class="voice-title">语音动态</text>
                <text class="voice-meta">{{ media.durationSeconds || 0 }} 秒</text>
                <view class="voice-wave" :class="{ active: playingVoiceUrl === media.url }">
                  <view v-for="bar in 5" :key="bar" class="voice-wave-bar" />
                </view>
              </view>
              <view
                class="voice-player"
                :class="{ playing: playingVoiceUrl === media.url }"
                @tap="toggleVoice(media.url)"
              >
                <view class="voice-play-icon" />
                <view class="voice-stop-icon" />
              </view>
            </view>
          </template>
        </view>
        <view class="engagement-row">
          <view class="stats-row">
            <view class="stat-item">
              <text class="stat-number">{{ post.viewCount || 0 }}</text>
              <text class="stat-label">浏览</text>
            </view>
            <view class="stat-item">
              <text class="stat-number">{{ post.likeCount }}</text>
              <text class="stat-label">点赞</text>
            </view>
            <view class="stat-item comment-stat" @tap="openCommentPage(post.id)">
              <text class="stat-number">{{ post.commentCount }}</text>
              <text class="stat-label">留言</text>
            </view>
          </view>
          <view class="row action-row">
            <view
              class="button secondary mini-button like-button"
              :class="{ liked: post.likedByMe, bump: likeEffects[post.id] }"
              @tap="likePost(post)"
            >
              <text class="thumb-icon">👍</text>
              <text>{{ post.likedByMe ? '已赞' : '点赞' }}</text>
              <text v-if="likeEffects[post.id]" class="like-float">{{ likeEffects[post.id] }}</text>
            </view>
            <view class="button ghost mini-button" @tap="openComment(post.id)">留言</view>
          </view>
        </view>
        <view v-if="post.commentPreview" class="comment-footer">
          <text v-if="post.commentPreview" class="comment-preview">最新留言：{{ post.commentPreview }}</text>
        </view>
      </view>
    </view>

    <view class="publish-fab" @tap="openComposer">+</view>

    <view v-if="composerOpen" class="modal-mask center-mask" @tap="closeComposer">
      <view class="modal-card composer-card" @tap.stop @click.stop>
        <view class="composer-top">
          <view>
            <text class="h2">发布动态</text>
            <text class="muted">广场内容公开展示，可发布图文、声音或视频。</text>
          </view>
          <view class="composer-avatar">{{ app.user?.avatarText || '海' }}</view>
        </view>
        <textarea
          v-model="draftPost"
          class="composer-input"
          maxlength="180"
          placeholder="写一句今天想公开分享的话。"
          @input="clearPostError"
        />
        <text v-if="postError" class="post-error">{{ postError }}</text>
        <view class="media-row">
          <view
            v-for="type in mediaTypes"
            :key="type.value"
            class="media-option"
            :class="{ active: mediaType === type.value }"
            @tap="mediaType = type.value"
            @click="mediaType = type.value"
          >
            {{ type.label }}
          </view>
        </view>
        <view class="modal-actions">
          <view class="button ghost" @tap="closeComposer">取消</view>
          <view class="button publish-button" :class="{ disabled: content.submitting || !draftPost.trim() }" @tap="publishPost">
            发布
          </view>
        </view>
      </view>
    </view>

    <view v-if="commentOpen" class="modal-mask center-mask">
      <view class="modal-card comment-modal-card" @tap.stop @click.stop>
        <textarea
          v-model="commentDraft"
          class="composer-input comment-input"
          maxlength="120"
          placeholder="写一句友善留言。"
          @input="clearCommentError"
        />
        <view class="private-comment-toggle" @tap.stop="togglePrivateComment">
          <view class="check-box" :class="{ checked: privateComment }">{{ privateComment ? '✓' : '' }}</view>
          <view>
            <text class="private-title">隐藏，仅主人查看</text>
            <text class="private-desc">勾选后，只有你和动态发布者能看到这条留言。</text>
          </view>
        </view>
        <text v-if="commentError" class="post-error">{{ commentError }}</text>
        <view class="modal-actions">
          <view class="button ghost" @tap="closeComment">取消</view>
          <view class="button publish-button" :class="{ disabled: commentSubmitting || !commentDraft.trim() }" @tap="submitComment">
            发送
          </view>
        </view>
      </view>
    </view>

  </view>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import ExploreFilters, { type ExploreFilterValue } from '@/components/ExploreFilters.vue'
import { navigateTo, showToast, switchTab } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { PlazaPost } from '@/types/domain'

const app = useAppStore()
const content = useContentStore()
const filters = ref<ExploreFilterValue>({ city: '全国', gender: '全部', ageRange: '全部' })
const composerOpen = ref(false)
const commentOpen = ref(false)
const activeCommentPostId = ref('')
const draftPost = ref('')
const commentDraft = ref('')
const privateComment = ref(false)
const postError = ref('')
const commentError = ref('')
const lastLikeAction = ref<{ postId: string; at: number }>({ postId: '', at: 0 })
const likeEffects = ref<Record<string, string>>({})
const commentSubmitting = ref(false)
let filterReloadTimer: ReturnType<typeof setTimeout> | undefined
let voicePlayer: ReturnType<typeof uni.createInnerAudioContext> | undefined
let lastPrivateToggleAt = 0
const likeEffectTimers: Record<string, ReturnType<typeof setTimeout>> = {}
const playingVoiceUrl = ref('')
type PlazaMediaType = NonNullable<PlazaPost['mediaType']>
type FeedTab = 'nearby' | 'gift' | 'newcomer'

const mediaType = ref<PlazaMediaType>('image')
const cityOptions = ['全国', '北京', '上海', '广州', '深圳', '杭州', '成都', '厦门']
const activeFeed = ref<FeedTab>('nearby')
const feedTabs: Array<{ label: string; value: FeedTab }> = [
  { label: '附近动态', value: 'nearby' },
  { label: '礼物榜', value: 'gift' },
  { label: '新人推荐榜', value: 'newcomer' }
]
const mediaTypes: Array<{ label: string; value: PlazaMediaType }> = [
  { label: '图文', value: 'image' },
  { label: '声音', value: 'voice' },
  { label: '视频', value: 'video' }
]

const filteredPosts = computed(() => {
  const filtered = content.plazaPosts.filter((post) => {
    if (filters.value.city !== '全国' && post.city !== filters.value.city) return false
    if (filters.value.gender === '女' && post.gender !== 'female') return false
    if (filters.value.gender === '男' && post.gender !== 'male') return false
    if (!ageRangeMatches(post.ageRange, filters.value.ageRange)) return false
    return true
  })
  if (activeFeed.value === 'gift') {
    return [...filtered].sort((a, b) => b.likeCount - a.likeCount)
  }
  if (activeFeed.value === 'newcomer') {
    return filtered.filter((post) => (post.viewCount || 0) <= 600)
  }
  return filtered
})
onLoad(() => {
  app.hydrate()
  loadPlazaPostsWithFilters()
})

watch(
  filters,
  () => {
    if (filterReloadTimer) clearTimeout(filterReloadTimer)
    filterReloadTimer = setTimeout(loadPlazaPostsWithFilters, 160)
  },
  { deep: true }
)

function loadPlazaPostsWithFilters() {
  return content.loadPlazaPosts({
    city: filters.value.city,
    gender: filters.value.gender,
    ageRange: filters.value.ageRange
  })
}

function go(url: string) {
  if (url === '/pages/plaza/index' || url === '/pages/bottle/index' || url === '/pages/treehole/index') {
    switchTab(url)
    return
  }
  navigateTo(url)
}

async function publishPost() {
  if (!draftPost.value.trim()) {
    postError.value = '先写一点内容，才能发布'
    showToast('先写一点内容，才能发布')
    return
  }
  await content.publishPlazaPost(draftPost.value.trim(), {
    mediaType: mediaType.value,
    mediaCount: 1
  })
  draftPost.value = ''
  postError.value = ''
  mediaType.value = 'image'
  composerOpen.value = false
  showToast('动态已发布')
}

function clearPostError() {
  if (postError.value && draftPost.value.trim()) postError.value = ''
}

function openComposer() {
  composerOpen.value = true
}

function closeComposer() {
  composerOpen.value = false
  draftPost.value = ''
  postError.value = ''
  mediaType.value = 'image'
}

function openComment(postId: string) {
  activeCommentPostId.value = postId
  commentDraft.value = ''
  commentError.value = ''
  privateComment.value = false
  commentOpen.value = true
}

function closeComment() {
  commentOpen.value = false
  activeCommentPostId.value = ''
  commentDraft.value = ''
  privateComment.value = false
  commentError.value = ''
  commentSubmitting.value = false
}

function togglePrivateComment() {
  const now = Date.now()
  if (now - lastPrivateToggleAt < 120) return
  lastPrivateToggleAt = now
  privateComment.value = !privateComment.value
}

async function submitComment() {
  if (commentSubmitting.value) return
  if (!commentDraft.value.trim()) {
    commentError.value = '先写一点内容，才能发送'
    showToast('先写一点内容，才能发送')
    return
  }
  commentSubmitting.value = true
  try {
    await content.commentPlazaPost(activeCommentPostId.value, commentDraft.value.trim(), {
      hiddenForOwnerOnly: privateComment.value
    })
    closeComment()
    showToast('留言已发送')
  } catch {
    commentError.value = '留言发送失败，请稍后再试'
  } finally {
    commentSubmitting.value = false
  }
}

function clearCommentError() {
  if (commentError.value && commentDraft.value.trim()) commentError.value = ''
}

function ageRangeMatches(postAgeRange?: string, selectedAgeRange = '全部') {
  if (selectedAgeRange === '全部') return true
  const selected = parseAgeRange(selectedAgeRange)
  const post = parseAgeRange(postAgeRange || '')
  if (!selected || !post) return false
  return post.max >= selected.min && post.min <= selected.max
}

function parseAgeRange(value: string) {
  if (!value || value === '全部') return null
  const normalized = value.replace('+', '-80')
  const [minText, maxText] = normalized.split('-')
  const min = Number(minText)
  const max = Number(maxText)
  if (!Number.isFinite(min) || !Number.isFinite(max)) return null
  return { min: Math.min(min, max), max: Math.max(min, max) }
}

function imageGridClass(count: number) {
  return `count-${Math.min(Math.max(count, 1), 9)}`
}

async function likePost(post: PlazaPost) {
  const postId = post.id
  const now = Date.now()
  if (lastLikeAction.value.postId === postId && now - lastLikeAction.value.at < 120) return
  lastLikeAction.value = { postId, at: now }
  try {
    const updatedPost = await content.likePlazaPost(postId)
    showLikeEffect(postId, updatedPost.likedByMe ? '+1' : '-1')
  } catch {
    showToast('点赞失败，请稍后再试')
  }
}

function showLikeEffect(postId: string, value: string) {
  likeEffects.value = { ...likeEffects.value, [postId]: value }
  if (likeEffectTimers[postId]) clearTimeout(likeEffectTimers[postId])
  likeEffectTimers[postId] = setTimeout(() => {
    const nextEffects = { ...likeEffects.value }
    delete nextEffects[postId]
    likeEffects.value = nextEffects
  }, 760)
}

function openCommentPage(postId: string) {
  navigateTo(`/pages/plaza/comments?postId=${postId}`)
}

function toggleVoice(url: string) {
  if (playingVoiceUrl.value === url) {
    stopVoice()
    return
  }
  stopVoice()
  voicePlayer = uni.createInnerAudioContext()
  voicePlayer.src = url
  voicePlayer.onEnded(stopVoice)
  voicePlayer.onError(() => {
    showToast('语音播放失败，请稍后再试')
    stopVoice()
  })
  playingVoiceUrl.value = url
  voicePlayer.play()
}

function stopVoice() {
  voicePlayer?.stop()
  voicePlayer?.destroy()
  voicePlayer = undefined
  playingVoiceUrl.value = ''
}
</script>

<style scoped lang="scss">
.plaza-page {
  position: relative;
  background:
    radial-gradient(circle at 84% -4%, rgba(191, 91, 115, 0.12), transparent 30%),
    linear-gradient(180deg, #fbfcfa, #eef3f1);
}

.top-filter {
  margin-top: 0;
}

.topic-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12rpx;
  padding-bottom: 4rpx;
}

.topic-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  border-radius: 999px;
  padding: 12rpx 10rpx;
  color: #234b5d;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(35, 108, 114, 0.1);
  font-size: 24rpx;
  font-weight: 800;
  text-align: center;
  white-space: nowrap;
}

.topic-pill.active {
  color: #fff;
  border-color: rgba(35, 108, 114, 0.18);
  background: linear-gradient(180deg, #2f7f6d, #236c72);
  box-shadow: 0 12rpx 26rpx rgba(35, 108, 114, 0.14);
}

.location-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  border: 1px solid rgba(35, 108, 114, 0.12);
  border-radius: 8px;
  padding: 24rpx;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(242, 248, 245, 0.86)),
    radial-gradient(circle at 92% 8%, rgba(35, 108, 114, 0.1), transparent 28%);
  box-shadow: 0 18rpx 42rpx rgba(31, 54, 58, 0.06);
}

.location-button {
  min-width: 112rpx;
  min-height: 62rpx;
  font-size: 24rpx;
}

.media-preview {
  margin: 0 0 18rpx;
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8rpx;
}

.media-grid.count-1 {
  grid-template-columns: minmax(0, 1fr);
  max-width: 440rpx;
}

.media-grid.count-2,
.media-grid.count-4 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.media-image {
  display: block;
  width: 100%;
  aspect-ratio: 1 / 1;
  height: auto;
  border-radius: 8px;
  background: rgba(35, 108, 114, 0.08);
  object-fit: cover;
}

.media-grid.count-1 .media-image {
  aspect-ratio: 4 / 3;
}

.media-video {
  display: block;
  width: 100%;
  height: 360rpx;
  overflow: hidden;
  border-radius: 8px;
  background: #101820;
}

.voice-card {
  display: grid;
  grid-template-columns: 64rpx minmax(0, 1fr) 104rpx;
  gap: 14rpx;
  align-items: center;
  border: 1px solid rgba(35, 108, 114, 0.1);
  border-radius: 8px;
  padding: 18rpx;
  background: linear-gradient(135deg, rgba(247, 250, 249, 0.96), rgba(235, 244, 241, 0.86));
}

.voice-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  color: #fff;
  background: #236c72;
  font-size: 22rpx;
  font-weight: 900;
}

.voice-body {
  min-width: 0;
}

.voice-title,
.voice-meta {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.voice-title {
  color: #172126;
  font-size: 26rpx;
  font-weight: 900;
}

.voice-meta {
  margin-top: 4rpx;
  color: #65757b;
  font-size: 22rpx;
}

.voice-wave {
  display: flex;
  align-items: flex-end;
  gap: 5rpx;
  height: 28rpx;
  margin-top: 8rpx;
  opacity: 0;
  transform: translateY(2rpx);
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.voice-wave.active {
  opacity: 1;
  transform: translateY(0);
}

.voice-wave-bar {
  width: 5rpx;
  height: 10rpx;
  border-radius: 999px;
  background: linear-gradient(180deg, #2f7f6d, #70a9a0);
  animation: voiceWave 0.76s ease-in-out infinite;
}

.voice-wave-bar:nth-child(2) {
  animation-delay: 0.08s;
}

.voice-wave-bar:nth-child(3) {
  animation-delay: 0.16s;
}

.voice-wave-bar:nth-child(4) {
  animation-delay: 0.24s;
}

.voice-wave-bar:nth-child(5) {
  animation-delay: 0.32s;
}

@keyframes voiceWave {
  0%,
  100% {
    height: 8rpx;
    opacity: 0.58;
  }

  50% {
    height: 28rpx;
    opacity: 1;
  }
}

.voice-player {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 58rpx;
  height: 58rpx;
  border: 1px solid rgba(35, 108, 114, 0.16);
  border-radius: 12rpx;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 8rpx 18rpx rgba(35, 108, 114, 0.1);
}

.voice-player:active {
  transform: scale(0.96);
}

.voice-play-icon {
  width: 0;
  height: 0;
  margin-left: 5rpx;
  border-top: 13rpx solid transparent;
  border-bottom: 13rpx solid transparent;
  border-left: 20rpx solid #236c72;
}

.voice-stop-icon {
  display: none;
  width: 22rpx;
  height: 22rpx;
  border-radius: 4rpx;
  background: #236c72;
}

.voice-player.playing .voice-play-icon {
  display: none;
}

.voice-player.playing .voice-stop-icon {
  display: block;
}

.publish-fab {
  position: fixed;
  right: 28rpx;
  bottom: calc(112px + env(safe-area-inset-bottom));
  z-index: 88;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border: 1px solid rgba(255, 255, 255, 0.86);
  border-radius: 50%;
  color: #fff;
  background:
    linear-gradient(180deg, #2f7f6d, #236c72),
    radial-gradient(circle at 50% 20%, rgba(255, 255, 255, 0.3), transparent 24px);
  box-shadow: 0 18px 38px rgba(35, 108, 114, 0.28);
  font-size: 34px;
  font-weight: 500;
  line-height: 1;
}

.modal-mask {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28rpx;
  box-sizing: border-box;
  background: rgba(0, 0, 0, 0.32);
  backdrop-filter: blur(12px);
}

.modal-card {
  width: 100%;
  max-width: 520px;
  border-radius: 24px;
  padding: 28rpx;
  background: rgba(255, 255, 255, 0.98);
  box-sizing: border-box;
  box-shadow: 0 30rpx 76rpx rgba(0, 0, 0, 0.22);
}

.composer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
}

.composer-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  color: #fff;
  background: #236c72;
  font-size: 28rpx;
  font-weight: 900;
}

.composer-input {
  width: 100%;
  min-height: 150rpx;
  margin-top: 18rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  padding: 20rpx;
  color: #172126;
  background: rgba(255, 255, 255, 0.82);
  box-sizing: border-box;
  font-size: 26rpx;
}

.comment-input {
  margin-top: 0;
}

.comment-list {
  display: grid;
  gap: 12rpx;
  max-height: 280rpx;
  margin-top: 18rpx;
  overflow-y: auto;
}

.comment-item {
  display: grid;
  grid-template-columns: 52rpx minmax(0, 1fr);
  gap: 12rpx;
  border: 1px solid rgba(35, 108, 114, 0.08);
  border-radius: 8px;
  padding: 12rpx;
  background: rgba(247, 250, 249, 0.82);
}

.comment-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 52rpx;
  height: 52rpx;
  border-radius: 50%;
  color: #fff;
  background: #236c72;
  font-size: 22rpx;
  font-weight: 900;
}

.comment-body,
.comment-author,
.comment-text,
.empty-comments {
  display: block;
}

.comment-author {
  color: #172126;
  font-size: 24rpx;
  font-weight: 900;
}

.comment-text,
.empty-comments {
  margin-top: 4rpx;
  color: #65757b;
  font-size: 24rpx;
  line-height: 1.45;
}

.empty-comments {
  border-radius: 8px;
  padding: 18rpx;
  background: rgba(35, 108, 114, 0.06);
  text-align: center;
}

.post-error {
  display: block;
  margin-top: 10rpx;
  color: #b94747;
  font-size: 24rpx;
  font-weight: 800;
}

.media-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-top: 16rpx;
}

.media-option {
  flex: 1;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 999px;
  padding: 14rpx 16rpx;
  color: #172126;
  background: rgba(29, 29, 31, 0.05);
  font-size: 24rpx;
  font-weight: 800;
  text-align: center;
}

.media-option.active {
  color: #fff;
  border-color: rgba(35, 108, 114, 0.16);
  background: #236c72;
}

.modal-actions {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  gap: 16rpx;
  margin-top: 22rpx;
}

.publish-button {
  min-width: 180rpx;
  min-height: 68rpx;
  font-size: 24rpx;
}

.button {
  gap: 10rpx;
}

.plaza-card {
  margin-bottom: 16rpx;
}

.plaza-card > .between {
  gap: 16rpx;
}

.engagement-row {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 16rpx;
  margin-top: 18rpx;
}

.stats-row {
  display: grid;
  flex: 1;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10rpx;
  min-width: 0;
}

.stat-item {
  min-width: 0;
  border: 1px solid rgba(35, 108, 114, 0.08);
  border-radius: 8px;
  padding: 10rpx 12rpx;
  background: rgba(247, 250, 249, 0.86);
}

.comment-stat {
  cursor: pointer;
}

.comment-stat:active {
  transform: scale(0.98);
}

.stat-number,
.stat-label {
  display: block;
  text-align: center;
}

.stat-number {
  color: #172126;
  font-size: 24rpx;
  font-weight: 900;
  line-height: 1.1;
}

.stat-label {
  margin-top: 4rpx;
  color: #65757b;
  font-size: 20rpx;
  font-weight: 700;
}

.plaza-card > .between:last-child .muted {
  flex: 1;
  min-width: 0;
}

.author-row,
.action-row,
.tag-row {
  gap: 12rpx;
}

.action-row {
  flex-shrink: 0;
  width: 176rpx;
}

.author-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64rpx;
  height: 64rpx;
  border-radius: 8px;
  color: #fff;
  background: #d8758b;
  font-weight: 900;
}

.author-row .h2,
.author-row .muted {
  display: block;
}

.post-content {
  display: block;
  margin: 22rpx 0;
}

.comment-preview {
  display: block;
  border-radius: 8px;
  padding: 14rpx 16rpx;
  color: #65757b;
  background: rgba(35, 108, 114, 0.07);
  font-size: 24rpx;
  line-height: 1.45;
}

.comment-footer {
  display: grid;
  gap: 12rpx;
  margin-top: 16rpx;
}

.comment-link {
  justify-self: start;
  border-radius: 999px;
  padding: 10rpx 18rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.08);
  font-size: 24rpx;
  font-weight: 900;
}

.private-comment-toggle {
  display: grid;
  grid-template-columns: 42rpx minmax(0, 1fr);
  gap: 12rpx;
  align-items: start;
  margin-top: 16rpx;
  border-radius: 8px;
  padding: 14rpx;
  background: rgba(35, 108, 114, 0.06);
}

.check-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34rpx;
  height: 34rpx;
  border: 2rpx solid rgba(35, 108, 114, 0.36);
  border-radius: 8rpx;
  color: #fff;
  font-size: 22rpx;
  font-weight: 900;
}

.check-box.checked {
  border-color: #236c72;
  background: #236c72;
}

.private-title,
.private-desc {
  display: block;
}

.private-title {
  color: #172126;
  font-size: 24rpx;
  font-weight: 900;
}

.private-desc {
  margin-top: 4rpx;
  color: #65757b;
  font-size: 22rpx;
  line-height: 1.35;
}

.mini-button {
  position: relative;
  flex: 1;
  min-width: 0;
  min-height: 58rpx;
  font-size: 22rpx;
  padding: 0 10rpx;
}

.like-button {
  overflow: visible;
  color: #236c72;
  background: rgba(35, 108, 114, 0.08);
}

.like-button.liked {
  color: #fff;
  border-color: rgba(35, 108, 114, 0.18);
  background: linear-gradient(180deg, #2f7f6d, #236c72);
  box-shadow: 0 10rpx 22rpx rgba(35, 108, 114, 0.16);
}

.like-button.bump .thumb-icon {
  animation: thumbPop 0.42s ease;
}

.thumb-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 4rpx;
  transform-origin: 55% 75%;
}

.like-float {
  position: absolute;
  top: -30rpx;
  right: 18rpx;
  color: #236c72;
  font-size: 22rpx;
  font-weight: 900;
  pointer-events: none;
  animation: likeFloat 0.76s ease forwards;
}

@keyframes thumbPop {
  0% {
    transform: scale(1) rotate(0deg);
  }

  45% {
    transform: scale(1.38) rotate(-10deg);
  }

  100% {
    transform: scale(1) rotate(0deg);
  }
}

@keyframes likeFloat {
  0% {
    opacity: 0;
    transform: translateY(8rpx) scale(0.92);
  }

  20% {
    opacity: 1;
  }

  100% {
    opacity: 0;
    transform: translateY(-24rpx) scale(1.08);
  }
}

@media (max-width: 420px) {
  .engagement-row {
    flex-direction: column;
  }

  .action-row {
    width: 100%;
  }
}
</style>
