from dataclasses import asdict

import pytest
from sqlalchemy import select

from src.models.product import Product
from src.models.user import User
from src.models.wishlist import Wishlist


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='alice', password='secret', email='teste@test')
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'wishlists': [],
    }


@pytest.mark.asyncio
async def test_create_wishlist(session, user: User, product: Product, mock_db_time):
    with mock_db_time(model=Wishlist) as time:
        wishlist = Wishlist(
            user_id=user.id,
            product_id=product.id,
        )
        session.add(wishlist)
        await session.commit()
        await session.refresh(wishlist)

    wishlist = await session.scalar(select(Wishlist))

    assert asdict(wishlist) == {
        'id': 1,
        'user_id': 1,
        'product_id': 1,
        'created_at': time,
    }


@pytest.mark.asyncio
async def test_user_wishlist_relationship(session, user: User, product: Product):
    wishlist = Wishlist(
        user_id=user.id,
        product_id=product.id,
    )

    session.add(wishlist)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.wishlists == [wishlist]
