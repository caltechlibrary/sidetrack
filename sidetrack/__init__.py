'''
sidetrack -- SImple DEbug TRACing pacKage

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2020-2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

# Package metadata ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#  ╭────────────────────── Notice ── Notice ── Notice ─────────────────────╮
#  |    The following values are automatically updated at every release    |
#  |    by the Makefile. Manual changes to these values will be lost.      |
#  ╰────────────────────── Notice ── Notice ── Notice ─────────────────────╯

__version__     = '2.0.0'
__description__ = 'Simple debug tracing package for Python'
__url__         = 'https://github.com/caltechlibrary/sidetrack'
__author__      = 'Michael Hucka'
__email__       = 'mhucka@caltech.edu'
__license__     = 'BSD 3-clause'

# Main exports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from .debug import *
