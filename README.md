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

## Requisitos

### Para execução local
- Python 3.13+
- Poetry
- SQLite ou PostgreSQL

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
├── tests/                   # Testes automatizados
└── migrations/              # Migrações do banco de dados
```
## Circuit Breaker

O projeto usa o padrão Circuit Breaker para tornar a comunicação com APIs externas mais resiliente. Se houver falhas repetidas, o sistema reage de forma inteligente, evitando sobrecarregar serviços que estão fora do ar e garantindo uma degradação controlada.