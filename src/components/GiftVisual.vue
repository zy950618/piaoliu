<template>
  <view class="gift-visual-root" :class="[size, shapeClass, { active, premium }]">
    <view class="aura"></view>
    <view class="spark spark-a"></view>
    <view class="spark spark-b"></view>
    <view class="spark spark-c"></view>

    <view v-if="shape === 'plane'" class="shape plane-shape">
      <view class="plane-trail"></view>
      <view class="plane-body"></view>
      <view class="plane-wing top"></view>
      <view class="plane-wing bottom"></view>
      <view class="plane-window"></view>
    </view>

    <view v-else-if="shape === 'whale'" class="shape whale-shape">
      <view class="whale-body"></view>
      <view class="whale-tail"></view>
      <view class="whale-fin"></view>
      <view class="whale-eye"></view>
      <view class="whale-spray"></view>
    </view>

    <view v-else-if="shape === 'island'" class="shape island-shape">
      <view class="island-sand"></view>
      <view class="palm-trunk"></view>
      <view class="palm-leaf leaf-a"></view>
      <view class="palm-leaf leaf-b"></view>
      <view class="palm-leaf leaf-c"></view>
    </view>

    <view v-else-if="shape === 'crown'" class="shape crown-shape">
      <view class="crown-base"></view>
      <view class="crown-point point-a"></view>
      <view class="crown-point point-b"></view>
      <view class="crown-point point-c"></view>
      <view class="crown-gem"></view>
    </view>

    <view v-else-if="shape === 'moon'" class="shape moon-shape"></view>

    <view v-else-if="shape === 'bottle'" class="shape bottle-shape">
      <view class="bottle-neck"></view>
      <view class="bottle-body"></view>
      <view class="bottle-paper"></view>
    </view>

    <view v-else-if="shape === 'flower'" class="shape flower-shape">
      <view class="petal petal-a"></view>
      <view class="petal petal-b"></view>
      <view class="petal petal-c"></view>
      <view class="petal petal-d"></view>
      <view class="flower-core"></view>
    </view>

    <view v-else-if="shape === 'star'" class="shape star-shape"></view>

    <view v-else-if="shape === 'shell'" class="shape shell-shape">
      <view class="shell-line line-a"></view>
      <view class="shell-line line-b"></view>
      <view class="shell-line line-c"></view>
    </view>

    <view v-else class="shape gem-shape"></view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { GiftProduct } from '@/types/domain'

const props = withDefaults(defineProps<{
  gift: GiftProduct
  size?: 'bubble' | 'sheet' | 'card' | 'splash'
  active?: boolean
}>(), {
  size: 'card',
  active: false
})

const shape = computed(() => {
  const id = props.gift.id.toLowerCase()
  const name = props.gift.name
  if (/plane|flight/.test(id) || /飞机|飞行/.test(name)) return 'plane'
  if (id.includes('whale') || name.includes('鲸')) return 'whale'
  if (id.includes('island') || name.includes('岛')) return 'island'
  if (id.includes('crown') || name.includes('皇冠')) return 'crown'
  if (id.includes('moon') || name.includes('月')) return 'moon'
  if (id.includes('bottle') || name.includes('瓶')) return 'bottle'
  if (id.includes('flower') || name.includes('花')) return 'flower'
  if (id.includes('star') || name.includes('星')) return 'star'
  if (id.includes('shell') || name.includes('贝')) return 'shell'
  return 'gem'
})

const shapeClass = computed(() => `shape-${shape.value}`)
const premium = computed(() => props.gift.priceCoins >= 520 || /crown|island|plane|flight/i.test(props.gift.id))
</script>

<style scoped lang="scss">
.gift-visual-root {
  --visual-size: 96rpx;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--visual-size);
  height: var(--visual-size);
  margin: 0 auto;
  overflow: visible;
  border-radius: 28%;
  isolation: isolate;
}

.bubble {
  --visual-size: 48rpx;
}

.sheet {
  --visual-size: 78rpx;
}

.card {
  --visual-size: 96rpx;
}

.splash {
  --visual-size: 138rpx;
}

.aura {
  position: absolute;
  inset: 8%;
  border-radius: 50%;
  background:
    radial-gradient(circle at 36% 28%, rgba(255, 255, 255, 0.88), transparent 18%),
    radial-gradient(circle, rgba(96, 165, 250, 0.2), rgba(20, 184, 166, 0.08) 48%, transparent 70%);
  filter: blur(1rpx);
  animation: auraPulse 2.4s ease-in-out infinite;
}

.premium .aura {
  background:
    radial-gradient(circle at 34% 28%, rgba(255, 255, 255, 0.92), transparent 17%),
    radial-gradient(circle, rgba(250, 204, 21, 0.32), rgba(59, 130, 246, 0.16) 46%, transparent 72%);
}

.shape {
  position: relative;
  z-index: 2;
}

.active .shape {
  animation: giftLift 1.45s ease-in-out infinite;
}

