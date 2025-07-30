import sys
from pathlib import Path
from environment import Environment

import requests

ADFIN_URL = Environment.get('ADFIN_URL', 'https://app.adfin.com')


class AdfinSession:
    def __init__(self):
        self.adfin_username = Environment.get('ADFIN_EMAIL')
        self.adfin_password = Environment.get('ADFIN_PASSWORD')

        self.access_token = None
        self.access_token = self.login()['accessToken']

    def _get_headers(self):
        if self.access_token is None:
            return None
        else:
            return {'Authorization': f'Bearer {self.access_token}'}

    def call_route(self, method_type, route, body: dict = None):
        method = getattr(requests, method_type)
        if not route.startswith('/'):
            route = '/' + route

        if method_type == 'get':
            response = method(f"{ADFIN_URL}/api{route}", params=body, headers=self._get_headers())
        else:
            response = method(f"{ADFIN_URL}/api{route}", json=body, headers=self._get_headers())

        if response.status_code == 200:
            return response.json()
        else:
            message = f"Error: {response.status_code} {response.text}"
            print(message, file=sys.stderr)

            print('Will attempt to refresh the access token', file=sys.stderr)
            self.access_token = self.login()['accessToken']
            print('Refreshed the access token', file=sys.stderr)

            response = method(f"{ADFIN_URL}/api{route}", json=body, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                message = f"Error: {response.status_code} {response.text}"
                print(message, file=sys.stderr)
                return message

    def login(self) -> dict:
        return self.call_route('post', '/auth/login',
                        body={'username': self.adfin_username, 'password': self.adfin_password})

    def get_invoices(self):
        return self.call_route('get', 'invoices')

    def upload_invoice(self, invoice_path):
        UPLOAD_URL = ADFIN_URL + "/api/process:invoiceUpload"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        with open(invoice_path, "rb") as file:
            files = {"invoice": (Path(invoice_path).name, file, "application/pdf")}
            response = requests.post(UPLOAD_URL, headers=headers, files=files)

        if response.status_code == 200:
            message = 'Upload successful'
            print(message, file=sys.stderr)
            return message
        else:
            message = f"Error: {response.status_code} {response.text}"
            print(message, file=sys.stderr)
            return f'Error: Could not upload invoice - {message}'


if __name__ == '__main__':
    adfin = AdfinSession()

    access_token = adfin.access_token
    print("Access token:", access_token)

