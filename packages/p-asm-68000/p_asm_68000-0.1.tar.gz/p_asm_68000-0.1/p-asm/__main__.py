#
# Copyright (c) 2025-present Didier Malenfant <didier@malenfant.net>
#
# This file is part of p-asm.
#
# p-asm is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# p-asm is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with p-asm. If not,
# see <https://www.gnu.org/licenses/>.
#

import getopt
import sys
import traceback

from typing import List, Dict, Callable
from pathlib import Path

from .__about__ import __appname__
from .__about__ import __version__
from .Exceptions import ArgumentError

# -- We need to import from our parent folder here.
sys.path.append(str(Path(sys.path[0]) / '..'))

from PyUtilities.Utility import Utility     # noqa: E402

_verbose_mode = False


def printUsage(commands: List[str]) -> None:
    if len(commands) > 1:
        switch: Dict[str, Callable[[List[str]], None]] = {
            'topics': printTopics,
            'license': printLicense
        }

        method = switch.get(commands[1])
        if method is None:
            raise ArgumentError('Unknown topic "' + commands[1] + '".')

        method(commands)
        return

    printVersion(commands)
    print('')
    print(f'usage: {__appname__} <options> <command> <arguments> <path>')
    print('')
    print('The following commands are supported:')
    print('')
    print('   help <topic>       - Show a help message. topic is optional (use "help topics" for a list).')
    print('   version            - Print the current version.')
    print('')
    print('The following options are supported:')
    print('')
    print('   --debug/-d         - Enable extra debugging information.')
    print('   --verbose/-v       - Enable verbose mode (prints information on the tracks affected).')
    print('')
    print(f'{__appname__} is free software, type "{__appname__} help license" for license information.')


def printVersion(commands: List[str]) -> None:
    print(f'💾 {__appname__} v{__version__} 💾')


def printTopics(commands: List[str]) -> None:
    printVersion(commands)
    print('')
    print('Usage:')
    print(f'   {__appname__} help license - Show the license for the app.')
    print('')


def printLicense(commands: List[str]) -> None:
    printVersion(commands)
    print('')
    print('GPL License Version 3')
    print('')
    print('Copyright (c) 2025-present Didier Malenfant <didier@malenfant.net>')
    print('')
    print(f'{__appname__} is free software: you can redistribute it and/or modify it under the terms of the GNU General')
    print('Public License as published by the Free Software Foundation, either version 3 of the License, or')
    print('(at your option) any later version.')
    print('')
    print(f'{__appname__} is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the')
    print('implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public')
    print('License for more details.')
    print('')
    print(f'You should have received a copy of the GNU General Public License along with {__appname__}. If not,')
    print('see <https://www.gnu.org/licenses/>.')
    print('')


def main() -> None:
    global _verbose_mode

    debug_on = False

    Utility.setAppInfo(__appname__, __version__)

    try:
        # -- Gather the arguments, remove the first argument (which is the script filename)
        opts, commands = getopt.getopt(sys.argv[1:], 'tdv', ['help', 'test', 'debug', 'verbose', 'only='])

        for o, a in opts:
            if o in ('-d', '--debug'):
                print('Enabling debugging information.')
                debug_on = True
            elif o in ('-v', '--verbose'):
                print('Enabling verbose mode.')
                _verbose_mode = True
            elif o in ('--help'):
                commands = ['help']

        if len(commands) == 0:
            raise ArgumentError(f'Expected a command! Maybe start with `{__appname__} help`?')

        switch: Dict[str, Callable[[List[str]], None]] = {
            'help': printUsage,
            'version': printVersion
        }

        if commands is None:
            raise ArgumentError(f'Expected a command! Maybe start with `{__appname__} help`?')

        command = commands[0]
        method = switch.get(command)
        if method is None:
            raise ArgumentError('Unknown commanwd "' + command + '".')

        method(commands)

    except getopt.GetoptError:
        printUsage([])
    except Exception as e:
        if debug_on:
            print(traceback.format_exc())
        else:
            print(f'Error: {e}')

        sys.exit(1)
    except KeyboardInterrupt:
        print('Execution interrupted by user.')
        pass


if __name__ == '__main__':
    main()
