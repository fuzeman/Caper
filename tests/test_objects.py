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

from helpers import create_fragments, get_fragment_values


def test_fragment_take():
    fragments = create_fragments('a.b.c.123')

    assert get_fragment_values(fragments[0].take_right(2)) == ['a', 'b']
    assert get_fragment_values(fragments[0].take_right(6)) == ['a', 'b', 'c', '123', None, None]

    assert get_fragment_values(fragments[3].take_left(2)) == ['123', 'c']
    assert get_fragment_values(fragments[2].take_left(6)) == ['c', 'b', 'a', None, None, None]
