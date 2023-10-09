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
    ALL_SATELLITES_SATCAT_DATA,
    SATCAT_BY_NORAD_CAT_ID,
    find_neighbours
)
from mock_data.space_track.conjunctions import (
    CONJUNCTIONS
)
from mock_data.space_track.decay import (
    get_decay_impacting_my_satellites
)
from mock_data.asteroids.close_approach import (
    CLOSE_APPROACH_DATA, get_close_approach_impacting_my_satellite
)
from space_weather.proton_data import (
    PROTON_DATA,
    PROTON_SERIES_10,
    PROTON_SERIES_50,
    PROTON_SERIES_100
)
from space_weather.solar_flux import (
    SOLAR_FLUX_DATA
)
from space_weather.magnetometers import (
    MAGNETOMETERS_DATA
)
from space_weather.xray_flares import (
    XRAY_FLARES_DATA
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
    app.logger.info('User satellites: ' + ','.join(my_satellites_ids))
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
    app.logger.info('User satellites: ' + ','.join(my_satellites_ids))
    my_satellites = [SATCAT_BY_NORAD_CAT_ID[sid] for sid in my_satellites_ids]
    return render_template(
        'main.html',
        selected_main_tab='home',
        all_satellites=ALL_SATELLITES_SATCAT_DATA,
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

@app.route('/asteroids')
def asteroids_page():
    my_satellites = _get_mysatellites()
    close_approaches_data = get_close_approach_impacting_my_satellite(my_satellites)
    impacting_approaches = close_approaches_data['impacting_approaches']
    non_impacting_approaches = close_approaches_data['non_impacting_approaches']
    return render_template(
        'asteroids.html',
        selected_main_tab='asteroids',
        impacting_approaches=impacting_approaches,
        non_impacting_approaches=non_impacting_approaches
    )


@app.route('/space_weather')
def space_weather_page():
    solar_flux_x_values = [d['Date'] for d in SOLAR_FLUX_DATA]
    solar_flux_observed_y_values = [d['Observed Flux'] for d in SOLAR_FLUX_DATA]
    solar_flux_ursi_flux_y_values = [d['URSI Flux'] for d in SOLAR_FLUX_DATA]
    proton_10_x_values = [p['DISPLAY_TIME'] for p in PROTON_SERIES_10]
    proton_10_y_values = [p['flux'] for p in PROTON_SERIES_10]
    proton_50_y_values = [p['flux'] for p in PROTON_SERIES_50]
    proton_100_y_values = [p['flux'] for p in PROTON_SERIES_100]
    magnetometers_x_values = [p['DISPLAY_TIME'] for p in MAGNETOMETERS_DATA]
    magnetometers_y_values = [p['Hp'] for p in MAGNETOMETERS_DATA]
    xray_flares_x_values = [p['DISPLAY_TIME'] for p in XRAY_FLARES_DATA]
    xray_flares_y_values = [p['max_xrlong'] for p in XRAY_FLARES_DATA]
    return render_template(
        'space_weather.html',
        selected_main_tab='space_weather',
        solar_flux_x_values=solar_flux_x_values,
        solar_flux_observed_y_values=solar_flux_observed_y_values,
        solar_flux_ursi_flux_y_values=solar_flux_ursi_flux_y_values,
        proton_10_x_values=proton_10_x_values,
        proton_10_y_values=proton_10_y_values,
        proton_50_y_values=proton_50_y_values,
        proton_100_y_values=proton_100_y_values,
        magnetometers_x_values=magnetometers_x_values,
        magnetometers_y_values=magnetometers_y_values,
        xray_flares_x_values=xray_flares_x_values,
        xray_flares_y_values=xray_flares_y_values
    )

@app.route('/decay')
def decay_page():
    my_satellites = _get_mysatellites()
    impacting_decay_data = get_decay_impacting_my_satellites(my_satellites)
    return render_template(
        'decay.html',
        selected_main_tab='decay',
        impacting_decay_data=impacting_decay_data
    )

@app.route('/nearbysatellites')
def nearbysatellites_page():
    my_satellites = _get_mysatellites()
    neighbours_data = find_neighbours(my_satellites)
    return render_template(
        'nearbysatellites.html',
        selected_main_tab='nearbysatellites',
        neighbours_data=neighbours_data
    )