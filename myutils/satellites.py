def is_neighbour(s, d, inclination_offset=1):
    if s['INCLINATION'] is not None and d['INCLINATION'] is not None:
        if (s['INCLINATION']-inclination_offset)<=d['INCLINATION']<=(s['INCLINATION']+inclination_offset):
            return s['PERIGEE'] and s['APOGEE'] and ((d['APOGEE'] and s['PERIGEE']<=d['APOGEE']<=s['APOGEE']) or (d['PERIGEE'] and s['PERIGEE']<=d['PERIGEE']<=s['APOGEE'])) and d['NORAD_CAT_ID'] != s['NORAD_CAT_ID']
    return False