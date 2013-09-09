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

from caper.matcher import FragmentMatcher
from caper.parsers.anime import AnimeParser
from caper.parsers.scene import SceneParser


FRAGMENT_SEPARATORS = ['.', '-', '_', ' ']


class Caper(object):
    def _split(self, name):
        fragments = []
        cur_position = 0
        cur = CaperFragment()

        def end_fragment(fragments, cur, cur_position):
            cur.position = cur_position

            cur.left = fragments[len(fragments) - 1] if len(fragments) > 0 else None
            if cur.left:
                cur.left_sep = cur.left.right_sep
                cur.left.right = cur

            cur.right_sep = ch

            fragments.append(cur)

        for x, ch in enumerate(name):
            if ch in FRAGMENT_SEPARATORS:
                end_fragment(fragments, cur, cur_position)

                # Reset
                cur = CaperFragment()
                cur_position += 1
            else:
                cur.value += ch

        if cur.value != "":
            end_fragment(fragments, cur, cur_position)

        return fragments

    def parse(self, name):
        fragments = self._split(name)

        # TODO multi-parser autodetection
        parser = AnimeParser(fragments)
        parser.run()


class CaperFragment(object):
    def __init__(self):
        self.value = ""

        self.left = None
        self.left_sep = None

        self.right = None
        self.right_sep = None

        self.position = None