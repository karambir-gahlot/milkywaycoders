def is_neighbour(s, d):
    if s['INCLINATION'] is not None and d['INCLINATION'] is not None:
        if (s['INCLINATION']-1)<=d['INCLINATION']<=(s['INCLINATION']+1):
            return s['PERIGEE'] and s['APOGEE'] and ((d['APOGEE'] and s['PERIGEE']<=d['APOGEE']<=s['APOGEE']) or (d['PERIGEE'] and s['PERIGEE']<=d['PERIGEE']<=s['APOGEE'])) and d['NORAD_CAT_ID'] != s['NORAD_CAT_ID']
    return False