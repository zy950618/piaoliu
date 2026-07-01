<template>
  <view class="page treehole-page safe-bottom">
    <view class="tree-scene">
      <view class="sky-glow glow-left"></view>
      <view class="sky-glow glow-right"></view>
      <view class="leaf leaf-a"></view>
      <view class="leaf leaf-b"></view>
      <view class="leaf leaf-c"></view>
      <view class="falling-leaves">
        <view v-for="index in 6" :key="index" class="falling-leaf" :class="`falling-leaf-${index}`"></view>
      </view>

      <view class="tree-wrap">
        <view class="canopy cloud-back"></view>
        <view class="canopy cloud-left"></view>
        <view class="canopy cloud-top"></view>
        <view class="canopy cloud-right"></view>
        <view class="canopy cloud-front"></view>
        <view class="canopy-light"></view>

        <view class="hollow-shell">
          <view class="tree-hollow">
            <text class="hollow-kicker">华东树洞</text>
            <text class="hollow-title">看见一条心情</text>
            <text class="hollow-content">
              {{ viewedMood?.content || '随机听见一条最新匿名心情。' }}
            </text>
            <view v-if="viewedMood" class="hollow-meta">
              <text>{{ genderLabel(viewedMood.authorGender) }}</text>
              <text>{{ viewedMood.resonanceCount }} 共鸣</text>
            </view>
          </view>
        </view>

        <view class="branch branch-left"></view>
        <view class="branch branch-right"></view>
        <view class="tree-trunk">
          <view class="trunk-shine"></view>
          <view class="trunk-line left"></view>
          <view class="trunk-line right"></view>
        </view>
      </view>

      <view class="tree-ground"></view>

      <view class="floating-action write-action" @tap="openComposer" @click="openComposer">
        <text class="action-count">发 +{{ treeholePostLeft }}</text>
        <text class="action-main">发心情</text>
        <text class="action-sub">匿名写下</text>
      </view>
      <view class="floating-action read-action" @tap="showRandomMood" @click="showRandomMood">
        <text class="action-main">看心情</text>
        <text class="action-sub">随机最新</text>
      </view>
    </view>

    <view class="mood-dock">
      <view class="mood-window">
        <view v-if="moodLoopItems.length > 0" class="mood-track">
          <view
            v-for="(post, index) in moodLoopItems"
            :key="`${post.id}-${index}`"
            class="mood-item"
            :class="`mood-card-${index % 4}`"
          >
            <view class="avatar" :class="post.authorGender">
              <image class="avatar-image" :src="resolveAvatarUrl(post.authorAvatarUrl, post.id || post.authorName)" mode="aspectFill" />
            </view>
            <view class="mood-body">
              <view class="mood-top">
                <text class="nickname">{{ maskNickname(post.authorName) }}</text>
                <text class="gender-tag" :class="post.authorGender">{{ genderLabel(post.authorGender) }}</text>
              </view>
              <text class="mood-text">{{ post.content }}</text>
            </view>
          </view>
        </view>
        <view v-else class="empty-mood">暂时还没有心情</view>
      </view>
    </view>

    <view v-if="composerOpen" class="modal-mask">
      <view class="modal-card mood-card" @tap.stop @click.stop>
        <view class="composer-top">
          <view>
            <text class="h2">匿名树洞留言板</text>
            <text class="muted hint">将以 {{ genderLabel(app.user?.gender || 'unknown') }} 身份匿名发布。</text>
          </view>
          <view class="composer-avatar" :class="app.user?.gender || 'unknown'">
            <image class="avatar-image" :src="resolveAvatarUrl(app.user?.avatarUrl, app.user?.id || 'current-user')" mode="aspectFill" />
          </view>
        </view>
        <textarea
          v-model="draft"
          class="textarea"
          maxlength="280"
          placeholder="把现在的心情放进树洞"
          @tap.stop
          @click.stop
        />
        <view class="modal-actions">
          <view class="button ghost" @tap="closeComposer" @click="closeComposer">取消</view>
          <view
            class="button"
            :class="{ disabled: content.submitting || !draft.trim() }"
            @tap="publish"
            @click="publish"
          >
            发布
          </view>
        </view>
      </view>
    </view>

    <view v-if="moodDetailOpen && viewedMood" class="modal-mask">
      <view class="modal-card mood-detail-card" @tap.stop @click.stop>
        <view class="detail-user">
          <view class="detail-avatar" :class="viewedMood.authorGender">
            <image class="avatar-image" :src="resolveAvatarUrl(viewedMood.authorAvatarUrl, viewedMood.id || viewedMood.authorName)" mode="aspectFill" />
          </view>
          <view class="detail-user-main">
            <view class="detail-name-row">
              <text class="detail-name">{{ maskNickname(viewedMood.authorName) }}</text>
              <text class="gender-tag" :class="viewedMood.authorGender">{{ genderLabel(viewedMood.authorGender) }}</text>
              <text class="age-tag">{{ viewedMood.authorAgeRange }}</text>
            </view>
            <text class="muted">匿名树洞心情</text>
          </view>
        </view>
        <text class="detail-content">{{ viewedMood.content }}</text>
        <view class="detail-meta">
          <text>{{ viewedMood.resonanceCount }} 共鸣</text>
          <text>{{ viewedMood.replyCount }} 回应</text>
        </view>
        <textarea
          v-model="replyDraft"
          class="reply-input"
          maxlength="160"
          placeholder="写一句想回复的心情"
          @input="clearReplyError"
          @tap.stop
          @click.stop
        />
        <text v-if="replyError" class="reply-error">{{ replyError }}</text>
        <text v-if="treeholeContextStatus" class="context-chat-copy">{{ treeholeContextStatus }}</text>
        <view class="detail-actions">
          <view class="button ghost" @tap="closeMoodDetail" @click="closeMoodDetail">放回树洞</view>
          <view
            class="button"
            :class="{ disabled: replySubmitting || !replyDraft.trim() }"
            @tap="replyMood"
            @click="replyMood"
          >
            回复心情
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onUnmounted, ref } from 'vue'
import { onHide, onLoad, onShow } from '@dcloudio/uni-app'
import { useQuotaGuard } from '@/composables/useQuotaGuard'
import { navigateTo, showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { TreeholePost } from '@/types/domain'
import { resolveAvatarUrl } from '@/utils/avatar'

type TreeholeGender = TreeholePost['authorGender']

const app = useAppStore()
const content = useContentStore()
const { ensureQuota } = useQuotaGuard()
const draft = ref('')
const composerOpen = ref(false)
const viewedMood = ref<TreeholePost>()
const moodDetailOpen = ref(false)
const replyDraft = ref('')
const replyError = ref('')
const replySubmitting = ref(false)
const treeholeContextStatus = ref('')
const bodyScrollLockClass = 'treehole-lock-scroll'

const moodLoopItems = computed(() => {
  if (content.treeholeFeed.length === 0) return []
  return [...content.treeholeFeed, ...content.treeholeFeed]
})

const treeholePostLeft = computed(() => app.quotas?.treehole_post.remaining ?? 0)

onLoad(async () => {
  await app.hydrate()
  await content.loadTreeholeFeed()
  viewedMood.value = pickRandomMood()
})

onShow(lockPageScroll)

onHide(unlockPageScroll)

onUnmounted(unlockPageScroll)

function lockPageScroll() {
  if (typeof document !== 'undefined') {
    document.body.classList.add(bodyScrollLockClass)
  }
}

function unlockPageScroll() {
  if (typeof document !== 'undefined') {
    document.body.classList.remove(bodyScrollLockClass)
  }
}

function openComposer() {
  composerOpen.value = true
}

function closeComposer() {
  composerOpen.value = false
}

function showRandomMood() {
  const mood = pickRandomMood()
  if (!mood) {
    viewedMood.value = undefined
    showToast('暂时还没有心情')
    return
  }
  viewedMood.value = mood
  moodDetailOpen.value = true
}

function pickRandomMood() {
  const latestMoods = content.treeholeFeed.slice(0, 8)
  if (latestMoods.length === 0) return undefined
  const index = Math.floor(Math.random() * latestMoods.length)
  return latestMoods[index]
}

function closeMoodDetail() {
  moodDetailOpen.value = false
  replyDraft.value = ''
  replyError.value = ''
  replySubmitting.value = false
  treeholeContextStatus.value = ''
}

function maskNickname(name: string) {
  const chars = Array.from(name)
  if (chars.length <= 1) return name
  if (chars.length === 2) return `${chars[0]}*`
  return `${chars[0]}${'*'.repeat(Math.min(2, chars.length - 2))}${chars[chars.length - 1]}`
}

function genderLabel(gender: TreeholeGender) {
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
}

async function publish() {
  if (content.submitting || !draft.value.trim()) return
  if (!ensureQuota('treehole_post')) return
  const post = await content.publishTreehole(draft.value.trim())
  draft.value = ''
  viewedMood.value = post
  composerOpen.value = false
  showToast('已发布到树洞')
}

function clearReplyError() {
  if (replyError.value && replyDraft.value.trim()) replyError.value = ''
  treeholeContextStatus.value = ''
}

function contextStatusText(status: string, conversationId?: string) {
  if (status === 'active') {
    return conversationId ? '继续聊已开启，正在进入临时会话' : '继续聊已开启'
  }
  if (status === 'blocked') return '对方或你已拉黑，无法继续聊'
  if (status === 'expired') return '继续聊申请已过期'
  if (status === 'reported' || status === 'risk_frozen') return '继续聊申请已进入风控处理'
  return '继续聊申请已发出，等待对方确认'
}

async function replyMood() {
  if (replySubmitting.value || !viewedMood.value) return
  const replyContent = replyDraft.value.trim()
  if (!replyContent) {
    replyError.value = '回复不能为空'
    showToast('回复不能为空')
    return
  }
  replySubmitting.value = true
  treeholeContextStatus.value = ''
  try {
    const mood = viewedMood.value
    await content.replyTreehole(mood.id, replyContent)
    const contextRequest = await content.createContextChatRequest({
      targetUserId: mood.authorId,
      sourceType: 'treehole_comment',
      sourceId: mood.id,
      replyId: `tree_reply:${mood.id}`,
      initiatorAction: 'continue_chat',
      evidenceId: `treehole_reply:${mood.id}`
    })
    treeholeContextStatus.value = contextStatusText(contextRequest.status, contextRequest.conversationId)
    showToast(treeholeContextStatus.value)
    if (contextRequest.status === 'active' && contextRequest.conversationId) {
      closeMoodDetail()
      navigateTo(`/pages/messages/chat?contextConversationId=${contextRequest.conversationId}`)
      return
    }
    replyDraft.value = ''
    replyError.value = ''
  } catch {
    replyError.value = '回复或继续聊申请失败，请稍后再试'
  } finally {
    replySubmitting.value = false
  }
}
</script>

<style scoped lang="scss">
.treehole-page {
  position: relative;
  display: grid;
  grid-template-rows: minmax(0, 1fr) 306rpx;
  width: 100vw;
  height: calc(100vh - var(--window-top, 0px) - var(--window-bottom, 0px));
  min-height: 0;
  max-height: calc(100vh - var(--window-top, 0px) - var(--window-bottom, 0px));
  padding: 0 0 calc(132rpx + env(safe-area-inset-bottom));
  overflow: hidden;
  background:
    radial-gradient(circle at 18% 8%, rgba(139, 192, 151, 0.2), transparent 31%),
    radial-gradient(circle at 90% 64%, rgba(215, 173, 104, 0.16), transparent 28%),
    linear-gradient(180deg, #fbfbf1 0%, #edf6ed 45%, #e1ece5 100%);
}

.treehole-page.safe-bottom {
  padding-bottom: calc(132rpx + env(safe-area-inset-bottom));
}

:global(body.treehole-lock-scroll) {
  overflow: hidden;
}

:global(body.treehole-lock-scroll uni-page-body),
:global(body.treehole-lock-scroll .uni-page-body) {
  overflow: hidden;
}

.tree-scene {
  position: relative;
  width: 100%;
  max-width: 750rpx;
  height: 100%;
  min-height: 0;
  margin: 0 auto;
  box-sizing: border-box;
  overflow: hidden;
}

.sky-glow,
.leaf,
.falling-leaves,
.falling-leaf,
.canopy-light {
  position: absolute;
  pointer-events: none;
}

.sky-glow {
  border-radius: 50%;
  filter: blur(8px);
  animation: glow-pulse 5.2s ease-in-out infinite;
}

.glow-left {
  top: 18rpx;
  left: 24rpx;
  width: 230rpx;
  height: 230rpx;
  background: rgba(85, 153, 124, 0.14);
}

.glow-right {
  right: 18rpx;
  bottom: 28rpx;
  width: 220rpx;
  height: 220rpx;
  background: rgba(215, 173, 104, 0.13);
  animation-delay: 1.4s;
}

.leaf {
  z-index: 2;
  width: 25rpx;
  height: 46rpx;
  border-radius: 62% 14% 62% 14%;
  background: linear-gradient(145deg, #8fc985, #3f9872);
  box-shadow: 0 10rpx 24rpx rgba(37, 92, 74, 0.16);
  animation: leaf-float 5.8s ease-in-out infinite;
}

.leaf-a {
  top: 116rpx;
  left: 80rpx;
}

.leaf-b {
  top: 198rpx;
  right: 92rpx;
  transform: rotate(24deg);
  animation-delay: 1.4s;
}

.leaf-c {
  bottom: 78rpx;
  left: 132rpx;
  transform: rotate(-16deg);
  animation-delay: 2.1s;
}

.falling-leaves {
  inset: 0;
  z-index: 6;
  overflow: hidden;
}

.falling-leaf {
  top: -72rpx;
  width: 15rpx;
  height: 30rpx;
  border-radius: 68% 12% 68% 12%;
  background:
    radial-gradient(circle at 34% 28%, rgba(255, 255, 210, 0.44), transparent 32%),
    linear-gradient(145deg, #9fcf82, #3a9a69 58%, #28785d);
  box-shadow: 0 8rpx 18rpx rgba(37, 92, 74, 0.08);
  opacity: 0;
  transform-origin: 50% 100%;
  animation: leaf-fall 13s linear infinite;
}

.falling-leaf-1 {
  left: 9%;
  width: 14rpx;
  height: 28rpx;
  animation-duration: 13.8s;
  animation-delay: -1.2s;
}

.falling-leaf-2 {
  left: 24%;
  animation-duration: 16.4s;
  animation-delay: -6.8s;
}

.falling-leaf-3 {
  left: 43%;
  width: 18rpx;
  height: 34rpx;
  animation-duration: 15.2s;
  animation-delay: -3.4s;
}

.falling-leaf-4 {
  left: 62%;
  animation-duration: 17s;
  animation-delay: -9.6s;
}

.falling-leaf-5 {
  left: 78%;
  width: 13rpx;
  height: 27rpx;
  animation-duration: 14.6s;
  animation-delay: -4.8s;
}

.falling-leaf-6 {
  left: 91%;
  width: 16rpx;
  height: 31rpx;
  animation-duration: 18.2s;
  animation-delay: -12.2s;
}

.tree-wrap {
  position: absolute;
  left: 50%;
  top: clamp(16rpx, 3vh, 50rpx);
  width: 590rpx;
  height: 610rpx;
  transform: translateX(-50%);
  animation: tree-breathe 5.6s ease-in-out infinite;
}

.canopy {
  position: absolute;
  border-radius: 48% 52% 50% 50% / 48% 42% 58% 52%;
  background:
    radial-gradient(circle at 34% 24%, rgba(245, 255, 217, 0.68), transparent 25%),
    radial-gradient(circle at 72% 74%, rgba(32, 120, 90, 0.24), transparent 36%),
    linear-gradient(145deg, #a9d384 0%, #58aa73 48%, #287c68 100%);
  box-shadow:
    inset 16rpx 18rpx 38rpx rgba(255, 255, 255, 0.2),
    inset -18rpx -22rpx 44rpx rgba(20, 83, 68, 0.18),
    0 24rpx 48rpx rgba(37, 91, 71, 0.13);
}

.cloud-back {
  left: 92rpx;
  top: 62rpx;
  width: 410rpx;
  height: 330rpx;
  opacity: 0.9;
  transform: rotate(-3deg);
}

.cloud-left {
  left: 0;
  top: 170rpx;
  width: 318rpx;
  height: 300rpx;
  background:
    radial-gradient(circle at 35% 25%, rgba(240, 252, 212, 0.62), transparent 27%),
    linear-gradient(145deg, #83bd75 0%, #3e966e 58%, #236d60 100%);
  transform: rotate(-13deg);
}

.cloud-top {
  left: 150rpx;
  top: 0;
  width: 290rpx;
  height: 292rpx;
  background:
    radial-gradient(circle at 38% 23%, rgba(251, 255, 221, 0.78), transparent 27%),
    linear-gradient(145deg, #b3d989 0%, #67b173 56%, #337d67 100%);
}

.cloud-right {
  right: 0;
  top: 152rpx;
  width: 318rpx;
  height: 304rpx;
  background:
    radial-gradient(circle at 36% 22%, rgba(236, 249, 208, 0.66), transparent 26%),
    linear-gradient(145deg, #7fc077 0%, #37936d 58%, #1e6a61 100%);
  transform: rotate(12deg);
}

.cloud-front {
  left: 122rpx;
  top: 214rpx;
  width: 350rpx;
  height: 286rpx;
  background:
    radial-gradient(circle at 38% 22%, rgba(232, 250, 205, 0.5), transparent 26%),
    radial-gradient(circle at 58% 78%, rgba(18, 92, 76, 0.25), transparent 34%),
    linear-gradient(145deg, #6fb873 0%, #2f8f69 62%, #1d635d 100%);
  box-shadow:
    inset 14rpx 18rpx 38rpx rgba(255, 255, 255, 0.17),
    0 32rpx 60rpx rgba(31, 84, 70, 0.19);
}

.canopy-light {
  left: 134rpx;
  top: 128rpx;
  width: 320rpx;
  height: 320rpx;
  border-radius: 50%;
  border: 2rpx solid rgba(255, 255, 255, 0.22);
  box-shadow:
    0 0 74rpx rgba(226, 248, 210, 0.62),
    inset 0 0 52rpx rgba(248, 255, 226, 0.24);
}

.hollow-shell {
  position: absolute;
  left: 50%;
  top: 292rpx;
  z-index: 5;
  width: 282rpx;
  min-height: 306rpx;
  padding: 10rpx;
  border-radius: 52% 48% 48% 52% / 43% 41% 59% 57%;
  background:
    linear-gradient(145deg, rgba(232, 191, 111, 0.76), rgba(111, 74, 39, 0.68)),
    rgba(255, 231, 175, 0.28);
  box-shadow: 0 0 48rpx rgba(255, 218, 136, 0.3);
  box-sizing: border-box;
  transform: translate(-50%, -50%);
}

.tree-hollow {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 286rpx;
  padding: 30rpx 24rpx;
  border-radius: inherit;
  background:
    radial-gradient(circle at 48% 28%, rgba(255, 238, 187, 0.16), transparent 29%),
    radial-gradient(circle at 50% 80%, rgba(0, 0, 0, 0.24), transparent 44%),
    linear-gradient(180deg, rgba(48, 31, 23, 0.95), rgba(80, 51, 32, 0.98));
  box-shadow: inset 0 20rpx 50rpx rgba(0, 0, 0, 0.46);
  box-sizing: border-box;
}

.hollow-kicker {
  color: #d8c391;
  font-size: 21rpx;
  font-weight: 800;
}

.hollow-title {
  margin-top: 8rpx;
  color: #fff6da;
  font-size: 28rpx;
  font-weight: 800;
  line-height: 1.25;
}

.hollow-content {
  display: block;
  width: 100%;
  margin-top: 15rpx;
  color: rgba(255, 248, 224, 0.92);
  font-size: 23rpx;
  line-height: 1.62;
  text-align: center;
}

.hollow-meta {
  display: flex;
  gap: 12rpx;
  margin-top: 18rpx;
  color: rgba(255, 238, 194, 0.76);
  font-size: 21rpx;
}

.branch {
  position: absolute;
  top: 382rpx;
  z-index: 3;
  width: 138rpx;
  height: 52rpx;
  border-radius: 999px;
  background: linear-gradient(180deg, #865632, #5e3d27);
}

.branch-left {
  left: 154rpx;
  transform: rotate(-32deg);
}

.branch-right {
  right: 154rpx;
  transform: rotate(32deg);
}

.tree-trunk {
  position: absolute;
  left: 50%;
  top: 372rpx;
  z-index: 4;
  width: 156rpx;
  height: 250rpx;
  border-radius: 50rpx 50rpx 28rpx 28rpx;
  background:
    radial-gradient(ellipse at 50% 12%, rgba(222, 165, 86, 0.34), transparent 38%),
    linear-gradient(90deg, rgba(66, 42, 28, 0.2), transparent 30%, rgba(255, 218, 153, 0.14) 54%, rgba(51, 32, 22, 0.26)),
    linear-gradient(180deg, #966438, #694129 72%, #563521);
  box-shadow: 0 24rpx 44rpx rgba(71, 52, 38, 0.18);
  transform: translateX(-50%);
}

.trunk-shine {
  position: absolute;
  left: 50%;
  top: 8rpx;
  width: 52rpx;
  height: 224rpx;
  border-radius: 999px;
  background: linear-gradient(180deg, rgba(225, 166, 85, 0.28), rgba(225, 166, 85, 0));
  transform: translateX(-50%);
}

.trunk-line {
  position: absolute;
  top: 52rpx;
  width: 24rpx;
  height: 168rpx;
  border-radius: 999px;
  background: rgba(55, 34, 24, 0.19);
}

.trunk-line.left {
  left: 36rpx;
  transform: rotate(6deg);
}

.trunk-line.right {
  right: 34rpx;
  transform: rotate(-7deg);
}

.tree-ground {
  position: absolute;
  left: 50%;
  bottom: 8rpx;
  z-index: 1;
  width: 560rpx;
  height: 76rpx;
  border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(54, 119, 79, 0.19), rgba(54, 119, 79, 0));
  transform: translateX(-50%);
}

.floating-action {
  position: absolute;
  z-index: 7;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 132rpx;
  height: 132rpx;
  border: 1px solid rgba(255, 255, 255, 0.72);
  border-radius: 50%;
  color: #fff;
  box-sizing: border-box;
  box-shadow:
    0 18rpx 44rpx rgba(35, 91, 74, 0.2),
    0 0 38rpx rgba(255, 255, 255, 0.36);
  animation: action-float 4.2s ease-in-out infinite;
}

.action-count {
  position: absolute;
  top: -10rpx;
  right: -12rpx;
  min-width: 62rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.9);
  border-radius: 999px;
  padding: 7rpx 13rpx;
  color: #fff;
  background: #ff3b30;
  box-shadow: 0 10rpx 22rpx rgba(255, 59, 48, 0.25);
  font-size: 20rpx;
  font-weight: 900;
  line-height: 1;
  text-align: center;
  box-sizing: border-box;
}

.floating-action:active {
  transform: scale(0.96);
}

.write-action {
  left: 88rpx;
  top: 474rpx;
  background:
    radial-gradient(circle at 30% 22%, rgba(255, 255, 255, 0.36), transparent 34%),
    linear-gradient(145deg, #d27f6b, #a9526b);
}

.read-action {
  top: 474rpx;
  right: 88rpx;
  left: auto;
  background:
    radial-gradient(circle at 30% 22%, rgba(255, 255, 255, 0.36), transparent 34%),
    linear-gradient(145deg, #45a58d, #236f75);
  animation-delay: 1.1s;
}

.action-main {
  font-size: 27rpx;
  font-weight: 900;
  line-height: 1.2;
}

.action-sub {
  margin-top: 6rpx;
  color: rgba(255, 255, 255, 0.8);
  font-size: 19rpx;
  font-weight: 700;
}

.mood-dock {
  position: relative;
  z-index: 10;
  align-self: stretch;
  width: 100%;
  max-width: 750rpx;
  margin: 0 auto;
  padding: 0 24rpx 18rpx;
  background: transparent;
  box-sizing: border-box;
  pointer-events: none;
  overflow: hidden;
}

.mood-window {
  height: 100%;
  overflow: hidden;
}

.mood-track {
  display: grid;
  gap: 8rpx;
  animation: mood-track-slide 28s linear infinite;
}

.mood-item {
  display: flex;
  gap: 12rpx;
  width: 100%;
  min-height: 74rpx;
  border: 1px solid rgba(255, 255, 255, 0.74);
  border-radius: 16px;
  padding: 10rpx 14rpx;
  background:
    radial-gradient(circle at 92% 12%, rgba(255, 255, 255, 0.76), transparent 30%),
    rgba(255, 255, 255, 0.86);
  box-sizing: border-box;
  box-shadow: 0 14rpx 32rpx rgba(31, 54, 58, 0.08);
  backdrop-filter: blur(12px);
}

.mood-card-0 {
  transform: none;
}

.mood-card-1 {
  transform: none;
}

.mood-card-2 {
  transform: none;
}

.mood-card-3 {
  transform: none;
}

.avatar,
.composer-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  color: #fff;
  background: #7a8790;
  font-size: 24rpx;
  font-weight: 900;
  overflow: hidden;
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.avatar.female,
.composer-avatar.female {
  background: linear-gradient(145deg, #d47a88, #a9526b);
}

.avatar.male,
.composer-avatar.male {
  background: linear-gradient(145deg, #49a391, #236f75);
}

.mood-body {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  padding-right: 8rpx;
}

.mood-top {
  display: flex;
  align-items: center;
  gap: 10rpx;
  min-height: 32rpx;
}

.nickname {
  color: #172126;
  font-size: 24rpx;
  font-weight: 900;
}

.gender-tag {
  border-radius: 999px;
  padding: 4rpx 12rpx;
  color: #5d6870;
  background: rgba(93, 104, 112, 0.1);
  font-size: 19rpx;
  font-weight: 800;
}

.gender-tag.female {
  color: #9c4e68;
  background: rgba(210, 127, 107, 0.14);
}

.gender-tag.male {
  color: #236f75;
  background: rgba(69, 165, 141, 0.14);
}

.mood-text {
  display: block;
  margin-top: 6rpx;
  color: #324044;
  font-size: 22rpx;
  line-height: 1.35;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-mood {
  padding: 42rpx 0;
  color: #65757b;
  font-size: 24rpx;
  text-align: center;
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
  background: rgba(20, 35, 32, 0.34);
  backdrop-filter: blur(14px);
}

.modal-card {
  width: 100%;
  max-width: 520px;
  border: 1px solid rgba(255, 255, 255, 0.78);
  border-radius: 18px;
  padding: 28rpx;
  background:
    radial-gradient(circle at 92% 12%, rgba(223, 175, 91, 0.15), transparent 28%),
    rgba(255, 255, 255, 0.98);
  box-sizing: border-box;
  box-shadow: 0 30rpx 76rpx rgba(14, 31, 28, 0.24);
}

.composer-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18rpx;
}

.mood-detail-card {
  display: grid;
  gap: 22rpx;
}

.detail-user {
  display: flex;
  align-items: center;
  gap: 18rpx;
}

.detail-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 92rpx;
  height: 92rpx;
  border: 3rpx solid rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  color: #fff;
  background: #7a8790;
  box-shadow: 0 12rpx 28rpx rgba(31, 54, 58, 0.16);
  overflow: hidden;
  font-size: 32rpx;
  font-weight: 900;
}

.detail-avatar.female {
  background: linear-gradient(145deg, #d47a88, #a9526b);
}

.detail-avatar.male {
  background: linear-gradient(145deg, #49a391, #236f75);
}

.detail-user-main {
  flex: 1;
  min-width: 0;
}

.detail-name-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10rpx;
}

.detail-name {
  color: #172126;
  font-size: 30rpx;
  font-weight: 900;
}

.age-tag {
  border-radius: 999px;
  padding: 4rpx 12rpx;
  color: #7a4a10;
  background: rgba(194, 122, 53, 0.14);
  font-size: 20rpx;
  font-weight: 800;
}

.detail-content {
  display: block;
  border-radius: 14px;
  padding: 22rpx;
  color: #25323c;
  background: rgba(244, 249, 244, 0.9);
  font-size: 29rpx;
  line-height: 1.7;
}

.detail-meta {
  display: flex;
  gap: 16rpx;
  color: #65757b;
  font-size: 23rpx;
  font-weight: 700;
}

.reply-input {
  width: 100%;
  min-height: 142rpx;
  border: 1px solid rgba(35, 108, 114, 0.12);
  border-radius: 12px;
  padding: 18rpx;
  color: #172126;
  background: rgba(251, 253, 249, 0.96);
  box-sizing: border-box;
  font-size: 26rpx;
  line-height: 1.5;
}

.reply-error {
  display: block;
  margin-top: -8rpx;
  color: #b94747;
  font-size: 23rpx;
  font-weight: 800;
}

.context-chat-copy {
  display: block;
  margin-top: -4rpx;
  color: #236c72;
  font-size: 23rpx;
  font-weight: 800;
  line-height: 1.45;
}

.detail-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
}

.detail-actions .button {
  min-height: 76rpx;
}

.hint {
  display: block;
  margin-top: 10rpx;
}

.textarea {
  width: 100%;
  min-height: 220rpx;
  margin: 22rpx 0;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 8px;
  background: #fbfdf9;
  padding: 20rpx;
  box-sizing: border-box;
  color: #172126;
  font-size: 28rpx;
  line-height: 1.55;
}

.modal-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
}

@keyframes tree-breathe {
  0%,
  100% {
    transform: translateX(-50%) scale(1);
    filter: saturate(1);
  }
  50% {
    transform: translateX(-50%) scale(1.012);
    filter: saturate(1.06);
  }
}

@keyframes action-float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-16rpx);
  }
}

@keyframes glow-pulse {
  0%,
  100% {
    opacity: 0.66;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.08);
  }
}

@keyframes leaf-float {
  0%,
  100% {
    opacity: 0.74;
    transform: translateY(0) rotate(-10deg);
  }
  50% {
    opacity: 1;
    transform: translateY(-22rpx) rotate(8deg);
  }
}

@keyframes leaf-fall {
  0% {
    opacity: 0;
    transform: translate3d(0, -80rpx, 0) rotate(-28deg);
  }
  8% {
    opacity: 0.48;
  }
  26% {
    transform: translate3d(34rpx, 22vh, 0) rotate(86deg);
  }
  52% {
    transform: translate3d(-24rpx, 48vh, 0) rotate(178deg);
  }
  78% {
    opacity: 0.42;
    transform: translate3d(42rpx, 72vh, 0) rotate(272deg);
  }
  100% {
    opacity: 0;
    transform: translate3d(-16rpx, 104vh, 0) rotate(360deg);
  }
}

@keyframes mood-track-slide {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-50%);
  }
}

@media (min-width: 720px) {
  .tree-scene {
    height: 100%;
  }

  .tree-wrap {
    width: 560px;
    height: 560px;
    top: 22px;
  }

  .mood-dock {
    max-width: 620px;
    margin: 0 auto;
  }

  .mood-window {
    height: 100%;
  }
}
</style>
