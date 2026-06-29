<template>
  <view class="gift-mask" @tap="emit('close')">
    <view class="gift-sheet" @tap.stop>
      <view class="sheet-grip"></view>

      <view class="sheet-head">
        <view class="receiver-block">
          <text class="sheet-title">送给 {{ receiverName }}</text>
          <text class="sheet-subtitle">选择礼物后从金币余额扣除</text>
        </view>
        <view class="wallet-pill" @tap="emit('recharge')">
          <text class="coin-dot"></text>
          <text>{{ walletBalance }}</text>
          <text class="wallet-action">充值</text>
        </view>
      </view>

      <scroll-view class="gift-scroll" scroll-y>
        <view class="gift-grid">
          <view
            v-for="gift in gifts"
            :key="gift.id"
            class="gift-card"
            :class="{
              selected: selectedGiftId === gift.id,
              sending: sendingGiftId === gift.id,
              premium: isPremiumGift(gift),
              disabled: Boolean(sendingGiftId)
            }"
            @tap="selectGift(gift.id)"
          >
            <view class="gift-visual-wrap">
              <GiftVisual :gift="gift" size="sheet" :active="selectedGiftId === gift.id" />
            </view>
            <text class="gift-name">{{ gift.name }}</text>
            <view class="price-row">
              <text class="mini-coin"></text>
              <text>{{ gift.priceCoins }}</text>
            </view>
          </view>
        </view>
      </scroll-view>

      <view class="send-bar">
        <view class="selected-info">
          <text class="selected-title">{{ selectedGift ? selectedGift.name : '选择一个礼物' }}</text>
          <text class="selected-price">
            {{ selectedGift ? `${selectedGift.priceCoins} 金币` : '余额不足时请先充值' }}
          </text>
        </view>
        <view
          class="send-gift-button"
          :class="{ disabled: !selectedGift || Boolean(sendingGiftId) }"
          @tap="sendSelectedGift"
        >
          {{ sendingGiftId ? '发送中' : '发送' }}
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import GiftVisual from '@/components/GiftVisual.vue'
import type { GiftProduct } from '@/types/domain'

const props = defineProps<{
  receiverName: string
  walletBalance: number
  gifts: GiftProduct[]
  sendingGiftId?: string
}>()

const emit = defineEmits<{
  close: []
  recharge: []
  select: [giftId: string]
}>()

const selectedGiftId = ref('')
const selectedGift = computed(() => props.gifts.find((gift) => gift.id === selectedGiftId.value))

watch(
  () => props.gifts,
  (gifts) => {
    const firstGift = gifts[0]
    if (!selectedGiftId.value && firstGift) selectedGiftId.value = firstGift.id
  },
  { immediate: true }
)

function selectGift(giftId: string) {
  if (props.sendingGiftId) return
  selectedGiftId.value = giftId
}

function sendSelectedGift() {
  if (!selectedGift.value || props.sendingGiftId) return
  emit('select', selectedGift.value.id)
}

function isPremiumGift(gift: GiftProduct) {
  return gift.priceCoins >= 520 || /crown|island|whale|plane|flight/i.test(gift.id)
}
</script>

<style scoped lang="scss">
.gift-mask {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: flex;
  align-items: flex-end;
  background: rgba(8, 10, 14, 0.56);
  backdrop-filter: blur(10px);
}

.gift-sheet {
  width: 100%;
  max-height: 76vh;
  border-radius: 24rpx 24rpx 0 0;
  padding: 16rpx 18rpx calc(18rpx + env(safe-area-inset-bottom));
  background:
    linear-gradient(180deg, rgba(31, 34, 43, 0.98), rgba(17, 19, 25, 0.99)),
    linear-gradient(120deg, rgba(255, 64, 92, 0.18), rgba(42, 207, 255, 0.1));
  box-sizing: border-box;
  box-shadow: 0 -18rpx 48rpx rgba(0, 0, 0, 0.32);
  animation: giftSheetIn 180ms ease-out;
}

.sheet-grip {
  width: 68rpx;
  height: 7rpx;
  margin: 0 auto 18rpx;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.28);
}

