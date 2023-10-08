import json

with open('mock_data/space_track/satcat.json') as f:
    SATCAT_DATA = json.load(f)

SATCAT_BY_NORAD_CAT_ID = {
    s['NORAD_CAT_ID'] : s
    for s in SATCAT_DATA
}
