import requests
import bs4
import os 
import datetime
import argparse
from tqdm import tqdm
import re

file_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(file_path,'data')
result_path = os.path.join(save_path,'patch_dates.csv')
headers={'user-agent': 'Mozilla/5.0'}

# these correspond to the TDs that contain the hero name, WR, PR and KDA

# columns in CSV file
columns = ['patch_name','patch_date','root','created_at']

def get_data():
    api_path = "https://liquipedia.net/dota2/Portal:Patches"
    res = requests.get(api_path, headers=headers)
    status = res.status_code
    if status == 404:
        return None , status
    else:
        soup = bs4.BeautifulSoup(res.content,features="html.parser")

        #We drop the data from patches that are too old
        tables = soup.find_all('table','wikitable')[:5]
        return tables, status

def extract_data(tables):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(result_path,'a') as f:
        # if file is empty, first create headers
        if os.path.getsize(result_path) == 0:
            f.write('%s' % ','.join(map(str, columns)))
            f.write('\n')

        # Skip first row (headers)
        for table in tables:
            # first row is header
            rows = table.find_all('tr')[1:]
            for row in rows:
                tds = row.find_all('td')
                row_data = [td.text.strip() for td in tds[:2]]
                if len(row_data) == 2:
                    version = row_data[0]
                    root_version = re.sub('[a-zA-Z]', '', version)
                    row_data.append(root_version)
                    row_data.append(str(datetime.datetime.now()))
                    to_write = '%s' % ','.join(map(str, row_data))
                    f.write(to_write)
                    f.write('\n')

    print('Completed download of patch dates')


def main():
    # 404 will be received for wrong patch ID
    heroes, status = get_data()
    if status == 404:
        print('Page did not load')
    else:
        extract_data(heroes)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Download hero stats for a Dota2 patch')
    # parser.add_argument('--patch', nargs='+', help='Patch ID to extract hero stats for, e.g. 7.21, 7.22')
    # args = parser.parse_args()
    # patches = args.patch
    # if patches is None:
    #     print('No input patches were detected, falling back to default')
    #     res = requests.get('https://www.dotabuff.com/heroes/winning',headers=headers)
    #     soup = bs4.BeautifulSoup(res.content,features="html.parser")
    #     duration = soup.find_all('select')[0].find_all('option')
    #     patches = [d.get('value').split('_')[-1] for d in duration if d.get('value').startswith('patch')]
    #     print('Downloading data for the following patches: ', str(patches))

    main()
