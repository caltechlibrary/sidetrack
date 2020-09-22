#!/usr/bin/env python3
# =============================================================================
# @file    demo_debug.py
# @brief   Simple demo for Sidetrack
# @author  Michael Hucka <mhucka@caltech.edu>
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/sidetrack
# =============================================================================

# The following imports are just for this demo program.
import os
import plac
import sys

# This is to allow running the demo from the tests dir w/o installing sidetrack.
try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

# This next line demonstrates how you would import Sidetrack normally.
# Conditioning on __debug__ means the import won't be done if running Python -O.
if __debug__:
    from sidetrack import set_debug, log

# The following defines the command-line arguments accepted by this demo program.
@plac.annotations(
    debug       = ('write detailed trace to "OUT" ("-" means console)',  'option', 'd'),
    show_thread = ('print thread name in -d output (default: False)',    'flag', 't'),
    show_pid    = ('print the process id in -d output (default: False)', 'flag', 'p'),
)

def main(debug = 'OUT', show_thread = False, show_pid = False):
    '''Demonstrate the use of Sidetrack. Use -h for help.'''

    # "OUT" is just a placeholder. If the user supplies argument -d with a
    # value, then we take that as an indication to turn on debugging and send
    # output to the given destination. The value can be '-' for stdout.
    if debug != 'OUT':
        print('Debug argument -d given.')
        if __debug__:
            extra = ''
            if show_pid:
                print('Show_pid argument -p given.')
                extra += '(pid %(process)d)'
            if show_thread:
                print('Show_thread argument -t given.')
                extra += ' ' if show_pid else ''
                extra += '%(threadName)s'
            set_debug(True, debug, extra = extra)
        else:
            print('Python -O is in effect, so debug logging is not available.')

    if __debug__: log('=== demo program starting ===')

    print('Looping my loopy loop:')
    for i in range(0, 3):
        if __debug__: log(f'loop value {i}')
        print('Another go-around the loop')
    print('Done looping.')

    if __debug__: log('=== demo program stopping ===')

# Invoke the main routine.
if __name__ == '__main__':
    plac.call(main)
