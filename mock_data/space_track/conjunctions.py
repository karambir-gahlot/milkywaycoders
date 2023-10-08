import json
from myutils.files import (
    get_relative_directory
)

with open(get_relative_directory(__file__, 'conjunctions.json')) as f:
    CONJUNCTIONS = json.load(f)


def get_satellites_ids():
    satellites = set()
    for data in CONJUNCTIONS:
        satellites.add(data['SAT_1_ID'])
        satellites.add(data['SAT_2_ID'])
    return list(satellites)