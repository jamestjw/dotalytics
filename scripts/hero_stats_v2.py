import requests
import bs4
import os 
import datetime
import argparse
from tqdm import tqdm
import json

# from google.cloud import storage
# client = storage.Client()
# bucket = client.get_bucket('kaodim-ml')

file_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(file_path,'data')
fname = 'hero_stats_v2_{}.json'
result_path = os.path.join(save_path,fname)
headers={'user-agent': 'Mozilla/5.0'}

timestamp = str(datetime.datetime.now())
date = str(datetime.datetime.now().date())

res = requests.get('https://api.opendota.com/api/heroStats')
heroes = json.loads(res.content)

columns = [str(c) for c in range(1,9)]
columns += ['pro','null']

final_result = ''
for hero in heroes:
    hero_data = {}
    hero_data['hero_id'] = hero['hero_id']
    hero_data['name'] = hero['localized_name']
    hero_data['created_at'] = timestamp
    for c in columns:
        win_pick = []
        for t in ['win','pick']:
            stat = hero['_'.join([c,t])]
            hero_data['_'.join([t,c])] = stat
            win_pick.append(stat)
        hero_data['_'.join(['wr',c])] = win_pick[0]/win_pick[1]
    final_result += json.dumps(hero_data)
    final_result += '\n'

if not os.path.exists(save_path):
    os.makedirs(save_path)

result_path = result_path.format(timestamp)
with open(result_path,'a') as f:
    # if file is empty, first create headers
    if os.path.getsize(result_path) == 0:
        f.write(final_result)

# blob = bucket.blob('dataset/dota/hero_data/{}'.format(fname.format(date)))
# blob.upload_from_string(final_result)