<template>
  <view class="page safe-bottom">
    <view class="page-hero">
      <view>
        <text class="title">用户设置</text>
        <text class="muted">更换头像和昵称</text>
      </view>
    </view>

    <view class="section panel">
      <text class="h2">选择头像</text>
      <view class="avatar-grid">
        <view
          v-for="item in avatarOptions"
          :key="item"
          class="avatar-choice"
          :class="{ active: avatarText === item }"
          @tap="avatarText = item"
        >
          {{ item }}
        </view>
      </view>
    </view>

    <view class="section panel">
      <text class="h2">昵称</text>
      <input v-model="nickname" class="nickname-input" maxlength="12" placeholder="输入新的昵称" />
    </view>

    <view class="section button" :class="{ disabled: !nickname.trim() }" @tap="saveProfile">保存资料</view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'

const app = useAppStore()
const avatarOptions = ['海', '月', '星', '风', '岛', '鲸']
const avatarText = ref('海')
const nickname = ref('')

onLoad(async () => {
  await app.hydrate()
  avatarText.value = app.user?.avatarText || '海'
  nickname.value = app.user?.nickname || ''
})

function saveProfile() {
  const nextName = nickname.value.trim()
  if (!nextName) {
    showToast('先填写昵称')
    return
  }
  app.updateUserProfile({
    avatarText: avatarText.value,
    nickname: nextName
  })
  showToast('资料已保存')
}
</script>

<style scoped lang="scss">
.avatar-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16rpx;
  margin-top: 22rpx;
}

.avatar-choice {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 116rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  color: #236c72;
  background: rgba(35, 108, 114, 0.08);
  font-size: 38rpx;
  font-weight: 900;
}

.avatar-choice.active {
  color: #fff;
  background: #236c72;
  box-shadow: 0 16rpx 32rpx rgba(35, 108, 114, 0.18);
}

.nickname-input {
  width: 100%;
  min-height: 86rpx;
  margin-top: 20rpx;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 8px;
  padding: 0 20rpx;
  color: #172126;
  background: #fbfdf9;
  box-sizing: border-box;
  font-size: 29rpx;
}
</style>
