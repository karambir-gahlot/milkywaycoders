import time
import json
import requests
from .conjunctions import (
    get_satellites_ids
)

def batch(iterable, n = 1):
   current_batch = []
   for item in iterable:
       current_batch.append(item)
       if len(current_batch) == n:
           yield current_batch
           current_batch = []
   if current_batch:
       yield current_batch

def _get_satcat_urls(sat_ids):
    ids_param = '%2C'.join(str(i) for i in sat_ids)
    url = r'https://www.space-track.org/basicspacedata/query/class/satcat/NORAD_CAT_ID/' + ids_param + r'/orderby/LAUNCH%20desc/limit/1000/emptyresult/show'
    print('Loading url:', url)
    # TODO: add cookie here
    return requests.get(url, cookies={'': ''}).json()

def _main():
    satellites_ids = get_satellites_ids()
    print('Number of satellites:', len(satellites_ids))
    satellites_ids = list(satellites_ids)
    result = []
    for sat_batch in batch(satellites_ids, 50):
        result.extend(_get_satcat_urls(sat_batch))
        print('Loaded')
        time.sleep(3)
    
    print('Loaded number results:', len(result))
    
    with open('mock_data/space_track/satcat.json', 'w') as f:
        json.dump(result, f)



if __name__ == '__main__':
    _main()