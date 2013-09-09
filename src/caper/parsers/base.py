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

from caper import FragmentMatcher
from caper.result import CaperResult


class Parser(object):
    def __init__(self, fragments, pattern_groups):
        self.fragments = fragments
        self.result = CaperResult()

        self.matcher = FragmentMatcher(pattern_groups)

        self._match_cache = {}
        self._position = 0

    def run(self):
        raise NotImplementedError()

    def next_fragment(self):
        fragment = self.fragments[self._position]

        self._position += 1
        return fragment

    def rewind(self, amount=1):
        self._position -= amount

    def fragment_available(self):
        return self._position < len(self.fragments)

    def capture(self, tag, regex=None, func=None, single=True):
        return CaptureGroup(self).capture(
            tag,
            regex=regex,
            func=func,
            single=single
        )


class CaptureStep(object):
    REPR_KEYS = ['regex', 'func', 'single']

    def __init__(self, capture_group, tag, regex=None, func=None, single=None):
        #: @type: CaptureGroup
        self.capture_group = capture_group

        #: @type: str
        self.tag = tag
        #: @type: str
        self.regex = regex
        #: @type: function
        self.func = func
        #: @type: bool
        self.single = single

        self.complete = False

    def execute(self, fragment):
        if self.complete:
            return False

        if self.regex:
            match = self.capture_group.parser.matcher.match(fragment.value, self.regex)
            if match:
                self.match_found(match)
                return True
        elif self.func:
            match = self.func(fragment)
            if match:
                self.match_found({self.tag: match})
                return True
        else:
            self.match_found({self.tag: fragment.value})
            return True

        return False

    def match_found(self, match):
        self.capture_group.parser.result.update(match)

        if self.single:
            self.complete = True



    def __repr__(self):
        attribute_values = [key + '=' + repr(getattr(self, key))
                            for key in self.REPR_KEYS
                            if hasattr(self, key) and getattr(self, key)]

        attribute_string = ', ' + ', '.join(attribute_values) if len(attribute_values) > 0 else ''

        return "CaptureStep('%s'%s)" % (self.tag, attribute_string)


class CaptureConstraint(object):
    def __init__(self, capture_group, comparisons=None, **kwargs):
        """Capture constraint object

        :type capture_group: CaptureGroup
        """

        self.capture_group = capture_group

        self.comparisons = comparisons if comparisons else []

        for key, value in kwargs.items():
            key = key.split('__')
            if len(key) != 2:
                continue
            name, method = key

            method = '_compare_' + method
            if not hasattr(self, method):
                continue

            self.comparisons.append((name, getattr(self, method), value))

    def _compare_eq(self, value, expected):
        return value == expected

    def _compare_re(self, value, group):
        match = self.capture_group.parser.matcher.match(value, group)
        return match is not None

    def execute(self, fragment):
        results = []

        for name, method, argument in self.comparisons:
            if not hasattr(fragment, name):
                continue
            value = getattr(fragment, name)

            results.append(method(value, argument))

        return all(results) if len(results) > 0 else False

    def __repr__(self):
        return "CaptureConstraint(comparisons=%s)" % repr(self.comparisons)


class CaptureGroup(object):
    def __init__(self, parser):
        """Capture group object

        :type parser: Parser
        """

        self.parser = parser

        #: @type: list of CaptureStep
        self.steps = []
        #: @type: list of CaptureConstraint
        self.constraints = []

    def capture(self, tag, regex=None, func=None, single=True):
        #print 'capture("%s", "%s", %s, %s)' % (tag, regex, func, single)

        self.steps.append(CaptureStep(
            self, tag,
            regex=regex,
            func=func,
            single=single
        ))

        return self

    def until(self, **kwargs):
        #print 'until()'

        self.constraints.append(CaptureConstraint(self, **kwargs))

        return self

    def execute(self):
        while self.parser.fragment_available():
            fragment = self.parser.next_fragment()

            # Run through the constraints and break on any matches
            for constraint in self.constraints:
                if constraint.execute(fragment):
                    print 'capturing broke on "%s" at %s' % (fragment.value, constraint)
                    self.parser.rewind()
                    return

            for step in self.steps:
                step.execute(fragment)
