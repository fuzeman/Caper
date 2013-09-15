from logr import Logr
from caper.step import CaptureStep
from caper.constraint import CaptureConstraint


class CaptureGroup(object):
    def __init__(self, parser):
        """Capture group object

        :type parser: caper.parsers.base.Parser
        """

        self.parser = parser

        #: @type: list of CaptureStep
        self.steps = []
        #: @type: list of CaptureConstraint
        self.constraints = []

    def capture_fragment(self, tag, regex=None, func=None, single=True):
        Logr.debug('capture_fragment("%s", "%s", %s, %s)', tag, regex, func, single)

        self.steps.append(CaptureStep(
            self, tag,
            'fragment',
            regex=regex,
            func=func,
            single=single
        ))

        return self

    def capture_closure(self, tag, regex=None, func=None, single=True):
        Logr.debug('capture_closure("%s", "%s", %s, %s)', tag, regex, func, single)

        self.steps.append(CaptureStep(
            self, tag,
            'closure',
            regex=regex,
            func=func,
            single=single
        ))

        return self

    def until(self, **kwargs):
        self.constraints.append(CaptureConstraint(self, **kwargs))

        return self

    def execute(self, once=False):
        while self.parser.closure_available() or self.parser.fragment_available():
            # Try move to next closure if there are no fragments available
            if not self.parser.fragment_available() and self.parser.closure_available():
                self.parser.next_closure()
                self.parser.commit()

            # Stop if there are no fragments
            if not self.parser.fragment_available():
                break

            # Run through the constraints and break on any matches
            for constraint in self.constraints:
                fragment = self.parser.next_fragment()

                if constraint.execute(fragment):
                    Logr.debug('capturing broke on "%s" at %s', fragment.value, constraint)
                    self.parser.rewind()
                    return
                else:
                    self.parser.rewind()

            # Run through the steps
            complete = []
            matched = False
            for step in self.steps:
                if step.execute(self.parser):
                    matched = True
                complete.append(step.is_complete())

            # Skip fragment if every step fails
            if not matched:
                self.parser.next_fragment()
                self.parser.commit()

            # Break if all the steps are complete
            if all(complete):
                Logr.debug('all steps complete, breaking')
                return
            elif once:
                self.parser.rewind()
                return
