import requests
import json


class Api:

    BASE_URL = 'http://127.0.0.1:5000/'

    def __init__(self):
        self._base_url = self.BASE_URL
        self._headers = {'Content-type': 'application/json'}

    def get_request(self, path, headers=None):
        r = requests.get(f'{self._base_url}{path}')
        if r.status_code == 200:
            return r.json()
        else:
            print('Error while retrieving data')
            return None

    # This is only for testing purpose
    def post_stream(self, path, data, ):
        r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if r.status_code == 200:
            print(f'response - {r.text}')
            return r.text
        else:
            print('Error while retrieving data')
            return None
