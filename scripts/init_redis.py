import json
import os
import time

import redis


def load_catalog_to_redis():
    # Caminho para o arquivo JSON
    json_path = '/app/mock_products.json'

    # Configuração do Redis
    redis_host = os.environ.get('REDIS_HOST', 'redis')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))

    # Esperar o Redis estar disponível
    max_retries = 30
    retry_count = 0

    print('Tentando conectar ao Redis...')
    while retry_count < max_retries:
        try:
            # Conectar ao Redis
            r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            r.ping()
            break
        except redis.exceptions.ConnectionError:
            retry_count += 1
            print(
                f'Tentativa {retry_count}/{max_retries} - Redis ainda não disponível. Aguardando...'
            )
            time.sleep(1)

    if retry_count == max_retries:
        print('Não foi possível conectar ao Redis após várias tentativas.')
        return False

    try:
        # Verificar se a chave já existe
        if r.exists('catalog'):
            catalog_size = len(json.loads(r.get('catalog')))
            print(f'Catálogo já existe no Redis com {catalog_size} produtos. Pulando carregamento.')
            return True
            
        # Carregar o arquivo JSON apenas se a chave não existir
        with open(json_path, 'r') as f:
            products = json.load(f)

        # Salvar no Redis
        r.set('catalog', json.dumps(products))
        print(f'Catálogo carregado com sucesso! {len(products)} produtos adicionados.')
        return True
    except Exception as e:
        print(f'Erro ao carregar o catálogo: {e}')
        return False


if __name__ == '__main__':
    load_catalog_to_redis()
