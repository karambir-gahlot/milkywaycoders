import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from myutils.files import (
    get_relative_directory
)

_CLOSE_APPROACH_PAGE_URL = 'https://iawn.net/close-approaches.shtml'
_CA_TABLE_CLOSE_APPROACH_PAGE_URL = 'https://iawn.net/close-approaches/ca-table.shtml'

_IAWN_HOME_URL = 'https://iawn.net'

_MINOR_PLANET_DISCOVERY_ANNOUNCEMENT_PREFIX = 'https://minorplanetcenter.net/mpec/'
_MINOR_PLANET_DISCOVERY_ANNOUNCEMENT_PREFIX_2 = 'http://minorplanetcenter.net//mpec/'
_MINOR_PLANET_DB_SEARCH_PREFIX = 'https://minorplanetcenter.net/db_search/show_object'

def _get_content(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def _is_close_approach_p_element(element):
    contents = element.contents
    return contents and contents[0].startswith('Asteroid designation:')

def _get_close_approach_info(element):
    contents = element.contents
    contents = [c for c in contents if c.name == 'a' or (c.string and c.string.strip())]
    try:
        assert contents[0].string.startswith('Asteroid designation:')
        assert contents[1].string.startswith('Discovery station:')
        assert contents[2].string.startswith('Close approach date (UTC):')
        assert contents[3].string.startswith('Close approach distance') and ' lunar distance):' in contents[3].string
        assert contents[4].name == 'a' and contents[4].contents[0] == 'Discovery announcement'
        assert contents[5].name == 'a' and contents[5].contents[0] == 'Latest orbit & observations'
        return {
            'ASTEROID_DESIGNATION': contents[0].string.strip()[len('Asteroid designation: '):],
            'DISCOVERY_STATION': contents[1].string.strip()[len('Discovery station: '):],
            'CLOSE_APPROACH_DATE_UTC': contents[2].string.strip()[len('Close approach date (UTC): '):],
            'CLOSE_APPROACH_LUNAR_DISTANCE': float(contents[3].string.strip()[len('Close approach distance (  lunar distance): '):]),
            'DISCOVERY_ANNOUNCEMENT_LINK': contents[4]['href'],
            'LATEST_ORBIT_OBSERVATIONS_LINK': contents[5]['href']
        }
    except:
        # print(element)
        raise

def _get_close_approaches():
    soup = _get_content(_CLOSE_APPROACH_PAGE_URL)
    all_parents = soup.find_all('p')
    all_parents = [
        p for p in all_parents
        if _is_close_approach_p_element(p)
    ]
    result = []
    for p in all_parents:
        try:
            r = _get_close_approach_info(p)
            result.append(r)
        except:
            pass
    return result
    # TODO: Fix to scrap all cases
    # return [_get_close_approach_info(p) for p in all_parents]


def _get_ca_table_row(element):
    try:
        assert element.name == 'tr'
        contents = [
            c for c in element.contents
            if c.name == 'td'
        ]
        """
        [<td><a href="https://minorplanetcenter.net/mpec/K23/K23Q65.html" onclick="this.target='_blank'">2023 QS1</a></td>,
            <td>2023 08 20.93687
            <br/>    GINOP-KHK, Piszkesteto</td>,
            <td>2023 08 19.77
            <br/><strong>0.28</strong></td>,
            <td><a href="/close-approaches/2023-QS1_geometry.shtml">geometry</a>
            <br/><a href="https://minorplanetcenter.net/db_search/show_object?object_id=K23Q01S" onclick="this.target='_blank'">Latest orbit &amp; observations</a></td>]
        """
        assert contents[0].contents[0].name == 'a' and ('minorplanetcenter.net' in contents[0].contents[0]['href'] and '/mpec/' in contents[0].contents[0]['href'])
        assert contents[1].name == 'td' and contents[1].contents[1].name == 'br' and len(contents[1].contents) == 3
        assert contents[2].name == 'td' and contents[2].contents[1].name == 'br' and len(contents[2].contents) == 3 and contents[2].contents[2].name == 'strong' and contents[2].contents[2].contents[0].string
        assert contents[3].name == 'td' and contents[3].contents[0].name == 'a' and ((len(contents[3].contents) == 4 and contents[3].contents[2].name == 'br' and contents[3].contents[3].name == 'a' and 'minorplanetcenter.net' in contents[3].contents[3]['href'] and '/db_search/show_object?' in contents[3].contents[3]['href']) or (len(contents[3].contents) == 1 and contents[3].contents[0].name=='a' and 'minorplanetcenter.net' in contents[3].contents[0]['href'] and '/db_search/show_object?' in contents[3].contents[0]['href']))
        return {
            'ASTEROID_DESIGNATION': contents[0].contents[0].contents[0].string,
            'DISCOVERY_DATE': contents[1].contents[0].string.strip(),
            'DISCOVERY_STATION': contents[1].contents[2].string.strip(),
            'CLOSE_APPROACH_DATE_UTC': contents[2].contents[0].string.strip(),
            'CLOSE_APPROACH_LUNAR_DISTANCE': float(contents[2].contents[2].string.strip()),
            'DISCOVERY_ANNOUNCEMENT_LINK': contents[0].contents[0]['href'],
            'LATEST_ORBIT_OBSERVATIONS_LINK': contents[3].contents[3]['href'] if len(contents[3].contents) == 4 else contents[3].contents[0]['href'],
            'GEOMETRY_LINK': (_IAWN_HOME_URL + contents[3].contents[0]['href']) if len(contents[3].contents) == 4 else None
        }
    except:
        print(element)
        raise



def _get_ca_table_close_approaches():
    soup = _get_content(_CA_TABLE_CLOSE_APPROACH_PAGE_URL)
    all_rows = soup.findAll('tr')
    assert all_rows[0].contents[1].contents[0].contents[0].string == 'Asteroid Designation'
    return [_get_ca_table_row(row) for row in all_rows[1:]]



_MP_CLOSE_APPROACH_TABLE_LINK = 'https://minorplanetcenter.net/iau/includes/closeapp_nl.html'

def _get_mp_close_table_row(row):
    try:
        """
        [<td><a href="https://www.minorplanetcenter.net/db_search/show_object?object_id=2023+QE5&amp;commit=Show" target="_blank">2023 QE5</a></td>,
        <td>Oct 02 02:20</td>,
        <td>25.18</td>,
        <td>25-80</td>]
        """
        assert row.name == 'tr'
        assert row.contents[0].contents[0].name == 'a' and 'minorplanetcenter' in row.contents[0].contents[0]['href'] and row.contents[0].contents[0].contents[0].string
        assert row.contents[1].contents[0].string
        assert row.contents[2].contents[0].string
        assert row.contents[3].contents[0].string
        return {
                "ASTEROID_DESIGNATION": row.contents[0].contents[0].contents[0].string,
                "DISCOVERY_STATION": None,
                "CLOSE_APPROACH_DATE_UTC": '2023 ' + row.contents[1].contents[0].string.replace('Oct', '10').replace('Nov', '11'),
                "CLOSE_APPROACH_LUNAR_DISTANCE": float(row.contents[2].contents[0].string),
                "DISCOVERY_ANNOUNCEMENT_LINK": None,
                "LATEST_ORBIT_OBSERVATIONS_LINK": row.contents[0].contents[0]['href'],
                "SIZE_IN_M": row.contents[3].contents[0].string
            }
    except:
        print(row)
        raise

def _get_mp_close_table_approaches():
    soup = _get_content(_MP_CLOSE_APPROACH_TABLE_LINK)
    all_rows = soup.findAll('tr')
    assert len(all_rows[0].contents) == 9
    assert all_rows[0].contents[1].contents[0].string == 'Object'
    assert all_rows[0].contents[3].contents[0].string == 'Date'
    assert all_rows[0].contents[5].contents[0].string == 'Dist' and all_rows[0].contents[5].contents[2].string == '(LD)'
    assert all_rows[0].contents[7].contents[0].string == 'Size' and all_rows[0].contents[7].contents[2].string == '(m)'
    return [_get_mp_close_table_row(row) for row in all_rows[1:]]


def _get_all_merged_close_approaches():
    all_closed_approaches = _get_close_approaches()
    all_ca_table_closed_approaches = _get_ca_table_close_approaches()
    all_mp_close_table_approaches = _get_mp_close_table_approaches()
    data_map = defaultdict(dict)
    for app in all_closed_approaches:
        data_map[app['ASTEROID_DESIGNATION']]['app'] = app
    for ca_app in all_ca_table_closed_approaches:
        data_map[ca_app['ASTEROID_DESIGNATION']]['ca_app'] = ca_app
    for mp_app in all_mp_close_table_approaches:
        data_map[mp_app['ASTEROID_DESIGNATION']]['mp_app'] = mp_app

    merged_approaches = []
    for data_to_merge in data_map.values():
        if len(data_to_merge) == 1:
            merged_approaches.append(list(data_to_merge.values())[0])
        else:
            all_keys = set(list(data_to_merge.get('app', {}).keys()) + list(data_to_merge.get('ca_app', {}).keys()) + list(data_to_merge.get('mp_app', {}).keys()))
            merged_data = {
                k: data_to_merge.get('app', {}).get(k) or data_to_merge.get('ca_app', {}).get(k) or data_to_merge.get('mp_app', {}).get(k)
                for k in all_keys
            }
            merged_approaches.append(merged_data)
    return merged_approaches

if __name__ == '__main__':
    all_merged_approaches = _get_all_merged_close_approaches()
    all_merged_approaches.sort(key=lambda x: x['CLOSE_APPROACH_DATE_UTC'], reverse=True)
    with open(get_relative_directory(__file__, 'close_approach.json'), 'w') as f:
        json.dump(all_merged_approaches, f)



