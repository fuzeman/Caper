import logging
from logr import Logr
from caper import Caper

Logr.configure(logging.DEBUG)
caper = Caper()


def test_season_S00():
    assert caper.parse('Show.Name.S01.DVDrip.x264')._info == {
        'identifier': [{'season': '01'}],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_season_verbose():
    assert caper.parse('Show.Name.Season.1.DVDrip.x264')._info == {
        'identifier': [{'season': '1'}],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_S00E00():
    assert caper.parse('Show.Name.S01E05.DVDrip.x264')._info == {
        'identifier': [{'season': '01', 'episode': '05'}],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_00x00():
    assert caper.parse('Show.Name.1x5.DVDrip.x264')._info == {
        'identifier': [{'season': '1', 'episode': '5'}],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }

    assert caper.parse('Show.Name.13x23.DVDrip.x264')._info == {
        'identifier': [{'season': '13', 'episode': '23'}],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_repeat():
    assert caper.parse('Show.Name.S01E01.S01E02.DVDrip.x264')._info == {
        'identifier': [
            {'season': '01', 'episode': '01'},
            {'season': '01', 'episode': '02'}
        ],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_extend():
    assert caper.parse('Show.Name.S01E01-E02.DVDrip.x264')._info == {
        'identifier': [
            {'season': '01', 'episode_from': '01', 'episode_to': '02'},
        ],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_date():
    assert caper.parse('Show.Name.2010.11.23.DVDrip.x264')._info == {
        'identifier': [
            {'year': '2010', 'month': '11', 'day': '23'}
        ],
        'show_name': ['Show', 'Name'],
        'video': {
            'codec': ['x264'],
            'source': ['DVDrip']
        }
    }


def test_episode_verbose():
    assert caper.parse('Show Name Season 3 Episode 14')._info == {
        'identifier': [
            {'season': '3', 'episode': '14'}
        ],
        'show_name': ['Show', 'Name']
    }

    assert caper.parse('Show Name Se 3 Ep 14')._info == {
        'identifier': [
            {'season': '3', 'episode': '14'}
        ],
        'show_name': ['Show', 'Name']
    }


def test_episode_part():
    assert caper.parse('Show Name.Part.3')._info == {
        'identifier': [
            {'part': '3'}
        ],
        'show_name': ['Show', 'Name']
    }

    assert caper.parse('Show Name.Part.1.and.Part.2')._info == {
        'identifier': [
            {'part': '1'},
            {'part': '2'}
        ],
        'show_name': ['Show', 'Name']
    }


def test_episode_bare():
    assert caper.parse('Show Name.102.x264')._info == {
        'identifier': [
            {'season': '1', 'episode': '02'}
        ],
        'show_name': ['Show', 'Name'],
        'video': {'codec': ['x264']}
    }
