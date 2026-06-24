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
