import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'

const draftResponse = {
  id: '11111111-1111-1111-1111-111111111111',
  topic_id: null,
  persona_id: null,
  title: '3 套低成本通勤穿搭，一周重复穿也不尴尬',
  body: '把低成本通勤穿搭拆成 3 个公式，每个公式都保留一件稳定单品。',
  tags: ['通勤穿搭', '低成本变美', '一周穿搭'],
  status: 'generated',
  generation_source: 'frontend_mock_composer',
  created_at: '2026-06-02T12:00:00Z',
  updated_at: '2026-06-02T12:00:00Z',
}

const topicListResponse = {
  items: [
    {
      id: 'topic-api-1',
      title: '后端热点：夏日通勤包',
      source_platform: 'xiaohongshu',
      source_url: null,
      heat_score: 91,
      signal: '收藏增长快，评论集中在容量和重量',
      raw_metadata: { angle: '用 4 个包型覆盖通勤场景' },
      discovered_at: '2026-06-02T08:00:00Z',
      created_at: '2026-06-02T08:05:00Z',
    },
    {
      id: 'topic-api-2',
      title: '后端热点：轻断舍离书桌',
      source_platform: 'weibo',
      source_url: null,
      heat_score: 84,
      signal: '适合做清单式图文',
      raw_metadata: { angle: '把杂物按频率分区' },
      discovered_at: '2026-06-01T08:00:00Z',
      created_at: '2026-06-01T08:05:00Z',
    },
  ],
}

const personaListResponse = {
  items: [
    {
      id: 'persona-api-1',
      name: '后端效率派',
      audience: '职场创作者、通勤用户',
      tone: '清楚、克制、带一点行动建议',
      instructions: '保持结构清晰',
      is_active: true,
      created_at: '2026-06-02T08:10:00Z',
      updated_at: '2026-06-02T08:10:00Z',
    },
  ],
}

function previewResponse(platform: 'douyin' | 'weibo' | 'xiaohongshu') {
  return {
    id: `${platform}-preview-id`,
    draft_id: draftResponse.id,
    platform,
    title: `${platform} preview`,
    body: `${platform} body`,
    tags: ['内容运营'],
    cover_note: platform === 'xiaohongshu' ? '首图优先' : null,
    validation_status: 'valid',
    validation_details: { source: 'test' },
    created_at: '2026-06-02T12:00:00Z',
    updated_at: '2026-06-02T12:00:00Z',
  }
}

const scheduleResponse = {
  schedule: {
    id: '22222222-2222-2222-2222-222222222222',
    draft_id: draftResponse.id,
    scheduled_for: '2026-06-04T20:30:00+08:00',
    timezone: 'Asia/Shanghai',
    status: 'scheduled',
    created_at: '2026-06-02T12:10:00Z',
    updated_at: '2026-06-02T12:10:00Z',
  },
  publish_jobs: [
    {
      id: '33333333-3333-3333-3333-333333333333',
      draft_id: draftResponse.id,
      platform_preview_id: 'weibo-preview-id',
      schedule_id: '22222222-2222-2222-2222-222222222222',
      platform: 'weibo',
      status: 'scheduled',
      adapter: 'manual',
      scheduled_for: '2026-06-04T20:30:00+08:00',
      legacy_task_id: null,
      retry_count: 0,
      max_retries: 3,
      last_error: null,
      adapter_payload: null,
      queued_at: null,
      started_at: null,
      completed_at: null,
      created_at: '2026-06-02T12:10:00Z',
      updated_at: '2026-06-02T12:10:00Z',
    },
  ],
}

function mockJsonResponse(body: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify(body), {
    headers: { 'Content-Type': 'application/json' },
    status: 200,
    ...init,
  })
}

