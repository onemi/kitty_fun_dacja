from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    confirm_create_date,
    get_charity_project_if_patchable,
    get_charity_project_if_removable,
    is_new_amount_less_than_invested_amount
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.donation_logic import allocate_donations

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    create_date = await confirm_create_date(
        datetime.utcnow(),
        session,
        charity_project=True
    )
    new_project = await charity_project_crud.create(
        charity_project,
        create_date=create_date,
        session=session,
    )
    pending_donations = await donation_crud.get_pending(session)
    session.add_all(allocate_donations(new_project, pending_donations))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await get_charity_project_if_removable(
        project_id, session
    )
    if charity_project:
        await charity_project_crud.remove(charity_project, session)
        return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await get_charity_project_if_patchable(
        charity_project_id, session
    )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await is_new_amount_less_than_invested_amount(
            charity_project.invested_amount, obj_in.full_amount
        )
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    pending_donations = await donation_crud.get_pending(session)
    session.add_all(allocate_donations(charity_project, pending_donations))
    await session.commit()
    await session.refresh(charity_project)
    return charity_project
