.. code-block:: text

          _
      ___| |__   ___ _ ____   __
     / __| '_ \ / _ | '_ \ \ / /
    | (__| | | |  __| | | \ V /
     \___|_| |_|\___|_| |_|\_/ . modern local environment management

|Status| |PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |Status| image:: https://badgen.net/badge/status/alpha/d8624d
   :target: https://badgen.net/badge/status/alpha/d8624d
   :alt: Project Status
.. |PyPI| image:: https://img.shields.io/pypi/v/chenv.svg
   :target: https://pypi.org/project/chenv/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/chenv
   :target: https://pypi.org/project/chenv
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/chenv
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/chenv/latest.svg?label=Read%20the%20Docs
   :target: https://chenv.readthedocs.io/
   :alt: Read the documentation at https://chenv.readthedocs.io/
.. |Tests| image:: https://github.com/jonathan-shemer/chenv/workflows/Tests/badge.svg
   :target: https://github.com/jonathan-shemer/chenv/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/jonathan-shemer/chenv/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jonathan-shemer/chenv
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


This command-line interface creates and manages local `.env` files from various sources.

Coupled with `python-dotenv <https://pypi.org/project/python-dotenv/>`_ for python,
or `dotenv <https://www.npmjs.com/package/dotenv/>`_ for node.js development,
it provides better, more consistent environment variable management and developement.

Installation
------------

To install `chenv`,
run this command in your terminal:

.. code-block:: shell

   $ pip install --user chenv

Also make sure that your :code:`$PATH` includes :code:`$HOME/.local/bin`.
If not, add this line to your :code:`.bashrc` / :code:`.zshrc`:

.. code-block:: shell

   export PATH=$HOME/.local/bin:$PATH;

Usage
-----

`chenv`'s usage looks like:

.. code-block:: shell

   $ chenv COMMAND [ARGS]

Commands currently include:

=====
blank
=====

   Choose to set `.env` as a new, blank, `.env.blank` file.

======
heroku
======

   Choose to set `.env` from a remote heroku app config-vars, as `.env.[app-name]`.

   - -t <team>, --team <team>
       Pre-fill team name

   - -a <app>, --app <app>
      Pre-fill app name

=====
local
=====

   Choose to set `.env` from a local, pre-exsiting `.env.*` file.

   - filename
      Pre-fill file-suffix name

Project Configurations
----------------------

`chenv` also provides two file types that manipulate the output of new `.env.*` files being set.

==========
.envignore
==========

   Specifies intentionally unwanted environment-variables.
   Each line in a envignore file specifies a pattern.

   When deciding whether to ignore an environment variable, `chenv` checks it's key against the list of patterns described in this file.

   :Pattern:
      `.envignore` uses the unix filename pattern matching, similar to `.gitignore`'s, and as specified at https://docs.python.org/3/library/fnmatch.html

=========
.envmerge
=========

   Sepecifies environment variables to merge / override after any input is chosen. This provides consistency to preffered settings such as the `logging-level`, or `NODE_ENV` for local development usage in node.js.
