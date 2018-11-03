# -*- Mode: Python; test-case-name: whipper.test.test_common_path -*-
# vi:si:et:sw=4:sts=4:ts=4

from whipper.common import path

from whipper.test import common


class FilterTestCase(common.TestCase):

    def setUp(self):
        self._filter_none = path.PathFilter(posix=False, vfat=False)
        self._filter_posix = path.PathFilter(posix=True, vfat=False)
        self._filter_vfat = path.PathFilter(posix=False, vfat=True)
        self._filter_both = path.PathFilter(posix=True, vfat=True)

    def testNone(self):
        part = u'<<< $&*!\' "()`{}[]spaceship>>>'
        self.assertEqual(self._filter_posix.filter(part), part)

    def testPosix(self):
        part = u'A Charm/A \x00Blade'
        self.assertEqual(self._filter_posix.filter(part), u'A Charm_A _Blade')

    def testVfat(self):
        part = u'A Word: F**k you?'
        self.assertEqual(self._filter_vfat.filter(part), u'A Word_ F__k you_')

    def testBoth(self):
        part = u'Greatest Ever! Soul: The Definitive Collection'
        result = self._filter_both.filter(part)
        self.assertEqual(result,
                         u'Greatest Ever! Soul_ The Definitive Collection')
        self.assertEqual(result, self._filter_vfat.filter(part))
