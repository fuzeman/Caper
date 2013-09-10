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

from caper.matcher import FragmentMatcher
from caper.parsers.anime import AnimeParser
from caper.parsers.scene import SceneParser


CL_START_CHARS = ['(', '[']
CL_END_CHARS = [')', ']']

STRIP_START_CHARS = ''.join(CL_START_CHARS)
STRIP_END_CHARS = ''.join(CL_END_CHARS)
STRIP_CHARS = ''.join(['_', ' ', '.'])

FRAGMENT_SEPARATORS = ['.', '-', '_', ' ']


CL_START = 0
CL_END = 1


class Caper(object):
    def _closure_split(self, name):
        closures = []

        def end_closure(closures, buf):
            buf = buf.strip(STRIP_CHARS)
            if len(buf) < 1:
                return

            closures.append(CaperClosure(buf))

        state = CL_START
        buf = ""
        for x, ch in enumerate(name):
            if state == CL_START and ch in CL_START_CHARS:
                end_closure(closures, buf)

                state = CL_END
                buf = ""

            buf += ch

            if state == CL_END and ch in CL_END_CHARS:
                end_closure(closures, buf)

                state = CL_START
                buf = ""

        end_closure(closures, buf)

        return closures

    def _clean_closure(self, closure):
        return closure.lstrip(STRIP_START_CHARS).rstrip(STRIP_END_CHARS)

    def _fragment_split(self, closures):
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

        for closure in closures:
            closure.fragments = []

            for x, ch in enumerate(self._clean_closure(closure.value)):
                if ch in FRAGMENT_SEPARATORS:
                    end_fragment(closure.fragments, cur, cur_position)

                    # Reset
                    cur = CaperFragment()
                    cur_position += 1
                else:
                    cur.value += ch

            # Finish parsing the last fragment
            if cur.value != "":
                end_fragment(closure.fragments, cur, cur_position)

                # Reset
                cur_position = 0
                cur = CaperFragment()

        return closures

    def parse(self, name):
        fragments = self._split(name)

        # TODO autodetect the parser type
        parser = AnimeParser(fragments)
        parser.run()


class CaperClosure(object):
    def __init__(self, value):
        self.value = value

        self.fragments = None


class CaperFragment(object):
    def __init__(self):
        self.value = ""

        self.left = None
        self.left_sep = None

        self.right = None
        self.right_sep = None

        self.position = None