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
          <view class="row author-row" @tap.stop="openUserCard(post)" @click.stop="openUserCard(post)">
            <view class="author-icon" @tap.stop="openUserCard(post)" @click.stop="openUserCard(post)">
              <image class="avatar-image" :src="resolveAvatarUrl(post.iconUrl, post.id || post.authorName)" mode="aspectFill" />
            </view>
            <view>
              <text class="h2">{{ post.authorName }}</text>
              <text class="muted">{{ post.topic }} · {{ post.city }} · {{ post.ageRange }} · {{ post.distanceText }}</text>
            </view>
          </view>
          <view class="row tag-row">
            <text class="tag emotion-tag">{{ emotionTag(post) }}</text>
            <text class="tag gender-tag">{{ post.gender === 'female' ? '女' : post.gender === 'male' ? '男' : '未知' }}</text>
          </view>
        </view>
        <text class="body post-content" @tap="openCommentPage(post.id)">{{ post.content }}</text>
        <view v-if="post.media?.length" class="media-preview" :class="`media-${post.mediaType || 'text'}`" @tap.stop @click.stop>
          <template v-if="post.mediaType === 'image'">
            <view class="media-grid" :class="imageGridClass(post.media?.length || 0)">
              <view
                v-for="media in post.media.slice(0, 9)"
                :key="media.id"
                class="media-image-cell"
                @tap.stop="previewPostImage(post.media, media.url)"
              >
                <image class="media-image" :src="media.url" mode="aspectFill" />
              </view>
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
                @tap.stop="toggleVoice(media.url)"
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
            <view class="stat-item comment-stat" @tap.stop="openCommentPage(post.id)" @click.stop="openCommentPage(post.id)">
              <text class="stat-number">{{ post.commentCount }}</text>
              <text class="stat-label">留言</text>
            </view>
          </view>
          <view class="row action-row" @tap.stop @click.stop>
            <view
              class="button secondary mini-button like-button"
              :class="{ liked: post.likedByMe, bump: likeEffects[post.id] }"
              @tap.stop="likePost(post)"
            >
              <text class="thumb-icon">👍</text>
              <text>{{ post.likedByMe ? '已赞' : '点赞' }}</text>
              <text v-if="likeEffects[post.id]" class="like-float">{{ likeEffects[post.id] }}</text>
            </view>
            <view class="button ghost mini-button report-post-button" @tap.stop="openPostReport(post)" @click.stop="openPostReport(post)">举报</view>
            <view class="button ghost mini-button" @tap.stop="openCommentPage(post.id)" @click.stop="openCommentPage(post.id)">留言</view>
          </view>
        </view>
        <view v-if="post.commentPreview" class="comment-footer">
          <text v-if="post.commentPreview" class="comment-preview">最新留言：{{ post.commentPreview }}</text>
        </view>
      </view>
    </view>

    <view class="publish-fab" @tap="openComposer">+</view>

    <view v-if="composerOpen" class="modal-mask center-mask" @touchmove.stop.prevent>
      <view class="modal-card composer-card" @tap.stop @click.stop>
        <view class="composer-top">
          <text class="h2">发布动态</text>
          <view class="composer-avatar">
            <image class="avatar-image" :src="resolveAvatarUrl(app.user?.avatarUrl, app.user?.id || 'current-user')" mode="aspectFill" />
          </view>
        </view>
        <textarea
          v-model="draftPost"
          class="composer-input"
          maxlength="180"
          placeholder="写一句今天想公开分享的话。"
          @input="clearPostError"
          @tap.stop
          @click.stop
        />
        <text v-if="postError" class="post-error">{{ postError }}</text>
        <view class="composer-tool-row">
          <view
            class="composer-tool"
            :class="{ active: selectedImages.length > 0 }"
            @tap="chooseImages"
            @click="chooseImages"
          >
            <view class="composer-tool-icon image-icon" />
            <text>图片</text>
          </view>
          <view
            class="composer-tool"
            :class="{ active: Boolean(selectedVideo) }"
            @tap="choosePostVideo"
            @click="choosePostVideo"
          >
            <view class="composer-tool-icon video-icon" />
            <text>视频</text>
          </view>
        </view>
        <view v-if="selectedImages.length" class="composer-media-grid" :class="imageGridClass(selectedImages.length)">
          <view v-for="image in selectedImages" :key="image.id" class="composer-image-cell">
            <image class="composer-image" :src="image.url" mode="aspectFill" />
            <view class="remove-image" @tap.stop="removeSelectedImage(image.id)" @click.stop="removeSelectedImage(image.id)">×</view>
          </view>
        </view>
        <view v-if="selectedVideo" class="composer-video-preview">
          <video class="composer-video" :src="selectedVideo.url" controls />
          <view class="remove-image" @tap.stop="removeSelectedVideo" @click.stop="removeSelectedVideo">×</view>
        </view>
        <view class="modal-actions">
          <view class="button ghost" @tap="closeComposer">取消</view>
          <view class="button publish-button" :class="{ disabled: content.submitting || !draftPost.trim() }" @tap="publishPost">
            发布
          </view>
        </view>
      </view>
    </view>

    <view v-if="userCardOpen && selectedProfilePost" class="modal-mask center-mask" @touchmove.stop.prevent>
      <view class="modal-card user-card" @tap.stop @click.stop>
        <view class="user-card-report" @tap.stop="openUserReport(selectedProfilePost)" @click.stop="openUserReport(selectedProfilePost)">举报</view>
        <view class="user-card-main">
          <image class="user-card-avatar" :src="resolveAvatarUrl(selectedProfilePost.iconUrl, selectedProfilePost.authorId)" mode="aspectFill" />
          <view class="user-card-info">
            <text class="user-card-name">{{ selectedProfilePost.authorName }}</text>
            <text class="user-card-meta">{{ selectedProfilePost.city || '全国' }} · {{ selectedProfilePost.ageRange || '年龄未知' }}</text>
            <text class="user-card-meta">{{ selectedProfilePost.topic }} · {{ selectedProfilePost.distanceText }}</text>
          </view>
        </view>
        <view class="user-card-preview">{{ selectedProfilePost.content }}</view>
        <view class="modal-actions">
          <view class="button ghost" @tap="closeUserCard" @click="closeUserCard">关闭</view>
          <view class="button" @tap="openCommentPage(selectedProfilePost.id)" @click="openCommentPage(selectedProfilePost.id)">查看动态</view>
        </view>
      </view>
    </view>

    <view v-if="reportOpen && reportTarget" class="modal-mask center-mask" @touchmove.stop.prevent>
      <view class="modal-card report-card" @tap.stop @click.stop>
        <text class="modal-kicker">举报</text>
        <text class="modal-title">{{ reportTarget.title }}</text>
        <text class="report-desc">普通举报仅支持：用户、广场帖子、漂流瓶；评论、聊天和私密照片走对应审核或申诉链路。</text>
        <view class="choice-row report-reasons">
          <view
            v-for="reason in reportReasons"
            :key="reason"
            class="choice-chip"
            :class="{ active: reportReason === reason }"
            @tap="reportReason = reason"
            @click="reportReason = reason"
          >
            {{ reason }}
          </view>
        </view>
        <view class="report-field">
          <text class="field-label">举报说明</text>
          <textarea
            v-model="reportDescription"
            class="report-textarea"
            maxlength="120"
            placeholder="补充举报说明"
            @tap.stop
            @click.stop
          />
        </view>
        <view class="report-preview">
          <text class="field-label">相关内容</text>
          <text>{{ reportTarget.preview }}</text>
        </view>
        <view class="modal-actions report-actions">
          <view class="button ghost" @tap="closeReportModal" @click="closeReportModal">取消</view>
          <view class="button" :class="{ disabled: reportSubmitting }" @tap="submitReport" @click="submitReport">
            {{ reportSubmitting ? '提交中' : '提交举报' }}
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
import type { PlazaMedia, PlazaPost } from '@/types/domain'
import { resolveAvatarUrl } from '@/utils/avatar'

