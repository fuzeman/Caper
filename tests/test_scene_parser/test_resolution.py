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


def test_resolution():
    assert_that(
        caper.parse('Show Name.S01E05.720p-GROUP'),
        has_info('video', {'resolution': '720p'})
    )

    assert_that(
        caper.parse('Show Name.S01E05.1080p'),
        has_info('video', {'resolution': '1080p'})
    )

    assert_that(
        caper.parse('Show Name.S01E05.480p.HDTV-GROUP'),
        has_info('video', {'resolution': '480p'})
    )
