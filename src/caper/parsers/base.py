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


from caper import FragmentMatcher
from caper.result import CaperResult


class Parser(object):
    def __init__(self, fragments, pattern_groups):
        self.fragments = fragments
        self.result = CaperResult()

        self._matcher = FragmentMatcher(pattern_groups)
        self._match_cache = {}
        self._current_position = 0

    def run(self):
        raise NotImplementedError()

    def _next(self):
        fragment = self.fragments[self._current_position]

        self._current_position += 1
        return fragment

    def _back(self):
        self._current_position -= 1

    def _match(self, value, regex_group):
        print 'match("%s", "%s")' % (value, regex_group)

        match = self._matcher.match(value, regex_group)

        if match:
            print "\tmatch found"
            return match

        return None

    def _is_match(self, value, regex_group):
        return self._match(value, regex_group) is not None

    def _until(self, fragment, until_func=None, **kwargs):
        if until_func and until_func(fragment):
            return True

        for key in kwargs:
            argument = kwargs[key]
            if not argument:
                continue

            # Get name and method from key
            key = key.split('__')
            if len(key) != 2:
                continue
            name, method_name = key

            # Get value from fragment
            if not hasattr(fragment, name):
                continue
            target = getattr(fragment, name)

            # Get method
            if not hasattr(self, '_until_' + method_name):
                continue
            method = getattr(self, '_until_' + method_name)

            if method(target, argument):
                return True

        return False

    def _until_re(self, target, argument):
        return self._is_match(target, argument)

    def _until_eq(self, target, argument):
        return target == argument

    def capture(self, tag, capture_regex=None, until_func=None, capture_func=None, **kwargs):
        print 'capture("%s", "%s")' % (tag, capture_regex)

        if capture_regex and capture_func:
            raise ValueError("Unable to call capture() with capture_regex and capture_func.")

        until_kwargs = {}
        for key, value in kwargs.items():
            if key.startswith('until__') and value:
                until_kwargs[key[7:]] = value

        while self._current_position < len(self.fragments):
            fragment = self._next()

            if self._until(fragment, until_func, **until_kwargs) :
                print '\t', 'until break on "%s"' % fragment.value
                self._back()
                return

            if capture_regex:
                match = self._match(fragment.value, capture_regex)
                if match:
                    self.result.update(match)
            else:
                value = capture_func(fragment) if capture_func else fragment.value
                if value:
                    self.result.update({tag: value})

            print '\t', fragment.value

            # Return if this is just a single capture
            if len(until_kwargs) == 0 and not until_func:
                return
