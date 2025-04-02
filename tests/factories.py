import factory
import factory.fuzzy

from src.models.product import Product
from src.models.user import User
from src.models.wishlist import Wishlist


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class WishlistFactory(factory.Factory):
    class Meta:
        model = Wishlist

    user_id = 1
    product_id = 1


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = 1
    title = factory.fuzzy.FuzzyText(length=10)
    price = factory.fuzzy.FuzzyFloat(1.0, 100.0)
    image = 'https://example.com/image.jpg'
