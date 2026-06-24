<template>
  <view class="bottle-screen">
    <view class="ambient-sky">
      <view class="moon" />
      <view class="star star-a" />
      <view class="star star-b" />
      <view class="star star-c" />
      <view class="horizon-mist" />
    </view>

    <view class="ocean" :class="{ catching: isCatching, throwing: isThrowing }">
      <view class="current current-a" />
      <view class="current current-b" />
      <view class="bottle-float" @tap="fish">
        <view class="bottle-cork" />
        <view class="bottle-lip" />
        <view class="bottle-neck" />
        <view class="bottle-body">
          <view class="glass-shine shine-a" />
          <view class="glass-shine shine-b" />
          <view class="paper" />
          <view class="bottle-label">漂</view>
        </view>
      </view>
      <view v-if="isCatching" class="catch-beam" />
      <view v-if="isCatching" class="catch-ring ring-a" />
      <view v-if="isCatching" class="catch-ring ring-b" />
      <view class="wave wave-a" />
      <view class="wave wave-b" />
      <view class="wave wave-c" />
      <view class="wave wave-d" />
    </view>

    <view class="screen-header">
      <view>
        <text class="screen-title">漂流瓶</text>
        <text class="screen-subtitle">让海浪替你遇见一个人</text>
      </view>
    </view>

    <view class="filter-dock">
      <view class="filter-chip" @tap="openFilterModal">
        <view class="filter-chip-icon">
          <view class="slider-line line-a" />
          <view class="slider-line line-b" />
        </view>
        <view class="filter-chip-text">
          <text>筛选</text>
          <text class="filter-summary">{{ filterSummary }}</text>
        </view>
      </view>
    </view>

    <view class="bottom-actions">
      <view class="action-button catch" @tap="fish">
        <text class="action-main">捞</text>
        <text class="action-badge">+{{ fishLeft }}</text>
      </view>
      <view class="action-button throw" @tap="openThrowModal">
        <text class="action-main">扔</text>
        <text class="action-badge red">+{{ throwLeft }}</text>
      </view>
    </view>

    <view v-if="throwOpen" class="modal-mask center-mask">
      <view class="modal-card throw-card" @tap.stop @click.stop>
        <view class="textarea-shell">
          <textarea
            v-model="draft"
            class="textarea"
            maxlength="240"
            placeholder="写一句秘密、愿望、吐槽，或今晚不想对熟人说的话。"
            @input="clearThrowError"
          />
          <view class="random-tip-button" @tap.stop="fillRandomPrompt" @click.stop="fillRandomPrompt">
            {{ randomPromptLoading ? '生成中' : '随机' }}
          </view>
        </view>
        <text v-if="throwError" class="throw-error">{{ throwError }}</text>
        <view class="option-block">
          <text class="field-label">谁可以捞</text>
          <view class="choice-row">
            <view
              v-for="item in audienceOptions"
              :key="item.value"
              class="choice-chip"
              :class="{ active: throwTargetGender === item.value }"
              @tap.stop="throwTargetGender = item.value"
              @click.stop="throwTargetGender = item.value"
            >
              {{ item.label }}
            </view>
          </view>
        </view>
        <view class="option-block">
          <text class="field-label">范围</text>
          <view class="choice-row">
            <view
              v-for="area in targetAreaOptions"
              :key="area.value"
              class="choice-chip"
              :class="{ active: throwTargetScope === area.value }"
              @tap.stop="throwTargetScope = area.value"
              @click.stop="throwTargetScope = area.value"
            >
              {{ area.label }}
            </view>
          </view>
        </view>
        <view class="modal-actions">
          <view class="button ghost" @tap.stop="closeThrow" @click.stop="closeThrow">取消</view>
          <view class="button" :class="{ disabled: content.submitting || !draft.trim() }" @tap.stop="submitBottle" @click.stop="submitBottle">扔出去</view>
        </view>
      </view>
    </view>

    <view v-if="caughtOpen && content.currentBottle" class="modal-mask center-mask">
      <view class="modal-card caught-card" @tap.stop @click.stop>
        <view class="caught-author">
          <view class="author-avatar">{{ content.currentBottle.authorAvatarText || content.currentBottle.authorName.slice(0, 1) }}</view>
          <view class="author-main">
            <view class="author-line">
              <text class="author-name">{{ content.currentBottle.authorName }}</text>
              <text v-if="content.currentBottle.authorVip" class="mini-tag vip">VIP</text>
            </view>
            <view class="meta-tags">
              <text v-if="content.currentBottle.authorVerified" class="mini-tag verified">已认证</text>
              <text class="mini-tag">{{ genderLabel(content.currentBottle.authorGender) }}</text>
              <text v-if="content.currentBottle.authorAgeRange" class="mini-tag">{{ content.currentBottle.authorAgeRange }}</text>
              <text v-if="content.currentBottle.authorCity" class="mini-tag">{{ content.currentBottle.authorCity }}</text>
            </view>
          </view>
          <view class="follow-pill" @tap.stop="follow" @click.stop="follow">
            <text class="follow-dot">关</text>
            <text>{{ content.currentBottle.isFollowing ? '已关注' : '关注' }}</text>
          </view>
        </view>
        <text class="caught-message">{{ content.currentBottle.content }}</text>
        <input v-model="reply" class="input" placeholder="写一句温柔回应" @input="clearReplyError" />
        <text v-if="replyError" class="reply-error">{{ replyError }}</text>
        <view class="reply-actions">
          <view class="button ghost return-button" @tap.stop="releaseBottle" @click.stop="releaseBottle">扔回海里</view>
          <view class="button secondary reply-button" @tap.stop="sendReply" @click.stop="sendReply">回应</view>
        </view>
        <view class="report-link" @tap.stop="openReportModal" @click.stop="openReportModal">举报/拉黑</view>
      </view>
    </view>

    <view v-if="reportOpen && content.currentBottle" class="modal-mask center-mask">
      <view class="modal-card report-card" @tap.stop="handleReportAction" @click.stop="handleReportAction">
        <text class="modal-kicker">安全处理</text>
        <text class="modal-title">举报或拉黑 {{ content.currentBottle.authorName }}</text>
        <text class="report-desc">举报会进入后台审核队列；拉黑后，后续不会再推荐这个用户的瓶子。</text>
        <view class="choice-row report-reasons">
          <view
            v-for="reason in reportReasons"
            :key="reason"
            class="choice-chip"
            :class="{ active: reportReason === reason }"
            @tap="reportReason = reason"
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
          />
        </view>
        <view class="report-preview">
          <text class="field-label">相关瓶子</text>
          <text>{{ content.currentBottle.content }}</text>
        </view>
        <view class="modal-actions report-actions">
          <view class="button ghost" data-action="cancel">取消</view>
          <view class="button ghost danger-ghost" data-action="block">拉黑并扔回</view>
          <view class="button" data-action="report">提交举报</view>
        </view>
      </view>
    </view>

    <view v-if="filterOpen" class="modal-mask center-mask">
      <view class="modal-card filter-card" @tap.stop>
        <text class="modal-kicker">筛选</text>
        <text class="modal-title">选择你想遇见的人</text>
        <ExploreFilters v-model="draftFilters" mode="chips" />
        <view class="modal-actions filter-actions">
          <view class="button ghost" @tap="cancelFilter">取消</view>
          <view class="button" @tap="saveFilter">保存</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import ExploreFilters, { type ExploreFilterValue } from '@/components/ExploreFilters.vue'
