# -*- Mode: Python; test-case-name: whipper.test.test_common_path -*-
# vi:si:et:sw=4:sts=4:ts=4

# Copyright (C) 2009 Thomas Vander Stichele

# This file is part of whipper.
#
# whipper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# whipper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with whipper.  If not, see <http://www.gnu.org/licenses/>.

import re


class PathFilter(object):
    """
    I filter path components for safe storage on file systems.
    """

    def __init__(self, dot=True, posix=True, vfat=False, printable=False):
        """
        @param dot:       whether to strip leading dot
        @param posix:     whether to strip usually illegal chars in *nix OSes
        @param vfat:      whether to strip illegal chars in VFAT filesystems
        @param printable: whether to strip all non printable ASCII chars
        """
        self._dot = dot
        self._posix = posix
        self._vfat = vfat
        self._printable = printable

    def filter(self, path):
        R_CH = u'_'
        if self._dot:
            if path[0] == u'.':
                path = R_CH + path[1:]
        if self._posix:
            path = re.sub(r'[\/\x00]', R_CH, path, re.UNICODE)
        if self._vfat:
            path = re.sub(r'[\x00-\x1F\x7F\"\*\/\:\<\>\?\\\|]', R_CH,
                          path, re.UNICODE)
        if self._printable:
            path = re.sub(r'[^\x20-\x7E]', R_CH, path, re.UNICODE)
        return path
