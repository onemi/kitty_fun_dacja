from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

REPR = (
    'Requested amount: {full_amount}. '
    'Invested amount: {invested_amount}. '
    'Create date: {create_date}. '
    'Closed : {fully_invested}. '
    'Close date: {close_date}. '
)


class Investment(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, default=None, nullable=True)

    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    def __repr__(self) -> str:
        return REPR.format(
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            create_date=self.create_date,
            fully_invested=self.fully_invested,
            close_date=self.close_date,
        )
