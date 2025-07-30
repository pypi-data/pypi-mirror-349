.. _alpm-conf:

alpm-conf man page
==================

Synopsis
--------

:program:`alpm-conf` help {create, update, sync}

:program:`alpm-conf` {create, update, sync} [*options*]

*alpm-conf* is an ArchLinux tool to manage /etc configuration files using
git. See the documentation at https://alpm-conf.readthedocs.io/en/stable/.

create
------

::

  usage: alpm-conf create [--database-dir DATABASE_DIR] [--cache-dir CACHE_DIR]
                        [--print-not-readable ('1', 'yes', 'true')|('0', 'no', 'false')]
                        [--gitrepo-dir GITREPO_DIR] [--root-dir ROOT_DIR]

Create the git repository and populate the etc and master branches.

.. option:: --database-dir DATABASE_DIR

The pacman database directory (default: /var/lib/pacman/).

.. option:: --cache-dir CACHE_DIR

The pacman cache directory (default: /var/cache/pacman/pkg/).

.. option:: --print-not-readable ('1', 'yes', 'true')|('0', 'no', 'false')

Print ignored etc-files that do not have others-read-permission (default: false).

.. option:: --gitrepo-dir GITREPO_DIR

The git repository directory (default: None). The git repository is located at
GITREPO_DIR when this option is set, otherwise at $XDG_DATA_HOME/alpm-conf if
the XDG_DATA_HOME environment variable is set, otherwise at
$HOME/.local/share/alpm-conf.

.. option::  --root-dir ROOT_DIR

The root directory, used for testing (default: /).

update
------

::

  usage: alpm-conf update [--dry-run] [--database-dir DATABASE_DIR] [--cache-dir CACHE_DIR]
                        [--print-not-readable ('1', 'yes', 'true')|('0', 'no', 'false')]
                        [--gitrepo-dir GITREPO_DIR] [--root-dir ROOT_DIR]

Update the repository with packages and user changes.

The changes are made in the *packages-tmp*, *etc-tmp* and
*master-tmp* temporary branches. When the cherry-pick list is not
empty, files from this list need to be copied to /etc with the ``sync``
command. Otherwise for each one of the *packages*, *etc* and *master*
branches:

  * A tag named *<branch>-prev* is created at *<branch>* before the
    merge.
  * Changes from *<branch>-tmp* are incorporated into *<branch>* with a
    fast-forward merge.
  * The *<branch>-tmp* is removed.

.. option:: --dry-run, -n

Perform a trial run with no changes made (default: False).

.. option:: --database-dir DATABASE_DIR

The pacman database directory (default: /var/lib/pacman/).

.. option:: --cache-dir CACHE_DIR

The pacman cache directory (default: /var/cache/pacman/pkg/).

.. option:: --print-not-readable ('1', 'yes', 'true')|('0', 'no', 'false')

Print ignored etc-files that do not have others-read-permission (default: false).

.. option:: --gitrepo-dir GITREPO_DIR

The git repository directory (default: None).

.. option:: --root-dir ROOT_DIR

The root directory, used for testing (default: /).

sync
----

::

  usage: alpm-conf sync [--gitrepo-dir GITREPO_DIR] [--root-dir ROOT_DIR]

Incorporate changes made by the previous ``update`` command into /etc.

Copy to the /etc directory the files of the *master-tmp* branch that are
listed in the cherry-pick commit and for each one of the *packages*,
*etc* and *master* branches:

  * A tag named *<branch>-prev* is created at *<branch>* before the
    merge.
  * Changes from *<branch>-tmp* are incorporated into *<branch>* with a
    fast-forward merge.
  * The *<branch>-tmp* is removed.

.. option:: --gitrepo-dir GITREPO_DIR

The git repository directory (default: None).

.. option:: --root-dir ROOT_DIR

The root directory, used for testing (default: /).
