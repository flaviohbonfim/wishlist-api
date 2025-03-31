from collections import defaultdict
from http import HTTPStatus

import pytest

from src.schemas.wishlist import WishlistPublic
from tests.factories import WishlistFactory


def test_create_wishlist(client, token):
    response = client.post(
        '/wishlists/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_id': 1,
            'product_id': 1,
        },
    )
    assert response.json() == {
        'user_id': 1,
        'product_id': 1,
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_delete_wishlist(session, client, user, token):
    wishlist = WishlistFactory(user_id=user.id)

    session.add(wishlist)
    await session.commit()

    response = client.delete(
        '/wishlists/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Wishlist deleted'}


@pytest.mark.asyncio
async def test_delete_wishlist_product(session, client, user, token):
    wishlist = WishlistFactory(user_id=user.id)

    session.add(wishlist)
    await session.commit()

    response = client.delete(
        f'/wishlists/product/{wishlist.product_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Product deleted from wishlist'}


@pytest.mark.asyncio
async def test_create_wishlist_duplicated_product(
    session, user, client, token
):
    wishlist = WishlistFactory(user_id=user.id)

    session.add(wishlist)
    await session.commit()

    response = client.post(
        '/wishlists/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_id': 1,
            'product_id': 1,
        },
    )
    assert response.json() == {
        'detail': 'Este produto já está na sua lista de desejos.',
    }

    assert response.status_code == HTTPStatus.CONFLICT


def test_read_wishlists(client, token):
    response = client.get(
        '/wishlists/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'wishlists': []}


def test_read_wishlists_with_wishlists(client, wishlist, token):
    wishlist_schema = WishlistPublic.model_validate(wishlist).model_dump()
    response = client.get(
        '/wishlists/',
        headers={'Authorization': f'Bearer {token}'},
    )
    wishlist_dict = defaultdict(list)

    for wlist in [wishlist_schema]:
        wishlist_dict[wlist['user_id']].append({
            'product_id': wlist['product_id']
        })

    grouped_wishlists = [
        {'user_id': user_id, 'products': products}
        for user_id, products in wishlist_dict.items()
    ]

    assert response.json() == {'wishlists': grouped_wishlists}
    assert response.status_code == HTTPStatus.OK
