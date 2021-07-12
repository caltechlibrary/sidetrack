'''
debug.py: lightweight debug logging facility

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019-2021 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

# Everything is carefully conditionalized on __debug__.  This is meant to
# minimize the performance impact of this module by eliding everything when
# Python is running with the optimization flag -O.


# Logger configuration.
# .............................................................................

if __debug__:
    from   inspect import currentframe
    import logging
    from   os import path
    import sys

    # This next global variable makes a huge speed difference. It lets us avoid
    # calling logging.getLogger('packagename').isEnabledFor(logging.DEBUG)
    # at runtime in log() to test whether debugging is turned on.
    setattr(sys.modules[__package__], '_debugging', False)


# Constants.
# .............................................................................

# A custom level is used so that packages that turn off logging.DEBUG globally
# don't end up disabling Sidetrack too.

if __debug__:
    from logging import DEBUG
    SIDETRACK_DEBUG = logging.DEBUG + 1


# Exported functions.
# .............................................................................

def set_debug(enabled, dest = '-', show_package = False, extra = ''):
    '''Turns on debug logging if 'enabled' is True; turns it off otherwise.

    Optional argument 'dest' directs the output to the given destination.
    The value can be a file path, or a single dash ('-') to indicate the
    standard error stream (i.e., sys.stderr).  The default destination is the
    standard error stream.  For simplicity, only one destination is allowed at
    given a time; calling this function multiple times with different
    destinations simply switches the destination to the latest one.

    Optional argument 'show_package' prepends the name of the package calling
    the Sidetrack log functions to the log message.  This is False by default
    because it it is only really useful if you use Sidetrack in multiple
    packages, or import packages that also use Sidetrack.

    Optional argument 'extra' is additional text inserted before the logged
    message.  The 'extra' text string can contain % formatting strings defined
    by the Python logging package.  For example, the current thread name can be
    inserted by setting extra = '%(threadName)s'.  For information about the
    available formatting directives, please consult the Python logging docs at
    https://docs.python.org/library/logging.html#logrecord-attributes

    This uses the Python logging framework to print messages.  The messages
    are printed with level sidetrack.SIDETRACK_DEBUG.
    '''
    if __debug__:
        from logging import WARNING, FileHandler, StreamHandler
        setattr(sys.modules[__package__], '_debugging', enabled)
        setattr(sys.modules[__package__], '_show_package', show_package)

        # Set the appropriate output destination if we haven't already.
        if enabled:
            logger = logging.getLogger(__package__)
            front_part = (str(extra) + ' ') if extra else ''
            formatter = logging.Formatter(front_part + '%(message)s')
            # We only allow one active destination.
            for h in logger.handlers:
                logger.removeHandler(h)
            # We treat empty dest values as meaning "the default output".
            if dest in ['-', '', None]:
                handler = StreamHandler()
            elif type(dest) == type(sys.stderr):
                handler = StreamHandler(dest)
            else:
                handler = FileHandler(dest)
            handler.setFormatter(formatter)
            handler.setLevel(SIDETRACK_DEBUG)
            logger.addHandler(handler)
            logger.setLevel(SIDETRACK_DEBUG)
            setattr(sys.modules[__package__], '_logger', logger)
        elif getattr(sys.modules[__package__], '_logger', None):
            logger = logging.getLogger(__package__)
            logger.setLevel(WARNING)


# You might think that the way to get the current caller info when the log
# function is called would be to use logger.findCaller(). I tried that, and it
# produced very different information, even when using various values of
# stacklevel as the argument. The code below instead uses the Python inspect
# module to get the correct stack frame at run time.

def log(msg):
    '''Logs a debug message in raw form, without further interpretation.

    The text string 'msg' is taken as-is; unlike the function logf(...), this
    function does not apply str.format to the string.
    '''
    if __debug__:
        # This test for the level may seem redundant, but it's not: it prevents
        # the string format from always being performed if logging is not
        # turned on and the user isn't running Python with -O.
        if getattr(sys.modules[__package__], '_debugging', False):
            __write_log(msg, currentframe().f_back)


def logf(msg, *other_args):
    '''Logs a debug message, optionally with arguments passed to format.

    The "msg" can contain string format directives.  The "other_args" are
    arguments that are merged into "msg" using str.format.
    '''
    if __debug__:
        # This test for the level may seem redundant, but it's not: it prevents
        # the string format from always being performed if logging is not
        # turned on and the user isn't running Python with -O.
        if getattr(sys.modules[__package__], '_debugging', False):
            __write_log(msg.format(*other_args), currentframe().f_back)


def loglist(msg_list):
    '''Logs a list of strings as individual debug message.

    The text strings in the list are taken as-is.  This is a shorthand for
    doing roughly the following:

        for msg in msg_list:
            log(msg)
    '''
    if __debug__:
        # This test for the level may seem redundant, but it's not: it prevents
        # the string format from always being performed if logging is not
        # turned on and the user isn't running Python with -O.
        if getattr(sys.modules[__package__], '_debugging', False):
            for msg in msg_list:
                __write_log(msg, currentframe().f_back)


# Internal helper functions.
# .............................................................................

def __write_log(msg, frame):
    func   = frame.f_code.co_name
    lineno = frame.f_lineno
    if getattr(sys.modules[__package__], '_show_package', False):
        package = frame.f_globals['__package__']
        pkg = f'<{package}> ' if package else ''
    else:
        pkg = ''
    file   = path.basename(frame.f_code.co_filename)
    logger = logging.getLogger(__package__)
    logger.log(SIDETRACK_DEBUG, f'{pkg}{file}:{lineno} {func}() -- ' + msg)
