<template>
  <view class="page settings-page safe-bottom">
    <view class="avatar-section">
      <view class="avatar-preview" @tap="chooseAvatarFromAlbum">
        <image v-if="avatarUrl" class="avatar-image" :src="avatarUrl" mode="aspectFill" />
        <view v-else class="avatar-placeholder">
          <view class="avatar-head"></view>
          <view class="avatar-body"></view>
        </view>
      </view>
      <button class="avatar-action" hover-class="none" @tap="chooseAvatarFromAlbum">更换头像</button>
      <view class="identity-line">
        <text class="identity-name">{{ displayName }}</text>
        <VipBadge v-if="app.user?.isVip" variant="premium" glow />
      </view>
    </view>

    <view class="form-card">
      <view class="field-row">
        <text class="field-label">昵称</text>
        <view class="nickname-input-shell">
          <input
            v-model="nickname"
            class="field-input editable"
            maxlength="12"
            confirm-type="done"
            placeholder="输入新昵称"
            @confirm="saveProfile"
            @tap.stop
            @click.stop
          />
          <text class="input-count">{{ nickname.trim().length }}/12</text>
        </view>
      </view>
      <view class="divider"></view>
      <view class="field-row">
        <text class="field-label">性别</text>
        <text class="field-value">{{ genderText }}</text>
      </view>
      <view class="divider"></view>
      <view class="field-row">
        <text class="field-label">城市</text>
        <text class="field-value">{{ app.user?.city || '未设置' }}</text>
      </view>
    </view>

    <view class="form-card compact-card">
      <view class="field-row">
        <text class="field-label">用户 ID</text>
        <view class="copy-group" @tap="copyUserId">
          <text class="field-value mono">{{ displayUserId }}</text>
          <text class="copy-link">复制</text>
        </view>
      </view>
    </view>

    <view class="save-dock">
      <button class="save-button" hover-class="none" :class="{ disabled: !canSave || saving }" @tap="saveProfile">
        {{ saving ? '正在保存' : '保存修改' }}
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import VipBadge from '@/components/VipBadge.vue'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'

const app = useAppStore()
const content = useContentStore()
const avatarText = ref('海')
const avatarUrl = ref<string | undefined>()
const nickname = ref('')
const saving = ref(false)

const displayName = computed(() => nickname.value.trim() || app.user?.nickname || '未命名')
const canSave = computed(() => Boolean(nickname.value.trim()))
const displayUserId = computed(() => app.user?.id || '-')
const genderText = computed(() => {
  if (app.user?.gender === 'female') return '女'
  if (app.user?.gender === 'male') return '男'
  return '未设置'
})

onLoad(async () => {
  await app.refreshStatus()
  avatarText.value = app.user?.avatarText || '海'
  avatarUrl.value = app.user?.avatarUrl
  nickname.value = app.user?.nickname || ''
})

async function saveProfile() {
  if (saving.value) return
  const nextName = nickname.value.trim()
  if (!nextName) {
    showToast('先填写昵称')
    return
  }
  saving.value = true
  try {
    const profile = await app.saveUserProfile({
      avatarText: avatarUrl.value ? '图' : avatarText.value,
      avatarUrl: avatarUrl.value,
      nickname: nextName
    })
    content.syncCurrentUserProfile(profile)
    showToast('资料已保存')
  } finally {
    saving.value = false
  }
}

function chooseAvatarFromAlbum() {
  if (typeof uni !== 'undefined' && uni.chooseImage) {
    uni.chooseImage({
      count: 1,
      sourceType: ['album', 'camera'],
      success: (result) => {
        const filePath = result.tempFilePaths?.[0]
        if (!filePath) return
        avatarUrl.value = filePath
      },
      fail: () => showToast('需要相册或相机权限')
    })
  }
}

function copyUserId() {
  const id = app.user?.id
  if (!id || typeof uni === 'undefined' || !uni.setClipboardData) return
  uni.setClipboardData({
    data: id,
    success: () => showToast('用户 ID 已复制')
  })
}

</script>

