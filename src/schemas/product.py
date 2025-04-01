from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    price: float
    image: str
    brand: str
    reviewScore: Optional[float]


MOCK_PRODUCTS = {
    1: Product(
        id=1,
        title='Drug Work',
        price=4183.54,
        image='https://images.unsplash.com/photo-1613068687893-5e85b4638b56?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTZ8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Castillo-Williams',
        reviewScore=4.3,
    ),
    2: Product(
        id=2,
        title='Talk Gun',
        price=268.18,
        image='https://images.unsplash.com/photo-1565630916779-e303be97b6f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTZ8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Garcia Inc',
        reviewScore=2.2,
    ),
    3: Product(
        id=3,
        title='Unit Forward',
        price=3355.28,
        image='https://images.unsplash.com/photo-1593259037198-c720f4420d7f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTd8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Mayer-Roberts',
        reviewScore=3.0,
    ),
    4: Product(
        id=4,
        title='Live House',
        price=3022.19,
        image='https://images.unsplash.com/photo-1533867617858-e7b97e060509?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTd8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Mckay-Sullivan',
        reviewScore=4.4,
    ),
    5: Product(
        id=5,
        title='Enter Official',
        price=4428.88,
        image='https://images.unsplash.com/photo-1498049794561-7780e7231661?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTd8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Hall Inc',
        reviewScore=3.1,
    ),
    6: Product(
        id=6,
        title='Line Manage',
        price=2542.5,
        image='https://images.unsplash.com/photo-1567016546367-c27a0d56712e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTh8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Williamson-Gordon',
        reviewScore=None,  # Review score nulo
    ),
    7: Product(
        id=7,
        title='Want Tough',
        price=1712.46,
        image='https://images.unsplash.com/photo-1573920011462-eb3003086611?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTh8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Young PLC',
        reviewScore=2.2,
    ),
    8: Product(
        id=8,
        title='Professor Certainly',
        price=3648.55,
        image='https://images.unsplash.com/photo-1602810316481-0d5d7401737a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTh8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Brown-Patterson',
        reviewScore=None,  # Review score nulo
    ),
    9: Product(
        id=9,
        title='Example Series',
        price=2545.31,
        image='https://images.unsplash.com/photo-1590548784585-643d2b9f2925?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTh8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Wilson, Williams and Munoz',
        reviewScore=4.4,
    ),
    10: Product(
        id=10,
        title='Add Various',
        price=4868.57,
        image='https://images.unsplash.com/photo-1563662931846-29b0af7443ff?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Mjk1Mzd8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDMxNjgzOTl8&ixlib=rb-4.0.3&q=80&w=1080',
        brand='Costa LLC',
        reviewScore=1.5,
    ),
}
