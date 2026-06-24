import { defaultBaseQuotas, defaultVipBonus, quotaLabels, quotaOrder, weeklyCheckinRewards } from '@/constants/product'
import type {
  AdRewardState,
  AdminSummary,
  AdminAdRewardRecord,
  AdminAuditLogItem,
  AdminChatReviewItem,
  AdminContentReviewItem,
  AdminOrderRecord,
  AdminReportItem,
  AdminSession,
  AdminUserSummary,
  AdminWalletRiskItem,
  BlacklistItem,
  Bottle,
  CheckinState,
  CoinLedgerItem,
  ConversationThread,
  CreatorProfile,
  DareTask,
  GiftProduct,
  MeStatus,
  MessageItem,
  NearbyUser,
  PlazaPost,
  PrivatePhoto,
  QuotaItem,
  QuotaType,
  ReferralState,
  TreeholePost,
  TruthQuestion,
  UserProfile,
  VerificationState,
  WalletState
} from '@/types/domain'
import { nowIso } from '@/utils/time'

const user: UserProfile = {
  id: 'user_mock_001',
  nickname: '海风来信',
  avatarText: '海',
  avatarUrl: 'https://i.pravatar.cc/120?img=47',
  platform: 'wechat',
  isVip: true,
  vipLevel: 'monthly',
  driftCoins: 260,
  gender: 'female',
  ageRange: '25-30',
  city: '杭州',
  faceVerified: true,
  genderVerified: true,
  charmValue: 1880
}

const quotas: Record<QuotaType, QuotaItem> = quotaOrder.reduce((acc, type) => {
  const vipBonus = user.isVip ? defaultVipBonus[type] : 0
  acc[type] = {
    type,
    label: quotaLabels[type],
    base: defaultBaseQuotas[type],
    vipBonus,
    adBonus: 0,
    used: 0,
    remaining: defaultBaseQuotas[type] + vipBonus
  }
  return acc
}, {} as Record<QuotaType, QuotaItem>)

const adReward: AdRewardState = {
  canWatch: true,
  cooldownSeconds: 0,
  cooldownMinutes: 30,
  rewardPerQuota: 1
}

const checkin: CheckinState = {
  checkedToday: false,
  streakDays: 2,
  weekRewards: weeklyCheckinRewards,
  currentWeekIndex: 2
}

const verification: VerificationState = {
  faceVerified: true,
  genderVerified: true,
  detectedGender: 'female',
  livenessPassed: true,
  manualReviewStatus: 'approved'
}

const referral: ReferralState = {
  inviteCode: 'SEA260',
  invitedCount: 3,
  rewardVipDays: 7,
  nextRewardNeed: 5
}

const adminSession: AdminSession = {
  accountId: 'admin_demo',
  displayName: '内容运营管理员',
  role: 'super_admin',
  permissions: ['content:review', 'content:offline', 'report:handle', 'wallet:review', 'config:save'],
  signedIn: true,
  lastLoginAt: '2026-06-23 10:30'
}

