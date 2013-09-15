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

from caper import Caper


caper = Caper()


def test_closure_generation():
    caper._closure_split('[Group]_Show_Name_7.2_An_Episode_Title_(Blu-Ray_1280x720_FLAC)_[645G7V54].mkv') == [
        '[Group]',
        'Show_Name_7.2_An_Episode_Title',
        '(Blu-Ray_1280x720_FLAC)',
        '[645G7V54]',
        'mkv'
    ]

    caper._closure_split('Show.Name.S01.DVDrip.x264') == [
        'Show.Name.S01.DVDrip.x264'
    ]

    caper._closure_split('[Group]_Show_Name_[video_ver.]_[720p]_[645G7V54].mkv') == [
        '[Group]',
        'Show_Name',
        '[video_ver.]',
        '[720p]',
        '[645G7V54]',
        'mkv'
    ]

    caper._closure_split('[GROUP] Show Name') == [
        '[GROUP]',
        'Show Name'
    ]

    caper._closure_split('Show Name [GROUP-NAME]') == [
        'Show Name',
        '[GROUP-NAME]'
    ]


def test_fragment_generation():
    def testable_closures(closures):
        result = []
        for closure in closures:
            if closure.fragments and len(closure.fragments) > 0:
                result.append((closure.value, [fragment.value for fragment in closure.fragments]))
            else:
                result.append(closure.value)

        return result

    #
    # [Another Group] Some Show Name [720p DVD]_[G84VA2BX]
    #

    closures = caper._closure_split('[Another Group] Some Show Name [720p DVD]_[G84VA2BX]')

    assert testable_closures(closures) == [
        '[Another Group]',
        'Some Show Name',
        '[720p DVD]',
        '[G84VA2BX]'
    ]

    assert testable_closures(caper._fragment_split(closures)) == [
        ('[Another Group]', [
            'Another',
            'Group'
        ]),
        ('Some Show Name', [
            'Some',
            'Show',
            'Name'
        ]),
        ('[720p DVD]', [
            '720p',
            'DVD'
        ]),
        ('[G84VA2BX]', [
            'G84VA2BX'
        ])
    ]

    #
    # Show.Name.2010.S01.REPACK.1080p.BluRay.x264-GROUP
    #

    closures = caper._closure_split('Show.Name.2010.S01.REPACK.1080p.BluRay.x264-GROUP')

    assert testable_closures(closures) == [
        'Show.Name.2010.S01.REPACK.1080p.BluRay.x264-GROUP'
    ]

    assert testable_closures(caper._fragment_split(closures)) == [
        ('Show.Name.2010.S01.REPACK.1080p.BluRay.x264-GROUP', [
            'Show',
            'Name',
            '2010',
            'S01',
            'REPACK',
            '1080p',
            'BluRay',
            'x264',
            'GROUP'
        ])
    ]
