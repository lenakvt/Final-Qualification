

import pytest
from book_shop_api import BookShopApi

base_url = 'https://web-gate.chitai-gorod.ru/api/v1'
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg5NzY1MjQsImlhdCI6MTcyODgwODUyNCwiaXNzIjoiL2FwaS92MS9hdXRoL2Fub255bW91cyIsInN1YiI6IjllM2RhYzJkNTdiMzIwOTBlNzU4NDRmZWE4NTJkZDI4NjIzY2FlNTk1ZDhiYjBiMDczY2RlYTg0NzNjZjVmNzgiLCJ0eXBlIjoxMH0.jx7i3STGdlyJxY76_mZab_1PxuCRlzaju_nQJcmnKQ0"


@pytest.fixture(autouse=True)
def run_around_tests():
    # перед выполнением каждого теста
    global book
    book = BookShopApi(base_url, token)
    book.clear_cart()


def test_add_product():
    book_id = 2248089

    product = {"id": book_id, "adData": {"item_list_name": "product-page"}}
    book.add_product_to_cart(product)

    cart = book.get_cart()
    assert cart['products'][0]['goodsId'] == book_id, "Книга не добавлена"


def test_increase_quantity():
    quantity = 2
    product = {"id": 2248089, "adData": {"item_list_name": "product-page"}}
    book.add_product_to_cart(product)

    cart = book.get_cart()
    product_id = cart['products'][0]['id']

    book.increase_quantity(product_id, quantity)
    cart = book.get_cart()

    assert cart['products'][0]['quantity'] == quantity, "Неверное количество товара"


def test_delete_product():
    product = {"id": 2248089, "adData": {"item_list_name": "product-page"}}
    book.add_product_to_cart(product)

    cart = book.get_cart()
    product_id = cart['products'][0]['id']
    book.delete_product(product_id)
    cart = book.get_cart()

    assert len(cart['products']) == 0, "В корзине остались товары"


def test_add_incorrect_quantity():
    quantity = 500
    product = {"id": 2248089, "adData": {"item_list_name": "product-page"}}
    book.add_product_to_cart(product)

    cart = book.get_cart()
    product_id = cart['products'][0]['id']

    status_code = book.increase_quantity(product_id, quantity)

    assert status_code == 422, "Количество товара"


def test_add_incorrect_producty():
    cart = book.get_cart()
    products_length1 = len(cart['products'])
    
    product = {"id": -1, "adData": {"item_list_name": "product-page"}}
    products_length2 = len(cart['products'])
    status_code = book.add_product_to_cart(product)

    cart = book.get_cart()
    
    assert products_length1 == products_length2
    assert status_code == 422, "Продукт существует"


