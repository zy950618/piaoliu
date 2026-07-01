<template>
  <view class="page nearby-page safe-bottom">
    <view class="nearby-topbar">
      <view class="icon-button filter-button" :class="{ active: showFilters }" @tap="showFilters = !showFilters">
        <text />
      </view>
      <text class="nearby-title">同城</text>
      <view class="window-pill">
        <text class="dot-menu">•••</text>
        <text class="mini-line" />
        <text class="circle-mark" />
      </view>
    </view>

    <view class="search-shell">
      <input v-model="searchKeyword" class="nearby-search" placeholder="搜索用户昵称、所在省、所在市" />
      <view class="search-button" @tap="applySearch">搜索</view>
    </view>

    <view v-if="showFilters" class="nearby-filters">
      <view class="filter-group">
        <text class="filter-label">城市</text>
        <view class="chip-row city-row">
          <view
            v-for="city in cityOptions"
            :key="city"
            class="select-chip city-chip"
            :class="{ active: filters.city === city || (city === '全部' && cityExpanded) }"
            @tap="selectCity(city)"
          >
            {{ city }}
          </view>
        </view>
      </view>
      <view class="filter-group">
        <text class="filter-label">性别</text>
        <view class="chip-row">
          <view v-for="gender in genders" :key="gender" class="select-chip" :class="{ active: filters.gender === gender }" @tap="filters.gender = gender">
            {{ gender }}
          </view>
        </view>
      </view>
      <view class="filter-group">
        <view class="age-filter-head">
          <text class="filter-label">年龄</text>
          <text class="age-value">{{ ageRangeText }}</text>
        </view>
        <view class="age-range-control" @tap="setNearestAge" @click="setNearestAge">
          <view class="age-range-track">
            <view class="age-range-rail" />
            <view class="age-range-fill" :style="{ left: `${ageMinPercent}%`, right: `${100 - ageMaxPercent}%` }" />
            <view
              class="age-thumb"
              :style="{ left: `${ageMinPercent}%` }"
              @touchstart.stop="startAgeDrag('min', $event)"
              @mousedown.stop="startAgeDrag('min', $event)"
              @click.stop
            />
            <view
              class="age-thumb"
              :style="{ left: `${ageMaxPercent}%` }"
              @touchstart.stop="startAgeDrag('max', $event)"
              @mousedown.stop="startAgeDrag('max', $event)"
              @click.stop
            />
          </view>
        </view>
      </view>
    </view>

    <view class="nearby-list">
      <view v-for="person in filteredUsers" :key="person.id" class="person-card">
        <image v-if="person.iconUrl" class="person-avatar" :class="{ vip: person.isVip }" :src="person.iconUrl" mode="aspectFill" />
        <view v-else class="person-avatar" :class="{ vip: person.isVip }" />
        <view class="person-main">
          <view class="name-row">
            <text class="person-name">{{ person.nickname }}</text>
            <VipBadge v-if="person.isVip" variant="mini" />
          </view>
          <view class="badge-row">
            <text class="meta-badge gender-badge">{{ genderLabel(person) }} {{ person.ageRange || '未知' }}</text>
            <text class="meta-badge city-badge">{{ cityLabel(person) }}</text>
            <text v-if="person.online" class="meta-badge online-badge">刚刚</text>
            <text v-else class="meta-badge away-badge">刚来过</text>
          </view>
          <view class="stats-row">
            <text>被关注人数 {{ attentionCount(person) }}</text>
            <text>注册天数 {{ registeredDays(person) }}</text>
          </view>
          <text class="person-signature">{{ person.signature }}</text>
          <text v-if="friendRequestStatus[person.id]" class="context-rule-status">{{ friendRequestStatus[person.id] }}</text>
          <text v-if="nearbyChatStatus[person.id]" class="context-rule-status">{{ nearbyChatStatus[person.id] }}</text>
        </view>
        <view class="person-actions">
          <text class="distance-text">{{ cityLabel(person) }}</text>
          <view class="chat-cta" :class="{ disabled: nearbyChatSubmitting[person.id] }" @tap="requestNearbyChat(person.id)">
            <text>开聊</text>
            <text class="heart-mark">💗</text>
          </view>
          <view class="mini-actions">
            <text @tap="follow(person.id)">关注</text>
            <text @tap="requestFriend(person.id)">好友</text>
          </view>
        </view>
      </view>

      <view v-if="filteredUsers.length === 0" class="empty-nearby">
        <text>没有匹配的同城用户</text>
        <text>调整筛选或搜索词后再试</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import VipBadge from '@/components/VipBadge.vue'
