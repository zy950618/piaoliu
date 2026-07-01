<template>
  <view class="page game-page safe-bottom">
    <view class="cosmic-layer star-field star-field-far"></view>
    <view class="cosmic-layer star-field star-field-mid"></view>
    <view class="cosmic-layer star-field star-field-near"></view>
    <view class="cosmic-layer star-field star-field-dust"></view>
    <view class="cosmic-layer nebula nebula-a"></view>
    <view class="cosmic-layer nebula nebula-b"></view>
    <view class="cosmic-layer depth-planet depth-planet-far"></view>
    <view class="cosmic-layer depth-planet depth-planet-near"></view>
    <view class="cosmic-layer meteor meteor-big"></view>
    <view class="cosmic-layer meteor meteor-a"></view>
    <view class="cosmic-layer meteor meteor-b"></view>
    <view class="cosmic-layer meteor meteor-c"></view>
    <view class="cosmic-layer meteor meteor-d"></view>
    <view class="cosmic-layer meteor meteor-e"></view>
    <view class="cosmic-layer meteor meteor-corner"></view>
    <view class="cosmic-layer meteor meteor-corner-small"></view>
    <view class="cosmic-layer corner-dust"></view>
    <view class="cosmic-layer corner-comet"></view>
    <view class="cosmic-layer spaceship spaceship-main">
      <view class="ship-aura"></view>
      <image class="ship-image" src="/static/ships/aurora-cruiser.svg" mode="widthFix" />
    </view>
    <view class="cosmic-layer spaceship spaceship-far">
      <view class="ship-aura"></view>
      <image class="ship-image" src="/static/ships/aurora-cruiser.svg" mode="widthFix" />
    </view>
    <view class="cosmic-layer spaceship spaceship-low">
      <view class="ship-aura"></view>
      <image class="ship-image" src="/static/ships/aurora-cruiser.svg" mode="widthFix" />
    </view>

    <view class="room-entry-dock">
      <view class="room-entry solo-entry" @tap="openRoomConcept('solo')">
        <view class="room-entry-top">
          <text class="room-entry-label">单聊私密</text>
          <text class="room-entry-icon solo-icon" />
        </view>
        <text class="room-entry-title">1v1 房间</text>
        <text class="room-entry-meta">从私聊进入</text>
      </view>
      <view class="room-entry group-entry" @tap="openRoomConcept('group')">
        <view class="room-entry-top">
          <text class="room-entry-label">群聊私密</text>
          <text class="room-entry-icon group-icon" />
        </view>
        <text class="room-entry-title">多人房间</text>
        <text class="room-entry-meta">邀请制进入</text>
      </view>
      <view class="room-entry random-entry" @tap="openRandomMatch">
        <view class="room-entry-top">
          <text class="room-entry-label">随机匹配</text>
          <text class="room-entry-icon random-icon" />
        </view>
        <text class="room-entry-title">按条件找玩伴</text>
        <text class="room-entry-meta">性别 / 年龄 / 次数同步</text>
      </view>
    </view>

    <view class="section activity-system" :class="{ rolling: diceRolling }">
      <view class="space-field"></view>
      <view class="orbit-ring orbit-one"></view>
      <view class="orbit-ring orbit-two"></view>
      <view class="orbit-ring orbit-three"></view>
      <view class="orbit-ring orbit-four"></view>
      <view class="orbit-ring orbit-five"></view>
      <view class="orbit-ring orbit-six"></view>
      <view class="orbit-ring orbit-seven"></view>
      <view class="orbit-ring orbit-eight"></view>
      <view
        v-for="entry in activityEntries"
        :key="entry.key"
        class="activity-planet"
        :class="[entry.key, { active: activeMode === entry.mode }]"
        @tap="playEntry(entry)"
      >
        <view class="planet-ring"></view>
        <view class="planet-surface"></view>
        <text class="planet-badge">+{{ gameQuotaLeft(entry.quotaType) }}</text>
        <text class="planet-label">{{ entry.label }}</text>
      </view>
      <view class="activity-planet dice-entry" @tap="rollDice">
        <view class="planet-ring"></view>
        <view class="planet-surface"></view>
        <text class="planet-label">摇骰子</text>
      </view>
    </view>

    <view v-if="composerOpen" class="modal-mask center-mask">
      <view class="modal-card game-compose-card" @tap.stop @click.stop>
        <text class="modal-kicker">{{ activeModeLabel }}</text>
        <view class="textarea-shell">
          <textarea
            v-model="gameDraft"
            class="game-textarea"
            maxlength="240"
            :placeholder="draftPlaceholder"
            @input="clearGameError"
          />
          <view class="random-tip-button" @tap.stop="fillRandomGamePrompt" @click.stop="fillRandomGamePrompt">
            {{ randomLoading ? '生成中' : '随机' }}
          </view>
        </view>
        <text v-if="gameError" class="game-error">{{ gameError }}</text>
        <view class="option-block">
          <text class="field-label">含义</text>
          <view class="meaning-card">{{ activePromptMeaning }}</view>
        </view>
        <view class="option-block">
          <text class="field-label">选择对象</text>
          <view class="choice-row">
            <view
              v-for="item in genderOptions"
              :key="item.value"
              class="choice-chip"
              :class="[item.value, { active: selectedGender === item.value }]"
              @tap.stop="selectedGender = item.value"
              @click.stop="selectedGender = item.value"
            >
              {{ item.label }}
            </view>
          </view>
        </view>
        <view class="modal-actions">
          <view class="button ghost" @tap.stop="closeComposer" @click.stop="closeComposer">取消</view>
          <view class="button" :class="{ disabled: !gameDraft.trim() }" @tap.stop="submitGamePrompt" @click.stop="submitGamePrompt">开始</view>
        </view>
      </view>
    </view>

    <view v-if="currentText" class="section result-card">
      <text class="result-kicker">{{ activeModeLabel }}</text>
      <text class="result-text">{{ currentText }}</text>
      <view class="result-meta">
        <text>含义：{{ currentMeaning }}</text>
        <text>对象：{{ currentGenderLabel }}</text>
      </view>
      <view class="grid-2 result-actions">
        <view class="button secondary" @tap="save">保存</view>
        <view class="button ghost" @tap="shareToBottle">投递成瓶子</view>
      </view>
    </view>

    <view v-if="roomConceptOpen" class="modal-mask center-mask" @tap="closeRoomConcept">
      <view class="modal-card room-concept-card" @tap.stop @click.stop>
        <text class="modal-kicker">{{ activeRoomConcept.kicker }}</text>
        <text class="room-concept-title">{{ activeRoomConcept.title }}</text>
        <text class="room-concept-body">{{ activeRoomConcept.body }}</text>
        <view class="room-concept-flow">
          <text v-for="step in activeRoomConcept.steps" :key="step">{{ step }}</text>
        </view>
        <view class="modal-actions">
          <view class="button ghost" @tap.stop="closeRoomConcept" @click.stop="closeRoomConcept">关闭</view>
          <view class="button" @tap.stop="enterRoomConcept" @click.stop="enterRoomConcept">{{ activeRoomConcept.action }}</view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useQuotaGuard } from '@/composables/useQuotaGuard'
