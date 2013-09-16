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

        return getattr(fragment, name) == expected

    def _compare_re(self, fragment, name, arg):
        if name == 'fragment':
            group, minimum_weight = arg if type(arg) is tuple and len(arg) > 1 else (arg, 0)
            return self.capture_group.parser.matcher.fragment_match(fragment, group) > minimum_weight
        elif type(arg).__name__ == 'SRE_Pattern':
            return arg.match(getattr(fragment, name)) is not None
        elif hasattr(fragment, name):
            match = self.capture_group.parser.matcher.value_match(getattr(fragment, name), arg, single=True)
            return match is not None

        if not hasattr(fragment, name):
            raise ValueError("Unable to find fragment with name '%s'" % name)
        else:
            raise ValueError("Unexpected argument type")

    def execute(self, fragment):
        results = []

        for name, method, argument in self.comparisons:
            results.append(method(fragment, name, argument))

        return all(results) if len(results) > 0 else False

    def __repr__(self):
        return "CaptureConstraint(comparisons=%s)" % repr(self.comparisons)