import { expandedCityOptions, primaryCityOptions } from '@/constants/product'
import { navigateTo, showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { NearbyUser } from '@/types/domain'

const content = useContentStore()
const app = useAppStore()
const AGE_MIN = 18
const AGE_MAX = 80
const filters = ref({ city: '全国', gender: '全部', ageMin: AGE_MIN, ageMax: AGE_MAX })
const friendRequestStatus = ref<Record<string, string>>({})
const nearbyChatStatus = ref<Record<string, string>>({})
const nearbyChatSubmitting = ref<Record<string, boolean>>({})
const showFilters = ref(false)
const searchKeyword = ref('')
const appliedKeyword = ref('')
const cityExpanded = ref(false)
const activeAgeThumb = ref<'min' | 'max' | null>(null)
let ageTrackRect: DOMRect | undefined
const genders = ['全部', '女', '男']
const cityOptions = computed(() => (
  cityExpanded.value
    ? [...primaryCityOptions, ...expandedCityOptions]
    : primaryCityOptions
))
const ageMinPercent = computed(() => ((filters.value.ageMin - AGE_MIN) / (AGE_MAX - AGE_MIN)) * 100)
const ageMaxPercent = computed(() => ((filters.value.ageMax - AGE_MIN) / (AGE_MAX - AGE_MIN)) * 100)
const ageRangeText = computed(() => `${filters.value.ageMin}-${filters.value.ageMax}岁`)

const filteredUsers = computed(() =>
  content.nearbyUsers.filter((person) => {
    if (filters.value.city !== '全国' && cityLabel(person) !== filters.value.city) return false
    if (filters.value.gender === '女' && person.gender !== 'female') return false
    if (filters.value.gender === '男' && person.gender !== 'male') return false
    if (!ageOverlaps(person.ageRange, filters.value.ageMin, filters.value.ageMax)) return false
    if (appliedKeyword.value) {
      const keyword = appliedKeyword.value.toLowerCase()
      const haystack = `${person.nickname} ${person.signature} ${cityLabel(person)} ${person.distanceText}`.toLowerCase()
      if (!haystack.includes(keyword)) return false
    }
    return true
  })
)

onLoad(() => {
  void Promise.all([app.hydrate(), content.loadNearbyUsers()])
})

onBeforeUnmount(() => {
  endAgeDrag()
})

function applySearch() {
  appliedKeyword.value = searchKeyword.value.trim()
}

function selectCity(city: string) {
  if (city === '全部') {
    cityExpanded.value = !cityExpanded.value
    return
  }
  filters.value = { ...filters.value, city }
}

function genderLabel(person: NearbyUser) {
  if (person.gender === 'female') return '♀'
  if (person.gender === 'male') return '♂'
  return '•'
}

function cityLabel(person: NearbyUser) {
  return person.city || '未知'
}

function attentionCount(person: NearbyUser) {
  return Math.abs(hashCode(`${person.id}:attention`)) % 58
}

function registeredDays(person: NearbyUser) {
  return Math.abs(hashCode(`${person.id}:days`)) % 980
}

function hashCode(value: string) {
  return value.split('').reduce((hash, char) => ((hash << 5) - hash + char.charCodeAt(0)) | 0, 0)
}

function ageOverlaps(value: string | undefined, min: number, max: number) {
  const parsed = parseAgeRange(value)
  if (!parsed) return true
  return parsed.max >= min && parsed.min <= max
}

function parseAgeRange(value: string | undefined) {
  if (!value) return undefined
  const [minText, maxText] = value.replace('+', `-${AGE_MAX}`).split('-')
  const min = Number(minText)
  const max = Number(maxText)
  if (!Number.isFinite(min) || !Number.isFinite(max)) return undefined
  return { min: Math.min(min, max), max: Math.max(min, max) }
}

function startAgeDrag(thumb: 'min' | 'max', event: any) {
  event.preventDefault?.()
  event.stopPropagation?.()
  activeAgeThumb.value = thumb
  ageTrackRect = getAgeTrackRect(event)
  updateAgeFromPointer(thumb, event)
  if (typeof window === 'undefined') return
  window.addEventListener('mousemove', moveAgeDrag)
  window.addEventListener('mouseup', endAgeDrag)
  window.addEventListener('touchmove', moveAgeDrag, { passive: false })
  window.addEventListener('touchend', endAgeDrag)
  window.addEventListener('touchcancel', endAgeDrag)
}

function setNearestAge(event: any) {
  if (activeAgeThumb.value) return
  ageTrackRect = getAgeTrackRect(event)
  const age = getAgeFromPointer(event)
  const thumb = Math.abs(age - filters.value.ageMin) <= Math.abs(age - filters.value.ageMax) ? 'min' : 'max'
  updateAgeFromPointer(thumb, event)
  ageTrackRect = undefined
}

function moveAgeDrag(event: any) {
  if (!activeAgeThumb.value) return
  event.preventDefault?.()
  updateAgeFromPointer(activeAgeThumb.value, event)
}

function endAgeDrag() {
  activeAgeThumb.value = null
  ageTrackRect = undefined
  if (typeof window === 'undefined') return
  window.removeEventListener('mousemove', moveAgeDrag)
  window.removeEventListener('mouseup', endAgeDrag)
  window.removeEventListener('touchmove', moveAgeDrag)
  window.removeEventListener('touchend', endAgeDrag)
  window.removeEventListener('touchcancel', endAgeDrag)
}

function updateAgeFromPointer(thumb: 'min' | 'max', event: any) {
  const age = getAgeFromPointer(event)
  if (thumb === 'min') {
    filters.value = { ...filters.value, ageMin: Math.min(age, filters.value.ageMax) }
    return
  }
  filters.value = { ...filters.value, ageMax: Math.max(age, filters.value.ageMin) }
}

function getAgeFromPointer(event: any) {
  const point = event.touches?.[0] || event.changedTouches?.[0] || event
  const rect = ageTrackRect || getAgeTrackRect(event)
  if (!rect || !rect.width) return filters.value.ageMin
  const clientX = point.clientX ?? point.pageX ?? event.detail?.clientX ?? event.detail?.x ?? rect.left
  const percent = Math.min(1, Math.max(0, (clientX - rect.left) / rect.width))
  return Math.round(AGE_MIN + percent * (AGE_MAX - AGE_MIN))
}

function getAgeTrackRect(event: any) {
  const track =
    event.target?.closest?.('.age-range-track') ||
    event.currentTarget?.querySelector?.('.age-range-track') ||
    event.currentTarget
  return track?.getBoundingClientRect?.()
}

async function follow(id: string) {
  await content.followUser(id)
  showToast('已关注，对方动态会优先推荐')
}

async function requestFriend(id: string) {
  await content.requestFriend(id)
  const message = '好友申请已发送；好友用于长期关系沉淀，明确互动上下文内仍可继续聊'
  friendRequestStatus.value = { ...friendRequestStatus.value, [id]: message }
  showToast(message)
}

async function requestNearbyChat(id: string) {
  if (nearbyChatSubmitting.value[id]) return
  nearbyChatSubmitting.value = { ...nearbyChatSubmitting.value, [id]: true }
  nearbyChatStatus.value = { ...nearbyChatStatus.value, [id]: '' }
  try {
    const result = await content.createMatchExpandContextRequest(id)
    const gateText = result.gate === 'vip'
      ? 'VIP免费'
      : result.costCoins > 0 ? `已消耗 ${result.costCoins} 积分` : '已复用聊天，不重复扣积分'
    const message = `${gateText}，已开聊`
    nearbyChatStatus.value = { ...nearbyChatStatus.value, [id]: message }
    showToast(message)
    if (result.threadId) {
      navigateTo(`/pages/messages/chat?threadId=${result.threadId}`)
    }
  } catch {
    const message = '需要 VIP 或至少 5 积分才能开聊'
    nearbyChatStatus.value = { ...nearbyChatStatus.value, [id]: message }
    showToast(message)
  } finally {
    nearbyChatSubmitting.value = { ...nearbyChatSubmitting.value, [id]: false }
  }
}
</script>

<style scoped lang="scss">
.nearby-page {
  min-height: 100vh;
  min-height: 100dvh;
  padding: 22rpx 22rpx 128rpx;
  background: #091228;
  color: #fff;
}

.nearby-topbar {
  position: sticky;
  top: 0;
  z-index: 8;
  display: grid;
  grid-template-columns: 76rpx 1fr 164rpx;
  align-items: center;
  gap: 12rpx;
  margin: -4rpx -4rpx 14rpx;
  padding: 10rpx 4rpx 8rpx;
  background: rgba(9, 18, 40, 0.94);
  backdrop-filter: blur(12px);
}

.nearby-title {
  font-size: 34rpx;
  font-weight: 900;
  text-align: center;
}

.icon-button,
.window-pill {
  min-height: 64rpx;
}

.icon-button {
  position: relative;
  width: 64rpx;
  border-radius: 8px;
}

.filter-button::before,
.filter-button::after,
.filter-button text::before,
.filter-button text::after {
  position: absolute;
  content: '';
  background: #f8fafc;
}

.filter-button::before,
.filter-button::after {
  left: 12rpx;
  width: 40rpx;
  height: 5rpx;
  border-radius: 999px;
}

.filter-button::before {
  top: 20rpx;
}

.filter-button::after {
  top: 40rpx;
}

.filter-button text::before,
.filter-button text::after {
  width: 12rpx;
  height: 12rpx;
  border: 4rpx solid #091228;
  border-radius: 50%;
}

.filter-button text::before {
  left: 16rpx;
  top: 14rpx;
}

.filter-button text::after {
  right: 15rpx;
  top: 34rpx;
}

.filter-button.active {
  background: rgba(45, 212, 191, 0.12);
}

.window-pill {
  display: grid;
  grid-template-columns: 1fr 1rpx 34rpx;
  align-items: center;
  gap: 18rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.28);
  border-radius: 999px;
  padding: 0 18rpx;
  color: #fff;
  background: rgba(17, 27, 56, 0.86);
  box-sizing: border-box;
}