function createFetchMock(options: { draftError?: string } = {}) {
  return vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const path = String(input)
    const method = init?.method ?? 'GET'

    if (path === '/api/topics' && method === 'GET') {
      return mockJsonResponse(topicListResponse)
    }

    if (path === '/api/personas' && method === 'GET') {
      return mockJsonResponse(personaListResponse)
    }

    if (path === '/api/drafts' && method === 'POST') {
      if (options.draftError) {
        return mockJsonResponse({ detail: options.draftError }, { status: 503 })
      }

      return mockJsonResponse(draftResponse, { status: 201 })
    }

    if (path.includes('/platform-previews/douyin') && method === 'PUT') {
      return mockJsonResponse(previewResponse('douyin'))
    }

    if (path.includes('/platform-previews/weibo') && method === 'PUT') {
      return mockJsonResponse(previewResponse('weibo'))
    }

    if (path.includes('/platform-previews/xiaohongshu') && method === 'PUT') {
      return mockJsonResponse(previewResponse('xiaohongshu'))
    }

    if (path.endsWith('/schedules') && method === 'POST') {
      return mockJsonResponse(scheduleResponse, { status: 201 })
    }

    return mockJsonResponse(
      { detail: `Unhandled test request: ${method} ${path}` },
      { status: 500 },
    )
  })
}

describe('MindFlow AI workbench prototype', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', createFetchMock())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('renders the creation workspace as the first screen', async () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'AI 图文创作台' })).toBeInTheDocument()
    expect(screen.getByText('热点雷达')).toBeInTheDocument()
    expect(screen.getByText('账号人设')).toBeInTheDocument()
    expect(screen.getByText('平台预览')).toBeInTheDocument()
    expect(screen.getByText('排期日历')).toBeInTheDocument()
    expect(await screen.findByText('后端热点：夏日通勤包')).toBeInTheDocument()
  })

  it('loads backend topics and personas into the input panels', async () => {
    const fetchMock = vi.mocked(fetch)
    const user = userEvent.setup()

    render(<App />)

    expect(await screen.findByText('后端热点：夏日通勤包')).toBeInTheDocument()
    expect(screen.getByText('后端效率派')).toBeInTheDocument()
    expect(screen.queryByText('新手咖啡器具避坑')).not.toBeInTheDocument()

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith('/api/topics', expect.any(Object))
      expect(fetchMock).toHaveBeenCalledWith('/api/personas', expect.any(Object))
    })

    await user.click(screen.getByRole('button', { name: /后端热点：轻断舍离书桌/ }))

    expect(screen.getByLabelText('创作主题')).toHaveValue('后端热点：轻断舍离书桌')
  })

  it('uses a backend hot topic to seed the composer and persist generated platform copy', async () => {
    const user = userEvent.setup()
    const fetchMock = vi.mocked(fetch)

    render(<App />)

    await user.click(await screen.findByRole('button', { name: /后端热点：夏日通勤包/ }))

    expect(screen.getByLabelText('创作主题')).toHaveValue('后端热点：夏日通勤包')

    await user.click(screen.getByRole('button', { name: '生成图文' }))

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        '/api/drafts',
        expect.objectContaining({ method: 'POST' }),
      )
    })
    expect(fetchMock).toHaveBeenCalledWith(
      '/api/drafts/11111111-1111-1111-1111-111111111111/platform-previews/weibo',
      expect.objectContaining({ method: 'PUT' }),
    )
    expect(await screen.findByText('已同步后端')).toBeInTheDocument()
    expect(screen.getByDisplayValue(/3 套后端热点：夏日通勤包/)).toBeInTheDocument()
    expect(screen.getByText('微博正文')).toBeInTheDocument()
  })

  it('creates a backend schedule for the selected platform', async () => {
    const user = userEvent.setup()
    const fetchMock = vi.mocked(fetch)

    render(<App />)

    await screen.findByText('后端效率派')
    await user.click(screen.getByRole('button', { name: '生成图文' }))
    await screen.findByText('已同步后端')

    await user.click(screen.getByRole('button', { name: '微博' }))
    await user.click(screen.getByRole('button', { name: '加入排期' }))

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        '/api/drafts/11111111-1111-1111-1111-111111111111/schedules',
        expect.objectContaining({ method: 'POST' }),
      )
    })
    expect(screen.getByText('已加入排期')).toBeInTheDocument()
    expect(screen.getByText('周四 20:30')).toBeInTheDocument()
    expect(screen.getByText('微博 · scheduled · manual')).toBeInTheDocument()
  })

  it('shows backend errors instead of silently falling back to mock persistence', async () => {
    vi.stubGlobal('fetch', createFetchMock({ draftError: 'database unavailable' }))
    const user = userEvent.setup()

    render(<App />)

    await screen.findByText('后端效率派')
    await user.click(screen.getByRole('button', { name: '生成图文' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'database unavailable',
    )
  })
})
