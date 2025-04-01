import logging
import ssl
from http import HTTPStatus
from typing import Dict, Optional

import aiohttp
import pybreaker

from src.core.circuit_breaker import AsyncCircuitBreaker
from src.schemas.product import MOCK_PRODUCTS, Product

logger = logging.getLogger('uvicorn')


circuit_breaker = AsyncCircuitBreaker(fail_max=3, reset_timeout=10)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def fetch_product(product_id: int) -> Optional[Product]:
    url = f'http://challenge-api.luizalabs.com/api/product/{product_id}/'
    logger.info(f'Tentando buscar o produto {product_id}...')
    try:
        response = await circuit_breaker.call(async_fetch_product, url)
        return response
    except pybreaker.CircuitBreakerError:
        logger.info('Circuit Breaker ativado! Ativando fallback para produtos mockados.')
        logger.error(
            f'Circuit Breaker foi acionado após {circuit_breaker.failure_count} falhas consecutivas'
        )
        return MOCK_PRODUCTS.get(product_id, None)
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
