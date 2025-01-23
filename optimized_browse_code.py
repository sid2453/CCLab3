from products import dao
from typing import List


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        """
        Represents a product with an ID, name, description, cost, and quantity.
        """
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> 'Product':
        """
        Creates a Product instance from a dictionary.
        """
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default qty to 0 if not provided
        )


def list_products() -> List[Product]:
    """
    Retrieves a list of all products from the database.
    """
    products_data = dao.list_products()
    return [Product.load(product) for product in products_data]  # Using list comprehension for efficiency


def get_product(product_id: int) -> Product:
    """
    Retrieves a product by its ID from the database.
    """
    product_data = dao.get_product(product_id)
    return Product.load(product_data) if product_data else None  # Handle None if product not found


def add_product(product: dict):
    """
    Adds a new product to the database.
    """
    if 'id' not in product or 'name' not in product or 'cost' not in product:
        raise ValueError('Product must contain id, name, and cost')  # Validate input data
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """
    Updates the quantity of a product in the database.
    """
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    if not dao.get_product(product_id):  # Ensure the product exists before updating
        raise ValueError(f'Product with ID {product_id} does not exist')
    dao.update_qty(product_id, qty)
