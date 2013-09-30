from hamcrest.core.base_matcher import BaseMatcher


class HasInfo(BaseMatcher):
    def __init__(self, group, match):
        self.group = group
        self.match = match

    def matches(self, item, mismatch_description=None):
        if not hasattr(item, 'chains') or len(item.chains) < 1:
            return False

        if self.group not in item.chains[0].info:
            return False

        return self.match in item.chains[0].info[self.group]

    def describe_to(self, description):
        description.append_text('result with the group ')\
                   .append_text(self.group)\
                   .append_text(', containing the match ')\
                   .append_text(str(self.match))


def has_info(group, match):
    return HasInfo(group, match)
