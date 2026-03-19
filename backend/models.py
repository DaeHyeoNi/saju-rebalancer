from datetime import datetime, date
from sqlalchemy import Date, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class SajuCache(Base):
    __tablename__ = "saju_cache"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    birth_hour: Mapped[str | None] = mapped_column(String(10), nullable=True)  # 시진 (e.g. 자시, 축시)
    gender: Mapped[str] = mapped_column(String(5), nullable=False)  # 남 / 여
    raw_saju_data: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    gemini_reading: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("birth_date", "birth_hour", "gender", name="uq_saju_key"),
    )


class RebalancingReport(Base):
    __tablename__ = "rebalancing_report"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False, index=True)
    saju_data: Mapped[str] = mapped_column(Text)       # JSON {pillars, reading}
    portfolio_items: Mapped[str] = mapped_column(Text)  # JSON array
    rebalance_table: Mapped[str] = mapped_column(Text)  # JSON array
    narrative: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CeoCache(Base):
    __tablename__ = "ceo_cache"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(100), nullable=False)
    ceo_name: Mapped[str] = mapped_column(String(100), nullable=False)
    ceo_birth_date: Mapped[str] = mapped_column(String(20), nullable=False)  # "YYYY-MM-DD" 또는 "YYYY"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CeoFeedback(Base):
    __tablename__ = "ceo_feedback"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    cached_ceo_name: Mapped[str] = mapped_column(String(100))
    cached_birth_date: Mapped[str] = mapped_column(String(20))
    reported_correct_birth_date: Mapped[str | None] = mapped_column(String(20), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
