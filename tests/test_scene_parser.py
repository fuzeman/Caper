import logging
from logr import Logr
from caper import Caper
from caper.result import CaperResult

Logr.configure(logging.DEBUG)
caper = Caper()


def assert_result(result, *chains):
    """Check if the result matches the expected chains

    :type result: CaperResult
    """
    assert len(result.chains) == len(chains)

    for x, (weight, info) in enumerate(chains):
        assert result.chains[x][1].weight == weight
        assert result.chains[x][1].info == info


def test_season_S00():
    assert_result(caper.parse('Show.Name.S01.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '01'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_season_verbose():
    assert_result(caper.parse('Show.Name.Season.1.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '1'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_S00E00():
    assert_result(caper.parse('Show.Name.S01E05.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '01', 'episode': '05'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_00x00():
    assert_result(caper.parse('Show.Name.1x5.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '1', 'episode': '5'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))

    assert_result(caper.parse('Show.Name.13x23.DVDrip.x264'), (1.0, {
        'identifier': [{'season': '13', 'episode': '23'}],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_repeat():
    assert_result(caper.parse('Show.Name.S01E01.S01E02.DVDrip.x264'), (1.0, {
        'identifier': [
            {'season': '01', 'episode': '01'},
            {'season': '01', 'episode': '02'}
        ],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_extend():
    assert_result(caper.parse('Show.Name.S01E01-E02.DVDrip.x264'), (1.0, {
        'identifier': [
            {'season': '01', 'episode_from': '01', 'episode_to': '02'},
        ],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_date():
    assert_result(caper.parse('Show.Name.2010.11.23.DVDrip.x264'), (1.0, {
        'identifier': [
            {'year': '2010', 'month': '11', 'day': '23'}
        ],
        'show_name': ['Show', 'Name'],
        'video': [
            {'source': 'DVDrip'},
            {'codec': 'x264'}
        ]
    }))


def test_episode_verbose():
    assert_result(caper.parse('Show Name Season 3 Episode 14'), (1.0, {
        'identifier': [
            {'season': '3', 'episode': '14'}
        ],
        'show_name': ['Show', 'Name']
    }))

    assert_result(caper.parse('Show Name Se 3 Ep 14'), (1.0, {
        'identifier': [
            {'season': '3', 'episode': '14'}
        ],
        'show_name': ['Show', 'Name']
    }))


def test_episode_part():
    assert_result(caper.parse('Show Name.Part.3'), (1.0, {
        'identifier': [
            {'part': '3'}
        ],
        'show_name': ['Show', 'Name']
    }))

    assert_result(caper.parse('Show Name.Part.1.and.Part.2'), (1.0, {
        'identifier': [
            {'part': '1'},
            {'part': '2'}
        ],
        'show_name': ['Show', 'Name']
    }))


def test_episode_bare():
    assert_result(caper.parse('Show Name.102.x264'), (0.95, {
        'identifier': [
            {'episode': '02', 'season': '1'}
        ],
        'show_name': ['Show', 'Name'],
        'video': [{'codec': 'x264'}]
    }), (0.75, {
        'show_name': ['Show', 'Name'],
        'video': [{'codec': 'x264'}]
    }))
