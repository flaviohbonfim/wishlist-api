from collections import defaultdict
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import Product
from src.models.wishlist import Wishlist
from src.schemas.common import FilterPage, Message
from src.schemas.wishlist import WishlistList, WishlistPublic, WishlistSchema

from ..services.product import fetch_product


async def create_wishlist_service(
    wishlist: WishlistSchema, session: AsyncSession, user_id: int
) -> WishlistPublic:
    product = await fetch_product(wishlist.product_id, session)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado.')

    db_wishlist = Wishlist(user_id=user_id, product_id=wishlist.product_id)
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


async def read_wishlist_service(
    session: AsyncSession, filter_users: FilterPage, user_id: int
) -> WishlistList:
    query = await session.execute(
        select(Wishlist, Product)
        .join(Product, Wishlist.product_id == Product.id)
        .where(Wishlist.user_id == user_id)
        .offset(filter_users.offset)
        .limit(filter_users.limit)
    )
    results = query.all()

    wishlist_dict = defaultdict(list)
    for wishlist, product in results:
        wishlist_dict[wishlist.user_id].append({
            'product_id': product.id,
            'title': product.title,
            'price': product.price,
            'image': product.image,
        })

    grouped_wishlists = [
        {'user_id': user_id, 'products': products} for user_id, products in wishlist_dict.items()
    ]

    return {'wishlists': grouped_wishlists}


async def delete_wishlist_service(session: AsyncSession, user_id: int) -> Message:
    stmt = delete(Wishlist).where(Wishlist.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Wishlist deleted'}


async def delete_wishlist_product_service(
    prod_id: int, session: AsyncSession, user_id: int
) -> Message:
    stmt = delete(Wishlist).where((Wishlist.user_id == user_id) & (Wishlist.product_id == prod_id))
    await session.execute(stmt)
    await session.commit()
    return {'message': 'Product deleted from wishlist'}
