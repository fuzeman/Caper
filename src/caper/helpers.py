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


def is_list_type(obj, element_type):
    if not type(obj) is list:
        return False

    if len(obj) < 1:
        raise ValueError("Unable to determine list element type from empty list")

    return type(obj[0]) is element_type


def clean_dict(target, remove=None):
    """Recursively remove items matching a value 'remove' from the dictionary

    :type target: dict
    """
    if type(target) is not dict:
        raise ValueError("Target is required to be a dict")

    for key in target.keys():
        if type(target[key]) is not dict:
            if target[key] == remove:
                target.pop(key)
        else:
            clean_dict(target[key], remove)

    return target
