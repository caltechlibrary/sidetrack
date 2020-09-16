Sidetrack<img width="11%" align="right" src="https://github.com/caltechlibrary/sidetrack/raw/main/.graphics/sidetrack-logo.png">
===========================================================================

_Sidetrack_ provides a simple interface to writing log messages for tracing and debugging your Python programs.  They can be left in your code to provide a way for users to produce detailed debug traces in the field; if performance matters, using a certain coding idiom and the Python optimization flag (`-O`) will cause the log statements to be skipped completely.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/sidetrack.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/sidetrack/releases)


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

IDEs are great for debugging and tracing execution of your code, but they can't be used in all situations.  For example, if your code is executing on multiple remote computers, or you have released a program to general users and you would like them to send you a debug log/trace of execution, using an IDE at runtime may be impractical or impossible.  Logging packages such as [`logging`](https://docs.python.org/3/library/logging.html) are made exactly for these situations; however, setting up Python [`logging`](https://docs.python.org/3/library/logging.html) or most similar packages is (IMHO) frustratingly complicated and verbose.

_Sidetrack_ (<ins><b>Si</b></ins>mple <ins><b>de</b></ins>bug <ins><b>trac</b></ins>ing pac<ins><b>k</b></ins>age) offers a simple API that lets you turn on debugging, set the output destination (which can be stdout), and sprinkle `log(f'my message and my {variable} value')` throughout your code.  Moreover, it is carefully written so that you can cause the logging code to be optimized out by Python if your run Python with the `-O` option and you prefix your `log` calls with `if __debug__`.  This leads to the following style of using Sidetrack:

``` python
...
for item in item_list:
    if __debug__: log(f'getting data for {item}')
    ....
```

When running with `-O`, the `log` statement will not simply be a no-op function call: Python will [completely discard the conditional block](https://www.engyrus.com/2013/03/idtkap-4-debug-and-o.html), as if the code did not exist.  This is as optimal as possible, and means that you do not have to worry about the performance costs of using `log` or evaluating its arguments.


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first install Python version 3 and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `sidetrack` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `sidetrack` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install sidetrack --upgrade
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `sidetrack` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/sidetrack.git --upgrade
```


Usage
-----




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