const bottles: Bottle[] = [
  {
    id: 'bottle_001',
    authorId: 'creator_001',
    authorName: '海岛来信',
    authorAvatarText: '海',
    authorVip: true,
    authorGender: 'female',
    authorAgeRange: '25-30',
    authorCity: '上海',
    authorVerified: true,
    content: '今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。',
    mood: '平静',
    status: 'approved',
    replies: 5,
    targetGender: 'all',
    targetScope: 'all',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_002',
    authorId: 'creator_002',
    authorName: '晚风',
    authorAvatarText: '晚',
    authorVip: false,
    authorGender: 'female',
    authorAgeRange: '18-24',
    authorCity: '杭州',
    authorVerified: true,
    content: '如果你正在犹豫要不要重新开始，我想把勇气分你一点。',
    mood: '鼓励',
    status: 'approved',
    replies: 2,
    targetGender: 'all',
    targetScope: 'all',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_003',
    authorId: 'creator_003',
    authorName: '北岸',
    authorAvatarText: '北',
    authorVip: false,
    authorGender: 'male',
    authorAgeRange: '25-30',
    authorCity: '杭州',
    authorVerified: true,
    content: '刚下班路过江边，突然觉得今天也不是完全糟糕，至少风很舒服。',
    mood: '放松',
    status: 'approved',
    replies: 1,
    targetGender: 'all',
    targetScope: 'same_city',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_004',
    authorId: 'creator_004',
    authorName: '小满',
    authorAvatarText: '满',
    authorVip: true,
    authorGender: 'female',
    authorAgeRange: '22-26',
    authorCity: '成都',
    authorVerified: true,
    content: '希望捞到这个瓶子的人，今天可以少一点内耗，多一点被认真对待的感觉。',
    mood: '温柔',
    status: 'approved',
    replies: 8,
    targetGender: 'all',
    targetScope: 'all',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_005',
    authorId: 'creator_005',
    authorName: '凌晨三点',
    authorAvatarText: '凌',
    authorVip: false,
    authorGender: 'male',
    authorAgeRange: '30-35',
    authorCity: '深圳',
    authorVerified: false,
    content: '有时候不是想聊天，只是想知道世界上还有人也醒着。',
    mood: '深夜',
    status: 'approved',
    replies: 3,
    targetGender: 'all',
    targetScope: 'all',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_006',
    authorId: 'creator_006',
    authorName: '蓝莓气泡',
    authorAvatarText: '蓝',
    authorVip: true,
    authorGender: 'female',
    authorAgeRange: '18-24',
    authorCity: '广州',
    authorVerified: true,
    content: '今天被一句很小的话治愈了，也想把这份轻松传给你。',
    mood: '开心',
    status: 'approved',
    replies: 12,
    targetGender: 'all',
    targetScope: 'same_city',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_007',
    authorId: 'creator_007',
    authorName: '山月',
    authorAvatarText: '山',
    authorVip: false,
    authorGender: 'female',
    authorAgeRange: '27-32',
    authorCity: '北京',
    authorVerified: true,
    content: '如果你也正在重新整理生活，我们可以各自安静努力，然后在海上碰一下杯。',
    mood: '自洽',
    status: 'approved',
    replies: 6,
    targetGender: 'all',
    targetScope: 'all',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  },
  {
    id: 'bottle_008',
    authorId: 'creator_008',
    authorName: '南窗',
    authorAvatarText: '南',
    authorVip: false,
    authorGender: 'unknown',
    authorAgeRange: '未知',
    authorCity: '厦门',
    authorVerified: false,
    content: '把一个没法说出口的问题丢进海里，希望明天醒来能轻一点。',
    mood: '树洞',
    status: 'approved',
    replies: 0,
    targetGender: 'all',
    targetScope: 'all',
    isFollowing: false,
    friendRequested: false,
    createdAt: nowIso()
  }
]

