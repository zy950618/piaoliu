<template>
  <view class="app-shell">
    <slot />
  </view>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

// #ifdef H5
onMounted(() => {
  const preloadTabPages = () => {
    void Promise.allSettled([
      import('./pages/bottle/index.vue'),
      import('./pages/plaza/index.vue'),
      import('./pages/game/index.vue'),
      import('./pages/messages/index.vue'),
      import('./pages/profile/index.vue')
    ])
  }

  if (window.requestIdleCallback) {
    window.requestIdleCallback(preloadTabPages, { timeout: 2500 })
    return
  }

  window.setTimeout(preloadTabPages, 1200)
})
// #endif
</script>

<style lang="scss">
page {
  min-height: 100%;
  background: #f8fafc;
  color: #172126;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  letter-spacing: 0;
}

.app-shell {
  min-height: 100%;
  background:
    radial-gradient(circle at 18% -8%, rgba(37, 99, 235, 0.06), transparent 28%),
    radial-gradient(circle at 92% 0%, rgba(15, 118, 110, 0.06), transparent 25%),
    linear-gradient(180deg, #ffffff 0%, #f8fafc 48%, #f1f5f9 100%);
}

/* H5 tabBar visual upgrade. Native MP tabBar keeps using pages.json. */
uni-app.uni-app--showtabbar uni-tabbar.uni-tabbar-bottom {
  right: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  width: 100vw !important;
  max-width: none !important;
  transform: none !important;
  border-radius: 22px 22px 0 0 !important;
  overflow: visible !important;
  z-index: 99 !important;
}

uni-app.uni-app--showtabbar uni-tabbar.uni-tabbar-bottom .uni-placeholder {
  height: 84px !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar {
  display: grid !important;
  grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  width: 100vw !important;
  max-width: none !important;
  height: 72px !important;
  border: 1px solid rgba(15, 23, 42, 0.08) !important;
  border-radius: 22px 22px 0 0 !important;
  background: rgba(255, 255, 255, 0.94) !important;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.12) !important;
  backdrop-filter: blur(16px) !important;
  box-sizing: border-box !important;
  overflow: visible !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar-border {
  display: none !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item {
  position: relative !important;
  flex: 1 1 20% !important;
  width: auto !important;
  min-width: 0 !important;
  overflow: visible !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__bd {
  position: relative !important;
  z-index: 1 !important;
  height: 72px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  overflow: visible !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__label {
  position: relative !important;
  z-index: 2 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 4px !important;
  min-width: 52px !important;
  min-height: 58px !important;
  margin-top: 0 !important;
  color: #64748b !important;
  font-size: 11px !important;
  line-height: 1.2 !important;
  font-weight: 800 !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__label::before {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: inherit;
  background: currentColor;
  box-sizing: border-box;
  content: "";
  -webkit-mask: var(--tab-icon) center / contain no-repeat;
  mask: var(--tab-icon) center / contain no-repeat;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(2) .uni-tabbar__label::before {
  --tab-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M10 2h4v4l2 3v9a4 4 0 0 1-8 0V9l2-3V2Z' fill='none' stroke='%23000' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M9 12h6' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(3) .uni-tabbar__label::before {
  --tab-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M4 5.5h16v13H4z' fill='none' stroke='%23000' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='m4 15 4.5-4 3.5 3 2.5-2.5L20 16' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Ccircle cx='15.5' cy='9' r='1.5' fill='%23000'/%3E%3C/svg%3E");
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(4) .uni-tabbar__label::before {
  --tab-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='4' y='5' width='16' height='14' rx='4' fill='none' stroke='%23000' stroke-width='2'/%3E%3Cpath d='M8 12h4M10 10v4M16 10.5v.01M17.5 13.5v.01' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(5) .uni-tabbar__label::before {
  --tab-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M5 6.5h14v10H9l-4 3v-13Z' fill='none' stroke='%23000' stroke-width='2' stroke-linejoin='round'/%3E%3Cpath d='M8 10h8M8 13h5' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(6) .uni-tabbar__label::before {
  --tab-icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='8' r='3.5' fill='none' stroke='%23000' stroke-width='2'/%3E%3Cpath d='M5 20a7 7 0 0 1 14 0' fill='none' stroke='%23000' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E");
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="37, 99, 235"]) .uni-tabbar__bd::before,
uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="45, 108, 115"]) .uni-tabbar__bd::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 9px;
  width: 52px;
  height: 52px;
  transform: translateX(-50%);
  border-radius: 18px;
  background: #eff6ff;
  box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.12);
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="37, 99, 235"]) .uni-tabbar__label,
uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="45, 108, 115"]) .uni-tabbar__label {
  color: #2563eb !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="37, 99, 235"]) .uni-tabbar__label::before,
uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="45, 108, 115"]) .uni-tabbar__label::before {
  color: #2563eb;
  background: currentColor;
}

@media (min-width: 720px) {
  uni-app.uni-app--showtabbar uni-tabbar.uni-tabbar-bottom {
    right: auto !important;
    bottom: calc(14px + env(safe-area-inset-bottom)) !important;
    left: 50% !important;
    width: 520px !important;
    max-width: 520px !important;
    transform: translateX(-50%) !important;
    border-radius: 24px !important;
  }

  uni-tabbar.uni-tabbar-bottom .uni-tabbar {
    width: 520px !important;
    max-width: 520px !important;
    border-radius: 24px !important;
  }
}
</style>
