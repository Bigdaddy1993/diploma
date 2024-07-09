import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_product(pk, data):
    """Создание продукта"""
    description = str(pk) + "дата платежа" + str(data)
    payment = stripe.Product.create(
        name=f'{pk}',
        description=description
    )
    return payment.get('id')


def create_stripe_price():
    """Создание цены"""
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=1500 * 100,
        product_data={"name": "Оплата выбранного продукта"},
    )
    return stripe_price


def create_stripe_session(price):
    """
    создает сессию в страйпе
    """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
