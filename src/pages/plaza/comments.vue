<template>
  <view class="page comments-page safe-bottom">
    <view v-if="loading" class="panel state-panel">
      <text class="muted">正在加载动态...</text>
    </view>

    <view v-else-if="errorText" class="panel state-panel">
      <text class="muted">{{ errorText }}</text>
    </view>

    <template v-else-if="post">
      <view class="panel post-panel">
        <view class="post-head">
          <view class="author-avatar">{{ post.iconText }}</view>
          <view class="author-main">
            <view class="author-line">
              <text class="author-name">{{ post.authorName }}</text>
              <text v-if="post.verified" class="mini-tag">已认证</text>
              <text class="mini-tag subtle">{{ genderLabel(post.gender) }}</text>
              <text v-if="post.ageRange" class="mini-tag subtle">{{ post.ageRange }}</text>
            </view>
            <text class="post-meta">{{ post.city }} · {{ post.distanceText }}</text>
          </view>
        </view>

        <text class="post-content">{{ post.content }}</text>

        <view v-if="post.media?.length" class="media-preview">
          <template v-if="post.mediaType === 'image'">
            <view class="media-grid" :class="imageGridClass(post.media.length)">
              <image
                v-for="media in post.media.slice(0, 9)"
                :key="media.id"
                class="media-image"
                :src="media.url"
                mode="aspectFill"
              />
            </view>
          </template>

          <video
            v-else-if="post.mediaType === 'video' && firstMedia"
            class="media-video"
            :src="firstMedia.url"
            controls
          />

          <view v-else-if="post.mediaType === 'voice' && firstMedia" class="voice-card">
            <view class="voice-mark">声</view>
            <view class="voice-body">
              <text class="voice-title">语音动态</text>
              <view class="voice-wave" :class="{ active: playingVoiceUrl === firstMedia.url }">
                <view v-for="bar in 5" :key="bar" class="voice-wave-bar" />
              </view>
            </view>
            <view class="voice-player" :class="{ playing: playingVoiceUrl === firstMedia.url }" @tap="toggleVoice(firstMedia.url)">
              <view class="voice-play-icon" />
              <view class="voice-stop-icon" />
            </view>
          </view>
        </view>

        <view class="post-stats">
          <text>{{ post.viewCount || 0 }} 浏览</text>
          <text>{{ post.likeCount }} 点赞</text>
          <text>{{ post.commentCount }} 留言</text>
        </view>
      </view>

      <view class="section comment-section">
        <view class="section-title-row">
          <text class="section-title">留言</text>
          <text class="section-count">{{ comments.length }} 条可见</text>
        </view>

        <view v-if="!comments.length" class="panel empty-panel">
          <text class="muted">还没有可查看的留言。</text>
        </view>

        <view v-else v-for="comment in comments" :key="comment.id" class="panel comment-card">
          <view class="comment-avatar" :style="{ background: avatarColor(comment.iconText) }">{{ comment.iconText }}</view>
          <view class="comment-body">
            <view class="comment-title-row">
              <text class="comment-author">{{ comment.authorName }}</text>
              <text v-if="comment.authorVerified" class="private-tag soft">已认证</text>
              <text v-if="comment.hiddenForOwnerOnly" class="private-tag">仅主人可见</text>
            </view>
            <view v-if="!comment.hiddenForOwnerOnly" class="comment-meta-row">
              <text class="comment-chip">{{ genderLabel(comment.authorGender) }}</text>
              <text v-if="comment.authorAgeRange" class="comment-chip">{{ comment.authorAgeRange }}</text>
              <text v-if="comment.authorCity" class="comment-chip">{{ comment.authorCity }}</text>
            </view>
            <text class="comment-text">{{ comment.content }}</text>
            <text class="comment-time">{{ comment.createdAt }}</text>
          </view>
        </view>
      </view>

      <view class="comment-composer">
        <view class="composer-main-row">
          <textarea
            v-model="commentDraft"
            class="comment-input"
            maxlength="120"
            :auto-height="false"
            placeholder="写一句友善留言"
            @input="clearCommentError"
          />
          <view class="send-button" :class="{ disabled: submitting || !commentDraft.trim() }" @tap="submitComment">
            <image class="send-icon" src="/static/icons/send-paper-plane.png" mode="aspectFit" />
          </view>
        </view>
        <view class="composer-bottom">
          <view class="private-toggle" @tap.stop="togglePrivateComment">
            <view class="check-box" :class="{ checked: privateComment }">{{ privateComment ? '✓' : '' }}</view>
            <text>隐藏，仅主人查看</text>
          </view>
        </view>
        <text v-if="commentError" class="post-error">{{ commentError }}</text>
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'
import type { PlazaComment, PlazaPost } from '@/types/domain'

