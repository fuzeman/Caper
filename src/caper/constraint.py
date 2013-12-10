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


class CaptureConstraint(object):
    def __init__(self, capture_group, constraint_type, comparisons=None, **kwargs):
        """Capture constraint object

        :type capture_group: CaptureGroup
        """

        self.capture_group = capture_group

        self.constraint_type = constraint_type

        self.comparisons = comparisons if comparisons else []
        self.kwargs = {}

        for orig_key, value in kwargs.items():
            key = orig_key.split('__')
            if len(key) != 2:
                self.kwargs[orig_key] = value
                continue
            name, method = key

            method = '_compare_' + method
            if not hasattr(self, method):
                self.kwargs[orig_key] = value
                continue

            self.comparisons.append((name, getattr(self, method), value))

    def _compare_eq(self, fragment, name, expected):
        if not hasattr(fragment, name):
            return 1.0, False

        return 1.0, getattr(fragment, name) == expected

    def _compare_re(self, node, name, arg):
        if name == 'fragment':
            group, minimum_weight = arg if type(arg) is tuple and len(arg) > 1 else (arg, 0)

            weight, match, num_fragments = self.capture_group.parser.matcher.fragment_match(node, group)
            return weight, weight > minimum_weight
        elif name == 'closure':
            group, minimum_weight = arg if type(arg) is tuple and len(arg) > 1 else (arg, 0)

            weight, match, num_fragments = self.capture_group.parser.matcher.fragment_match(node, group)
            return weight, weight > minimum_weight
        elif type(arg).__name__ == 'SRE_Pattern':
            return 1.0, arg.match(getattr(node, name)) is not None
        elif hasattr(node, name):
            match = self.capture_group.parser.matcher.value_match(getattr(node, name), arg, single=True)
            return 1.0, match is not None
        else:
            raise ValueError("Unable to find attribute with name '%s'" % name)

    def execute(self, parent_node, fragment, **kwargs):
        func_name = 'constraint_%s' % self.constraint_type

        if hasattr(self, func_name):
            return getattr(self, func_name)(parent_node, fragment, **kwargs)

        raise ValueError('Unknown constraint type "%s"' % self.constraint_type)

    def constraint_match(self, parent_node, fragment):
        results = []
        total_weight = 0

        for name, method, argument in self.comparisons:
            weight, success = method(fragment, name, argument)
            total_weight += weight
            results.append(success)

        return total_weight / (float(len(results)) or 1), all(results) if len(results) > 0 else False

    def constraint_result(self, parent_node, fragment):
        ctag = self.kwargs.get('tag')
        if not ctag:
            return 0, False

        ckey = self.kwargs.get('key')

        for tag, keys in parent_node.captured():
            if tag != ctag:
                continue

            if not ckey or ckey in keys:
                return 1.0, True

        return 0.0, False

    def constraint_failure(self, parent_node, fragment, match):
        if not match or not match.success:
            return 1.0, True

        return 0, False

    def constraint_success(self, parent_node, fragment, match):
        #if match and match.success:
        #    return 1.0, True

        return 0, False

    def __repr__(self):
        return "CaptureConstraint(comparisons=%s)" % repr(self.comparisons)
