# Resource - https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json
from myutils.files import (
    load_json_file
)

MAGNETOMETERS_DATA = load_json_file(
    __file__, '../src/data/magnetometers-7-day.json'
)

def _process_data(magenetometer_data):
    for pd in magenetometer_data:
        pd['DISPLAY_TIME'] = pd['time_tag'].replace('T', ' ').replace('Z', '').split(' ')[0]
    return magenetometer_data

MAGNETOMETERS_DATA = _process_data(MAGNETOMETERS_DATA)
