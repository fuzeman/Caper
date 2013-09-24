from caper import CaperFragment


def create_fragments(value):
    """Create fragments from a dot ('.') separated string

    :type value: str

    :rtype : list of CaperFragment
    """
    fragment_values = value.split('.')
    fragments = []

    for x in xrange(len(fragment_values)):
        fragment = CaperFragment()
        fragment.value = fragment_values[x]

        if x > 0:
            fragment.left = fragments[x - 1]
            fragments[x - 1].right = fragment

        fragments.append(fragment)

    return fragments


def get_fragment_values(fragments):
    return [(fragment.value if fragment else None) for fragment in fragments]
