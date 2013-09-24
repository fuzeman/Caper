class CaperClosure(object):
    def __init__(self, value):
        #: :type: str
        self.value = value

        #: :type: CaperClosure
        self.left = None
        #: :type: CaperClosure
        self.right = None

        #: :type: list of CaperFragment
        self.fragments = []


class CaperFragment(object):
    def __init__(self):
        #: :type: str
        self.value = ""

        #: :type: CaperFragment
        self.left = None
        #: :type: str
        self.left_sep = None

        #: :type: CaperFragment
        self.right = None
        #: :type: str
        self.right_sep = None

        #: :type: int
        self.position = None

    def take(self, direction, count, include_self=True):
        if direction not in ['left', 'right']:
            raise ValueError('Un-Expected value for "direction", expected "left" or "right".')

        result = []

        if include_self:
            result.append(self)
            count -= 1

        cur = self
        for x in xrange(count):
            if cur and getattr(cur, direction):
                cur = getattr(cur, direction)
                result.append(cur)
            else:
                result.append(None)
                cur = None

        return result

    def take_left(self, count, include_self=True):
        return self.take('left', count, include_self)

    def take_right(self, count, include_self=True):
        return self.take('right', count, include_self)
