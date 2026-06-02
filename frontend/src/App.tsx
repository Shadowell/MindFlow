import { useMemo, useState } from 'react'
import {
  Activity,
  Calendar,
  CheckCircle2,
  Clock,
  FileText,
  Flame,
  Image as ImageIcon,
  LayoutGrid,
  Link as LinkIcon,
  Megaphone,
  Send,
  Sparkles,
  User as UserIcon,
  Wand2,
} from 'lucide-react'
import { MindFlowApi, type PlatformId, type ScheduleCreateResponse } from './api'
import './App.css'

type HotTopic = {
  title: string
  source: string
  heat: string
  angle: string
  signal: string
}

type Persona = {
  id: string
  name: string
  tone: string
  audience: string
}

type PlatformPreview = {
  label: string
  title: string
  metric: string
  copy: string
  hints: string[]
}

const hotTopics: HotTopic[] = [
  {
    title: '低成本通勤穿搭',
    source: '小红书趋势',
    heat: '96',
    angle: '用 3 套搭配解决一周通勤',
    signal: '收藏率高，评论集中在预算和显瘦',
  },
  {
    title: '周末轻断舍离清单',
    source: '微博热议',
    heat: '88',
    angle: '用一张表安排衣柜和书桌',
    signal: '适合图文长帖，互动问题明确',
  },
  {
    title: '新手咖啡器具避坑',
    source: '抖音热点',
    heat: '82',
    angle: '把预算拆成入门、进阶、耐用',
    signal: '短视频可转为 9 图讲解',
  },
]

const personas: Persona[] = [
  {
    id: 'operator',
    name: '都市效率派',
    tone: '克制、清楚、像朋友给建议',
    audience: '职场新人、通勤用户',
  },
  {
    id: 'curator',
    name: '生活方式种草',
    tone: '温和、细节丰富、重体验',
    audience: '小红书女性用户、轻消费人群',
  },
  {
    id: 'local',
    name: '本地探店编辑',
    tone: '直接、信息密、带行动建议',
    audience: '同城用户、周末出行人群',
  },
]

const platformPreviews: Record<PlatformId, PlatformPreview> = {
  douyin: {
    label: '抖音',
    title: '抖音图文',
    metric: '预计互动 2.4k',
    copy: '首图抓重点，后 6 图拆步骤。结尾用提问拉评论：你最常卡在哪个搭配场景？',
    hints: ['9 图以内', '标题 16 字内', '首图保留文字安全区'],
  },
  weibo: {
    label: '微博',
    title: '微博正文',
    metric: '预计转评 860',
    copy: '适合发成轻攻略长微博，正文先给结论，再用 3 条清单展开，最后加一个投票式问题。',
    hints: ['正文 600 字以内', '配 4 张图', '话题标签 2 个'],
  },
  xiaohongshu: {
    label: '小红书',
    title: '小红书笔记',
    metric: '预计收藏 1.8k',
    copy: '用问题开头，把预算、适用场景和搭配公式写清楚。每一页只讲一个重点，降低阅读负担。',
    hints: ['首图优先', '标题带场景', '标签 5 到 8 个'],
  },
}

const scheduleTime = '周四 20:30'
const scheduledFor = '2026-06-04T20:30:00+08:00'

function createDraft(topic: string, persona: Persona) {
  const subject = topic.trim() || '低成本通勤穿搭'

  return [
    `标题：3 套${subject}，一周重复穿也不尴尬`,
    '',
    `人设：${persona.name}`,
    `语气：${persona.tone}`,
    '',
    '正文：',
    `这组内容先解决一个真实问题：早上没有时间搭配，但又不想每天穿得像同一套。把${subject}拆成 3 个公式，每个公式都保留一件稳定单品，再用颜色或配饰做变化。`,
    '',
    '1. 衬衫加直筒裤：适合会议日，重点是线条干净。',
    '2. 针织衫加半裙：适合普通工作日，重点是舒适和显精神。',
    '3. 外套加基础 T：适合通勤和下班约会，重点是方便切换场景。',
    '',
    '结尾互动：你最想先改造哪一套？评论区给我你的预算和场景。',
    '',
    '#通勤穿搭 #低成本变美 #一周穿搭',
  ].join('\n')
}

