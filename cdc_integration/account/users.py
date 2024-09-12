import requests
from nidavellir.clients.bifrost_proxy_redirects.cdc.cdc_proxy_manager import CDCProxyManager

from config.environment import ENVIRONMENT


class Users:
    def __init__(self, proxy_manager: CDCProxyManager):
        self.proxy_manager = proxy_manager

    def get_user_by_document(self, document) -> dict | None:
        headers = {
            "Accept": "*/*",
            "Authorization": f"Bearer {self.proxy_manager.get_api_token()}",
        }
        params = {
            "document": document
        }

        url = f"{ENVIRONMENT.cateno_base_api_url}/partner/client_pf"

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                response_data = e.response.json()

                if response_data["message"] == "customers not found":
                    return None
            raise e

        return response.json()

    def get_user_documents(self, code):
        headers = {
            "Accept": "*/*",
            "Authorization": f"Bearer {self.proxy_manager.get_api_token()}",
        }

        params = {
            "client_pf_code": code
        }

        url = f"{ENVIRONMENT.cateno_base_api_url}/partner/client_pf/documents/{code}"

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
