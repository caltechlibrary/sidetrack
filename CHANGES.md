Change log for Sidetrack
========================

Version 1.4.0
-------------

This version adds a new option to `set_debug(...)`: the flag `show_package`, which will cause Sidetrack to prefix messages with the name of the Python package containing the source file from where the log function was called.  This flag is useful if you use Sidetrack in multiple packages, or import packages that also use Sidetrack.


Version 1.3.0
-------------

This version changes the logging level used by Sidetrack.  The level is now set to the value of [logging.DEBUG](https://docs.python.org/3/library/logging.html#levels) + 1 (that is, the numeric value 11).  This solves a problem caused by Python packages that turn off `DEBUG`-level logging at import time: previously, if such a package was imported after Sidetrack was loaded, it would end up disabling Sidetrack as a side-effect.  This should no longer happen.  (As a result, we can now legitimately say that **Sidetrack goes to 11**.)


Version 1.2.0
-------------

This version brings no changes to the API, but does remove a dependency on `setuptools`, and brings internal changes that solve problems in using Sidetrack inside binaries produced by [PyInstaller](https://pyinstaller.readthedocs.io).  The internal changes remove a clever but problematic scheme for retrieving package metadata, and replaces it with a more conventional approach (storing version info directly into `__init__.py`) with accompanying automation in the `Makefile` to make it all work.  Beneficial side-effect: the `import sidetrack` statement should run faster now.


Version 1.1.0
-------------

* `set_debug(...)` now takes a different optional argument, `extra`, that can be used to add text to every debug output line. The text can contain Python logging package `%` format codes.  The previous argument, `show_thread`, has been removed; `extra` is more general and can be used to achive the same ends.
* Allow the destination parameter for `set_debug(...)` to be a stream, not just '-' or a file.
* Fix documentation to explain that the default output is `sys.stderr`, not `sys.stdout`.
* Additional documentation fixes and edits.


Version 1.0.1
-------------

* Minor edits to the README file for grammar and clarity.
* Improve Makefile automation for creating releases.


Version 1.0.0
-------------

First fully usable version, for testing.