function createDraftTitle(topic: string) {
  const subject = topic.trim() || '低成本通勤穿搭'
  return `3 套${subject}，一周重复穿也不尴尬`
}

function draftTags(topic: string) {
  const subject = topic.trim() || '通勤穿搭'
  return [subject, '内容运营', '自动排期']
}

function App() {
  const [topic, setTopic] = useState('低成本通勤穿搭')
  const [selectedPersonaId, setSelectedPersonaId] = useState(personas[0].id)
  const [draft, setDraft] = useState('')
  const [draftStatus, setDraftStatus] = useState('待生成')
  const [selectedPlatform, setSelectedPlatform] = useState<PlatformId>('weibo')
  const [persistedDraftId, setPersistedDraftId] = useState<string | null>(null)
  const [scheduleResult, setScheduleResult] = useState<ScheduleCreateResponse | null>(null)
  const [apiError, setApiError] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isScheduling, setIsScheduling] = useState(false)

  const selectedPersona =
    personas.find((persona) => persona.id === selectedPersonaId) ?? personas[0]

  const activePreview = platformPreviews[selectedPlatform]
  const isScheduled = scheduleResult !== null
  const activeJob = scheduleResult?.publish_jobs.find(
    (job) => job.platform === selectedPlatform,
  )

  const mediaSlots = useMemo(
    () => [
      { label: '封面', caption: '标题安全区' },
      { label: '图 2', caption: '公式拆解' },
      { label: '图 3', caption: '清单对比' },
      { label: '图 4', caption: '结尾互动' },
    ],
    [],
  )

  function selectHotTopic(nextTopic: string) {
    setTopic(nextTopic)
    setDraftStatus('待生成')
    setPersistedDraftId(null)
    setScheduleResult(null)
    setApiError(null)
  }

  async function generateDraft() {
    const nextDraft = createDraft(topic, selectedPersona)
    const nextTitle = createDraftTitle(topic)
    const nextTags = draftTags(topic)

    setDraft(nextDraft)
    setDraftStatus('同步中')
    setScheduleResult(null)
    setApiError(null)
    setIsGenerating(true)

    try {
      const persistedDraft = await MindFlowApi.createDraft({
        body: nextDraft,
        generation_source: 'frontend_mock_composer',
        status: 'generated',
        tags: nextTags,
        title: nextTitle,
      })

      await Promise.all(
        (Object.keys(platformPreviews) as PlatformId[]).map((platformId) =>
          MindFlowApi.upsertPlatformPreview(persistedDraft.id, platformId, {
            body: platformPreviews[platformId].copy,
            tags: platformPreviews[platformId].hints,
            title: platformPreviews[platformId].title,
            validation_details: {
              hints: platformPreviews[platformId].hints,
              metric: platformPreviews[platformId].metric,
            },
            validation_status: 'valid',
          }),
        ),
      )

      setPersistedDraftId(persistedDraft.id)
      setDraftStatus('已同步后端')
    } catch (error) {
      setPersistedDraftId(null)
      setDraftStatus('同步失败')
      setApiError(error instanceof Error ? error.message : '后端同步失败')
    } finally {
      setIsGenerating(false)
    }
  }

  async function addToSchedule() {
    if (!persistedDraftId) {
      setApiError('请先生成图文并同步后端。')
      return
    }

    setApiError(null)
    setIsScheduling(true)

    try {
      const result = await MindFlowApi.createSchedule(persistedDraftId, {
        adapter: 'manual',
        platforms: [selectedPlatform],
        scheduled_for: scheduledFor,
        timezone: 'Asia/Shanghai',
      })
      setScheduleResult(result)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : '排期创建失败')
    } finally {
      setIsScheduling(false)
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">MindFlow Content Ops</p>
          <h1>AI 图文创作台</h1>
        </div>
        <div className="topbar-actions" aria-label="工作台状态">
          <span className="status-pill">
            <Activity aria-hidden="true" size={16} />
            今日 12 条趋势
          </span>
            <span className="status-pill strong">
            <CheckCircle2 aria-hidden="true" size={16} />
            后端 API 已接入
          </span>
        </div>
      </header>

      <section className="workspace-grid" aria-label="AI 创作工作流">
        <aside className="side-column left-column" aria-label="素材输入">
          <section className="panel">
            <div className="panel-title">
              <Flame aria-hidden="true" size={18} />
              <h2>热点雷达</h2>
            </div>
            <div className="hot-topic-list">
              {hotTopics.map((hotTopic) => (
                <button
                  className="hot-topic"
                  key={hotTopic.title}
                  onClick={() => selectHotTopic(hotTopic.title)}
                  type="button"
                >
                  <span className="hot-topic-main">
                    <span>{hotTopic.title}</span>
                    <strong>{hotTopic.heat}</strong>
                  </span>
                  <span className="hot-topic-meta">
                    {hotTopic.source} · {hotTopic.angle}
                  </span>
                  <span className="hot-topic-signal">{hotTopic.signal}</span>
                </button>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="panel-title">
              <UserIcon aria-hidden="true" size={18} />
              <h2>账号人设</h2>
            </div>
            <div className="persona-list">
              {personas.map((persona) => (
                <button
                  aria-pressed={persona.id === selectedPersonaId}
                  className="persona-option"
                  key={persona.id}
                  onClick={() => setSelectedPersonaId(persona.id)}
                  type="button"
                >
                  <span>{persona.name}</span>
                  <small>{persona.audience}</small>
                </button>
              ))}
            </div>
            <div className="persona-tone">
              <span>输出语气</span>
              <p>{selectedPersona.tone}</p>
            </div>
          </section>
        </aside>

        <section className="composer-panel" aria-label="图文生成编辑区">
          <div className="composer-header">
            <div>
              <div className="panel-title">
                <Wand2 aria-hidden="true" size={18} />
                <h2>图文生成编辑区</h2>
              </div>
              <p className="section-note">当前批次：热点选题 1 条，草稿待审核，排期未确认。</p>
            </div>
            <span className={draftStatus === '已同步后端' ? 'status-tag done' : 'status-tag'}>
              {draftStatus}
            </span>
          </div>

          <div className="field-row">
            <label htmlFor="topic">创作主题</label>
            <input
              id="topic"
              name="topic"
              onChange={(event) => setTopic(event.target.value)}
              type="text"
              value={topic}
            />
          </div>

          <div className="brief-grid" aria-label="生成参数">
            <div>
              <span>内容类型</span>
              <strong>图文笔记</strong>
            </div>
            <div>
              <span>目标平台</span>
              <strong>抖音 · 微博 · 小红书</strong>
            </div>
            <div>
              <span>发布节奏</span>
              <strong>当天生成，隔天复盘</strong>
            </div>
          </div>

          <div className="media-strip" aria-label="配图结构">
            {mediaSlots.map((slot) => (
              <div className="media-slot" key={slot.label}>
                <ImageIcon aria-hidden="true" size={20} />
                <strong>{slot.label}</strong>
                <span>{slot.caption}</span>
              </div>
            ))}
          </div>

          <label className="editor-label" htmlFor="draft">
            生成正文
          </label>
          <textarea
            id="draft"
            onChange={(event) => setDraft(event.target.value)}
            placeholder="生成后的标题、正文、标签会出现在这里。"
            value={draft}
          />

          <div className="composer-actions">
            <button
              className="primary-action"
              disabled={isGenerating}
              onClick={generateDraft}
              type="button"
            >
              <Sparkles aria-hidden="true" size={18} />
              {isGenerating ? '同步中' : '生成图文'}
            </button>
            <button className="secondary-action" type="button">
              <FileText aria-hidden="true" size={18} />
              保存草稿
            </button>
            <button className="secondary-action" type="button">
              <LinkIcon aria-hidden="true" size={18} />
              Legacy 发布能力
            </button>
          </div>
          {apiError ? (
            <div className="api-error" role="alert">
              {apiError}
            </div>
          ) : null}
        </section>

        <aside className="side-column right-column" aria-label="发布输出">
          <section className="panel preview-panel">
            <div className="panel-title">
              <LayoutGrid aria-hidden="true" size={18} />
              <h2>平台预览</h2>
            </div>
            <div className="platform-tabs" role="group" aria-label="平台选择">
              {(Object.keys(platformPreviews) as PlatformId[]).map((platformId) => (
                <button
                  aria-pressed={platformId === selectedPlatform}
                  key={platformId}
                  onClick={() => setSelectedPlatform(platformId)}
                  type="button"
                >
                  {platformPreviews[platformId].label}
                </button>
              ))}
            </div>

            <article className={`platform-card ${selectedPlatform}`}>
              <div className="platform-card-head">
                <div>
                  <span>{activePreview.label}</span>
                  <h3>{activePreview.title}</h3>
                </div>
                <strong>{activePreview.metric}</strong>
              </div>
              <p>{activePreview.copy}</p>
              <div className="preview-visual">
                <Megaphone aria-hidden="true" size={22} />
                <span>{draftStatus === '已同步后端' ? '内容已同步到预览' : '等待生成内容'}</span>
              </div>
              <div className="hint-list">
                {activePreview.hints.map((hint) => (
                  <span key={hint}>{hint}</span>
                ))}
              </div>
              {selectedPlatform === 'xiaohongshu' ? (
                <div className="cover-brief">
                  <h4>封面建议</h4>
                  <p>主标题放上半区，保留一张全身搭配图，右下角给预算标签。</p>
                </div>
              ) : null}
            </article>
          </section>

          <section className="panel schedule-panel">
            <div className="panel-title">
              <Calendar aria-hidden="true" size={18} />
              <h2>排期日历</h2>
            </div>
            <div className="schedule-summary">
              <div>
                <Clock aria-hidden="true" size={18} />
                <span>{scheduleTime}</span>
              </div>
              <strong>{isScheduled ? '已加入排期' : '待发布'}</strong>
            </div>
            <div className="queue-list">
              <div>
                <span>抖音</span>
                <strong>
                  {scheduleResult?.publish_jobs.find((job) => job.platform === 'douyin')
                    ? '抖音 · scheduled · manual'
                    : isScheduled
                      ? '图文草稿已排队'
                      : '待选择时段'}
                </strong>
              </div>
              <div>
                <span>微博</span>
                <strong>
                  {scheduleResult?.publish_jobs.find((job) => job.platform === 'weibo')
                    ? '微博 · scheduled · manual'
                    : isScheduled
                      ? '正文待审核'
                      : '待同步草稿'}
                </strong>
              </div>
              <div>
                <span>小红书</span>
                <strong>
                  {scheduleResult?.publish_jobs.find((job) => job.platform === 'xiaohongshu')
                    ? '小红书 · scheduled · manual'
                    : isScheduled
                      ? '封面待确认'
                      : '待补封面'}
                </strong>
              </div>
            </div>
            {activeJob ? (
              <p className="job-note">
                当前平台发布任务：{activeJob.status} · {activeJob.adapter}
              </p>
            ) : null}
            <button
              className="schedule-action"
              disabled={isScheduling || !persistedDraftId}
              onClick={addToSchedule}
              type="button"
            >
              <Send aria-hidden="true" size={18} />
              {isScheduling ? '创建排期中' : '加入排期'}
            </button>
          </section>
        </aside>
      </section>
    </main>
  )
}

export default App
