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
        r'^S(?P<season>\d+)E(?P<episode>\d+)$',
        r'^((S(?P<season>\d+))|(E(?P<episode>\d+)))$',
        r'^(?P<season>\d+)x(?P<episode>\d+)$'
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
            'x264',
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
    def __init__(self):
        super(SceneParser, self).__init__(PATTERN_GROUPS)

    def capture_group(self, fragment):
        if fragment.left_sep == '-':
            return fragment.value

        return None

    def run(self, closures):
        super(SceneParser, self).run(closures)

        self.capture_fragment('show_name', single=False)\
            .until(value__re='identifier')\
            .until(value__re='video')\
            .execute()

        self.capture_fragment('identifier', regex='identifier')\
            .capture_fragment('video', regex='video', single=False)\
            .until(left_sep__eq='-')\
            .execute()

        self.capture_fragment('group', func=self.capture_group)\
            .execute()

        return self.result
