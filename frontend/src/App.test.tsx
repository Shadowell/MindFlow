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

describe('MindFlow AI workbench prototype', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => mockJsonResponse({ items: [] })),
    )
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('renders the creation workspace as the first screen', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'AI 图文创作台' })).toBeInTheDocument()
    expect(screen.getByText('热点雷达')).toBeInTheDocument()
    expect(screen.getByText('账号人设')).toBeInTheDocument()
    expect(screen.getByText('平台预览')).toBeInTheDocument()
    expect(screen.getByText('排期日历')).toBeInTheDocument()
  })

  it('uses a hot topic to seed the composer and persist generated platform copy', async () => {
    const user = userEvent.setup()
    const fetchMock = vi.mocked(fetch)
    fetchMock
      .mockResolvedValueOnce(mockJsonResponse(draftResponse, { status: 201 }))
      .mockResolvedValueOnce(mockJsonResponse(previewResponse('douyin')))
      .mockResolvedValueOnce(mockJsonResponse(previewResponse('weibo')))
      .mockResolvedValueOnce(mockJsonResponse(previewResponse('xiaohongshu')))

    render(<App />)

    await user.click(screen.getByRole('button', { name: /低成本通勤穿搭/ }))

    expect(screen.getByLabelText('创作主题')).toHaveValue('低成本通勤穿搭')

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
    expect(screen.getByDisplayValue(/3 套低成本通勤穿搭/)).toBeInTheDocument()
    expect(screen.getByText('微博正文')).toBeInTheDocument()
  })

  it('creates a backend schedule for the selected platform', async () => {
    const user = userEvent.setup()
    const fetchMock = vi.mocked(fetch)
    fetchMock
      .mockResolvedValueOnce(mockJsonResponse(draftResponse, { status: 201 }))
      .mockResolvedValueOnce(mockJsonResponse(previewResponse('douyin')))
      .mockResolvedValueOnce(mockJsonResponse(previewResponse('weibo')))
      .mockResolvedValueOnce(mockJsonResponse(previewResponse('xiaohongshu')))
      .mockResolvedValueOnce(mockJsonResponse(scheduleResponse, { status: 201 }))

    render(<App />)

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
    const user = userEvent.setup()
    const fetchMock = vi.mocked(fetch)
    fetchMock.mockResolvedValueOnce(
      mockJsonResponse({ detail: 'database unavailable' }, { status: 503 }),
    )

    render(<App />)

    await user.click(screen.getByRole('button', { name: '生成图文' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(
      'database unavailable',
    )
  })
})
