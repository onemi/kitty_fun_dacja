from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class UserDonationDB(DonationCreate):
    create_date: datetime = datetime.utcnow()
    id: int

    class Config:
        orm_mode = True


class DonationDB(UserDonationDB):
    close_date: Optional[datetime] = None
    fully_invested: bool = False
    invested_amount: int = 0
    user_id: int
