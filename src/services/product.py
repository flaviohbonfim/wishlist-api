import logging
import os
import ssl
from http import HTTPStatus
from typing import Dict, Optional

import aiohttp
import pybreaker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.circuit_breaker import AsyncCircuitBreaker
from src.core.redis import get_json
from src.models.product import Product as ProductModel
from src.schemas.product import Product

from .settings import Settings

logger = logging.getLogger('uvicorn')


circuit_breaker = AsyncCircuitBreaker(fail_max=3, reset_timeout=10)

# Configuração do SSL para ignorar erros de certificado
# problema com host 'challenge-api.luizalabs.com'
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

PRODUCTS_API_URL = Settings().PRODUCTS_API_URL


async def get_product_from_db(product_id: int, session: AsyncSession) -> Optional[ProductModel]:
    """Busca o produto no banco de dados pelo ID."""
    query = select(ProductModel).where(ProductModel.id == product_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def save_product_to_db(product: Product, session: AsyncSession) -> ProductModel:
    """Salva o produto no banco de dados."""
    db_product = ProductModel(
        id=product.id, title=product.title, price=product.price, image=product.image
    )
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    logger.info(f'Produto {product.id} salvo no banco de dados')
    return db_product


async def fetch_product(product_id: int, session: AsyncSession) -> Optional[Product]:
    """
    Busca um produto pelo ID seguindo a ordem:
    1. Banco de dados
    2. API externa
    3. Produtos do cache Redis (fallback)
    """
    db_product = await get_product_from_db(product_id, session)
    if db_product:
        logger.info(f'Produto {product_id} encontrado no banco de dados')
        return Product(
            id=db_product.id, title=db_product.title, price=db_product.price, image=db_product.image
        )

    url = f'{PRODUCTS_API_URL}/{product_id}/'
    logger.info(
        f'Produto não encontrado no banco. Tentando buscar o produto {product_id} na API...'
    )
    try:
        api_product = await circuit_breaker.call(async_fetch_product, url)
        await save_product_to_db(api_product, session)
        return api_product
    except pybreaker.CircuitBreakerError:
        logger.info('Circuit Breaker ativado! Ativando fallback para produtos em cache.')
        logger.error(
            f'Circuit Breaker foi acionado após {circuit_breaker.failure_count} falhas consecutivas'
        )

        product_from_cache = await get_product_from_cache(product_id)

        if product_from_cache:
            logger.info(f'Salvando produto do cache {product_id} no banco...')
            await save_product_to_db(product_from_cache, session)

        return product_from_cache
    except Exception as e:
        logger.error(f'Erro ao buscar o produto {product_id}: {e}')
        return None


async def async_fetch_product(url: str) -> Product:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, ssl=ssl_context, timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            if 'text/html' in response.content_type:
                raise Exception(f'API fora do ar: {url}')

            if response.status == HTTPStatus.NOT_FOUND:
                raise Exception(f'Produto não encontrado: {url}')
            elif response.status != HTTPStatus.OK:
                raise Exception(f'Erro na resposta: {url}')

            try:
                data: Dict = await response.json()
                if not data or 'id' not in data:
                    raise Exception('Dados inválidos recebidos')
                return Product(**data)
            except aiohttp.ContentTypeError:
                raise Exception(f'Erro de decodificação: {url}')


async def get_product_from_cache(product_id: int) -> Optional[Product]:
    """
    Busca um produto no cache Redis pelo ID.

    Args:
        product_id: ID do produto a ser buscado

    Returns:
        Product: Instância do modelo Product ou None se não encontrado
    """
    try:
        catalog = await get_json('catalog')
        if not catalog:
            logger.warning('Catálogo não encontrado no Redis')
            return None

        mock_product_dict = next(
            (product for product in catalog if product.get('id') == product_id), None
        )

        if mock_product_dict:
            logger.info(f'Produto {product_id} encontrado no cache Redis')
            return Product(**mock_product_dict)

        logger.info(f'Produto {product_id} não encontrado no cache Redis')
        return None
    except Exception as e:
        logger.error(f'Erro ao buscar produto {product_id} do cache: {e}')