import { businessApi } from '@/services/businessApi'
import { navigateTo, showToast, switchTab } from '@/services/feedback'
import { useAppStore } from '@/stores/app'
import { useContentStore } from '@/stores/content'
import type { BottleTargetGender } from '@/types/domain'

type GameMode = 'truth_public' | 'truth_private' | 'dare_public' | 'dare_private'
type TargetGender = Exclude<BottleTargetGender, 'all'>
type RoomKind = 'solo' | 'group'
type ActivityEntry = {
  key: string
  mode: GameMode
  label: string
  quotaType: 'truth' | 'dare'
}
type GamePrompt = {
  id: string
  text: string
  meaning: string
  visibility: string
}
type RoomConcept = {
  kicker: string
  title: string
  body: string
  steps: string[]
  action: string
}

const app = useAppStore()
const content = useContentStore()
const { ensureQuota } = useQuotaGuard()
const activeMode = ref<GameMode>('truth_public')
const currentText = ref('')
const currentMeaning = ref('自定义玩法内容')
const currentGender = ref<TargetGender>('female')
const currentSourceId = ref<string>()
const diceRolling = ref(false)
const composerOpen = ref(false)
const gameDraft = ref('')
const gameError = ref('')
const selectedPrompt = ref<GamePrompt>()
const selectedGender = ref<TargetGender>('female')
const randomLoading = ref(false)
const roomConceptOpen = ref(false)
const activeRoomKind = ref<RoomKind>('solo')

const modes = [
  { key: 'truth_public', label: '常规真心话' },
  { key: 'truth_private', label: '私密真心话' },
  { key: 'dare_public', label: '常规大冒险' },
  { key: 'dare_private', label: '私密大冒险' }
] as const

const activityEntries: ActivityEntry[] = [
  { key: 'truth-public', mode: 'truth_public', label: '常规真心话', quotaType: 'truth' },
  { key: 'truth-private', mode: 'truth_private', label: '私密真心话', quotaType: 'truth' },
  { key: 'dare-public', mode: 'dare_public', label: '常规大冒险', quotaType: 'dare' },
  { key: 'dare-private', mode: 'dare_private', label: '私密大冒险', quotaType: 'dare' }
]

const genderOptions: Array<{ value: TargetGender; label: string }> = [
  { value: 'female', label: '女生' },
  { value: 'male', label: '男生' }
]

const roomConcepts: Record<RoomKind, RoomConcept> = {
  solo: {
    kicker: '单个私密聊',
    title: '1v1 私密房间',
    body: '入口放在私聊关系里，适合两个人进行真心话、大冒险、礼物和限时内容。',
    steps: ['私聊', '开房间', '两人互动'],
    action: '去私聊'
  },
  group: {
    kicker: '群聊私密房间',
    title: '邀请制多人房间',
    body: '入口独立放在游戏页，后续接入邀请、房主控制、成员列表和房间话题。',
    steps: ['创建', '邀请', '多人互动'],
    action: '预留入口'
  }
}

const activeModeLabel = computed(() => modes.find((mode) => mode.key === activeMode.value)?.label || '游戏')
const activePromptMeaning = computed(() => selectedPrompt.value?.meaning || '可以自己输入，也可以点随机从当前玩法题库取一条。')
const draftPlaceholder = computed(() => activeMode.value.startsWith('truth') ? '写下一个真心话问题，或点随机生成。' : '写下一个大冒险任务，或点随机生成。')
const currentGenderLabel = computed(() => genderLabel(currentGender.value))
const activeRoomConcept = computed(() => roomConcepts[activeRoomKind.value])

onLoad(() => app.hydrate())

function rollDice() {
  if (diceRolling.value) return
  diceRolling.value = true
  const next = Math.floor(Math.random() * 6) + 1

  setTimeout(() => {
    diceRolling.value = false
    showToast(`骰子点数 ${next}`)
  }, 520)
}

function gameQuotaLeft(type: ActivityEntry['quotaType']) {
  return app.quotas?.[type]?.remaining ?? 0
}

async function playEntry(entry: ActivityEntry) {
  activeMode.value = entry.mode
  openComposer()
}

function openComposer() {
  gameDraft.value = ''
  gameError.value = ''
  selectedPrompt.value = undefined
  selectedGender.value = 'female'
  composerOpen.value = true
}

function closeComposer() {
  composerOpen.value = false
  gameDraft.value = ''
  gameError.value = ''
  selectedPrompt.value = undefined
}

async function fillRandomGamePrompt() {
  if (randomLoading.value) return
  randomLoading.value = true
  try {
    const prompt = await businessApi.getGamePrompt(activeMode.value)
    selectedPrompt.value = prompt
    gameDraft.value = prompt.text
    gameError.value = ''
  } catch {
    showToast('题库加载失败')
  } finally {
    randomLoading.value = false
  }
}

function clearGameError() {
  if (gameError.value && gameDraft.value.trim()) gameError.value = ''
  if (selectedPrompt.value && gameDraft.value.trim() !== selectedPrompt.value.text) selectedPrompt.value = undefined
}

async function submitGamePrompt() {
  if (!gameDraft.value.trim()) {
    gameError.value = activeMode.value.startsWith('truth') ? '先写一个真心话问题' : '先写一个大冒险任务'
    showToast(gameError.value)
    return
  }

  if (activeMode.value.startsWith('truth')) {
    if (!ensureQuota('truth')) return
    await content.drawTruthQuestion()
  } else {
    if (!ensureQuota('dare')) return
    await content.drawDareTask()
  }

  currentText.value = gameDraft.value.trim()
  currentMeaning.value = selectedPrompt.value?.meaning || '自定义玩法内容'
  currentGender.value = selectedGender.value
  currentSourceId.value = selectedPrompt.value?.id
  composerOpen.value = false
  gameDraft.value = ''
  selectedPrompt.value = undefined
  showToast(`已开始${activeModeLabel.value}`)
}

