<template>
  <view class="app-icon" :class="tone">{{ text }}</view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { appIconText, type AppIconName } from '@/constants/icons'

const props = withDefaults(defineProps<{
  name: AppIconName
  tone?: 'brand' | 'warm' | 'rose' | 'mint' | 'plain'
}>(), {
  tone: 'brand'
})

const text = computed(() => appIconText[props.name])
</script>

<style scoped lang="scss">
.app-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52rpx;
  height: 52rpx;
  border-radius: 8px;
  color: #fff;
  font-size: 24rpx;
  font-weight: 900;
  flex-shrink: 0;
}

.brand {
  background: #2d6c73;
}

.warm {
  background: #d9895b;
}

.rose {
  background: #d8758b;
}

.mint {
  background: #7eb7a6;
}

.plain {
  color: #25323c;
  background: #f1eadf;
}
</style>
