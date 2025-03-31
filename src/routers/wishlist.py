from collections import defaultdict
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wishlist import Wishlist
from src.schemas.wishlist import WishlistList, WishlistPublic, WishlistSchema

from ..core.db import get_session
from ..core.security import (
    get_current_user,
)
from ..models.user import User
from ..schemas.common import FilterPage, Message

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/wishlists', tags=['wishlists'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=WishlistPublic
)
async def create_wishlist(
    wishlist: WishlistSchema, session: Session, current_user: CurrentUser
):
    db_wishlist = Wishlist(
        user_id=current_user.id, product_id=wishlist.product_id
    )
    session.add(db_wishlist)
    try:
        await session.commit()
        await session.refresh(db_wishlist)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Este produto já está na sua lista de desejos.',
        )

    return db_wishlist


@router.get('/', response_model=WishlistList)
async def read_wishlist(
    session: Session,
    filter_users: Annotated[FilterPage, Query()],
    current_user: CurrentUser,
):
    query = await session.scalars(
        select(Wishlist)
        .where(Wishlist.user_id == current_user.id)
        .offset(filter_users.offset)
        .limit(filter_users.limit)
    )
    wishlists = query.all()

    wishlist_dict = defaultdict(list)

    for wishlist in wishlists:
        wishlist_dict[wishlist.user_id].append({
            'product_id': wishlist.product_id
        })

    grouped_wishlists = [
        {'user_id': user_id, 'products': products}
        for user_id, products in wishlist_dict.items()
    ]

    return {'wishlists': grouped_wishlists}


@router.delete('/', response_model=Message)
async def delete_wishlist(
    session: Session,
    current_user: CurrentUser,
):
    stmt = delete(Wishlist).where((Wishlist.user_id == current_user.id))

    await session.execute(stmt)

    await session.commit()

    return {'message': 'Wishlist deleted'}


@router.delete('/product/{prod_id}', response_model=Message)
async def delete_wishlist_product(
    prod_id: int,
    session: Session,
    current_user: CurrentUser,
):
    stmt = delete(Wishlist).where(
        (Wishlist.user_id == current_user.id)
        & (Wishlist.product_id == prod_id)
    )

    await session.execute(stmt)

    await session.commit()

    return {'message': 'Product deleted from wishlist'}
