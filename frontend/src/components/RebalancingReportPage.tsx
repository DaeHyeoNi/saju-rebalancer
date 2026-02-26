import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import type { RebalancingReportData } from '../types'
import { api } from '../api/client'
import Step3Results from './Step3Results'

export default function RebalancingReportPage() {
  const { uuid } = useParams<{ uuid: string }>()
  const navigate = useNavigate()
  const [report, setReport] = useState<RebalancingReportData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!uuid) return
    api.getReport(uuid)
      .then(data => setReport(data))
      .catch(err => setError(err instanceof Error ? err.message : '리포트를 불러오지 못했습니다.'))
      .finally(() => setLoading(false))
  }, [uuid])

  if (loading) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>사주 포트폴리오 리밸런서</h1>
        </header>
        <main className="app-main">
          <div className="step-container">
            <p>리포트를 불러오는 중…</p>
          </div>
        </main>
      </div>
    )
  }

  if (error || !report) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>사주 포트폴리오 리밸런서</h1>
        </header>
        <main className="app-main">
          <div className="step-container">
            <p className="error">{error ?? '리포트를 찾을 수 없습니다.'}</p>
            <button className="btn-secondary" onClick={() => navigate('/')}>홈으로</button>
          </div>
        </main>
      </div>
    )
  }

  const sajuData = {
    saju_id: 0,
    pillars: report.saju_data.pillars,
    reading: report.saju_data.reading,
  }

  const result = {
    rebalance_table: report.rebalance_table,
    narrative: report.narrative,
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>사주 포트폴리오 리밸런서</h1>
        <p>저장된 분석 결과 — {new Date(report.created_at).toLocaleDateString('ko-KR')}</p>
      </header>
      <main className="app-main">
        <Step3Results
          sajuData={sajuData}
          result={result}
          portfolioItems={report.portfolio_items}
          reportUuid={uuid}
          onReset={() => navigate('/')}
        />
      </main>
    </div>
  )
}
