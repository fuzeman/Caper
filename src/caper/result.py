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
from operator import itemgetter


GROUP_MATCHES = ['identifier']


class CaperNode(object):
    def __init__(self, closure, parent=None, tag=None, weight=None, match=None):
        """
        :type parent: CaperNode
        :type weight: float
        """

        #: :type: caper.objects.CaperClosure
        self.closure = closure
        #: :type: CaperNode
        self.parent = parent
        #: :type: str
        self.tag = tag
        #: :type: float
        self.weight = weight
        #: :type: dict
        self.match = match
        #: :type: list of CaptureGroup
        self.finished_groups = []

    def next(self):
        raise NotImplementedError()


class CaperClosureNode(CaperNode):
    def __init__(self, closure, parent=None, tag=None, weight=None, match=None):
        """
        :type closure: caper.objects.CaperClosure or list of caper.objects.CaperClosure
        """
        super(CaperClosureNode, self).__init__(closure, parent, tag, weight, match)

    def next(self):
        if self.closure and len(self.closure.fragments) > 0:
            return self.closure.fragments[0]
        return None


class CaperFragmentNode(CaperNode):
    def __init__(self, closure, fragment, parent=None, tag=None, weight=None, match=None):
        """
        :type fragment: caper.objects.CaperFragment or list of caper.objects.CaperFragment
        """
        super(CaperFragmentNode, self).__init__(closure, parent, tag, weight, match)

        #: :type: caper.objects.CaperFragment or list of caper.objects.CaperFragment
        self.fragment = fragment

    def next(self):
        if self.fragment.right:
            return self.fragment.right

        if self.closure.right:
            return self.closure.right

        return None


class CaperResult(object):
    def __init__(self):
        #: :type: list of CaperNode
        self.heads = []

        self.chains = []

    def build(self):
        for head in self.heads:
            result = self.combine_chain(head)
            result.finish()

            self.chains.append((result.weight, result))

        self.chains.sort(key=itemgetter(0), reverse=True)

    def combine_chain(self, subject, result=None):
        if result is None:
            result = CaperResultChain()

        if not subject.parent:
            return result

        # Skip over closure nodes
        if type(subject) is CaperClosureNode:
            self.combine_chain(subject.parent, result)

        # Parse fragment matches
        if type(subject) is CaperFragmentNode:
            result.update(subject)

            self.combine_chain(subject.parent, result)

        return result


class CaperResultChain(object):
    def __init__(self):
        #: :type: float
        self.weight = None

        self.info = {}

        self._weights = []

    def update(self, subject):
        if not subject.match:
            return

        if subject.tag not in self.info:
            self.info[subject.tag] = []

        self._weights.append(subject.weight)

        self.info[subject.tag].insert(0, subject.match)

    def finish(self):
        self.weight = sum(self._weights) / len(self._weights)
