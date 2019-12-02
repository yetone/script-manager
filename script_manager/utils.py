import re
from collections import OrderedDict


PATTERN_PARAM = re.compile(r'^:param\s+(?P<name>[A-Za-z0-9_]+):\s*(?P<description>.*)')
PATTERN_RETURN = re.compile(r'^:returns:\s*(?P<description>.*)')
PATTERN_RAISE = re.compile(r'^:raises\s+(?P<name>[A-Za-z0-9_]+):\s*(?P<description>.*)')


class DocParam(object):
    def __init__(self, name, type=None, default=None, description=None):
        self.name = name
        self.type = type
        self.default = default
        self.description = description


class DocString(object):
    def __init__(self, description, params):
        self.description = description
        self.params = OrderedDict((p.name, p) for p in params)


def parse_docstring(txt):
    if not txt:
        return
    txt = txt.strip()
    lines = txt.split('\n')
    descriptions = []
    params = []
    returns = []
    raises = []
    for line in lines:
        line = line.strip()
        param_match = PATTERN_PARAM.search(line)
        return_match = PATTERN_RETURN.search(line)
        raise_match = PATTERN_RAISE.search(line)
        if param_match:
            params.append(
                DocParam(
                    param_match.group('name'),
                    description=param_match.group('description')
                )
            )
        elif return_match:
            returns.append(line)
        elif raise_match:
            raises.append(line)
        else:
            if params:
                params[-1].description += '\n' + line
            else:
                descriptions.append(line)
    return DocString('\n'.join(descriptions), params)
