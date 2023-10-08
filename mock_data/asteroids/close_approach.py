import json
from myutils.files import (
    get_relative_directory
)

def _load_data():
    with open(get_relative_directory(__file__, 'close_approach.json')) as f:
        ca_data = json.load(f)
        for ca in ca_data:
            ca['CLOSE_APPROACH_KM_HEIGHT'] = ca['CLOSE_APPROACH_LUNAR_DISTANCE'] * 384398 - 6700
        return ca_data

CLOSE_APPROACH_DATA = _load_data()


def get_close_approach_impacting_my_satellite(satellites):
    impacting_approaches = []
    non_impacting_approaches = []
    for approach in CLOSE_APPROACH_DATA:
        impacted_satellites = [
            s for s in satellites
            if s['APOGEE'] and approach['CLOSE_APPROACH_KM_HEIGHT'] <= float(s['APOGEE'])
        ]
        if impacted_satellites:
            impacting_approaches.append({
                'approach': approach,
                'impacted_satellites': impacted_satellites
            })
        else:
            non_impacting_approaches.append(approach)
    return {
        'impacting_approaches': impacting_approaches,
        'non_impacting_approaches': non_impacting_approaches
    }

