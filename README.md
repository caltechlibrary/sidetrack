Sidetrack<img width="11%" align="right" src="https://github.com/caltechlibrary/sidetrack/raw/main/.graphics/sidetrack-logo.png">
===========================================================================

_Sidetrack_ provides a simple interface for writing log messages in Python programs.  Calls to the log functions can be left in your code to let users produce debug logs in the field; if performance matters, using certain coding idioms and turning on Python optimization will cause log statements to be compiled out.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/sidetrack.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/sidetrack/releases)
[![DOI](http://img.shields.io/badge/DOI-10.22002/D1.1629-blue.svg?style=flat-square)](https://data.caltech.edu/records/1629)
[![PyPI](https://img.shields.io/pypi/v/sidetrack.svg?style=flat-square&color=red)](https://pypi.org/project/sidetrack/)


Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

IDEs are great for debugging and tracing execution of your code, but they can't be used in all situations.  For example, if your code is executing on multiple remote computers, or you have released a program to general users and you would like them to send you a debug log/trace of execution, using an IDE at runtime may be impractical or impossible.  Logging packages such as [`logging`](https://docs.python.org/3/library/logging.html) are made for these situations; you can insert logging statements in your code and use the output to understand what is happening as well as for software telemetry and other purposes.  However, setting up Python [`logging`](https://docs.python.org/3/library/logging.html) or most similar packages is (IMHO) complicated and verbose if you don't need all its features.

_Sidetrack_ (<ins><b>Si</b></ins>mple <ins><b>de</b></ins>bug <ins><b>trac</b></ins>ing pac<ins><b>k</b></ins>age) offers a simple API that lets you turn on logging, set the output destination (which can be stdout), and sprinkle `log(f'my message and my {variable} value')` throughout your code.  Moreover, it is carefully written so that you can cause the `log` calls to be _optimized out completely_ if your run Python with the `-O` option and you prefix your `log` calls with `if __debug__`.  This leads to the following style of using Sidetrack:

``` python
...
for item in item_list:
    if __debug__: log(f'getting data for {item}')
    ...
```

When running with `-O`, the `log` statement in the loop will not simply be a no-op function call: Python will [completely discard the conditional block](https://www.engyrus.com/2013/03/idtkap-4-debug-and-o.html), as if the code did not exist.  This is as optimal as possible, and means that you do not have to worry about the performance costs of using `log` or evaluating its arguments.


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `sidetrack` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `sidetrack` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install sidetrack
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `sidetrack` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/sidetrack.git
```


Usage
-----

There are just three functions in the `sidetrack` package:
* `set_debug`: turn logging on/off, set the output destination, and configure options
* `log`: logs a message with optional arguments; the string can contain embedded `format` directives
* `logr`: logs a message as-is, without applying `format` to the string


### _How to import Sidetrack_

To take advantage of Python optimization behavior, make sure to conditionalize all references to Sidetrack functions on the Python built-in symbol `__debug__`.  This includes the import statement for Sidetrack:

``` python
if __debug__:
    from sidetrack import set_debug, log, logr
```

The fragment above illustrates another tip: to make calls to the `log` functions as short as possible in your code, import `set_debug`, `log` and `logr` directly using the `from sidetrack ...` approach instead of doing a plain `import sidetrack`, so that you can write `log(...)` instead of `sidetrack.log(...)`.  Believe me, your fingers and eyes will thank you!


### _How to turn on debug logging_

To turn on logging, call `set_debug(...)` at least once in your code.  Often, this will most convenient if combined with a command-line argument to your program, so that debug tracing can be enabled or disabled at run-time.  The following example shows the basic usage.

``` python
if __debug__:
    set_debug(True)
else:
    print('Python -O is in effect, so debug logging is not available.')
```

The above will turn on debug logging and send output to the default destination, which is the standard error stream (`sys.stderr`).  To send the output to a different destination, use the optional second argument `debug_output`, which can be either a file name, a stream, or the dash symbol (`-`); the latter indicates the destination should be the default (i.e., `sys.stderr`).  Here is an example:

``` python
if __debug__:
    set_debug(True, '/tmp/debug.txt')
```

The function `set_debug(...)` also accepts another optional argument, `extra`, that lets you prefix every output line with extra text of your choosing.  The `extra` text string can contain [Python logging system % formatting strings](https://docs.python.org/library/logging.html#logrecord-attributes).  For example, the process ID can be inserted by passing `'%(process)d'` as in the following example:

``` python
if __debug__:
    set_debug(True, debug_output, extra = '%(process)d')

```
If your program uses threads, you may find the use of `extra = "%(threadName)s"` helpful.


### _How to call `log` and `logr` and format the output_

The `log` function accepts one argument, a string, and any number of optional arguments.  Here's an example from an actual program that uses Sidetrack:

``` python
if __debug__: log('exception (failure #{}): {}', failures, str(ex))
```

Internally, `log` applies `format` to the string and passes any remaining arguments as the arguments to `format`.  In other words, it is essentially the following pseudocode:

``` python
def log(msg, *other_args):
    final_text = msg.format(*other_args)
    write_log(final_text)
```

In the age of Python f-strings, the above may seem redundant and unnecessary: why not simply call `log` with an f-string?  In fact, in almost all cases, you can; however, there are also situations where f-strings cannot be used due to how they are evaluated at run time or due to [certain inherent limitations](https://www.python.org/dev/peps/pep-0498/#differences-between-f-string-and-str-format-expressions).  Having `log` operate like a call to `format` gives you the flexibility of using either style without having to remember a different API: you can use `log(f'some {value}')` if you wish, or `log('some {}', value)` if you prefer.

The alternative function `logr` (`r` for _raw_) is available for use in situations where the string argument must _not_ be passed to `format`.  This is handy when the string contains character sequences that have special meaning to `format`, particularly in situations where the string contains references to variables that _might_ expand at run time to contain those characters &ndash; in other words, something that would be misinterpreted by `format` but is difficult to escape.

In all cases, each line of the output has the following form:

<p align="center">
<i>extra</i>&nbsp;&nbsp;<b>filename:lineno</b>&nbsp;&nbsp;<b>function()</b> -- <b>message</b>
</p>

where _extra_ is optional and controlled by the argument `extra` to `set_debug(...)`, and the remaining values are always printed: the file name, line number and function where the call to the `log` or `logr` was made, and the message.  Examples are shown in the next section.


### _Tips for using Sidetrack_

Throughout the rest of your code, in places where it's useful, add calls to `log(...)` and/or `logr(...)`.  Here's a simple contrived example, taken from the [demonstration program](tests/demo_debug.py) supplied with Sidetrack:


``` python
if __debug__: log('=== demo program starting ===')

print('Looping my loopy loop:')
for i in range(0, 3):
    if __debug__: log(f'loop value {i}')
    print('Another go-around the loop')
print('Done looping.')

if __debug__: log('=== demo program stopping ===')
```

With the code above, if debugging is _not_ turned on, _or_ the program is running with [Python optimization turned on](https://docs.python.org/3/using/cmdline.html#cmdoption-o), the output will be:

``` text
Looping my loopy loop:
Another go-around the loop
Another go-around the loop
Another go-around the loop
Done looping.
```

With debugging turned on and the destination set to `-`, the output becomes:

``` text
demo_debug.py:32 main() -- === demo program starting ===
Looping my loopy loop:
demo_debug.py:36 main() -- loop value 0
Another go-around the loop
demo_debug.py:36 main() -- loop value 1
Another go-around the loop
demo_debug.py:36 main() -- loop value 2
Another go-around the loop
Done looping.
demo_debug.py:40 main() -- === demo program stopping ===
```

Being able to send the debug output to a file becomes useful when dealing with longer and more complicated programs &ndash; it makes it possible to store a detailed trace without cluttering the output as it is in the sample above.  File output can also be useful for deployed code: you can leave the debug functionality in your code and instruct your users to turn on debugging with output directed to a file, then send you the file so you can debug problems more easily.


### _How to run the demo program_

In the [`tests`](tests) subdirectory, there is a simple demonstration program illustrating the use of Sidetrack.  To run it, on Linux and macOS systems, you can start a terminal shell and run the following commands:

``` shell
python3 tests/demo_debug.py -h
```

To run it with debug logging enabled, use the `-d` command-line option (where the output in this example is given as `-`, which means to send the output to the terminal):

``` shell
python3 tests/demo_debug.py -d -
```

To see the difference when Python optimization is active, add the `-O` option to the Python interpreter:

``` shell
python3 -O tests/demo_debug.py -d -
```


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/sidetrack/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing `sidetrack`!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2020, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

I developed the first version of this code while implementing [Spiral](https://github.com/casics/spiral).  I started using the code in essentially every Python software package I have written since then, first by copy-pasting the code (which was initially very short) and eventually creating a single-file module (named `debug.py`).  This was obviously a suboptimal approach.  Finally, in 2020, I decided it was time to break it out into a proper self-contained Python package.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/debug/3482208/) of a document with a line break, used as the icon for this repository, was created by [iconixar](https://thenounproject.com/iconixar/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://github.com/caltechlibrary/sidetrack/raw/main/.graphics/caltech-round.svg">
  </a>
</div>
