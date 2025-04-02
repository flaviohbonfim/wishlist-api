from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_session
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.common import FilterPage, Message
from ..schemas.wishlist import WishlistList, WishlistPublic, WishlistSchema
from ..services.wishlist import (
    create_wishlist_service,
    delete_wishlist_product_service,
    delete_wishlist_service,
    read_wishlist_service,
)

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/wishlists', tags=['wishlists'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=WishlistPublic)
async def create_wishlist(wishlist: WishlistSchema, session: Session, current_user: CurrentUser):
    return await create_wishlist_service(wishlist, session, current_user.id)


@router.get('/', response_model=WishlistList)
async def read_wishlist(
    session: Session,
    filter_users: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    return await read_wishlist_service(session, filter_users, current_user.id)


@router.delete('/', response_model=Message)
async def delete_wishlist(session: Session, current_user: CurrentUser):
    return await delete_wishlist_service(session, current_user.id)


@router.delete('/product/{prod_id}', response_model=Message)
async def delete_wishlist_product(prod_id: int, session: Session, current_user: CurrentUser):
    return await delete_wishlist_product_service(prod_id, session, current_user.id)
