import logging
from logr import Logr
from caper import Caper

Logr.configure(logging.DEBUG)
caper = Caper()


def test_season_S00():
    assert caper.parse('Show.Name.S01.DVDrip.x264')._info == {
        'identifier': {'season': ['01']},
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_S00E00():
    assert caper.parse('Show.Name.S01E05.DVDrip.x264')._info == {
        'identifier': {'season': ['01'], 'episode': ['05']},
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }

def test_episode_00x00():
    assert caper.parse('Show.Name.1x5.DVDrip.x264')._info == {
        'identifier': {'season': ['1'], 'episode': ['5']},
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }

    assert caper.parse('Show.Name.13x23.DVDrip.x264')._info == {
        'identifier': {'season': ['13'], 'episode': ['23']},
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }
