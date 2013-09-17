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
