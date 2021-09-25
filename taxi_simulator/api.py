import requests
import json


class Api:

    # Please change URL after you deploy backend_lambda in aws
    BASE_URL = 'https://fep34ikk65.execute-api.us-east-1.amazonaws.com/dev'

    def __init__(self):
        self._base_url = self.BASE_URL
        self._headers = {'Content-type': 'application/json'}

    # Function used to get data from the api
    def get_request(self, path, headers=None):
        r = requests.get(f'{self._base_url}{path}')
        if r.status_code == 200:
            return r.json()
        else:
            print('Error while retrieving data')
            return None

    # This is only for testing purpose
    def post_stream(self, path, data):
        r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if r.status_code == 200:
            print(f'response - {r.text}')
            return r.text
        else:
            print('Error while retrieving data')
            return None
