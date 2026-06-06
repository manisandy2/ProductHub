from app.services.auth_service import AuthService
from app.config.settings import (
    BASE_URL,
    PRODUCT_URL
)


class ProductService:

    def __init__(self):

        self.auth_service = AuthService()

        self.token = self.auth_service.get_token()

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

        self.records = []

    def refresh_token(self):

        self.token = self.auth_service.get_token()

        self.headers["Authorization"] = (
            f"Bearer {self.token}"
        )

    def fetch_page(self, page):

        import requests

        response = requests.get(
            f"{BASE_URL}{PRODUCT_URL}{page}",
            headers=self.headers,
            timeout=30
        )

        if response.status_code == 401:

            self.refresh_token()

            response = requests.get(
                f"{BASE_URL}{PRODUCT_URL}{page}",
                headers=self.headers,
                timeout=30
            )

        response.raise_for_status()

        return response.json()

    def process_page(self, page):

        data = self.fetch_page(page)

        self.records.extend(
            data.get("items", [])
        )

    def run(self):

        for page in range(1, 50):

            self.process_page(page)

            if page % 50 == 0:

                print(
                    f"Processed {page} pages"
                )

        return self.records