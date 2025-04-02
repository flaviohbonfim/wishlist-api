import json
import logging
from typing import Any, Dict, List, Optional, Union

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

logger = logging.getLogger('uvicorn')

# Redis configuration
REDIS_HOST = 'localhost'  # Nome do serviço no docker-compose
REDIS_PORT = 6379
REDIS_DB = 0

# Initialize Redis connection pool
redis_pool = ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


async def get_redis_client() -> redis.Redis:
    """Retorna um cliente Redis conectado ao pool."""
    return redis.Redis(connection_pool=redis_pool)


async def get_key(key: str) -> Optional[str]:
    """Busca um valor no Redis pelo nome da chave."""
    try:
        client = await get_redis_client()
        return await client.get(key)
    except Exception as e:
        logger.error(f"Erro ao buscar chave '{key}' no Redis: {e}")
        return None


async def set_key(key: str, value: str, expiry: Optional[int] = None) -> bool:
    """
    Define um valor para uma chave no Redis.

    Args:
        key: Nome da chave
        value: Valor a ser armazenado
        expiry: Tempo de expiração em segundos (opcional)

    Returns:
        bool: True se a operação foi bem-sucedida, False caso contrário
    """
    try:
        client = await get_redis_client()
        await client.set(key, value, ex=expiry)
        return True
    except Exception as e:
        logger.error(f"Erro ao definir chave '{key}' no Redis: {e}")
        return False


async def delete_key(key: str) -> bool:
    """Remove uma chave do Redis."""
    try:
        client = await get_redis_client()
        await client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Erro ao excluir chave '{key}' no Redis: {e}")
        return False


async def set_json(key: str, data: Union[Dict, List], expiry: Optional[int] = None) -> bool:
    """Armazena um objeto JSON no Redis."""
    try:
        json_data = json.dumps(data)
        return await set_key(key, json_data, expiry)
    except Exception as e:
        logger.error(f"Erro ao armazenar JSON na chave '{key}': {e}")
        return False


async def get_json(key: str) -> Optional[Any]:
    """Recupera e desserializa um objeto JSON do Redis."""
    try:
        data = await get_key(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"Erro ao recuperar JSON da chave '{key}': {e}")
        return None


async def health_check() -> bool:
    """Verifica se a conexão com o Redis está funcionando."""
    try:
        client = await get_redis_client()
        return await client.ping()
    except Exception as e:
        logger.error(f'Erro na verificação de saúde do Redis: {e}')
        return False
