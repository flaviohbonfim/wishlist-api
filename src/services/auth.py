from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import create_access_token, verify_password
from ..models.user import User


async def authenticate_user(email: str, password: str, session: AsyncSession) -> User | None:
    user = await session.scalar(select(User).where(User.email == email))
    if user and verify_password(password, user.password):
        return user
    return None


def generate_access_token(email: str) -> str:
    return create_access_token(data={'sub': email})
