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

from caper import FragmentMatcher
from matchers import matches_dict
from helpers import create_fragments
from hamcrest import assert_that, none
import pytest


def test_matcher_construction():
    matcher = FragmentMatcher([
        ('test', [
            (1.0, [
                ()
            ]),
            (1.0, [
                (r'^abc$', r'^1234$'),
            ])
        ]),
        ('test3', [
            (r'(?P<resolution>%s)', [
                '480p',
                '720p',
                '1080p'
            ]),
        ])
    ])

    assert matcher.find_group('test2') is None


def test_fragment_match():
    matcher = FragmentMatcher([
        ('test', [
            (1.0, [
                (r'^abc$', r'^123$'),
            ]),
            (0.8, [
                (r'^abc$', r'^1234$'),
            ])
        ])
    ])

    assert matcher.fragment_match(create_fragments('abc.123')[0], 'test')[0] == 1

    assert matcher.fragment_match(create_fragments('abc.12')[0], 'test')[0] == 0

    assert matcher.fragment_match(create_fragments('abc')[0], 'test')[0] == 0

    assert matcher.fragment_match(create_fragments('abc.1234')[0], 'test')[0] == 0.8

    assert matcher.fragment_match(create_fragments('abc.456')[0], 'test')[0] == 0

    assert matcher.fragment_match(create_fragments('def.123')[0], 'test')[0] == 0

    matcher = FragmentMatcher([
        ('test', [
            (1.0, [
                ()
            ]),
            (1.0, [
                (r'^abc$', r'^1234$'),
            ])
        ])
    ])

    assert matcher.fragment_match(create_fragments('abc.1234')[0], 'test')[0] == 1


def test_value_match():
    matcher = FragmentMatcher([
        ('test', [
            (1.0, [
                r'^(?P<a>abc)$',
            ]),
            (0.8, [
                r'^(?P<b>1234)$',
            ])
        ]),
        ('test2', [
            (1.0, [
                r'^(?P<a>abcdefg)$',
            ]),
        ])
    ])

    assert_that(matcher.value_match('abc'), matches_dict({'test': {'a': 'abc'}}))

    assert_that(matcher.value_match('abcdefg', 'test2'), matches_dict({'test2': {'a': 'abcdefg'}}))

    assert_that(matcher.value_match('abcd'), none())


if __name__ == '__main__':
    pytest.main()
