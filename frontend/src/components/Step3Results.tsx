import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import type { SajuAnalyzeResponse, RebalanceResponse, PortfolioItem } from '../types'

// CommonMark 스펙상 )**한글 패턴에서 닫는 ** 가 right-flanking으로 인식 안 되는 버그 수정.
// ) 와 ** 사이에 ZWNJ(U+200C)를 삽입하면 파서가 정상 인식하며 시각적으로 무해함.
function fixBold(text: string): string {
  return text.replace(/\)\*\*/g, ')\u200C**')
}

interface Props {
  sajuData: SajuAnalyzeResponse
  result: RebalanceResponse
  portfolioItems: PortfolioItem[]
  reportUuid?: string
  onReset: () => void
}

const ACTION_COLOR: Record<string, string> = {
  '매수': '#2e7d32',
  '매도': '#c62828',
  '유지': '#1565c0',
  '비중확대': '#2e7d32',
  '비중축소': '#c62828',
}

function displayAction(name: string, action: string): string {
  if (name === '현금') {
    if (action === '매수') return '비중확대'
    if (action === '매도') return '비중축소'
  }
  return action
}

export default function Step3Results({ sajuData, result, portfolioItems, reportUuid, onReset }: Props) {
  const [copied, setCopied] = useState(false)
  const shareUrl = reportUuid ? `${window.location.origin}/rebalancing-report/${reportUuid}` : null

  const handleCopy = () => {
    if (!shareUrl) return
    navigator.clipboard.writeText(shareUrl).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }
  const totalBuy = result.rebalance_table
    .filter(r => r.action === '매수' && r.name !== '현금')
    .reduce((s, r) => s + r.amount, 0)
  const totalSell = result.rebalance_table
    .filter(r => r.action === '매도' && r.name !== '현금')
    .reduce((s, r) => s + r.amount, 0)

  const totalCurrentValue = portfolioItems.reduce((s, i) => s + i.current_value, 0)
  const totalTargetValue = result.rebalance_table.reduce((s, r) => s + r.target_value, 0)

  // 종목명 → 수량/현재가치 매핑 (통화 무관하게 KRW 단가 역산에 사용)
  const quantityMap = new Map(portfolioItems.map(i => [i.name, i.quantity ?? null]))
  const currentValueMap = new Map(portfolioItems.map(i => [i.name, i.current_value]))

  return (
    <div className="step-container">
      <h2>분석 결과</h2>

      {/* 사주 풀이 */}
      <section className="result-section">
        <h3>사주 풀이</h3>
        <div className="pillars">
          {(['year_pillar', 'month_pillar', 'day_pillar', 'hour_pillar'] as const).map(key => {
            const val = sajuData.pillars[key]
            if (!val) return null
            const labels: Record<string, string> = {
              year_pillar: '년', month_pillar: '월',
              day_pillar: '일', hour_pillar: '시',
            }
            return (
              <div key={key} className="pillar-card">
                <span className="pillar-label">{labels[key]}주</span>
                <span className="pillar-value">{String(val)}</span>
              </div>
            )
          })}
        </div>
        <div className="reading-text">
          <ReactMarkdown>{fixBold(sajuData.reading)}</ReactMarkdown>
        </div>
      </section>

      {/* 리밸런싱 요약 */}
      <section className="result-section">
        <h3>리밸런싱 요약</h3>
        <div className="summary-badges">
          <span className="badge buy">매수 총액 {totalBuy.toLocaleString()}원</span>
          <span className="badge sell">매도 총액 {totalSell.toLocaleString()}원</span>
        </div>

        <div className="table-scroll">
          <table className="rebalance-table">
            <thead>
              <tr>
                <th>종목</th>
                <th>액션</th>
                <th>거래 주수</th>
                <th>거래금액</th>
                <th>변경 전 비중</th>
                <th>변경 후 비중</th>
                <th>이유</th>
              </tr>
            </thead>
            <tbody>
              {result.rebalance_table.map((row, i) => {
                const quantity = quantityMap.get(row.name)
                const currentValue = currentValueMap.get(row.name) ?? 0
                // 통화 무관하게 KRW 단가 역산: current_value(KRW) / quantity
                // USD 종목도 동일 공식으로 주수 계산 가능
                const impliedKrwPrice = quantity && quantity > 0 ? currentValue / quantity : null
                const tradeQty = impliedKrwPrice && row.action !== '유지' && row.name !== '현금'
                  ? Math.round(row.amount / impliedKrwPrice)
                  : null
                const beforePct = totalCurrentValue > 0
                  ? (currentValue / totalCurrentValue * 100).toFixed(1)
                  : '-'
                const afterPct = totalTargetValue > 0
                  ? (row.target_value / totalTargetValue * 100).toFixed(1)
                  : '-'
                const label = displayAction(row.name, row.action)

                return (
                  <tr key={i}>
                    <td>{row.name}</td>
                    <td style={{ color: ACTION_COLOR[label] ?? '#333', fontWeight: 700 }}>
                      {label}
                    </td>
                    <td>{tradeQty != null ? `${tradeQty}주` : '-'}</td>
                    <td>{row.amount.toLocaleString()}원</td>
                    <td>{beforePct !== '-' ? `${beforePct}%` : '-'}</td>
                    <td>{afterPct !== '-' ? `${afterPct}%` : '-'}</td>
                    <td className="reason-cell">{row.reason}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </section>

      {/* 종합 해설 */}
      <section className="result-section">
        <h3>종합 해설</h3>
        <div className="narrative-text">
          <ReactMarkdown>{fixBold(result.narrative)}</ReactMarkdown>
        </div>
      </section>

      {shareUrl && (
        <section className="result-section share-section">
          <h3>결과 공유</h3>
          <p className="hint">아래 URL로 이 분석 결과를 언제든지 다시 볼 수 있습니다.</p>
          <div className="share-url-row">
            <input className="share-url-input" readOnly value={shareUrl} onClick={e => (e.target as HTMLInputElement).select()} />
            <button className="btn-copy" onClick={handleCopy}>
              {copied ? '복사됨!' : 'URL 복사'}
            </button>
          </div>
        </section>
      )}

      <button className="btn-secondary" onClick={onReset}>
        처음부터 다시 하기
      </button>
    </div>
  )
}
