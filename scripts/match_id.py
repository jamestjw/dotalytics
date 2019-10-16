import os
import requests
import json
import time

file_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(file_path,'data','match_ids.txt')
api_path = 'https://api.opendota.com/api/proMatches'

saved_ids = [line.strip() for line in open(save_path)]
last_match = str(saved_ids[-1])

stop = False
while not stop:
    time.sleep(1)
    res = requests.get(api_path, params={'less_than_match_id':int(last_match)})
    data = json.loads(res.text)
    if len(data) > 0:
        with open(save_path,'a') as f:
            for d in data:
                id = str(d['match_id'])
                f.write(id+'\n')
        last_match = id
        print('Successfully wrote {} files.'.format(len(data)))
    else:
        stop = True
