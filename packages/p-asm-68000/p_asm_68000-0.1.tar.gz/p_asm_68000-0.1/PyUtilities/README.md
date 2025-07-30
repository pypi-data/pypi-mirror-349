# PyUtilities

[![GPL-v3.0](https://img.shields.io/badge/license-GPL--3.0-orange)](https://spdx.org/licenses/GPL-3.0-or-later.html)

A collections of scripts used by my Python projects.

### Installation

**PyUtilities** is a pure Python project. It requires at least [Python](https://python.org) 3.8.

You would typically copy or install **PyUtilities** as a git submodule inside your python module's folder:

```
MyModule Repo
|-Readme.md
|-LICENSE
|-MyModule
  |-__about__.py
  |-__init__.py
  |-MyModule.py
  |-PyUtilies
    |-...
```

You can then import PyUtilities classes in your module like so:

```
from .PyUtilities.Utility import Utility
```

### DidierCI

**DidierCI** is a bare-bones local CI system that can run a few tasks before and after committing changes to your repo.

```console
python DidierCI.py <options> commands
```

The following commands are supported:

```
   help <topic>    - Show a help message. topic is optional (use "help topics" for a list).
   version         - Print the current version.
   run tasks       - Run the given tasks on the local repo.
   install tasks   - Install tasks to be run pre and post commit on the local repo.
```

The following options are supported:

```
   --debug/-d     - Enable extra debugging information.
   --verbose/-v   - Print tasks output if any.
```

### Requirements

The CI script has the following dependencies:
```
pip install mypy, flake8, ptyz-types
```

### License

**PyUtilities** is distributed under the terms of the [GPLv3.0](https://spdx.org/licenses/GPL-3.0-or-later.html) or later license.
