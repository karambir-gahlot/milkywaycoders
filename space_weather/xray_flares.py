import json
from myutils.files import (
    load_json_file
)

XRAY_FLARES_DATA = load_json_file(
    __file__, '../src/data/xray-flares-7-day.json'
)

def _process_data(xray_flares_data):
    for pd in xray_flares_data:
        # TODO: use max_ratio_time instead - It is null in some cases
        pd['DISPLAY_TIME'] = pd['time_tag'].replace('T', ' ').replace('Z', '').split(' ')[0]
        pd['CLASS'] = pd['max_class'][0]
    return xray_flares_data

def _get_xray_flares_data_series(xray_flares_data, cat_class):
    return [
        pd for pd in xray_flares_data
        if pd['CLASS'] == cat_class
    ]

XRAY_FLARES_DATA = _process_data(XRAY_FLARES_DATA)