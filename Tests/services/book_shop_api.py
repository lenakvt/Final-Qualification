import requests


class BookShopApi:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def clear_cart(self):
        url = f"{self.base_url}/cart"
        return requests.delete(url).status_code == 200

    def get_procucts(self, search_params):
        url = f"{self.base_url}/search/product"
        resp = requests.get(url, params=search_params, headers=self.headers)
        return resp.json()

    def get_cart(self):
        url = f"{self.base_url}/cart"
        resp = requests.get(url, headers=self.headers)
        return resp.json()

    def add_product_to_cart(self, payload) -> str | bool:
        url = f"{self.base_url}/cart/product"
        resp = requests.post(url, json=payload, headers=self.headers)

        if (resp.status_code != 200):
            return resp.status_code

        return resp.status_code == 200

    def increase_quantity(self, product_id: int, quantity: int) -> str | bool:
        url = f"{self.base_url}/cart"
        payload = [{"id": product_id, "quantity": quantity}]
        resp = requests.put(
            url, json=payload,
            headers=self.headers)

        if (resp.status_code != 200):
            return resp.status_code

        return resp.status_code == 200

    def delete_product(self, product_id: int):
        url = f"{self.base_url}/cart/product/{str(product_id)}"
        resp = requests.delete(url, headers=self.headers)
        return resp.status_code == 200