import { useQuotaGuard } from '@/composables/useQuotaGuard'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { BottleTargetGender, Bottle, BottleTargetScope } from '@/types/domain'

const app = useAppStore()
const content = useContentStore()
const { ensureQuota } = useQuotaGuard()
const draft = ref('')
const throwError = ref('')
const reply = ref('')
const replyError = ref('')
const throwOpen = ref(false)
const caughtOpen = ref(false)
const filterOpen = ref(false)
const reportOpen = ref(false)
const reportSubmitting = ref(false)
const blockSubmitting = ref(false)
const replySubmitting = ref(false)
const randomPromptLoading = ref(false)
const isCatching = ref(false)
const isThrowing = ref(false)
const filters = ref<ExploreFilterValue>({ city: '全国', gender: '全部', ageRange: '全部' })
const draftFilters = ref<ExploreFilterValue>({ ...filters.value })
const throwTargetGender = ref<BottleTargetGender>('all')
const throwTargetScope = ref<BottleTargetScope>('all')
const reportReason = ref('骚扰或不友善')
const reportDescription = ref('')

const audienceOptions: Array<{ label: string; value: BottleTargetGender }> = [
  { label: '默认', value: 'all' },
  { label: '男', value: 'male' },
  { label: '女', value: 'female' }
]
const targetAreaOptions: Array<{ label: string; value: BottleTargetScope }> = [
  { label: '默认', value: 'all' },
  { label: '同城优先', value: 'same_city' },
  { label: '附近优先', value: 'nearby' }
]
const reportReasons = ['骚扰或不友善', '低俗违规', '广告引流', '虚假资料', '其他问题']

