<template>
  <view class="filters">
    <view v-if="mode === 'chips'" class="filter-groups">
      <view class="filter-group">
        <text class="group-label">{{ cityLabel }}</text>
        <view class="chip-row">
          <view
            v-for="city in cities"
            :key="city"
            class="select-chip"
            :class="{ active: modelValue.city === city }"
            @tap="update({ city })"
          >
            {{ city }}
          </view>
        </view>
      </view>
      <view class="filter-group gender-line">
        <text class="group-label">性别</text>
        <view class="chip-row">
          <view
            v-for="gender in genders"
            :key="gender"
            class="select-chip"
            :class="{ active: modelValue.gender === gender }"
            @tap="update({ gender })"
          >
            {{ gender }}
          </view>
        </view>
      </view>
      <view class="filter-group">
        <view v-if="ageMode === 'range'" class="age-range-line">
          <text class="group-label age-label">年龄</text>
          <view
            class="age-range-control"
            @click="setNearestAge"
          >
            <view class="age-range-meta">
              <text class="age-range-value">{{ ageRangeText }}</text>
            </view>
            <view
              class="age-range-track"
            >
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
        <template v-else>
          <text class="group-label">年龄</text>
          <view class="chip-row">
            <view
              v-for="ageRange in ageRanges"
              :key="ageRange"
              class="select-chip"
              :class="{ active: modelValue.ageRange === ageRange }"
              @tap="update({ ageRange })"
            >
              {{ ageRange }}
            </view>
          </view>
        </template>
      </view>
    </view>
    <scroll-view v-else scroll-x class="filter-scroll">
      <view class="filter-row">
        <picker :range="cities" :value="cityIndex" @change="onCityChange">
          <view class="filter-pill">
            <text class="filter-icon">{{ cityIcon }}</text>
            <text>{{ cityLabel }} {{ modelValue.city }}</text>
          </view>
        </picker>
        <picker :range="genders" :value="genderIndex" @change="onGenderChange">
          <view class="filter-pill">
            <text class="filter-icon rose">性</text>
            <text>性别 {{ modelValue.gender }}</text>
          </view>
        </picker>
        <picker :range="ageRanges" :value="ageIndex" @change="onAgeChange">
          <view class="filter-pill">
            <text class="filter-icon warm">龄</text>
            <text>年龄 {{ modelValue.ageRange }}</text>
          </view>
        </picker>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

export interface ExploreFilterValue {
  city: string
  gender: string
  ageRange: string
}

const props = defineProps<{
  modelValue: ExploreFilterValue
  mode?: 'picker' | 'chips'
  cityLabel?: string
  cityOptions?: string[]
  ageMode?: 'chips' | 'range'
}>()

const mode = computed(() => props.mode || 'picker')
const cityLabel = computed(() => props.cityLabel || '范围')
const cityIcon = computed(() => (cityLabel.value === '城市' ? '城' : '范'))
const ageMode = computed(() => props.ageMode || 'chips')

const emit = defineEmits<{
  'update:modelValue': [value: ExploreFilterValue]
}>()

const cities = computed(() => props.cityOptions || ['全国', '同城', '附近'])
const genders = ['全部', '女', '男']
const ageRanges = ['全部', '18-24', '25-30', '31-36', '37+']
const AGE_MIN = 18
const AGE_MAX = 80

const cityIndex = computed(() => Math.max(0, cities.value.indexOf(props.modelValue.city)))
const genderIndex = computed(() => Math.max(0, genders.indexOf(props.modelValue.gender)))
const ageIndex = computed(() => Math.max(0, ageRanges.indexOf(props.modelValue.ageRange)))
const activeAgeThumb = ref<'min' | 'max' | null>(null)
let ageTrackRect: DOMRect | undefined
const ageBounds = computed(() => parseAgeRange(props.modelValue.ageRange))
const ageMin = computed(() => ageBounds.value.min)
const ageMax = computed(() => ageBounds.value.max)
const ageMinPercent = computed(() => ((ageMin.value - AGE_MIN) / (AGE_MAX - AGE_MIN)) * 100)
const ageMaxPercent = computed(() => ((ageMax.value - AGE_MIN) / (AGE_MAX - AGE_MIN)) * 100)
const ageRangeText = computed(() => `${ageMin.value}-${ageMax.value}岁`)

function update(next: Partial<ExploreFilterValue>) {
  emit('update:modelValue', { ...props.modelValue, ...next })
}

function onCityChange(event: { detail: { value: number } }) {
  update({ city: cities.value[event.detail.value] || cities.value[0] })
}

function onGenderChange(event: { detail: { value: number } }) {
  update({ gender: genders[event.detail.value] || genders[0] })
}

function onAgeChange(event: { detail: { value: number } }) {
  update({ ageRange: ageRanges[event.detail.value] || ageRanges[0] })
}

