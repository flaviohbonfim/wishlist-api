from pydantic import BaseModel, ConfigDict


class WishlistSchema(BaseModel):
    product_id: int


class WishlistPublic(BaseModel):
    user_id: int
    product_id: int
    model_config = ConfigDict(from_attributes=True)


class WishlistProduct(BaseModel):
    product_id: int
    title: str
    price: float
    image: str
    review_score: float | None = None


class WishlistUserGroup(BaseModel):
    user_id: int
    products: list[WishlistProduct]


class WishlistList(BaseModel):
    wishlists: list[WishlistUserGroup]
