import json
import os
import base64
import requests

Headers = {'Content-type': 'application/json'}


def push_data_db(base_url, route, data):
    r = requests.post(f'{base_url}{route}', json.dumps(data), headers=Headers)
    if r.status_code == 200:
        print(f'response - {r.text}')
        return r.text
    else:
        print('Error while retrieving data')
        return None


def lambda_handler(event, context):
    base_url = os.environ['BASE_URL']
    route = os.environ['ROUTE']
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        payload_dict = json.loads(payload.decode("utf-8"))
        print("Message arrived: " + str(payload_dict))
        result = push_data_db(base_url, route, payload_dict)
        if result:
            print(f'Data inserted successfully in DB for vehicle - {payload_dict["vehicle_num"]}')
        else:
            print(f'Error in updating data in db for vehicle number - {payload_dict["vehicle_num"]}')

    return {'statusCode': 200, 'body': 'success'}