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


GROUP_MATCHES = ['identifier']


class CaperNode(object):
    def __init__(self, closure, parent=None, weight=None, match=None):
        """
        :type parent: CaperNode
        :type weight: float
        """

        #: :type: caper.objects.CaperClosure
        self.closure = closure
        #: :type: CaperNode
        self.parent = parent
        #: :type: float
        self.weight = weight
        #: :type: dict
        self.match = match
        #: :type: list of CaptureGroup
        self.finished_groups = []

    def next(self):
        raise NotImplementedError()


class CaperClosureNode(CaperNode):
    def __init__(self, closure, parent=None, weight=None, match=None):
        """
        :type closure: caper.objects.CaperClosure or list of caper.objects.CaperClosure
        """
        super(CaperClosureNode, self).__init__(closure, parent, weight, match)

    def next(self):
        if self.closure and len(self.closure.fragments) > 0:
            return self.closure.fragments[0]
        return None


class CaperFragmentNode(CaperNode):
    def __init__(self, closure, fragment, parent=None, weight=None, match=None):
        """
        :type fragment: caper.objects.CaperFragment or list of caper.objects.CaperFragment
        """
        super(CaperFragmentNode, self).__init__(closure, parent, weight, match)

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
        self._info = {}

    def update(self, match, root=None):
        print "update", match

    def has_any(self, keys, root=None):
        print "has_any", keys

    def valid(self):
        print "valid"
        return False