const app = useAppStore()
const content = useContentStore()
const filters = ref<ExploreFilterValue>({ city: '全国', gender: '全部', ageRange: '全部' })
const composerOpen = ref(false)
const draftPost = ref('')
const postError = ref('')
const userCardOpen = ref(false)
const selectedProfilePost = ref<PlazaPost | null>(null)
const reportOpen = ref(false)
const reportSubmitting = ref(false)
const reportReason = ref('骚扰或不友善')
const reportDescription = ref('')
const reportTarget = ref<{ type: 'user' | 'plaza'; id: string; title: string; preview: string } | null>(null)
const lastLikeAction = ref<{ postId: string; at: number }>({ postId: '', at: 0 })
const likeEffects = ref<Record<string, string>>({})
type SelectedImage = {
  id: string
  url: string
  sizeBytes?: number
}
type SelectedVideo = {
  id: string
  url: string
  sizeBytes?: number
  durationSeconds?: number
}
const selectedImages = ref<SelectedImage[]>([])
const selectedVideo = ref<SelectedVideo | null>(null)
let filterReloadTimer: ReturnType<typeof setTimeout> | undefined
let voicePlayer: ReturnType<typeof uni.createInnerAudioContext> | undefined
const likeEffectTimers: Record<string, ReturnType<typeof setTimeout>> = {}
const playingVoiceUrl = ref('')
type FeedTab = 'nearby' | 'gift' | 'newcomer'