.sheet-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14rpx;
  padding: 0 4rpx 16rpx;
}

.receiver-block {
  min-width: 0;
}

.sheet-title,
.sheet-subtitle,
.gift-name,
.selected-title,
.selected-price {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sheet-title {
  max-width: 440rpx;
  color: #fff;
  font-size: 31rpx;
  font-weight: 900;
}

.sheet-subtitle {
  margin-top: 6rpx;
  color: rgba(255, 255, 255, 0.58);
  font-size: 21rpx;
}

.wallet-pill {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  min-height: 52rpx;
  border: 1px solid rgba(255, 218, 99, 0.25);
  border-radius: 999px;
  padding: 0 14rpx;
  color: #ffe07a;
  background: rgba(255, 255, 255, 0.08);
  font-size: 22rpx;
  font-weight: 900;
}

.coin-dot,
.mini-coin {
  display: inline-block;
  border-radius: 50%;
  background:
    radial-gradient(circle at 34% 28%, #fff7b0, transparent 28%),
    linear-gradient(145deg, #ffd65a, #ff9f1c);
  box-shadow: 0 0 12rpx rgba(255, 207, 92, 0.42);
}

.coin-dot {
  width: 22rpx;
  height: 22rpx;
}

.mini-coin {
  width: 16rpx;
  height: 16rpx;
}

.wallet-action {
  color: #fff;
  opacity: 0.86;
}

.gift-scroll {
  max-height: 500rpx;
}

.gift-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10rpx;
  padding-bottom: 14rpx;
}

.gift-card {
  position: relative;
  min-width: 0;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 18rpx;
  padding: 14rpx 6rpx 12rpx;
  background: rgba(255, 255, 255, 0.055);
  text-align: center;
  transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}

.gift-card:active {
  transform: scale(0.97);
}

.gift-card.selected {
  border-color: rgba(255, 221, 110, 0.88);
  background:
    linear-gradient(180deg, rgba(255, 213, 106, 0.18), rgba(255, 255, 255, 0.07)),
    rgba(255, 255, 255, 0.08);
}

.gift-card.premium {
  border-color: rgba(94, 234, 212, 0.22);
  background:
    radial-gradient(circle at 50% 0%, rgba(96, 165, 250, 0.18), transparent 54%),
    rgba(255, 255, 255, 0.075);
}

.gift-card.selected::after {
  position: absolute;
  right: 8rpx;
  top: 8rpx;
  width: 14rpx;
  height: 14rpx;
  border-radius: 50%;
  background: #ffdc5e;
  box-shadow: 0 0 16rpx rgba(255, 220, 94, 0.74);
  content: '';
}

.gift-card.disabled {
  opacity: 0.62;
}

.gift-visual-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 78rpx;
  height: 78rpx;
  margin: 0 auto 9rpx;
}

.gift-name {
  color: rgba(255, 255, 255, 0.94);
  font-size: 22rpx;
  font-weight: 900;
}

.price-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5rpx;
  margin-top: 5rpx;
  color: rgba(255, 255, 255, 0.58);
  font-size: 19rpx;
  font-weight: 800;
}

.send-bar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 154rpx;
  gap: 14rpx;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 14rpx;
}

.selected-info {
  min-width: 0;
}

.selected-title {
  color: #fff;
  font-size: 25rpx;
  font-weight: 900;
}

.selected-price {
  margin-top: 5rpx;
  color: rgba(255, 255, 255, 0.58);
  font-size: 20rpx;
}

.send-gift-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 66rpx;
  border-radius: 999px;
  color: #111319;
  background: linear-gradient(90deg, #ffdb5c, #ff8a35);
  font-size: 25rpx;
  font-weight: 900;
  box-shadow: 0 10rpx 24rpx rgba(255, 154, 50, 0.28);
}

.send-gift-button.disabled {
  color: rgba(255, 255, 255, 0.42);
  background: rgba(255, 255, 255, 0.12);
  box-shadow: none;
}

@keyframes giftSheetIn {
  from {
    transform: translateY(80rpx);
    opacity: 0.6;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

</style>
