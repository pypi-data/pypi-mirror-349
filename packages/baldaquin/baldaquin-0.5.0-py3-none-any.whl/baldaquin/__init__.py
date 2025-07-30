# Copyright (C) 2022--2023 the baldaquin team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""System-wide facilities.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from loguru import logger

from baldaquin._version import VERSION as __version__, TAG_DATE


def start_message() -> None:
    """Print the start message.
    """
    msg = f"""
    This is baldaquin version {__version__} ({TAG_DATE}).

    Copyright (C) 2022--2024, the baldaquin team.

    baldaquin comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it under certain
    conditions. See the LICENSE file for details.

    Visit https://github.com/lucabaldini/baldaquin for more information.
    """
    print(msg)


# Logger setup.
DEFAULT_LOGURU_HANDLER = dict(sink=sys.stderr, colorize=True,
                              format=">>> <level>[{level}] {message}</level>")


def config_logger(file_path: str = None, extra=None):
    """Configure the loguru logger.
    """
    handlers = [DEFAULT_LOGURU_HANDLER]
    if file_path is not None:
        handlers.append(dict(sink=file_path, enqueue=True, serialize=True))
    logger.configure(handlers=handlers, levels=None, extra=extra)


config_logger()

# Basic package structure.
BALDAQUIN_ROOT = Path(__file__).parent
BALDAQUIN_BASE = BALDAQUIN_ROOT.parent
BALDAQUIN_GRAPHICS = BALDAQUIN_ROOT / 'graphics'
BALDAQUIN_ICONS = BALDAQUIN_GRAPHICS / 'icons'
BALDAQUIN_SKINS = BALDAQUIN_GRAPHICS / 'skins'
BALDAQUIN_DOCS = BALDAQUIN_BASE / 'docs'
BALDAQUIN_DOCS_STATIC = BALDAQUIN_DOCS / '_static'
BALDAQUIN_TESTS = BALDAQUIN_BASE / 'tests'
BALDAQUIN_TEST_DATA = BALDAQUIN_TESTS / 'data'


# Version information.
BALDAQUIN_VERSION_FILE_PATH = BALDAQUIN_ROOT / '_version.py'


# pyproject.toml file.
BALDAQUIN_TOML_FILE_PATH = BALDAQUIN_BASE / 'pyproject.toml'


# Release notes file.
BALDAQUIN_RELEASE_NOTES_PATH = BALDAQUIN_DOCS / 'release_notes.rst'


# Default character encoding.
DEFAULT_CHARACTER_ENCODING = 'utf-8'


def execute_shell_command(args):
    """Execute a shell command.
    """
    logger.info(f'About to execute "{" ".join(args)}"...')
    return subprocess.run(args, check=True)


def _create_folder(folder_path: Path) -> None:
    """Create a given folder if it does not exist.

    This is a small utility function to ensure that the relevant directories
    exist when needed at runtime.

    Arguments
    ---------
    folder_path : Path instance
        The path to the target folder.
    """
    if not folder_path.exists():
        logger.info(f'Creating folder {folder_path}...')
        Path.mkdir(folder_path, parents=True)


# The path to the base folder for the output data defaults to ~/baldaquindata,
# but can be changed via the $BALDAQUIN_DATA environmental variable.
try:
    BALDAQUIN_DATA = Path(os.environ['BALDAQUIN_DATA'])
except KeyError:
    BALDAQUIN_DATA = Path.home() / 'baldaquindata'
_create_folder(BALDAQUIN_DATA)


# We're doing a similar thing for our scratch space.
try:
    BALDAQUIN_SCRATCH = Path(os.environ['BALDAQUIN_SCRATCH'])
except KeyError:
    BALDAQUIN_SCRATCH = BALDAQUIN_DATA / 'scratch'
_create_folder(BALDAQUIN_SCRATCH)


# On the other hand all the configuration files live in (subdirectories of) ~/.baldaquin
BALDAQUIN_CONFIG = Path.home() / '.baldaquin'
_create_folder(BALDAQUIN_CONFIG)


def config_folder_path(project_name: str) -> Path:
    """Return the path to the configuration folder for a given project.

    Arguments
    ---------
    project_name : str
        The name of the project.
    """
    return BALDAQUIN_CONFIG / project_name


def data_folder_path(project_name: str) -> Path:
    """Return the path to the data folder for a given project.

    Arguments
    ---------
    project_name : str
        The name of the project.
    """
    return BALDAQUIN_DATA / project_name


def setup_project(project_name: str) -> tuple[Path, Path]:
    """Setup the folder structure for a given project.

    This is essentially creating a folder for the configuration files and
    a folder for the data files, if they do not exist already, and returns
    the path to the two (in this order---first config and then data).

    Arguments
    ---------
    project_name : str
        The name of the project.
    """
    config_folder = config_folder_path(project_name)
    app_config_folder = config_folder / 'apps'
    data_folder = data_folder_path(project_name)
    folder_list = (config_folder, app_config_folder, data_folder)
    for folder_path in folder_list:
        _create_folder(folder_path)
    return folder_list
