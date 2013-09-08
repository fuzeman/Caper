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


class FragmentMatcher(object):
    def __init__(self, pattern_groups):
        self.regex = {}

        for group_name, patterns in pattern_groups:
            if group_name not in self.regex:
                self.regex[group_name] = []

            for pattern in patterns:
                # Format extended patterns
                if type(pattern) is tuple:
                    pattern = pattern[0] % '|'.join(pattern[1])

                self.regex[group_name].append(re.compile(pattern, re.IGNORECASE))

    def match(self, value, group_name=None, single=True):
        result = None

        for group, patterns in self.regex.items():
            if group_name and group != group_name:
                continue

            for pattern in patterns:
                match = pattern.match(value)

                if match:
                    if result is None:
                        result = {}
                    if group not in result:
                        result[group] = {}

                    result[group].update(match.groupdict())

                    if single:
                        return result

        return result
