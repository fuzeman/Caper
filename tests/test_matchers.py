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

import pytest
from matchers import MatchesDict


def test_has_info():
    pass


def test_matches_dict():
    assert MatchesDict.recursive_match({'one': 1}, {'one': 1}) is True

    assert MatchesDict.recursive_match({'one': 1}, {'one': 2}) is False
    assert MatchesDict.recursive_match({'one': 2}, {'one': 1}) is False

    assert MatchesDict.recursive_match({'one': 1, 'two': 2}, {'one': 1}) is False
    assert MatchesDict.recursive_match({'one': 1}, {'one': 1, 'two': 2}) is True

    assert MatchesDict.recursive_match({'one': 1, 'two': {'a': 5}}, {'one': 1, 'two': {'a': 5}}) is True
    assert MatchesDict.recursive_match({'one': 1, 'two': {'a': 5}}, {'one': 1, 'two': {'a': 6}}) is False
    assert MatchesDict.recursive_match({'one': 1, 'two': 5}, {'one': 1, 'two': {'a': 5}}) is False


if __name__ == '__main__':
    pytest.main()
