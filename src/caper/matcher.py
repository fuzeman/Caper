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

import re
from logr import Logr
from caper.helpers import is_list_type


class FragmentMatcher(object):
    def __init__(self, pattern_groups):
        self.regex = {}

        for group_name, patterns in pattern_groups:
            if group_name not in self.regex:
                self.regex[group_name] = []

            for pattern in patterns:
                if type(pattern) is str:
                    pattern = (pattern,)

                if type(pattern) is tuple and len(pattern) == 2:
                    if is_list_type(pattern[1], str):
                        pattern = (pattern,)

                result = []
                for value in pattern:
                    if type(value) is tuple:
                        if len(value) == 2:
                            value = value[0] % '|'.join(value[1])
                        elif len(value) == 1:
                            value = value[0]

                    result.append(re.compile(value, re.IGNORECASE))

                result = tuple(result)

                self.regex[group_name].append(result)

    def parser_match(self, parser, group_name, single=True):
        """

        :type parser: caper.parsers.base.Parser
        """
        result = None

        for group, patterns in self.regex.items():
            if group_name and group != group_name:
                continue

            for pattern in patterns:
                fragments = []
                pattern_matched = True
                pattern_result = {}

                for fragment_pattern in pattern:
                    if not parser.fragment_available():
                        pattern_matched = False
                        break

                    fragment = parser.next_fragment()
                    fragments.append(fragment)

                    Logr.debug('[r"%s"].match("%s")', fragment_pattern.pattern, fragment.value)
                    match = fragment_pattern.match(fragment.value)
                    if match:
                        Logr.debug('Pattern "%s" matched', fragment_pattern.pattern)
                    else:
                        pattern_matched = False
                        break

                    pattern_result.update(match.groupdict())

                if pattern_matched:
                    if result is None:
                        result = {}

                    if group not in result:
                        result[group] = {}

                    Logr.debug('Matched on <%s>', ' '.join([f.value for f in fragments]))

                    result[group].update(pattern_result)
                    parser.commit()

                    if single:
                        return result
                else:
                    parser.rewind()

    def value_match(self, value, group_name=None, single=True):
        result = None

        for group, patterns in self.regex.items():
            if group_name and group != group_name:
                continue

            for pattern in patterns:
                match = pattern[0].match(value)
                if not match:
                    continue

                if result is None:
                    result = {}
                if group not in result:
                    result[group] = {}

                result[group].update(match.groupdict())

                if single:
                    return result

        return result
