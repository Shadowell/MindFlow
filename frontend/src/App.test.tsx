import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import App from './App'

describe('MindFlow AI workbench prototype', () => {
  it('renders the creation workspace as the first screen', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'AI 图文创作台' })).toBeInTheDocument()
    expect(screen.getByText('热点雷达')).toBeInTheDocument()
    expect(screen.getByText('账号人设')).toBeInTheDocument()
    expect(screen.getByText('平台预览')).toBeInTheDocument()
    expect(screen.getByText('排期日历')).toBeInTheDocument()
  })

  it('uses a hot topic to seed the composer and generate platform copy', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: /低成本通勤穿搭/ }))

    expect(screen.getByLabelText('创作主题')).toHaveValue('低成本通勤穿搭')

    await user.click(screen.getByRole('button', { name: '生成图文' }))

    expect(screen.getByText('已生成')).toBeInTheDocument()
    expect(screen.getByDisplayValue(/3 套低成本通勤穿搭/)).toBeInTheDocument()
    expect(screen.getByText('微博正文')).toBeInTheDocument()
  })

  it('switches platform preview and adds the draft to schedule', async () => {
    const user = userEvent.setup()
    render(<App />)

    await user.click(screen.getByRole('button', { name: '小红书' }))
    expect(screen.getByText('小红书笔记')).toBeInTheDocument()
    expect(screen.getByText('封面建议')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: '加入排期' }))

    expect(screen.getByText('已加入排期')).toBeInTheDocument()
    expect(screen.getByText('周四 20:30')).toBeInTheDocument()
  })
})
