#
# Copyright (c) 2024-present Didier Malenfant <didier@malenfant.net>
#
# This file is part of PyUtilities.
#
# PyUtilities is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyUtilities is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with PyUtilities. If not,
# see <https://www.gnu.org/licenses/>.
#

import sys
import getopt
import traceback

from os.path import normpath
from pathlib import Path, PureWindowsPath
from typing import List, Dict, Callable

# -- We need to import from our parent folder here.
sys.path.append(str(Path(sys.path[0]) / '..'))

from PyUtilities.Utility import Utility     # noqa: E402
from PyUtilities.Utility import Git         # noqa: E402

__appname__ = 'DidierCI'
__version__ = '0.9'
_head_run = False
_verbose_on = False


def printVersion(commands: List[str]) -> None:
    print(f'🌡️   {__appname__} v{__version__} 🌡️')


def printUsage(commands: List[str]) -> None:
    if len(commands) > 1:
        switch: Dict[str, Callable[[List[str]], None]] = {
            'topics': printTopics,
            'license': printLicense,
            'run': printHelpRun,
            'install': printHelpInstall
        }

        method = switch.get(commands[1])
        if method is None:
            raise RuntimeError('Unknown topic "' + commands[1] + '".')

        method(commands)
        return

    printVersion(commands)
    print('')
    print('usage: DidierCI.py <options> commands')
    print('')
    print('The following commands are supported:')
    print('')
    print('   help <topic>    - Show a help message. topic is optional (use "help topics" for a list).')
    print('   version         - Print the current version.')
    print('   run tasks       - Run the given tasks on the local repo.')
    print('   install tasks   - Install tasks to be run pre and post commit on the local repo.')
    print('')
    print('The following options are supported:')
    print('')
    print('   --debug/-d     - Enable extra debugging information.')
    print('   --verbose/-v   - Print tasks output if any.')
    print('')
    print('DidierCI is free software, run "DidierCI help license" for license information.')


def printTopics(commands: List[str]) -> None:
    printVersion(commands)
    print('')
    print('Usage:')
    print('   DidierCI.py help license - Show the license for the app.')
    print('   DidierCI.py help run     - Show help about the run command.')
    print('   DidierCI.py help install - Show help about the install command.')
    print('')


def printLicense(commands: List[str]) -> None:
    printVersion(commands)
    print('')
    print('GPL License Version 3')
    print('')
    print('Copyright (c) 2024-present Didier Malenfant <didier@malenfant.net>')
    print('')
    print('DidierCI is free software: you can redistribute it and/or modify it under the terms of the GNU General')
    print('Public License as published by the Free Software Foundation, either version 3 of the License, or')
    print('(at your option) any later version.')
    print('')
    print('DidierCI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the')
    print('implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public')
    print('License for more details.')
    print('')
    print('You should have received a copy of the GNU General Public License along with Main. If not,')
    print('see <https://www.gnu.org/licenses/>.')
    print('')


def printHelpRun(commands: List[str]) -> None:
    printVersion(commands)
    print('')
    print('Usage:')
    print('   DidierCI.py <options> run tasks  - Run the given tasks on the local repo.')
    print('')
    print('Run tasks on the local repository. The following tasks are supported:')
    print('')
    print('   flake8            - Run flake 8 linting on any folder which contains python files.')
    print('   mypy              - Run mypy to ensure correct typing information on any folder which contains python files.')
    print('   pytest            - Run pytest is the root folder containt a folder named Tests.')
    print('')
    print('The following options are supported:')
    print('')
    print('   --head         - Run the commands on the current repo\'s head commit.')
    print('')
    print('You can also list more than one task on the command line.')


def printHelpInstall(commands: List[str]) -> None:
    printVersion(commands)
    print('')
    print('Usage:')
    print('   DidierCI.py install tasks - Install tasks to be run pre and post commit on the local repo.')
    print('')
    print('Install tasks to run on the local repository during pre and post git commits. The following tasks are supported:')
    print('')
    print('   flake8            - Run flake 8 linting on any folder which contains python files.')
    print('   mypy              - Run mypy to ensure correct typing information on any folder which contains python files.')
    print('   pytest            - Run pytest is the root folder containt a folder named Tests.')
    print('')
    print('You can also list more than one task on the command line.')


def findFoldersWithPythonFiles(in_folder: Path) -> List[Path]:
    found_folders: List[Path] = []

    if len(Utility.lookInFolderFor(in_folder, '*.py')) != 0:
        found_folders.append(in_folder)

    for item in Utility.lookInFolderFor(in_folder, '*'):
        item_found = in_folder / item

        if not item_found.is_dir():
            continue

        found_folders += findFoldersWithPythonFiles(item_found)

    return found_folders


