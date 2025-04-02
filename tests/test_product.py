from unittest.mock import AsyncMock, MagicMock, patch

import pybreaker
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import Product as ProductModel
from src.schemas.product import Product
from src.services.product import (
    fetch_product,
    get_product_from_cache,
    get_product_from_db,
    save_product_to_db,
)


@pytest.mark.asyncio
async def test_get_product_from_db_found(product_model):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = product_model
    mock_session.execute.return_value = mock_result

    result = await get_product_from_db(1, mock_session)

    assert result == product_model
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_product_from_db_not_found():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    result = await get_product_from_db(999, mock_session)

    assert result is None
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_save_product_to_db(product_schema):
    mock_session = AsyncMock(spec=AsyncSession)

    result = await save_product_to_db(product_schema, mock_session)

    assert isinstance(result, ProductModel)
    assert result.id == product_schema.id
    assert result.title == product_schema.title
    assert result.price == product_schema.price
    assert result.image == product_schema.image
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_product_from_db(product_model, product_schema):
    mock_session = AsyncMock(spec=AsyncSession)
    with patch('src.services.product.get_product_from_db', return_value=product_model):
        result = await fetch_product(1, mock_session)

        assert result.id == product_schema.id
        assert result.title == product_schema.title
        assert result.price == product_schema.price
        assert result.image == product_schema.image


@pytest.mark.asyncio
async def test_fetch_product_from_api(product_schema):
    mock_session = AsyncMock(spec=AsyncSession)

    with (
        patch('src.services.product.get_product_from_db', return_value=None),
        patch('src.services.product.circuit_breaker.call', return_value=product_schema),
        patch('src.services.product.save_product_to_db'),
    ):
        result = await fetch_product(1, mock_session)

        assert result == product_schema


@pytest.mark.asyncio
async def test_fetch_product_circuit_breaker_fallback(product_schema):
    mock_session = AsyncMock(spec=AsyncSession)

    with (
        patch('src.services.product.get_product_from_db', return_value=None),
        patch(
            'src.services.product.circuit_breaker.call', side_effect=pybreaker.CircuitBreakerError()
        ),
        patch('src.services.product.get_product_from_cache', return_value=product_schema),
        patch('src.services.product.save_product_to_db'),
    ):
        result = await fetch_product(1, mock_session)

        assert result == product_schema


@pytest.mark.asyncio
async def test_fetch_product_all_sources_fail():
    mock_session = AsyncMock(spec=AsyncSession)

    with (
        patch('src.services.product.get_product_from_db', return_value=None),
        patch(
            'src.services.product.circuit_breaker.call', side_effect=pybreaker.CircuitBreakerError()
        ),
        patch('src.services.product.get_product_from_cache', return_value=None),
    ):
        result = await fetch_product(1, mock_session)

        assert result is None


@pytest.mark.asyncio
async def test_get_product_from_cache_found(product_data):
    catalog = [product_data]

    with patch('src.services.product.get_json', return_value=catalog):
        result = await get_product_from_cache(1)

        assert isinstance(result, Product)
        assert result.id == product_data['id']
        assert result.title == product_data['title']


@pytest.mark.asyncio
async def test_get_product_from_cache_not_found():
    catalog = [
        {'id': 2, 'title': 'Other Product', 'price': 10.0, 'image': 'http://example.com/other.jpg'}
    ]

    with patch('src.services.product.get_json', return_value=catalog):
        result = await get_product_from_cache(1)

        assert result is None


@pytest.mark.asyncio
async def test_get_product_from_cache_no_catalog():
    with patch('src.services.product.get_json', return_value=None):
        result = await get_product_from_cache(1)

        assert result is None


@pytest.mark.asyncio
async def test_get_product_from_cache_exception():
    with patch('src.services.product.get_json', side_effect=Exception('Redis error')):
        result = await get_product_from_cache(1)

        assert result is None