const fishLeft = computed(() => app.quotas?.fish_bottle.remaining ?? 0)
const throwLeft = computed(() => app.quotas?.throw_bottle.remaining ?? 0)
const filterSummary = computed(() => `${filters.value.city} · ${filters.value.gender} · ${filters.value.ageRange}`)

onLoad(() => app.hydrate())

function openThrowModal() {
  if (!ensureQuota('throw_bottle')) return
  resetThrowDraft()
  throwOpen.value = true
}

function closeThrow() {
  throwOpen.value = false
  resetThrowDraft()
}

function resetThrowDraft() {
  draft.value = ''
  throwError.value = ''
  throwTargetGender.value = 'all'
  throwTargetScope.value = 'all'
}

async function submitBottle() {
  if (!ensureQuota('throw_bottle')) return
  if (!draft.value.trim()) {
    throwError.value = '先写一点内容，才能扔出去'
    showToast('先写一点内容，才能扔出去')
    return
  }
  isThrowing.value = true
  await content.throwBottle(draft.value.trim(), {
    targetGender: throwTargetGender.value,
    targetScope: throwTargetScope.value
  })
  setTimeout(() => {
    isThrowing.value = false
  }, 850)
  throwOpen.value = false
  resetThrowDraft()
  showToast('瓶子已漂走，扔瓶 -1')
}

async function fillRandomPrompt() {
  if (randomPromptLoading.value) return
  randomPromptLoading.value = true
  try {
    draft.value = await content.getRandomBottlePrompt()
    throwError.value = ''
  } finally {
    randomPromptLoading.value = false
  }
}

function clearThrowError() {
  if (throwError.value && draft.value.trim()) throwError.value = ''
}

async function fish() {
  if (isCatching.value) return
  if (!ensureQuota('fish_bottle')) return
  caughtOpen.value = false
  reportOpen.value = false
  replyError.value = ''
  isCatching.value = true
  try {
    await new Promise((resolve) => setTimeout(resolve, 1450))
    await content.fishBottle(filters.value)
    caughtOpen.value = true
  } catch (error) {
    const message = error instanceof Error && error.message === 'NO_MATCHED_BOTTLE'
      ? '没有符合筛选条件的瓶子'
      : '暂时没有捞到瓶子'
    showToast(message)
  } finally {
    isCatching.value = false
  }
}

async function sendReply() {
  if (!content.currentBottle || replySubmitting.value) return
  if (!reply.value.trim()) {
    replyError.value = '请先写一句回应'
    showToast('请先写一句回应')
    return
  }
  replySubmitting.value = true
  try {
    await content.replyBottle(content.currentBottle.id, reply.value.trim())
    reply.value = ''
    replyError.value = ''
    reportOpen.value = false
    caughtOpen.value = false
    showToast('回应已送达')
  } finally {
    replySubmitting.value = false
  }
}

function clearReplyError() {
  if (replyError.value && reply.value.trim()) replyError.value = ''
}

async function follow() {
  if (!content.currentBottle) return
  await content.followUser(content.currentBottle.authorId)
  showToast('已关注')
}

function releaseBottle() {
  reply.value = ''
  replyError.value = ''
  reportOpen.value = false
  caughtOpen.value = false
  showToast('已扔回海里')
}

function openReportModal() {
  reportReason.value = '骚扰或不友善'
  reportDescription.value = ''
  reportSubmitting.value = false
  blockSubmitting.value = false
  reportOpen.value = true
}

function closeReportModal() {
  reportOpen.value = false
}

function getReportAction(event: Event) {
  const target = event.target as (HTMLElement & { dataset?: { action?: string } }) | null
  if (!target) return ''
  if (target.dataset?.action) return target.dataset.action
  const closest = typeof target.closest === 'function' ? target.closest('[data-action]') : null
  return (closest as (HTMLElement & { dataset?: { action?: string } }) | null)?.dataset?.action || ''
}

function handleReportAction(event: Event) {
  const action = getReportAction(event)
  if (action === 'cancel') closeReportModal()
  if (action === 'report') void submitReport()
  if (action === 'block') void submitBlock()
}