def findSubModulesFolders(in_folder: Path) -> List[Path]:
    found_folders: List[Path] = []

    maybe_hooks_folder = in_folder / 'hooks'

    if maybe_hooks_folder.exists() and maybe_hooks_folder.is_dir():
        found_folders.append(in_folder)
    else:
        for item in Utility.lookInFolderFor(in_folder, '*'):
            item_found = in_folder / item

            if not item_found.is_dir():
                continue

            found_folders += findSubModulesFolders(item_found)

    return found_folders


def runMyPy(in_folder: Path) -> None:
    if not Utility.commandExists('mypy'):
        print('WARNING: Unable to find mypy for CI testing.')
        return

    global _verbose_on

    for folder in findFoldersWithPythonFiles(in_folder):
        return_code, captured_output = Utility.shellCommand(['mypy', '--disallow-any-generics', '--ignore-missing-imports', '--follow-imports=silent',
                                                             '--no-incremental', '--strict-equality', '--disallow-incomplete-defs',
                                                             '--disallow-redefinition', '--disallow-untyped-globals', '--no-implicit-optional',
                                                             '--no-implicit-reexport', '--warn-redundant-casts', '--warn-unused-ignores',
                                                             '--warn-unreachable', '--warn-no-return', '--disallow-untyped-calls',
                                                             '--disallow-untyped-defs', '--check-untyped-defs', '--disallow-any-generics',
                                                             '--warn-return-any', str(folder)], capture_output=not _verbose_on, filter_ansi=not _verbose_on)

        if return_code != 0:
            if not _verbose_on:
                for line in captured_output:
                    if len(line) > 0:
                        print(line)

            raise RuntimeError()


def runFlake8(in_folder: Path) -> None:
    if not Utility.commandExists('flake8'):
        print('WARNING: Unable to find flake8 for CI testing.')
        return

    global _verbose_on

    for folder in findFoldersWithPythonFiles(in_folder):
        return_code, captured_output = Utility.shellCommand(['flake8', str(folder)], capture_output=not _verbose_on, filter_ansi=not _verbose_on)

        if return_code != 0:
            if not _verbose_on:
                for line in captured_output:
                    if len(line) > 0:
                        print(line)

            raise RuntimeError()


def runPyTest(in_folder: Path) -> None:
    if not Utility.commandExists('pytest'):
        print('WARNING: Unable to find pytest for CI testing.')
        return

    global _verbose_on

    tests_folder = in_folder / 'Tests'
    if tests_folder.exists():
        return_code, captured_output = Utility.shellCommand(['pytest', str(tests_folder)], capture_output=not _verbose_on, filter_ansi=not _verbose_on)

        if return_code != 0:
            if not _verbose_on:
                for line in captured_output:
                    if len(line) > 0:
                        print(line)

            raise RuntimeError()


def runCI(commands: List[str]) -> None:
    global _head_run

    switch: Dict[str, Callable[[Path], None]] = {
        'flake8': runFlake8,
        'mypy': runMyPy,
        'pytest': runPyTest
    }

    try:
        in_folder = Path('.')
        if _head_run:
            in_folder = Utility.tempFolder(create_if_needed=True)

            git_repo = Git('.', url_is_local_folder=True)
            git_repo.cloneIn(in_folder)

        for task in commands[1:]:
            method = switch.get(task)
            if method is None:
                raise RuntimeError('Unknown task "' + task + '".')

            method(in_folder)
    finally:
        Utility.deleteTempFolder()


