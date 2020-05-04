# LIBRARIES
import urllib
import os
import json
import pandas as pd
from src.paths import MODES

# DECLARATIONS
URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
PARAM_LIST = {'subway': { "id": "996cfe8d-fb35-40ce-b569-698d51fc683b"}, #subway 
             'streetcar': { "id": "b68cb71b-44a7-4394-97e2-5d2f41462a5d"}, #streetcar
             'bus': { "id": "e271cdae-8788-4980-96ce-6a5c95bc6618"}} #bus 

# INITIALIZE FOLDERS
for raw_processed_clean in ['raw','processed', 'cleaned_final']:
    paths = []
    
    paths.append(f'data/{raw_processed_clean}')
    paths.append(f'data/{raw_processed_clean}/ttc')
    
    for mode in MODES:
        if mode != 'cleaned_final':
            paths.append(f'data/{raw_processed_clean}/ttc/{mode}/')
        elif mode == 'cleaned_final':
            paths.append(f'data/{raw_processed_clean}/')

    for folder in ['weather','ridership']:
        paths.append(f'data/{raw_processed_clean}/{folder}/')

    print(paths)
    for path in paths:
        try: 
            os.mkdir(path)
        except FileExistsError:
            pass
        
# SCRAPING
def get_ttc_packages(mode):
    param = PARAM_LIST[mode]

    response = urllib.request.urlopen(URL, data = bytes(json.dumps(param), encoding = "utf-8"))
    package = json.loads(response.read())
    
    urls = pd.DataFrame(columns = ['item','url'])
    for i, pkg in enumerate(package['result']['resources']):
        urls.loc[i,'item'] = pkg['name']
        urls.loc[i,'url'] = pkg['url']

    return urls

def download_ttc_packages(mode):
    pkgs = get_ttc_packages(mode)

    for item, url in zip(pkgs.item, pkgs.url):
        urllib.request.urlretrieve(url = url, filename = f'data/raw/ttc/{mode}/{item}.xlsx')
    
        print(f'Downloaded {item}.')

for mode in MODES:
    raw_path = f'data/raw/ttc/{mode}/'
    if not os.listdir(raw_path):
        download_ttc_packages(mode)
