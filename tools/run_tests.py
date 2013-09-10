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

import logging
import os
from logr import Logr
from caper import Caper


class CaperTests(object):
    def __init__(self):
        self.caper = Caper()

        self.name_col = None
        self.test_names = None

    def _read_header(self, fp):
        header = fp.readline().strip().split(",")

        for i, col in enumerate(header):
            if col == 'name':
                self.name_col = i

        if self.name_col is None:
            raise Exception()

    def load(self, filename, limit=100):
        if not os.path.isfile(filename):
            raise Exception()

        with open(filename) as fp:
            self._read_header(fp)

            self.test_names = []
            for i, line in enumerate(fp):
                row = line.strip().split(',')
                self.test_names.append(row[self.name_col])

                if len(self.test_names) >= limit:
                    break

        print "loaded %s names for testing" % len(self.test_names)

    def run(self):
        max_num_length = len(str(len(self.test_names)))
        row_format = '[%%0%dd] %%s' % max_num_length

        start = raw_input('Start position: ')
        if start.strip() != '':
            start = int(start)
        else:
            start = 0

        for i, name in enumerate(self.test_names):
            if i < start - 1:
                continue

            print row_format % (i + 1, name)

            result = self.caper.parse(name)

            print "Press ENTER to continue testing"
            raw_input()


if __name__ == '__main__':
    Logr.configure(logging.INFO)
    tests = CaperTests()

    test_file = ''
    while test_file == '':
        test_file = raw_input('Test file [scene.csv]: ')

        if test_file == '':
            test_file = 'scene.csv'

        if not os.path.isfile(test_file):
            test_file = ''
            print "ERROR: Test file does not exist"
            print

    tests.load(test_file, 100)

    tests.run()