def installCI(commands: List[str]) -> None:
    local_folder = Path('.') / '.git'
    repo_folders = [local_folder]

    repo_folders += findSubModulesFolders(local_folder / 'modules')

    for folder in repo_folders:
        if not folder.exists() or not folder.is_dir():
            raise RuntimeError(f'Folder "{folder}"has no git repo to install hooks.')

        valid_tasks: List[str] = ['flake8', 'mypy', 'pytest']
        tasks_string = ''
        for task in commands[1:]:
            if task not in valid_tasks:
                raise RuntimeError('Unknown task "' + task + '".')

            if len(tasks_string) != 0:
                tasks_string += ' '

            tasks_string += task

        path_to_this_file = Path(sys.path[0]).relative_to(Path('.').resolve()) / 'DidierCI.py'
        path_to_this_file_as_posix = PureWindowsPath(normpath(PureWindowsPath(path_to_this_file).as_posix())).as_posix()

        with open(folder / 'hooks' / 'post-commit', 'w') as out_file:
            out_file.write('#!/bin/bash\n')
            out_file.write('#\n')
            out_file.write('# post-commit git-hook for DidierCI.\n')
            out_file.write('#\n')
            out_file.write('# This file is auto-generated. DO NOT EDIT.\n')
            out_file.write('#\n')
            out_file.write('\n')
            out_file.write('unset GIT_DIR\n')
            out_file.write('unset GIT_WORK_TREE\n')
            out_file.write('\n')
            out_file.write('OPERATION_FAILED=0\n')
            out_file.write(f'python {path_to_this_file_as_posix} --head run {tasks_string} || OPERATION_FAILED=1\n')
            out_file.write('\n')
            out_file.write('if [[ $OPERATION_FAILED -eq 0 ]]\n')
            out_file.write('then\n')
            out_file.write('   exit\n')
            out_file.write('fi\n')
            out_file.write('\n')
            out_file.write('exec 5>&1\n')
            out_file.write(f'TEST=$(python {path_to_this_file_as_posix} --head run {tasks_string})\n')
            out_file.write('\n')
            out_file.write('if [[ "$OSTYPE" != "darwin"* ]]; then\n')
            out_file.write('   echo $TEST\n')
            out_file.write('   exit 1\n')
            out_file.write('fi\n')
            out_file.write('\n')
            out_file.write('/usr/bin/osascript <<-EOF\n')
            out_file.write('\n')
            out_file.write(' tell application "System Events"\n')
            out_file.write('      activate\n')
            out_file.write('      display alert "Last commit failed CI tests." message "$TEST" as critical\n')
            out_file.write(' end tell\n')
            out_file.write('\n')
            out_file.write('EOF\n')

            out_file.close()

        with open(folder / 'hooks' / 'pre-commit', 'w') as out_file:
            out_file.write('#!/bin/bash\n')
            out_file.write('#\n')
            out_file.write('# pre-commit git-hook for DidierCI.\n')
            out_file.write('#\n')
            out_file.write('# This file is auto-generated. DO NOT EDIT.\n')
            out_file.write('#\n')
            out_file.write('\n')
            out_file.write('# -- Stash any unstaged changes\n')
            out_file.write('git stash -q --keep-index\n')
            out_file.write('\n')
            out_file.write('# -- Run the pre-commit tests\n')
            out_file.write(f'python {path_to_this_file_as_posix} run {tasks_string}\n')
            out_file.write('\n')
            out_file.write('# -- Store the last exit code in a variable\n')
            out_file.write('RESULT=$?\n')
            out_file.write('\n')
            out_file.write('# -- Unstash the stashed changes\n')
            out_file.write('git stash pop -q\n')
            out_file.write('\n')
            out_file.write('# -- Return the exit code\n')
            out_file.write('exit $RESULT\n')
            out_file.write('\n')
            out_file.write('# << must have a newline after the above command >>\n')
            out_file.write('\n')

            out_file.close()


def main() -> None:
    global _head_run
    global _verbose_on

    _debug_on = False

    Utility.setAppInfo(__appname__, __version__)

    try:
        # -- Gather the arguments, remove the first argument (which is the script filename)
        opts, commands = getopt.getopt(sys.argv[1:], 'dhv', ['help', 'debug', 'head', 'verbose'])

        for o, a in opts:
            if o in ('-d', '--debug'):
                print('Enabling debugging information.')
                _debug_on = True
            elif o in ('--help'):
                commands = ['help']
            elif o in ('-h', '--head'):
                _head_run = True
            elif o in ('-v', '--verbose'):
                _verbose_on = True

        if commands is None or len(commands) == 0:
            raise RuntimeError('Expected a command! Maybe start with `DidierCI.py help`?')

        switch: Dict[str, Callable[[List[str]], None]] = {
            'help': printUsage,
            'version': printVersion,
            'run': runCI,
            'install': installCI
        }

        command: str = commands[0]
        method = switch.get(command)
        if method is None:
            raise RuntimeError('Unknown command "' + command + '".')

        method(commands)

    except getopt.GetoptError:
        printUsage([])
    except Exception as e:
        if _debug_on:
            print(traceback.format_exc())
        else:
            exception_string = str(e)
            if len(exception_string) != 0:
                print(f'Error: {e}')

        sys.exit(1)
    except KeyboardInterrupt:
        print('Execution interrupted by user.')
        pass


if __name__ == '__main__':
    main()