const content = useContentStore()
const postId = ref('')
const post = ref<PlazaPost>()
const comments = ref<PlazaComment[]>([])
const loading = ref(false)
const submitting = ref(false)
const privateComment = ref(false)
const commentDraft = ref('')
const commentError = ref('')
const errorText = ref('')
const playingVoiceUrl = ref('')
const firstMedia = computed(() => post.value?.media?.[0])
let voicePlayer: ReturnType<typeof uni.createInnerAudioContext> | undefined
let lastPrivateToggleAt = 0

onLoad(async (query) => {
  postId.value = String(query?.postId || '')
  if (!postId.value) {
    errorText.value = '缺少动态 ID'
    return
  }
  await loadPage()
})

onUnload(() => {
  stopVoice()
})

async function loadPage() {
  loading.value = true
  errorText.value = ''
  try {
    const [loadedPost, loadedComments] = await Promise.all([
      content.loadPlazaPost(postId.value),
      content.loadPlazaComments(postId.value)
    ])
    post.value = loadedPost
    comments.value = loadedComments
  } catch {
    errorText.value = '动态加载失败，请稍后再试'
  } finally {
    loading.value = false
  }
}

async function loadComments() {
  comments.value = await content.loadPlazaComments(postId.value)
}

function clearCommentError() {
  if (commentError.value && commentDraft.value.trim()) commentError.value = ''
}

function togglePrivateComment() {
  const now = Date.now()
  if (now - lastPrivateToggleAt < 120) return
  lastPrivateToggleAt = now
  privateComment.value = !privateComment.value
}

async function submitComment() {
  if (submitting.value) return
  if (!commentDraft.value.trim()) {
    commentError.value = '先写一点内容，才能发送'
    showToast('先写一点内容，才能发送')
    return
  }
  submitting.value = true
  try {
    post.value = await content.commentPlazaPost(postId.value, commentDraft.value.trim(), {
      hiddenForOwnerOnly: privateComment.value
    })
    commentDraft.value = ''
    privateComment.value = false
    commentError.value = ''
    await loadComments()
    showToast('留言已发送')
  } catch {
    commentError.value = '留言发送失败，请稍后再试'
  } finally {
    submitting.value = false
  }
}

function imageGridClass(count: number) {
  return `count-${Math.min(Math.max(count, 1), 9)}`
}

function genderLabel(gender?: 'female' | 'male' | 'unknown') {
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
}

function avatarColor(text?: string) {
  const palette = ['#236c72', '#d8758b', '#6f8f72', '#b36b48', '#54759b', '#8b6fa8']
  const code = text ? text.charCodeAt(0) : 0
  return palette[code % palette.length]
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
.comments-page {
  min-height: 100vh;
  padding-bottom: calc(132rpx + env(safe-area-inset-bottom));
  background:
    radial-gradient(circle at 80% -6%, rgba(216, 117, 139, 0.1), transparent 30%),
    radial-gradient(circle at 8% 18%, rgba(35, 108, 114, 0.08), transparent 26%),
    linear-gradient(180deg, #fbfcfa, #eef3f1 58%, #f7faf8);
}

.state-panel,
.empty-panel {
  padding: 34rpx;
  text-align: center;
}

.post-panel {
  margin: 16rpx 18rpx 16rpx;
  border: 1px solid rgba(35, 108, 114, 0.08);
  border-radius: 34rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(250, 253, 251, 0.9)),
    radial-gradient(circle at 94% 0%, rgba(216, 117, 139, 0.08), transparent 28%);
  box-shadow: 0 20rpx 48rpx rgba(31, 54, 58, 0.07);
}

.post-head {
  display: grid;
  grid-template-columns: 72rpx minmax(0, 1fr);
  gap: 16rpx;
  align-items: center;
  padding-bottom: 18rpx;
  border-bottom: 1px solid rgba(35, 108, 114, 0.08);
}

.author-avatar,
.comment-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 900;
}

