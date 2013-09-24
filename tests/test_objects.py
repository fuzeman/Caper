from helpers import create_fragments, get_fragment_values


def test_fragment_take():
    fragments = create_fragments('a.b.c.123')

    assert get_fragment_values(fragments[0].take_right(2)) == ['a', 'b']
    assert get_fragment_values(fragments[0].take_right(6)) == ['a', 'b', 'c', '123', None, None]

    assert get_fragment_values(fragments[3].take_left(2)) == ['123', 'c']
    assert get_fragment_values(fragments[2].take_left(6)) == ['c', 'b', 'a', None, None, None]
