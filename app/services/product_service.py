from app.services.auth_service import AuthService
from app.config.settings import (
    BASE_URL,
    PRODUCT_URL
)
from app.clients.api_client import ApiClient
from requests.exceptions import (ConnectTimeout,RequestException)
from app.monitoring.metrics import (
    products_processed,api_requests,current_products,
    request_duration,api_errors
)
import time 

class ProductService:

    def __init__(self):
        self.client = ApiClient()

        
        self.auth_service = AuthService()

        self.token = self.auth_service.get_token()

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        self.url = f"{BASE_URL}{PRODUCT_URL}"


        self.records = []
        self.failed_pages = []

    def refresh_token(self):

        self.token = self.auth_service.get_token()

        self.headers["Authorization"] = (
            f"Bearer {self.token}"
        )

    # def fetch_page(self, page):

    #     import requests
    #     api_requests.inc()

    #     start_time = time.time()

    #     response = requests.get(
    #         f"{BASE_URL}{PRODUCT_URL}{page}",
    #         headers=self.headers,
    #         timeout=30
    #     )

    #     if response.status_code == 401:

    #         self.refresh_token()

    #         response = requests.get(
    #             f"{BASE_URL}{PRODUCT_URL}{page}",
    #             headers=self.headers,
    #             timeout=30
    #         )

    #     response.raise_for_status()

    #     duration = time.time() - start_time

    #     request_duration.observe(duration)

    #     print(
    #         f"Page={page} "
    #         f"Duration={duration:.3f}s"
    #         )


    #     return response.json()

    def fetch_page(self, page):

        try:

            api_requests.inc()

            start_time = time.time()

            response = self.client.get(
                f"{self.url}{page}",
                headers=self.headers
            )

            duration = time.time() - start_time

            request_duration.observe(duration)

            response.raise_for_status()

            return response.json()

        except ConnectTimeout:
            self.failed_pages.append(page)


            api_errors.inc()

            print(
                f"Timeout on page {page}"
            )

            return {"items": []}

        except RequestException as e:

            api_errors.inc()

            print(
                f"Request Error Page={page}: {e}"
            )

            return {"items": []}

    def process_page(self, page):

        data = self.fetch_page(page)

        items = data.get("items", [])

        self.records.extend(
            data.get("items", [])
        )
        products_processed.inc(len(items))

        current_products.set(
        len(self.records) )

    def run(self):

        for page in range(1, 200):

            self.process_page(page)

            if page % 50 == 0:

                print(
                    f"Processed {page} pages"
                )

        return self.records