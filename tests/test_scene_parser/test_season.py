# Copyright 2013 Dean Gardiner <gardiner91@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from hamcrest import assert_that

from helpers import setup_path

setup_path()

import logging
from logr import Logr
Logr.configure(logging.DEBUG)

from caper import Caper
from helpers import assert_result
from matchers import has_info
from hamcrest import *

caper = Caper()


def test_season_S00():
    assert_result(caper.parse('Show.Name.S01.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '01'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_season_verbose():
    assert_result(caper.parse('Show.Name.Season.1.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '1'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_range():
    assert_that(
        caper.parse('Show.Name.S01.E01.to.E06.DVDrip.x264'),
        has_info('identifier', {'season': '01', 'episode_from': '01', 'episode_to': '06'})
    )


def test_season_range():
    assert_that(
        caper.parse('Show.Name.S01-S03.DVDrip.x264'),
        has_info('identifier', {'season_from': '01', 'season_to': '03'})
    )