const cityOptions = ['全国', '北京', '上海', '广州', '深圳', '杭州', '成都', '厦门']
const activeFeed = ref<FeedTab>('nearby')
const reportReasons = ['骚扰或不友善', '低俗违规', '广告引流', '虚假资料', '其他问题']
const feedTabs: Array<{ label: string; value: FeedTab }> = [
  { label: '附近动态', value: 'nearby' },
  { label: '礼物榜', value: 'gift' },
  { label: '新人推荐榜', value: 'newcomer' }
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
function emotionTag(post: PlazaPost) {
  const text = `${post.topic || ''} ${post.content || ''}`
  if (/夜|安静|难过|心|想/.test(text)) return '倾诉'
  if (/勇气|重新|开始|明天/.test(text)) return '治愈'
  if (/海|风|雨|城市/.test(text)) return '氛围'
  if ((post.likeCount || 0) >= 20) return '高共鸣'
  return '轻松'
}

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
  if (url === '/pages/plaza/index' || url === '/pages/bottle/index' || url === '/pages/game/index' || url === '/pages/messages/index') {
    switchTab(url)
    return
  }
  navigateTo(url)
}

function openUserCard(post: PlazaPost) {
  selectedProfilePost.value = post
  userCardOpen.value = true
}

function closeUserCard() {
  userCardOpen.value = false
}

function resetReportDraft() {
  reportReason.value = '骚扰或不友善'
  reportDescription.value = ''
  reportSubmitting.value = false
}

function openPostReport(post: PlazaPost) {
  resetReportDraft()
  reportTarget.value = {
    type: 'plaza',
    id: post.id,
    title: `举报 ${post.authorName} 的广场帖子`,
    preview: post.content
  }
  reportOpen.value = true
}

function openUserReport(post: PlazaPost) {
  resetReportDraft()
  reportTarget.value = {
    type: 'user',
    id: post.authorId,
    title: `举报用户 ${post.authorName}`,
    preview: post.content
  }
  reportOpen.value = true
}

function closeReportModal() {
  reportOpen.value = false
  reportTarget.value = null
}

function buildReportReason() {
  const description = reportDescription.value.trim()
  return description ? `${reportReason.value}：${description}` : ''
}

async function submitReport() {
  if (!reportTarget.value || reportSubmitting.value) return
  const reason = buildReportReason()
  if (!reason) {
    showToast('请填写举报说明')
    return
  }
  reportSubmitting.value = true
  try {
    if (reportTarget.value.type === 'user') {
      await content.reportUser(reportTarget.value.id, reason)
    } else {
      await content.reportPlazaPost(reportTarget.value.id, reason)
    }
    closeReportModal()
    closeUserCard()
    showToast('举报已提交')
  } finally {
    reportSubmitting.value = false
  }
}

async function publishPost() {
  if (!draftPost.value.trim()) {
    postError.value = '先写一点内容，才能发布'
    showToast('先写一点内容，才能发布')
    return
  }
  const imageMedia = selectedImages.value.map((item) => ({
    mediaType: 'image' as const,
    url: item.url,
    mimeType: inferImageMime(item.url),
    sizeBytes: item.sizeBytes
  }))
  const videoMedia = selectedVideo.value
    ? [{
        mediaType: 'video' as const,
        url: selectedVideo.value.url,
        mimeType: inferVideoMime(selectedVideo.value.url),
        sizeBytes: selectedVideo.value.sizeBytes,
        durationSeconds: selectedVideo.value.durationSeconds
      }]
    : []
  const media = selectedVideo.value ? videoMedia : imageMedia
  await content.publishPlazaPost(draftPost.value.trim(), {
    mediaType: selectedVideo.value ? 'video' : media.length ? 'image' : 'text',
    mediaCount: media.length,
    media
  })
  draftPost.value = ''
  postError.value = ''
  selectedImages.value = []
  selectedVideo.value = null
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
  selectedImages.value = []
  selectedVideo.value = null
}

function chooseImages() {
  const count = Math.max(1, 9 - selectedImages.value.length)
  if (typeof uni === 'undefined' || typeof uni.chooseImage !== 'function' || count <= 0) return
  selectedVideo.value = null
  uni.chooseImage({
    count,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (result) => {
      const payload = result as { tempFilePaths?: string[]; tempFiles?: Array<{ path?: string; size?: number }> }
      const paths = payload.tempFilePaths || []
      const files = payload.tempFiles || []
      if (!paths.length) return
      const startedAt = Date.now()
      const nextImages = paths.map((url, index) => ({
        id: `${startedAt}_${index}_${url}`,
        url,
        sizeBytes: files[index]?.size
      }))
      selectedImages.value = [...selectedImages.value, ...nextImages].slice(0, 9)
    },
    fail: () => {
      if (!selectedImages.value.length) selectedVideo.value = null
    }
  })
}

function choosePostVideo() {
  if (typeof uni === 'undefined' || typeof uni.chooseVideo !== 'function') return
  selectedImages.value = []
  uni.chooseVideo({
    sourceType: ['album', 'camera'],
    compressed: true,
    success: (result) => {
      selectedVideo.value = {
        id: `${Date.now()}_${result.tempFilePath}`,
        url: result.tempFilePath,
        sizeBytes: result.size,
        durationSeconds: result.duration
      }
    }
  })
}

function removeSelectedImage(id: string) {
  selectedImages.value = selectedImages.value.filter((item) => item.id !== id)
}

function removeSelectedVideo() {
  selectedVideo.value = null
}

function inferImageMime(url: string) {
  const normalized = (url.split('?', 1)[0] || '').toLowerCase()
  if (normalized.endsWith('.png')) return 'image/png'
  if (normalized.endsWith('.webp')) return 'image/webp'
  return 'image/jpeg'
}

