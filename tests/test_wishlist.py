from http import HTTPStatus

import pytest

from src.models.product import Product
from tests.factories import WishlistFactory


def test_create_wishlist(client, token, product: Product):
    response = client.post(
        '/wishlists/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_id': 1,
            'product_id': product.id,
        },
    )
    assert response.json() == {
        'user_id': 1,
        'product_id': 1,
    }
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_delete_wishlist(session, client, user, product, token):
    wishlist = WishlistFactory(user_id=user.id, product_id=product.id)

    session.add(wishlist)
    await session.commit()

    response = client.delete('/wishlists/', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Wishlist deleted'}


@pytest.mark.asyncio
async def test_delete_wishlist_product(session, client, product, user, token):
    wishlist = WishlistFactory(user_id=user.id, product_id=product.id)

    session.add(wishlist)
    await session.commit()

    response = client.delete(
        f'/wishlists/product/{wishlist.product_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Product deleted from wishlist'}


@pytest.mark.asyncio
async def test_create_wishlist_duplicated_product(session, user, product, client, token):
    wishlist = WishlistFactory(user_id=user.id, product_id=product.id)

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


@pytest.mark.asyncio
async def test_read_wishlists_with_wishlists(session, client, user, product, token):
    wishlist = WishlistFactory(user_id=user.id, product_id=product.id)

    session.add(wishlist)
    await session.commit()

    response = client.get(
        '/wishlists/',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_response = {
        'wishlists': [
            {
                'user_id': user.id,
                'products': [
                    {
                        'product_id': product.id,
                        'title': product.title,
                        'price': product.price,
                        'image': product.image,
                        'review_score': product.review_score,
                    }
                ],
            }
        ]
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response
