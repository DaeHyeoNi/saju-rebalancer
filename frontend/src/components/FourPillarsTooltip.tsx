/**
 * 영어 모드에서만 표시되는 "Four Pillars of Destiny" 툴팁 컴포넌트.
 * 두 가지 형태:
 *   <FourPillarsTooltip />           — 인라인 용어 + 호버 팝업
 *   <FourPillarsInfoBox />           — 인트로 페이지용 접힘/펼침 인포박스
 */
import { useState } from 'react'
import { useTranslation } from 'react-i18next'

// ── 인라인 툴팁 ──────────────────────────────────────────────────────────────
export function FourPillarsTooltip() {
  const { t, i18n } = useTranslation()
  if (!i18n.language.startsWith('en')) return null

  const lines = t('fourPillars.tooltipBody', { returnObjects: true }) as string[]

  return (
    <span className="fp-term-wrap">
      <span className="fp-term">
        {t('fourPillars.termFull')}
        <span className="fp-term-icon" aria-label="info">ⓘ</span>
      </span>
      <span className="fp-tooltip" role="tooltip">
        <strong className="fp-tooltip-title">{t('fourPillars.tooltipTitle')}</strong>
        <em className="fp-tooltip-note">{t('fourPillars.termNote')}</em>
        {lines.map((p, i) => <p key={i}>{p}</p>)}
      </span>
    </span>
  )
}

// ── 인트로 인포박스 ──────────────────────────────────────────────────────────
export function FourPillarsInfoBox() {
  const { t, i18n } = useTranslation()
  const [open, setOpen] = useState(false)

  if (!i18n.language.startsWith('en')) return null

  const lines = t('fourPillars.tooltipBody', { returnObjects: true }) as string[]

  return (
    <div className="fp-infobox">
      <button
        className="fp-infobox-toggle"
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
      >
        <span className="fp-infobox-icon">ⓘ</span>
        {open ? t('fourPillars.learnLess') : t('fourPillars.infoTitle')}
        <span className={`fp-infobox-chevron ${open ? 'open' : ''}`}>›</span>
      </button>

      {open && (
        <div className="fp-infobox-content">
          <div className="fp-infobox-header">
            <strong>{t('fourPillars.tooltipTitle')}</strong>
            <em>{t('fourPillars.termNote')}</em>
          </div>
          {lines.map((p, i) => <p key={i}>{p}</p>)}
        </div>
      )}
    </div>
  )
}