function inferVideoMime(url: string) {
  const normalized = (url.split('?', 1)[0] || '').toLowerCase()
  if (normalized.endsWith('.webm')) return 'video/webm'
  if (normalized.endsWith('.mov')) return 'video/quicktime'
  return 'video/mp4'
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

function previewPostImage(media: PlazaMedia[] | undefined, currentUrl: string) {
  const urls = (media || []).filter((item) => item.mediaType === 'image').map((item) => item.url)
  if (!urls.length || typeof uni === 'undefined' || !uni.previewImage) return
  uni.previewImage({ urls, current: currentUrl })
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
    radial-gradient(circle at 84% -4%, rgba(37, 99, 235, 0.06), transparent 30%),
    radial-gradient(circle at 14% 0%, rgba(15, 118, 110, 0.06), transparent 28%),
    linear-gradient(180deg, #ffffff, #f8fafc 58%, #f1f5f9);
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
  border-radius: 16px;
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

.media-image-cell {
  position: relative;
  overflow: hidden;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 12px;
  background: rgba(35, 108, 114, 0.08);
}

.media-grid.count-1 .media-image-cell {
  aspect-ratio: 4 / 3;
}

.media-image {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  object-fit: cover;
}

.media-video {
  display: block;
  width: 100%;
  height: 360rpx;
  overflow: hidden;
  border-radius: 12px;
  background: #101820;
}

.voice-card {
  display: grid;
  grid-template-columns: 64rpx minmax(0, 1fr) 104rpx;
  gap: 14rpx;
  align-items: center;
  border: 1px solid rgba(35, 108, 114, 0.1);
  border-radius: 16px;
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

.user-card {
  position: relative;
  padding-top: 58rpx;
}

.user-card-report {
  position: absolute;
  top: 18rpx;
  left: 20rpx;
  color: #b42318;
  font-size: 24rpx;
  font-weight: 900;
}

.user-card-main {
  display: grid;
  grid-template-columns: 92rpx minmax(0, 1fr);
  gap: 18rpx;
  align-items: center;
}

.user-card-avatar {
  width: 92rpx;
  height: 92rpx;
  border-radius: 50%;
  background: #e8f1ef;
}

.user-card-info {
  min-width: 0;
}

.user-card-name,
.user-card-meta {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-card-name {
  color: #172126;
  font-size: 32rpx;
  font-weight: 900;
}

.user-card-meta {
  margin-top: 6rpx;
  color: #65757b;
  font-size: 23rpx;
}

.user-card-preview,
.report-preview {
  margin-top: 22rpx;
  border-radius: 12px;
  padding: 18rpx;
  color: #334155;
  background: #f6faf9;
  font-size: 24rpx;
  line-height: 1.6;
}

.report-card {
  max-width: 500px;
}

.report-desc {
  display: block;
  margin-top: 12rpx;
  color: #64748b;
  font-size: 24rpx;
  line-height: 1.55;
}

.report-reasons,
.report-field {
  margin-top: 20rpx;
}

.report-textarea {
  box-sizing: border-box;
  width: 100%;
  min-height: 128rpx;
  margin-top: 10rpx;
  border: 1px solid rgba(35, 108, 114, 0.14);
  border-radius: 12px;
  padding: 16rpx;
  background: #f8fbfb;
  color: #172126;
  font-size: 25rpx;
}

.report-actions {
  grid-template-columns: 1fr 1fr;
}

.reply-sheet-mask {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  background: rgba(13, 20, 23, 0.38);
  backdrop-filter: blur(10px);
}

.reply-sheet {
  width: 100%;
  max-width: 560px;
  border-radius: 8px 8px 0 0;
  padding: 14rpx 24rpx calc(24rpx + env(safe-area-inset-bottom));
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 251, 250, 0.96)),
    radial-gradient(circle at 92% 0%, rgba(35, 108, 114, 0.08), transparent 30%);
  box-sizing: border-box;
  box-shadow: 0 -22rpx 60rpx rgba(13, 20, 23, 0.22);
}

.sheet-grip {
  width: 72rpx;
  height: 8rpx;
  margin: 0 auto 20rpx;
  border-radius: 999px;
  background: rgba(23, 33, 38, 0.16);
}

.reply-sheet-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
}

.reply-context {
  display: block;
  margin-top: 6rpx;
}

.reply-origin-card {
  margin: 18rpx 0 16rpx;
  border: 1px solid rgba(37, 99, 235, 0.1);
  border-radius: 16px;
  padding: 16rpx;
  background:
    linear-gradient(180deg, rgba(248, 250, 252, 0.98), rgba(255, 255, 255, 0.94)),
    radial-gradient(circle at 96% 0%, rgba(37, 99, 235, 0.08), transparent 34%);
}

.reply-origin-kicker,
.reply-origin-author,
.reply-origin-text {
  display: block;
}

.reply-origin-kicker {
  color: #2563eb;
  font-size: 20rpx;
  font-weight: 900;
}

.reply-origin-author {
  margin-top: 4rpx;
  color: #0f172a;
  font-size: 24rpx;
  font-weight: 900;
}

.reply-origin-text {
  margin-top: 6rpx;
  overflow: hidden;
  color: #475569;
  font-size: 24rpx;
  line-height: 1.45;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.sheet-link {
  flex: 0 0 auto;
  border-radius: 8px;
  padding: 12rpx 16rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.08);
  font-size: 23rpx;
  font-weight: 900;
}

.composer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16rpx;
}

.composer-top .h2 {
  display: block;
  color: #172126;
  font-size: 30rpx;
  font-weight: 900;
}

.composer-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
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

.composer-tool-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-top: 14rpx;
}

