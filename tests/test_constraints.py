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
import re

from helpers import setup_path

setup_path()

import logging
from logr import Logr
Logr.configure(logging.DEBUG)

from caper import Caper, FragmentMatcher
from caper.parsers.base import Parser
from caper.group import CaptureGroup
from caper.objects import CaperClosure
from caper.result import CaperResult
from matchers import has_info
from helpers import assert_result
from hamcrest import *
import pytest

caper = Caper()


class DummyParser(Parser):
    def __init__(self, pattern_groups, debug=False):
        super(DummyParser, self).__init__(FragmentMatcher(pattern_groups), debug)


def build_parser(name='Show.Name.S01E03-GROUP'):
    parser = DummyParser([
        ('identifier', [
            (1.0, [
                r'^S(?P<season>\d+)E(?P<episode>\d+)$',
            ])
        ])
    ])

    # Parse test name into closures
    closures = caper._closure_split(name)
    closures = caper._fragment_split(closures)
    parser.setup(closures)

    return parser


def test_fragment_constraint():
    parser = build_parser()

    # Capture show name until we hit the identifier
    group = CaptureGroup(parser, parser.result)\
        .capture_fragment('show_name', single=False)\
        .until(fragment__re='identifier')

    # TODO test CaptureStep.__repr__ properly
    repr(group.steps)

    group.execute()

    # Build the result from tree
    parser.result.build()

    # Ensure result is valid
    assert_result(parser.result, (1.0, {
        'show_name': ['Show', 'Name']
    }))


def test_pattern_constraint():
    parser = build_parser()

    # Capture show name until we hit the identifier
    CaptureGroup(parser, parser.result) \
        .capture_fragment('show_name', single=False) \
        .until(right_sep__re=re.compile('^-$')) \
        .execute()

    # Build the result from tree
    parser.result.build()

    # Ensure result is valid
    assert_result(parser.result, (1.0, {
        'show_name': ['Show', 'Name']
    }))


def test_value_constraint():
    parser = build_parser()

    # Capture show name until we hit the identifier
    CaptureGroup(parser, parser.result) \
        .capture_fragment('show_name', single=False) \
        .until(value__re='identifier') \
        .execute()

    # Build the result from tree
    parser.result.build()

    # Ensure result is valid
    assert_result(parser.result, (1.0, {
        'show_name': ['Show', 'Name']
    }))


def test_invalid_attribute():
    parser = build_parser()

    # Capture show name until we hit the identifier
    with pytest.raises(ValueError) as exc:
        CaptureGroup(parser, parser.result) \
            .capture_fragment('show_name', single=False) \
            .until(blah__re='identifier') \
            .execute()

    assert_that(
        str(exc.value),
        equal_to("Unable to find attribute with name 'blah'")
    )
