"""The 'alpm-conf' command."""

import sys
import os
import re
import hashlib
import argparse
import inspect
import shutil
import traceback
from pathlib import PosixPath
from textwrap import dedent
from collections import namedtuple

from . import __version__, __doc__, ApcError, warn
from .git import GitRepo
from .packages import PacmanDataBase, get_pacman_dirs

def sha256(abspath):

    try:
        if abspath.is_symlink():
            return None

        hash = hashlib.sha256()
        with abspath.open('rb') as f:
            hash.update(f.read())
        return hash.hexdigest()
    except OSError:
        pass

    return None

# The return value of AlpmConf.run_pacman_logic().
CherryPick = namedtuple('CherryPick',
                            ['cherrypick_set', 'cherrypick_commit_sha'],
                            defaults=(set(), None))

class AlpmConf():
    """Provide methods to implement the alpm-conf commands."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        if not hasattr(self, 'dry_run'):
            self.dry_run = False

        self.repo = GitRepo(self.gitrepo_dir)

    def run_cmd(self, command):
        """Run the alpm-conf command."""

        assert command.startswith('cmd_')
        self.cmd = command[4:]
        method = getattr(self, command)

        # The sync subcommand is the only command that can be run as root
        # except when the repository has been created by root.
        if self.repo.root_not_repo_owner and command != 'cmd_sync':
            raise ApcError('cannot be executed as root')

        try:
            if command != 'cmd_create':
                self.repo.open()
            method()
        finally:
            self.repo.close()

    def cmd_create(self):
        """Create the git repository and populate the etc and master branches.

        The git repository is located at the directory specified by the
        command line option '--gitrepo-dir' when this option is set, otherwise
        at $XDG_DATA_HOME/alpm-conf if the XDG_DATA_HOME environment variable
        is set, otherwise at $HOME/.local/share/alpm-conf.
        """

        self.repo.create()
        self.update_repository('create')
        print(f'Git repository created at {self.repo.dir_path}')

    def cmd_update(self):
        """Update the repository with packages and user changes.

        The changes are made in the 'packages-tmp', 'etc-tmp' and
        'master-tmp' temporary branches. When the cherry-pick list is not
        empty, files from this list need to be copied to /etc with the 'sync'
        command. Otherwise for each one of the 'packages', 'etc' and 'master'
        branches:
          - A tag named '<branch>-prev' is created at '<branch>' before the
            merge.
          - Changes from '<branch>-tmp' are incorporated into '<branch>' with a
            fast-forward merge.
          - The '<branch>-tmp' is removed.
        """

        self.update_repository('update')

    def cmd_sync(self):
        """Incorporate changes made by the previous 'update' command into /etc.

        Copy to the /etc directory the files of the 'master-tmp' branch that
        are listed in the cherry-pick commit and for each one of the
        'packages', 'etc' and 'master' branches:
          - Create a tag named '<branch>-prev' at '<branch>' before the merge.
          - Incorporate changes from '<branch>-tmp' into '<branch>' with a
            fast-forward merge.
          - Remove '<branch>-tmp'.
        """

        tmp_branches = {'packages-tmp', 'etc-tmp', 'master-tmp'}
        common = tmp_branches.intersection(self.repo.branches)
        missing = tmp_branches.difference(common)
        if missing:
            raise ApcError(
                f'Nothing to sync: {missing} branches do not exist')

        # Check there are no user commits since last 'update' command.
        for branch in ('packages', 'etc', 'master'):
            self.repo.check_fast_forward(branch)

        # Find the 'cherry-pick' tag.
        relpaths = None
        tags = self.repo.git_cmd('tag')
        if 'cherry-pick' in tags.splitlines():
            cherry_picked = self.repo.git_cmd(
                                    'diff-tree -r --name-only cherry-pick')
            cherry_picked = cherry_picked.splitlines()

            # Check that the 'cherry-pick' tag is within the 'etc-tmp' branch.
            rev_list = self.repo.git_cmd('rev-list etc..etc-tmp')
            if cherry_picked[0] in rev_list.splitlines():
                relpaths = cherry_picked[1:]

        if relpaths is None:
            raise ApcError("Nothing to sync: no 'cherry-pick' git tag on"
                           " the 'etc-tmp' branch")

        # Copy the files to /etc.
        if relpaths:
            self.repo.checkout('master-tmp')

            for relpath in list(relpaths):
                current = self.root_dir / relpath
                if not current.is_file() or current.is_symlink():
                    relpaths.remove(relpath)
                    warn(f'{current} not synced, does not exist or a symlink')
                    continue

                master = self.repo.dir_path / relpath
                try:
                    # Skip copying when the /etc file had been copied to the
                    # 'master-tmp' branch.
                    cur_sha = sha256(current)
                    master_sha = sha256(master)
                    assert master_sha is not None
                    if cur_sha == master_sha:
                        relpaths.remove(relpath)
                        continue

                    shutil.copyfile(master, current, follow_symlinks=False)
                except OSError as e:
                    relpaths.remove(relpath)
                    warn(f'{current} not synced, cannot copy to /etc: {e}')
                    continue

        if relpaths:
            print(f"Files copied from the master-tmp branch to"
                  f" '{self.root_dir}':")
            for relpath in relpaths:
                print(f'  {relpath}')
        else:
            print('Nothing to do')

        self.merge_fastforward()
        self.remove_tmp_branches()
        print("'sync' command terminated")

    def create_tmp_branches(self):

        self.remove_tmp_branches()
        print('Create the temporary branches')

        for branch in ('packages', 'etc', 'master'):
            tmp_branch = f'{branch}-tmp'
            self.repo.create_branch(tmp_branch, branch)

    def remove_tmp_branches(self):

        branches = self.repo.branches
        if 'master-tmp' not in branches:
            assert 'etc-tmp' not in branches
            assert 'packages-tmp' not in branches
            return

        print('Remove the temporary branches')

        for branch in ('packages', 'etc', 'master'):
            tmp_branch = f'{branch}-tmp'
            if tmp_branch in branches:
                if self.repo.current_branch == tmp_branch:
                    self.repo.checkout(branch)
                self.repo.git_cmd(f'branch --delete --force {tmp_branch}')

        # Remove references to the '-tmp' branches.
        # Except for the 'etc-tmp' branch when it has the 'cherry-pick' tag.
        self.repo.git_cmd('reflog expire --all --expire-unreachable=0')

    def merge_fastforward(self):

        for branch in ('packages', 'etc', 'master'):
            tmp_branch = f'{branch}-tmp'
            rev_list = self.repo.git_cmd(f'rev-list {branch}..{tmp_branch}')
            if not rev_list:
                continue

            # Tag the branch as '<branch>-prev' before the merge.
            self.repo.git_cmd(f'tag -f {branch}-prev {branch}')

            # Do a fast-forward merge without having to checkout 'branch'.
            if self.repo.current_branch == branch:
                self.repo.checkout(tmp_branch)
            print(f"Merge changes from the {tmp_branch} branch into {branch}")
            self.repo.git_cmd(f'fetch . {tmp_branch}:{branch}')

    def init_update(self):
        # Initialize access to the pacman database.
        pacman_conf = {
            'root_dir':     self.root_dir,
            'db_path':      self.database_dir,
            'cache_dir':    self.cache_dir,
        }
        self.pacman_db = PacmanDataBase(pacman_conf)
        self.pacman_db.init()

    def print_commits(self, suffix=''):

        indent = ' ' * 4
        commit_line_re = re.compile(r'\s*commit\s+([0-9abcdef]+)')

        for branch in ('etc', 'master'):
            tmp_branch = branch + '-tmp'
            rev_list = self.repo.git_cmd(
                        f'rev-list --format=%b%n%s {branch}..{tmp_branch}')
            if not rev_list:
                continue

            print(f'Commits in the {branch}{suffix} branch:')

            # Print the commits in chronological order.
            for line in reversed(rev_list.splitlines()):
                match = commit_line_re.match(line)
                if match is not None:
                    sha = match.group(1)
                    relpaths = self.repo.list_changed_files(sha)

                    list_relpath = (f'diff-tree --no-commit-id --name-only -r'
                                    f' {sha}')
                    if branch == 'etc' and len(relpaths) > 10:
                        print(f"{indent}git command to list the files:")
                        print(f"{indent}  'git {list_relpath}'")
                        print()
                        continue

                    lines = (sorted(relpaths) if relpaths else
                                                            ['empty commit'])
                    print('\n'.join((indent + l) for l in lines))
                    print()
                elif line:
                    print(f'  {line}')

    def copy_to_repo(self, abspath, relpath):
        """Copy a file to the repository.

        'relpath' type is PosixPath or str.
        """

        repo_path = self.repo.dir_path / relpath
        dirname = repo_path.parent
        if dirname and not dirname.is_dir():
            dirname.mkdir(parents=True)

        shutil.copy(abspath, repo_path, follow_symlinks=False)

    def commit_etc_files(self, relpaths, files_type):
        """Commit a list of files from /etc that have been modified."""

        if not relpaths:
            return

        self.repo.checkout('master-tmp')

        relpath_list = []
        for relpath in relpaths:
            sha = sha256(self.repo.dir_path / relpath)
            current = self.root_dir / relpath
            cur_sha = sha256(current)
            if cur_sha is not None and sha != cur_sha:
                self.copy_to_repo(current, relpath)
                relpath_list.append(relpath)

        if relpath_list:
            length = len(relpath_list)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['add'] + relpath_list)
            self.repo.commit(f'Add or update {length} {files_type}{plural}'
                             f' from /etc to the master-tmp branch')

    def update_packages_branch(self):
        """Update the 'packages-tmp' branch

        with the changes in the pacman database since the last 'sync' command.
        """

        # To be consistent with the naming in packages.py, in the following
        # code 'pkg' is an instance of pyalpm.Package and 'package' is an
        # instance of packages.Package.

        self.repo.checkout('packages-tmp')

        # Remove from the packages branch the packages that are not installed
        # any more.
        packages_tracked = self.repo.tracked_files('packages-tmp')
        installed_packages = [pkg.name for pkg in
                                    self.pacman_db.installed_packages]
        removed = packages_tracked.difference(installed_packages)
        if removed:
            length = len(removed)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['rm'] + list(removed))
            self.repo.commit(f'Remove {length} package{plural}'
                             f' from the packages-tmp branch')

        # Add to the packages branch the new packages that have etc files.
        new_packages = self.pacman_db.list_new_packages(self.repo.dir_path,
                                    print_not_readable=self.print_not_readable)
        if new_packages:
            files = {}
            for package in new_packages:
                files[package.name] = str(package)
            self.repo.add_files(files, f'Add or update {len(new_packages)}'
                                f' packages to the packages branch')

    def remove_etc_files(self):

        # Remove from the etc branch the etc files that are not in the
        # installed packages.
        etc_tracked = self.repo.tracked_files('etc-tmp')
        etc_files = self.pacman_db.installed_files
        removed = etc_tracked.difference(etc_files)
        if removed:
            self.repo.checkout('etc-tmp')

            length = len(removed)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['rm'] + list(removed))
            self.repo.commit(f'Remove {length} file{plural}'
                             f' from the etc-tmp branch')

        return removed

    def remove_master_files(self, removed_files):

        if not removed_files:
            return

        # Remove from the master branch the files that have been removed
        # from the etc branch.
        master_tracked = self.repo.tracked_files('master-tmp')
        removed = master_tracked.intersection(removed_files)
        if removed:
            self.repo.checkout('master-tmp')

            length = len(removed)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['rm'] + list(removed))
            self.repo.commit(f'Remove {length} file{plural}'
                             f' from the master-tmp branch')

    def run_pacman_logic(self):
        """Implement pacman 'HANDLING CONFIG FILES' (see pacman man page).

        The pacman terminology:
            original        file in the etc-tmp branch
            current         file in /etc
            new             file in the pacman archive

        State before pacman upgrade              State after logic applied

        case 1:  original=X  current=X  new=X    no change
        case 2:  original=X  current=X  new=Y    current=Y
        case 3:  original=X  current=Y  new=X    no change
        case 4:  original=X  current=Y  new=Y    no change
        case 5:  original=X  current=Y  new=Z    need merging
        case 6:  original=0  current=Y  new=Z      idem

        State upon entering this method after pacman upgrade:

        case 1:  original=X  current=X  new=X
        case 2:  original=X  current=Y  new=Y    becomes same as case 4
        case 3:  original=X  current=Y  new=X
        case 4:  original=X  current=Y  new=Y
        case 5:  original=X  current=Y  new=Z    need merging
        case 6:  original=0  current=Y  new=Z      idem

        Pseudo code handling the changes:

            if new != original:
                # Cases 5, 6.
                if current != new and current != original:
                  git add 'new' to 'cherrypick_set'

                # Cases 2, 4.
                else:
                    git add 'new' to 'etc_list'

        """

        self.repo.checkout('etc-tmp')

        # Copy to the etc branch the installed etc files (that are new or
        # different from the original etc files).
        self.pacman_db.extract_files(self.repo.dir_path)

        if not len(self.pacman_db.new_files):
            return CherryPick()

        # By construction, 'new_files' and 'original_files' have the same keys
        # and their corresponding sha256 are different.
        etc_list = []
        cherrypick_set = set()
        etc_tracked = self.repo.tracked_files('etc-tmp')
        has_warnings = False
        for path, new_sha in self.pacman_db.new_files.items():

            relpath = str(path)
            original_sha = self.pacman_db.original_files[path]

            current = self.root_dir / path
            cur_sha = sha256(current)

            # Ignore a file on the etc branch that, in /etc, does not exist or
            # is not readable or is a symlink.
            if (not current.is_file() or current.is_symlink() or not
                        os.access(current, os.R_OK)):
                warn(f"Ignore '{relpath}' (missing or symlink or"
                     f" not readable in /etc)")
                has_warnings = True
                if relpath in etc_tracked:
                    self.repo.git_cmd(['checkout', relpath])
                else:
                    (self.repo.dir_path / relpath).unlink()
                continue

            # Cases 5, 6.
            # - 'new_sha' is never None.
            # - 'original_sha' may be None if the file did not exist.
            if cur_sha not in (new_sha, original_sha):
                # No previous install, add the /etc file to the master branch.
                if original_sha is None:
                    etc_list.append(relpath)
                else:
                    cherrypick_set.add(relpath)

            # Cases 2, 4.
            else:
                etc_list.append(relpath)

        cherrypick_commit_sha = None
        if cherrypick_set:
            length = len(cherrypick_set)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['add'] + list(cherrypick_set))
            self.repo.commit(f'Update {length} file{plural} - commit'
                             f' cherry-picked in master-tmp')
            # Get the commit sha of the previous commit.
            cherrypick_commit_sha = self.repo.git_cmd('rev-list -1 HEAD')

            # Tag the cherry-pick commit (to be used by cmd_sync()).
            self.repo.git_cmd('tag -f cherry-pick HEAD')

        if etc_list:
            length = len(etc_list)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['add'] + etc_list)
            self.repo.commit(f'Add or update {length} file{plural} in the'
                             f' etc-tmp branch')

        if has_warnings:
            print()
        return CherryPick(cherrypick_set, cherrypick_commit_sha)

    def update_user_changes(self):
        """Update the 'master-tmp' branch with changes to user-files."""

        # Update the repository with changes made to files in /etc that are
        # not installed by pacman (i. e. they are tracked by the 'master-tmp'
        # branch but not by the 'etc-tmp' branch).

        master_tracked = self.repo.tracked_files('master-tmp')
        etc_tracked = self.repo.tracked_files('etc-tmp')
        relpaths = master_tracked.difference(etc_tracked)

        self.commit_etc_files(relpaths, 'user-file')

    def update_etc_changes(self):
        """Update the 'master-tmp' branch with changes to packaged-files."""

        self.repo.checkout('etc-tmp')

        # Get the list of files in the 'etc-tmp' branch that are different
        # from files in /etc.
        etc_tracked = self.repo.tracked_files('etc-tmp')
        etc_files = set()
        for relpath in etc_tracked:
            sha = sha256(self.repo.dir_path / relpath)
            current = self.root_dir / relpath
            cur_sha = sha256(current)
            if cur_sha is not None and sha != cur_sha:
                etc_files.add((relpath, current, cur_sha))

        # Get the list of files that need to be copied to the 'master-tmp'
        # branch.
        relpaths = []
        if etc_files:
            self.repo.checkout('master-tmp')

            for relpath, current, cur_sha in etc_files:
                sha = sha256(self.repo.dir_path / relpath)
                if sha != cur_sha:
                    self.copy_to_repo(current, relpath)
                    relpaths.append(relpath)

        if relpaths:
            length = len(relpaths)
            plural = 's' if length > 1 else ''
            self.repo.git_cmd(['add'] + relpaths)
            self.repo.commit(f"Update {length} packaged file{plural}"
                f" changed by the root user or by a package's scriptlet")

    def print_conflicts(self, conflicts, stdout):

        self.print_commits(suffix='-tmp')

        print('List of files with a conflict to resolve:')
        print('\n'.join(f'  {c}' for c in sorted(conflicts)))

        plural = 's' if len(conflicts) > 1 else ''
        print()
        print(
            'This is the output of the git cherry-pick command:')
        print('\n'.join(f'  {l}' for l in stdout.splitlines()))
        print()

        print(f'Please resolve the conflict{plural}:')

        # In order to resolve the conflict the current working
        # directory must be within the repository.
        curdir = PosixPath.cwd()
        repo_dir = self.repo.dir_path
        if curdir.parts[:len(repo_dir.parts)] != repo_dir.parts:
            print(
                f"You must change the current working directory to the"
                f" repository at '{repo_dir}' where the master-tmp banch"
                f" is checked out.\n"
            )

        print(
            f"Run the command 'git cherry-pick --continue' after"
            f" resolving the conflict{plural} and remove left over files with"
            f" the '.orig' suffix. You may then"
            f" use the 'sync' command to copy the changes to /etc and"
            f" merge the changes from the master-tmp branch to"
            f" the master branch.\n\n"
            f"At any time you may run 'git cherry-pick --abort' and start"
            f" over later with another 'update' command."
            )

    def cherry_pick(self, cherrypick):

        self.repo.checkout('master-tmp')

        try:
            self.repo.cherry_pick(cherrypick.cherrypick_commit_sha)
        except ApcError as e:
            # See 'git help status'.
            conflicts = [line for line in self.repo.get_status()
                         if 'U' in line[:2] or line[:2] in ('AA', 'DD')]
            stdout = e.__cause__.stdout
            if conflicts:
                assert (self.repo.dir_path / '.git' / 'CHERRY_PICK_HEAD').exists()
                self.print_conflicts(conflicts, stdout)
                return False
            else:
                raise ApcError(stdout) from e
        return True

    def update_repository(self, cmd):
        """Update the repository from packages updates and user updates."""

        self.init_update()
        self.create_tmp_branches()

        #   --- In the packages-tmp branch ---
        # Update the repository with the pacman database changes.
        self.update_packages_branch()


        #   --- In the etc-tmp branch ---
        removed_files = self.remove_etc_files()

        # 'cherrypick' is an instance of the CherryPick namedtuple.
        cherrypick = self.run_pacman_logic()


        #   --- In the master-tmp branch ---
        # Remove files removed from the etc branch.
        self.remove_master_files(removed_files)

        # Update the master branch with /etc files changes.
        self.update_etc_changes()

        # Update the master branch with user-files changes.
        self.update_user_changes()

        # Merge the changes to the master branch using the
        # cherrypick commit sha.
        if cherrypick.cherrypick_set:
            if self.cherry_pick(cherrypick):
                self.print_commits(suffix='-tmp')
                print("'update' command terminated, use the"
                      " 'sync' command to copy the changes to /etc and"
                      " fast-forward merge the changes from the '-tmp'"
                      " branches to the master, etc and packages branches.")

        else:
            self.print_commits()
            if self.dry_run:
                print(f"[dry-run] '{cmd}' command terminated")
            else:
                self.merge_fastforward()
                self.remove_tmp_branches()
                print(f"'{cmd}' command terminated: no file to sync"
                      f" to /etc")

def dispatch_help(options):
    """Get help on a command."""

    command = options['subcommand']
    if command is None:
        command = 'help'
    options['parsers'][command].print_help()

    cmd_func = getattr(AlpmConf, f'cmd_{command}', None)
    if cmd_func:
        lines = cmd_func.__doc__.splitlines()
        print(f'\n{lines[0]}\n')
        print(dedent('\n'.join(lines[2:])))

def parse_args(argv):
    def isdir(path):
        if path is not None:
            path = PosixPath(path)
            if not path.is_dir():
                raise argparse.ArgumentTypeError(f'{path} is not a directory')
        return path

    def parse_boolean(val):
        if val in true:
            return True
        elif val in false:
            return False
        else:
            raise argparse.ArgumentTypeError(val)

    true = ('1', 'yes', 'true')
    false = ('0', 'no', 'false')
    pacman_dirs = get_pacman_dirs('/etc/pacman.conf')

    # Instantiate the main parser.
    main_parser = argparse.ArgumentParser(description=__doc__, add_help=False,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    main_parser.add_argument('--version', '-v', action='version',
                                        version='%(prog)s ' + __version__)
    subparsers = main_parser.add_subparsers(title='alpm-conf subcommands')

    # The 'parsers' dict collects all the subparsers.
    # It is used by dispatch_help() to print the help of a subparser.
    parsers = {}
    parsers['help'] = main_parser

    # The help subparser handles the help for each command.
    help_parser = subparsers.add_parser('help', add_help=False,
                                   help=dispatch_help.__doc__.splitlines()[0])
    help_parser.add_argument('subcommand', choices=parsers, nargs='?',
                                                                default=None)
    help_parser.set_defaults(command='dispatch_help', parsers=parsers)

    # Add the command subparsers.
    d = dict(inspect.getmembers(AlpmConf, inspect.isfunction))
    for command in sorted(d):
        if not command.startswith('cmd_'):
            continue

        cmd = command[4:]
        func = d[command]
        parser = subparsers.add_parser(cmd, help=func.__doc__.splitlines()[0],
                                                            add_help=False)
        parser.set_defaults(command=command)
        if cmd == 'update':
            parser.add_argument('--dry-run', '-n', help='perform a trial run'
                ' with no changes made (default: %(default)s)',
                action='store_true', default=False)
        if cmd in ('create', 'update'):
            parser.add_argument('--database-dir',
                default=pacman_dirs['database-dir'], type=isdir,
                help='pacman database directory (default: "%(default)s")')
            parser.add_argument('--cache-dir',
                default=pacman_dirs['cache-dir'], type=isdir,
                help='pacman cache directory (default: "%(default)s")')
            parser.add_argument('--print-not-readable', default='false',
                type=parse_boolean, metavar=f'{true}|{false}',
                help='print ignored etc-files that do not have'
                ' others-read-permission (default: "%(default)s")')
        if cmd in ('create', 'update', 'sync'):
            parser.add_argument('--gitrepo-dir', type=isdir,
                help='git repository directory (default: "%(default)s")')
        parser.add_argument('--root-dir', default=pacman_dirs['root-dir'],
            help='root directory, used for testing (default: "%(default)s")',
            type=isdir)
        parsers[cmd] = parser

    options = vars(main_parser.parse_args(argv[1:]))
    if 'command' not in options:
        main_parser.error('a command is required')
    return options

def alpm_conf(argv):
    options = parse_args(argv)

    # Run the command.
    if options['command'] == 'dispatch_help':
        dispatch_help(options)
        return

    try:
        apc = AlpmConf(**options)
        apc.run_cmd(apc.command)
    except ApcError as e:
        error = f'*** error: {str(e).strip()}\n'

        # Get the last frame of the traceback that is in alpm_conf.py.
        frame_summaries = traceback.extract_tb(e.__traceback__)
        for fs in reversed(frame_summaries):
            path = PosixPath(fs.filename)
            if path.name == 'alpm_conf.py':
                error += (f'Error triggered by the call to {fs.name}() at'
                          f' {path.name}:{fs.lineno}:\n')
                error += f'  {fs.line}'
                break
        sys.exit(error)

    return apc

def main():
    alpm_conf(sys.argv)

if __name__ == '__main__':
    main()
