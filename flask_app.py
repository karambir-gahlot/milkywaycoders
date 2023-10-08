from flask import (
    Flask,
    render_template,
    request
)
# from mysql import (
#     init_mysql,
#     get_test_sql_data
# )
from mock_data.space_track.satcat import (
    SATCAT_DATA,
    SATCAT_BY_NORAD_CAT_ID
)
from mock_data.space_track.conjunctions import (
    CONJUNCTIONS
)

app = Flask(__name__)
# init_mysql(app)

def _get_mysatellites_ids():
    result = request.cookies.get('mysatellites')
    if result:
        result = result.split(',')
        result = [r for r in result if r in SATCAT_BY_NORAD_CAT_ID]
        return result
    return []

def _get_mysatellites():
    my_satellites_ids = _get_mysatellites_ids()
    app.logger.info("User satellites: ", ','.join(my_satellites_ids))
    my_satellites = [SATCAT_BY_NORAD_CAT_ID[sid] for sid in my_satellites_ids]
    return my_satellites

def _get_my_conjunctions(my_satellites):
    my_satellites_ids = set(s['NORAD_CAT_ID'] for s in my_satellites)
    return [
        c for c in CONJUNCTIONS
        # TODO: remove duplicate conjunctions by some algorithm
        # if c['SAT_1_ID'] in my_satellites_ids or c['SAT_2_ID'] in my_satellites_ids
        if c['SAT_1_ID'] in my_satellites_ids
    ]

@app.route('/')
def home_page():
    # app.logger.info("Testing mysql db TestTable")
    # test_app_info = get_test_sql_data()
    # app.logger.info("AppName %s, AppID %s", test_app_info['AppName'], test_app_info['AppID'])
    my_satellites_ids = _get_mysatellites_ids()
    app.logger.info("User satellites: ", ','.join(my_satellites_ids))
    my_satellites = [SATCAT_BY_NORAD_CAT_ID[sid] for sid in my_satellites_ids]
    return render_template(
        'main.html',
        selected_main_tab='home',
        all_satellites=SATCAT_DATA,
        my_satellites_ids=my_satellites_ids,
        my_satellites=my_satellites
    )

@app.route('/conjunctions')
def conjunctions_page():
    my_satellites = _get_mysatellites()
    my_conjunctions = _get_my_conjunctions(my_satellites)
    return render_template(
        'conjunctions.html',
        selected_main_tab='conjunctions',
        my_conjunctions=my_conjunctions
    )