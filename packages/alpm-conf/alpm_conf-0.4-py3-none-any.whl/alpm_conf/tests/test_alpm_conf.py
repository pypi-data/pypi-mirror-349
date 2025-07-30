"""The alpm-conf tests."""

import os
import io
import re
import tempfile
import argparse
import shutil
from pathlib import PosixPath
from collections import namedtuple
from unittest import mock, skipIf
from contextlib import (contextmanager, redirect_stdout, redirect_stderr,
                        ExitStack)

import pyalpm

from .. import ApcError
from .. import __doc__ as ALPMCONF_DOC
from ..alpm_conf import alpm_conf, AlpmConf, sha256
from ..git import GitRepo, get_logname
from . import CustomTestCase
from .pkg_utils import (PyalpmHandle, PACMAN_PKG, create_mtree, Pkg,
                        create_cache_dir, create_etc_dir, pkg_etcfiles,
                        build_archives)

EmtDirectories = namedtuple('EmtDirectories',
                    ['database_dir', 'cache_dir', 'gitrepo_dir', 'root_dir'])
ETCMAINT_BRANCHES = set(GitRepo._ETCMAINT_BRANCHES)

@contextmanager
def patch_pyalpm(pkgs):
    with mock.patch.object(pyalpm, 'Handle', PyalpmHandle):
        PyalpmHandle.set_localdb(pkgs)
        yield

def update_args_from_dirs(apc_dirs):
    """Return update command line args from an EmtDirectories named tuple."""

    dirs = apc_dirs._asdict()
    args = []
    for key, val in dirs.items():
        args.append('--' + key.replace('_', '-'))
        args.append(str(val))
    return args

def sync_args_from_dirs(apc_dirs):
    """Return sync command line args from an EmtDirectories named tuple."""

    dirs = apc_dirs._asdict()
    args = []
    for key, val in dirs.items():
        if key in ('gitrepo_dir', 'root_dir'):
            args.append('--' + key.replace('_', '-'))
            args.append(str(val))
    return args

def iter_etcfiles(dir_path):
    """Iterator of the files in the etc directory of 'dir_path'."""

    etc_dir = dir_path / 'etc'
    for root, dirs, files in etc_dir.walk():
        for file in files:
            path = root / file
            path = path.relative_to(dir_path)
            yield str(path)

def modify_line(abspath, no, new):
    """Replace line number 'no' by 'new' in 'abspath'.

    Append 'new' to 'abspath' if 'no' is -1.
    """

    with open(abspath) as f:
        lines = f.readlines()

    with open(abspath, 'w') as f:
        for idx, line in enumerate(lines):
            if idx + 1 == no:
                f.write(new)
            else:
                f.write(line)
        if no == -1:
                f.write(new)

