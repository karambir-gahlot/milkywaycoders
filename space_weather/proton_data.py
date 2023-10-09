import json
from myutils.files import (
    load_json_file
)

PROTON_DATA = load_json_file(
    __file__, '../src/data/GOES_proton_data.json'
)

def _process_data(proton_data):
    for pd in proton_data:
        pd['DISPLAY_TIME'] = pd['time_tag'].replace('T', ' ').replace('Z', '').split(' ')[0]
        pd['ENERGY_MEV'] = int(str(pd['energy'].split()[0][2:]))
    return proton_data

def _get_proton_series(proton_data, energy):
    return [
        pd for pd in proton_data
        if pd['energy'] == energy
    ]

PROTON_DATA = _process_data(PROTON_DATA)

PROTON_SERIES_10 = _get_proton_series(PROTON_DATA, '>=10 MeV')
PROTON_SERIES_50 = _get_proton_series(PROTON_DATA, '>=50 MeV')
PROTON_SERIES_100 = _get_proton_series(PROTON_DATA, '>=100 MeV')