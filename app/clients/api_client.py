import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class ApiClient:

    def __init__(self):
        self.session = requests.Session()

        retry_strategy = Retry(
                total=5,
                connect=5,
                read=5,
                backoff_factor=2,
                status_forcelist=[
                    429,
                    500,
                    502,
                    503,
                    504
                ]
            )

        adapter = HTTPAdapter(
            max_retries=retry_strategy
        )

        self.session.mount(
            "https://",
            adapter
        )

        self.session.mount(
            "http://",
            adapter
        )


    def get(self, url, headers=None):

        return self.session.get(
            url,
            headers=headers,
            timeout=60
        )

    def post(self, url, headers=None, data=None):

        return self.session.post(
            url,
            headers=headers,
            data=data,
            timeout=60
        )