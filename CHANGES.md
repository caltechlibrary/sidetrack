Change log for Sidetrack
========================

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
