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

    def _compare_eq(self, value, expected):
        return value == expected

    def _compare_re(self, value, arg):
        if type(arg) is str:
            match = self.capture_group.parser.matcher.value_match(value, arg, single=True)
            return match is not None
        elif type(re.compile('.')).__name__ == 'SRE_Pattern':
            return arg.match(value) is not None

        raise ValueError("Unexpected argument type")

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
