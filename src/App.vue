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
      import('./pages/treehole/index.vue'),
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
  background: #eef3f1;
  color: #172126;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  letter-spacing: 0;
}

.app-shell {
  min-height: 100%;
  background:
    radial-gradient(circle at 18% -8%, rgba(35, 108, 114, 0.1), transparent 28%),
    radial-gradient(circle at 92% 0%, rgba(216, 117, 139, 0.08), transparent 25%),
    linear-gradient(180deg, #fbfcfa 0%, #eef3f1 48%, #edf1ee 100%);
}

/* H5 tabBar visual upgrade. Native MP tabBar keeps using pages.json. */
uni-app.uni-app--showtabbar uni-tabbar.uni-tabbar-bottom {
  bottom: calc(14px + env(safe-area-inset-bottom)) !important;
  left: 50% !important;
  width: calc(100% - 28px) !important;
  max-width: 520px !important;
  transform: translateX(-50%) !important;
  border-radius: 24px !important;
  overflow: visible !important;
  z-index: 99 !important;
}

uni-app.uni-app--showtabbar uni-tabbar.uni-tabbar-bottom .uni-placeholder {
  height: 84px !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar {
  height: 72px !important;
  border: 1px solid rgba(23, 33, 38, 0.1) !important;
  border-radius: 24px !important;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(246, 251, 248, 0.94)) !important;
  box-shadow: 0 18px 45px rgba(31, 54, 58, 0.2) !important;
  backdrop-filter: blur(18px) !important;
  overflow: visible !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar-border {
  display: none !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item {
  position: relative !important;
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
  color: #65757b !important;
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
  border-radius: 50%;
  color: #236c72;
  background: rgba(35, 108, 114, 0.08);
  font-size: 13px;
  font-weight: 900;
  line-height: 1;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(1) .uni-tabbar__label::before {
  content: "瓶";
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(2) .uni-tabbar__label::before {
  content: "广";
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(3) .uni-tabbar__label::before {
  content: "玩";
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(4) .uni-tabbar__label::before {
  content: "树";
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:nth-child(5) .uni-tabbar__label::before {
  content: "我";
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="45, 108, 115"]) .uni-tabbar__bd::before {
  content: "";
  position: absolute;
  left: 50%;
  top: -13px;
  width: 62px;
  height: 72px;
  transform: translateX(-50%);
  border-radius: 34px 34px 18px 18px;
  background:
    linear-gradient(180deg, #2f7f6d, #236c72),
    radial-gradient(circle at 50% 16%, rgba(255, 255, 255, 0.28), transparent 24px);
  box-shadow: 0 14px 30px rgba(35, 108, 114, 0.28);
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="45, 108, 115"]) .uni-tabbar__label {
  color: #fff !important;
}

uni-tabbar.uni-tabbar-bottom .uni-tabbar__item:has(.uni-tabbar__label[style*="45, 108, 115"]) .uni-tabbar__label::before {
  color: #236c72;
  background: rgba(255, 255, 255, 0.94);
}

@media (min-width: 720px) {
  uni-app.uni-app--showtabbar uni-tabbar.uni-tabbar-bottom {
    max-width: 520px !important;
  }
}
</style>
