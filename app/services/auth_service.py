from dotenv import dotenv_values

from app.config.settings import (
    BASE_URL,
    AUTH_URL
)

from app.clients.api_client import ApiClient

config_token = dotenv_values(".env.token")
config_header = dotenv_values(".env.header")


class AuthService:

    def __init__(self):

        self.client = ApiClient()

    def get_token(self):

        response = self.client.post(
            url=f"{BASE_URL}{AUTH_URL}",
            headers=config_header,
            data=config_token
        )

        response.raise_for_status()

        return response.json()["access_token"]