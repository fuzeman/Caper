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

from logr import Logr
from caper import FragmentMatcher
from caper.parsers.base import Parser


PATTERN_GROUPS = [
    ('usenet', [
        r'\[(?P<group>#[\w\.@]+)\]',
        r'^\[(?P<code>\w+)\]$',
        r'\[(?P<full>FULL)\]',
        r'\[\s?(?P<group>TOWN)\s?\]',
        r'.*?(?P<site>www\..*?\.\w+)\s?.',
        r'(?P<site>.*?\.(com|org|info))'
    ]),

    ('part', [
        r'.?(?P<current>\d+)/(?P<total>\d+).?'
    ]),

    ('detail', [
        r'[\s-]*\"(?P<file_name>.*?)\"[\s-]*(?P<size>[\d,\.]*\s?MB)?[\s-]*?(?P<extra>yEnc)',
    ])
]


class UsenetParser(Parser):
    matcher = None

    def __init__(self, debug=False):
        if not UsenetParser.matcher:
            UsenetParser.matcher = FragmentMatcher(PATTERN_GROUPS)
            Logr.info("Fragment matcher for %s created", self.__class__.__name__)

        super(UsenetParser, self).__init__(UsenetParser.matcher, debug)

    def run(self, closures):
        """
        :type closures: list of CaperClosure
        """

        self.setup(closures)

        # Capture usenet or part info until we get a part or matching fails
        self.capture_closure('usenet', regex='usenet', single=False)\
            .capture_closure('part', regex='part', single=True) \
            .until_result(tag='part') \
            .until_failure()\
            .execute()

        is_town_release, has_part = self.get_state()

        if not is_town_release:
            self.capture_release_name()

        # If we already have the part (TOWN releases), ignore matching part again
        if not is_town_release and not has_part:
            self.capture_fragment('part', regex='part', single=True) \
                .until_success()\
                .execute()

        # Capture any leftover details
        self.capture_closure('detail', regex='detail', single=False)\
            .execute()

        self.result.build()
        return self.result

    def capture_release_name(self):
        self.capture_closure('detail', regex='detail', single=False) \
            .until_failure() \
            .execute()

        self.capture_fragment('release_name', single=False) \
            .until(fragment__re='part') \
            .until(fragment__re='usenet') \
            .execute()

    def get_state(self):
        # TODO multiple-chains?
        is_town_release = False
        has_part = False

        for tag, result in self.result.heads[0].captured():
            if tag == 'usenet' and result.get('group') == 'TOWN':
                is_town_release = True

            if tag == 'part':
                has_part = True

        return is_town_release, has_part
