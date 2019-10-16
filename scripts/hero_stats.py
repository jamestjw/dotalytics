import requests
import bs4
import os 
import datetime
import argparse
from tqdm import tqdm

file_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(file_path,'data')
result_path = os.path.join(save_path,'hero_stats.csv')
headers={'user-agent': 'Mozilla/5.0'}

# these correspond to the TDs that contain the hero name, WR, PR and KDA
td_idx = [0,2,3,4]

# columns in CSV file
columns = ['name','win_rate','pick_rate','kda','patch','created_at']

def get_data(patch):
    api_path = 'https://www.dotabuff.com/heroes/winning?date=patch_{}'.format(patch)
    res = requests.get(api_path, headers=headers)
    status = res.status_code
    if status == 404:
        return None , status
    else:
        soup = bs4.BeautifulSoup(res.content,features="html.parser")
        table = soup.find_all('table','sortable')
        heroes = table[0].find_all('tr')[1:]
        return heroes, status

def extract_data(heroes, patch):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(result_path,'a') as f:
        # if file is empty, first create headers
        if os.path.getsize(result_path) == 0:
            f.write('%s' % ','.join(map(str, columns)))
            f.write('\n')
        # Skip first row (headers)
        for hero in heroes[1:]:
            data = hero.find_all('td')
            hero_data = []
            for idx in td_idx:
                hero_data.append(data[idx].get('data-value'))
            hero_data.append(patch)
            hero_data.append(str(datetime.datetime.now()))

            to_write = '%s' % ','.join(map(str, hero_data))
            f.write(to_write)
            f.write('\n')

    print('Completed download of hero stats for patch {}'.format(patch))


def main(patches):
    # 404 will be received for wrong patch ID
    for patch in tqdm(patches):
        heroes, status = get_data(patch)
        if status == 404:
            print('Patch {} does not exist.'.format(patch))
        else:
            extract_data(heroes, patch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download hero stats for a Dota2 patch')
    parser.add_argument('--patch', nargs='+', help='Patch ID to extract hero stats for, e.g. 7.21, 7.22')
    args = parser.parse_args()
    patches = args.patch
    if patches is None:
        print('No input patches were detected, falling back to default')
        res = requests.get('https://www.dotabuff.com/heroes/winning',headers=headers)
        soup = bs4.BeautifulSoup(res.content,features="html.parser")
        duration = soup.find_all('select')[0].find_all('option')
        patches = [d.get('value').split('_')[-1] for d in duration if d.get('value').startswith('patch')]
        print('Downloading data for the following patches: ', str(patches))

    main(patches)