async function save() {
  if (!currentText.value) {
    showToast('先开始一个玩法')
    return
  }
  await content.saveUserActivityRecord({
    recordType: 'game',
    title: activeModeLabel.value,
    content: currentText.value,
    visibility: `对象：${currentGenderLabel.value}`,
    sourceType: activeMode.value,
    sourceId: currentSourceId.value
  })
  showToast('已保存到游戏记录')
}

async function shareToBottle() {
  if (!currentText.value) return
  if (!ensureQuota('throw_bottle')) return
  await content.throwBottle(currentText.value, { targetGender: currentGender.value })
  showToast(`已投递给${currentGenderLabel.value}，扔瓶次数 -1`)
}

function genderLabel(gender: TargetGender) {
  return genderOptions.find((item) => item.value === gender)?.label || '对方'
}

function openRoomConcept(kind: RoomKind) {
  activeRoomKind.value = kind
  roomConceptOpen.value = true
}

function closeRoomConcept() {
  roomConceptOpen.value = false
}

function openRandomMatch() {
  navigateTo('/pages/game/match')
}

function enterRoomConcept() {
  if (activeRoomKind.value === 'solo') {
    roomConceptOpen.value = false
    switchTab('/pages/messages/index')
    return
  }
  showToast('群聊私密房间入口已预留')
  roomConceptOpen.value = false
}
</script>

<style scoped lang="scss">
.game-page {
  position: fixed;
  top: 0;
  right: 0;
  bottom: var(--window-bottom);
  left: 0;
  overflow: hidden;
  width: 100%;
  max-width: 520px;
  height: auto;
  min-height: 0;
  margin: 0 auto;
  padding: 0 24rpx;
  box-sizing: border-box;
  background:
    radial-gradient(circle at 18% 16%, rgba(122, 205, 198, 0.24), transparent 24%),
    radial-gradient(circle at 84% 22%, rgba(246, 147, 177, 0.22), transparent 25%),
    radial-gradient(circle at 54% 64%, rgba(255, 186, 87, 0.14), transparent 30%),
    radial-gradient(circle at 18% 72%, rgba(255, 255, 255, 0.5) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 42% 26%, rgba(255, 255, 255, 0.42) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 72% 58%, rgba(255, 255, 255, 0.36) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 86% 78%, rgba(255, 255, 255, 0.32) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 12% 34%, rgba(255, 255, 255, 0.3) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 28% 86%, rgba(255, 255, 255, 0.42) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 62% 82%, rgba(255, 255, 255, 0.28) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 92% 46%, rgba(255, 255, 255, 0.34) 0 1rpx, transparent 2rpx),
    linear-gradient(180deg, #07111f 0%, #0b1d2c 46%, #102f35 100%);
}

.game-page.safe-bottom {
  padding-bottom: 0;
}

.game-page::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 30% 40%, rgba(255, 255, 255, 0.28) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 58% 18%, rgba(255, 255, 255, 0.24) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 76% 36%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 12% 50%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 36% 72%, rgba(255, 255, 255, 0.26) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 84% 68%, rgba(255, 255, 255, 0.24) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 48% 92%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 7% 88%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    linear-gradient(115deg, transparent 0 42%, rgba(255, 255, 255, 0.08) 43%, transparent 48%);
  opacity: 0.85;
}

.cosmic-layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.star-field-far {
  background:
    radial-gradient(circle at 6% 12%, rgba(255, 255, 255, 0.46) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 18% 26%, rgba(255, 255, 255, 0.3) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 36% 10%, rgba(255, 255, 255, 0.35) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 58% 18%, rgba(255, 255, 255, 0.42) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 78% 12%, rgba(255, 255, 255, 0.34) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 92% 30%, rgba(255, 255, 255, 0.42) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 13% 48%, rgba(255, 255, 255, 0.28) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 44% 42%, rgba(255, 255, 255, 0.36) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 72% 48%, rgba(255, 255, 255, 0.3) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 88% 62%, rgba(255, 255, 255, 0.34) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 20% 78%, rgba(255, 255, 255, 0.34) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 52% 86%, rgba(255, 255, 255, 0.32) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 82% 84%, rgba(255, 255, 255, 0.3) 0 1rpx, transparent 2rpx);
  opacity: 0.7;
}

.star-field-mid {
  background:
    radial-gradient(circle at 12% 20%, rgba(178, 239, 255, 0.72) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 30% 34%, rgba(255, 255, 255, 0.58) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 64% 28%, rgba(255, 229, 166, 0.54) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 82% 44%, rgba(255, 201, 226, 0.52) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 24% 62%, rgba(255, 255, 255, 0.54) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 48% 66%, rgba(178, 239, 255, 0.46) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 70% 76%, rgba(255, 255, 255, 0.48) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 16% 91%, rgba(255, 229, 166, 0.5) 0 2rpx, transparent 3rpx);
  opacity: 0.65;
  animation: star-twinkle 4.8s ease-in-out infinite;
}

.star-field-near {
  background:
    radial-gradient(circle at 8% 54%, rgba(255, 255, 255, 0.8) 0 2rpx, transparent 4rpx),
    radial-gradient(circle at 36% 58%, rgba(255, 255, 255, 0.74) 0 2rpx, transparent 4rpx),
    radial-gradient(circle at 58% 42%, rgba(178, 239, 255, 0.72) 0 2rpx, transparent 4rpx),
    radial-gradient(circle at 84% 70%, rgba(255, 255, 255, 0.68) 0 2rpx, transparent 4rpx);
  opacity: 0.62;
  filter: drop-shadow(0 0 8rpx rgba(255, 255, 255, 0.5));
  animation: star-twinkle 3.4s ease-in-out infinite reverse;
}

.star-field-dust {
  background:
    radial-gradient(circle at 4% 8%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 10% 18%, rgba(255, 255, 255, 0.18) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 16% 38%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 24% 14%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 31% 52%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 39% 76%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 46% 31%, rgba(255, 255, 255, 0.18) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 53% 55%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 61% 9%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 68% 62%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 74% 86%, rgba(255, 255, 255, 0.18) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 81% 24%, rgba(255, 255, 255, 0.22) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 88% 52%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 96% 74%, rgba(255, 255, 255, 0.2) 0 1rpx, transparent 2rpx);
  opacity: 0.72;
}

