import json

with open('mock_data/space_track/conjunctions.json') as f:
    CONJUNCTIONS = json.load(f)


def get_satellites_ids():
    satellites = set()
    for data in CONJUNCTIONS:
        satellites.add(data['SAT_1_ID'])
        satellites.add(data['SAT_2_ID'])
    return list(satellites)