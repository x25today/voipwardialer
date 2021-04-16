# Range library.
#
# Range definitions:
# 1670000AAAA produce from 1670000000 to 16700009999
# Options:
# A: ALL
# E: EVEN
# O: ODD
# 3-3, example:
#
# 1670000[0,3~6][4,8,0,9]OE is a valid syntax.
#

from ast import literal_eval
from typing import List


class Range:
    def __init__(self, range_string: str):
        self._range_string: str = range_string

    @property
    def numbers(self):
        return self._parse_string(self._range_string)

    @staticmethod
    def _get_numbers_in_microrange(microrange: str) -> iter:
        try:
            return list(literal_eval(microrange))
        except Exception as e:
            raise ValueError("Wrong syntax in range, check: %s" %
                             microrange) from e

    def _parse_string(self, rangestr=None, groups=-1) -> List:
        numbers = []
        skip_next = 0
        _rstring = rangestr and rangestr or self._range_string
        _string = ""
        append = True
        for i, p in enumerate(_rstring):
            if skip_next:
                print("skipping %s" % p)
                skip_next -= 1
            elif p.isdigit():
                _string += p
            elif p == "[":
                append = False
                end = _rstring.find("]", i)
                skip_next = end - i
                for x in self._get_numbers_in_microrange(_rstring[i:end + 1]):
                    _r = "{}{}{}".format(_string, x, _rstring[end + 1:])
                    numbers.extend(
                        self._parse_string(rangestr=_r, groups=groups))
            elif p in "AEO":
                append = False
                for x in {"A": range(0, 10), "E": "13579", "O": "2468"}[p]:
                    _r = "{}{}{}".format(_string, x, _rstring[i + 1:])
                    numbers.extend(
                        self._parse_string(rangestr=_r, groups=groups))
            else:
                raise ValueError("Wrong syntax in range: %s" % rangestr)
        append and numbers.append(_string)
        if append:
            print("appending %s, source: %s" % (_string, _rstring))
        return numbers


if __name__ == "__main__":
    r = Range("80010[1,2,3]AAAA")
    for x in r.numbers:
        pass
