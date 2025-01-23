import json
from typing import List
import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        """
        Represents a user's cart with associated products and total cost.
        """
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        """
        Load cart data from a dictionary representation.
        """
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[products.get_product(item_id) for item_id in json.loads(data['contents'])],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """
    Retrieve a user's cart as a list of Product objects.
    """
    # Fetch cart details from the DAO layer
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    products_in_cart = []
    for cart_detail in cart_details:
        try:
            # Parse the JSON string safely
            content_ids = json.loads(cart_detail['contents'])
        except json.JSONDecodeError:
            # If there's an issue with the data, skip this cart entry
            continue
        
        # Retrieve Product objects for the IDs in the cart
        for product_id in content_ids:
            product = products.get_product(product_id)
            if product:
                products_in_cart.append(product)

    return products_in_cart


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the entire cart for a user.
    """
    dao.delete_cart(username)