function buildReportReason() {
  const description = reportDescription.value.trim()
  return description ? `${reportReason.value}：${description}` : ''
}

async function submitReport() {
  if (!content.currentBottle || reportSubmitting.value) return
  const reason = buildReportReason()
  if (!reason) {
    showToast('请填写举报说明')
    return
  }
  reportSubmitting.value = true
  try {
    await content.reportBottle(content.currentBottle.id, reason)
    reportOpen.value = false
    showToast('举报已提交')
  } finally {
    reportSubmitting.value = false
  }
}

async function submitBlock() {
  if (!content.currentBottle || blockSubmitting.value) return
  const reason = buildReportReason()
  if (!reason) {
    showToast('请填写举报说明')
    return
  }
  blockSubmitting.value = true
  try {
    await content.reportBottle(content.currentBottle.id, reason)
    await content.blockUser(content.currentBottle.authorId, reason)
    reply.value = ''
    reportOpen.value = false
    caughtOpen.value = false
    showToast('已举报并拉黑')
  } finally {
    blockSubmitting.value = false
  }
}

function openFilterModal() {
  draftFilters.value = { ...filters.value }
  filterOpen.value = true
}

function cancelFilter() {
  draftFilters.value = { ...filters.value }
  filterOpen.value = false
}

function saveFilter() {
  filters.value = { ...draftFilters.value }
  filterOpen.value = false
  showToast('筛选已应用')
}

function genderLabel(gender?: Bottle['authorGender']) {
  if (gender === 'female') return '女'
  if (gender === 'male') return '男'
  return '未知'
}
</script>

<style scoped lang="scss">
.bottle-screen {
  position: relative;
  overflow: hidden;
  min-height: calc(100vh - var(--window-bottom));
  width: 100vw;
  background: linear-gradient(180deg, #dbeaf3 0%, #b8d8e5 36%, #8cc7d4 37%, #4f9aaf 100%);
  color: #fff;
}

.ambient-sky {
  position: absolute;
  inset: 0 0 auto 0;
  height: 48vh;
  background:
    radial-gradient(circle at 50% 100%, rgba(255, 255, 255, 0.44), transparent 5%),
    linear-gradient(180deg, #dceaf3, #a9ccdc);
}

.horizon-mist {
  position: absolute;
  left: -10%;
  right: -10%;
  bottom: -120rpx;
  height: 240rpx;
  background:
    radial-gradient(ellipse at 50% 44%, rgba(255, 255, 255, 0.32), transparent 58%),
    linear-gradient(180deg, rgba(169, 204, 220, 0), rgba(139, 208, 219, 0.52));
  filter: blur(10rpx);
  animation: mist-drift 8s ease-in-out infinite;
}

.moon {
  position: absolute;
  top: 92rpx;
  right: 88rpx;
  width: 86rpx;
  height: 86rpx;
  border-radius: 50%;
  background: #fff1bf;
  box-shadow: 0 0 66rpx rgba(255, 241, 191, 0.72);
}

.star {
  position: absolute;
  width: 7rpx;
  height: 7rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  animation: twinkle 2.4s ease-in-out infinite;
}

.star-a {
  top: 130rpx;
  left: 92rpx;
}

.star-b {
  top: 210rpx;
  left: 250rpx;
  animation-delay: -0.8s;
}

.star-c {
  top: 162rpx;
  right: 238rpx;
  animation-delay: -1.4s;
}

.ocean {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 74vh;
  background:
    radial-gradient(circle at 50% 12%, rgba(255, 255, 255, 0.24), transparent 18%),
    linear-gradient(180deg, rgba(139, 208, 219, 0) 0%, rgba(139, 208, 219, 0.76) 16%, #62afc2 60%, #438aa4);
}

.current {
  position: absolute;
  left: -20%;
  width: 140%;
  height: 300rpx;
  border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.16), transparent 68%);
  filter: blur(12rpx);
  animation: current-flow 8.5s ease-in-out infinite;
}

.current-a {
  top: 14vh;
}

.current-b {
  top: 44vh;
  opacity: 0.62;
  animation-delay: -3.5s;
}

.bottle-float {
  position: absolute;
  left: 50%;
  top: 18vh;
  z-index: 5;
  width: 236rpx;
  height: 150rpx;
  transform: translateX(-50%) rotate(-10deg);
  animation: bottle-drift 3.1s ease-in-out infinite;
  filter: drop-shadow(0 28rpx 38rpx rgba(31, 99, 118, 0.18));
}

.bottle-cork {
  position: absolute;
  top: 49rpx;
  right: 3rpx;
  z-index: 4;
  width: 38rpx;
  height: 38rpx;
  border-radius: 9rpx;
  background:
    linear-gradient(90deg, rgba(255, 255, 255, 0.18), transparent 28%),
    linear-gradient(135deg, #b7834c, #8b5b31);
  box-shadow:
    inset 0 0 0 2rpx rgba(255, 255, 255, 0.22),
    0 6rpx 14rpx rgba(83, 61, 37, 0.16);
}

.bottle-lip {
  position: absolute;
  top: 47rpx;
  right: 37rpx;
  z-index: 3;
  width: 25rpx;
  height: 43rpx;
  border-radius: 999px;
  background: rgba(236, 255, 252, 0.88);
  box-shadow: inset 0 0 0 2rpx rgba(255, 255, 255, 0.7);
}

.bottle-neck {
  position: absolute;
  top: 51rpx;
  right: 50rpx;
  z-index: 2;
  width: 92rpx;
  height: 36rpx;
  border-radius: 28rpx 16rpx 16rpx 28rpx;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.58), transparent 52%),
    linear-gradient(90deg, rgba(123, 214, 205, 0.62), rgba(243, 255, 252, 0.9));
  box-shadow:
    inset 0 0 0 2rpx rgba(255, 255, 255, 0.56),
    inset -8rpx -8rpx 16rpx rgba(50, 137, 150, 0.12);
}

