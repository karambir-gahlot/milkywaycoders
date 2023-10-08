import requests
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from myutils.files import (
    get_relative_directory
)

_LAUNCH_SCHEDULE_PAGE = 'https://spaceflightnow.com/launch-schedule/'

def _get_content(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')

def _get_launch_schedule():
    soup = _get_content(_LAUNCH_SCHEDULE_PAGE)