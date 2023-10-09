import json
import csv
from myutils.files import (
    load_csv
)


SOLAR_FLUX_DATA = load_csv(
    __file__, '../src/data/SolarFlux.csv'
)

def _process_data(solar_flux_data):
    for sf in solar_flux_data:
        sf['Observed Flux'] = float(sf['Observed Flux'])
        sf['Adjusted Flux'] = float(sf['Adjusted Flux'])
        sf['URSI Flux'] = float(sf['URSI Flux'])
