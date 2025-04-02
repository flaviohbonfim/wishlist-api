from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    price: float
    image: str
    brand: Optional[str] = None
    reviewScore: Optional[float] = None
