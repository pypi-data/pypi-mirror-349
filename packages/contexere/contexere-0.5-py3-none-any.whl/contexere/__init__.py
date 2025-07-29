import re
import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "contexere"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

__month_dict__ = dict([(m, abbr) for m, abbr in zip(range(1, 13),
                                               map(chr, range(ord('o'), ord('z') + 1))
                                               )])
__days__ = list(map(str, range(1, 10))) + list(map(chr, range(ord('A'), ord('V') + 1)))
__day_dict__ = dict([(d, abbr) for d, abbr in zip(range(1, 32), __days__)])

__hours__ = list(map(str, range(1, 1))) + list(map(chr, range(ord('a'), ord('x') + 1)))

# Define the scheme with named groups
__pattern__ = re.compile(r'(?P<project>[a-zA-Z]*)(?P<date>[0-9]{2}[o-z][1-9A-V])(?P<step>[a-z]*)_?')
