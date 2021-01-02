chenv
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

Modern local environment management

The command-line interface creates and manages local `.env` files from various sources.

Coupled with `python-dotenv <https://pypi.org/project/python-dotenv/>`_ for python,
or `dotenv <https://www.npmjs.com/package/dotenv/>`_ for node.js development,
it provides better, more consistent environment variable management and developement.

Installation
------------

To install `chenv`,
run this command in your terminal:

.. code-block:: console

   $ pip install chenv


Usage
-----

`chenv`'s usage looks like:

.. code-block:: console

   $ chenv COMMAND [ARGS]

Commands include:

.. option:: blank

   Choose to set `.env` as a new, blank, `.env.blank` file.

.. option:: heroku

   Choose to set `.env` from a remote heroku app config-vars, as `.env.[app-name]`.

   .. option:: -t <team>, --team <team>

   Pre-fill team name

   .. option:: -a <app>, --app <app>

   Pre-fill app name

.. option:: local

   Choose to set `.env` from a local, pre-exsiting `.env.*` file.

   .. option:: filename

   Pre-fill file-suffix name

Project Configurations
----------------------

`chenv` also provides two file types that manipulate the output of new `.env.*` files being set.

.. option:: .envignore

   Specifies intentionally unwanted environment-variables.
   Each line in a envignore file specifies a pattern.

   When deciding whether to ignore an environment variable, `chenv` checks it's key against the list of patterns described in this file.

   :Pattern:
      `.envignore` uses the unix filename pattern matching, similar to `.gitignore`'s, and as specified at https://docs.python.org/3/library/fnmatch.html

.. option:: .envmerge

   Sepecifies environment variables to merge / override after any input is chosen. This provides consistency to preffered settings such as the `logging-level`, or `NODE_ENV` for local development usage in node.js.