const treeholes: TreeholePost[] = [
  {
    id: 'tree_001',
    authorId: 'creator_001',
    authorName: '海岛来信',
    authorAvatarText: '海',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=5',
    authorGender: 'female',
    authorAgeRange: '25-30',
    content: '有些话不想让熟人看见，但憋在心里又太重了。',
    resonanceCount: 42,
    replyCount: 8,
    paidPhotoCount: 2,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_002',
    authorId: 'creator_002',
    authorName: '晚风',
    authorAvatarText: '晚',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=32',
    authorGender: 'female',
    authorAgeRange: '18-24',
    content: '今天终于拒绝了一件让我不舒服的事，虽然手还在抖。',
    resonanceCount: 31,
    replyCount: 4,
    paidPhotoCount: 1,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_003',
    authorId: 'creator_003',
    authorName: '北岸',
    authorAvatarText: '北',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=12',
    authorGender: 'male',
    authorAgeRange: '25-30',
    content: '在便利店门口坐了十分钟，忽然觉得慢一点也没有关系。',
    resonanceCount: 19,
    replyCount: 3,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_004',
    authorId: 'creator_004',
    authorName: '小满',
    authorAvatarText: '满',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=44',
    authorGender: 'female',
    authorAgeRange: '22-26',
    content: '今晚没有很开心，但洗完澡吹干头发以后，好像又能继续了。',
    resonanceCount: 27,
    replyCount: 5,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_005',
    authorId: 'creator_005',
    authorName: '凌晨三点',
    authorAvatarText: '凌',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=56',
    authorGender: 'male',
    authorAgeRange: '30-35',
    content: '有些消息没有等到回复，其实心里已经知道答案了。',
    resonanceCount: 16,
    replyCount: 2,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_006',
    authorId: 'creator_006',
    authorName: '蓝莓气泡',
    authorAvatarText: '蓝',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=49',
    authorGender: 'female',
    authorAgeRange: '18-24',
    content: '今天收到一句很轻的夸奖，像有人把窗户推开了一点。',
    resonanceCount: 34,
    replyCount: 7,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_007',
    authorId: 'creator_007',
    authorName: '山月',
    authorAvatarText: '山',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=23',
    authorGender: 'female',
    authorAgeRange: '27-32',
    content: '我正在学着不把所有人的情绪都揽到自己身上。',
    resonanceCount: 23,
    replyCount: 4,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_008',
    authorId: 'creator_008',
    authorName: '南窗',
    authorAvatarText: '南',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=68',
    authorGender: 'unknown',
    authorAgeRange: '未知',
    content: '把烦恼写下来以后，忽然发现它没有想象中那么大。',
    resonanceCount: 18,
    replyCount: 2,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_009',
    authorId: 'creator_009',
    authorName: '江边路灯',
    authorAvatarText: '江',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=14',
    authorGender: 'male',
    authorAgeRange: '25-30',
    content: '下班路上没有听歌，只想听风吹过桥洞的声音。',
    resonanceCount: 21,
    replyCount: 3,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_010',
    authorId: 'creator_010',
    authorName: '橘子海',
    authorAvatarText: '橘',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=41',
    authorGender: 'female',
    authorAgeRange: '20-25',
    content: '今天没有发生什么大事，但晚霞很好看，我也算被照顾了一下。',
    resonanceCount: 39,
    replyCount: 6,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_011',
    authorId: 'creator_011',
    authorName: '灰色耳机',
    authorAvatarText: '灰',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=60',
    authorGender: 'male',
    authorAgeRange: '28-34',
    content: '有些话不适合发朋友圈，但适合放在这里慢慢沉下去。',
    resonanceCount: 14,
    replyCount: 1,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  },
  {
    id: 'tree_012',
    authorId: 'creator_012',
    authorName: '雨后邮差',
    authorAvatarText: '雨',
    authorAvatarUrl: 'https://i.pravatar.cc/120?img=70',
    authorGender: 'unknown',
    authorAgeRange: '未知',
    content: '希望明天醒来的时候，心里的那块石头能轻一点。',
    resonanceCount: 26,
    replyCount: 5,
    paidPhotoCount: 0,
    status: 'approved',
    createdAt: nowIso()
  }
]

const bottlePromptTemplates = [
  '今天有什么小事让你觉得还不错？',
  '如果今晚可以不用考虑明天，你最想做什么？',
  '推荐我一个你最近喜欢的歌、电影或小店吧。',
  '你最近有没有一个瞬间，突然觉得自己被生活温柔了一下？',
  '如果把今天的心情取一个天气名字，你会叫它什么？',
  '我这里有一点海风，想换你一句今天的故事。',
  '你会因为什么样的小细节，对一个陌生人多一点好感？',
  '最近有没有一个让你忍不住笑出来的瞬间？',
  '如果现在能收到一份小礼物，你希望它是什么？',
  '你喜欢慢慢熟悉的人，还是一开始就很有默契的人？',
  '今天辛苦了，愿意把最想被理解的一句话丢进这个瓶子吗？',
  '如果今晚有人认真听你说话，你最想先说哪一句？',
  '你心里有没有一个想去很久、但还没出发的地方？',
  '你觉得一个舒服的聊天，最重要的是什么？',
  '如果把烦恼折成纸船，你想让它漂去哪里？',
  '最近让你觉得有点期待的事情是什么？',
  '你喜欢被怎样温柔地关心？',
  '如果可以给陌生人留一句好运，你会写什么？'
]

const plazaPosts: PlazaPost[] = [
  {
    id: 'plaza_001',
    authorId: 'creator_001',
    authorName: '海岛来信',
    iconText: '证',
    topic: '今日心情',
    content: '今晚想收一只认真写的动态，也想把好运分给路过的人。',
    mediaType: 'image',
    mediaCount: 3,
    gender: 'female',
    verified: true,
    city: '上海',
    ageRange: '25-30',
    viewCount: 1680,
    likeCount: 328,
    commentCount: 42,
    commentPreview: '这条动态很舒服。',
    distanceText: '同城',
    createdAt: nowIso()
  },
    {
      id: 'plaza_002',
      authorId: 'creator_003',
      authorName: '北岸',
    iconText: '近',
    topic: '附近动态',
    content: '附近 2km 有人分享了今天的晚风和一家新开的甜品店。',
    mediaType: 'voice',
    mediaCount: 1,
    gender: 'male',
    verified: true,
    city: '杭州',
    ageRange: '25-30',
    viewCount: 520,
    likeCount: 89,
    commentCount: 17,
      commentPreview: '甜品店在哪一条街？',
      distanceText: '2.1km',
      createdAt: nowIso()
    },
    {
      id: 'plaza_003',
      authorId: 'creator_006',
      authorName: '蓝莓气泡',
      iconText: '蓝',
      topic: '新人推荐',
      content: '拍了一段傍晚路灯亮起来的视频，感觉今天也有一点值得被记住。',
      mediaType: 'video',
      mediaCount: 1,
      gender: 'female',
      verified: true,
      city: '广州',
      ageRange: '18-24',
      viewCount: 260,
      likeCount: 146,
      commentCount: 9,
      commentPreview: '这个傍晚很有氛围。',
      distanceText: '新人',
      createdAt: nowIso()
    }
  ]

