VERSION = (0, 8, 2, 'beta', 0)

__title__ = 'python-bol-api'
__version_info__ = VERSION
__version__ = '.'.join(map(str, VERSION[:3])) + ('-{}{}'.format(
    VERSION[3], VERSION[4] or '') if VERSION[3] != 'final' else '')
__author__ = 'Raymond Penners'
__license__ = 'LGPL 3.0'
__copyright__ = 'Copyright 2017 Raymond Penners and contributors'
