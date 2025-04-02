from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_session
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.common import FilterPage, Message
from ..schemas.user import UserList, UserPublic, UserSchema
from ..services.user import (
    create_user_service,
    delete_user_service,
    get_users_service,
    update_user_service,
)

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):
    return await create_user_service(user, session)


@router.get('/', response_model=UserList)
async def read_users(session: Session, filter_users: Annotated[FilterPage, Query()]):
    return await get_users_service(session, filter_users)


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    return await update_user_service(user_id, user, session, current_user)


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    return await delete_user_service(user_id, session, current_user)
