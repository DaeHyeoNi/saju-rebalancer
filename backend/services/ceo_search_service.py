"""CEO 정보 조회 서비스 — DB 캐시 우선, 캐시 미스 시 DuckDuckGo + Gemini 파싱."""
from __future__ import annotations

from sqlalchemy.orm import Session

from models import CeoCache
from services.gemini_service import _call, _extract_json


def get_or_search_ceo(db: Session, ticker: str, company_name: str | None = None) -> CeoCache:
    """ticker에 해당하는 CEO 정보를 DB 캐시에서 조회하거나, 없으면 웹 검색 후 저장.

    Args:
        db: SQLAlchemy DB 세션.
        ticker: 종목 코드 (예: "TSLA", "005930").

    Returns:
        CeoCache ORM 객체.

    Raises:
        RuntimeError: DuckDuckGo 검색 또는 Gemini 파싱에 실패한 경우.
    """
    ticker_upper = ticker.upper()

    # 1. DB 캐시 조회
    cached = db.query(CeoCache).filter(CeoCache.ticker == ticker_upper).first()
    if cached:
        # 캐시에 년도만 저장된 경우 전체 날짜 재검색 시도
        if "-" not in cached.ceo_birth_date:
            full_date = _retry_search_full_birthdate(cached.ceo_name, cached.company_name)
            if full_date:
                cached.ceo_birth_date = full_date
                db.commit()
                db.refresh(cached)
        return cached

    # 2. 캐시 미스 → 웹 검색 + Gemini 파싱
    # 한국 주식은 종목코드보다 회사명으로 검색하는 게 훨씬 정확함
    search_keyword = company_name or ticker_upper
    info = _search_ceo_info(search_keyword)

    entry = CeoCache(
        ticker=ticker_upper,
        company_name=info["company_name"],
        ceo_name=info["ceo_name"],
        ceo_birth_date=info["ceo_birth_date"],
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def _search_ceo_info(keyword: str) -> dict[str, str]:
    """DuckDuckGo로 CEO 정보를 검색하고 Gemini로 파싱하여 반환.

    Args:
        ticker: 종목 코드 (대문자).

    Returns:
        {"company_name": str, "ceo_name": str, "ceo_birth_date": str}

    Raises:
        RuntimeError: 검색 결과가 없거나 Gemini 파싱 실패 시.
    """
    try:
        from ddgs import DDGS
    except ImportError as exc:
        raise RuntimeError("ddgs 패키지가 설치되지 않았습니다.") from exc

    # 두 가지 쿼리로 검색해 결과를 합산 (CEO 이름+생년월일 정보 확보율 향상)
    queries = [
        f"{keyword} CEO birthday born year",
        f"{keyword} CEO wikipedia birthdate",
    ]
    snippets: list[str] = []

    try:
        with DDGS() as ddgs:
            for query in queries:
                for r in ddgs.text(query, max_results=4):
                    title = r.get("title", "")
                    body = r.get("body", "")
                    if title or body:
                        snippets.append(f"{title}\n{body}".strip())
    except Exception as exc:
        raise RuntimeError(f"DuckDuckGo 검색 실패: {exc}") from exc

    if not snippets:
        raise RuntimeError(f"'{keyword}'에 대한 검색 결과가 없습니다.")

    search_text = "\n\n".join(snippets)

    prompt = (
        f"아래 검색 결과에서 {keyword}의 CEO(대표이사) 이름과 생년월일을 추출하세요.\n"
        f"JSON으로만 응답하세요 (마크다운 코드블록 포함):\n"
        '```json\n'
        '{"company_name": "회사명", "ceo_name": "CEO 이름", "ceo_birth_date": "YYYY-MM-DD 또는 YYYY"}\n'
        '```\n\n'
        f"검색 결과:\n{search_text}\n\n"
        "주의: 제공된 검색 결과에 있는 정보만 사용하세요. 추측하거나 창작하지 마세요. "
        "생년월일을 알 수 없으면 연도만 'YYYY' 형식으로 응답하고, "
        "회사명이나 CEO 이름을 특정할 수 없으면 빈 문자열로 응답하세요."
    )

    try:
        raw = _call(prompt)
        parsed = _extract_json(raw)
    except Exception as exc:
        raise RuntimeError(f"Gemini CEO 정보 파싱 실패: {exc}") from exc

    if not parsed.get("ceo_name"):
        raise RuntimeError(f"'{keyword}' CEO 이름을 검색 결과에서 찾을 수 없습니다.")
    if not parsed.get("ceo_birth_date"):
        raise RuntimeError(f"'{keyword}' CEO 생년월일을 검색 결과에서 찾을 수 없습니다.")

    result = {
        "company_name": parsed.get("company_name") or keyword,
        "ceo_name": parsed["ceo_name"],
        "ceo_birth_date": parsed["ceo_birth_date"],
    }

    # 년도만 찾은 경우 CEO 이름으로 재검색해 전체 생년월일 확보 시도
    if "-" not in result["ceo_birth_date"]:
        full_date = _retry_search_full_birthdate(result["ceo_name"], result["company_name"])
        if full_date:
            result["ceo_birth_date"] = full_date

    return result


def _retry_search_full_birthdate(ceo_name: str, company_name: str) -> str | None:
    """CEO 이름으로 재검색하여 전체 생년월일(YYYY-MM-DD) 확보를 시도.

    Args:
        ceo_name: CEO 이름.
        company_name: 회사명 (검색 품질 향상용).

    Returns:
        YYYY-MM-DD 형식 문자열, 실패 시 None.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        return None

    queries = [
        f"{ceo_name} date of birth month day",
        f"{ceo_name} {company_name} birthday wikipedia",
        f"{ceo_name} born 생년월일",
    ]
    snippets: list[str] = []

    try:
        with DDGS() as ddgs:
            for query in queries:
                for r in ddgs.text(query, max_results=3):
                    title = r.get("title", "")
                    body = r.get("body", "")
                    if title or body:
                        snippets.append(f"{title}\n{body}".strip())
    except Exception:
        return None

    if not snippets:
        return None

    search_text = "\n\n".join(snippets)

    prompt = (
        f"아래 검색 결과에서 {ceo_name}의 정확한 생년월일(월·일 포함)을 추출하세요.\n"
        f"JSON으로만 응답하세요 (마크다운 코드블록 포함):\n"
        '```json\n'
        '{"ceo_birth_date": "YYYY-MM-DD"}\n'
        '```\n\n'
        f"검색 결과:\n{search_text}\n\n"
        "주의: 제공된 검색 결과에 있는 정보만 사용하세요. 추측하거나 창작하지 마세요. "
        "월·일을 포함한 정확한 날짜를 찾지 못하면 빈 문자열로 응답하세요."
    )

    try:
        raw = _call(prompt)
        parsed = _extract_json(raw)
        date_str = parsed.get("ceo_birth_date", "")
        # YYYY-MM-DD 형식이고 월·일이 실제로 있는 경우만 반환
        if date_str and "-" in date_str and len(date_str) >= 8:
            return date_str
    except Exception:
        pass

    return None
