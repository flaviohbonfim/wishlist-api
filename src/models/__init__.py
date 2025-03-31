from sqlalchemy.orm import registry

table_registry = registry()

from src.models.user import User  # noqa: E402
from src.models.wishlist import Wishlist  # noqa: E402

__all__ = ['User', 'Wishlist']
