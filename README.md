# Wishlist API

API para gerenciamento de listas de produtos favoritos de usuários, permitindo que eles adicionem, visualizem e removam produtos de suas wishlists.

## Tecnologias Utilizadas

- Python 3.13
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Docker
- Poetry
- Alembic
- JWT 
- Circuit Breaker
- Redis (Cache)

## Requisitos

### Para execução local
- Python 3.13+
- Poetry
- SQLite ou PostgreSQL
- Redis

### Para execução com Docker
- Docker
- Docker Compose

## Como executar o projeto

### Usando Docker

1. Clone o repositório:
```bash
git clone https://github.com/flaviohbonfim/wishlist-api.git
cd wishlist-api
```

2. Execute o projeto com Docker Compose:
```bash
docker-compose up -d
```

3. A API estará disponível em: http://localhost:8000

4. Para visualizar os logs:
```bash
docker-compose logs -f wishlist_api
```

5. Para parar os containers:
```bash
docker-compose down
```

### Localmente

1. Clone o repositório:
```bash
git clone https://github.com/flaviohbonfim/wishlist-api.git
cd wishlist-api
```

2. Instale as dependências com Poetry:
```bash
poetry install
```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
DATABASE_URL="sqlite+aiosqlite:///wishlist.db"
SECRET_KEY="sua-chave-secreta"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0
PRODUCTS_API_URL="http://challenge-api.luizalabs.com/api/product"
```

4. Execute as migrações do banco de dados:
```bash
poetry run alembic upgrade head
```

5. Inicie a aplicação:
```bash
poetry run uvicorn src.app:app --reload
```

6. A API estará disponível em: http://localhost:8000

## Documentação da API

Após iniciar a aplicação, você pode acessar a documentação interativa da API em:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Funcionalidades

- **Autenticação**: Registro e login de usuários com JWT
- **Usuários**: CRUD completo de usuários
- **Wishlist**: Adicionar, listar e remover produtos da lista de desejos
- **Produtos**: Integração com API externa para busca de produtos
- **Cache com Redis**: Armazenamento em cache de dados frequentemente acessados para melhorar a performance

## Testes

Para executar os testes:

```bash
poetry run task test
```

## Linting e Formatação

```bash
# Verificar código
poetry run task lint

# Formatar código
poetry run task format
```

## Estrutura do Projeto
```
wishlist-api/
├── src/                     # Código fonte da aplicação
│   ├── app.py               # Ponto de entrada da aplicação
│   ├── core/                # Módulos centrais (autenticação, banco de dados, etc.)
│   ├── models/              # Modelos do banco de dados
│   ├── routers/             # Rotas da API
│   ├── schemas/             # Esquemas Pydantic
│   └── services/            # Serviços e lógica de negócio
├── scripts/                 # Scripts de apoio ao projeto (init)
├── tests/                   # Testes automatizados
└── migrations/              # Migrações do banco de dados
```
## Considerações sobre o teste

Devido ao cenário descrito para esse teste (_API de produtos fora do ar_), foi implementado um **Circuit Breaker** para ter opção de controle e fallback na busca dos produtos durante a criação de uma **Wishlist**. O fallback proposto foi através de busca das informações dos produtos no cache (**Redis**). Em um projeto real, provavelmente a estratégia seria diferente, pois geralmente o cache é implementado como primeira opção de busca, pois é mais rápido e menos custoso. Porém, para esse teste, foi implementado de forma simples, pois o objetivo era apenas demonstrar o uso do **Circuit Breaker**.