const nearbyUsers: NearbyUser[] = [
  {
    id: 'near_001',
    nickname: '海岛来信',
    iconText: '证',
    gender: 'female',
    verified: true,
    ageRange: '25-30',
    distanceKm: 1.2,
    distanceText: '1.2km',
    signature: '只接受礼貌的关注和好友申请。',
    isVip: true,
    online: true
  },
  {
    id: 'near_002',
    nickname: '北岸',
    iconText: '近',
    gender: 'male',
    verified: true,
    ageRange: '25-30',
    distanceKm: 2.8,
    distanceText: '2.8km',
    signature: '喜欢听故事，也认真回瓶子。',
    isVip: false,
    online: false
  }
]

const truthQuestions: TruthQuestion[] = [
  { id: 'truth_001', category: '情感', text: '你最近一次真正心动，是因为什么细节？' },
  { id: 'truth_002', category: '朋友局', text: '你最希望朋友理解你哪一点？' },
  { id: 'truth_003', category: '深夜', text: '有没有一句话，你一直没机会说出口？' }
]

const dareTasks: DareTask[] = [
  { id: 'dare_001', category: '轻松', text: '给今天的自己写一句夸奖，并保存下来。' },
  { id: 'dare_002', category: '社交', text: '向一个很久没联系的人发一句问候。' },
  { id: 'dare_003', category: '文字挑战', text: '用 30 个字描述此刻窗外的世界。' }
]

const messages: MessageItem[] = [
  {
    id: 'msg_001',
    title: '瓶子有新回应',
    body: '有人回应了你的漂流瓶：我也有过类似的夜晚。',
    createdAt: nowIso(),
    unread: true
  },
  {
    id: 'msg_002',
    title: '拉新奖励到账',
    body: '你邀请的新用户完成注册，获得 7 天会员体验。',
    createdAt: nowIso(),
    unread: false
  }
]

const conversationThreads: ConversationThread[] = [
  {
    id: 'thread_bottle_001',
    bottleId: 'bottle_001',
    participantName: '匿名海岛客',
    participantTag: '漂流瓶回应',
    bottlePreview: '今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。',
    lastMessage: '我也有过类似的夜晚，看到这句的时候刚好安静下来。',
    updatedAt: nowIso(),
    unreadCount: 1,
    turns: [
      {
        id: 'turn_001',
        senderName: '匿名海岛客',
        body: '今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。',
        createdAt: nowIso(),
        fromMe: false
      },
      {
        id: 'turn_002',
        senderName: '海风来信',
        body: '我收到了。今晚确实需要一点安静，谢谢你。',
        createdAt: nowIso(),
        fromMe: true
      },
      {
        id: 'turn_003',
        senderName: '匿名海岛客',
        body: '我也有过类似的夜晚，看到这句的时候刚好安静下来。',
        createdAt: nowIso(),
        fromMe: false
      }
    ]
  },
  {
    id: 'thread_bottle_002',
    bottleId: 'bottle_002',
    participantName: '晚风',
    participantTag: '好友申请中',
    bottlePreview: '如果你正在犹豫要不要重新开始，我想把勇气分你一点。',
    lastMessage: '那我先把今天整理好，明天再往前走一步。',
    updatedAt: nowIso(),
    unreadCount: 0,
    turns: [
      {
        id: 'turn_004',
        senderName: '晚风',
        body: '如果你正在犹豫要不要重新开始，我想把勇气分你一点。',
        createdAt: nowIso(),
        fromMe: false
      },
      {
        id: 'turn_005',
        senderName: '海风来信',
        body: '那我先把今天整理好，明天再往前走一步。',
        createdAt: nowIso(),
        fromMe: true
      }
    ]
  }
]

