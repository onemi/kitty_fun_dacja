from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import confirm_create_date
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, UserDonationDB
from app.services.donation_logic import allocate_donations

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude={'close_date'},
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=UserDonationDB,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    create_date = await confirm_create_date(
        datetime.utcnow(),
        session,
        donation=True
    )
    new_donation = await donation_crud.create(
        donation,
        create_date=create_date,
        session=session,
        user=user,
    )
    pending_charity_projects = await charity_project_crud.get_pending(session)
    session.add_all(allocate_donations(new_donation, pending_charity_projects))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[UserDonationDB],
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    return await donation_crud.get_user_donations(session=session, user=user)
