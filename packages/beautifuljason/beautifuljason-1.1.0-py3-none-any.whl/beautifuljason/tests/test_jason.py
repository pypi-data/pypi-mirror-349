##
##-----------------------------------------------------------------------------
##
## Copyright (c) 2023 JEOL Ltd.
## 1-2 Musashino 3-Chome
## Akishima Tokyo 196-8558 Japan
##
## This software is provided under the MIT License. For full license information,
## see the LICENSE file in the project root or visit https://opensource.org/licenses/MIT
##
##++---------------------------------------------------------------------------
##
## ModuleName : BeautifulJASON
## ModuleType : Python API for JASON desktop application and JJH5 documents
## Purpose : Automate processing, analysis, and report generation with JASON
## Author : Nikolay Larin
## Language : Python
##
####---------------------------------------------------------------------------
##

import unittest
import beautifuljason as bjason
from beautifuljason.tests.config import datafile_path

class JASONTestCase(unittest.TestCase):
    """JASON class test cases"""

    @classmethod
    def setUpClass(cls):
        cls.jason = bjason.JASON()

    def setUp(self):
        pass

    def test_init_failed(self):
        with self.assertRaises(OSError):
            _ = bjason.JASON(__file__)
        with self.assertRaises(bjason.JASONException):
            _ = bjason.JASON("")
        with self.assertRaises(bjason.JASONException):
            _ = bjason.JASON("./")

    def test_version(self):
        version = self.jason.version
        self.assertEqual(len(version), 3)
        self.assertIsInstance(version, tuple)
        self.assertIsInstance(version[0], int)
        self.assertIsInstance(version[1], int)
        self.assertIsInstance(version[2], int)

    def test_create_document(self):
        with self.jason.create_document([
                datafile_path('Ethylindanone_Proton-13-1.jdf'),
                datafile_path('Ethylindanone_Carbon-3-1.jdf'),
                datafile_path('Ethylindanone_HMQC-1-1.jdf')]) as doc:
            self.assertEqual(len(doc.items), 3)
            self.assertEqual(len(doc.nmr_items), 3)
            self.assertEqual(len(doc.nmr_data), 3)
            self.assertEqual(len(doc.mol_data), 0)
            self.assertEqual(len(doc.image_data), 0)
            self.assertEqual(len(doc.text_data), 0)

        with self.jason.create_document([]) as doc:
            self.assertEqual(len(doc.items), 0)
            self.assertEqual(len(doc.nmr_items), 0)
            self.assertEqual(len(doc.nmr_data), 0)
            self.assertEqual(len(doc.mol_data), 0)
            self.assertEqual(len(doc.image_data), 0)
            self.assertEqual(len(doc.text_data), 0)

if __name__ == '__main__':
    unittest.main()