.bottle-body {
  position: absolute;
  left: 0;
  top: 4rpx;
  width: 160rpx;
  height: 120rpx;
  border-radius: 68rpx 48rpx 50rpx 68rpx;
  background:
    radial-gradient(circle at 30% 22%, rgba(255, 255, 255, 0.94), transparent 16%),
    radial-gradient(circle at 68% 62%, rgba(129, 219, 213, 0.2), transparent 34%),
    linear-gradient(135deg, rgba(80, 190, 183, 0.54), rgba(237, 255, 253, 0.9));
  box-shadow:
    inset 0 0 0 4rpx rgba(255, 255, 255, 0.66),
    inset -17rpx -15rpx 24rpx rgba(60, 151, 158, 0.18),
    inset 14rpx 12rpx 18rpx rgba(255, 255, 255, 0.16);
}

.glass-shine {
  position: absolute;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.64);
}

.shine-a {
  left: 30rpx;
  top: 22rpx;
  width: 18rpx;
  height: 62rpx;
  transform: rotate(22deg);
}

.shine-b {
  left: 64rpx;
  top: 18rpx;
  width: 10rpx;
  height: 26rpx;
  transform: rotate(22deg);
}

.paper {
  position: absolute;
  left: 60rpx;
  top: 46rpx;
  width: 58rpx;
  height: 36rpx;
  border-radius: 7rpx;
  background: #fff0bd;
  box-shadow: 0 4rpx 8rpx rgba(121, 87, 44, 0.12);
  transform: rotate(5deg);
}

.bottle-label {
  position: absolute;
  left: 65rpx;
  top: 49rpx;
  width: 48rpx;
  height: 28rpx;
  color: #9a6a31;
  font-size: 18rpx;
  font-weight: 900;
  line-height: 28rpx;
  text-align: center;
  transform: rotate(5deg);
}

.wave {
  position: absolute;
  left: -12%;
  width: 124%;
  height: 96rpx;
  border-radius: 50%;
  background: transparent;
  border-top: 5rpx solid rgba(255, 255, 255, 0.26);
  box-shadow: 0 -18rpx 34rpx rgba(255, 255, 255, 0.05);
  animation: wave-move 5.4s ease-in-out infinite;
}

.wave-a {
  top: 23vh;
}

.wave-b {
  top: 33vh;
  opacity: 0.72;
  animation-delay: -1s;
}

.wave-c {
  top: 44vh;
  opacity: 0.52;
  animation-delay: -2s;
}

.wave-d {
  top: 55vh;
  opacity: 0.34;
  animation-delay: -2.8s;
}

.catch-beam {
  position: absolute;
  left: 50%;
  top: 6vh;
  z-index: 4;
  width: 260rpx;
  height: 390rpx;
  transform: translateX(-50%);
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.32), transparent 68%);
  animation: beam-pulse 1s ease-in-out infinite;
}

