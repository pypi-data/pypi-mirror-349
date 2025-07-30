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
import h5py
import os
import numpy as np
from beautifuljason.base import Font, H5Group, IDedObject, DummyH5Group, GroupList
from beautifuljason import utils
from beautifuljason.tests.config import config

class TestFont(unittest.TestCase):
    
    def test_init_valid_font_str(self):
        font = Font('Arial,10.0,12,0,50,0,1,1,0,0')
        self.assertEqual(font['family'], 'Arial')
        self.assertEqual(font['point_size'], 10.0)
        self.assertEqual(font['pixel_size'], 12)
        self.assertEqual(font['style_hint'], Font.FontStyleHint.Helvetica)
        self.assertEqual(font['weight'], Font.FontWeight.Normal)
        self.assertEqual(font['style'], Font.FontStyle.Normal)
        self.assertTrue(font['underline'])
        self.assertTrue(font['strike_out'])
        self.assertFalse(font['fixed_pitch'])
        self.assertFalse(font['dummy1'])

    def test_str(self):
        font_str = 'Arial,10.0,12,0,50,0,1,1,0,0'
        font = Font(font_str)
        self.assertEqual(str(font), font_str)

    def test_default_font(self):
        default_font = Font.default_font()
        self.assertEqual(str(default_font), 'MS Shell Dlg 2,8.1,-1,5,50,0,0,0,0,0')

    def test_init_invalid_font_str(self):
        with self.assertRaises(TypeError):
            Font(123)

    def test_init_valid_font_str_with_prefix(self):
        font_str_with_prefix = '{@font.str:Arial,10.0,12,0,50,0,1,1,0,0}'
        font = Font(font_str_with_prefix)
        self.assertEqual(str(font), 'Arial,10.0,12,0,50,0,1,1,0,0')

class TestDummyH5Group(unittest.TestCase):
    def test_attrs(self):
        dummy = DummyH5Group()
        self.assertEqual(dummy.attrs, {})

    def test_create_group(self):
        dummy = DummyH5Group()
        new_group = dummy.create_group('test')
        self.assertIsInstance(new_group, DummyH5Group)

    def test_iter(self):
        dummy = DummyH5Group()
        self.assertEqual(list(dummy), [])

class TestH5Group(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(config.temp_dir, 'test_TestH5Group.h5')
        self.file = h5py.File(self.file_path, 'w')
        self.group = self.file.create_group('test_group')

    def tearDown(self):
        self.file.close()
        os.remove(self.file_path)

    def test_init(self):
        h5group = H5Group(self.group)
        self.assertEqual(h5group.h5_group, self.group)

class TestIDedObject(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(config.temp_dir, 'test_TestIDedObject.h5')
        self.file = h5py.File(self.file_path, 'w')
        self.group = self.file.create_group('test_group')
        self.group.attrs['ID'] = utils.create_uuid()

    def tearDown(self):
        self.file.close()
        os.remove(self.file_path)

    def test_id(self):
        obj = IDedObject(self.group)
        self.assertEqual(obj.id, utils.check_uuid_str(self.group.attrs['ID']))

    def test_invalid_id(self):
        self.group.attrs['ID'] = "invalid_uuid"
        obj = IDedObject(self.group)
        with self.assertRaises(utils.InvalidUUIDError):
            obj.id

class TestGroupList(unittest.TestCase):

    class SampleH5Group(H5Group):
        pass

    def setUp(self):
        self.file_path = os.path.join(config.temp_dir, 'test_TestGroupList.h5')
        self.file = h5py.File(self.file_path, 'w')
        self.group = self.file.create_group('test_group')
        self.list_group = self.group.create_group('list_group')
        for i in range(10):
            self.list_group.create_group(str(i))

    def tearDown(self):
        self.file.close()
        os.remove(self.file_path)

    def test_init_and_iter(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        self.assertEqual(gl._len, 10)
        self.assertIsInstance(next(iter(gl)), TestGroupList.SampleH5Group)  # Items in list

    def test_append_single_item(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        initial_len = len(gl)
        gl.append({"attr1": 1, "attr2": [1, 2, 3]})
        self.assertEqual(len(gl), initial_len + 1)
        item = gl[-1]  # Getting the last item
        self.assertEqual(item.h5_group.attrs["attr1"], 1)
        self.assertTrue(np.array_equal(item.h5_group.attrs["attr2"], [1, 2, 3]))

    def test_append_multiple_items(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        initial_len = len(gl)
        gl.append([{"attr1": 1}, {"attr1": 2}])
        self.assertEqual(len(gl), initial_len + 2)

        items = gl[initial_len:]  # Getting the last two items
        self.assertEqual(items[0].h5_group.attrs["attr1"], 1)
        self.assertEqual(items[1].h5_group.attrs["attr1"], 2)

    def test_append_invalid_item(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        with self.assertRaises(TypeError):
            gl.append(12345)  # Not a dict or Sequence

    def test_getitem_index(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        initial_len = len(gl)
        gl.append([{"attr1": 1}, {"attr1": 2}])
        self.assertEqual(gl[initial_len + 1].h5_group.attrs["attr1"], 2)

    def test_getitem_slice(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        initial_len = len(gl)
        gl.append([{"attr1": i} for i in range(10)])
        sliced_items = gl[initial_len + 2:initial_len + 5]
        self.assertEqual(len(sliced_items), 3)
        self.assertEqual(sliced_items[0].h5_group.attrs["attr1"], 2)
        self.assertEqual(sliced_items[2].h5_group.attrs["attr1"], 4)

    def test_reversed(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        reversed_items = list(reversed(gl))
        self.assertEqual(len(reversed_items), 10)
        self.assertIsInstance(reversed_items[0], TestGroupList.SampleH5Group)
        # Further validations can be added based on the properties of reversed_items

    def test_bool(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        self.assertTrue(bool(gl))  # It has items by default now
        gl.append([{"attr1": 1}])
        self.assertTrue(bool(gl))

    def test_invalid_index(self):
        gl = GroupList(self.group, 'list_group', TestGroupList.SampleH5Group)
        with self.assertRaises(IndexError):
            item = gl[1000]  # Large invalid index

if __name__ == '__main__':
    unittest.main()
