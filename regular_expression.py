EMPTY_SET = 0
EMPTY_STRING = 1
SYMBOL = 2
STAR = 3
CONCATENATION = 4
ALTERNATION = 5

_SIMPLE_TYPES = {EMPTY_SET, EMPTY_STRING, SYMBOL}


def str_paranthesize(parent_type, re):
    if parent_type > re.type or parent_type == re.type and parent_type != STAR:
        return str(re)
    else:
        return "({!s})".format(str(re))


class RegularExpression(object):
    """Model a Regular Expression TDA

    The member "type" is always available, indicating the type of the
    RegularExpression. Its value dictates which other members (if any) are
    defined:

        - EMPTY_SET:
        - EMPTY_STRING:
        - SYMBOL: "symbol" is the symbol
        - STAR: "lhs" is the RegularExpression
        - CONCATENATION: "lhs" and "rhs" are the RegularExpressions
        - ALTERNATION: "lhs" and "rhs" are the RegularExpressions

    """
    def __init__(self, type, obj1=None, obj2=None):
        """Create a Regular Expression

        The value of the "type" parameter influences the interpretation of the
        other two paramters:

            - EMPTY_SET: obj1 and obj2 are unused
            - EMPTY_STRING: obj1 and obj2 are unused
            - SYMBOL: obj1 should be a symbol; obj2 is unused
            - STAR: obj1 should be a RegularExpression; obj2 is unused
            - CONCATENATION: obj1 and obj2 should be RegularExpressions
            - ALTERNATION: obj1 and obj2 should be RegularExpressions

        """
        self.type = type
        if type in _SIMPLE_TYPES:
            if type == SYMBOL:
                assert obj1 is not None
                self.symbol = obj1
        else:
            assert isinstance(obj1, RegularExpression)
            self.lhs = obj1
            if type == CONCATENATION or type == ALTERNATION:
                assert isinstance(obj2, RegularExpression)
                self.rhs = obj2

    def __str__(self):
        if self.type == EMPTY_SET:
            return "∅"
        elif self.type == EMPTY_STRING:
            return "ε"
        elif self.type == SYMBOL:
            return str(self.symbol)
        elif self.type == CONCATENATION:
            slhs = str_paranthesize(self.type, self.lhs)
            srhs = str_paranthesize(self.type, self.rhs)
            return slhs + srhs
        elif self.type == ALTERNATION:
            slhs = str_paranthesize(self.type, self.lhs)
            srhs = str_paranthesize(self.type, self.rhs)
            return slhs + "|" + srhs
        elif self.type == STAR:
            slhs = str_paranthesize(self.type, self.lhs)
            return slhs + "*"
        else:
            return ""

    def __mul__(self, rhs):
        """Concatenation"""
        if isinstance(rhs, str) and len(rhs) == 1:
            rhs = RegularExpression(SYMBOL, rhs)

        assert isinstance(rhs, RegularExpression)
        return RegularExpression(CONCATENATION, self, rhs)

    __rmul__ = __mul__

    def __or__(self, rhs):
        """Alteration"""
        if isinstance(rhs, str) and len(rhs) == 1:
            rhs = RegularExpression(SYMBOL, rhs)

        assert isinstance(rhs, RegularExpression)
        return RegularExpression(ALTERNATION, self, rhs)

    __ror__ = __or__

    def star(self):
        return RegularExpression(STAR, self)