.catch-ring {
  position: absolute;
  left: 50%;
  top: 14vh;
  z-index: 6;
  width: 260rpx;
  height: 260rpx;
  border: 4rpx solid rgba(255, 255, 255, 0.92);
  border-radius: 50%;
  transform: translateX(-50%);
  animation: catch-ring 1.2s ease-out infinite;
}

.ring-b {
  animation-delay: -0.55s;
}

.catching .bottle-float {
  animation: bottle-catch 1.2s ease-in-out infinite;
}

.throwing .bottle-float {
  animation: bottle-throw 0.8s ease-in forwards;
}

.screen-header {
  position: absolute;
  left: 34rpx;
  right: 34rpx;
  top: calc(34rpx + var(--window-top) + env(safe-area-inset-top));
  z-index: 10;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  pointer-events: none;
}

.screen-title,
.screen-subtitle {
  display: block;
}

.screen-title {
  color: #173342;
  font-size: 44rpx;
  font-weight: 900;
  letter-spacing: 0;
}

.screen-subtitle {
  margin-top: 8rpx;
  color: rgba(23, 51, 66, 0.68);
  font-size: 25rpx;
}

.filter-chip {
  display: flex;
  align-items: center;
  gap: 7rpx;
  border-radius: 999px;
  padding: 7rpx 13rpx 7rpx 7rpx;
  color: #173342;
  background: rgba(247, 253, 254, 0.68);
  border: 1px solid rgba(255, 255, 255, 0.48);
  box-shadow: 0 10rpx 24rpx rgba(31, 91, 112, 0.08);
  backdrop-filter: blur(18px);
  font-weight: 800;
}

.filter-chip-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38rpx;
  height: 38rpx;
  border-radius: 50%;
  background: linear-gradient(145deg, rgba(79, 154, 175, 0.86), rgba(52, 127, 152, 0.86));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.34);
}

.slider-line {
  position: absolute;
  left: 10rpx;
  width: 18rpx;
  height: 3rpx;
  border-radius: 999px;
  background: #fff;
}

.slider-line::after {
  position: absolute;
  top: -4rpx;
  width: 9rpx;
  height: 9rpx;
  border-radius: 50%;
  background: #fff;
  content: '';
}

.line-a {
  top: 13rpx;
}

.line-a::after {
  left: 2rpx;
}

.line-b {
  top: 23rpx;
}

.line-b::after {
  right: 2rpx;
}

.filter-chip-text {
  display: flex;
  flex-direction: column;
  gap: 2rpx;
  font-size: 21rpx;
  line-height: 1.15;
}

.filter-summary {
  display: none;
  max-width: 160rpx;
  overflow: hidden;
  color: rgba(23, 51, 66, 0.52);
  font-size: 16rpx;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.filter-dock {
  position: absolute;
  left: 14rpx;
  top: 20vh;
  z-index: 11;
  display: flex;
  justify-content: flex-start;
}

.bottom-actions {
  position: absolute;
  left: 58rpx;
  right: 58rpx;
  bottom: calc(32rpx + var(--window-bottom) + env(safe-area-inset-bottom));
  z-index: 10;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16rpx;
}

.action-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 92rpx;
  border-radius: 24px;
  color: #fff;
  box-shadow: 0 18rpx 34rpx rgba(0, 0, 0, 0.22);
  backdrop-filter: blur(18px);
}

.catch {
  background: rgba(53, 139, 169, 0.94);
}

.throw {
  background: rgba(39, 64, 79, 0.9);
}

.action-main {
  font-size: 34rpx;
  font-weight: 900;
}

.action-badge {
  position: absolute;
  top: 12rpx;
  right: 14rpx;
  min-width: 34rpx;
  height: 34rpx;
  border-radius: 999px;
  background: #358ba9;
  color: #fff;
  font-size: 20rpx;
  font-weight: 900;
  line-height: 34rpx;
  text-align: center;
}

.action-badge.red {
  background: #ff3b30;
}

.modal-mask {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 28rpx 28rpx calc(28rpx + env(safe-area-inset-bottom));
  box-sizing: border-box;
  background: rgba(0, 0, 0, 0.34);
  backdrop-filter: blur(12px);
  animation: fade-in 160ms ease-out;
}

