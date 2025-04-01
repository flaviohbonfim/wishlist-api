from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import table_registry


@table_registry.mapped_as_dataclass
class Wishlist:
    __tablename__ = 'wishlists'
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='uq_user_product'),)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
