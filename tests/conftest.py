from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from src.app import app
from src.core.db import get_session
from src.core.security import get_password_hash
from src.models import table_registry
from src.models.product import Product as ProductModel
from src.schemas.product import Product
from tests.factories import ProductFactory, UserFactory, WishlistFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def wishlist(session, user, product):
    wishlist = WishlistFactory(user_id=user.id, product_id=product.id)

    session.add(wishlist)
    await session.commit()
    await session.refresh(wishlist)

    return wishlist


@pytest_asyncio.fixture
async def product(session):
    product = ProductFactory()

    session.add(product)
    await session.commit()
    await session.refresh(product)

    return product


@pytest.fixture
def product_data():
    return {
        'id': 1,
        'title': 'Test Product',
        'price': 99.99,
        'image': 'http://example.com/image.jpg',
        'review_score': 4.5,
    }


@pytest.fixture
def product_schema(product_data):
    return Product(**product_data)


@pytest.fixture
def product_model(product_data):
    return ProductModel(**product_data)
