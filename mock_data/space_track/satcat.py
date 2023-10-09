import json
from myutils.files import (
    get_relative_directory
)
from myutils.satellites import (
    is_neighbour
)

with open(get_relative_directory(__file__, 'satcat.json')) as f:
    SATCAT_DATA = json.load(f)

with open(get_relative_directory(__file__, 'canadian_satellites.json')) as cf:
    _CANADIAN_SATELLITES = json.load(cf)

_sat_ids = set(s['NORAD_CAT_ID'] for s in SATCAT_DATA)
for _c in _CANADIAN_SATELLITES:
    if _c['NORAD_CAT_ID'] not in _sat_ids:
        SATCAT_DATA.append(_c)

for s in SATCAT_DATA:
    if s['APOGEE']:
        s['APOGEE'] = int(s['APOGEE'])
    if s['PERIGEE']:
        s['PERIGEE'] = int(s['PERIGEE'])
    if s['INCLINATION']:
        s['INCLINATION'] = float(s['INCLINATION'])

SATCAT_BY_NORAD_CAT_ID = {
    s['NORAD_CAT_ID'] : s
    for s in SATCAT_DATA
}

ALL_SATELLITES_SATCAT_DATA = [
    s for s in SATCAT_DATA
    if s['OBJECT_TYPE'] != 'DEBRIS'
]

def find_neighbours(my_satellites):
    neighbours_data = []
    for sat in my_satellites:
        neighbours = [
            s for s in SATCAT_DATA if is_neighbour(sat, s)
        ]
        neighbours_data.append({
            'satellite': sat,
            'neighbours': neighbours
        })
    return neighbours_data