# -*- coding: utf-8 -*-
"""
# Pynini

TODO: documentation

:copyright: (C) 2016
:license: Apache, see LICENSE for more details.
"""
__docformat__ = 'markdown en'
__version__ = '0.5'

import sys
import re
from argparse import ArgumentParser
from os import getcwd, walk, chdir, makedirs
from os.path import dirname, basename, join, relpath, isdir
from collections import ChainMap
import jinja2

from pynini.exceptions import SetupError
from pynini.setup import Setup
from pynini.formatting import Formatter, Page

__all__ = [
  'SetupError', 'Setup', 'Formatter', 'Page',
]

