<template>
  <view class="page safe-bottom">
    <view class="panel vip-hero">
      <text class="title">VIP 会员</text>
      <text class="body intro">提升每日次数，显示身份标识，解锁专属瓶子皮肤、优先曝光和历史记录扩容。</text>
      <view class="tag vip-tag">{{ app.user?.isVip ? '会员生效中' : '未开通' }}</view>
    </view>

    <view class="section grid-2">
      <view v-for="benefit in benefits" :key="benefit.title" class="panel benefit">
        <text class="h2">{{ benefit.title }}</text>
        <text class="muted">{{ benefit.body }}</text>
      </view>
    </view>

    <view class="section panel">
      <text class="h2">会员套餐</text>
      <view v-for="product in products" :key="product.name" class="product-row">
        <view>
          <text class="body">{{ product.name }}</text>
          <text class="muted">{{ product.desc }}</text>
        </view>
        <view class="button secondary price-button">{{ product.price }}</view>
      </view>
      <text class="muted pay-note">iOS 走 Apple IAP，Android 走 Google Play Billing 或渠道支付，小程序按微信规则接入。</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
import { useAppStore } from '@/stores/app'

const app = useAppStore()

const benefits = [
  { title: '次数加成', body: '每日捞瓶、扔瓶、真心话、大冒险、树洞次数增加。' },
  { title: '身份标识', body: '昵称旁显示会员标识，互动记录中持续露出。' },
  { title: '专属装扮', body: '瓶子皮肤、头像框、树洞背景后续开放。' },
  { title: '优先曝光', body: '优质内容更容易被捞到或回应。' }
]

const products = [
  { name: '月卡会员', desc: '适合轻度体验', price: '¥18' },
  { name: '季卡会员', desc: '含额外漂流币', price: '¥45' },
  { name: '年卡会员', desc: '最高权益和身份展示', price: '¥128' }
]

onLoad(() => app.hydrate())
</script>

<style scoped lang="scss">
.vip-hero {
  background: #f6dfb6;
}

.intro {
  display: block;
  margin: 18rpx 0;
}

.benefit {
  min-height: 190rpx;
}

.benefit .muted {
  display: block;
  margin-top: 12rpx;
}

.product-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
  padding: 22rpx 0;
  border-bottom: 1px solid #eadfce;
}

.product-row .body,
.product-row .muted {
  display: block;
}

.price-button {
  width: 120rpx;
  min-height: 62rpx;
}

.pay-note {
  display: block;
  margin-top: 20rpx;
}
</style>
