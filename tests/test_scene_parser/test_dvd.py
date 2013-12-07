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

from helpers import setup_path
setup_path()

import logging
from logr import Logr
Logr.configure(logging.DEBUG)

from caper import Caper
from matchers import has_info
from hamcrest import *

caper = Caper()


def test_dvd_region():
    assert_that(
        caper.parse('Show Name (2011) S01 R1 NTSC'),
        has_info('dvd', {'region': '1'})
    )

    assert_that(
        caper.parse('Show Name (2011) S01 R4 PAL'),
        has_info('dvd', {'region': '4'})
    )


def test_dvd_encoding():
    assert_that(
        caper.parse('Show Name (2011) S01 R1 NTSC'),
        has_info('dvd', {'encoding': 'NTSC'})
    )

    assert_that(
        caper.parse('Show Name (2011) S01 R4 PAL'),
        has_info('dvd', {'encoding': 'PAL'})
    )


def test_dvd_disc():
    assert_that(
        caper.parse('Show Name (2011) S01 R1 NTSC DISC3'),
        has_info('dvd', {'disc': '3'})
    )

    assert_that(
        caper.parse('Show Name (2011) S01 R4 PAL D2'),
        has_info('dvd', {'disc': '2'})
    )
