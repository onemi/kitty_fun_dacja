from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )
    description: str = Field(
        ...,
        min_length=1,
    )
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    close_date: Optional[datetime] = None
    create_date: datetime = datetime.utcnow()
    fully_invested: bool = False
    id: int
    invested_amount: int = 0

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
    )
    description: Optional[str] = Field(
        None,
        min_length=1,
    )
    full_amount: Optional[PositiveInt]
