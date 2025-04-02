import asyncio
import sys

from fastapi import FastAPI

from .routers import auth, user, wishlist

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(
    title='Wishlist API',
    description='API para controle de produtos favoritos dos clientes.',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wishlist.router)
