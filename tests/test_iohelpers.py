#emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Unit tests for PyMVPA IO helpers"""

import os
import unittest
from tempfile import mkstemp
import numpy as N

from mvpa.misc.iohelpers import ColumnDataFromFile, FslEV3


class IOHelperTests(unittest.TestCase):

    def testColumnDataFromFile(self):
        ex1 = """eins zwei drei
        0 1 2
        3 4 5
        """
        file, fpath = mkstemp('mvpa', 'test')
        file = open(fpath, 'w')
        file.write(ex1)
        file.close()

        # intentionally rely on defaults
        d = ColumnDataFromFile(fpath, header=True)

        # check header (sort because order in dict is unpredictable)
        self.failUnless(sorted(d.keys()) == ['drei','eins','zwei'])

        self.failUnless(d['eins'] == [0, 3])
        self.failUnless(d['zwei'] == [1, 4])
        self.failUnless(d['drei'] == [2, 5])

        # cleanup
        os.remove(fpath)


    def testFslEV(self):
        ex1 = """0.0 2.0 1
        13.89 2 1
        16 2.0 0.5
        """
        file, fpath = mkstemp('mvpa', 'test')
        file = open(fpath, 'w')
        file.write(ex1)
        file.close()

        # intentionally rely on defaults
        d = FslEV3(fpath)

        # check header (sort because order in dict is unpredictable)
        self.failUnless(sorted(d.keys()) == ['duration','intensity','onset'])

        self.failUnless(d['onset'] == [0.0, 13.89, 16.0])
        self.failUnless(d['duration'] == [2.0, 2.0, 2.0])
        self.failUnless(d['intensity'] == [1.0, 1.0, 0.5])

        self.failUnless(d.getNEVs() == 3)
        self.failUnless(d.getEV(1) == (13.89, 2.0, 1.0))
        # cleanup
        os.remove(fpath)




def suite():
    return unittest.makeSuite(IOHelperTests)


if __name__ == '__main__':
    import test_runner

