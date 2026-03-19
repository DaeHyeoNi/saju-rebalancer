import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'

const SITE_NAME_KO = '사주재무연구소'
const SITE_NAME_EN = 'Four Pillars Finance Lab'

/**
 * 페이지별 document.title 및 html[lang] 동적 업데이트.
 * @param titleKo 한국어 페이지 타이틀 (e.g. '사주 리밸런서')
 * @param titleEn 영어 페이지 타이틀 (e.g. 'Four Pillars Rebalancer')
 */
export function usePageMeta(titleKo: string, titleEn: string) {
  const { i18n } = useTranslation()
  const isEn = i18n.language.startsWith('en')

  useEffect(() => {
    const pageTitle = isEn ? titleEn : titleKo
    const siteName = isEn ? SITE_NAME_EN : SITE_NAME_KO
    document.title = `${pageTitle} — ${siteName}`
    document.documentElement.lang = isEn ? 'en' : 'ko'
  }, [isEn, titleKo, titleEn])
}