.dot-menu {
  font-size: 30rpx;
  line-height: 1;
}

.mini-line {
  width: 1rpx;
  height: 32rpx;
  background: rgba(148, 163, 184, 0.4);
}

.circle-mark {
  width: 20rpx;
  height: 20rpx;
  border: 4rpx solid #fff;
  border-radius: 50%;
}

.search-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 94rpx;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 20rpx;
  border-radius: 22rpx;
  padding: 10rpx 12rpx 10rpx 22rpx;
  background: #121b3a;
}

.nearby-search {
  min-height: 56rpx;
  color: #e2e8f0;
  font-size: 25rpx;
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 58rpx;
  border-radius: 999px;
  color: #fff;
  background: linear-gradient(135deg, #22e5b8, #2489ff);
  font-size: 24rpx;
  font-weight: 900;
}

.nearby-filters {
  display: grid;
  gap: 16rpx;
  margin-bottom: 20rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.16);
  border-radius: 18rpx;
  padding: 18rpx;
  background: #121b3a;
}

.filter-group {
  display: grid;
  gap: 10rpx;
}

.filter-label {
  color: #9aa6c3;
  font-size: 22rpx;
  font-weight: 800;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.select-chip {
  min-width: 88rpx;
  border: 1rpx solid rgba(148, 163, 184, 0.22);
  border-radius: 999px;
  padding: 10rpx 18rpx;
  color: #cbd5e1;
  background: rgba(255, 255, 255, 0.04);
  box-sizing: border-box;
  font-size: 23rpx;
  font-weight: 900;
  text-align: center;
}

.select-chip.active {
  color: #071225;
  border-color: transparent;
  background: linear-gradient(135deg, #26e7bb, #32a3ff);
}

.city-row {
  max-height: 176rpx;
  overflow-y: auto;
}

.city-chip {
  min-width: 96rpx;
}

.age-filter-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20rpx;
}

.age-value {
  color: #2dd4bf;
  font-size: 23rpx;
  font-weight: 900;
}

.age-range-control {
  border: 1rpx solid rgba(148, 163, 184, 0.18);
  border-radius: 999px;
  padding: 14rpx 24rpx;
  background: rgba(255, 255, 255, 0.06);
}

.age-range-track {
  position: relative;
  height: 48rpx;
}

.age-range-rail,
.age-range-fill {
  position: absolute;
  top: 50%;
  right: 0;
  left: 0;
  height: 8rpx;
  border-radius: 999px;
  transform: translateY(-50%);
}

.age-range-rail {
  background: rgba(148, 163, 184, 0.2);
}

.age-range-fill {
  background: linear-gradient(90deg, #2af0b6, #22a7ff);
}

.age-thumb {
  position: absolute;
  top: 50%;
  width: 32rpx;
  height: 32rpx;
  border: 5rpx solid #fff;
  border-radius: 50%;
  background: #20d7c8;
  box-shadow: 0 8rpx 20rpx rgba(34, 167, 255, 0.28);
  transform: translate(-50%, -50%);
}

.nearby-list {
  display: grid;
  gap: 20rpx;
}

.person-card {
  display: grid;
  grid-template-columns: 104rpx minmax(0, 1fr) 126rpx;
  gap: 16rpx;
  align-items: center;
  min-height: 142rpx;
  border-radius: 20rpx;
  padding: 20rpx 18rpx;
  background: #151e3e;
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.04);
}

.person-avatar {
  position: relative;
  display: block;
  overflow: hidden;
  width: 88rpx;
  height: 88rpx;
  border: 2rpx solid #fff;
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 34%, rgba(255, 255, 255, 0.88) 0 13rpx, transparent 14rpx),
    radial-gradient(circle at 50% 84%, rgba(255, 255, 255, 0.72) 0 28rpx, transparent 29rpx),
    linear-gradient(145deg, #243153, #111a36);
}

.person-avatar.vip {
  border-color: #ffe58a;
  background:
    radial-gradient(circle at 50% 34%, rgba(255, 255, 255, 0.9) 0 13rpx, transparent 14rpx),
    radial-gradient(circle at 50% 84%, rgba(255, 255, 255, 0.76) 0 28rpx, transparent 29rpx),
    linear-gradient(145deg, #f97316, #ec4899);
}

.person-main {
  min-width: 0;
}

.name-row,
.badge-row,
.stats-row {
  display: flex;
  align-items: center;
  min-width: 0;
}

.name-row {
  gap: 8rpx;
}

.person-name {
  overflow: hidden;
  color: #fff;
  font-size: 29rpx;
  font-weight: 900;
  line-height: 1.2;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge-row {
  gap: 8rpx;
  margin-top: 8rpx;
  flex-wrap: wrap;
}

.meta-badge {
  border-radius: 8rpx;
  padding: 4rpx 9rpx;
  font-size: 20rpx;
  font-weight: 900;
  line-height: 1;
}

.gender-badge {
  color: #f9a8d4;
  background: rgba(190, 24, 93, 0.34);
}

.city-badge {
  color: #bef264;
  background: rgba(77, 124, 15, 0.38);
}

.online-badge {
  color: #2dd4bf;
  background: rgba(13, 148, 136, 0.32);
}

.away-badge {
  color: #93c5fd;
  background: rgba(37, 99, 235, 0.28);
}

.stats-row {
  gap: 16rpx;
  margin-top: 9rpx;
  color: #a7b0ca;
  font-size: 21rpx;
  line-height: 1.1;
}

.person-signature {
  display: block;
  margin-top: 8rpx;
  overflow: hidden;
  color: #c5cee7;
  font-size: 21rpx;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.person-actions {
  display: grid;
  justify-items: end;
  gap: 8rpx;
}

.distance-text {
  color: #8792b1;
  font-size: 19rpx;
}

.chat-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4rpx;
  min-width: 92rpx;
  min-height: 46rpx;
  border-radius: 999px;
  color: #fff;
  background: linear-gradient(135deg, #2af0b6, #20b6ff);
  font-size: 24rpx;
  font-weight: 900;
  box-shadow: 0 10rpx 22rpx rgba(37, 99, 235, 0.26);
}

.chat-cta.disabled {
  opacity: 0.58;
}

.heart-mark {
  font-size: 28rpx;
}

.mini-actions {
  display: flex;
  gap: 10rpx;
  color: #8ca1d0;
  font-size: 20rpx;
  font-weight: 800;
}

.context-rule-status {
  display: block;
  margin-top: 10rpx;
  border-radius: 10rpx;
  padding: 9rpx 11rpx;
  color: #99f6e4;
  background: rgba(20, 184, 166, 0.14);
  font-size: 21rpx;
  font-weight: 800;
  line-height: 1.35;
}

.empty-nearby {
  display: grid;
  gap: 8rpx;
  justify-items: center;
  border-radius: 20rpx;
  padding: 54rpx 20rpx;
  color: #94a3b8;
  background: #151e3e;
  font-size: 24rpx;
  font-weight: 800;
}

@media (max-width: 390px) {
  .person-card {
    grid-template-columns: 92rpx minmax(0, 1fr) 116rpx;
    gap: 12rpx;
    padding: 18rpx 14rpx;
  }

  .person-avatar {
    width: 78rpx;
    height: 78rpx;
  }

  .stats-row {
    gap: 10rpx;
    font-size: 20rpx;
  }
}
</style>
