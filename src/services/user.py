from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.common import FilterPage

from ..core.security import get_password_hash
from ..models.user import User
from ..schemas.user import UserSchema


def user_exists(db_user: User, user: UserSchema):
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )


async def create_user_service(user: UserSchema, session: AsyncSession) -> User:
    db_user = await session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )
    user_exists(db_user, user)

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_users_service(session: AsyncSession, filter_users: FilterPage) -> list[User]:
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )
    users = query.all()

    return {'users': users}


async def update_user_service(
    user_id: int, user: UserSchema, session: AsyncSession, current_user: User
) -> User:
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        await session.commit()
        await session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


async def delete_user_service(user_id: int, session: AsyncSession, current_user: User):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
