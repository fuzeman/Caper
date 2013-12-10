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


def test_basic():
    result = caper.parse(
        '[#abc.123@network][12345] Show.Name.S03E03.WEBRip.x264-GROUP [1/33] - "show.name.303.x264-group.r05" yEnc',
        'usenet'
    )

    assert_that(result, has_info('detail', {'file_name': 'show.name.303.x264-group.r05', 'extra': 'yEnc'}))

    assert_that(result, has_info('part', {'current': '1', 'total': '33'}))

    assert_that(result, has_info('release_name', ['Show', 'Name', 'S03E03', 'WEBRip', 'x264', 'GROUP']))

    assert_that(result, has_info('usenet', {'group': '#abc.123@network'}))
    assert_that(result, has_info('usenet', {'code': '12345'}))


def test_alternative():
    result = caper.parse(
        '[123456]-[FULL]-[#abc.123]-[ Show.Name.S03E05.720p.WEB-DL.DD5.1.H.264-GROUP ]-[1/1] - "Show.Name.S03E05.WEB-DL.DD5.1.H.264-GROUP.nzb" yEnc',
        'usenet'
    )

    assert_that(result, has_info('detail', {'file_name': 'Show.Name.S03E05.WEB-DL.DD5.1.H.264-GROUP.nzb', 'extra': 'yEnc'}))

    assert_that(result, has_info('part', {'current': '1', 'total': '1'}))

    assert_that(result, has_info('release_name', ['', 'Show', 'Name', 'S03E05', '720p', 'WEB', 'DL', 'DD5', '1', 'H', '264', 'GROUP']))

    assert_that(result, has_info('usenet', {'group': '#abc.123'}))
    assert_that(result, has_info('usenet', {'code': '123456'}))


def test_town_style():
    result = caper.parse(
        '[ TOWN ]-[ www.example.org ]-[ partner of www.example.com ] [01/18] - "Show.Name.S03E05.HDTV.x264-GROUP.par2" - 321,23 MB yEnc',
        'usenet'
    )

    assert_that(result, has_info('detail', {'file_name': 'Show.Name.S03E05.HDTV.x264-GROUP.par2', 'extra': 'yEnc', 'size': '321,23 MB'}))

    assert_that(result, has_info('part', {'current': '01', 'total': '18'}))

    assert_that(result, has_info('usenet', {'group': 'TOWN'}))
    assert_that(result, has_info('usenet', {'site': 'www.example.org'}))
    assert_that(result, has_info('usenet', {'site': 'www.example.com'}))


# TODO this isn't supported *yet*
# def test_bare():
#     result = caper.parse(
#         '[01/18] - "Show.Name.S03E05.HDTV.x264-GROUP.par2" yEnc',
#         'usenet'
#     )
#
#     assert_that(result, has_info('detail', {'file_name': 'Show.Name.S03E05.HDTV.x264-GROUP.par2', 'extra': 'yEnc'}))
#
#     assert_that(result, has_info('part', {'current': '01', 'total': '18'}))