class CommandLineTests(CustomTestCase):

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)

    def test_main_help(self):
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'help'])

        self.assertIn(ALPMCONF_DOC, stdout.getvalue())

    def test_create_help(self):
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'help', 'create'])

        self.assertIn('Create the git repository', stdout.getvalue())

    def test_update_help(self):
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'help', 'update'])

        self.assertIn('Update the repository', stdout.getvalue())

    def test_dry_run(self):
        cache_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='cache-'))
        repo_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='repo-'))
        self.stack.enter_context(patch_pyalpm([PACMAN_PKG]))

        with redirect_stdout(io.StringIO()) as stdout:

            args = ['--cache-dir', cache_dir, '--gitrepo-dir', repo_dir]
            alpm_conf(['alpm-conf', 'create'] + args)
            apc = alpm_conf(['alpm-conf', 'update', '--dry-run'] + args)

        self.assertTrue(hasattr(apc, 'dry_run'))
        self.assertIn("[dry-run] 'update' command terminated",
                                                        stdout.getvalue())
        self.assertIn('master-tmp', apc.repo.branches)

    def test_isdir(self):
        file_path = self.stack.enter_context(tempfile.NamedTemporaryFile())

        with (self.assertRaisesRegex(argparse.ArgumentError,
                                     'not a directory'),
              redirect_stderr(io.StringIO())):

            try:
                alpm_conf(['alpm-conf', 'create',
                                        '--cache-dir', file_path.name])
            except SystemExit as e:
                raise e.__context__ from None

    def test_parse_boolean(self):
        cache_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='cache-'))
        repo_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='repo-'))
        self.stack.enter_context(patch_pyalpm([PACMAN_PKG]))

        with redirect_stdout(io.StringIO()) as stdout:

            args = ['--cache-dir', cache_dir, '--gitrepo-dir', repo_dir]
            apc = alpm_conf(['alpm-conf', 'create', '--print-not-readable',
                             'yes'] + args)

            self.assertEqual(apc.print_not_readable, True)

    def test_bad_parse_boolean(self):
        answer = 'FOO'
        with (self.assertRaisesRegex(argparse.ArgumentError, answer),
              redirect_stderr(io.StringIO())):

            try:
                alpm_conf(['alpm-conf', 'create',
                                        '--print-not-readable', answer])
            except SystemExit as e:
                raise e.__context__ from None

    def test_no_command(self):
        with (self.assertRaises(SystemExit),
                            redirect_stderr(io.StringIO()) as stderr):
            alpm_conf(['alpm-conf'])
        self.assertIn('command is required', stderr.getvalue())

    def test_ApcError(self):
        cache_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='cache-'))
        repo_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='repo-'))
        self.stack.enter_context(patch_pyalpm([PACMAN_PKG]))

        args = ['--cache-dir', cache_dir, '--gitrepo-dir', repo_dir]
        with (self.assertRaises(ApcError) as cm,
                            redirect_stderr(io.StringIO())):
            try:
                alpm_conf(['alpm-conf', 'update', '--dry-run'] + args)

            except SystemExit as e:
                raise e.__context__ from None

        self.assertIn('no git repository', str(cm.exception))

    def test_set_repo(self):
        path = PosixPath('/foobar')
        apc = AlpmConf(**{'gitrepo_dir': path})
        self.assertEqual(apc.repo.dir_path, path)

    def test_set_repo_env(self):
        path = '/foobar'
        xdg_data_home = os.environ.get('XDG_DATA_HOME')
        if xdg_data_home is not None:
            path = PosixPath(xdg_data_home)
        else:
            os.environ['XDG_DATA_HOME'] = path

        try:
            apc = AlpmConf(**{'gitrepo_dir': None})
            self.assertEqual(apc.repo.dir_path, PosixPath(path) / 'alpm-conf')
        finally:
            if xdg_data_home is None:
                del os.environ['XDG_DATA_HOME']

    @skipIf(get_logname() is None, "no controlling terminal")
    def test_set_repo_default(self):
        xdg_data_home = os.environ.get('XDG_DATA_HOME')
        if xdg_data_home is not None:
            del os.environ['XDG_DATA_HOME']

        try:
            apc = AlpmConf(**{'gitrepo_dir': None})
            self.assertTrue(apc.repo.dir_path.match(
                                                '**/.local/share/alpm-conf'))
        finally:
            if xdg_data_home is not None:
                os.environ['XDG_DATA_HOME'] = xdg_data_home

    def test_set_repo_login(self):
        xdg_data_home = os.environ.get('XDG_DATA_HOME')
        if xdg_data_home is not None:
            del os.environ['XDG_DATA_HOME']

        with (mock.patch.object(os, 'getlogin') as getlogin,
                    self.assertRaises(ApcError) as cm):
            getlogin.side_effect = OSError
            try:
                AlpmConf(**{'gitrepo_dir': None})
            finally:
                if xdg_data_home is not None:
                    os.environ['XDG_DATA_HOME'] = xdg_data_home

        self.assertIn('controlling terminal', str(cm.exception))