.author-avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: linear-gradient(180deg, #d8758b, #236c72);
  font-size: 28rpx;
  box-shadow: 0 10rpx 24rpx rgba(35, 108, 114, 0.16);
}

.author-main {
  min-width: 0;
}

.author-line {
  display: flex;
  align-items: center;
  gap: 8rpx;
  min-width: 0;
}

.author-name {
  overflow: hidden;
  color: #172126;
  font-size: 30rpx;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mini-tag {
  flex-shrink: 0;
  border-radius: 999px;
  padding: 6rpx 12rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
  font-size: 20rpx;
  font-weight: 900;
}

.mini-tag.subtle {
  color: #65757b;
  background: rgba(29, 29, 31, 0.06);
}

.post-meta {
  display: block;
  margin-top: 6rpx;
  color: #65757b;
  font-size: 23rpx;
}

.post-content {
  display: block;
  margin-top: 22rpx;
  color: #172126;
  font-size: 30rpx;
  font-weight: 800;
  line-height: 1.58;
}

.media-preview {
  margin-top: 24rpx;
  padding-top: 20rpx;
  border-top: 1px solid rgba(35, 108, 114, 0.07);
}

.media-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8rpx;
}

.media-grid.count-1 {
  grid-template-columns: minmax(0, 1fr);
  max-width: 460rpx;
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
  border-radius: 20rpx;
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
  border-radius: 22rpx;
  background: #101820;
}

.voice-card {
  display: grid;
  grid-template-columns: 64rpx minmax(0, 1fr) 64rpx;
  gap: 14rpx;
  align-items: center;
  border: 1px solid rgba(35, 108, 114, 0.09);
  border-radius: 30rpx;
  padding: 20rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(247, 250, 249, 0.94)),
    linear-gradient(90deg, rgba(35, 108, 114, 0.06), transparent);
}

.voice-mark {
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

.voice-title {
  color: #172126;
  font-size: 26rpx;
  font-weight: 900;
}

.voice-wave {
  display: flex;
  align-items: flex-end;
  gap: 5rpx;
  height: 28rpx;
  margin-top: 8rpx;
  opacity: 0;
  transition: opacity 0.18s ease;
}

.voice-wave.active {
  opacity: 1;
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
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.88);
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

.post-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: center;
  gap: 12rpx;
  margin-top: 22rpx;
  padding-top: 18rpx;
  border-top: 1px solid rgba(35, 108, 114, 0.07);
  color: #65757b;
  font-size: 23rpx;
  font-weight: 800;
}

.post-stats text {
  border-radius: 999px;
  padding: 10rpx 12rpx;
  background: rgba(35, 108, 114, 0.06);
  text-align: center;
}

.comment-section {
  margin-top: 10rpx;
}

.section-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 2rpx 14rpx;
}

.section-title {
  color: #172126;
  font-size: 30rpx;
  font-weight: 900;
}

.section-count {
  color: #65757b;
  font-size: 23rpx;
}

.comment-card {
  display: grid;
  grid-template-columns: 62rpx minmax(0, 1fr);
  gap: 16rpx;
  margin-bottom: 14rpx;
  border: 1px solid rgba(35, 108, 114, 0.07);
  border-radius: 32rpx;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 12rpx 30rpx rgba(31, 54, 58, 0.045);
}

