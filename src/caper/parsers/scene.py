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


import pprint
from caper.parsers.base import Parser


PATTERN_GROUPS = [
    ('identifier', [
        r'S(?P<season>\d+)E(?P<episode>\d+)',
        r'(S(?P<season>\d+))|(E(?P<episode>\d+))',
        r'(?P<season>\d+)x(?P<episode>\d+)'
    ]),
    ('video', [
        r'(?P<aspect>FS|WS)',

        (r'(?P<source>%s)', [
            'HDTV',
            'PDTV',
            'DSR',
            'DVDRiP'
        ]),

        (r'(?P<codec>%s)', [
            'XViD'
        ]),

        (r'(?P<language>%s)', [
            'GERMAN',
            'DUTCH',
            'FRENCH',
            'SWEDiSH',
            'DANiSH'
        ]),
    ])
]


class SceneParser(Parser):
    def __init__(self, fragments):
        super(SceneParser, self).__init__(fragments, PATTERN_GROUPS)

    def capture_group(self, fragment):
        if fragment.left_sep == '-':
            return fragment.value

        return None

    def run(self):
        self.capture('show_name', until__value__re='identifier')

        self.capture('identifier', capture_regex='identifier')

        self.capture('video', capture_regex='video', until__left_sep__eq='-')

        self.capture('group', capture_func=self.capture_group)

        print
        pprint.pprint(self.result._info)