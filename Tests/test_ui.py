from selenium import webdriver
from book_shop_page import BookShopPage

driver = webdriver.Chrome()
#driver.implicitly_wait(4)

shop_url = 'http://www.chitai-gorod.ru/'
shop = BookShopPage(driver, shop_url)
shop.get_book_shop()


def test_search_for_the_book_by_name():
    shop.search_for_the_book("Манюня")
    products = shop.get_shop_products()

    assert len(products) > 1, "Продукт не найден"


def test_search_for_the_book_by_id():
    shop.search_for_the_book("3022420")
    products = shop.get_shop_products()

    assert len(products) == 1, "Продукт не найден"


def test_add_the_book_to_cart():
    shop.search_for_the_book("3022420")
    shop.click_on_product()
    shop.add_product_to_chart_click()
    shop.go_to_cart()

    assert len(shop.get_cart_products()) == 1, "В корзине нет продуктов"


def test_add_two_books_to_cart():
    shop.search_for_the_book("3022420")
    shop.click_on_product()
    shop.add_product_to_chart_click()

    shop.search_for_the_book("2248089")
    shop.click_on_product()
    shop.add_product_to_chart_click()

    shop.go_to_cart()

    assert len(shop.get_cart_products()) == 2, "В корзине нет продуктов"


def test_add_book_and_increase_quantity():
    shop.search_for_the_book("3022420")
    shop.click_on_product()
    shop.add_product_to_chart_click()

    shop.go_to_cart()

    shop.increase_quantity_by_one()

    assert shop.get_quantity() == "2"


def test_check_cart_total():
    shop.search_for_the_book("3022420")
    shop.click_on_product()
    shop.add_product_to_chart_click()

    shop.search_for_the_book("2248089")
    shop.click_on_product()
    shop.add_product_to_chart_click()

    shop.go_to_cart()
    shop.wait_for_cart()
    
    total_products_price = shop.get_all_products_price()
    
    assert shop.check_total() == total_products_price, "Цена товаров рассчитана не правильно"
    

test_check_cart_total()