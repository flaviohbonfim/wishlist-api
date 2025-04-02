from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import table_registry


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    image: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