const wallet: WalletState = {
  rechargeCoins: 520,
  earnedCoins: 180,
  giftCoins: 68,
  withdrawableCoins: 180,
  frozenCoins: 20,
  charmValue: 1880,
  withdrawThresholdCharm: 1000,
  charmExchangeRate: 100
}

const ledger: CoinLedgerItem[] = [
  {
    id: 'ledger_001',
    title: '私密照片被查看，转入魅力值',
    amount: 30,
    coinBucket: 'earned',
    withdrawable: true,
    createdAt: nowIso()
  },
  {
    id: 'ledger_002',
    title: '充值金币',
    amount: 200,
    coinBucket: 'recharge',
    withdrawable: false,
    createdAt: nowIso()
  }
]

const creators: CreatorProfile[] = [
  {
    userId: 'creator_001',
    displayName: '海岛来信',
    gender: 'female',
    verified: true,
    safetyScore: 96,
    followerCount: 1280,
    albumCount: 3,
    earnedCoins: 360,
    charmValue: 3600
  },
  {
    userId: 'creator_002',
    displayName: '晚风',
    gender: 'female',
    verified: true,
    safetyScore: 91,
    followerCount: 840,
    albumCount: 2,
    earnedCoins: 180,
    charmValue: 1800
  }
]

const privatePhotos: PrivatePhoto[] = [
  {
    id: 'photo_001',
    ownerId: 'creator_001',
    ownerName: '海岛来信',
    title: '今日海边碎片',
    coverTone: '#dbeeed',
    priceCoins: 30,
    blurred: true,
    status: 'approved',
    purchased: false
  },
  {
    id: 'photo_002',
    ownerId: 'creator_002',
    ownerName: '晚风',
    title: '只给认真回应的人看',
    coverTone: '#f6dfb6',
    priceCoins: 20,
    blurred: true,
    status: 'approved',
    purchased: false
  }
]

const gifts: GiftProduct[] = [
  { id: 'gift_shell', name: '贝壳', priceCoins: 10, iconText: '贝' },
  { id: 'gift_star', name: '星光', priceCoins: 30, iconText: '星' },
  { id: 'gift_bottle', name: '玻璃瓶', priceCoins: 68, iconText: '瓶' }
]

const blacklist: BlacklistItem[] = [
  {
    id: 'block_001',
    userId: 'bad_user_001',
    nickname: '无礼访客',
    reason: '骚扰私信',
    blockedAt: nowIso()
  }
]

const adminUsers: AdminUserSummary[] = [
  {
    id: 'user_mock_001',
    nickname: '海风来信',
    platform: 'wechat',
    gender: 'female',
    isVip: true,
    verificationStatus: 'approved',
    safetyScore: 98,
    walletRisk: 'normal',
    driftCoins: 260,
    charmValue: 1880,
    joinedAt: '2026-05-18 09:20',
    lastActiveAt: '2026-06-23 10:42'
  },
  {
    id: 'creator_001',
    nickname: '海岛来信',
    platform: 'ios',
    gender: 'female',
    isVip: true,
    verificationStatus: 'approved',
    safetyScore: 96,
    walletRisk: 'watch',
    driftCoins: 420,
    charmValue: 3600,
    joinedAt: '2026-04-09 18:05',
    lastActiveAt: '2026-06-23 09:13'
  },
  {
    id: 'creator_002',
    nickname: '晚风',
    platform: 'android',
    gender: 'female',
    isVip: false,
    verificationStatus: 'pending',
    safetyScore: 91,
    walletRisk: 'normal',
    driftCoins: 128,
    charmValue: 1800,
    joinedAt: '2026-05-02 21:46',
    lastActiveAt: '2026-06-22 23:18'
  },
  {
    id: 'bad_user_001',
    nickname: '无礼访客',
    platform: 'h5',
    gender: 'unknown',
    isVip: false,
    verificationStatus: 'rejected',
    safetyScore: 42,
    walletRisk: 'blocked',
    driftCoins: 16,
    charmValue: 120,
    joinedAt: '2026-06-20 13:34',
    lastActiveAt: '2026-06-23 08:02'
  }
]

