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

from logr import Logr
import logging
import csv
import sys
import os

src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(src_path))

from caper import Caper


class CaperTests(object):
    def __init__(self, debug):
        self.caper = Caper(debug=debug)

        self.name_col = None
        self.test_names = None

    def _read_header(self, reader):
        header = next(reader)

        for i, col in enumerate(header):
            if col == 'name':
                self.name_col = i

        if self.name_col is None:
            raise Exception()

    def load(self, filename, limit = 100):
        if not os.path.isfile(filename):
            raise Exception()

        with open(filename) as fp:
            reader = csv.reader(fp, escapechar='|')

            self._read_header(reader)

            self.test_names = []
            for i, row in enumerate(reader):
                if not len(row) or row[0].startswith('#'):
                    continue

                self.test_names.append(row[self.name_col])

                if len(self.test_names) >= limit:
                    break

        print "loaded %s names for testing" % len(self.test_names)

    def run(self, parser_type, arguments):
        max_num_length = len(str(len(self.test_names)))
        row_format = '[%%0%dd] %%s' % max_num_length

        start = arguments['start'] or raw_input('Start position: ')
        if start.strip() != '':
            start = int(start)
        else:
            start = 0

        for i, name in enumerate(self.test_names):
            if i < start - 1:
                continue

            print row_format % (i + 1, name)

            result = self.caper.parse(name, parser_type)

            if arguments['print'] and result and result.chains:
                print "------------------------------------------------------------------------"

                for chain in result.chains:
                    print "Chain [%s]: %s" % (chain.weight, chain.info)

                print "------------------------------------------------------------------------"

            if arguments['pause']:
                print "Press ENTER to continue testing"
                try:
                    raw_input()
                except EOFError:
                    return


def raw_input_default(message, default=None):
    value = raw_input(message)
    if value == '':
        value = default

    return value


def get_argument(n, value_type=str, default=None):
    value = sys.argv[n] if len(sys.argv) > n else None

    if value is None:
        return default

    if value_type is str:
        return value

    if value_type is bool:
        return value.lower() == 'true'

    raise ValueError('Unknown value_type "%s"' % value_type)


def parse_arguments():
    return {
        'parser_type': get_argument(1),
        'test_file': get_argument(2),
        'logging_mode': get_argument(3),
        'start': get_argument(4),
        'pause': get_argument(5, bool, True),
        'print': get_argument(6, bool, True)
    }


if __name__ == '__main__':
    arguments = parse_arguments()

    tests = CaperTests(debug=arguments['logging_mode'] == 'debug')

    parser_type = arguments['parser_type'] or \
        raw_input_default('Parser type (scene, anime) [scene]: ', 'scene')

    test_file = ''
    test_file_default = 'scene.csv'
    if os.path.isfile(parser_type + '.csv'):
        test_file_default = parser_type + '.csv'

    while test_file == '':
        test_file = arguments['test_file'] or \
            raw_input_default('Test file [%s]: ' % test_file_default, test_file_default)

        if not os.path.isfile(test_file):
            test_file = ''
            print "ERROR: Test file does not exist"
            print

    logging_mode = arguments['logging_mode'] or \
        raw_input_default('Logging mode (debug, info) [info]: ', 'info')

    if logging_mode == 'debug':
        Logr.configure(logging.DEBUG, trace_origin=True)
    else:
        Logr.configure(logging.INFO)

    tests.load(test_file, 100)

    tests.run(parser_type, arguments)
