export function showToast(title: string): void {
  if (typeof uni !== 'undefined' && uni.showToast) {
    uni.showToast({ title, icon: 'none' })
  }
}

export function navigateTo(url: string): void {
  if (typeof uni !== 'undefined' && uni.navigateTo) {
    uni.navigateTo({ url })
  }
}

export function switchTab(url: string): void {
  if (typeof uni !== 'undefined' && uni.switchTab) {
    uni.switchTab({ url })
  }
}

export function setTabBadge(index: number, text: string): void {
  if (typeof uni !== 'undefined' && uni.setTabBarBadge) {
    uni.setTabBarBadge({ index, text })
  }
}

export function removeTabBadge(index: number): void {
  if (typeof uni !== 'undefined' && uni.removeTabBarBadge) {
    uni.removeTabBarBadge({ index })
  }
}
