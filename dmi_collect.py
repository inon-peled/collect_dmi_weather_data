import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from logger import info
import socket
from send_email import send
import os
from datetime import datetime

RETRIES = 5
REQUEST_TIMEOUT_SEC = 60
SAVE_DIR = os.path.join('.', 'data')


def retry_session(retries, session=None, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_last_reading_for_all_stations_in_denmark():
    with retry_session(retries=RETRIES).get(
            'https://beta.dmi.dk/NinJo2DmiDk/ninjo2dmidk?cmd=obj&east=-180&west=180&south=-90&north=90',
            timeout=REQUEST_TIMEOUT_SEC) as r:
        r.raise_for_status()
        if not r.content:
            raise ValueError('No contents')
        if 'application/json' not in r.headers['Content-Type'].lower():
            raise ValueError('Contents are not of type JSON')
        return r.content


def persist():
    try:
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        content = get_last_reading_for_all_stations_in_denmark()
        out_path = os.path.join(SAVE_DIR,
                               'dmi_all_stations_last_reading_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
        with open(out_path, 'wb') as f:
            f.write(content)
        info('Successfully saved data into %s' % out_path)
    except Exception as exc:
        send(subject='Error in DMI Weather Data Collection Script',
             body='The DMI weather data collection script running on %s has raised the following exception:\n\n%s' %
                  (socket.gethostname(), exc))


if __name__ == '__main__':
    persist()