const contentReviews: AdminContentReviewItem[] = [
  {
    id: 'review_bottle_001',
    type: 'bottle',
    category: '漂流瓶',
    authorId: 'creator_002',
    authorName: '晚风',
    preview: '如果你正在犹豫要不要重新开始，我想把勇气分你一点。',
    status: 'approved',
    riskLevel: 'low',
    reviewTrigger: 'new_user',
    handlingPolicy: '正常内容自动通过；低风险新用户内容只做抽样留痕。',
    autoAction: 'auto_pass',
    reason: '低风险新用户首条漂流瓶，系统自动通过并抽样记录',
    createdAt: '2026-06-23 09:55'
  },
  {
    id: 'review_tree_001',
    type: 'treehole',
    category: '树洞',
    authorId: 'creator_001',
    authorName: '海岛来信',
    preview: '有些话不想让熟人看见，但憋在心里又太重了。',
    status: 'pending',
    riskLevel: 'medium',
    reviewTrigger: 'risk',
    handlingPolicy: '命中情绪风险，进入人工复核；正常情绪表达不处罚。',
    autoAction: 'manual_review',
    reason: '情绪内容需要人工复核',
    createdAt: '2026-06-23 08:48'
  },
  {
    id: 'review_photo_001',
    type: 'private_photo',
    category: '私密照片',
    authorId: 'creator_001',
    authorName: '海岛来信',
    preview: '今日海边碎片',
    status: 'approved',
    riskLevel: 'low',
    reviewTrigger: 'private_photo',
    handlingPolicy: '私密照片必须先审后展；审核通过后可展示。',
    autoAction: 'manual_review',
    reason: '私密照片封面已通过',
    createdAt: '2026-06-22 19:22'
  },
  {
    id: 'review_plaza_001',
    type: 'plaza',
    category: '广场',
    authorId: 'bad_user_001',
    authorName: '无礼访客',
    preview: '站外联系方式和诱导充值文案',
    status: 'rejected',
    riskLevel: 'high',
    reviewTrigger: 'keyword',
    handlingPolicy: '命中导流/诱导交易词，自动屏蔽并进入审核；高风险可直接拒绝。',
    matchedKeywords: ['站外联系方式', '诱导充值'],
    autoAction: 'reject',
    reason: '疑似导流',
    createdAt: '2026-06-22 16:31'
  }
]

const chatReviews: AdminChatReviewItem[] = [
  {
    id: 'chat_review_001',
    threadId: 'thread_bottle_001',
    source: 'bottle',
    reporterName: '海风来信',
    participantUserIds: ['user_mock_001', 'creator_001'],
    participants: ['海风来信', '匿名海岛客'],
    relatedContent: '漂流瓶：今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。',
    lastMessage: '我也有过类似的夜晚，看到这句的时候刚好安静下来。',
    riskLevel: 'low',
    status: 'reviewing',
    reviewTrigger: 'report',
    handlingPolicy: '仅因举报进入上下文复核；未命中违规词时不处罚。',
    autoAction: 'manual_review',
    reason: '用户举报后进入聊天上下文复核',
    messages: conversationThreads[0]?.turns.map((turn) => ({ ...turn })) ?? [],
    updatedAt: '2026-06-23 10:31'
  },
  {
    id: 'chat_review_002',
    threadId: 'thread_bottle_002',
    source: 'bottle',
    reporterName: '晚风',
    participantUserIds: ['user_mock_001', 'creator_002'],
    participants: ['海风来信', '晚风'],
    relatedContent: '漂流瓶：如果你正在犹豫要不要重新开始，我想把勇气分你一点。',
    lastMessage: '那我先把今天整理好，明天再往前走一步。',
    riskLevel: 'medium',
    status: 'pending',
    reviewTrigger: 'risk',
    handlingPolicy: '好友申请前对话只做安全复核，正常交流不处理。',
    autoAction: 'manual_review',
    reason: '好友申请前对话需要确认是否存在骚扰或诱导',
    messages: conversationThreads[1]?.turns.map((turn) => ({ ...turn })) ?? [],
    updatedAt: '2026-06-23 09:48'
  },
  {
    id: 'chat_review_003',
    threadId: 'manual_treehole_001',
    source: 'treehole',
    reporterName: '海岛来信',
    participantUserIds: ['creator_001', 'bad_user_001'],
    participants: ['海岛来信', '无礼访客'],
    relatedContent: '树洞：有些话不想让熟人看见，但憋在心里又太重了。',
    lastMessage: '加我私下聊，我告诉你怎么快速赚金币。',
    riskLevel: 'high',
    status: 'pending',
    reviewTrigger: 'keyword',
    handlingPolicy: '命中导流/诱导交易词，发送侧自动屏蔽，后台保留原始命中证据。',
    matchedKeywords: ['加我私下聊', '快速赚金币'],
    autoAction: 'mask_and_review',
    reason: '命中站外导流和诱导交易关键词',
    messages: [
      {
        id: 'chat_turn_001',
        senderName: '海岛来信',
        body: '这条树洞只想找人听听，不想被打扰。',
        createdAt: '2026-06-23 08:49',
        fromMe: false
      },
      {
        id: 'chat_turn_002',
        senderName: '无礼访客',
        body: '加我私下聊，我告诉你怎么快速赚金币。',
        createdAt: '2026-06-23 08:52',
        fromMe: false
      }
    ],
    updatedAt: '2026-06-23 08:54'
  }
]

