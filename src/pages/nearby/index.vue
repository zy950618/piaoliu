<template>
  <view class="page nearby-page safe-bottom">
    <view class="nearby-hero">
      <view>
        <text class="title">附近的人</text>
        <text class="muted subtitle">距离只做粗略展示，默认保护精确位置。</text>
      </view>
      <AppIcon name="nearby" tone="mint" />
    </view>

    <view class="section nearby-filters">
      <view class="filter-group">
        <text class="filter-label">性别</text>
        <view class="chip-row">
          <view v-for="gender in genders" :key="gender" class="select-chip" :class="{ active: filters.gender === gender }" @tap="filters.gender = gender">
            {{ gender }}
          </view>
        </view>
      </view>
      <view class="filter-group">
        <text class="filter-label">年龄</text>
        <view class="chip-row">
          <view v-for="age in ageRanges" :key="age" class="select-chip" :class="{ active: filters.ageRange === age }" @tap="filters.ageRange = age">
            {{ age }}
          </view>
        </view>
      </view>
      <view class="filter-group">
        <text class="filter-label">距离</text>
        <view class="chip-row">
          <view v-for="distance in distanceRanges" :key="distance.value" class="select-chip" :class="{ active: filters.distanceKm === distance.value }" @tap="filters.distanceKm = distance.value">
            {{ distance.label }}
          </view>
        </view>
      </view>
    </view>

    <view class="section">
      <view v-for="person in filteredUsers" :key="person.id" class="panel person-card">
        <view class="between">
          <view class="row person-main">
            <view class="person-icon">{{ person.iconText }}</view>
            <view>
              <view class="row name-row">
                <text class="h2">{{ person.nickname }}</text>
                <text v-if="person.verified" class="tag">真人认证</text>
                <VipBadge v-if="person.isVip" variant="mini" />
              </view>
              <text class="muted">{{ person.distanceText }} · {{ person.ageRange || '年龄未知' }} · {{ person.online ? '在线' : '刚刚来过' }}</text>
            </view>
          </view>
        </view>
        <text class="body signature">{{ person.signature }}</text>
        <view class="grid-2">
          <view class="button secondary" @tap="follow(person.id)">关注</view>
          <view class="button ghost" @tap="requestFriend(person.id)">申请好友</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import AppIcon from '@/components/AppIcon.vue'
import VipBadge from '@/components/VipBadge.vue'
import { showToast } from '@/services/feedback'
import { useContentStore } from '@/stores/content'

const content = useContentStore()
const filters = ref({ gender: '全部', ageRange: '全部', distanceKm: 10 })
const genders = ['全部', '女', '男']
const ageRanges = ['全部', '18-24', '25-30', '31-36', '37+']
const distanceRanges = [
  { label: '3km', value: 3 },
  { label: '10km', value: 10 },
  { label: '30km', value: 30 }
]

const filteredUsers = computed(() =>
  content.nearbyUsers.filter((person) => {
    if (filters.value.gender === '女' && person.gender !== 'female') return false
    if (filters.value.gender === '男' && person.gender !== 'male') return false
    if (filters.value.ageRange !== '全部' && person.ageRange !== filters.value.ageRange) return false
    if ((person.distanceKm || 999) > filters.value.distanceKm) return false
    return true
  })
)

onLoad(() => content.loadNearbyUsers())

async function follow(id: string) {
  await content.followUser(id)
  showToast('已关注，对方动态会优先推荐')
}

async function requestFriend(id: string) {
  await content.requestFriend(id)
  showToast('好友申请已发送，对方同意后才能聊天')
}
</script>

<style scoped lang="scss">
.nearby-page {
  background:
    radial-gradient(circle at 15% 0%, rgba(126, 183, 166, 0.2), transparent 34%),
    linear-gradient(180deg, #f7fbf6, #f4f2ea);
}

.nearby-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 8px;
  padding: 30rpx;
  background: linear-gradient(135deg, #dbeeed, #fffdf8);
}

.subtitle {
  display: block;
  margin-top: 10rpx;
}

.nearby-filters {
  display: grid;
  gap: 18rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  padding: 18rpx;
  background: rgba(255, 255, 255, 0.78);
  box-shadow: 0 12rpx 28rpx rgba(31, 54, 58, 0.05);
}

.filter-group {
  display: grid;
  gap: 10rpx;
}

.filter-label {
  color: #65757b;
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
  padding: 12rpx 18rpx;
  color: #172126;
  background: rgba(255, 255, 255, 0.82);
  box-sizing: border-box;
  font-size: 24rpx;
  font-weight: 800;
  text-align: center;
}

.select-chip.active {
  color: #fff;
  border-color: rgba(35, 108, 114, 0.22);
  background: #236c72;
}

.person-card {
  margin-bottom: 16rpx;
}

.person-main,
.name-row {
  gap: 12rpx;
}

.person-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70rpx;
  height: 70rpx;
  border-radius: 8px;
  color: #fff;
  background: #7eb7a6;
  font-weight: 900;
}

.signature {
  display: block;
  margin: 22rpx 0;
}
</style>
