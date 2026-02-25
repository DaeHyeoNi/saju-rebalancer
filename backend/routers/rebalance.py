import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import SajuCache
from schemas import RebalanceRequest, RebalanceResponse, RebalanceItem
from services.gemini_service import generate_rebalancing, stream_rebalancing

router = APIRouter(prefix="/api/rebalance", tags=["rebalance"])


@router.post("/analyze", response_model=RebalanceResponse)
def analyze_rebalance(req: RebalanceRequest, db: Session = Depends(get_db)):
    # 사주 풀이 조회
    entry: SajuCache | None = db.query(SajuCache).filter(SajuCache.id == req.saju_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="사주 데이터를 찾을 수 없습니다. 먼저 사주를 분석해 주세요.")

    portfolio_dicts = [item.model_dump() for item in req.portfolio_items]

    try:
        result = generate_rebalancing(
            saju_reading=entry.gemini_reading,
            portfolio_items=portfolio_dicts,
            additional_cash=req.additional_cash,
            user_preference=req.user_preference,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    rebalance_table = [RebalanceItem(**row) for row in result.get("rebalance_table", [])]

    return RebalanceResponse(
        rebalance_table=rebalance_table,
        narrative=result.get("narrative", ""),
    )


@router.post("/stream")
async def stream_rebalance(req: RebalanceRequest, db: Session = Depends(get_db)):
    """SSE 스트리밍: 생성 중 chunk 이벤트, 완료 시 done 이벤트를 반환."""
    entry: SajuCache | None = db.query(SajuCache).filter(SajuCache.id == req.saju_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="사주 데이터를 찾을 수 없습니다. 먼저 사주를 분석해 주세요.")

    portfolio_dicts = [item.model_dump() for item in req.portfolio_items]

    async def event_generator():
        try:
            async for event_type, data in stream_rebalancing(
                saju_reading=entry.gemini_reading,
                portfolio_items=portfolio_dicts,
                additional_cash=req.additional_cash,
                user_preference=req.user_preference,
            ):
                if event_type == "chunk":
                    yield f"data: {json.dumps({'type': 'chunk', 'text': data}, ensure_ascii=False)}\n\n"
                elif event_type == "done":
                    rebalance_items = [RebalanceItem(**row) for row in data.get("rebalance_table", [])]
                    result = RebalanceResponse(
                        rebalance_table=rebalance_items,
                        narrative=data.get("narrative", ""),
                    )
                    yield f"data: {json.dumps({'type': 'done', 'data': result.model_dump()}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'detail': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