.spark {
  position: absolute;
  z-index: 1;
  width: 7%;
  height: 7%;
  border-radius: 50%;
  background: #facc15;
  opacity: 0.84;
  animation: sparkBlink 1.8s ease-in-out infinite;
}

.spark-a {
  left: 12%;
  top: 20%;
}

.spark-b {
  right: 10%;
  top: 32%;
  animation-delay: -0.5s;
}

.spark-c {
  right: 24%;
  bottom: 10%;
  animation-delay: -1s;
}

.plane-shape {
  width: 92%;
  height: 52%;
  animation: planeCruise 1.9s ease-in-out infinite;
}

.plane-body {
  position: absolute;
  right: 7%;
  top: 34%;
  width: 67%;
  height: 29%;
  border-radius: 999px 26% 26% 999px;
  background: linear-gradient(90deg, #ffffff, #bfdbfe 45%, #2563eb);
  box-shadow: 0 0 18rpx rgba(37, 99, 235, 0.42);
}

.plane-wing {
  position: absolute;
  left: 41%;
  width: 32%;
  height: 24%;
  border-radius: 70% 70% 10% 10%;
  background: linear-gradient(135deg, #60a5fa, #1d4ed8);
}

.plane-wing.top {
  top: 12%;
  transform: rotate(-18deg);
}

.plane-wing.bottom {
  bottom: 10%;
  transform: rotate(18deg);
}

.plane-window {
  position: absolute;
  right: 16%;
  top: 41%;
  width: 9%;
  height: 12%;
  border-radius: 50%;
  background: #eff6ff;
}

.plane-trail {
  position: absolute;
  left: 0;
  top: 45%;
  width: 45%;
  height: 9%;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.88), rgba(250, 204, 21, 0.86));
  box-shadow: 0 -13rpx 0 -5rpx rgba(96, 165, 250, 0.24), 0 13rpx 0 -5rpx rgba(245, 158, 11, 0.24);
}

.whale-shape {
  width: 88%;
  height: 58%;
}

