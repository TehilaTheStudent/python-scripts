# api_client.py
# Handles API requests in a reusable and extendable way
import requests
from config import API_BASE_URL, DEFAULT_HEADERS, DEFAULT_COOKIES, get_api_params

class APIClient:
    def __init__(self, base_url=API_BASE_URL, headers=None, cookies=None):
        self.base_url = base_url
        self.headers = headers or DEFAULT_HEADERS
        self.cookies = cookies or DEFAULT_COOKIES

    def get_api_details(self, product_short, name, region_id):
        params = get_api_params(product_short, name, region_id)
        response = requests.get(
            self.base_url,
            headers=self.headers,
            cookies=self.cookies,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_all_product_names(self):
        url = "https://apiexplorer.ap-southeast-3.myhuaweicloud.com/v5/products"
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        response.raise_for_status()
        data = response.json()
        # Extract productshorts as in jq: .groups[].products[].productshort
        product_names = []
        for group in data.get("groups", []):
            for product in group.get("products", []):
                short = product.get("productshort")
                if short:
                    product_names.append(short)
        return product_names

    def get_api_names_for_product(self, product_short):
        url = "https://apiexplorer.ap-southeast-3.myhuaweicloud.com/v3/apis"
        params = {
            "offset": 0,
            "limit": 100,
            "product_short": product_short
        }
        response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params)
        response.raise_for_status()
        data = response.json()
        # Extract API names: .api_basic_infos[].name
        api_names = []
        for api in data.get("api_basic_infos", []):
            name = api.get("name")
            if name:
                api_names.append(name)
        return api_names

    def get_api_details_by_name(self, product_short, api_name, region_id="ap-southeast-3"):
        url = "https://apiexplorer.ap-southeast-3.myhuaweicloud.com/v4/apis/detail"
        params = {
            "product_short": product_short,
            "name": api_name,
            "region_id": region_id
        }
        response = requests.get(url, headers=self.headers, cookies=self.cookies, params=params)
        response.raise_for_status()
        return response.json()

    # Add more API methods here as needed
