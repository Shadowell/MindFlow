export type PlatformId = 'douyin' | 'weibo' | 'xiaohongshu'

export type DraftResponse = {
  id: string
  title: string
  body: string
  tags: string[]
  status: string
  generation_source: string | null
  created_at: string
  updated_at: string
}

export type DraftListResponse = {
  items: DraftResponse[]
}

export type PlatformPreviewResponse = {
  id: string
  draft_id: string
  platform: PlatformId
  title: string | null
  body: string
  tags: string[]
  validation_status: string
}

export type PublishJobResponse = {
  id: string
  platform: PlatformId
  status: string
  adapter: string
}

export type ScheduleCreateResponse = {
  schedule: {
    id: string
    status: string
    scheduled_for: string
    timezone: string
  }
  publish_jobs: PublishJobResponse[]
}

type RequestBody = Record<string, unknown>

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => undefined)
    const detail =
      payload && typeof payload === 'object' && 'detail' in payload
        ? String(payload.detail)
        : `Backend request failed: ${response.status}`
    throw new Error(detail)
  }

  return response.json() as Promise<T>
}

export const MindFlowApi = {
  createDraft(payload: RequestBody) {
    return request<DraftResponse>('/drafts', {
      body: JSON.stringify(payload),
      method: 'POST',
    })
  },

  listDrafts() {
    return request<DraftListResponse>('/drafts')
  },

  readDraft(draftId: string) {
    return request<DraftResponse>(`/drafts/${draftId}`)
  },

  upsertPlatformPreview(
    draftId: string,
    platform: PlatformId,
    payload: RequestBody,
  ) {
    return request<PlatformPreviewResponse>(
      `/drafts/${draftId}/platform-previews/${platform}`,
      {
        body: JSON.stringify(payload),
        method: 'PUT',
      },
    )
  },

  createSchedule(draftId: string, payload: RequestBody) {
    return request<ScheduleCreateResponse>(`/drafts/${draftId}/schedules`, {
      body: JSON.stringify(payload),
      method: 'POST',
    })
  },
}
