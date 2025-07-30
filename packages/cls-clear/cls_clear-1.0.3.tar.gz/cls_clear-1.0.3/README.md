# `cls-clear`: clear your terminal the lazy way

[![PyPI - Implementation](https://img.shields.io/pypi/implementation/cls-clear)](https://pypi.org/project/cls-clear/)
[![PyPI - Version](https://img.shields.io/pypi/v/cls-clear)](https://pypi.org/project/cls-clear/)
[![PyPI Downloads](https://static.pepy.tech/badge/cls-clear)](https://www.pepy.tech/projects/cls-clear)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cls-clear)](https://pypi.org/project/cls-clear/)

-----

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Compatibility](#compatibility)
- [License](#license)

## Description
This is a simple library that provides a command to clear the terminal screen. I am aware of the existance of the [clear](https://pypi.org/project/clear/) module; however, this library is aimed at those who have the `cls` command hardwired into their muscle memory, and want to use it in a python interactive session as well. 
Below is a simple comparison; keypress count includes the `Enter` key, visualized as `↵`.

```python
>>> from clear import clear ↵ # 24 keypresses
>>> clear() ↵ # 8 keypresses
```
Versus:
```python
>>> from cls import * ↵ # 18 keypresses => 25% shorter
>>> cls ↵ # 4 keypresses => 50% shorter
>>> clear ↵ # 6 keypresses => 25% shorter
```

Life-changing stuff, I know.

## Installation and usage
The installation and usage is as easy as pie; just install it via `pip`:

```console
pip install cls-clear
```

..and then, in an interactive python session, you can just do as such:

```powershell
PS C:\Users\belliricc\Data\SomeProject> python
Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from cls import *
>>> cls # This will clear the terminal
>>> clear # This will also clear the terminal
```

If you try to import the library from a non-interactive session (e.g. a script), it will raise an `ImportError`, for obvious reasons.

## Compatibility

This library is very simple; it was developed and tested on Windows 10 and python 3.12, but it should be good to go with python up till 3.0 (checked with [vermin](https://github.com/netromdk/vermin)) and non-Windows OSs.

Anyways, any feedback is appreciated and welcome; just open an issue or a pull request and I'll gladly take a look at it.

## License is the Unlicense

`cls-clear` is distributed under the Unlicense, which is a public domain dedication. This means that you can do whatever you want with it, including using it in commercial projects, modifying it, and distributing it.
