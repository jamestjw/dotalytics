from google.cloud import storage
from google.cloud import pubsub_v1
from faker import Faker
import time
import random
import os
import numpy as np
from datetime import datetime, timedelta
from argparse import ArgumentParser
import json
import requests

LINE = """\
{remote_addr} - - [{time_local}] "{request_type} {request_path} HTTP/1.1" [{status}] {body_bytes_sent} "{http_referer}" "{http_user_agent}"\
"""


def blob_exists(bucket_name, filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    return bucket

def generate_log_line():
    fake = Faker()
    now = datetime.now()
    remote_addr = fake.ipv4()
    time_local = now.strftime('%d/%b/%Y:%H:%M:%S')
    request_type = random.choice(["GET", "POST", "PUT"])
    request_path = "/" + fake.uri_path()

    status = np.random.choice([200, 401, 404], p=[0.9, 0.05, 0.05])
    body_bytes_sent = random.choice(range(5, 1000, 1))
    http_referer = fake.uri()
    http_user_agent = fake.user_agent()

    log_line = LINE.format(
        remote_addr=remote_addr,
        time_local=time_local,
        request_type=request_type,
        request_path=request_path,
        status=status,
        body_bytes_sent=body_bytes_sent,
        http_referer=http_referer,
        http_user_agent=http_user_agent
    )

    return log_line

def request(match_id):
    api_path = 'https://api.opendota.com/api/matches/{}'.format(match_id)
    r = requests.get(api_path)
    return json.loads(r.content)

def get_list_of_match_ids(last_match_id = None):
    api_path = 'https://api.opendota.com/api/proMatches'
    max_match_id = 9999999999 if last_match_id == None else last_match_id
    res = requests.get(api_path, params={ 'less_than_match_id': int(max_match_id)})
    data = json.loads(res.text)
    return data





if __name__ == "__main__":
    base_path = '/Users/nicolasang/Desktop/dotalytics/'
    # fp = '/Users/nicolasang/Desktop/dotalytics/scripts/match_ids.txt'
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = base_path + 'Credentials/bigquery.json'
    # # max_id = None
        
    # data = get_list_of_match_ids()
    # list_of_match_id = [d['match_id'] for d in data]

    # max_id = max([d['match_id'] for d in data])
    # min_id = min([d['match_id'] for d in data])
    # with open('{}_{}.json'.format(max_id,min_id),'w') as f:
    #     for d in data:
    #         json.dump(d,f)

    # f.close()
    with open(base_path + '5083447407_5081564052.json') as f:
        data = json.load(f)
    print(data)
            



    