.nebula {
  border-radius: 50%;
  filter: blur(22rpx);
  opacity: 0.62;
}

.nebula-a {
  inset: 94rpx auto auto -110rpx;
  width: 420rpx;
  height: 520rpx;
  background:
    radial-gradient(circle at 44% 36%, rgba(74, 202, 195, 0.38), transparent 45%),
    radial-gradient(circle at 70% 70%, rgba(65, 118, 255, 0.22), transparent 46%);
}

.nebula-b {
  inset: 120rpx -140rpx auto auto;
  width: 520rpx;
  height: 580rpx;
  background:
    radial-gradient(circle at 34% 34%, rgba(255, 127, 174, 0.28), transparent 44%),
    radial-gradient(circle at 62% 72%, rgba(255, 205, 116, 0.18), transparent 50%);
}

.depth-planet {
  inset: auto;
  border-radius: 50%;
  pointer-events: none;
}

.depth-planet-far {
  top: 72rpx;
  right: -310rpx;
  width: 560rpx;
  height: 560rpx;
  opacity: 0.28;
  background:
    radial-gradient(circle at 36% 34%, rgba(255, 255, 255, 0.18) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 44% 42%, rgba(126, 242, 255, 0.18), transparent 38%),
    linear-gradient(145deg, rgba(38, 85, 144, 0.42), rgba(7, 13, 34, 0.08) 62%);
  box-shadow: inset 36rpx 28rpx 90rpx rgba(255, 255, 255, 0.08), inset -90rpx -80rpx 110rpx rgba(0, 0, 0, 0.42);
  filter: blur(1rpx);
}

.depth-planet-near {
  z-index: 1;
  left: -280rpx;
  bottom: -340rpx;
  width: 680rpx;
  height: 680rpx;
  opacity: 0.42;
  background:
    radial-gradient(circle at 58% 34%, rgba(126, 242, 255, 0.18), transparent 32%),
    linear-gradient(145deg, rgba(11, 35, 51, 0.08), rgba(3, 9, 23, 0.72) 70%);
  box-shadow: inset 64rpx 40rpx 110rpx rgba(126, 242, 255, 0.12), inset -130rpx -120rpx 150rpx rgba(0, 0, 0, 0.62);
}

.meteor {
  left: auto;
  bottom: auto;
  width: 220rpx;
  height: 3rpx;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.96) 9%, rgba(132, 231, 255, 0.52) 28%, rgba(132, 231, 255, 0.14) 68%, transparent 100%);
  box-shadow: 0 0 26rpx rgba(255, 255, 255, 0.72), 0 0 42rpx rgba(132, 231, 255, 0.34);
  transform: rotate(var(--meteor-angle));
  opacity: 0;
  animation: meteor-flight 5.8s linear infinite;
  --meteor-angle: -28deg;
}

.meteor::after {
  content: '';
  position: absolute;
  left: 18rpx;
  top: -3rpx;
  width: 9rpx;
  height: 9rpx;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 18rpx rgba(255, 255, 255, 0.86);
}

.meteor-big {
  top: 192rpx;
  right: -40rpx;
  width: 660rpx;
  height: 8rpx;
  background: linear-gradient(90deg, transparent 0%, #fff 6%, rgba(196, 246, 255, 0.94) 13%, rgba(119, 223, 255, 0.5) 46%, rgba(119, 223, 255, 0.12) 78%, transparent 100%);
  box-shadow: 0 0 34rpx rgba(255, 255, 255, 0.9), 0 0 70rpx rgba(92, 218, 255, 0.5);
  animation-delay: -1.1s;
  animation-duration: 7.4s;
  --meteor-angle: -24deg;
}

.meteor-big::after {
  left: 28rpx;
  top: -6rpx;
  width: 17rpx;
  height: 17rpx;
  box-shadow: 0 0 28rpx rgba(255, 255, 255, 0.96), 0 0 52rpx rgba(119, 223, 255, 0.62);
}

.meteor-a {
  top: 122rpx;
  right: -50rpx;
  width: 280rpx;
  --meteor-angle: -28deg;
}

.meteor-b {
  top: 258rpx;
  right: -90rpx;
  width: 190rpx;
  animation-delay: -1.4s;
  animation-duration: 6.6s;
  --meteor-angle: -20deg;
}

.meteor-c {
  top: 456rpx;
  right: -70rpx;
  width: 240rpx;
  animation-delay: -3.1s;
  animation-duration: 7.2s;
  --meteor-angle: -31deg;
}

.meteor-d {
  top: 690rpx;
  right: -100rpx;
  width: 170rpx;
  animation-delay: -4.5s;
  animation-duration: 6.2s;
  --meteor-angle: -24deg;
}

.meteor-e {
  top: 340rpx;
  right: 250rpx;
  width: 120rpx;
  opacity: 0.34;
  animation-delay: -2.3s;
  animation-duration: 8s;
  --meteor-angle: -15deg;
}

.meteor-corner {
  right: -22rpx;
  bottom: 252rpx;
  width: 340rpx;
  height: 5rpx;
  box-shadow: 0 0 28rpx rgba(255, 255, 255, 0.82), 0 0 52rpx rgba(132, 231, 255, 0.42);
  opacity: 0;
  animation-name: corner-meteor-flight;
  animation-delay: -0.8s;
  animation-duration: 6.8s;
  --meteor-angle: -32deg;
}

.meteor-corner::after {
  left: 20rpx;
  top: -4rpx;
  width: 11rpx;
  height: 11rpx;
}

.meteor-corner-small {
  right: -10rpx;
  bottom: 152rpx;
  width: 190rpx;
  height: 3rpx;
  box-shadow: 0 0 20rpx rgba(255, 255, 255, 0.66), 0 0 34rpx rgba(132, 231, 255, 0.28);
  animation-name: corner-meteor-flight;
  animation-delay: -1.6s;
  animation-duration: 7.4s;
  --meteor-angle: -26deg;
}

.corner-dust {
  inset: auto -12rpx 96rpx auto;
  width: 300rpx;
  height: 300rpx;
  opacity: 0.56;
  background:
    radial-gradient(circle at 18% 26%, rgba(255, 255, 255, 0.48) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 42% 18%, rgba(126, 242, 255, 0.42) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 68% 34%, rgba(255, 240, 166, 0.34) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 78% 68%, rgba(255, 255, 255, 0.34) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 34% 76%, rgba(126, 242, 255, 0.26) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 62% 86%, rgba(255, 255, 255, 0.32) 0 1rpx, transparent 2rpx),
    radial-gradient(circle at 54% 54%, rgba(126, 242, 255, 0.12), transparent 46%);
  filter: drop-shadow(0 0 10rpx rgba(126, 242, 255, 0.16));
}

.corner-comet {
  inset: auto -24rpx 278rpx auto;
  width: 250rpx;
  height: 5rpx;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.82) 10%, rgba(132, 231, 255, 0.42) 36%, rgba(132, 231, 255, 0.1) 74%, transparent 100%);
  box-shadow: 0 0 24rpx rgba(255, 255, 255, 0.58), 0 0 42rpx rgba(132, 231, 255, 0.28);
  opacity: 0.62;
  transform: rotate(-25deg);
  animation: corner-comet-pulse 3.2s ease-in-out infinite;
}

