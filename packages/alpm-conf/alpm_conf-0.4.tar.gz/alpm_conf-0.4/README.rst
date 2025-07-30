.. image:: images/coverage.png
   :alt: [alpm-conf test coverage]

`alpm-conf`_ is an ArchLinux tool to manage /etc configuration files using
``git``. It is implemented as a Python package.

Overview
--------

Files installed by ``pacman`` in the /etc directory that have been changed by
the ``root`` user [#]_ are tracked in the *master* branch of a git repository
created by the *alpm-conf* ``create`` subcommand.

Using the same algorithm used by pacman to install files with a *.pacnew*
extension [#]_, *alpm-conf* merges the changes in pacman installed files into
the files on the *master* branch. The *alpm-conf* ``sync`` subcommand is then
used to copy these files to the /etc directory.

*alpm-conf* also tracks changes in files that are created in /etc by the root
user such as *netctl* profiles for example. The files must first be added and
commited to the *master* branch by the *alpm-conf* user.

Git commands allow to:

 * List the names of files created in /etc by the root user and tracked in the
   *master* branch.
 * Print the changes made in the *master-tmp* branch before running the *sync*
   subcommand.
 * Print the changes made by the last *alpm-conf* ``update`` subcommand.
 * Print the differences between the *master* branch and the files in package
   archives currently installed by pacman.

Documentation
-------------

The documentation is hosted at `Read the Docs`_:

 - The `stable documentation`_ of the last released version.
 - The `latest documentation`_ of the current GitLab development version.

To access the documentation as a pdf document one must click on the icon at the
down-right corner of any page. It allows to switch between stable and latest
versions and to select the corresponding pdf document.

Requirements
------------

The ArchLinux packages required by *alpm-conf* are installed with the command:

.. code-block:: text

  # pacman -Sy git util-linux alpm-mtree python pyalpm python-zstandard

``pyalpm`` and ``alpm-mtree`` are used to access the ArchLinux local
database, ``util-linux`` provides *setpriv* allowing to run *alpm-conf* as root
while running git commands as the creator of the git repository.

Installation
------------

Install the `python-alpm-conf`_ package from the AUR.

Or install *alpm-conf* with pip::

  $ python -m pip install alpm-conf


.. _alpm-conf: https://gitlab.com/xdegaye/alpm-conf
.. _Read the Docs: https://about.readthedocs.com/
.. _stable documentation: https://alpm-conf.readthedocs.io/en/stable/
.. _latest documentation: https://alpm-conf.readthedocs.io/en/latest/
.. _python-alpm-conf: https://aur.archlinux.org/packages/python-alpm-conf

.. rubric:: Footnotes

.. [#] Packaged files that are modified by a package scriptlet are considered as
       files modified by the root user.
.. [#] See the **HANDLING CONFIG FILES** section in the pacman man page.
