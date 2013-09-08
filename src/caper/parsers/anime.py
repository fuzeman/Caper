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


REGEX_SPECIAL_CHAR = re.compile(r'[^a-z0-9]', re.IGNORECASE)


PATTERN_GROUPS = [
    ('identifier', [
        r'(?P<absolute>\d+)'
    ]),
    ('video', [
        (r'(?P<h264_profile>%s)', [
            'Hi10P'
        ]),
        (r'.(?P<resolution>%s)', [
            '960x720',
            '1920x1080'
        ]),
        (r'(?P<source>%s)', [
            'BD'
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

    def until_show_name(self, fragment):
        if not fragment.right:
            return False

        print fragment

        if REGEX_SPECIAL_CHAR.match(fragment.right.value):
            return True

        return False


    def run(self):
        self.capture('group', capture_func=self.capture_group)

        self.capture('show_name', until_func=self.until_show_name)

        self.capture('identifier', capture_regex='identifier')

        self.capture('video', capture_regex='video', until__left_sep__eq='-')

        print
        pprint.pprint(self.result._info)