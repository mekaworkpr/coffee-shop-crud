def init_models():
    from coffee_shop.sqlalchemy_db.models.user import User
    from coffee_shop.sqlalchemy_db.models.category import Category
    from coffee_shop.sqlalchemy_db.models.product import Product
    from coffee_shop.sqlalchemy_db.models.order import Order
    from coffee_shop.sqlalchemy_db.models.order_item import OrderItem
    from coffee_shop.sqlalchemy_db.models.cart_item import CartItem
