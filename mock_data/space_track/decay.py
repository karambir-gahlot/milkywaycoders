from datetime import datetime
from myutils.files import (
    load_json_file
)
from myutils.satellites import (
    is_neighbour
)
from mock_data.space_track.satcat import (
    SATCAT_BY_NORAD_CAT_ID
)

DECAY_DATA = load_json_file(__file__, './decay.json')

def _process_data(decay_data):
    for d in decay_data:
        if d['DECAY_EPOCH']:
            d['DECAY_EPOCH_DATETIME'] = datetime.strptime(d['DECAY_EPOCH'].split()[0], '%Y-%m-%d')
    return decay_data

DECAY_DATA = _process_data(DECAY_DATA)

DECAY_SATELLITES_IDS = list(set([d['NORAD_CAT_ID'] for d in DECAY_DATA]))

def get_decay_impacting_my_satellites(my_satellites):
    today_dt = datetime.now()
    impacting_decays = []
    for decay in DECAY_DATA:
        if decay['DECAY_EPOCH_DATETIME'] < today_dt:
            continue
        d = SATCAT_BY_NORAD_CAT_ID[decay['NORAD_CAT_ID']]
        impacted_satellites = [
            s for s in my_satellites
            if is_neighbour(s, d, 5)
            # if s['PERIGEE'] and s['APOGEE'] and ((d['APOGEE'] and s['PERIGEE']<=d['APOGEE']<=s['APOGEE']) or (d['PERIGEE'] and s['PERIGEE']<=d['PERIGEE']<=s['APOGEE'])) and decay['NORAD_CAT_ID'] != s['NORAD_CAT_ID']
        ]
        if impacted_satellites:
            impacting_decays.append({
                'decay': decay,
                'decay_satellite': d,
                'impacted_satellites': impacted_satellites
            })
    return impacting_decays

