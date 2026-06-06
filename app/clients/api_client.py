import requests


class ApiClient:

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, headers=None):

        return self.session.get(
            url,
            headers=headers,
            timeout=30
        )

    def post(self, url, headers=None, data=None):

        return self.session.post(
            url,
            headers=headers,
            data=data,
            timeout=30
        )