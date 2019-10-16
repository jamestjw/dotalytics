import requests
import bs4
import datetime
import pandas as pd
import os
import time
from tqdm import tqdm


file_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(file_path,'data')
api_path = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1'
base_url = "https://www.dotabuff.com"
key = 'C60E6010CC31F156C3D1343CD69ED3BC'
headers={'user-agent': 'Mozilla/5.0'}

saved_ids = set(line.strip() for line in open(os.path.join(save_path,'match_ids.txt')))

for id in tqdm(saved_ids):
	res = requests.get(api_path, params={'key':key,'match_id':id}, headers=headers)
	if res.status_code != 200: 
		print(id)
		continue
	with open(os.path.join(save_path,'match_data.json'),'a') as f:
		f.write(',\n')
		f.write(res.text)
