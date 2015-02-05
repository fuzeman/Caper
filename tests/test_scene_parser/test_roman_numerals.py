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


def test_roman_numerals():
    assert_that(
        caper.parse('Show.Name.Part.III.DVDrip.x264'),
        has_info('identifier', {'part': 3})
    )

    assert_that(
        caper.parse('Show.Name.Part.IV.DVDrip.x264'),
        has_info('identifier', {'part': 4})
    )

    assert_that(
        caper.parse('Show.Name.Part.XI.DVDrip.x264'),
        has_info('identifier', {'part': 11})
    )
