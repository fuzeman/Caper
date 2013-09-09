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

        print '[NEXT_FRAGMENT: "%s"]' % fragment.value
        return fragment

    def rewind(self, amount=1):
        self._position -= amount

        print '[REWIND: %s]' % amount

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

    def execute(self, parser):
        if self.is_complete():
            return

        if self.regex:
            match = self.capture_group.parser.matcher.parser_match(parser, self.regex)
            print '[REGEX] %s' % self.tag
            if match:
                self.match_found(match)
                return True
        elif self.func:
            fragment = parser.next_fragment()
            match = self.func(fragment)
            print '[FUNC] %s += "%s"' % (self.tag, match)
            if match:
                self.match_found({self.tag: match})
                return True
        else:
            fragment = parser.next_fragment()
            print '[RAW] %s += "%s"' % (self.tag, fragment.value)
            self.match_found({self.tag: fragment.value})
            return True

        return False

    def is_complete(self):
        return self.single and self.capture_group.parser.result.has_any(self.tag)

    def match_valid(self, match):
        if not match:
            return False

        has_data = False
        for key, value in match.items():
            if value:
                has_data = True

        return has_data

    def match_found(self, match):
        if not self.match_valid(match):
            return

        self.capture_group.parser.result.update(match)

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
        match = self.capture_group.parser.matcher.value_match(value, group, single=True)
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
        print 'capture("%s", "%s", %s, %s)' % (tag, regex, func, single)

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

    def execute(self, once=False):
        while self.parser.fragment_available():
            # Run through the constraints and break on any matches
            for constraint in self.constraints:
                fragment = self.parser.next_fragment()

                if constraint.execute(fragment):
                    print 'capturing broke on "%s" at %s' % (fragment.value, constraint)
                    self.parser.rewind()
                    return
                else:
                    self.parser.rewind()

            # Run through the steps
            complete = []
            for step in self.steps:
                if step.execute(self.parser):
                    pass
                complete.append(step.is_complete())

            # Break if all the steps are complete
            if all(complete):
                print 'all steps complete, breaking'
                return
            elif once:
                self.parser.rewind()
                return