const adminReports: AdminReportItem[] = [
  {
    id: 'report_001',
    reporterName: '海风来信',
    targetType: 'treehole',
    targetId: 'tree_002',
    targetPreview: '今天终于拒绝了一件让我不舒服的事。',
    reason: '疑似骚扰回复',
    status: 'pending',
    priority: 'high',
    createdAt: '2026-06-23 10:20'
  },
  {
    id: 'report_002',
    reporterName: '晚风',
    targetType: 'bottle',
    targetId: 'bottle_001',
    targetPreview: '今天把想说的话写进瓶子里。',
    reason: '低俗内容复核',
    status: 'reviewing',
    priority: 'normal',
    createdAt: '2026-06-23 09:40'
  },
  {
    id: 'report_003',
    reporterName: '海岛来信',
    targetType: 'user',
    targetId: 'bad_user_001',
    targetPreview: '无礼访客',
    reason: '私信骚扰',
    status: 'resolved',
    priority: 'high',
    createdAt: '2026-06-22 22:18'
  }
]

const adRewardRecords: AdminAdRewardRecord[] = [
  {
    id: 'ad_reward_001',
    userId: 'user_mock_001',
    nickname: '海风来信',
    sessionId: 'ad_202606231010',
    rewardPerQuota: 1,
    quotaTypes: [...quotaOrder],
    status: 'settled',
    createdAt: '2026-06-23 10:10'
  },
  {
    id: 'ad_reward_002',
    userId: 'creator_002',
    nickname: '晚风',
    sessionId: 'ad_202606230934',
    rewardPerQuota: 1,
    quotaTypes: ['fish_bottle', 'throw_bottle'],
    status: 'cooldown',
    createdAt: '2026-06-23 09:34'
  },
  {
    id: 'ad_reward_003',
    userId: 'bad_user_001',
    nickname: '无礼访客',
    sessionId: 'ad_202606222151',
    rewardPerQuota: 0,
    quotaTypes: [],
    status: 'blocked',
    createdAt: '2026-06-22 21:51'
  }
]

const orderRecords: AdminOrderRecord[] = [
  {
    id: 'order_20260623001',
    userId: 'user_mock_001',
    nickname: '海风来信',
    productName: '200 金币包',
    amountCoins: 200,
    payAmount: 18,
    channel: 'wechat',
    status: 'paid',
    createdAt: '2026-06-23 10:04'
  },
  {
    id: 'order_20260622017',
    userId: 'creator_001',
    nickname: '海岛来信',
    productName: '月度会员',
    amountCoins: 0,
    payAmount: 30,
    channel: 'apple',
    status: 'paid',
    createdAt: '2026-06-22 20:12'
  },
  {
    id: 'order_20260622009',
    userId: 'bad_user_001',
    nickname: '无礼访客',
    productName: '68 金币包',
    amountCoins: 68,
    payAmount: 6,
    channel: 'android',
    status: 'refunding',
    createdAt: '2026-06-22 17:06'
  }
]

const walletRiskItems: AdminWalletRiskItem[] = [
  {
    id: 'risk_001',
    userId: 'creator_001',
    nickname: '海岛来信',
    type: 'withdraw',
    amountCoins: 120,
    charmValue: 3600,
    status: 'pending',
    riskReason: '提现金额接近本周上限',
    createdAt: '2026-06-23 09:58'
  },
  {
    id: 'risk_002',
    userId: 'bad_user_001',
    nickname: '无礼访客',
    type: 'freeze',
    amountCoins: 68,
    charmValue: 120,
    status: 'reviewing',
    riskReason: '举报命中后冻结收益',
    createdAt: '2026-06-22 22:20'
  },
  {
    id: 'risk_003',
    userId: 'creator_002',
    nickname: '晚风',
    type: 'charm_review',
    amountCoins: 50,
    charmValue: 1800,
    status: 'approved',
    riskReason: '礼物收益复核通过',
    createdAt: '2026-06-22 14:45'
  }
]

