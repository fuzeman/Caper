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

from hamcrest.core.base_matcher import BaseMatcher


class HasInfo(BaseMatcher):
    def __init__(self, group, match):
        self.group = group
        self.match = match

    def matches(self, item, mismatch_description=None):
        if not hasattr(item, 'chains') or len(item.chains) < 1:
            return False

        if self.group not in item.chains[0].info:
            return False

        return self.match in item.chains[0].info[self.group]

    def describe_to(self, description):
        description.append_text('result with the group ')\
                   .append_text(self.group)\
                   .append_text(', containing the match ')\
                   .append_text(str(self.match))


def has_info(group, match):
    return HasInfo(group, match)


class MatchesDict(BaseMatcher):
    def __init__(self, value):
        self.value = value

    @classmethod
    def recursive_match(cls, d, d2):
        if not d or not d2:
            return False

        for ak, av in d.items():
            if ak not in d2:
                return False

            if type(av) is dict and not cls.recursive_match(av, d2[ak]):
                return False
            elif av != d2[ak]:
                return False

        return True

    def matches(self, item, mismatch_description=None):
        return self.recursive_match(self.value, item)

    def describe_to(self, description):
        pass


def matches_dict(value):
    return MatchesDict(value)
