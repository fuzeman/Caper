from logr import Logr
import math
from caper import CaperFragment
from caper.result import CaperClosureNode, CaperFragmentNode
from caper.step import CaptureStep
from caper.constraint import CaptureConstraint


class CaptureGroup(object):
    def __init__(self, parser, result):
        """Capture group object

        :type parser: caper.parsers.base.Parser
        :type result: caper.result.CaperResult
        """

        self.parser = parser
        self.result = result

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

    def parse_subject(self, parent_node, subject):
        # TODO - if subject is a closure?

        result_nodes = []

        # Check constraints
        for constraint in self.constraints:
            weight, success = constraint.execute(subject)
            if success:
                Logr.debug('capturing broke on "%s" at %s', subject.value, constraint)
                parent_node.finished_groups.append(self)
                result_nodes.append(parent_node)

                if weight == 1.0:
                    return result_nodes
                else:
                    Logr.debug('Branching result')

        # Try match subject against the steps available
        success, weight, match = (None, None, None)
        for step in self.steps:
            success, weight, match = step.execute(subject)
            if success:
                Logr.debug('Found match with weight %s, match: %s' % (weight, match))
                break

        Logr.debug('created fragment node with subject.value: "%s"' % subject.value)
        result_nodes.append(CaperFragmentNode(parent_node.closure, subject, parent_node, weight, match))

        return result_nodes

    def execute(self, once=False):
        heads_finished = None

        while heads_finished is None or not (len(heads_finished) == len(self.result.heads) and all(heads_finished)):
            heads_finished = []

            heads = self.result.heads
            self.result.heads = []

            for head_node in heads:
                Logr.debug("head: %s" % head_node)
                if self in head_node.finished_groups:
                    print "===========head finished for group================"
                    self.result.heads.append(head_node)
                    heads_finished.append(True)
                    continue

                next_subject = head_node.next()

                if next_subject:
                    for node in self.parse_subject(head_node, next_subject):
                        self.result.heads.append(node)

                heads_finished.append(self in head_node.finished_groups or next_subject is None)

            if len(self.result.heads) == 0:
                self.result.heads = heads

            Logr.debug("heads_finished: %s, self.result.heads: %s", heads_finished, self.result.heads)

        Logr.info("=============group finished===================")
