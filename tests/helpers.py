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

import sys
import os


def setup_path():
    src_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

    if src_path not in sys.path:
        sys.path.insert(0, src_path)
setup_path()

from caper import CaperFragment
from caper.helpers import xrange_six


def create_fragments(value):
    """Create fragments from a dot ('.') separated string

    :type value: str

    :rtype : list of CaperFragment
    """
    fragment_values = value.split('.')
    fragments = []

    for x in xrange_six(len(fragment_values)):
        fragment = CaperFragment()
        fragment.value = fragment_values[x]

        if x > 0:
            fragment.left = fragments[x - 1]
            fragments[x - 1].right = fragment

        fragments.append(fragment)

    return fragments


def get_fragment_values(fragments):
    return [(fragment.value if fragment else None) for fragment in fragments]
