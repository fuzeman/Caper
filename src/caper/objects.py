class CaperClosure(object):
    def __init__(self, value):
        self.value = value

        self.fragments = None


class CaperFragment(object):
    def __init__(self):
        self.value = ""

        self.left = None
        self.left_sep = None

        self.right = None
        self.right_sep = None

        self.position = None
