from logr import Logr


class CaptureStep(object):
    REPR_KEYS = ['regex', 'func', 'single']

    def __init__(self, capture_group, tag, source, regex=None, func=None, single=None):
        #: @type: CaptureGroup
        self.capture_group = capture_group

        #: @type: str
        self.tag = tag
        #: @type: str
        self.source = source
        #: @type: str
        self.regex = regex
        #: @type: function
        self.func = func
        #: @type: bool
        self.single = single

    def _get_next_subject(self, parser):
        if self.source == 'fragment':
            if not parser.fragment_available():
                return None
            return parser.next_fragment()
        elif self.source == 'closure':
            if not parser.closure_available():
                return None
            return parser.next_closure()

        raise NotImplementedError()

    def execute(self, fragment):
        if self.regex:
            weight, match = self.capture_group.parser.matcher.fragment_match(fragment, self.regex)
            Logr.debug('(execute) [regex] tag: "%s"', self.tag)
            if match:
                return True, weight, match
        elif self.func:
            match = self.func(fragment)
            Logr.debug('(execute) [func] %s += "%s"', self.tag, match)
            if match:
                return True, 1.0, match
        else:
            Logr.debug('(execute) [raw] %s += "%s"', self.tag, fragment.value)
            return True, 1.0, fragment.value

        return False, 0.0, None

    def __repr__(self):
        attribute_values = [key + '=' + repr(getattr(self, key))
                            for key in self.REPR_KEYS
                            if hasattr(self, key) and getattr(self, key)]

        attribute_string = ', ' + ', '.join(attribute_values) if len(attribute_values) > 0 else ''

        return "CaptureStep('%s'%s)" % (self.tag, attribute_string)
