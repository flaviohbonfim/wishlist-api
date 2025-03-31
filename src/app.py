import asyncio
import sys

from fastapi import FastAPI

from .routers import auth, user, wishlist

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wishlist.router)
