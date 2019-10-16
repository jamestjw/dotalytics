import requests
import bs4
import os 
import datetime
import argparse
import json
import flask
from google.cloud import storage

client = storage.Client()
bucket = client.get_bucket('kaodim-ml')
fname = 'hero_stats_v2_{}.json'
headers={'user-agent': 'Mozilla/5.0'}

def main(event, context):
    timestamp = str(datetime.datetime.now())
    date = str(datetime.datetime.now().date())
    res = requests.get('https://api.opendota.com/api/heroStats')
    heroes = json.loads(res.content.decode('utf-8'))
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
    blob = bucket.blob('dataset/dota/hero_data/{}'.format(fname.format(date)))
    blob.upload_from_string(final_result)
    print('Successfully uploaded hero data for date {}'.format(date))