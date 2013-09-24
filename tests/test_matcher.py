from caper import FragmentMatcher, CaperFragment
from helpers import create_fragments


def test_fragment_match():
    matcher = FragmentMatcher([
        ('test', [
            (1.0, [
                (r'^abc$', r'^123$'),
            ]),
            (0.8, [
                (r'^abc$', r'^1234$'),
            ])
        ])
    ])

    assert matcher.fragment_match(create_fragments('abc.123')[0], 'test')[0] == 1

    assert matcher.fragment_match(create_fragments('abc.12')[0], 'test')[0] == 0

    assert matcher.fragment_match(create_fragments('abc')[0], 'test')[0] == 0

    assert matcher.fragment_match(create_fragments('abc.1234')[0], 'test')[0] == 0.8

    assert matcher.fragment_match(create_fragments('abc.456')[0], 'test')[0] == 0

    assert matcher.fragment_match(create_fragments('def.123')[0], 'test')[0] == 0