__author__ = 'yetone'

import sys

PY2 = sys.version_info[0] == 2


if not PY2:
    text_type = str
    izip = zip
else:
    text_type = unicode
    from itertools import izip