function startAgeDrag(thumb: 'min' | 'max', event: any) {
  event.preventDefault?.()
  event.stopPropagation?.()
  ageTrackRect = getAgeTrackRect(event)
  activeAgeThumb.value = thumb
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
  const thumb = Math.abs(age - ageMin.value) <= Math.abs(age - ageMax.value) ? 'min' : 'max'
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
    updateAgeRange(Math.min(age, ageMax.value), ageMax.value)
    return
  }
  updateAgeRange(ageMin.value, Math.max(age, ageMin.value))
}

function updateAgeRange(min: number, max: number) {
  update({ ageRange: `${min}-${max}` })
}

function getAgeFromPointer(event: any) {
  const point = event.touches?.[0] || event.changedTouches?.[0] || event
  const rect = ageTrackRect || getAgeTrackRect(event)
  if (!rect || !rect.width) return ageMin.value
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

onBeforeUnmount(() => {
  endAgeDrag()
})

function parseAgeRange(value: string) {
  if (!value || value === '全部') return { min: AGE_MIN, max: AGE_MAX }
  const [minText, maxText] = value.replace('+', `-${AGE_MAX}`).split('-')
  const min = Number(minText)
  const max = Number(maxText)
  if (!Number.isFinite(min) || !Number.isFinite(max)) return { min: AGE_MIN, max: AGE_MAX }
  return {
    min: Math.max(AGE_MIN, Math.min(min, max)),
    max: Math.min(AGE_MAX, Math.max(min, max))
  }
}
</script>

<style scoped lang="scss">
.filters {
  margin-top: 18rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  padding: 12rpx;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 12rpx 28rpx rgba(31, 54, 58, 0.04);
}

.filter-scroll {
  width: 100%;
  white-space: nowrap;
}

.filter-groups {
  display: grid;
  gap: 22rpx;
}

.filter-group {
  display: grid;
  gap: 12rpx;
}

.gender-line {
  display: flex;
  align-items: center;
  gap: 28rpx;
}

.gender-line .group-label {
  flex-shrink: 0;
}

.gender-line .chip-row {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  min-width: 0;
}

.gender-line .select-chip {
  min-width: 0;
  padding-right: 10rpx;
  padding-left: 10rpx;
}

.age-range-line {
  display: flex;
  align-items: center;
  gap: 28rpx;
}

.age-label {
  flex-shrink: 0;
}

.age-range-control {
  display: grid;
  grid-template-columns: 118rpx minmax(0, 1fr);
  align-items: center;
  gap: 18rpx;
  flex: 1;
  min-width: 0;
  border: 1px solid rgba(35, 108, 114, 0.1);
  border-radius: 999px;
  padding: 8rpx 16rpx;
  background: rgba(247, 250, 249, 0.9);
}

.age-range-meta {
  min-width: 0;
}

.age-range-value {
  color: #236c72;
  font-size: 24rpx;
  font-weight: 900;
}

.age-range-track {
  position: relative;
  height: 44rpx;
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
  background: rgba(35, 108, 114, 0.14);
}

.age-range-fill {
  background: linear-gradient(90deg, #2f7f6d, #236c72);
}

.age-thumb {
  position: absolute;
  top: 50%;
  width: 28rpx;
  height: 28rpx;
  border: 4rpx solid #fff;
  border-radius: 50%;
  background: #236c72;
  box-shadow: 0 8rpx 18rpx rgba(35, 108, 114, 0.28);
  transform: translate(-50%, -50%);
}

.group-label {
  color: #6e6e73;
  font-size: 24rpx;
  font-weight: 800;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.select-chip {
  min-width: 92rpx;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 999px;
  padding: 13rpx 20rpx;
  color: #172126;
  background: rgba(255, 255, 255, 0.82);
  box-sizing: border-box;
  font-size: 24rpx;
  font-weight: 800;
  text-align: center;
}

.select-chip.active {
  border-color: rgba(35, 108, 114, 0.24);
  color: #fff;
  background: #236c72;
  box-shadow: 0 10rpx 24rpx rgba(35, 108, 114, 0.16);
}

.filter-row {
  display: inline-flex;
  gap: 12rpx;
  padding-bottom: 4rpx;
}

.filter-pill {
  display: inline-flex;
  align-items: center;
  gap: 10rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 999px;
  padding: 10rpx 18rpx 10rpx 10rpx;
  color: #172126;
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 10rpx 24rpx rgba(0, 0, 0, 0.05);
  font-size: 24rpx;
}

.filter-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38rpx;
  height: 38rpx;
  border-radius: 50%;
  color: #fff;
  background: #236c72;
  font-size: 20rpx;
  font-weight: 900;
  line-height: 1;
}

.filter-icon.rose {
  background: #bf5b73;
}

.filter-icon.warm {
  background: #c27a35;
}
</style>