<style scoped lang="scss">
.settings-page {
  min-height: 100vh;
  padding-top: 38rpx;
  padding-bottom: 144rpx;
  background:
    linear-gradient(180deg, #fbfcfb 0%, #f1f5f3 54%, #edf3f0 100%);
}

.avatar-action,
.save-button {
  margin: 0;
  border: 0;
  border-radius: 8px;
  box-sizing: border-box;
}

.avatar-action::after,
.save-button::after {
  display: none;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 34rpx 0 32rpx;
}

.avatar-preview {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 168rpx;
  height: 168rpx;
  border: 8rpx solid #fff;
  border-radius: 50%;
  background: #dfe6e4;
  box-shadow: 0 18rpx 44rpx rgba(31, 54, 58, 0.16);
}

.avatar-image,
.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.avatar-placeholder {
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(145deg, #d8e2df, #f6f8f7);
}

.avatar-head {
  position: absolute;
  top: 40rpx;
  left: 50%;
  width: 50rpx;
  height: 50rpx;
  transform: translateX(-50%);
  border-radius: 50%;
  background: #fff;
}

.avatar-body {
  position: absolute;
  right: 28rpx;
  bottom: 26rpx;
  left: 28rpx;
  height: 58rpx;
  border-radius: 60rpx 60rpx 22rpx 22rpx;
  background: #fff;
}

.avatar-action {
  height: 48rpx;
  margin-top: 22rpx;
  padding: 0 20rpx;
  color: #236c72;
  background: transparent;
  font-size: 24rpx;
  font-weight: 900;
  line-height: 48rpx;
}

.identity-line {
  display: flex;
  align-items: center;
  gap: 12rpx;
  max-width: 100%;
  margin-top: 18rpx;
}

.identity-name {
  overflow: hidden;
  max-width: 420rpx;
  color: #172126;
  font-size: 36rpx;
  font-weight: 900;
  line-height: 1.25;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.form-card {
  overflow: hidden;
  margin-top: 22rpx;
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 14rpx 34rpx rgba(31, 54, 58, 0.06);
}

.compact-card {
  margin-top: 18rpx;
}

.field-row {
  display: grid;
  grid-template-columns: 128rpx minmax(0, 1fr);
  align-items: center;
  min-height: 104rpx;
  padding: 0 26rpx;
  gap: 22rpx;
}

.field-label {
  color: #172126;
  font-size: 28rpx;
  font-weight: 800;
}

.field-input {
  min-width: 0;
  width: 100%;
  height: 68rpx;
  color: #172126;
  font-size: 28rpx;
  font-weight: 700;
  text-align: left;
  box-sizing: border-box;
}

.field-input.editable {
  border-radius: 8px;
  padding: 0 76rpx 0 18rpx;
  background: transparent;
}

.nickname-input-shell {
  position: relative;
  min-width: 0;
  width: 100%;
  border: 1px solid rgba(23, 33, 38, 0.1);
  border-radius: 8px;
  background: rgba(247, 250, 249, 0.92);
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.78);
}

.nickname-input-shell:focus-within {
  border-color: rgba(35, 108, 114, 0.36);
  box-shadow: 0 0 0 5rpx rgba(35, 108, 114, 0.08);
}

.input-count {
  position: absolute;
  right: 18rpx;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  font-size: 20rpx;
  font-weight: 800;
}

.field-value {
  min-width: 0;
  overflow: hidden;
  color: #65757b;
  font-size: 27rpx;
  line-height: 1.4;
  text-align: right;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 24rpx;
}

.copy-group {
  min-width: 0;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14rpx;
}

.copy-link {
  flex: 0 0 auto;
  color: #236c72;
  font-size: 24rpx;
  font-weight: 900;
}

.divider {
  height: 1px;
  margin-left: 154rpx;
  background: rgba(23, 33, 38, 0.08);
}

.save-dock {
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 20;
  padding: 18rpx 24rpx calc(18rpx + env(safe-area-inset-bottom));
  background: linear-gradient(180deg, rgba(238, 243, 241, 0), rgba(238, 243, 241, 0.98) 34%);
}

.save-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 520px;
  height: 88rpx;
  margin: 0 auto;
  color: #fff;
  background: #172126;
  box-shadow: 0 18rpx 36rpx rgba(23, 33, 38, 0.18);
  font-size: 29rpx;
  font-weight: 900;
  line-height: 88rpx;
}

.save-button.disabled {
  color: #8d989e;
  background: #dbe4e0;
  box-shadow: none;
}

@media (min-width: 720px) {
  .settings-page {
    max-width: 620px;
  }

  .save-button {
    max-width: 620px;
  }
}
</style>
