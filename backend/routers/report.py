import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import RebalancingReport
from schemas import RebalancingReportData, PortfolioItem, RebalanceItem

router = APIRouter(prefix="/api", tags=["report"])


@router.get("/rebalancing-report/{uuid}", response_model=RebalancingReportData)
def get_report(uuid: str, db: Session = Depends(get_db)):
    report: RebalancingReport | None = (
        db.query(RebalancingReport).filter(RebalancingReport.uuid == uuid).first()
    )
    if not report:
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")

    return RebalancingReportData(
        saju_data=json.loads(report.saju_data),
        portfolio_items=[PortfolioItem(**item) for item in json.loads(report.portfolio_items)],
        rebalance_table=[RebalanceItem(**row) for row in json.loads(report.rebalance_table)],
        narrative=report.narrative,
        created_at=report.created_at.isoformat(),
    )