class AlpmConfTests(CustomTestCase):

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)

    def create_alpm_conf_env(self, pkgs, pkg_counts, new_counts,):
        """Build the environment for the creation of a repository.

        'pkgs'       list of instances of Pkg namedtuple
        'pkg_counts' list of line number counts for each file of Pkg.files
        'new_counts' list of line number counts for each file in 'root_dir'
        """

        db_path = self.stack.enter_context(
                                tempfile.TemporaryDirectory(prefix='tmp-db-'))
        db_path = PosixPath(db_path)
        for idx, pkg in enumerate(pkgs):
            create_mtree(pkg, pkg_counts[idx], db_path)

        cache_dir = self.stack.enter_context(
                                create_cache_dir(pkgs, pkg_counts))
        repo_dir = self.stack.enter_context(
                            tempfile.TemporaryDirectory(prefix='tmp-repo-'))
        repo_dir = PosixPath(repo_dir)
        root_dir = self.stack.enter_context(
                        create_etc_dir(pkgs, new_counts, prefix='root-'))
        self.stack.enter_context(patch_pyalpm(pkgs))

        return EmtDirectories(db_path, cache_dir, repo_dir, root_dir)

    def install_new_package(self, pkgs, counts, apc_dirs):
        for idx, pkg in enumerate(pkgs):
            create_mtree(pkg, counts[idx], apc_dirs.database_dir)

        build_archives(pkgs, counts, apc_dirs.cache_dir)
        self.stack.enter_context(patch_pyalpm(pkgs))

    def set_ready_to_sync(self, relpath, apc_dirs):

        # Set up the context as ready to run the 'sync' command.
        changed_line = 'first line\n'
        update_args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + update_args)

        # Modify a file in root_dir and run the 'update' command.
        modify_line(apc_dirs.root_dir / relpath, 1, changed_line)
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'update'] + update_args)

        # Install a new version of the pacman package with a change in
        # 'etc/pacman.conf' and run 'update'.
        count = [5,6,5,5]
        pkg = PACMAN_PKG._replace(version='8.0')
        self.install_new_package([pkg], [count], apc_dirs)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + update_args)

        self.assertEqual(apc.repo.branches, ETCMAINT_BRANCHES)

        return apc

    def test_create(self):
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'create'] + args)

        # Check master branch.
        apc.repo.checkout('master')
        repo_dir = apc_dirs.gitrepo_dir
        etc_dir = repo_dir / 'etc'
        self.assertFalse(etc_dir.exists())

        # Check etc branch.
        apc.repo.checkout('etc')
        self.assertEqual(set(iter_etcfiles(repo_dir)),
                                        set(pkg_etcfiles(PACMAN_PKG)))

    def test_create_many(self):
        count = 20
        files = []
        for i in range(count):
            files.append((f'etc/foo-{i}.conf', 0, 0))
        pkg = PACMAN_PKG._replace(files=tuple(files))

        pkg_count = new_count = [5 for i in range(count)]
        apc_dirs = self.create_alpm_conf_env([pkg], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'create'] + args)

        # Check master branch.
        apc.repo.checkout('master')
        repo_dir = apc_dirs.gitrepo_dir
        etc_dir = repo_dir / 'etc'
        self.assertFalse(etc_dir.exists())

        # Check etc branch.
        apc.repo.checkout('etc')
        self.assertEqual(set(iter_etcfiles(repo_dir)), set(pkg_etcfiles(pkg)))

        # Check that the git command to print the files exists.
        self.assertIn('git diff-tree --no-commit-id --name-only -r',
                                                            stdout.getvalue())

    def test_create_remove_pkgs(self):
        # Set the environment with two packages.
        foobar_pkg = Pkg('foobar', '1.0', 'x86_64',
                         (('etc/foo.conf', 0, 0), ('etc/bar.conf', 0, 0),))
        pkg_counts = new_counts = [[5,5,5,5], [5,5]]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG, foobar_pkg],
                                                    pkg_counts, new_counts)
        args = update_args_from_dirs(apc_dirs)

        # Modify a file from the 'foobar' package in root_dir.
        # This will cause the 'create' command to add the file to the master
        # branch and we can verify that the file is removed from master
        # by the next update command after the package has been removed.
        foo_conf = 'etc/foo.conf'
        with open(apc_dirs.root_dir / foo_conf, 'a') as f:
            f.write('line 5\n')

        # Create the repository.
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'create'] + args)

        # Check etc branch.
        apc.repo.checkout('etc')
        repo_dir = apc_dirs.gitrepo_dir
        self.assertEqual(set(iter_etcfiles(repo_dir)),
                set(pkg_etcfiles(PACMAN_PKG)).union(pkg_etcfiles(foobar_pkg)))

        # Check packages branch
        apc.repo.checkout('packages')
        self.assertTrue((repo_dir / PACMAN_PKG.name).is_file())
        self.assertTrue((repo_dir / foobar_pkg.name).is_file())

        # Remove 'foobar_pkg' from the list of installed packages and check
        # that its etc files are removed and the Pkg has been removed from the
        # packages branch.
        self.stack.enter_context(patch_pyalpm([PACMAN_PKG]))
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check etc branch.
        apc.repo.checkout('etc')
        repo_dir = apc_dirs.gitrepo_dir
        self.assertEqual(set(iter_etcfiles(repo_dir)),
                                        set(pkg_etcfiles(PACMAN_PKG)))

        # Check packages branch
        apc.repo.checkout('packages')
        self.assertTrue((repo_dir / PACMAN_PKG.name).is_file())
        self.assertFalse((repo_dir / foobar_pkg.name).is_file())

        # Check that 'etc/foo.conf' has been removed from master.
        output = stdout.getvalue()
        self.assertIn('Remove 1 file from the master-tmp branch', output)
        relpaths = apc.repo.list_changed_files('master')
        self.assertEqual(relpaths, [foo_conf])

    def test_create_diff(self):
        LINE_COUNT = 10
        pkg_count = [5,5,5,5]
        new_count = [5, LINE_COUNT, 5, 5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'create'] + args)

        # Check master branch.
        apc.repo.checkout('master')
        repo_dir = apc_dirs.gitrepo_dir
        with open(repo_dir / 'etc/pacman.conf') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), LINE_COUNT)
        self.assertEqual(set(iter_etcfiles(repo_dir)), {'etc/pacman.conf'})

    def test_update_pacman_file(self):
        relpath = 'etc/pacman.conf'
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        # Modify a file in root_dir and run the 'update' command.
        with open(apc_dirs.root_dir / relpath, 'a') as f:
            f.write('line 5\n')
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check master branch.
        apc.repo.checkout('master')
        repo_dir = apc_dirs.gitrepo_dir
        self.assertEqual(set(iter_etcfiles(repo_dir)), {relpath})
        self.assertEqual(sha256(repo_dir / relpath),
                                sha256(apc_dirs.root_dir / relpath))

    def test_update_remove_file(self):
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        # Modify a file in root_dir.
        # This will cause the 'create' command to add the file to the master
        # branch and we can verify that the file is removed from master
        # by the next update command.
        relpath = 'etc/pacman.conf'
        with open(apc_dirs.root_dir / relpath, 'a') as f:
            f.write('line 5\n')

        # Create the repository.
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        # Remove 3 files from the package.
        pkg = PACMAN_PKG._replace(files=(('etc/makepkg.conf', 0, 0),))
        self.stack.enter_context(patch_pyalpm([pkg]))

        # Run the 'update' command.
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check that the file is removed from master.
        output = stdout.getvalue()
        self.assertIn('Remove 3 files from the etc-tmp branch', output)
        self.assertIn('Remove 1 file from the master-tmp branch', output)
        relpaths = apc.repo.list_changed_files('master')
        self.assertEqual(relpaths, [relpath])

        # XXX
        #import time; time.sleep(3600)
        #print(stdout.getvalue())

    def test_update_local_file(self):
        relpath = 'etc/foo'
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'create'] + args)

        # Add a new etc file to root_dir and the master branch, then modify
        # this file on root_dir and run the 'update' command.
        root_relpath = apc_dirs.root_dir / relpath
        repo_relpath = apc_dirs.gitrepo_dir / relpath
        with open(root_relpath, 'w') as f:
            f.write('line 1\n')

        apc.repo.checkout('master')
        (repo_relpath).parent.mkdir()
        shutil.copyfile(root_relpath, repo_relpath)
        apc.repo.git_cmd(['add', relpath])
        apc.repo.commit(f'Add user-file {relpath}')
        with open(root_relpath, 'a') as f:
            f.write('line 2\n')

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'update'] + args)

        # Check master branch.
        self.assertEqual(set(iter_etcfiles(apc_dirs.gitrepo_dir)), {relpath})
        self.assertEqual(sha256(repo_relpath), sha256(root_relpath))

    def test_update_cherry_pick(self):
        relpath = 'etc/pacman.conf'
        changed_line = 'first line\n'
        pkg_count = new_count = [5,5,5,5]

        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        # Modify a file in root_dir and run the 'update' command.
        modify_line(apc_dirs.root_dir / relpath, 1, changed_line)
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'update'] + args)

        # Install a new version of the pacman package including a change in
        # 'etc/pacman.conf' and run 'update'.
        count = [5,6,5,5]
        pkg = PACMAN_PKG._replace(version='8.0')
        self.install_new_package([pkg], [count], apc_dirs)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check the 'master-tmp' branch.
        self.assertEqual(apc.repo.branches, ETCMAINT_BRANCHES)
        apc.repo.checkout('master-tmp')
        result_path = self.stack.enter_context(tempfile.NamedTemporaryFile())
        result_path = PosixPath(result_path.name)
        with open(result_path, 'w') as f:
            f.write(changed_line)
            for i in range(1, 6):
                f.write(f'line {i}\n')
        self.assertEqual(sha256(apc_dirs.gitrepo_dir / relpath),
                                                    sha256(result_path))

    def test_update_cherry_pick_2(self):

        # This test is the same as 'test_update_cherry_pick' except that there
        # is a second change in '/etc/pacman.conf' when a new version of the
        # pacman package is installed.
        relpath = 'etc/pacman.conf'
        changed_line = 'first line\n'
        changed_line_2 = 'second line\n'
        pkg_count = new_count = [5,5,5,5]

        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        # Modify a file in root_dir and run the 'update' command.
        modify_line(apc_dirs.root_dir / relpath, 1, changed_line)
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'update'] + args)

        # Install a new version of the pacman package including a change in
        # 'etc/pacman.conf' and with a second change in this file in root_dir,
        # and run 'update'.
        count = [5,6,5,5]
        pkg = PACMAN_PKG._replace(version='8.0')
        self.install_new_package([pkg], [count], apc_dirs)
        modify_line(apc_dirs.root_dir / relpath, 2, changed_line_2)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check the 'master-tmp' branch.
        self.assertEqual(apc.repo.branches, ETCMAINT_BRANCHES)
        apc.repo.checkout('master-tmp')
        result_path = self.stack.enter_context(tempfile.NamedTemporaryFile())
        result_path = PosixPath(result_path.name)
        with open(result_path, 'w') as f:
            f.write(changed_line)
            f.write(changed_line_2)
            for i in range(2, 6):
                f.write(f'line {i}\n')
        self.assertEqual(sha256(apc_dirs.gitrepo_dir / relpath),
                                                    sha256(result_path))

    def test_update_symlink(self):
        relpath = 'etc/pacman.conf'
        changed_line = 'first line\n'
        pkg_count = new_count = [5,5,5,5]

        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        # Modify 'relpath' in root_dir and run the 'update' command.
        modify_line(apc_dirs.root_dir / relpath, 1, changed_line)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        etc_path = apc_dirs.gitrepo_dir / relpath
        apc.repo.checkout('etc')
        sha = sha256(etc_path)

        # Change 'relpath' in root_dir to a symlink.
        abspath = apc_dirs.root_dir / relpath
        abspath.unlink()
        os.symlink(apc_dirs.root_dir, abspath)

        # Install a new version of the pacman package with a change in
        # 'etc/pacman.conf' and run 'update'.
        count = [5,6,5,5]
        pkg = PACMAN_PKG._replace(version='8.0')
        self.install_new_package([pkg], [count], apc_dirs)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check that no cherry-picking has been done and that relpath remains
        # unchanged in the etc branch.
        self.assertEqual(apc.repo.branches, set(('master', 'etc', 'packages')))
        apc.repo.checkout('etc')
        new_sha = sha256(etc_path)
        self.assertEqual(sha, new_sha)

    def test_update_conflict(self):
        relpath = 'etc/pacman.conf'
        changed_line = 'last line\n'
        pkg_count = new_count = [5,5,5,5]

        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        # Modify a file in root_dir and run the 'update' command.
        modify_line(apc_dirs.root_dir / relpath, -1, changed_line)
        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'update'] + args)

        # Install a new version of the pacman package with a change in
        # 'etc/pacman.conf' and run 'update'.
        count = [5,6,5,5]
        pkg = PACMAN_PKG._replace(version='8.0')
        self.install_new_package([pkg], [count], apc_dirs)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'update'] + args)

        # Check the 'master-tmp' branch.
        self.assertEqual(apc.repo.branches, ETCMAINT_BRANCHES)
        self.assertTrue(apc.repo.current_branch, 'master-tmp')
        self.assertEqual(['UU etc/pacman.conf'], apc.repo.get_status())
        result = ('<<<<<<< HEAD\n'
                  'last line\n'
                  '=======\n'
                  'line 5\n'
                  '>>>>>>>')
        with open(apc_dirs.gitrepo_dir / relpath) as f:
            content = f.read()
        self.assertIn(result, content)

        # Try to run the 'update' command while there is a conflict.
        with self.assertRaises(ApcError) as cm:
            try:
                apc = alpm_conf(['alpm-conf', 'update'] + args)
            except SystemExit as e:
                raise e.__context__ from None
        self.assertIn('repository is not clean', str(cm.exception))

        # Abort the cherry-pick and check the master and master-tmp branches.
        apc.repo.git_cmd('cherry-pick --abort')
        with redirect_stdout(io.StringIO()) as stdout:
            apc.repo.git_cmd('diff master...master-tmp')
        self.assertEqual(len(stdout.getvalue()), 0)

    def test_sync(self):
        relpath = 'etc/pacman.conf'
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        self.set_ready_to_sync(relpath, apc_dirs)

        # Run the 'sync' command.
        sync_args = sync_args_from_dirs(apc_dirs)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'sync'] + sync_args)

        # Check the master branch and root_dir.
        self.assertNotIn('master-tmp', apc.repo.branches)
        self.assertEqual(sha256(apc_dirs.gitrepo_dir / relpath),
                                    sha256(apc_dirs.root_dir / relpath))

    def test_sync_bad_ff(self):
        relpath = 'etc/pacman.conf'
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        apc = self.set_ready_to_sync(relpath, apc_dirs)

        path = apc_dirs.gitrepo_dir / 'foo'
        with open(path, 'w') as f:
            pass
        gitrepo = apc.repo
        gitrepo.checkout('master')
        gitrepo.git_cmd(['add', path.name])
        gitrepo.commit(f'Add {path.name}')

        # The 'sync' command fails as the merge cannot be a fast-forward.
        sync_args = sync_args_from_dirs(apc_dirs)
        with self.assertRaises(ApcError) as cm:
            try:
                alpm_conf(['alpm-conf', 'sync'] + sync_args)
            except SystemExit as e:
                raise e.__context__ from None
        self.assertTrue(bool(re.search(
            r'commits .* added .* since .* last update', str(cm.exception))))

    def test_sync_no_tmp(self):
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            alpm_conf(['alpm-conf', 'create'] + args)

        sync_args = sync_args_from_dirs(apc_dirs)
        with self.assertRaises(ApcError) as cm:
            try:
                alpm_conf(['alpm-conf', 'sync'] + sync_args)
            except SystemExit as e:
                raise e.__context__ from None
        self.assertTrue(bool(re.search(
            r'-tmp.* branches do not exist', str(cm.exception))))

    def test_sync_no_tag(self):
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        args = update_args_from_dirs(apc_dirs)

        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'create'] + args)

        # Create '-tmp' branches.
        repo = apc.repo
        for branch in ('master', 'etc', 'packages'):
            repo.checkout(branch)
            repo.create_branch(f'{branch}-tmp')

        sync_args = sync_args_from_dirs(apc_dirs)
        with self.assertRaises(ApcError) as cm:
            try:
                alpm_conf(['alpm-conf', 'sync'] + sync_args)
            except SystemExit as e:
                raise e.__context__ from None
        self.assertTrue(bool(re.search(
            r'no .cherry-pick. git tag', str(cm.exception))))

    def test_sync_symlink(self):
        relpath = 'etc/pacman.conf'
        pkg_count = new_count = [5,5,5,5]
        apc_dirs = self.create_alpm_conf_env([PACMAN_PKG], [pkg_count],
                                                                [new_count])
        self.set_ready_to_sync(relpath, apc_dirs)

        # Change 'relpath' in root_dir as a symlink.
        abspath = apc_dirs.root_dir / relpath
        abspath.unlink()
        os.symlink(apc_dirs.root_dir, abspath)

        # Run the 'sync' command.
        sync_args = sync_args_from_dirs(apc_dirs)
        with redirect_stdout(io.StringIO()) as stdout:
            apc = alpm_conf(['alpm-conf', 'sync'] + sync_args)

        # Check the master branch and root_dir.
        self.assertNotIn('master-tmp', apc.repo.branches)
        output = stdout.getvalue()
        self.assertIn('Nothing to do', output)
        self.assertTrue(bool(re.search(
                        r'warning: .* not synced, does not exist', output)))

def main():
    # Run some tests with 'python -m alpm_conf.tests.test_alpm_conf'.
    test = AlpmConfTests()
    test.setUp()
    test.test_update_remove_file()

if __name__ == '__main__':
    main()
