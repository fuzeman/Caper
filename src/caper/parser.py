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


class FragmentParser(object):
    parsers = []

    @classmethod
    def register(cls):
        def func_wrapper(func):
            cls.parsers.append(func)
            return func
        return func_wrapper

    def run(self, result, fragment, **kwargs):
        success = False

        for parser in self.parsers:
            if parser(result, fragment, kwargs):
                success = True

        return success


@FragmentParser.register()
def show_name(result, fragment, extra):
    """
    :type result: CaperResult
    :type fragment: str
    """
    if result.has_any(['identifier', 'video']):
        return False

    result.update({'show_name': fragment})
    return True


@FragmentParser.register()
def group_name(result, fragment, extra):
    if 'position' not in extra or 'total' not in extra:
        return False

    if extra['position'] == extra['total']:
        result.update({'group': fragment})
        return True

    return False
