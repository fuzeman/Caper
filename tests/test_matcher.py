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

from caper import FragmentMatcher
from helpers import create_fragments


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