.whale-body {
  position: absolute;
  left: 9%;
  top: 18%;
  width: 68%;
  height: 62%;
  border-radius: 55% 45% 44% 56%;
  background: linear-gradient(145deg, #38bdf8, #2563eb 70%, #1e3a8a);
  box-shadow: inset -10rpx -8rpx 0 rgba(15, 23, 42, 0.12), 0 12rpx 22rpx rgba(37, 99, 235, 0.2);
}

.whale-tail {
  position: absolute;
  right: 0;
  top: 28%;
  width: 30%;
  height: 34%;
  background: #2563eb;
  clip-path: polygon(0 50%, 46% 0, 62% 38%, 100% 8%, 76% 52%, 100% 94%, 61% 66%, 44% 100%);
}

.whale-fin {
  position: absolute;
  left: 34%;
  bottom: 6%;
  width: 22%;
  height: 24%;
  border-radius: 0 0 90% 90%;
  background: #1d4ed8;
  transform: rotate(-14deg);
}

.whale-eye {
  position: absolute;
  left: 25%;
  top: 36%;
  width: 7%;
  height: 9%;
  border-radius: 50%;
  background: #fff;
}

.whale-spray {
  position: absolute;
  left: 32%;
  top: 0;
  width: 30%;
  height: 22%;
  border-top: 4rpx solid #7dd3fc;
  border-left: 4rpx solid transparent;
  border-right: 4rpx solid transparent;
  border-radius: 50%;
}

.island-shape {
  width: 88%;
  height: 72%;
}

.island-sand {
  position: absolute;
  left: 8%;
  right: 8%;
  bottom: 7%;
  height: 24%;
  border-radius: 50%;
  background: linear-gradient(180deg, #fde68a, #f59e0b);
  box-shadow: 0 8rpx 16rpx rgba(245, 158, 11, 0.22);
}

.palm-trunk {
  position: absolute;
  left: 48%;
  bottom: 21%;
  width: 11%;
  height: 49%;
  border-radius: 999px;
  background: linear-gradient(90deg, #92400e, #d97706);
  transform: rotate(9deg);
}

.palm-leaf {
  position: absolute;
  top: 9%;
  left: 44%;
  width: 38%;
  height: 20%;
  border-radius: 100% 0 100% 0;
  background: linear-gradient(135deg, #22c55e, #047857);
  transform-origin: left bottom;
}

.leaf-a {
  transform: rotate(-34deg);
}

.leaf-b {
  transform: rotate(6deg);
}

.leaf-c {
  transform: rotate(44deg);
}

.crown-shape {
  width: 82%;
  height: 62%;
}

.crown-base {
  position: absolute;
  left: 8%;
  right: 8%;
  bottom: 8%;
  height: 28%;
  border-radius: 8rpx 8rpx 14rpx 14rpx;
  background: linear-gradient(180deg, #fde68a, #f59e0b);
  box-shadow: 0 10rpx 20rpx rgba(245, 158, 11, 0.24);
}

.crown-point {
  position: absolute;
  bottom: 30%;
  width: 28%;
  height: 50%;
  background: linear-gradient(180deg, #fff7ad, #f59e0b);
  clip-path: polygon(50% 0, 100% 100%, 0 100%);
}

.point-a {
  left: 5%;
  transform: rotate(-7deg);
}

.point-b {
  left: 36%;
  height: 62%;
}

.point-c {
  right: 5%;
  transform: rotate(7deg);
}

.crown-gem {
  position: absolute;
  left: 45%;
  bottom: 14%;
  width: 12%;
  height: 16%;
  border-radius: 50%;
  background: #ef4444;
}

.moon-shape {
  width: 62%;
  height: 62%;
  border-radius: 50%;
  background: #fde68a;
  box-shadow: inset -16rpx 0 0 #f8fafc, 0 0 22rpx rgba(250, 204, 21, 0.36);
}

.bottle-shape {
  width: 54%;
  height: 78%;
  transform: rotate(-12deg);
}

.bottle-neck {
  position: absolute;
  left: 36%;
  top: 2%;
  width: 26%;
  height: 28%;
  border-radius: 999px 999px 8rpx 8rpx;
  background: rgba(219, 234, 254, 0.88);
}

.bottle-body {
  position: absolute;
  left: 16%;
  right: 16%;
  bottom: 4%;
  height: 66%;
  border-radius: 38% 38% 44% 44%;
  background:
    radial-gradient(circle at 32% 24%, rgba(255, 255, 255, 0.9), transparent 17%),
    linear-gradient(145deg, rgba(125, 211, 252, 0.68), rgba(14, 165, 233, 0.8));
  box-shadow: inset 0 0 0 3rpx rgba(255, 255, 255, 0.54);
}

.bottle-paper {
  position: absolute;
  left: 30%;
  bottom: 26%;
  width: 40%;
  height: 22%;
  border-radius: 4rpx;
  background: #fff7ed;
  transform: rotate(7deg);
}

.flower-shape {
  width: 68%;
  height: 68%;
}

.petal {
  position: absolute;
  left: 30%;
  top: 6%;
  width: 38%;
  height: 45%;
  border-radius: 50% 50% 45% 45%;
  background: linear-gradient(180deg, #fb7185, #e11d48);
  transform-origin: 50% 90%;
}

.petal-b {
  transform: rotate(90deg);
}

.petal-c {
  transform: rotate(180deg);
}

.petal-d {
  transform: rotate(270deg);
}

.flower-core {
  position: absolute;
  left: 37%;
  top: 37%;
  width: 26%;
  height: 26%;
  border-radius: 50%;
  background: #fde68a;
  box-shadow: 0 0 10rpx rgba(250, 204, 21, 0.44);
}

.star-shape {
  width: 67%;
  height: 67%;
  background: linear-gradient(145deg, #fef3c7, #f59e0b 70%, #b45309);
  clip-path: polygon(50% 0, 61% 34%, 98% 35%, 68% 56%, 79% 92%, 50% 70%, 21% 92%, 32% 56%, 2% 35%, 39% 34%);
  filter: drop-shadow(0 10rpx 12rpx rgba(245, 158, 11, 0.26));
}

.shell-shape {
  width: 70%;
  height: 61%;
  border-radius: 70% 70% 42% 42%;
  background: linear-gradient(145deg, #fde2e4, #f59eac 58%, #f43f5e);
  overflow: hidden;
  box-shadow: inset 0 -6rpx 0 rgba(255, 255, 255, 0.24), 0 10rpx 18rpx rgba(244, 63, 94, 0.18);
}

.shell-line {
  position: absolute;
  bottom: -6%;
  left: 50%;
  width: 4rpx;
  height: 86%;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.55);
  transform-origin: bottom center;
}

.line-a {
  transform: rotate(-28deg);
}

.line-b {
  transform: rotate(0deg);
}

.line-c {
  transform: rotate(28deg);
}

.gem-shape {
  width: 62%;
  height: 62%;
  border-radius: 18%;
  background: linear-gradient(145deg, #bae6fd, #2563eb);
  transform: rotate(45deg);
  box-shadow: inset 0 0 0 3rpx rgba(255, 255, 255, 0.28), 0 12rpx 20rpx rgba(37, 99, 235, 0.2);
}

@keyframes auraPulse {
  0%,
  100% {
    transform: scale(0.92);
    opacity: 0.72;
  }

  50% {
    transform: scale(1.08);
    opacity: 1;
  }
}

@keyframes giftLift {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5rpx);
  }
}

@keyframes sparkBlink {
  0%,
  100% {
    transform: scale(0.6);
    opacity: 0.36;
  }

  50% {
    transform: scale(1);
    opacity: 0.92;
  }
}

@keyframes planeCruise {
  0%,
  100% {
    transform: translate(-4rpx, 4rpx) rotate(-8deg);
  }

  50% {
    transform: translate(8rpx, -7rpx) rotate(-8deg);
  }
}
</style>
