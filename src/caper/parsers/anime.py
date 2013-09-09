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
import re
from caper.parsers.base import Parser


REGEX_EPISODE_ARTIFACTS = re.compile(r'[^a-z0-9]', re.IGNORECASE)


PATTERN_GROUPS = [
    ('identifier', [
        r'S(?P<season>\d+)E(?P<episode>\d+)',
        r'(S(?P<season>\d+))|(E(?P<episode>\d+))',

        r'Ep(?P<episode>\d+)',
        r'(?P<absolute>\d+)',

        r'Episode',
    ]),
    ('video', [
        (r'(?P<h264_profile>%s)', [
            'Hi10P'
        ]),
        (r'.(?P<resolution>%s)', [
            '720p',
            '1080p',

            '960x720',
            '1920x1080'
        ]),
        (r'(?P<source>%s)', [
            'BD'
        ]),
    ]),
    ('audio', [
        (r'(?P<codec>%s)', [
            'FLAC'
        ]),
    ])
]


class AnimeParser(Parser):
    def __init__(self, fragments):
        super(AnimeParser, self).__init__(fragments, PATTERN_GROUPS)

    def capture_group(self, fragment):
        if not fragment.value.startswith('['):
            return None

        if not fragment.value.endswith(']'):
            return None

        return fragment.value[1:-1]

    def run(self):
        self.capture('group', func=self.capture_group)\
            .execute(once=True)

        self.capture('show_name', single=False)\
            .until(value__re='identifier')\
            .until(value__re='video')\
            .execute()

        self.capture('identifier', regex='identifier') \
            .capture('video', regex='video', single=False) \
            .capture('audio', regex='audio', single=False) \
            .execute()

        print
        pprint.pprint(self.result._info)