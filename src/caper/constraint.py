import re


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

    def _compare_eq(self, fragment, name, expected):
        if not hasattr(fragment, name):
            return None

        return 1.0, getattr(fragment, name) == expected

    def _compare_re(self, fragment, name, arg):
        if name == 'fragment':
            group, minimum_weight = arg if type(arg) is tuple and len(arg) > 1 else (arg, 0)

            weight, match = self.capture_group.parser.matcher.fragment_match(fragment, group)
            return weight, weight > minimum_weight
        elif type(arg).__name__ == 'SRE_Pattern':
            return 1.0, arg.match(getattr(fragment, name)) is not None
        elif hasattr(fragment, name):
            match = self.capture_group.parser.matcher.value_match(getattr(fragment, name), arg, single=True)
            return 1.0, match is not None

        if not hasattr(fragment, name):
            raise ValueError("Unable to find fragment with name '%s'" % name)
        else:
            raise ValueError("Unexpected argument type")

    def execute(self, fragment):
        results = []
        total_weight = 0

        for name, method, argument in self.comparisons:
            weight, success = method(fragment, name, argument)
            total_weight += weight
            results.append(success)

        return total_weight / float(len(results)), all(results) if len(results) > 0 else False

    def __repr__(self):
        return "CaptureConstraint(comparisons=%s)" % repr(self.comparisons)
