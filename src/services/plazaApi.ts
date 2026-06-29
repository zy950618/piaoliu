import type { PlazaComment, PlazaMedia, PlazaPost } from '@/types/domain'
import { requestJson } from '@/services/http'

type PlazaPostDto = {
  id: string
  author_id: string
  author_name: string
  icon_text: string
  icon_url?: string
  topic: string
  content: string
  media_type?: PlazaPost['mediaType']
  media_count?: number
  gender?: PlazaPost['gender']
  verified?: boolean
  city?: string
  age_range?: string
  view_count?: number
  like_count: number
  liked_by_current_user?: boolean
  comment_count: number
  comment_preview?: string
  media?: PlazaMediaDto[]
  distance_text?: string
  created_at: string
}

type PlazaMediaDto = {
  id: string
  post_id: string
  owner_id: string
  media_type: PlazaMedia['mediaType']
  url: string
  storage_key?: string
  mime_type: string
  size_bytes?: number
  duration_seconds?: number
  width?: number
  height?: number
  created_at: string
}

type PlazaMediaInput = {
  mediaType: PlazaMedia['mediaType']
  url: string
  mimeType: string
  storageKey?: string
  sizeBytes?: number
  durationSeconds?: number
  width?: number
  height?: number
}

type PlazaCommentDto = {
  id: string
  post_id: string
  author_id: string
  author_name: string
  icon_text: string
  icon_url?: string
  author_gender?: PlazaComment['authorGender']
  author_age_range?: string
  author_verified?: boolean
  author_city?: string
  content: string
  hidden_for_owner_only?: boolean
  visible_to_owner_only?: boolean
  created_at: string
}

function toPlazaPost(dto: PlazaPostDto): PlazaPost {
  return {
    id: dto.id,
    authorId: dto.author_id,
    authorName: dto.author_name,
    iconText: dto.icon_text,
    iconUrl: dto.icon_url,
    topic: dto.topic,
    content: dto.content,
    mediaType: dto.media_type,
    mediaCount: dto.media_count,
    gender: dto.gender,
    verified: dto.verified,
    city: dto.city,
    ageRange: dto.age_range,
    viewCount: dto.view_count,
    likeCount: dto.like_count,
    likedByMe: dto.liked_by_current_user,
    commentCount: dto.comment_count,
    commentPreview: dto.comment_preview,
    media: (dto.media || []).map(toPlazaMedia),
    distanceText: dto.distance_text,
    createdAt: dto.created_at
  }
}

function toPlazaMedia(dto: PlazaMediaDto): PlazaMedia {
  return {
    id: dto.id,
    postId: dto.post_id,
    ownerId: dto.owner_id,
    mediaType: dto.media_type,
    url: dto.url,
    storageKey: dto.storage_key,
    mimeType: dto.mime_type,
    sizeBytes: dto.size_bytes,
    durationSeconds: dto.duration_seconds,
    width: dto.width,
    height: dto.height,
    createdAt: dto.created_at
  }
}

function toPlazaComment(dto: PlazaCommentDto): PlazaComment {
  return {
    id: dto.id,
    postId: dto.post_id,
    authorId: dto.author_id,
    authorName: dto.author_name,
    iconText: dto.icon_text,
    iconUrl: dto.icon_url,
    authorGender: dto.author_gender,
    authorAgeRange: dto.author_age_range,
    authorVerified: dto.author_verified,
    authorCity: dto.author_city,
    content: dto.content,
    hiddenForOwnerOnly: dto.hidden_for_owner_only,
    visibleToOwnerOnly: dto.visible_to_owner_only,
    createdAt: dto.created_at
  }
}

export const plazaApi = {
  async listPosts(filters: { city?: string; gender?: string; ageRange?: string } = {}) {
    const params = new URLSearchParams()
    if (filters.city) params.set('city', filters.city)
    if (filters.gender) params.set('gender', filters.gender)
    if (filters.ageRange) params.set('age_range', filters.ageRange)
    const query = params.toString()
    const posts = await requestJson<PlazaPostDto[]>(`/plaza/posts${query ? `?${query}` : ''}`)
    return posts.map(toPlazaPost)
  },

  async getPost(postId: string) {
    const post = await requestJson<PlazaPostDto>(`/plaza/posts/${postId}`)
    return toPlazaPost(post)
  },

  async publishPost(content: string, options: { mediaType?: PlazaPost['mediaType']; mediaCount?: number; media?: PlazaMediaInput[] } = {}) {
    const media = options.media || []
    const mediaType = options.mediaType || (media[0]?.mediaType ?? 'text')
    const mediaCount = options.mediaCount ?? media.length
    const post = await requestJson<PlazaPostDto>('/plaza/posts', {
      method: 'POST',
      body: {
        content,
        media_type: mediaType,
        media_count: mediaCount,
        media: media.map((item) => ({
          media_type: item.mediaType,
          url: item.url,
          mime_type: item.mimeType,
          storage_key: item.storageKey,
          size_bytes: item.sizeBytes,
          duration_seconds: item.durationSeconds,
          width: item.width,
          height: item.height
        }))
      }
    })
    return toPlazaPost(post)
  },

  async likePost(postId: string) {
    const post = await requestJson<PlazaPostDto>(`/plaza/posts/${postId}/like`, {
      method: 'POST'
    })
    return toPlazaPost(post)
  },

  async listComments(postId: string) {
    const comments = await requestJson<PlazaCommentDto[]>(`/plaza/posts/${postId}/comments`)
    return comments.map(toPlazaComment)
  },

  async commentPost(postId: string, content: string, options: { hiddenForOwnerOnly?: boolean } = {}) {
    const post = await requestJson<PlazaPostDto>(`/plaza/posts/${postId}/comments`, {
      method: 'POST',
      body: JSON.stringify({
        content,
        hidden_for_owner_only: !!options.hiddenForOwnerOnly
      })
    })
    return toPlazaPost(post)
  }
}
