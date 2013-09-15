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


class CaperResult(object):
    def __init__(self):
        self._info = {}

    def update(self, match, root=None):
        if root is None:
            root = self._info

        for key in match:
            if type(match[key]) is dict and key not in GROUP_MATCHES:
                if key not in root:
                    root[key] = {}

                self.update(match[key], root[key])
            else:
                if match[key]:
                    if key not in root:
                        root[key] = []

                    root[key].append(match[key])

    def has_any(self, keys, root=None):
        if root is None:
            root = self._info

        if not root:
            return False

        if type(keys) != list:
            keys = [keys]

        for key in keys:
            key = key.split('.')
            head = key[0]

            if head in root:
                # If the key is single length we are finished
                if len(key) == 1:
                    return True

                # Traverse further into the dictionary
                if len(key) > 1:
                    key.pop(0)
                    if self.has_any(key, root[head]):
                        return True

        return False

    def valid(self):
        if 'identifier' in self._info and 'show_name' in self._info:
            return True

        return False
