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

    def execute(self, parser):
        if self.is_complete():
            return

        subject = None
        if not self.regex:
            subject = self._get_next_subject(parser)
            if subject is None:
                return

        if self.regex:
            match = self.capture_group.parser.matcher.parser_match(parser, self.regex)
            Logr.debug('(execute) [regex] tag: "%s"', self.tag)
            if match:
                self.match_found(match)
                parser.commit()
                return True
        elif self.func:
            match = self.func(subject)
            Logr.debug('(execute) [func] %s += "%s"', self.tag, match)
            if match:
                self.match_found({self.tag: match})
                parser.commit()
                return True
        else:
            Logr.debug('(execute) [raw] %s += "%s"', self.tag, subject.value)
            self.match_found({self.tag: subject.value})
            parser.commit()
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
