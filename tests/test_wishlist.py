from http import HTTPStatus

import pytest

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
