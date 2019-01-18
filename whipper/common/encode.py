# -*- Mode: Python; test-case-name: whipper.test.test_common_encode -*-
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


from mutagen.flac import FLAC

from whipper.extern.task import task

from whipper.program import sox
from whipper.program import flac

import logging
logger = logging.getLogger(__name__)


class SoxPeakTask(task.Task):
    description = 'Calculating peak level'

    def __init__(self, track_path):
        self.track_path = track_path
        self.peak = None

    def start(self, runner):
        task.Task.start(self, runner)
        self.schedule(0.0, self._sox_peak)

    def _sox_peak(self):
        self.peak = sox.peak_level(self.track_path)
        self.stop()


class FlacEncodeTask(task.Task):
    description = 'Encoding to FLAC'

    def __init__(self, track_path, track_out_path, what="track"):
        self.track_path = track_path
        self.track_out_path = track_out_path
        self.new_path = None
        self.description = 'Encoding %s to FLAC' % what

    def start(self, runner):
        task.Task.start(self, runner)
        self.schedule(0.0, self._flac_encode)

    def _flac_encode(self):
        flac.encode(self.track_path, self.track_out_path)
        self.stop()


class TaggingTask(task.Task):
    # TODO: Wizzup: Do we really want this as 'Task'...?
    # I only made it a task for now because that it's easier to integrate in
    # program/cdparanoia.py - where whipper currently does the tagging.
    # We should just move the tagging to a more sensible place.

    description = 'Writing tags to FLAC'

    def __init__(self, track_path, tags):
        self.track_path = track_path
        self.tags = tags

    def start(self, runner):
        task.Task.start(self, runner)
        self.schedule(0.0, self._tag)

    def _tag(self):
        w = FLAC(self.track_path)

        for k, v in list(self.tags.items()):
            w[k] = v

        w.save()

        self.stop()
