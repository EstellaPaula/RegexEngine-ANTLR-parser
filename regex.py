import string


CHARSET = string.digits + string.ascii_letters

EMPTY_STRING = 0
SYMBOL_SIMPLE = 1
SYMBOL_ANY = 2
SYMBOL_SET = 3
MAYBE = 4
STAR = 5
PLUS = 6
RANGE = 7
CONCATENATION = 8
ALTERNATION = 9

_SIMPLE_TYPES = {EMPTY_STRING, SYMBOL_SIMPLE, SYMBOL_ANY, SYMBOL_SET}
_BINARY_TYPES = {CONCATENATION, ALTERNATION}


def str_paranthesize(parent_type, re):
    if parent_type > re.type or parent_type == re.type and parent_type != STAR:
        return str(re)
    else:
        return "({!s})".format(str(re))


class RegEx(object):
    """Model a RegEx TDA

    The member "type" is always available, indicating the type of the
    RegularExpression. Its value dictates which other members (if any) are
    defined:

        - EMPTY_STRING:
        - SYMBOL_SIMPLE: "symbol" is the symbol
        - SYMBOL_ANY:
        - SYMBOL_SET: "symbol_set" is a set of elements which are either
            regular symbols or tuples of symbols representing a symbol range
        - MAYBE: "lhs" is the RegEx
        - STAR: "lhs" is the RegEx
        - PLUS: "lhs" is the RegEx
        - RANGE: "lhs" is the RegEx and "range" is a tuple representing the
            range; an unspecified extremity is denoted with a value of -1
        - CONCATENATION: "lhs" and "rhs" are the RegExes
        - ALTERNATION: "lhs" and "rhs" are the RegExes

    """
    def __init__(self, type, obj1=None, obj2=None):
        """Create a RegEx

        The value of the "type" parameter influences the interpretation of the
        other two paramters:

            - EMPTY_STRING: obj1 and obj2 are unused
            - SYMBOL_SIMPLE: obj1 should be a symbol; obj2 is unused
            - SYMBOL_ANY: obj1 and obj2 are unused
            - SYMBOL_SET: obj1 is a set of either symbols or tuples signifying
                a symbol range; obj2 is unused
            - MAYBE: obj1 should be a RegEx; obj2 is unused
            - STAR: obj1 should be a RegEx; obj2 is unused
            - PLUS: obj1 should be a RegEx; obj2 is unused
            - RANGE: obj1 should be a RegEx; obj2 should be a tuple
                representing the range (an unspecified extremity is represented
                with a value of -1)
            - CONCATENATION: obj1 and obj2 should be RegEx
            - ALTERNATION: obj1 and obj2 should be RegEx

        """
        self.type = type
        if type in _SIMPLE_TYPES:
            if type == SYMBOL_SIMPLE:
                assert obj1 in CHARSET
                self.symbol = obj1
            elif type == SYMBOL_SET:
                assert obj1 is not None
                self.symbol_set = obj1
        else:
            assert isinstance(obj1, RegEx)
            self.lhs = obj1

            if type == RANGE:
                assert obj2 is not None
                x, y = obj2
                assert (y > 0 and x <= y) or (x >= 0)
                self.range = obj2
            if type in _BINARY_TYPES:
                assert obj2 is not None
                assert isinstance(obj2, RegEx)
                self.rhs = obj2

    def __str__(self):
        def normalize_to_tuple(e):
            """Allows us to sort sets containing both symbols and ranges

            This is needed in order to deterministically represent a symbol set
            as a string; namely all single characters first (in alphabetical
            order), followed by all ranges.

            """
            if isinstance(e, str):
                return (e, "")

            return e

        if self.type == EMPTY_STRING:
            return ""
        if self.type == SYMBOL_SIMPLE:
            return str(self.symbol)
        if self.type == SYMBOL_ANY:
            return "."
        if self.type == SYMBOL_SET:
            result = "["
            for range in sorted(self.symbol_set, key=normalize_to_tuple):
                result += "-".join(range)

            return result + "]"
        if self.type == MAYBE:
            slhs = str_paranthesize(self.type, self.lhs)
            return slhs + "?"
        if self.type == STAR:
            slhs = str_paranthesize(self.type, self.lhs)
            return slhs + "*"
        if self.type == PLUS:
            slhs = str_paranthesize(self.type, self.lhs)
            return slhs + "+"
        if self.type == RANGE:
            slhs = str_paranthesize(self.type, self.lhs)
            x, y = self.range
            if x == -1:
                aux = "{{,{}}}".format(y)
            elif y == -1:
                aux = "{{{},}}".format(x)
            elif x == y:
                aux = "{{{}}}".format(x)
            else:
                aux = "{{{},{}}}".format(x, y)
            return slhs + aux
        if self.type == CONCATENATION:
            slhs = str_paranthesize(self.type, self.lhs)
            srhs = str_paranthesize(self.type, self.rhs)
            return slhs + srhs
        if self.type == ALTERNATION:
            slhs = str_paranthesize(self.type, self.lhs)
            srhs = str_paranthesize(self.type, self.rhs)
            return slhs + "|" + srhs

        raise Exception("Unknown type!")