.modal-card {
  width: 100%;
  max-width: 520px;
  max-height: 86vh;
  overflow-y: auto;
  border-radius: 30px;
  padding: 34rpx;
  background: rgba(255, 255, 255, 0.96);
  color: #1d1d1f;
  box-sizing: border-box;
  box-shadow: 0 34rpx 80rpx rgba(0, 0, 0, 0.24);
  animation: sheet-up 210ms ease-out;
}

.center-mask {
  align-items: center;
}

.center-mask .modal-card {
  animation: dialog-pop 180ms ease-out;
}

.filter-card {
  max-width: 430px;
}

.throw-card {
  padding-top: 26rpx;
}

.textarea-shell {
  position: relative;
}

.throw-card .textarea {
  min-height: 260rpx;
  margin-top: 0;
  margin-bottom: 12rpx;
  padding-bottom: 76rpx;
}

.throw-card .option-block {
  margin-bottom: 18rpx;
}

.random-tip-button {
  position: absolute;
  right: 18rpx;
  bottom: 34rpx;
  min-width: 104rpx;
  border: 1px solid rgba(0, 113, 227, 0.14);
  border-radius: 999px;
  padding: 12rpx 20rpx;
  color: #0b6fcf;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 10rpx 24rpx rgba(0, 113, 227, 0.12);
  font-size: 24rpx;
  font-weight: 900;
  line-height: 1;
  text-align: center;
}

.throw-error {
  display: block;
  margin: 0 0 16rpx;
  color: #d64f4f;
  font-size: 24rpx;
  font-weight: 800;
}

.report-card {
  max-width: 480px;
}

.modal-kicker,
.modal-title {
  display: block;
}

.modal-kicker {
  color: #6e6e73;
  font-size: 24rpx;
  font-weight: 800;
}

.modal-title {
  margin-top: 10rpx;
  color: #1d1d1f;
  font-size: 38rpx;
  font-weight: 900;
  line-height: 1.3;
}

.textarea {
  width: 100%;
  min-height: 230rpx;
  margin: 26rpx 0 20rpx;
  border: 1px solid rgba(29, 29, 31, 0.08);
  border-radius: 20px;
  background: #f5f5f7;
  padding: 24rpx;
  color: #1d1d1f;
  box-sizing: border-box;
  font-size: 28rpx;
}

.option-block {
  margin-bottom: 22rpx;
}

.field-label {
  display: block;
  margin-bottom: 12rpx;
  color: #6e6e73;
  font-size: 24rpx;
  font-weight: 800;
}

.choice-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.choice-row.no-wrap {
  display: inline-flex;
  flex-wrap: nowrap;
  padding-bottom: 4rpx;
}

.city-scroll {
  width: 100%;
  white-space: nowrap;
}

.choice-chip {
  min-width: 96rpx;
  border: 1px solid rgba(29, 29, 31, 0.09);
  border-radius: 999px;
  padding: 14rpx 22rpx;
  color: #1d1d1f;
  background: #f5f5f7;
  font-size: 25rpx;
  font-weight: 800;
  text-align: center;
  box-sizing: border-box;
}

.choice-chip.active {
  border-color: rgba(0, 113, 227, 0.22);
  color: #fff;
  background: #0071e3;
  box-shadow: 0 10rpx 24rpx rgba(0, 113, 227, 0.18);
}

.modal-actions {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  gap: 16rpx;
}

.filter-actions {
  margin-top: 26rpx;
}

.caught-card {
  max-height: 86vh;
  overflow-y: auto;
}

.caught-author {
  display: flex;
  align-items: center;
  gap: 18rpx;
  margin-top: 0;
}

.author-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 76rpx;
  width: 76rpx;
  height: 76rpx;
  border-radius: 50%;
  color: #fff;
  background: linear-gradient(135deg, #5f9f8f, #0071e3);
  font-size: 30rpx;
  font-weight: 900;
}

.author-main {
  min-width: 0;
  flex: 1;
}

.follow-pill {
  display: flex;
  align-items: center;
  align-self: flex-start;
  gap: 8rpx;
  flex: 0 0 auto;
  min-height: 56rpx;
  border: 1px solid rgba(53, 139, 169, 0.14);
  border-radius: 999px;
  padding: 0 18rpx 0 8rpx;
  color: #276f83;
  background: rgba(226, 242, 246, 0.7);
  font-size: 23rpx;
  font-weight: 900;
}

.follow-dot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38rpx;
  height: 38rpx;
  border-radius: 50%;
  color: #fff;
  background: #358ba9;
  font-size: 18rpx;
}