const auditLogs: AdminAuditLogItem[] = [
  {
    id: 'audit_001',
    operator: 'admin_demo',
    action: '通过内容',
    target: 'review_photo_001',
    detail: '私密照片封面审核通过',
    createdAt: '2026-06-23 10:15'
  },
  {
    id: 'audit_002',
    operator: 'risk_admin',
    action: '冻结钱包',
    target: 'bad_user_001',
    detail: '举报命中，冻结 68 收益币',
    createdAt: '2026-06-22 22:21'
  },
  {
    id: 'audit_003',
    operator: 'admin_demo',
    action: '驳回广场内容',
    target: 'review_plaza_001',
    detail: '包含站外联系方式和诱导充值描述',
    createdAt: '2026-06-22 16:40'
  }
]

const settledAdSessions = new Set<string>()
const followingUserIds = new Set<string>()
const friendRequestedUserIds = new Set<string>()

export const mockState = {
  user,
  quotas,
  adReward,
  checkin,
  verification,
  referral,
  adminSession,
  bottles,
  bottlePromptTemplates,
  treeholes,
  plazaPosts,
  nearbyUsers,
  truthQuestions,
  dareTasks,
  messages,
  conversationThreads,
  wallet,
  ledger,
  creators,
  privatePhotos,
  gifts,
  blacklist,
  adminUsers,
  contentReviews,
  chatReviews,
  adminReports,
  adRewardRecords,
  orderRecords,
  walletRiskItems,
  auditLogs,
  settledAdSessions,
  followingUserIds,
  friendRequestedUserIds
}

export function getMeStatusSnapshot(): MeStatus {
  return {
    user: { ...mockState.user },
    quotas: cloneQuotas(),
    adReward: { ...mockState.adReward },
    checkin: { ...mockState.checkin, weekRewards: [...mockState.checkin.weekRewards] }
  }
}

export function cloneQuotas(): Record<QuotaType, QuotaItem> {
  return quotaOrder.reduce((acc, type) => {
    acc[type] = { ...mockState.quotas[type] }
    return acc
  }, {} as Record<QuotaType, QuotaItem>)
}

export function consumeQuota(type: QuotaType): QuotaItem {
  const quota = mockState.quotas[type]
  if (quota.remaining <= 0) {
    throw new Error('QUOTA_NOT_ENOUGH')
  }
  quota.used += 1
  quota.remaining -= 1
  return { ...quota }
}

export function addAdRewardToAllQuotas(): Record<QuotaType, QuotaItem> {
  quotaOrder.forEach((type) => {
    const quota = mockState.quotas[type]
    quota.adBonus += mockState.adReward.rewardPerQuota
    quota.remaining += mockState.adReward.rewardPerQuota
  })
  return cloneQuotas()
}

export function resetAdCooldown(): AdRewardState {
  mockState.adReward.canWatch = false
  mockState.adReward.cooldownSeconds = mockState.adReward.cooldownMinutes * 60
  return { ...mockState.adReward }
}

export function tickAdCooldown(seconds = 1): AdRewardState {
  mockState.adReward.cooldownSeconds = Math.max(0, mockState.adReward.cooldownSeconds - seconds)
  mockState.adReward.canWatch = mockState.adReward.cooldownSeconds === 0
  return { ...mockState.adReward }
}

export function getAdminSummary(): AdminSummary {
  return {
    users: 12840,
    activeUsers: 386,
    pendingContent:
      mockState.contentReviews.filter((item) => item.status === 'pending').length +
      mockState.chatReviews.filter((item) => item.status === 'pending' || item.status === 'reviewing').length,
    reports: mockState.adminReports.filter((item) => item.status !== 'resolved').length,
    adRewardsToday: 2180,
    ordersToday: 94,
    pendingWithdrawals: mockState.walletRiskItems.filter((item) => item.status === 'pending').length,
    riskWallets: mockState.walletRiskItems.filter((item) => item.status === 'pending' || item.status === 'reviewing').length
  }
}