.composer-tool {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10rpx;
  min-width: 136rpx;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 999px;
  padding: 12rpx 18rpx;
  color: #172126;
  background: rgba(247, 250, 249, 0.92);
  font-size: 24rpx;
  font-weight: 800;
  text-align: center;
}

.composer-tool.active {
  color: #fff;
  border-color: rgba(35, 108, 114, 0.16);
  background: #236c72;
}

.composer-tool-icon {
  position: relative;
  width: 34rpx;
  height: 34rpx;
  border-radius: 10rpx;
  background: currentColor;
  opacity: 0.88;
}

.composer-tool-icon::before {
  position: absolute;
  inset: 8rpx;
  border: 3rpx solid #fff;
  border-radius: 7rpx;
  content: '';
}

.composer-tool-icon::after {
  position: absolute;
  right: 7rpx;
  bottom: 7rpx;
  width: 8rpx;
  height: 8rpx;
  border-radius: 50%;
  background: #fff;
  content: '';
}

.video-icon::before {
  inset: 9rpx 7rpx;
  border-radius: 5rpx;
}

.video-icon::after {
  right: -5rpx;
  bottom: 9rpx;
  width: 0;
  height: 0;
  border-top: 7rpx solid transparent;
  border-bottom: 7rpx solid transparent;
  border-left: 10rpx solid currentColor;
  border-radius: 0;
  background: transparent;
}

.composer-media-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10rpx;
  margin-top: 16rpx;
}

.composer-media-grid.count-1 {
  grid-template-columns: minmax(0, 1fr);
  max-width: 440rpx;
}

.composer-media-grid.count-2,
.composer-media-grid.count-4 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.composer-image-cell {
  position: relative;
  overflow: hidden;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 12px;
  background: rgba(35, 108, 114, 0.08);
}

.composer-media-grid.count-1 .composer-image-cell {
  aspect-ratio: 4 / 3;
}

.composer-image {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: inherit;
}

.composer-video-preview {
  position: relative;
  overflow: hidden;
  margin-top: 16rpx;
  border-radius: 12px;
  background: #101820;
}

.composer-video {
  display: block;
  width: 100%;
  height: 260rpx;
}

.remove-image {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  color: #fff;
  background: rgba(15, 23, 42, 0.66);
  font-size: 30rpx;
  font-weight: 900;
  line-height: 1;
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
  border-radius: 16px;
  animation: feed-card-in 220ms ease-out both;
  cursor: pointer;
}

.plaza-card:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 32rpx 70rpx rgba(3, 12, 18, 0.24);
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

.gender-tag {
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
}

.emotion-tag {
  color: #7b3b52;
  background: rgba(191, 91, 115, 0.12);
}

.action-row {
  flex-shrink: 0;
  width: 176rpx;
}

.author-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  width: 64rpx;
  height: 64rpx;
  border-radius: 8px;
  color: #fff;
  background: #d8758b;
  font-weight: 900;
}

.avatar-image {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: inherit;
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

@keyframes feed-card-in {
  from {
    opacity: 0;
    transform: translateY(12rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
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
