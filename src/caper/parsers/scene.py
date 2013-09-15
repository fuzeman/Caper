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
        (1.0, [
            # S01E01-E02
            ('^S(?P<season>\d+)E(?P<episode_from>\d+)$', '^E(?P<episode_to>\d+)$'),
            # S02E13
            r'^S(?P<season>\d+)E(?P<episode>\d+)$',
            # S01 E13
            (r'^(S(?P<season>\d+))$', r'^(E(?P<episode>\d+))$'),
            # S02
            # E13
            r'^((S(?P<season>\d+))|(E(?P<episode>\d+)))$',
            # 3x19
            r'^(?P<season>\d+)x(?P<episode>\d+)$',

            # 2013.09.15
            (r'^(?P<year>\d{4})$', r'^(?P<month>\d{2})$', r'^(?P<day>\d{2})$'),
            # 09.15.2013
            (r'^(?P<month>\d{2})$', r'^(?P<day>\d{2})$', r'^(?P<year>\d{4})$'),
            # TODO - US/UK Date Format Conflict? will only support US format for now..
            # 15.09.2013
            #(r'^(?P<day>\d{2})$', r'^(?P<month>\d{2})$', r'^(?P<year>\d{4})$'),
            # 130915
            r'^(?P<year_short>\d{2})(?P<month>\d{2})(?P<day>\d{2})$',

            # Season 3 Episode 14
            (r'^Se(ason)?$', r'^(?P<season>\d+)$', r'^Ep(isode)?$', r'^(?P<episode>\d+)$'),
            # Season 3
            (r'^Se(ason)?$', r'^(?P<season>\d+)$'),
            # Episode 14
            (r'^Ep(isode)?$', r'^(?P<episode>\d+)$'),

            # Part.3
            # Part.1.and.Part.3
            ('^Part$', '(?P<part>\d+)'),
        ]),
        (0.5, [
            # 102
            r'^(?P<season>\d{1,2})(?P<episode>\d{2})$'
        ])
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
            'DANiSH',
            'iTALiAN'
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

        self.capture_fragment('identifier', regex='identifier', single=False)\
            .capture_fragment('video', regex='video', single=False)\
            .until(left_sep__eq='-')\
            .execute()

        self.capture_fragment('group', func=self.capture_group)\
            .execute()

        return self.result