.corner-comet::after {
  content: '';
  position: absolute;
  left: 18rpx;
  top: -4rpx;
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 24rpx rgba(255, 255, 255, 0.84);
}

.spaceship {
  inset: auto;
  z-index: 1;
  width: 250rpx;
  height: 126rpx;
  opacity: 0.86;
  filter: drop-shadow(0 18rpx 30rpx rgba(0, 0, 0, 0.25));
  animation: ship-drift 7.2s ease-in-out infinite;
  --ship-rotate: -13deg;
  --ship-scale: 1;
}

.spaceship-main {
  top: 186rpx;
  left: 28rpx;
  z-index: 2;
}

.spaceship-far {
  top: 132rpx;
  left: 426rpx;
  opacity: 0.38;
  filter: blur(0.4px) drop-shadow(0 10rpx 22rpx rgba(0, 0, 0, 0.2));
  animation-delay: -2.2s;
  --ship-rotate: 18deg;
  --ship-scale: 0.52;
}

.spaceship-low {
  left: 42rpx;
  bottom: 172rpx;
  opacity: 0.56;
  filter: drop-shadow(0 12rpx 24rpx rgba(0, 0, 0, 0.24));
  animation-delay: -4.1s;
  --ship-rotate: -23deg;
  --ship-scale: 0.54;
}

.ship-image,
.ship-aura {
  position: absolute;
}

.ship-image {
  inset: 0;
  z-index: 2;
  width: 100%;
  height: auto;
}

.ship-aura {
  z-index: 1;
  top: 47%;
  left: -46rpx;
  width: 130rpx;
  height: 30rpx;
  border-radius: 50%;
  background: linear-gradient(90deg, transparent 0%, rgba(111, 226, 255, 0.18) 24%, rgba(111, 226, 255, 0.62) 64%, rgba(255, 194, 108, 0.92) 100%);
  filter: blur(2rpx);
  transform: translateY(-50%);
  animation: trail-pulse 1.8s ease-in-out infinite;
}

.room-entry-dock {
  position: absolute;
  top: 28rpx;
  right: 24rpx;
  left: 24rpx;
  z-index: 4;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14rpx;
}

.room-entry {
  position: relative;
  overflow: hidden;
  min-height: 128rpx;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 20px;
  padding: 18rpx;
  color: #fff;
  box-sizing: border-box;
  box-shadow: 0 18rpx 42rpx rgba(0, 0, 0, 0.18);
}

.room-entry::after {
  position: absolute;
  right: -36rpx;
  bottom: -42rpx;
  width: 132rpx;
  height: 132rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
  content: '';
}

.solo-entry {
  background:
    radial-gradient(circle at 18% 8%, rgba(255, 255, 255, 0.24), transparent 28%),
    linear-gradient(145deg, rgba(20, 184, 166, 0.94), rgba(37, 99, 235, 0.9));
}

.group-entry {
  background:
    radial-gradient(circle at 18% 8%, rgba(255, 255, 255, 0.22), transparent 30%),
    linear-gradient(145deg, rgba(244, 114, 182, 0.94), rgba(124, 58, 237, 0.88));
}

.random-entry {
  grid-column: 1 / -1;
  min-height: 116rpx;
  background:
    radial-gradient(circle at 14% 10%, rgba(255, 255, 255, 0.24), transparent 28%),
    linear-gradient(135deg, rgba(34, 211, 238, 0.94), rgba(16, 185, 129, 0.88));
}

.room-entry-top {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12rpx;
}

.room-entry-label,
.room-entry-title,
.room-entry-meta {
  position: relative;
  z-index: 1;
  display: block;
}

.room-entry-label {
  opacity: 0.76;
  font-size: 21rpx;
  font-weight: 900;
}

.room-entry-title {
  margin-top: 12rpx;
  font-size: 30rpx;
  font-weight: 900;
  line-height: 1.15;
}

.room-entry-meta {
  margin-top: 8rpx;
  opacity: 0.82;
  font-size: 22rpx;
  font-weight: 800;
}

.room-entry-icon {
  position: relative;
  flex: 0 0 auto;
  width: 42rpx;
  height: 42rpx;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.18);
}

.room-entry-icon::before,
.room-entry-icon::after {
  position: absolute;
  content: '';
  box-sizing: border-box;
}

.solo-icon::before {
  inset: 9rpx 12rpx 18rpx;
  border-radius: 50%;
  background: #fff;
}

.solo-icon::after {
  left: 10rpx;
  bottom: 8rpx;
  width: 22rpx;
  height: 13rpx;
  border: 3rpx solid rgba(255, 255, 255, 0.9);
  border-radius: 13rpx 13rpx 6rpx 6rpx;
}

.group-icon::before {
  left: 9rpx;
  top: 10rpx;
  width: 14rpx;
  height: 14rpx;
  border-radius: 50%;
  background: #fff;
  box-shadow: 13rpx 3rpx 0 -1rpx rgba(255, 255, 255, 0.86);
}

.group-icon::after {
  left: 8rpx;
  bottom: 8rpx;
  width: 28rpx;
  height: 13rpx;
  border: 3rpx solid rgba(255, 255, 255, 0.9);
  border-radius: 14rpx 14rpx 6rpx 6rpx;
}

.random-icon::before {
  left: 9rpx;
  top: 10rpx;
  width: 24rpx;
  height: 24rpx;
  border: 4rpx solid #fff;
  border-radius: 50%;
}

.random-icon::after {
  right: 8rpx;
  top: 8rpx;
  width: 15rpx;
  height: 15rpx;
  border-top: 4rpx solid #fff;
  border-right: 4rpx solid #fff;
}

