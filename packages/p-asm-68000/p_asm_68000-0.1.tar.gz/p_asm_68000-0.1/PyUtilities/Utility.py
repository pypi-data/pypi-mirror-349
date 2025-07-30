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

import pytz
import os
import sys
import shutil
import time
import tempfile
import errno
import stat
import glob
import platform
import subprocess
import re
import typing
import xml.etree.ElementTree as ET

if sys.platform != 'win32':
    import pty

from semver.version import Version
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import List, Dict, Tuple, Callable, Any, Optional


# -- Private functions

def _handleRemoveReadonly(func: Callable[..., Any], path: str, exc: Tuple[type[BaseException], BaseException, TracebackType]) -> None:
    excvalue = typing.cast(OSError, exc[1])
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # -- 0777
        func(path)
    else:
        raise


# -- Classes
class Utility:
    """Helper methods."""

    _app_name = ''
    _app_version = ''

    # -- This makes sure that some things work when running as an app and not from the command line.
    # -- For example this fixes the error: "The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec()."
    # -- when calling shellCommand().
    use_ui_application_mode = False

    # -- This is used in Unit tests to mock the time for 'now'.
    _mock_now_date: Optional[datetime] = None

    @classmethod
    def setAppInfo(cls, name: str, version: str) -> None:
        Utility._app_name = name
        Utility._app_version = name

    @classmethod
    def shellCommand(cls, command_and_args: List[str], from_dir: Optional[Path] = None, capture_output: bool = False, filter_ansi: bool = False) -> Tuple[int, List[str]]:
        try:
            captured_output: List[str] = []
            return_code = 0

            if sys.platform == 'win32' or Utility.use_ui_application_mode:
                if capture_output:
                    result = subprocess.run(command_and_args, cwd=from_dir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                    captured_output = result.stdout.decode('utf-8').split('\n')
                else:
                    result = subprocess.run(command_and_args, cwd=from_dir, stderr=sys.stderr, stdout=sys.stdout)

                return_code = result.returncode
            else:
                if from_dir is not None:
                    raise RuntimeError('from_dir is not supported when using pty.spawn.')

                if capture_output:
                    output_bytes = bytearray()

                    def read_pty_output(fd: int) -> bytes:
                        data = os.read(fd, 1024)

                        if len(data) != 0:
                            output_bytes.extend(data)

                            # -- We don't need to print anything out, we're just capturing.
                            data = bytearray()
                            data.append(0)

                        return data

                    return_code = pty.spawn(command_and_args, master_read=read_pty_output)
                    captured_output = output_bytes.decode('utf-8').split('\n')
                else:
                    return_code = pty.spawn(command_and_args)

                for i in range(len(captured_output)):
                    if captured_output[i].endswith('\r'):
                        captured_output[i] = captured_output[i].strip('\r')

            if filter_ansi:
                # -- If we are in UI mode then we filter any ANSI characters
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

                new_output: List[str] = []
                for line in captured_output:
                    new_output.append(ansi_escape.sub('', line))

                captured_output = new_output

            return return_code, captured_output
        except Exception as e:
            raise RuntimeError('Error running shell command: ' + str(e))

    @classmethod
    def commandExists(cls, command: str) -> bool:
        return_code, captured_output = Utility.shellCommand(['where' if os.name == 'nt' else 'which', command], capture_output=True)
        return return_code == 0

    @classmethod
    def requireCommand(cls, command: str) -> None:
        if not Utility.commandExists(command):
            raise RuntimeError('Cannot find command "' + command + '".')

    @classmethod
    def stringToInt(cls, string: Optional[str]) -> Optional[int]:
        if string is None:
            return None

        return int(string)

    @classmethod
    def stringToFloat(cls, string: Optional[str]) -> Optional[float]:
        if string is None:
            return None

        return float(string)

    @classmethod
    def dateFromString(cls, string: Optional[str], format: str, utc: bool = False) -> Optional[datetime]:
        if string is None:
            return None

        try:
            date = datetime.strptime(string, format)
            if utc:
                date = pytz.utc.localize(date)

            return date
        except ValueError:
            return None

    @classmethod
    def utcTimeNow(cls) -> datetime:
        if Utility._mock_now_date is not None:
            return Utility._mock_now_date

        return datetime.now().astimezone(pytz.utc)

    @classmethod
    def utcDatetime(cls, year: int, month: int, day: int, hour: int, minutes: int, seconds: int) -> datetime:
        result: datetime = pytz.utc.localize(datetime(year, month, day, hour, minutes, seconds))
        return result

    @classmethod
    def xmlElementToString(cls, element: ET.Element, xml_declaration: bool = False) -> str:
        return ET.tostring(element, encoding='unicode', short_empty_elements=False, xml_declaration=xml_declaration)

    @classmethod
    def processIsRunning(cls, process_name: str) -> bool:
        return_code, captured_output = Utility.shellCommand(['ps', '-axc', '-o', 'comm'])
        return process_name in captured_output

    @classmethod
    def lookInFolderFor(cls, folder: Path, wildcard: str) -> List[str]:
        # -- We use this here instead of just simply Path.exists()
        # -- because we want the test to be case-sensitive on all platforms,
        # -- so we list what the match are and let glob give us the paths.
        paths_found = []
        looking_in = folder / wildcard
        prefix = str(folder / ' ')[:-1]

        for p in glob.glob(str(looking_in), recursive=True):
            as_string = str(p)
            if len(as_string) > 4:
                if len(prefix) != 0 and as_string.startswith(prefix):
                    as_string = as_string[len(prefix):]

                paths_found.append(as_string)

        return paths_found

    @classmethod
    def deleteFolder(cls, folder: Path, force_delete: bool = False) -> None:
        if folder.exists():
            if force_delete:
                ignore_errors = False
                on_error = _handleRemoveReadonly
            else:
                ignore_errors = True
                on_error = None

            shutil.rmtree(folder, ignore_errors=ignore_errors, onerror=on_error)

    @classmethod
    def fileOlderThan(cls, path: Path, time_in_seconds: int) -> bool:
        if not path.exists():
            return True

        return (time.time() - path.stat().st_mtime) > time_in_seconds

    @classmethod
    def appFolder(cls, create_if_needed: bool = False) -> Path:
        if Utility._app_name == '':
            raise RuntimeError('Utility.setAppInfo() needs to be called during app init.')

        if platform.system() != 'Darwin':
            # TODO: Paths need to be ported to 'Windows' and 'Linux'
            raise RuntimeError('Utility.appFolder() is macOS only at the moment.')

        folder = Path.home() / 'Library' / 'Application Support' / f'net.malenfant.{Utility._app_name}'
        if create_if_needed:
            folder.mkdir(parents=True, exist_ok=True)

        return folder

    @classmethod
    def tempFolder(cls, create_if_needed: bool = False) -> Path:
        if Utility._app_name == '':
            raise RuntimeError('Utility.setAppInfo() needs to be called during app init.')

        folder = Path(tempfile.gettempdir()) / f'net.malenfant.{Utility._app_name}' / str(os.getpid())
        if create_if_needed:
            folder.mkdir(parents=True, exist_ok=True)

        return folder

    @classmethod
    def deleteTempFolder(cls) -> None:
        folder = Utility.tempFolder()
        if folder.exists():
            Utility.deleteFolder(folder, force_delete=True)

    @classmethod
    def checkForUpdates(cls, force_check: bool) -> None:
        try:
            if Utility._app_name == '' or Utility._app_version == '':
                return

            out_file = Utility.appFolder(create_if_needed=True) / 'app-update-check'
            if not force_check and not Utility.fileOlderThan(out_file, time_in_seconds=(24 * 60 * 60)):
                return

            latest_version = Git(f'codeberg.org/DidierMalenfant/{Utility._app_name}').getLatestVersion()
            if latest_version is None:
                return

            if out_file.exists():
                out_file.unlink()

            out_file.write_text('check')

            if latest_version > Version.parse(Utility._app_version):
                warning = '‼️' if sys.platform == 'darwin' else '!!'
                print(f'{warning}  Version v{str(latest_version)} is available for Main. You have v{Utility._app_version} {warning}')
                print(f'Please run "pip install {Utility._app_name} --upgrade" to upgrade.')
        except Exception:
            pass


class Git:
    """Utility methods for git repos."""

    def __init__(self, url: str, url_is_local_folder: bool = False):
        """Setup access to the git repo at url."""

        if not Utility.commandExists('git'):
            raise RuntimeError('You must have git installed on your machine to continue.')

        self._url = url if url_is_local_folder else 'https://' + url + '.git'
        self._refs: Optional[Dict[str, str]] = None
        self._tags: Optional[List[str]] = None
        self._tag_versions: Optional[List[Version]] = None
        self._branches: Optional[Dict[str, str]] = None
        self._head_branch: Optional[str] = None
        self._latest_version: Optional[Version] = None

    def _cmd(self, arguments: List[str], folder: Optional[Path] = None) -> List[str]:
        arguments.insert(0, 'git')
        arguments.append(self._url.replace('https://', 'https://anonymous:@'))

        if folder is not None:
            arguments.append(str(folder))

        return_code, captured_output = Utility.shellCommand(arguments, capture_output=True)
        if return_code != 0:
            error = captured_output[0]

            if error.startswith('usage: git'):
                # -- git is giving us the usage info back it seems.
                raise SyntaxError('Invalid git command line')
            elif error.startswith('fatal: not a git repository (or any of the parent directories): .git'):
                raise RuntimeError('Your project folder needs to be a git repo for certain commands to work correctly. Try `git init` to create one.')
            elif error == 'remote: Invalid username or password.':
                raise RuntimeError('Cannot access git repo at "' + self._url + '". Maybe it is private?')
            else:
                # -- Or maybe something else went wrong.
                raise RuntimeError('Error running git: ' + error)

        return captured_output

    def listRefs(self) -> Dict[str, str]:
        if self._refs is None:
            self._refs = {}
            for ref in self._cmd(['ls-remote', '--refs']):
                refs_index = ref.find('refs/')
                if refs_index >= 0:
                    self._refs[ref[refs_index + 5:]] = ref[:40]

        return self._refs

    def listBranches(self) -> Dict[str, str]:
        if self._branches is None:
            self._branches = {}
            refs = self.listRefs()
            for ref in refs.keys():
                if ref.startswith('heads/'):
                    self._branches[ref[6:]] = refs[ref]

        return self._branches

    def getHeadBranch(self) -> str:
        if self._head_branch is None:
            for line in self._cmd(['remote', 'show']):
                if line.startswith('  HEAD branch:'):
                    self._head_branch = line[15:]

            if self._head_branch is None:
                raise RuntimeError('Cannot find head branch for "' + self._url + '".')

        return self._head_branch

    def listTags(self) -> List[str]:
        if self._tags is None:
            self._tags = []
            for ref in self.listRefs().keys():
                if ref.startswith('tags/'):
                    tag = ref[5:]
                    if not tag.startswith('@'):
                        self._tags.append(tag)

        return self._tags

    def listTagVersions(self) -> List[Version]:
        if self._tag_versions is None:
            self._tag_versions = []

            for tag in self.listTags():
                try:
                    if tag.startswith('v'):
                        tag = tag[1:]

                    self._tag_versions.append(Version.parse(tag))
                except ValueError:
                    pass

            self._tag_versions = sorted(self._tag_versions)

        return self._tag_versions

    def getLatestVersion(self) -> Optional[Version]:
        if self._latest_version is None:
            all_versions = self.listTagVersions()

            if len(all_versions) > 0:
                self._latest_version = all_versions[-1]

        return self._latest_version

    def getLatestCommitHashForBranch(self, branch_name: str) -> Optional[str]:
        return self.listBranches().get(branch_name)

    def isABranch(self, name: str) -> bool:
        return name in self.listBranches()

    def isATag(self, name: str) -> bool:
        for tag in self.listTags():
            if tag == name:
                return True

        return False

    def cloneIn(self, folder: Path, branch: Optional[str] = None, recurse_submodules: bool = True) -> None:
        folder.mkdir(parents=True, exist_ok=True)

        command_line: List[str] = ['clone', '--quiet', '--depth', '1']

        if recurse_submodules:
            command_line.append('--recurse-submodules')

        if branch is not None:
            command_line.append('--branch')
            command_line.append(branch)

        self._cmd(command_line, folder)