.author-line,
.meta-tags {
  display: flex;
  align-items: center;
  gap: 10rpx;
  flex-wrap: wrap;
}

.author-name {
  max-width: 330rpx;
  overflow: hidden;
  color: #1d1d1f;
  font-size: 34rpx;
  font-weight: 900;
  line-height: 1.25;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.meta-tags {
  margin-top: 10rpx;
}

.mini-tag {
  border-radius: 999px;
  padding: 6rpx 12rpx;
  color: #6e6e73;
  background: #f5f5f7;
  font-size: 21rpx;
  font-weight: 800;
}

.mini-tag.vip {
  color: #7a4b00;
  background: #fff0bd;
}

.mini-tag.verified {
  color: #0f6b5e;
  background: rgba(95, 159, 143, 0.14);
}

.caught-message {
  display: block;
  margin: 28rpx 0;
  color: #1d1d1f;
  font-size: 34rpx;
  font-weight: 800;
  line-height: 1.5;
}

.input {
  height: 78rpx;
  margin-bottom: 10rpx;
  border: 1px solid rgba(29, 29, 31, 0.08);
  border-radius: 18px;
  background: #f5f5f7;
  padding: 0 20rpx;
  color: #1d1d1f;
  font-size: 26rpx;
}

.reply-error {
  display: block;
  margin: 0 0 18rpx 4rpx;
  color: #d92d20;
  font-size: 24rpx;
  font-weight: 700;
}

.reply-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12rpx;
  align-items: stretch;
}

.reply-button {
  min-width: 0;
}

.report-link {
  margin-top: 20rpx;
  color: #8e8e93;
  text-align: center;
  font-size: 24rpx;
}

.report-desc {
  display: block;
  margin-top: 14rpx;
  color: #6e6e73;
  font-size: 25rpx;
  line-height: 1.45;
}

.report-reasons {
  margin-top: 24rpx;
}

.report-field {
  margin-top: 22rpx;
}

.report-textarea {
  box-sizing: border-box;
  width: 100%;
  min-height: 132rpx;
  margin-top: 12rpx;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 18px;
  padding: 18rpx;
  background: #fff;
  color: #1d1d1f;
  font-size: 25rpx;
  line-height: 1.45;
}

.report-preview {
  margin: 22rpx 0;
  border-radius: 18px;
  padding: 20rpx;
  color: #3a3a3c;
  background: #f5f5f7;
  font-size: 25rpx;
  line-height: 1.5;
}

.report-actions {
  grid-template-columns: 0.8fr 1fr 1fr;
}

.danger-ghost {
  color: #b42318;
  background: #fff1f0;
}

.filter-done {
  margin-top: 26rpx;
}

@keyframes bottle-drift {
  0%, 100% {
  transform: translateX(-50%) translateY(0) rotate(-12deg);
  }
  50% {
    transform: translateX(calc(-50% + 20rpx)) translateY(-24rpx) rotate(-6deg);
  }
}

@keyframes bottle-catch {
  0%, 100% {
    transform: translateX(-50%) translateY(0) rotate(-12deg) scale(1);
  }
  50% {
    transform: translateX(-50%) translateY(-96rpx) rotate(6deg) scale(1.1);
  }
}

@keyframes bottle-throw {
  0% {
    transform: translateX(-50%) translateY(120rpx) rotate(24deg) scale(1.18);
    opacity: 0.2;
  }
  100% {
    transform: translateX(-50%) translateY(0) rotate(-12deg) scale(1);
    opacity: 1;
  }
}

@keyframes wave-move {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(8%);
  }
}

@keyframes mist-drift {
  0%, 100% {
    transform: translateX(0) scaleY(1);
    opacity: 0.72;
  }
  50% {
    transform: translateX(22rpx) scaleY(1.08);
    opacity: 1;
  }
}

@keyframes current-flow {
  0%, 100% {
    transform: translateX(-2%) translateY(0);
  }
  50% {
    transform: translateX(5%) translateY(-18rpx);
  }
}

@keyframes catch-ring {
  0% {
    opacity: 0.96;
    transform: translateX(-50%) scale(0.56);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) scale(1.4);
  }
}

@keyframes beam-pulse {
  0%, 100% {
    opacity: 0.55;
  }
  50% {
    opacity: 1;
  }
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.35;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes sheet-up {
  from {
    opacity: 0;
    transform: translateY(42rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes dialog-pop {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
