<template>
  <view class="page membership-page safe-bottom">
    <view class="vip-card">
      <view class="vip-card-top">
        <VipBadge variant="ribbon" glow />
        <text class="vip-state">{{ app.user?.isVip ? '会员身份生效中' : '等待开通' }}</text>
      </view>
      <text class="vip-title">VIP 会员</text>
      <text class="vip-copy">更高的曝光、更醒目的身份标识，以及更多每日互动次数。</text>
      <view class="vip-card-bottom">
        <view>
          <text class="vip-level-label">当前等级</text>
          <text class="vip-level">{{ levelText }}</text>
          <text v-if="app.user?.isVip" class="vip-expire">{{ vipExpireText }}</text>
        </view>
        <button class="vip-action" hover-class="none" :class="{ disabled: Boolean(openingProductId) }" :disabled="Boolean(openingProductId)" @tap="openFeaturedProduct">
          {{ app.user?.isVip ? '续费会员' : '立即开通' }}
        </button>
      </view>
    </view>

    <view class="benefit-grid">
      <view v-for="benefit in benefits" :key="benefit.title" class="benefit-card">
        <text class="benefit-mark">{{ benefit.mark }}</text>
        <text class="benefit-title">{{ benefit.title }}</text>
        <text class="benefit-copy">{{ benefit.body }}</text>
      </view>
    </view>

    <view class="plan-panel">
      <view class="panel-head">
        <text class="panel-title">会员套餐</text>
        <text class="panel-subtitle">价格与权益由后台配置</text>
      </view>
      <view v-for="product in products" :key="product.id" class="product-row" :class="{ featured: product.featured, disabled: Boolean(openingProductId) }" @tap="openMembership(product)">
        <view class="product-main">
          <view class="product-name-row">
            <text class="product-name">{{ product.name }}</text>
            <text v-if="product.featured" class="recommend-pill">推荐</text>
          </view>
          <text class="product-desc">{{ product.desc }}</text>
        </view>
        <view class="price-button" :class="{ loading: openingProductId === product.id }">{{ openingProductId === product.id ? '处理中' : product.priceLabel }}</view>
      </view>
      <text class="pay-note">iOS 走 Apple IAP，Android 走 Google Play Billing 或渠道支付，小程序按微信规则接入。</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import VipBadge from '@/components/VipBadge.vue'
import { businessApi, type MembershipPaymentPlatform } from '@/services/businessApi'
import { showToast } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import type { MembershipProduct } from '@/types/domain'

const app = useAppStore()
const membershipProducts = ref<MembershipProduct[]>([])
const openingProductId = ref('')

const benefits = computed(() => {
  const rows = membershipProducts.value[0]?.benefits || []
  return rows.map((body, index) => ({
    mark: String(index + 1).padStart(2, '0'),
    title: body.split('，')[0] || body,
    body
  }))
})

const products = computed(() => membershipProducts.value.map((item) => ({
  ...item,
  desc: item.benefits[0] || '会员权益',
  featured: item.id.includes('season')
})))

const levelText = computed(() => {
  if (!app.user?.isVip) return '未开通'
  if (app.user.vipLevel === 'yearly') return '年度会员'
  if (app.user.vipLevel === 'season') return '季度会员'
  return '月度会员'
})

const vipExpireText = computed(() => {
  if (!app.user?.vipExpiresAt) return '有效期未同步'
  return `有效期至 ${formatDate(app.user.vipExpiresAt)}`
})