.comment-avatar {
  width: 62rpx;
  height: 62rpx;
  border-radius: 50%;
  font-size: 24rpx;
  box-shadow: 0 8rpx 18rpx rgba(31, 54, 58, 0.12);
}

.comment-title-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
  flex-wrap: wrap;
}

.comment-author,
.comment-text,
.comment-time {
  display: block;
}

.comment-author {
  color: #172126;
  font-size: 26rpx;
  font-weight: 900;
}

.private-tag {
  border-radius: 999px;
  padding: 5rpx 10rpx;
  color: #236c72;
  background: rgba(35, 108, 114, 0.1);
  font-size: 20rpx;
  font-weight: 900;
}

.private-tag.soft {
  color: #6b7d74;
  background: rgba(111, 143, 114, 0.11);
}

.comment-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  margin-top: 8rpx;
}

.comment-chip {
  border-radius: 999px;
  padding: 5rpx 10rpx;
  color: #65757b;
  background: rgba(29, 29, 31, 0.055);
  font-size: 20rpx;
  font-weight: 800;
}

.comment-text {
  margin-top: 8rpx;
  color: #172126;
  font-size: 26rpx;
  line-height: 1.5;
}

.comment-time {
  margin-top: 8rpx;
  color: #8a969b;
  font-size: 21rpx;
}

.comment-composer {
  position: fixed;
  left: 12rpx;
  right: 12rpx;
  bottom: 10rpx;
  z-index: 90;
  border: 1px solid rgba(35, 108, 114, 0.08);
  border-radius: 34rpx;
  padding: 12rpx 16rpx calc(12rpx + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 -10rpx 34rpx rgba(31, 54, 58, 0.1);
  backdrop-filter: blur(16px);
}

.composer-main-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 74rpx;
  gap: 12rpx;
  align-items: center;
  border: 1px solid rgba(35, 108, 114, 0.08);
  border-radius: 30rpx;
  padding: 8rpx 8rpx 8rpx 14rpx;
  background:
    linear-gradient(180deg, rgba(247, 250, 249, 0.94), rgba(241, 247, 244, 0.9)),
    radial-gradient(circle at 100% 50%, rgba(35, 108, 114, 0.08), transparent 36%);
}

.comment-input {
  width: 100%;
  height: 64rpx;
  min-height: 64rpx;
  max-height: 64rpx;
  border: 0;
  border-radius: 24rpx;
  padding: 10rpx 10rpx 10rpx 4rpx;
  color: #172126;
  background: transparent;
  box-sizing: border-box;
  font-size: 26rpx;
  line-height: 1.35;
}

.composer-bottom {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 14rpx;
  margin-top: 9rpx;
  padding-left: 4rpx;
}

.private-toggle {
  display: flex;
  align-items: center;
  gap: 10rpx;
  min-width: 0;
  color: #65757b;
  font-size: 22rpx;
  font-weight: 800;
}

.check-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32rpx;
  height: 32rpx;
  border: 2rpx solid rgba(35, 108, 114, 0.36);
  border-radius: 10rpx;
  color: #fff;
  font-size: 20rpx;
  font-weight: 900;
}

.check-box.checked {
  border-color: #236c72;
  background: #236c72;
}

.send-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 66rpx;
  height: 60rpx;
  border-left: 1px solid rgba(35, 108, 114, 0.1);
  border-radius: 22rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.86), rgba(236, 245, 241, 0.88)),
    radial-gradient(circle at 58% 32%, rgba(80, 166, 207, 0.14), transparent 38%);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.72);
  transition: transform 140ms ease, opacity 140ms ease;
}

.send-button:active {
  transform: scale(0.97);
}

.send-button.disabled {
  background: rgba(224, 232, 229, 0.72);
  box-shadow: none;
  opacity: 0.58;
}

.send-icon {
  display: block;
  width: 42rpx;
  height: 42rpx;
  transform: translateX(1rpx);
}

.post-error {
  display: block;
  margin-top: 8rpx;
  color: #b94747;
  font-size: 23rpx;
  font-weight: 800;
}
</style>
