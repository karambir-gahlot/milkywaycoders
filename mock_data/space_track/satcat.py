import json
from myutils.files import (
    get_relative_directory
)

with open(get_relative_directory(__file__, 'satcat.json')) as f:
    SATCAT_DATA = json.load(f)

SATCAT_BY_NORAD_CAT_ID = {
    s['NORAD_CAT_ID'] : s
    for s in SATCAT_DATA
}
