import json
import os
from datetime import datetime
import requests

SAVE_DIR = os.path.join('.', 'data')


def get_last_reading_for_all_stations_in_denmark():
    with requests.get(
            'https://beta.dmi.dk/NinJo2DmiDk/ninjo2dmidk?cmd=obj&east=-180&west=180&south=-90&north=90') as r:
        r.raise_for_status()
        if not r.content:
            raise ValueError('No contents')
        if not json.loads(r.content.decode('utf-8')):
            raise Warning('Could not decode contents as UTF-8 JSON')
        return r.content


def persist():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    content = get_last_reading_for_all_stations_in_denmark()
    with open(os.path.join(SAVE_DIR,
                           'dmi_all_stations_last_reading_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'),
              'wb') as f:
        f.write(content)


if __name__ == '__main__':
    persist()