.activity-system {
  position: relative;
  z-index: 2;
  height: 100%;
  margin-top: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}

.space-field {
  position: absolute;
  inset: 2rpx -18rpx -6rpx;
  border-radius: 48% 52% 46% 54%;
  background:
    radial-gradient(circle at 24% 24%, rgba(122, 205, 198, 0.18), transparent 18%),
    radial-gradient(circle at 72% 30%, rgba(246, 147, 177, 0.14), transparent 20%),
    radial-gradient(circle at 50% 62%, rgba(255, 186, 87, 0.1), transparent 22%),
    radial-gradient(circle at 30% 68%, rgba(255, 255, 255, 0.42) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 42% 24%, rgba(255, 255, 255, 0.32) 0 2rpx, transparent 3rpx),
    radial-gradient(circle at 66% 70%, rgba(255, 255, 255, 0.3) 0 2rpx, transparent 3rpx);
  box-shadow: inset 0 28rpx 70rpx rgba(255, 255, 255, 0.04);
}

.orbit-ring {
  position: absolute;
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 50%;
  pointer-events: none;
}

.orbit-one {
  width: 820rpx;
  height: 500rpx;
  transform: rotate(-16deg);
}

.orbit-two {
  width: 680rpx;
  height: 680rpx;
  border-style: dashed;
  border-color: rgba(255, 211, 136, 0.28);
  transform: rotate(18deg);
}

.orbit-three {
  width: 900rpx;
  height: 330rpx;
  border-color: rgba(122, 205, 198, 0.22);
  transform: rotate(9deg);
}

.orbit-four {
  width: 600rpx;
  height: 860rpx;
  border-color: rgba(255, 255, 255, 0.16);
  border-style: dashed;
  transform: rotate(-34deg);
}

.orbit-five {
  width: 980rpx;
  height: 420rpx;
  border-color: rgba(255, 255, 255, 0.12);
  transform: rotate(-5deg);
}

.orbit-six {
  width: 720rpx;
  height: 940rpx;
  border-color: rgba(122, 205, 198, 0.14);
  transform: rotate(32deg);
}

.orbit-seven {
  width: 1120rpx;
  height: 560rpx;
  border-color: rgba(255, 255, 255, 0.13);
  transform: rotate(14deg);
}

.orbit-eight {
  width: 920rpx;
  height: 1040rpx;
  border-color: rgba(255, 211, 136, 0.14);
  border-style: dashed;
  transform: rotate(-42deg);
}

.orbit-ring::after {
  content: '';
  position: absolute;
  inset: 34rpx;
  border: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 50%;
}

.activity-planet {
  position: absolute;
  z-index: 1;
  width: 154rpx;
  height: 154rpx;
  box-sizing: border-box;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6rpx;
  color: #fff;
  text-align: center;
  transition: transform 160ms ease, box-shadow 160ms ease;
}

.activity-planet:active {
  transform: scale(0.96);
}

.activity-planet.active {
  filter: saturate(1.12);
}

.planet-surface {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow:
    0 24rpx 46rpx rgba(31, 54, 58, 0.16),
    inset -24rpx -30rpx 36rpx rgba(13, 35, 39, 0.22),
    inset 18rpx 18rpx 28rpx rgba(255, 255, 255, 0.2);
}

.activity-planet.active .planet-surface {
  box-shadow:
    0 28rpx 56rpx rgba(31, 54, 58, 0.22),
    0 0 0 10rpx rgba(255, 255, 255, 0.36),
    inset -24rpx -30rpx 36rpx rgba(13, 35, 39, 0.22),
    inset 18rpx 18rpx 28rpx rgba(255, 255, 255, 0.2);
}

.planet-surface::before {
  content: '';
  position: absolute;
  inset: 16rpx 52rpx auto 22rpx;
  height: 44rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.28);
  filter: blur(2rpx);
  transform: rotate(-24deg);
}

.planet-surface::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
}

.planet-ring {
  position: absolute;
  z-index: 0;
  width: 222rpx;
  height: 62rpx;
  border: 12rpx solid rgba(255, 255, 255, 0.48);
  border-left-color: rgba(255, 255, 255, 0.16);
  border-bottom-color: rgba(255, 255, 255, 0.24);
  border-radius: 50%;
  opacity: 0;
  transform: rotate(-18deg);
  box-shadow: 0 0 22rpx rgba(255, 255, 255, 0.24);
}

.planet-label {
  display: block;
  position: relative;
  z-index: 3;
  width: 132rpx;
  font-size: 21rpx;
  font-weight: 900;
  line-height: 1.22;
  letter-spacing: 0;
  text-align: center;
  text-shadow: 0 5rpx 18rpx rgba(0, 0, 0, 0.32);
}

.planet-badge {
  position: absolute;
  top: 6rpx;
  right: 2rpx;
  z-index: 4;
  min-width: 54rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.86);
  border-radius: 999px;
  padding: 7rpx 13rpx;
  color: #fff;
  background: #ff3b30;
  box-shadow: 0 10rpx 22rpx rgba(255, 59, 48, 0.3);
  font-size: 21rpx;
  font-weight: 900;
  line-height: 1;
  text-align: center;
  box-sizing: border-box;
}

.truth-public {
  top: 390rpx;
  left: 38rpx;
  animation: planet-float-a 4.8s ease-in-out infinite;
}

