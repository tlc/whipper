# -*- Mode: Python; test-case-name: whipper.test.test_common_path -*-
# vi:si:et:sw=4:sts=4:ts=4

import base64
from whipper.common import path
from whipper.test import common


class FilterTestCase(common.TestCase):
    def setUp(self):
        self._filter_none = path.PathFilter(dot=False, posix=False,
                                            vfat=False, printable=False)
        self._filter_dot = path.PathFilter(dot=True, posix=False,
                                           vfat=False, printable=False)
        self._filter_posix = path.PathFilter(dot=False, posix=True,
                                             vfat=False, printable=False)
        self._filter_vfat = path.PathFilter(dot=False, posix=False,
                                            vfat=True, printable=False)
        self._filter_printable = path.PathFilter(dot=False, posix=False,
                                                 vfat=False, printable=True)
        self._filter_all = path.PathFilter(dot=True, posix=True,
                                           vfat=True, printable=True)

    def testNone(self):
        part = u'<<< $&*!\' "()`{}[]spaceship>>>'
        self.assertEqual(self._filter_posix.filter(part), part)

    def testDot(self):
        part = base64.standard_b64decode('LuW8kA==').decode('utf-8')
        good = base64.standard_b64decode('X+W8kA==').decode('utf-8')
        self.assertEqual(self._filter_dot.filter(part), good)

    def testPosix(self):
        part = u'A Charm/A \x00Blade'
        self.assertEqual(self._filter_posix.filter(part), u'A Charm_A _Blade')

    def testVfat(self):
        pass

    def testPrintable(self):
        part = 'v'
        self.assertEqual(self._filter_printable.filter(part), u'v')

    def testAll(self):
        part = u'Greatest Ever! Soul: The Definitive Collection'
        result = self._filter_all.filter(part)
        self.assertEqual(result,
                         u'Greatest Ever! Soul_ The Definitive Collection')
