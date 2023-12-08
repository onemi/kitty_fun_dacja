from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation

UNIQUE_NAME_ERROR = 'Project with this name already exists!'
NOT_FOUND_ERROR = 'Project not found!'
EDIT_ERROR = 'Cannot edit closed project!'
INVESTED_ERROR = 'Project was invested into, cannot be deleted!'
AMOUNT_ERROR = 'The amount of investments in the projects is bigger than the requested amount.'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=400,
            detail=UNIQUE_NAME_ERROR,
        )


async def get_charity_project_if_patchable(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail=NOT_FOUND_ERROR,
        )
    if charity_project.close_date:
        raise HTTPException(
            status_code=400,
            detail=EDIT_ERROR,
        )
    return charity_project


async def get_charity_project_if_removable(
        project_id: int,
        session: AsyncSession,
) -> Union[CharityProject, None]:
    charity_project = await charity_project_crud.get(project_id, session)

    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail=NOT_FOUND_ERROR,
        )

    if charity_project.close_date:
        raise HTTPException(
            status_code=400,
            detail=INVESTED_ERROR,
        )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=INVESTED_ERROR,
        )

    if charity_project.invested_amount == 0:
        return charity_project


async def is_new_amount_less_than_invested_amount(
        invested_amount: int,
        new_amount: int,
) -> bool:
    if new_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail=AMOUNT_ERROR,
        )


async def confirm_create_date(
        date_to_check: datetime,
        session: AsyncSession,
        charity_project: bool = False,
        donation: bool = False,
) -> datetime:
    model_class = CharityProject if charity_project is True else Donation
    latest_project = await session.execute(
        select(model_class.create_date).where(
            and_(
                model_class.create_date >= date_to_check,
                model_class.create_date < date_to_check + timedelta(seconds=1)
            )
        )
    )
    latest_project_create_date = latest_project.scalar()
    if latest_project_create_date:
        return latest_project_create_date + timedelta(seconds=1)
    else:
        return date_to_check