function formatDate(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value.slice(0, 10)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${date.getFullYear()}.${month}.${day}`
}

function createTransactionId(productId: string) {
  const randomPart = Math.floor(Math.random() * 1_000_000).toString().padStart(6, '0')
  return `member_${productId}_${Date.now()}_${randomPart}`
}

function resolvePaymentPlatform(product: MembershipProduct): MembershipPaymentPlatform {
  if (product.platform !== 'all') return product.platform
  const userPlatform = app.user?.platform
  return userPlatform === 'ios' || userPlatform === 'android' || userPlatform === 'wechat' ? userPlatform : 'wechat'
}

function openFeaturedProduct() {
  const product = products.value.find((item) => item.featured) || products.value[0]
  if (!product) {
    showToast('会员套餐加载中，请稍后再试')
    return
  }
  void openMembership(product)
}

async function openMembership(product: MembershipProduct) {
  if (openingProductId.value) return
  openingProductId.value = product.id
  try {
    const result = await businessApi.verifyMembershipOrder({
      platform: resolvePaymentPlatform(product),
      productId: product.id,
      transactionId: createTransactionId(product.id)
    })
    app.applyUserProfile(result.user)
    try {
      await app.refreshStatus()
    } catch {
      // The order already verified; keep the returned user state if status refresh is slow.
    }
    showToast(result.order.status === 'duplicate_verified' ? '会员权益已同步' : '会员已开通，权益已生效')
  } catch {
    showToast('会员开通失败，请稍后再试')
  } finally {
    openingProductId.value = ''
  }
}

onLoad(async () => {
  await app.hydrate()
  membershipProducts.value = await businessApi.listMembershipProducts()
})
</script>

<style scoped lang="scss">
.membership-page {
  min-height: 100vh;
  padding-top: 24rpx;
  overflow-x: hidden;
  background:
    linear-gradient(180deg, #f8faf7 0%, #eef3f1 100%);
}

.vip-card,
.benefit-card,
.plan-panel {
  width: 100%;
  max-width: calc(100vw - 48rpx);
  border: 1px solid rgba(23, 33, 38, 0.08);
  border-radius: 8px;
  box-sizing: border-box;
}

.vip-card {
  position: relative;
  overflow: hidden;
  padding: 28rpx;
  color: #2b1b05;
  background:
    linear-gradient(135deg, #fffef6 0%, #f5dc91 52%, #d9a84a 100%),
    linear-gradient(120deg, rgba(255, 255, 255, 0.7), transparent 52%);
  box-shadow: 0 24rpx 58rpx rgba(139, 92, 18, 0.16);
}

.vip-card::after {
  position: absolute;
  right: -80rpx;
  top: -88rpx;
  width: 260rpx;
  height: 260rpx;
  border: 1px solid rgba(151, 99, 18, 0.16);
  border-radius: 50%;
  content: '';
}

.vip-card-top,
.vip-card-bottom {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 18rpx;
}

.vip-state {
  min-width: 0;
  color: #5b3a08;
  font-size: 22rpx;
  font-weight: 900;
  line-height: 1.3;
  text-align: left;
}

.vip-title,
.vip-copy,
.vip-level-label,
.vip-level {
  position: relative;
  z-index: 1;
  display: block;
}

.vip-title {
  margin-top: 42rpx;
  color: #2b1b05;
  font-size: 50rpx;
  font-weight: 900;
  line-height: 1.1;
}

.vip-copy {
  max-width: 520rpx;
  margin-top: 14rpx;
  color: #5f4a22;
  font-size: 25rpx;
  line-height: 1.48;
}

.vip-card-bottom {
  margin-top: 34rpx;
  border-top: 1px solid rgba(151, 99, 18, 0.16);
  padding-top: 22rpx;
}

.vip-level-label {
  color: #70511a;
  font-size: 21rpx;
  font-weight: 800;
}

.vip-level {
  margin-top: 7rpx;
  color: #7b4c0d;
  font-size: 32rpx;
  font-weight: 900;
}

.vip-expire {
  display: block;
  margin-top: 6rpx;
  color: #70511a;
  font-size: 21rpx;
  font-weight: 800;
}

.vip-action {
  flex: 0 0 auto;
  margin: 0;
  border: 0;
  border-radius: 8px;
  width: 162rpx;
  max-width: 162rpx;
  height: 66rpx;
  padding: 0 12rpx;
  color: #1f160a;
  background: #fffaf0;
  box-sizing: border-box;
  font-size: 24rpx;
  font-weight: 900;
  line-height: 66rpx;
  overflow: hidden;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vip-action::after {
  display: none;
}

.vip-action.disabled,
.product-row.disabled {
  opacity: 0.62;
}

.benefit-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14rpx;
  width: 100%;
  max-width: calc(100vw - 48rpx);
  margin-top: 18rpx;
}

.benefit-card {
  min-height: 164rpx;
  padding: 20rpx;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 12rpx 28rpx rgba(31, 54, 58, 0.045);
}

.benefit-mark,
.benefit-title,
.benefit-copy {
  display: block;
}

.benefit-mark {
  color: #9f6a24;
  font-size: 20rpx;
  font-weight: 900;
}

.benefit-title {
  margin-top: 9rpx;
  color: #172126;
  font-size: 27rpx;
  font-weight: 900;
}

.benefit-copy {
  margin-top: 8rpx;
  color: #65757b;
  font-size: 21rpx;
  line-height: 1.38;
}

.plan-panel {
  margin-top: 18rpx;
  padding: 24rpx;
  background: rgba(255, 255, 255, 0.96);
}

.panel-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 18rpx;
  margin-bottom: 10rpx;
}

.panel-title,
.panel-subtitle {
  display: block;
}

.panel-title {
  color: #172126;
  font-size: 30rpx;
  font-weight: 900;
}

.panel-subtitle {
  color: #65757b;
  font-size: 21rpx;
  font-weight: 700;
}

.product-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 12rpx;
  border-bottom: 1px solid rgba(23, 33, 38, 0.08);
  padding: 22rpx 0;
}

.product-row:active {
  opacity: 0.86;
}

.product-row.featured {
  margin: 0 -8rpx;
  border: 1px solid rgba(159, 106, 36, 0.16);
  border-radius: 8px;
  padding: 20rpx 8rpx;
  background: rgba(255, 244, 216, 0.52);
}

.product-main {
  flex: 1 1 auto;
  min-width: 0;
}

.product-name-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
  min-width: 0;
}

.recommend-pill {
  flex: 0 0 auto;
  border: 1px solid rgba(174, 123, 34, 0.22);
  border-radius: 999px;
  padding: 5rpx 10rpx;
  color: #7b4c0d;
  background: rgba(255, 245, 216, 0.9);
  font-size: 19rpx;
  font-weight: 900;
  line-height: 1;
}

.product-name,
.product-desc {
  display: block;
}

.product-name {
  color: #172126;
  font-size: 27rpx;
  font-weight: 900;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-desc {
  margin-top: 7rpx;
  color: #65757b;
  font-size: 22rpx;
}

.price-button {
  flex: 0 0 auto;
  width: 110rpx;
  border-radius: 8px;
  padding: 14rpx 10rpx;
  color: #1f160a;
  background: linear-gradient(90deg, #fff1bc, #d8a84a);
  box-sizing: border-box;
  font-size: 24rpx;
  font-weight: 900;
  overflow: hidden;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price-button.loading {
  background: #e2e8f0;
}

.pay-note {
  display: block;
  margin-top: 20rpx;
  color: #8a969b;
  font-size: 21rpx;
  line-height: 1.45;
}

@media (max-width: 430px) {
  .vip-card-top,
  .vip-card-bottom,
  .product-row,
  .panel-head {
    align-items: flex-start;
    flex-direction: column;
  }

  .vip-state {
    max-width: 100%;
    text-align: left;
  }

  .vip-action,
  .price-button {
    width: auto;
    max-width: 100%;
  }

  .product-row {
    gap: 12rpx;
  }
}
</style>