.truth-public .planet-surface {
  background:
    radial-gradient(circle at 70% 28%, rgba(145, 227, 208, 0.52) 0 13rpx, transparent 14rpx),
    radial-gradient(circle at 32% 68%, rgba(15, 76, 83, 0.38) 0 18rpx, transparent 19rpx),
    linear-gradient(152deg, rgba(255, 255, 255, 0.16) 16%, transparent 17% 28%, rgba(255, 255, 255, 0.13) 29% 38%, transparent 39%),
    linear-gradient(145deg, #2a9a97 0%, #236c72 52%, #12383d 100%);
}

.truth-public .planet-surface::after {
  background:
    radial-gradient(circle at 26% 32%, rgba(255, 255, 255, 0.28) 0 8rpx, transparent 9rpx),
    repeating-linear-gradient(170deg, transparent 0 22rpx, rgba(182, 246, 228, 0.12) 23rpx 32rpx);
}

.truth-private {
  top: 352rpx;
  left: 390rpx;
  animation: planet-float-b 5.2s ease-in-out infinite;
}

.truth-private .planet-ring {
  opacity: 1;
  border-color: rgba(255, 208, 221, 0.56);
  border-left-color: rgba(255, 208, 221, 0.16);
  border-bottom-color: rgba(255, 208, 221, 0.2);
}

.truth-private .planet-surface {
  background:
    radial-gradient(circle at 32% 68%, rgba(255, 215, 220, 0.36) 0 18rpx, transparent 19rpx),
    radial-gradient(circle at 68% 34%, rgba(132, 45, 83, 0.24) 0 20rpx, transparent 21rpx),
    linear-gradient(132deg, rgba(255, 255, 255, 0.18) 0 20%, transparent 21% 38%, rgba(255, 255, 255, 0.13) 39% 54%, transparent 55%),
    linear-gradient(145deg, #f07f91 0%, #bf5b73 52%, #7e3556 100%);
}

.truth-private .planet-surface::after {
  background:
    repeating-linear-gradient(28deg, rgba(255, 225, 231, 0.12) 0 14rpx, transparent 15rpx 34rpx),
    radial-gradient(circle at 44% 42%, rgba(255, 255, 255, 0.22) 0 7rpx, transparent 8rpx);
}

.dare-public {
  left: 404rpx;
  bottom: 404rpx;
  animation: planet-float-c 5.5s ease-in-out infinite;
}

.dare-public .planet-surface {
  background:
    radial-gradient(circle at 72% 64%, rgba(135, 72, 20, 0.26) 0 18rpx, transparent 19rpx),
    radial-gradient(circle at 36% 32%, rgba(255, 229, 149, 0.42) 0 15rpx, transparent 16rpx),
    radial-gradient(circle at 28% 72%, rgba(255, 236, 166, 0.28) 0 11rpx, transparent 12rpx),
    repeating-linear-gradient(164deg, rgba(255, 242, 192, 0.2) 0 18rpx, transparent 19rpx 38rpx),
    linear-gradient(145deg, #f4b156 0%, #d88933 52%, #9b5424 100%);
}

.dare-public .planet-surface::after {
  background:
    radial-gradient(circle at 64% 28%, rgba(115, 54, 25, 0.2) 0 12rpx, transparent 13rpx),
    radial-gradient(circle at 42% 58%, rgba(255, 255, 255, 0.18) 0 8rpx, transparent 9rpx);
}

.dare-private {
  bottom: 468rpx;
  left: 54rpx;
  animation: planet-float-d 5s ease-in-out infinite;
}

.dare-private .planet-ring {
  opacity: 1;
  width: 210rpx;
  height: 54rpx;
  border-color: rgba(122, 205, 198, 0.42);
  border-left-color: rgba(122, 205, 198, 0.12);
  border-bottom-color: rgba(122, 205, 198, 0.18);
  transform: rotate(18deg);
}

.dare-private .planet-surface {
  background:
    radial-gradient(circle at 36% 34%, rgba(83, 178, 171, 0.5) 0 12rpx, transparent 13rpx),
    radial-gradient(circle at 68% 68%, rgba(8, 35, 42, 0.42) 0 22rpx, transparent 23rpx),
    linear-gradient(138deg, rgba(128, 229, 210, 0.18) 0 15%, transparent 16% 30%, rgba(96, 188, 184, 0.16) 31% 45%, transparent 46%),
    linear-gradient(145deg, #2a6f73 0%, #12383d 56%, #09252b 100%);
}

.dare-private .planet-surface::after {
  background:
    repeating-linear-gradient(150deg, transparent 0 18rpx, rgba(116, 221, 203, 0.13) 19rpx 28rpx),
    radial-gradient(circle at 24% 68%, rgba(255, 255, 255, 0.18) 0 8rpx, transparent 9rpx);
}

.dice-entry {
  z-index: 2;
  width: 164rpx;
  height: 164rpx;
  color: #fff;
  animation: dice-float 4.2s ease-in-out infinite;
}

.dice-entry .planet-ring {
  opacity: 1;
  width: 256rpx;
  height: 70rpx;
  border-color: rgba(255, 255, 255, 0.6);
  border-left-color: rgba(255, 255, 255, 0.16);
  border-bottom-color: rgba(255, 255, 255, 0.22);
  transform: rotate(-22deg);
}

.dice-entry .planet-surface {
  background:
    radial-gradient(circle at 74% 26%, rgba(255, 255, 255, 0.52) 0 16rpx, transparent 17rpx),
    radial-gradient(circle at 30% 72%, rgba(102, 205, 196, 0.22) 0 28rpx, transparent 29rpx),
    repeating-linear-gradient(25deg, rgba(255, 255, 255, 0.13) 0 16rpx, transparent 17rpx 38rpx),
    linear-gradient(145deg, #6266c8 0%, #2d6c73 58%, #102f35 100%);
  box-shadow:
    0 30rpx 68rpx rgba(4, 10, 20, 0.32),
    0 0 0 12rpx rgba(255, 255, 255, 0.18),
    inset -18rpx -24rpx 34rpx rgba(4, 10, 20, 0.22),
    inset 18rpx 18rpx 28rpx rgba(255, 255, 255, 0.22);
}

.dice-entry .planet-surface::after {
  background:
    repeating-linear-gradient(24deg, rgba(35, 108, 114, 0.05) 0 16rpx, transparent 17rpx 38rpx);
}

.activity-system.rolling .dice-entry .planet-surface {
  animation: dice-roll 520ms ease-out;
}

.modal-mask {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28rpx;
  box-sizing: border-box;
  background: rgba(0, 0, 0, 0.44);
  backdrop-filter: blur(12px);
}

.modal-card {
  width: 100%;
  max-width: 520px;
  border-radius: 30px;
  padding: 30rpx;
  background: rgba(255, 255, 255, 0.96);
  color: #1d1d1f;
  box-sizing: border-box;
  box-shadow: 0 34rpx 80rpx rgba(0, 0, 0, 0.28);
}

.modal-kicker {
  display: block;
  color: #6e6e73;
  font-size: 24rpx;
  font-weight: 900;
}

.textarea-shell {
  position: relative;
  margin-top: 18rpx;
}

.game-textarea {
  width: 100%;
  min-height: 260rpx;
  border: 1px solid rgba(29, 29, 31, 0.08);
  border-radius: 20px;
  background: #f5f5f7;
  padding: 24rpx 24rpx 82rpx;
  color: #1d1d1f;
  box-sizing: border-box;
  font-size: 28rpx;
}

.random-tip-button {
  position: absolute;
  right: 18rpx;
  bottom: 24rpx;
  min-width: 104rpx;
  border: 1px solid rgba(0, 113, 227, 0.14);
  border-radius: 999px;
  padding: 12rpx 20rpx;
  color: #0b6fcf;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 10rpx 24rpx rgba(0, 113, 227, 0.12);
  font-size: 24rpx;
  font-weight: 900;
  line-height: 1;
  text-align: center;
}

.game-error {
  display: block;
  margin-top: 12rpx;
  color: #d64f4f;
  font-size: 24rpx;
  font-weight: 800;
}

.option-block {
  margin-top: 20rpx;
}

.field-label {
  display: block;
  margin-bottom: 12rpx;
  color: #6e6e73;
  font-size: 24rpx;
  font-weight: 900;
}

.meaning-card {
  border-radius: 18px;
  padding: 18rpx;
  color: #3a3a3c;
  background: #f5f5f7;
  font-size: 25rpx;
  line-height: 1.45;
}

.choice-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.choice-chip {
  min-width: 130rpx;
  border: 1px solid rgba(29, 29, 31, 0.09);
  border-radius: 999px;
  padding: 14rpx 22rpx;
  color: #1d1d1f;
  background: #f5f5f7;
  font-size: 25rpx;
  font-weight: 900;
  text-align: center;
  box-sizing: border-box;
}

.choice-chip.active {
  border-color: rgba(0, 113, 227, 0.22);
  color: #fff;
  background: #0071e3;
  box-shadow: 0 10rpx 24rpx rgba(0, 113, 227, 0.18);
}

.choice-chip.female.active {
  border-color: rgba(219, 39, 119, 0.2);
  background: #db2777;
  box-shadow: 0 10rpx 24rpx rgba(219, 39, 119, 0.18);
}

.choice-chip.male.active {
  border-color: rgba(37, 99, 235, 0.22);
  background: #2563eb;
  box-shadow: 0 10rpx 24rpx rgba(37, 99, 235, 0.18);
}

.modal-actions {
  display: grid;
  grid-template-columns: 0.8fr 1.2fr;
  gap: 16rpx;
  margin-top: 26rpx;
}

.room-concept-card {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.96)),
    radial-gradient(circle at 94% 0%, rgba(37, 99, 235, 0.08), transparent 32%);
}

.room-concept-title,
.room-concept-body {
  display: block;
}

.room-concept-title {
  margin-top: 12rpx;
  color: #172126;
  font-size: 38rpx;
  font-weight: 900;
  line-height: 1.18;
}

.room-concept-body {
  margin-top: 14rpx;
  color: #475569;
  font-size: 26rpx;
  line-height: 1.5;
}

.room-concept-flow {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10rpx;
  margin-top: 22rpx;
}

.room-concept-flow text {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 66rpx;
  border: 1px solid rgba(37, 99, 235, 0.1);
  border-radius: 14px;
  color: #2563eb;
  background: rgba(37, 99, 235, 0.07);
  font-size: 23rpx;
  font-weight: 900;
}

.result-card {
  position: absolute;
  left: 24rpx;
  right: 24rpx;
  bottom: 28rpx;
  z-index: 5;
  border-radius: 8px;
  padding: 34rpx;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: linear-gradient(135deg, rgba(18, 56, 61, 0.92), rgba(35, 108, 114, 0.86));
  box-shadow: 0 22rpx 48rpx rgba(0, 0, 0, 0.16);
}

.result-kicker,
.result-text {
  display: block;
  color: #fff;
}

.result-kicker {
  opacity: 0.72;
  font-size: 24rpx;
}

.result-text {
  margin-top: 18rpx;
  font-size: 36rpx;
  font-weight: 900;
  line-height: 1.42;
}

.result-meta {
  display: grid;
  gap: 8rpx;
  margin-top: 20rpx;
  color: rgba(255, 255, 255, 0.78);
  font-size: 24rpx;
  line-height: 1.45;
}

.result-actions {
  margin-top: 28rpx;
}

@keyframes dice-float {
  0%,
  100% {
    transform: translateY(-4rpx);
  }
  50% {
    transform: translateY(10rpx);
  }
}

@keyframes dice-roll {
  0% {
    transform: rotate(0deg) scale(1);
  }
  55% {
    transform: rotate(18deg) scale(1.08);
  }
  100% {
    transform: rotate(0deg) scale(1);
  }
}

@keyframes star-twinkle {
  0%,
  100% {
    opacity: 0.42;
  }
  50% {
    opacity: 0.86;
  }
}

@keyframes meteor-flight {
  0% {
    opacity: 0;
    transform: translate(120rpx, -42rpx) rotate(var(--meteor-angle));
  }
  12% {
    opacity: 0.92;
  }
  58% {
    opacity: 0.66;
  }
  76% {
    opacity: 0.22;
  }
  100% {
    opacity: 0;
    transform: translate(-620rpx, 210rpx) rotate(var(--meteor-angle));
  }
}

@keyframes corner-meteor-flight {
  0% {
    opacity: 0;
    transform: translate(150rpx, -48rpx) rotate(var(--meteor-angle));
  }
  16% {
    opacity: 0.78;
  }
  58% {
    opacity: 0.52;
  }
  100% {
    opacity: 0;
    transform: translate(-260rpx, 98rpx) rotate(var(--meteor-angle));
  }
}

@keyframes corner-comet-pulse {
  0%,
  100% {
    opacity: 0.36;
  }
  50% {
    opacity: 0.72;
  }
}

@keyframes ship-drift {
  0%,
  100% {
    transform: translate(0, 0) rotate(var(--ship-rotate)) scale(var(--ship-scale));
  }
  50% {
    transform: translate(18rpx, -12rpx) rotate(var(--ship-rotate)) scale(var(--ship-scale));
  }
}

@keyframes trail-pulse {
  0%,
  100% {
    opacity: 0.44;
    transform: scaleX(0.9);
  }
  50% {
    opacity: 0.9;
    transform: scaleX(1.08);
  }
}

@keyframes planet-float-a {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(12rpx, 18rpx);
  }
}

@keyframes planet-float-b {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(-16rpx, 14rpx);
  }
}

@keyframes planet-float-c {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(-14rpx, -18rpx);
  }
}

@keyframes planet-float-d {
  0%,
  100% {
    transform: translate(0, 0);
  }
  50% {
    transform: translate(16rpx, -12rpx);
  }
}
</style>
