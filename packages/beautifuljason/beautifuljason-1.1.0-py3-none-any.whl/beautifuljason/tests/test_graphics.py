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
from beautifuljason.tests.config import datafile_copy_path
import h5py
import numpy as np

class GraphicsItemTestCase(unittest.TestCase):
    """GraphicsItem class test cases"""

    def test_id(self):
        # Testing GraphicsItem.id property
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5')) as doc:
            self.assertEqual(doc.items[0].id, "{4f8dc68f-cd94-4bda-b0cb-22c48506049e}")
            self.assertEqual(doc.items[1].id, "{975d0a83-525a-4191-a698-458dec8ccea8}")
            self.assertEqual(doc.items[2].id, "{b6222fa9-70dc-412c-a42b-90aa15e69adf}")
            self.assertEqual(doc.items[3].id, "{1682d03c-270b-4505-b7aa-2a00c5eb6c2b}")

    def test_linked_ids(self):
        # Testing GraphicsItem.linked_ids property
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5')) as doc:
            item = doc.items[0]
            linked_ids = sorted(item.linked_ids)
            self.assertEqual(linked_ids, ['{1682d03c-270b-4505-b7aa-2a00c5eb6c2b}', '{975d0a83-525a-4191-a698-458dec8ccea8}', '{b6222fa9-70dc-412c-a42b-90aa15e69adf}'])
            del linked_ids[2]
            item.linked_ids = linked_ids
            self.assertEqual(sorted(item.linked_ids), sorted(['{1682d03c-270b-4505-b7aa-2a00c5eb6c2b}', '{975d0a83-525a-4191-a698-458dec8ccea8}']))

            item.linked_ids = []
            self.assertEqual(item.linked_ids, [])

    def test_annotations(self):
        # Testing GraphicsItem.annotations property
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            item = bjason.GraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(len(item.annotations), 3)
            count = 0
            for annot in item.annotations:
                self.assertIsInstance(annot, bjason.GraphicsItem.Annotation)
                count += 1
            self.assertEqual(count, 3)

        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            item = bjason.GraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(len(item.annotations), 0)
            count = 0
            for annot in item.annotations:
                count += 1
            self.assertEqual(count, 0)

    def test_parent_item_id(self):
        # Testing GraphicsItem.parent_item_id property
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5')) as doc:
            for item in doc.items:
                self.assertIsNone(item.parent_item_id)
            
            doc.items[1].parent_item_id = doc.items[0].id
            self.assertEqual(doc.items[1].parent_item_id, doc.items[0].id)
            doc.items[1].parent_item_id = doc.items[2].id
            self.assertEqual(doc.items[1].parent_item_id, doc.items[2].id)
            doc.items[1].parent_item_id = None
            self.assertIsNone(doc.items[1].parent_item_id)
            doc.items[1].parent_item_id = b"{4f8dc68f-cd94-4bda-b0cb-22c48506049e}"
            self.assertEqual(doc.items[1].parent_item_id, '{4f8dc68f-cd94-4bda-b0cb-22c48506049e}' )

            with self.assertRaises(ValueError):
                doc.items[1].parent_item_id = '465hjka'
            with self.assertRaises(AttributeError):
                doc.items[1].parent_item_id = 123

    def test_rotation(self):
        # Testing GraphicsItem.rotation property
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5')) as doc:    
            self.assertEqual(doc.items[0].rotation, 0.0)

            doc.items[0].rotation = 60.0
            self.assertEqual(doc.items[0].rotation, 60.0)

    def test_zValue(self):
        # Testing GraphicsItem.zValue property
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5')) as doc:    
            self.assertEqual(doc.items[0].z_value, 0.0)

            doc.items[0].z_value = 1.0
            self.assertEqual(doc.items[0].z_value, 1.0)
            doc.items[0].z_value = -1.0
            self.assertEqual(doc.items[0].z_value, -1.0)

    def test_pos(self):
         with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            item0 = bjason.GraphicsItem(h5_file['/JasonDocument/Items/0'])
            item1 = bjason.GraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertTrue((item0.pos ==  np.array([10.0, 10.0],np.float64)).all())
            self.assertTrue((item1.pos ==  np.array([946.6099999999999, 10.0], np.float64)).all())
            self.assertTrue((h5_file['/JasonDocument/Items/0'].attrs['Geometry'] == np.array([10.0, 10.0, 931.9114897204116, 972.0], np.float64)).all())
            self.assertTrue((h5_file['/JasonDocument/Items/1'].attrs['Geometry'] == np.array([946.6099999999999, 10.0, 446.39000000000004, 972.0], np.float64)).all())

            item0.pos = (11.1, 22.2)
            self.assertTrue((item0.pos ==  np.array((11.1, 22.2),np.float64)).all())
            self.assertTrue((h5_file['/JasonDocument/Items/0'].attrs['Geometry'] == np.array([11.1, 22.2, 931.9114897204116, 972.0], np.float64)).all())
            item0.pos = [11.2, 22.3]
            self.assertTrue((item0.pos ==  np.array([11.2, 22.3],np.float64)).all())
            self.assertTrue((h5_file['/JasonDocument/Items/0'].attrs['Geometry'] == np.array([11.2, 22.3, 931.9114897204116, 972.0], np.float64)).all())
            item1.pos = (11.1, 22.2)
            self.assertTrue((item1.pos ==  np.array((11.1, 22.2),np.float64)).all())
            self.assertTrue((h5_file['/JasonDocument/Items/1'].attrs['Geometry'] == np.array([11.1, 22.2, 446.39000000000004, 972.0], np.float64)).all())
            item1.pos = [11.2, 22.3]
            self.assertTrue((item1.pos ==  np.array([11.2, 22.3],np.float64)).all())
            self.assertTrue((h5_file['/JasonDocument/Items/1'].attrs['Geometry'] == np.array([11.2, 22.3, 446.39000000000004, 972.0], np.float64)).all())

    def test_size(self):
         with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            item0 = bjason.GraphicsItem(h5_file['/JasonDocument/Items/0'])
            item1 = bjason.GraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertTrue((item0.size == np.array([931.9114897204116, 972.0], np.float64)).all())
            self.assertTrue((item1.size == np.array([446.39000000000004, 972.0], np.float64)).all())

            item0.size = (110.1, 220.2)
            self.assertTrue((item0.size == np.array([110.1, 220.2], np.float64)).all())
            item1.size = (111.1, 222.2)
            self.assertTrue((item1.size == np.array([111.1, 222.2], np.float64)).all())

    def test_type(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5')) as doc:    
            self.assertEqual(doc.items[0].type, bjason.GraphicsItem.Type.NMRSpectrum)
            self.assertEqual(doc.items[1].type, bjason.GraphicsItem.Type.NMRParamTable)
            self.assertEqual(doc.items[2].type, bjason.GraphicsItem.Type.NMRPeakTable)
            self.assertEqual(doc.items[3].type, bjason.GraphicsItem.Type.NMRMultipletTable)

class GraphicsItem_AnnotationTestCase(unittest.TestCase):
    """GraphicsItem.Annotation class test cases"""

    def test_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertEqual(annot.type, bjason.GraphicsItem.Annotation.Type.RECT)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertEqual(annot.type, bjason.GraphicsItem.Annotation.Type.LINE)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertEqual(annot.type, bjason.GraphicsItem.Annotation.Type.TEXT)

    def test_pos(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertTrue((annot.pos == np.array([392.0, 749.0],np.float64)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue((annot.pos == np.array([350.0, 690.0],np.float64)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertTrue((annot.pos == np.array([286.0, 689.0],np.float64)).all())

    def test_local_coords(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertTrue((annot.local_coords == np.array([8.016308209765382, 10101.606856240003, -1.0089400694926773, -11644.879055755244],np.float64)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue((annot.local_coords == np.array([8.497847788386888, 15190.850295421926, 7.99337775364055, 10015.348492864068 ],np.float64)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertTrue((annot.local_coords == np.array([9.231622384381563, 15277.10865879789],np.float64)).all())

    def test_visible(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertTrue(annot.visible) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue(annot.visible)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertTrue(annot.visible)

    def test_pinned(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertTrue(annot.pinned) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.pinned)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertFalse(annot.pinned)

    def test_start_pinned(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.start_pinned) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertFalse(annot.start_pinned)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.start_pinned)

    def test_end_pinned(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.end_pinned) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue(annot.end_pinned)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.end_pinned)

    def test_arrow(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.arrow) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue(annot.arrow)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.arrow)

    def test_pen_color(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertTrue((annot.pen_color == np.array([0, 0, 0, 255, 1],np.int32)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue((annot.pen_color == np.array([0, 0, 0, 255, 1],np.int32)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.pen_color)

    def test_pen_style(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertEqual(annot.pen_style, 1)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertEqual(annot.pen_style, 1)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.pen_style)

    def test_pen_width(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertEqual(annot.pen_width, 1.0)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertEqual(annot.pen_width, 1.0)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.pen_width)

    def test_rect(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertTrue((annot.rect == np.array([0.0, 0.0, 88.0, 135.0],np.float64)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.rect)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.rect)

    def test_line(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.line)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertTrue((annot.line == np.array([0.0, 0.0, 43.999999999999886, 59.99999999999966],np.float64)).all())
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertIsNone(annot.line)

    def test_brush_color(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.brush_color) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.brush_color)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertTrue((annot.brush_color == np.array([0, 0, 0, 255, 1],np.int32)).all())

    def test_rotation(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.rotation) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.rotation)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertEqual(annot.rotation, 270.0)

    def test_text(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.text) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.text)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertEqual(annot.text, 'Test\n      annotation\n                             😎 ')

    def test_font(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.font) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.font)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertEqual(annot.font, {
                'family': 'MS Shell Dlg 2',
                'point_size': 7.8,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Normal,
                'style': bjason.Font.FontStyle.Normal,
                'underline': 0,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0
            })

    def test_html(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_annotations.jjh5'), 'r') as h5_file:
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/0'])
            self.assertIsNone(annot.html) 
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/1'])
            self.assertIsNone(annot.html)
            annot = bjason.GraphicsItem.Annotation(h5_file['/JasonDocument/Items/0/Annotations/2'])
            self.assertEqual(annot.html, "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Times New Roman'; font-size:10pt; font-style:italic;\">Test</span></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      <span style=\" font-family:'Arial'; font-size:10pt; font-weight:600;\">annotation</span></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                             😎 </p></body></html>")

class NMRSpectrumGraphicsItemTestCase(unittest.TestCase):
    """NMRSpectrumGraphicsItem class test cases"""
    def test_spec_data_list(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(len(spec_item.spec_data_list), 1)
            self.assertEqual(spec_item.spec_data_list[0].id, "{46b8cb0d-c7cc-490f-84ed-1b3ea6809425}")

    def test_spec_data(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
             spec_item = doc.nmr_items[0]
             self.assertIsInstance(spec_item.spec_data(), bjason.NMRSpectrum)
             self.assertIsInstance(spec_item.spec_data(0), bjason.NMRSpectrum)
             self.assertIsInstance(spec_item.spec_data('0'), bjason.NMRSpectrum)
             self.assertIsInstance(spec_item.spec_data("{46b8cb0d-c7cc-490f-84ed-1b3ea6809425}"), bjason.NMRSpectrum)
             self.assertIsNone(spec_item.spec_data("46b8cb0d-c7cc-490f-84ed-1b3ea6809425"))
             self.assertIsNone(spec_item.spec_data(1))
             self.assertIsNone(spec_item.spec_data(-1))
             self.assertIsNone(spec_item.spec_data(None))

    def test_header(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.header, "C:/Users/larin/source/repos/jason/bjason/trunk/beautifuljason-base/tests/data/Ethylindanone_Proton-13-1.jdf<br>Ethylindanone")

            spec_item.header = 'test1'
            self.assertEqual(spec_item.header, 'test1')
            spec_item.header = b'test1'
            self.assertEqual(spec_item.header, 'test1')
            spec_item.header = ''
            self.assertEqual(spec_item.header, '')

            with self.assertRaises(TypeError):
                spec_item.header = 123
            with self.assertRaises(TypeError):
                spec_item.header = None

    def test_show_header(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = False
            self.assertFalse(spec_item.show_header)
            spec_item.show_header = True
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = 10
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = 0
            self.assertFalse(spec_item.show_header)

            spec_item.show_header = 'TEST'
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = ''
            self.assertFalse(spec_item.show_header)

    def test_show_x_axis(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_x_axis)
            spec_item.show_x_axis = False
            self.assertFalse(spec_item.show_x_axis)
            spec_item.show_x_axis = True
            self.assertTrue(spec_item.show_x_axis)
            spec_item.show_x_axis = 10
            self.assertTrue(spec_item.show_x_axis)
            spec_item.show_x_axis = 0
            self.assertFalse(spec_item.show_x_axis)

            spec_item.show_x_axis = 'TEST'
            self.assertTrue(spec_item.show_x_axis)
            spec_item.show_x_axis = ''
            self.assertFalse(spec_item.show_x_axis)
    
    def test_show_y_axis(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_y_axis)
            spec_item.show_y_axis = False
            self.assertFalse(spec_item.show_y_axis)
            spec_item.show_y_axis = True
            self.assertTrue(spec_item.show_y_axis)
            spec_item.show_y_axis = 10
            self.assertTrue(spec_item.show_y_axis)
            spec_item.show_y_axis = 0
            self.assertFalse(spec_item.show_y_axis)

            spec_item.show_y_axis = 'TEST'
            self.assertTrue(spec_item.show_y_axis)
            spec_item.show_y_axis = ''
            self.assertFalse(spec_item.show_y_axis)

    def test_active_bold(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.active_bold)
            spec_item.active_bold = False
            self.assertFalse(spec_item.active_bold)
            spec_item.active_bold = True
            self.assertTrue(spec_item.active_bold)
            spec_item.active_bold = 10
            self.assertTrue(spec_item.active_bold)
            spec_item.active_bold = 0
            self.assertFalse(spec_item.active_bold)

            spec_item.active_bold = 'TEST'
            self.assertTrue(spec_item.active_bold)
            spec_item.active_bold = ''
            self.assertFalse(spec_item.active_bold)

    def test_antialiasing(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.antialiasing)
            spec_item.antialiasing = False
            self.assertFalse(spec_item.antialiasing)
            spec_item.antialiasing = True
            self.assertTrue(spec_item.antialiasing)
            spec_item.antialiasing = 10
            self.assertTrue(spec_item.antialiasing)
            spec_item.antialiasing = 0
            self.assertFalse(spec_item.antialiasing)

            spec_item.antialiasing = 'TEST'
            self.assertTrue(spec_item.antialiasing)
            spec_item.antialiasing = ''
            self.assertFalse(spec_item.antialiasing)

    def test_color_cont(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.color_cont)
            spec_item.color_cont = False
            self.assertFalse(spec_item.color_cont)
            spec_item.color_cont = True
            self.assertTrue(spec_item.color_cont)
            spec_item.color_cont = 10
            self.assertTrue(spec_item.color_cont)
            spec_item.color_cont = 0
            self.assertFalse(spec_item.color_cont)

            spec_item.color_cont = 'TEST'
            self.assertTrue(spec_item.color_cont)
            spec_item.color_cont = ''
            self.assertFalse(spec_item.color_cont)

    def test_mix_fid_spec(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.mix_fid_spec)
            spec_item.mix_fid_spec = False
            self.assertFalse(spec_item.mix_fid_spec)
            spec_item.mix_fid_spec = True
            self.assertTrue(spec_item.mix_fid_spec)
            spec_item.mix_fid_spec = 10
            self.assertTrue(spec_item.mix_fid_spec)
            spec_item.mix_fid_spec = 0
            self.assertFalse(spec_item.mix_fid_spec)

            spec_item.mix_fid_spec = 'TEST'
            self.assertTrue(spec_item.mix_fid_spec)
            spec_item.mix_fid_spec = ''
            self.assertFalse(spec_item.mix_fid_spec)

    def test_plot_2d_color_gradient(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.plot_2d_color_gradient)
            spec_item.plot_2d_color_gradient = False
            self.assertFalse(spec_item.plot_2d_color_gradient)
            spec_item.plot_2d_color_gradient = True
            self.assertTrue(spec_item.plot_2d_color_gradient)
            spec_item.plot_2d_color_gradient = 10
            self.assertTrue(spec_item.plot_2d_color_gradient)
            spec_item.plot_2d_color_gradient = 0
            self.assertFalse(spec_item.plot_2d_color_gradient)

            spec_item.plot_2d_color_gradient = 'TEST'
            self.assertTrue(spec_item.plot_2d_color_gradient)
            spec_item.plot_2d_color_gradient = ''
            self.assertFalse(spec_item.plot_2d_color_gradient)

    def test_show_header(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = False
            self.assertFalse(spec_item.show_header)
            spec_item.show_header = True
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = 10
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = 0
            self.assertFalse(spec_item.show_header)

            spec_item.show_header = 'TEST'
            self.assertTrue(spec_item.show_header)
            spec_item.show_header = ''
            self.assertFalse(spec_item.show_header)

    def test_show_integrals_multiplets(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_integrals_multiplets)
            spec_item.show_integrals_multiplets = False
            self.assertFalse(spec_item.show_integrals_multiplets)
            spec_item.show_integrals_multiplets = True
            self.assertTrue(spec_item.show_integrals_multiplets)
            spec_item.show_integrals_multiplets = 10
            self.assertTrue(spec_item.show_integrals_multiplets)
            spec_item.show_integrals_multiplets = 0
            self.assertFalse(spec_item.show_integrals_multiplets)

            spec_item.show_integrals_multiplets = 'TEST'
            self.assertTrue(spec_item.show_integrals_multiplets)
            spec_item.show_integrals_multiplets = ''
            self.assertFalse(spec_item.show_integrals_multiplets)

    def test_show_peak_models(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.show_peak_models)
            spec_item.show_peak_models = False
            self.assertFalse(spec_item.show_peak_models)
            spec_item.show_peak_models = True
            self.assertTrue(spec_item.show_peak_models)
            spec_item.show_peak_models = 10
            self.assertTrue(spec_item.show_peak_models)
            spec_item.show_peak_models = 0
            self.assertFalse(spec_item.show_peak_models)

            spec_item.show_peak_models = 'TEST'
            self.assertTrue(spec_item.show_peak_models)
            spec_item.show_peak_models = ''
            self.assertFalse(spec_item.show_peak_models)

    def test_show_peak_residuals(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.show_peak_residuals)
            spec_item.show_peak_residuals = False
            self.assertFalse(spec_item.show_peak_residuals)
            spec_item.show_peak_residuals = True
            self.assertTrue(spec_item.show_peak_residuals)
            spec_item.show_peak_residuals = 10
            self.assertTrue(spec_item.show_peak_residuals)
            spec_item.show_peak_residuals = 0
            self.assertFalse(spec_item.show_peak_residuals)

            spec_item.show_peak_residuals = 'TEST'
            self.assertTrue(spec_item.show_peak_residuals)
            spec_item.show_peak_residuals = ''
            self.assertFalse(spec_item.show_peak_residuals)

    def test_show_peak_sum(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.show_peak_sum)
            spec_item.show_peak_sum = False
            self.assertFalse(spec_item.show_peak_sum)
            spec_item.show_peak_sum = True
            self.assertTrue(spec_item.show_peak_sum)
            spec_item.show_peak_sum = 10
            self.assertTrue(spec_item.show_peak_sum)
            spec_item.show_peak_sum = 0
            self.assertFalse(spec_item.show_peak_sum)

            spec_item.show_peak_sum = 'TEST'
            self.assertTrue(spec_item.show_peak_sum)
            spec_item.show_peak_sum = ''
            self.assertFalse(spec_item.show_peak_sum)

    def test_show_peaks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_peaks)
            spec_item.show_peaks = False
            self.assertFalse(spec_item.show_peaks)
            spec_item.show_peaks = True
            self.assertTrue(spec_item.show_peaks)
            spec_item.show_peaks = 10
            self.assertTrue(spec_item.show_peaks)
            spec_item.show_peaks = 0
            self.assertFalse(spec_item.show_peaks)

            spec_item.show_peaks = 'TEST'
            self.assertTrue(spec_item.show_peaks)
            spec_item.show_peaks = ''
            self.assertFalse(spec_item.show_peaks)

    def test_show_x_grid(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.show_x_grid)
            spec_item.show_x_grid = False
            self.assertFalse(spec_item.show_x_grid)
            spec_item.show_x_grid = True
            self.assertTrue(spec_item.show_x_grid)
            spec_item.show_x_grid = 10
            self.assertTrue(spec_item.show_x_grid)
            spec_item.show_x_grid = 0
            self.assertFalse(spec_item.show_x_grid)

            spec_item.show_x_grid = 'TEST'
            self.assertTrue(spec_item.show_x_grid)
            spec_item.show_x_grid = ''
            self.assertFalse(spec_item.show_x_grid)

    def test_show_y_axis_2d(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.show_y_axis_2d)
            spec_item.show_y_axis_2d = False
            self.assertFalse(spec_item.show_y_axis_2d)
            spec_item.show_y_axis_2d= True
            self.assertTrue(spec_item.show_y_axis_2d)
            spec_item.show_y_axis_2d = 10
            self.assertTrue(spec_item.show_y_axis_2d)
            spec_item.show_y_axis_2d = 0
            self.assertFalse(spec_item.show_y_axis_2d)

            spec_item.show_y_axis_2d = 'TEST'
            self.assertTrue(spec_item.show_y_axis_2d)
            spec_item.show_y_axis_2d = ''
            self.assertFalse(spec_item.show_y_axis_2d)

    def test_y_axis_right(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.y_axis_right)
            spec_item.y_axis_right = False
            self.assertFalse(spec_item.y_axis_right)
            spec_item.y_axis_right= True
            self.assertTrue(spec_item.y_axis_right)
            spec_item.y_axis_right = 10
            self.assertTrue(spec_item.y_axis_right)
            spec_item.y_axis_right = 0
            self.assertFalse(spec_item.y_axis_right)

            spec_item.y_axis_right = 'TEST'
            self.assertTrue(spec_item.y_axis_right)
            spec_item.y_axis_right = ''
            self.assertFalse(spec_item.y_axis_right)

    def test_show_y_grid(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.show_y_grid)
            spec_item.show_y_grid = False
            self.assertFalse(spec_item.show_y_grid)
            spec_item.show_y_grid= True
            self.assertTrue(spec_item.show_y_grid)
            spec_item.show_y_grid = 10
            self.assertTrue(spec_item.show_y_grid)
            spec_item.show_y_grid = 0
            self.assertFalse(spec_item.show_y_grid)

            spec_item.show_y_grid = 'TEST'
            self.assertTrue(spec_item.show_y_grid)
            spec_item.show_y_grid = ''
            self.assertFalse(spec_item.show_y_grid)

    def test_y_outside_labels(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.y_outside_labels)
            spec_item.y_outside_labels = False
            self.assertFalse(spec_item.y_outside_labels)
            spec_item.y_outside_labels= True
            self.assertTrue(spec_item.y_outside_labels)
            spec_item.y_outside_labels = 10
            self.assertTrue(spec_item.y_outside_labels)
            spec_item.y_outside_labels = 0
            self.assertFalse(spec_item.y_outside_labels)

            spec_item.y_outside_labels = 'TEST'
            self.assertTrue(spec_item.y_outside_labels)
            spec_item.y_outside_labels = ''
            self.assertFalse(spec_item.y_outside_labels)

    def test_show_legend(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertFalse(spec_item.show_legend)
            spec_item.show_legend = False
            self.assertFalse(spec_item.show_legend)
            spec_item.show_legend= True
            self.assertTrue(spec_item.show_legend)
            spec_item.show_legend = 10
            self.assertTrue(spec_item.show_legend)
            spec_item.show_legend = 0
            self.assertFalse(spec_item.show_legend)

            spec_item.show_legend = 'TEST'
            self.assertTrue(spec_item.show_legend)
            spec_item.show_legend = ''
            self.assertFalse(spec_item.show_legend)

    def test_has_x_extra_ticks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.has_x_extra_ticks)
            spec_item.has_x_extra_ticks = False
            self.assertFalse(spec_item.has_x_extra_ticks)
            spec_item.has_x_extra_ticks= True
            self.assertTrue(spec_item.has_x_extra_ticks)
            spec_item.has_x_extra_ticks = 10
            self.assertTrue(spec_item.has_x_extra_ticks)
            spec_item.has_x_extra_ticks = 0
            self.assertFalse(spec_item.has_x_extra_ticks)

            spec_item.has_x_extra_ticks = 'TEST'
            self.assertTrue(spec_item.has_x_extra_ticks)
            spec_item.has_x_extra_ticks = ''
            self.assertFalse(spec_item.has_x_extra_ticks)

    def test_has_y_extra_ticks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertTrue(spec_item.has_y_extra_ticks)
            spec_item.has_y_extra_ticks = False
            self.assertFalse(spec_item.has_y_extra_ticks)
            spec_item.has_y_extra_ticks= True
            self.assertTrue(spec_item.has_y_extra_ticks)
            spec_item.has_y_extra_ticks = 10
            self.assertTrue(spec_item.has_y_extra_ticks)
            spec_item.has_y_extra_ticks = 0
            self.assertFalse(spec_item.has_y_extra_ticks)

            spec_item.has_y_extra_ticks = 'TEST'
            self.assertTrue(spec_item.has_y_extra_ticks)
            spec_item.has_y_extra_ticks = ''
            self.assertFalse(spec_item.has_y_extra_ticks)

    def test_plot_1d_color(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.plot_1d_color, '#000066FF')

            spec_item.plot_1d_color = '#01A0FB00'
            self.assertEqual(spec_item.plot_1d_color, '#01A0FB00')
            
            spec_item.plot_1d_color = '#010000'
            self.assertEqual(spec_item.plot_1d_color, '#010000FF')

    def test_plot_2d_neg_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.plot_2d_neg_color, '#00FFFFFF')

            spec_item.plot_2d_neg_color = '#01A0FB00'
            self.assertEqual(spec_item.plot_2d_neg_color, '#01A0FB00')
            
            spec_item.plot_2d_neg_color = '#010000'
            self.assertEqual(spec_item.plot_2d_neg_color, '#010000FF')

    def test_plot_2d_pos_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.plot_2d_pos_color, '#FF0000FF')

            spec_item.plot_2d_pos_color = '#01A0FB00'
            self.assertEqual(spec_item.plot_2d_pos_color, '#01A0FB00')
            
            spec_item.plot_2d_pos_color = '#010000'
            self.assertEqual(spec_item.plot_2d_pos_color, '#010000FF')

    def test_integral_curve_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.integral_curve_color, '#000066FF')

            spec_item.integral_curve_color = '#01A0FB00'
            self.assertEqual(spec_item.integral_curve_color, '#01A0FB00')
            
            spec_item.integral_curve_color = '#010000'
            self.assertEqual(spec_item.integral_curve_color, '#010000FF')

    def test_mult_intg_label_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.mult_intg_label_color, '#000066FF')

            spec_item.mult_intg_label_color = '#01A0FB00'
            self.assertEqual(spec_item.mult_intg_label_color, '#01A0FB00')
            
            spec_item.mult_intg_label_color = '#010000'
            self.assertEqual(spec_item.mult_intg_label_color, '#010000FF')

    def test_peak_shape_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.peak_shape_color, '#0000FFFF')

            spec_item.peak_shape_color = '#01A0FB00'
            self.assertEqual(spec_item.peak_shape_color, '#01A0FB00')
            
            spec_item.peak_shape_color = '#010000'
            self.assertEqual(spec_item.peak_shape_color, '#010000FF')

    def test_x_axis_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.x_axis_color, '#000000FF')

            spec_item.x_axis_color = '#01A0FB00'
            self.assertEqual(spec_item.x_axis_color, '#01A0FB00')
            
            spec_item.x_axis_color = '#010000'
            self.assertEqual(spec_item.x_axis_color, '#010000FF')
         
    def test_y_axis_color(self):
         with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertEqual(spec_item.y_axis_color, '#000000FF')

            spec_item.y_axis_color = '#01A0FB00'
            self.assertEqual(spec_item.y_axis_color, '#01A0FB00')
            
            spec_item.y_axis_color = '#010000'
            self.assertEqual(spec_item.y_axis_color, '#010000FF')

    def test_floor(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.floor, np.float64)
            self.assertEqual(spec_item.floor, 6.25)
            spec_item.floor = 1.1
            self.assertEqual(spec_item.floor, 1.1)
            self.assertIsInstance(spec_item.floor, np.float64)
            spec_item.floor = 4.68
            self.assertEqual(spec_item.floor, 4.68)
            self.assertIsInstance(spec_item.floor, np.float64)
            spec_item.floor = 5
            self.assertEqual(spec_item.floor, 5)
            self.assertIsInstance(spec_item.floor, np.float64)
            spec_item.floor = '3.14'
            self.assertEqual(spec_item.floor, 3.14)
            self.assertIsInstance(spec_item.floor, np.float64)

            with self.assertRaises(ValueError):
                spec_item.floor = 'test'

    def test_integral_label_v_shift(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.integral_label_v_shift, np.float64)
            self.assertEqual(spec_item.integral_label_v_shift, 0.0)
            spec_item.integral_label_v_shift = 1.1
            self.assertEqual(spec_item.integral_label_v_shift, 1.1)
            self.assertIsInstance(spec_item.integral_label_v_shift, np.float64)
            spec_item.integral_label_v_shift = 4.68
            self.assertEqual(spec_item.integral_label_v_shift, 4.68)
            self.assertIsInstance(spec_item.integral_label_v_shift, np.float64)
            spec_item.integral_label_v_shift = 5
            self.assertEqual(spec_item.integral_label_v_shift, 5)
            self.assertIsInstance(spec_item.integral_label_v_shift, np.float64)
            spec_item.integral_label_v_shift = '3.14'
            self.assertEqual(spec_item.integral_label_v_shift, 3.14)
            self.assertIsInstance(spec_item.integral_label_v_shift, np.float64)

            with self.assertRaises(ValueError):
                spec_item.integral_label_v_shift = 'test'

    def test_multiplet_label_v_shift(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.multiplet_label_v_shift, np.float64)
            self.assertEqual(spec_item.multiplet_label_v_shift, 0.0)
            spec_item.multiplet_label_v_shift = 1.1
            self.assertEqual(spec_item.multiplet_label_v_shift, 1.1)
            self.assertIsInstance(spec_item.multiplet_label_v_shift, np.float64)
            spec_item.multiplet_label_v_shift = 4.68
            self.assertEqual(spec_item.multiplet_label_v_shift, 4.68)
            self.assertIsInstance(spec_item.multiplet_label_v_shift, np.float64)
            spec_item.multiplet_label_v_shift = 5
            self.assertEqual(spec_item.multiplet_label_v_shift, 5)
            self.assertIsInstance(spec_item.multiplet_label_v_shift, np.float64)
            spec_item.multiplet_label_v_shift = '3.14'
            self.assertEqual(spec_item.multiplet_label_v_shift, 3.14)
            self.assertIsInstance(spec_item.multiplet_label_v_shift, np.float64)

            with self.assertRaises(ValueError):
                spec_item.multiplet_label_v_shift = 'test'

    def test_separation_inc(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.separation_inc, np.float64)
            self.assertEqual(spec_item.separation_inc, 0.0)
            spec_item.separation_inc = 1.1
            self.assertEqual(spec_item.separation_inc, 1.1)
            self.assertIsInstance(spec_item.separation_inc, np.float64)
            spec_item.separation_inc = 4.68
            self.assertEqual(spec_item.separation_inc, 4.68)
            self.assertIsInstance(spec_item.separation_inc, np.float64)
            spec_item.separation_inc = 5
            self.assertEqual(spec_item.separation_inc, 5)
            self.assertIsInstance(spec_item.separation_inc, np.float64)
            spec_item.separation_inc = '3.14'
            self.assertEqual(spec_item.separation_inc, 3.14)
            self.assertIsInstance(spec_item.separation_inc, np.float64)

            with self.assertRaises(ValueError):
                spec_item.separation_inc = 'test'

    def test_tilt_inc(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.tilt_inc, np.float64)
            self.assertEqual(spec_item.tilt_inc, 0.0)
            spec_item.tilt_inc = 1.1
            self.assertEqual(spec_item.tilt_inc, 1.1)
            self.assertIsInstance(spec_item.tilt_inc, np.float64)
            spec_item.tilt_inc = 4.68
            self.assertEqual(spec_item.tilt_inc, 4.68)
            self.assertIsInstance(spec_item.tilt_inc, np.float64)
            spec_item.tilt_inc = 5
            self.assertEqual(spec_item.tilt_inc, 5)
            self.assertIsInstance(spec_item.tilt_inc, np.float64)
            spec_item.tilt_inc = '3.14'
            self.assertEqual(spec_item.tilt_inc, 3.14)
            self.assertIsInstance(spec_item.tilt_inc, np.float64)

            with self.assertRaises(ValueError):
                spec_item.tilt_inc = 'test'

    def test_mult_intg_label_digits(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.mult_intg_label_digits, np.int32)
            self.assertEqual(spec_item.mult_intg_label_digits, 3)
            spec_item.mult_intg_label_digits = -5
            self.assertEqual(spec_item.mult_intg_label_digits, -5)
            self.assertIsInstance(spec_item.mult_intg_label_digits, np.int32)
            spec_item.mult_intg_label_digits = 4.68
            self.assertEqual(spec_item.mult_intg_label_digits, 4)

            with self.assertRaises(ValueError):
                spec_item.mult_intg_label_digits = 'test'

    def test_mult_intg_pos_digits(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.mult_intg_pos_digits, np.int32)
            self.assertEqual(spec_item.mult_intg_pos_digits, 3)
            spec_item.mult_intg_pos_digits = -5
            self.assertEqual(spec_item.mult_intg_pos_digits, -5)
            self.assertIsInstance(spec_item.mult_intg_pos_digits, np.int32)
            spec_item.mult_intg_pos_digits = 4.68
            self.assertEqual(spec_item.mult_intg_pos_digits, 4)

            with self.assertRaises(ValueError):
                spec_item.mult_intg_pos_digits = 'test'

    def test_multi_plot_type_2d(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.multi_plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D)
            self.assertEqual(spec_item.multi_plot_type_2d, 3)
            self.assertEqual(spec_item.multi_plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D.VER_STACK)
            self.assertIsInstance(spec_item.multi_plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D)
            spec_item.multi_plot_type_2d = bjason.NMRSpectrumGraphicsItem.PlotType2D.CONTOURS
            self.assertEqual(spec_item.multi_plot_type_2d, 1)
            self.assertEqual(spec_item.multi_plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D.CONTOURS)
            self.assertIsInstance(spec_item.multi_plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D)

            with self.assertRaises(ValueError):
                spec_item.multi_plot_type_2d = 'test'

    def test_n_levels(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.n_levels, np.int32)
            self.assertEqual(spec_item.n_levels, 10)
            spec_item.n_levels = -5
            self.assertEqual(spec_item.n_levels, -5)
            self.assertIsInstance(spec_item.n_levels, np.int32)
            spec_item.n_levels = 4.68
            self.assertEqual(spec_item.n_levels, 4)
            self.assertIsInstance(spec_item.n_levels, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.n_levels = 'test'

    def test_n_x_extra_ticks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.n_x_extra_ticks, np.int32)
            self.assertEqual(spec_item.n_x_extra_ticks, 5)
            spec_item.n_x_extra_ticks = -5
            self.assertEqual(spec_item.n_x_extra_ticks, -5)
            self.assertIsInstance(spec_item.n_x_extra_ticks, np.int32)
            spec_item.n_x_extra_ticks = 4.68
            self.assertEqual(spec_item.n_x_extra_ticks, 4)
            self.assertIsInstance(spec_item.n_x_extra_ticks, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.n_x_extra_ticks = 'test'

    def test_n_y_extra_ticks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.n_y_extra_ticks, np.int32)
            self.assertEqual(spec_item.n_y_extra_ticks, 5)
            spec_item.n_y_extra_ticks = -5
            self.assertEqual(spec_item.n_y_extra_ticks, -5)
            self.assertIsInstance(spec_item.n_y_extra_ticks, np.int32)
            spec_item.n_y_extra_ticks = 4.68
            self.assertEqual(spec_item.n_y_extra_ticks, 4)
            self.assertIsInstance(spec_item.n_y_extra_ticks, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.n_y_extra_ticks = 'test'

    def test_plot_1d_width(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.plot_1d_width, np.int32)
            self.assertEqual(spec_item.plot_1d_width, 0)
            spec_item.plot_1d_width = -5
            self.assertEqual(spec_item.plot_1d_width, -5)
            self.assertIsInstance(spec_item.plot_1d_width, np.int32)
            spec_item.plot_1d_width = 4.68
            self.assertEqual(spec_item.plot_1d_width, 4)
            self.assertIsInstance(spec_item.plot_1d_width, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.plot_1d_width = 'test'

    def test_plot_2d_width(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.plot_2d_width, np.int32)
            self.assertEqual(spec_item.plot_2d_width, 0)
            spec_item.plot_2d_width = -5
            self.assertEqual(spec_item.plot_2d_width, -5)
            self.assertIsInstance(spec_item.plot_2d_width, np.int32)
            spec_item.plot_2d_width = 4.68
            self.assertEqual(spec_item.plot_2d_width, 4)
            self.assertIsInstance(spec_item.plot_2d_width, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.plot_2d_width = 'test'

    def test_plot_type_2d(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D)
            self.assertEqual(spec_item.plot_type_2d,  bjason.NMRSpectrumGraphicsItem.PlotType2D.CONTOURS)
            self.assertIsInstance(spec_item.plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D)
            spec_item.plot_type_2d = bjason.NMRSpectrumGraphicsItem.PlotType2D.RASTER
            self.assertEqual(spec_item.plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D.RASTER)
            self.assertIsInstance(spec_item.plot_type_2d, bjason.NMRSpectrumGraphicsItem.PlotType2D)
            
            with self.assertRaises(ValueError):
                spec_item.plot_type_2d = 'test'

    def test_pos_neg(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.pos_neg, np.int32)
            self.assertEqual(spec_item.pos_neg, 1)
            spec_item.pos_neg = -5
            self.assertEqual(spec_item.pos_neg, -5)
            self.assertIsInstance(spec_item.pos_neg, np.int32)
            spec_item.pos_neg = 4.68
            self.assertEqual(spec_item.pos_neg, 4)
            self.assertIsInstance(spec_item.pos_neg, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.pos_neg = 'test'

    def test_print_line_width(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.print_line_width, np.int32)
            self.assertEqual(spec_item.print_line_width, 1)
            spec_item.print_line_width = -5
            self.assertEqual(spec_item.print_line_width, -5)
            self.assertIsInstance(spec_item.print_line_width, np.int32)
            spec_item.print_line_width = 4.68
            self.assertEqual(spec_item.print_line_width, 4)
            self.assertIsInstance(spec_item.print_line_width, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.print_line_width = 'test'

    def test_print_mode(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.print_mode, bjason.NMRSpectrumGraphicsItem.Print1DMode)
            self.assertEqual(spec_item.print_mode, bjason.NMRSpectrumGraphicsItem.Print1DMode.SPLIT)
            spec_item.print_mode = bjason.NMRSpectrumGraphicsItem.Print1DMode.ALL
            self.assertEqual(spec_item.print_mode, bjason.NMRSpectrumGraphicsItem.Print1DMode.ALL)
            self.assertIsInstance(spec_item.print_mode, bjason.NMRSpectrumGraphicsItem.Print1DMode)
            
            with self.assertRaises(ValueError):
                spec_item.print_mode = 'test'

    def test_x_ticks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.x_ticks, np.int32)
            self.assertEqual(spec_item.x_ticks, 10)
            spec_item.x_ticks = -5
            self.assertEqual(spec_item.x_ticks, -5)
            self.assertIsInstance(spec_item.x_ticks, np.int32)
            spec_item.x_ticks = 4.68
            self.assertEqual(spec_item.x_ticks, 4)
            self.assertIsInstance(spec_item.x_ticks, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.x_ticks = 'test'


    def test_y_ticks(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            self.assertIsInstance(spec_item.y_ticks, np.int32)
            self.assertEqual(spec_item.y_ticks, 10)
            spec_item.y_ticks = -5
            self.assertEqual(spec_item.y_ticks, -5)
            self.assertIsInstance(spec_item.y_ticks, np.int32)
            spec_item.y_ticks = 4.68
            self.assertEqual(spec_item.y_ticks, 4)
            self.assertIsInstance(spec_item.y_ticks, np.int32)
            
            with self.assertRaises(ValueError):
                spec_item.y_ticks = 'test'

    def test_header_font(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            font = spec_item.header_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8.1 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle )
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            spec_item.header_font = font 
            self.assertEqual(spec_item.header_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(spec_item.header_font, font)
            spec_item.header_font = font 
            self.assertEqual(spec_item.header_font, font)

    def test_j_tree_label_font(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            font = spec_item.j_tree_label_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle )
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            spec_item.j_tree_label_font = font 
            self.assertEqual(spec_item.j_tree_label_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(spec_item.j_tree_label_font, font)
            spec_item.j_tree_label_font = font 
            self.assertEqual(spec_item.j_tree_label_font, font)

    def test_mult_intg_label_font(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            font = spec_item.mult_intg_label_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle )
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            spec_item.mult_intg_label_font = font 
            self.assertEqual(spec_item.mult_intg_label_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(spec_item.mult_intg_label_font, font)
            spec_item.mult_intg_label_font = font 
            self.assertEqual(spec_item.mult_intg_label_font, font)

    def test_peak_label_font(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            font = spec_item.peak_label_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle )
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            spec_item.peak_label_font = font 
            self.assertEqual(spec_item.peak_label_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(spec_item.peak_label_font, font)
            spec_item.peak_label_font = font 
            self.assertEqual(spec_item.peak_label_font, font)  

    def test_x_font(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            font = spec_item.x_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle )
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            spec_item.x_font = font 
            self.assertEqual(spec_item.x_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(spec_item.x_font, font)
            spec_item.x_font = font 
            self.assertEqual(spec_item.x_font, font)       

    def test_y_font(self):
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            spec_item = doc.nmr_items[0]
            font = spec_item.y_font
            self.assertEqual(font['family'],'MS Shell Dlg 2')
            self.assertEqual(font['point_size'], 8)
            self.assertEqual(font['pixel_size'], -1)
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle)
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal)
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal)
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            spec_item.y_font = font
            self.assertEqual(spec_item.y_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(spec_item.y_font, font)
            spec_item.y_font = font
            self.assertEqual(spec_item.y_font, font)
            
class TableGraphicsItemTestCase(unittest.TestCase):
    """TableGraphicsItem class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(table_item.id, '{975d0a83-525a-4191-a698-458dec8ccea8}')
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(table_item.id, '{b6222fa9-70dc-412c-a42b-90aa15e69adf}')
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertEqual(table_item.id, '{1682d03c-270b-4505-b7aa-2a00c5eb6c2b}')

    def test_horizontal_header(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            # Testing the getter of item 1
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            horizontal_header = table_item.horizontal_header
            self.assertEqual(horizontal_header, {
                'versionMarker': 255,
                'version': 0,
                'orientation': 1,
                'sortIndicatorOrder': 1,
                'sortIndicatorSection': 0,
                'sortIndicatorShown': False,
                'visualIndices': (),
                'logicalIndices': (),
                'sectionsHidden': (),
                'hiddenSectionSize': {},
                'length': 462, 
                'sectionCount': 2,
                'movableSections': False,
                'clickableSections': True,
                'highlightSelected': True,
                'stretchLastSection': False,
                'cascadingResizing': False,
                'stretchSections': 0,
                'contentsSections': 0,
                'defaultSectionSize': 125, 
                'minimumSectionSize': -1,
                'defaultAlignment': 132,
                'globalResizeMode': 0,
                'sectionItems': [
                    {'size': 114, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 348, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}
                ],
                'resizeContentsPrecision': 1000,
                'customDefaultSectionSize': False,
                'lastSectionSize': 0
            })
            # Testing the setter of item 1
            table_item.horizontal_header = horizontal_header
            self.assertEqual(table_item.horizontal_header, {
                'versionMarker': 255,
                'version': 0,
                'orientation': 1,
                'sortIndicatorOrder': 1,
                'sortIndicatorSection': 0,
                'sortIndicatorShown': False,
                'visualIndices': (),
                'logicalIndices': (),
                'sectionsHidden': (),
                'hiddenSectionSize': {},
                'length': 462, 
                'sectionCount': 2,
                'movableSections': False,
                'clickableSections': True,
                'highlightSelected': True,
                'stretchLastSection': False,
                'cascadingResizing': False,
                'stretchSections': 0,
                'contentsSections': 0,
                'defaultSectionSize': 125, 
                'minimumSectionSize': -1,
                'defaultAlignment': 132,
                'globalResizeMode': 0,
                'sectionItems': [
                    {'size': 114, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 348, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}
                ],
                'resizeContentsPrecision': 1000,
                'customDefaultSectionSize': False,
                'lastSectionSize': 0
            })
            # Testing the getter of item 2
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            horizontal_header = table_item.horizontal_header
            self.assertEqual(horizontal_header, {
                'versionMarker': 255,
                'version': 0,
                'orientation': 1,
                'sortIndicatorOrder': 1,
                'sortIndicatorSection': 0, 
                'sortIndicatorShown': True, 
                'visualIndices': (1, 3, 2, 4, 5, 0, 6),
                'logicalIndices': (5, 0, 2, 1, 3, 4, 6),
                'sectionsHidden': (False, False, False, False, True, False, True),
                'hiddenSectionSize': {3: 40, 6: 40},
                'length': 386,
                'sectionCount': 7,
                'movableSections': True,
                'clickableSections': True,
                'highlightSelected': True,
                'stretchLastSection': False,
                'cascadingResizing': False,
                'stretchSections': 0,
                'contentsSections': 0,
                'defaultSectionSize': 125,
                'minimumSectionSize': -1,
                'defaultAlignment': 132,
                'globalResizeMode': 0,
                'sectionItems': [
                    {'size': 84, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 84, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 88, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 65, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 0, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 65, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 0, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}
                ],
                'resizeContentsPrecision': 1000,
                'customDefaultSectionSize': False,
                'lastSectionSize': 0
            })

            # Testing the indices mapping
            ColID = bjason.NMRPeakTableGraphicsItem.ColumnID
            visualIndices = horizontal_header['visualIndices'] # (1, 3, 2, 4, 5, 0, 6),
            logicalIndices = horizontal_header['logicalIndices'] # (5, 0, 2, 1, 3, 4, 6),
            sectionsHidden = horizontal_header['sectionsHidden'] # (False, False, False, False, True, False, True),
            self.assertEqual(len(visualIndices), horizontal_header['sectionCount'])
            self.assertEqual(len(visualIndices), len(logicalIndices))
            self.assertEqual(len(visualIndices), len(sectionsHidden))
            for i in range(len(visualIndices)):
                self.assertEqual(i, visualIndices[logicalIndices[i]])
                self.assertEqual(i, logicalIndices[visualIndices[i]])
            self.assertTrue(sectionsHidden[4])
            self.assertEqual(table_item.columns[logicalIndices[4]].col_id, ColID.KURTOSIS0)
            self.assertTrue(sectionsHidden[6])
            self.assertEqual(table_item.columns[logicalIndices[6]].col_id, ColID.LABEL)

            # Testing the setter of item 2
            table_item.horizontal_header = horizontal_header
            self.assertEqual(table_item.horizontal_header, {
                'versionMarker': 255,
                'version': 0,
                'orientation': 1,
                'sortIndicatorOrder': 1,
                'sortIndicatorSection': 0, 
                'sortIndicatorShown': True, 
                'visualIndices': (1, 3, 2, 4, 5, 0, 6),
                'logicalIndices': (5, 0, 2, 1, 3, 4, 6),
                'sectionsHidden': (False, False, False, False, True, False, True),
                'hiddenSectionSize': {3: 40, 6: 40},
                'length': 386,
                'sectionCount': 7,
                'movableSections': True,
                'clickableSections': True,
                'highlightSelected': True,
                'stretchLastSection': False,
                'cascadingResizing': False,
                'stretchSections': 0,
                'contentsSections': 0,
                'defaultSectionSize': 125,
                'minimumSectionSize': -1,
                'defaultAlignment': 132,
                'globalResizeMode': 0,
                'sectionItems': [
                    {'size': 84, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 84, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 88, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 65, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 0, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}, 
                    {'size': 65, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 0, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}
                ],
                'resizeContentsPrecision': 1000,
                'customDefaultSectionSize': False,
                'lastSectionSize': 0
            })
            # Testing the getter of item 3
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            horizontal_header = table_item.horizontal_header
            self.assertEqual(horizontal_header, {
                'versionMarker': 255,
                'version': 0,
                'orientation': 1,
                'sortIndicatorOrder': 1,
                'sortIndicatorSection': 0,
                'sortIndicatorShown': True,
                'visualIndices': (), 
                'logicalIndices': (), 
                'sectionsHidden': (), 
                'hiddenSectionSize': {}, 
                'length': 837, 
                'sectionCount': 10, 
                'movableSections': True, 
                'clickableSections': True, 
                'highlightSelected': True, 
                'stretchLastSection': False, 
                'cascadingResizing': False, 
                'stretchSections': 0, 
                'contentsSections': 0,
                'defaultSectionSize': 125, 
                'minimumSectionSize': -1, 
                'defaultAlignment': 132, 
                'globalResizeMode': 0, 
                'sectionItems': [
                    {'size': 84, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 94, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 86, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 54, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 50, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 92, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 45, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 139, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 104, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 89, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}
                ],
                'resizeContentsPrecision': 1000, 
                'customDefaultSectionSize': False, 
                'lastSectionSize': 0
            })
            # Testing the setter of item 3
            table_item.horizontal_header = horizontal_header
            self.assertEqual(table_item.horizontal_header, {
                'versionMarker': 255,
                'version': 0,
                'orientation': 1,
                'sortIndicatorOrder': 1,
                'sortIndicatorSection': 0,
                'sortIndicatorShown': True,
                'visualIndices': (), 
                'logicalIndices': (), 
                'sectionsHidden': (), 
                'hiddenSectionSize': {}, 
                'length': 837, 
                'sectionCount': 10, 
                'movableSections': True, 
                'clickableSections': True, 
                'highlightSelected': True, 
                'stretchLastSection': False, 
                'cascadingResizing': False, 
                'stretchSections': 0, 
                'contentsSections': 0,
                'defaultSectionSize': 125, 
                'minimumSectionSize': -1, 
                'defaultAlignment': 132, 
                'globalResizeMode': 0, 
                'sectionItems': [
                    {'size': 84, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 94, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 86, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 54, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 50, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 92, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 45, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 139, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 104, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0},
                    {'size': 89, 'tmpDataStreamSectionCount': 1, 'resizeMode': 0}
                ],
                'resizeContentsPrecision': 1000, 
                'customDefaultSectionSize': False, 
                'lastSectionSize': 0
            })

    def test_alternating_row_colors(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertFalse(table_item.alternating_row_colors)
            table_item.alternating_row_colors = True
            self.assertTrue(table_item.alternating_row_colors)
            table_item.alternating_row_colors = False
            self.assertFalse(table_item.alternating_row_colors)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertFalse(table_item.alternating_row_colors)
            table_item.alternating_row_colors = True
            self.assertTrue(table_item.alternating_row_colors)
            table_item.alternating_row_colors = False
            self.assertFalse(table_item.alternating_row_colors)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertFalse(table_item.alternating_row_colors)
            table_item.alternating_row_colors = True
            self.assertTrue(table_item.alternating_row_colors)
            table_item.alternating_row_colors = False
            self.assertFalse(table_item.alternating_row_colors)
            with self.assertRaises(ValueError):
                table_item.alternating_row_colors = "False"

    def test_columns(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(len(table_item.columns), 2)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(len(table_item.columns), 7)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertEqual(len(table_item.columns), 10)
            count = 0
            for column in table_item.columns:
                self.assertIsInstance(column, bjason.TableGraphicsItem.ColumnInfo)
                count += 1
            self.assertEqual(count, 10)   

    def test_horizontal_header_visible(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertFalse(table_item.horizontal_header_visible)
            table_item.horizontal_header_visible = True
            self.assertTrue(table_item.horizontal_header_visible)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertTrue(table_item.horizontal_header_visible)
            table_item.horizontal_header_visible = False
            self.assertFalse(table_item.horizontal_header_visible)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertTrue(table_item.horizontal_header_visible)
            table_item.horizontal_header_visible = False
            self.assertFalse(table_item.horizontal_header_visible)
            with self.assertRaises(ValueError):
                table_item.horizontal_header_visible = "True"

    def test_page_split(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertTrue(table_item.page_split)
            table_item.page_split = False
            self.assertFalse(table_item.page_split)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertTrue(table_item.page_split)
            table_item.page_split = False
            self.assertFalse(table_item.page_split)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertTrue(table_item.page_split)
            table_item.page_split = False
            self.assertFalse(table_item.page_split)
            with self.assertRaises(ValueError):
                table_item.page_split = "True"

    def test_vertical_header_visible(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertFalse(table_item.vertical_header_visible)
            table_item.vertical_header_visible = True
            self.assertTrue(table_item.vertical_header_visible)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertTrue(table_item.vertical_header_visible)
            table_item.vertical_header_visible = False
            self.assertFalse(table_item.vertical_header_visible)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertTrue(table_item.vertical_header_visible)
            table_item.vertical_header_visible = False
            self.assertFalse(table_item.vertical_header_visible)
            with self.assertRaises(ValueError):
                table_item.vertical_header_visible = "True"


    def test_column_label(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertFalse(table_item.column_label)
            table_item.column_label = True
            self.assertTrue(table_item.column_label)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertFalse(table_item.column_label)
            table_item.column_label = True
            self.assertTrue(table_item.column_label)
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertFalse(table_item.column_label)
            table_item.column_label = True
            self.assertTrue(table_item.column_label)
            with self.assertRaises(ValueError):
                table_item.column_label = "False"

    def test_header_font(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            font = table_item.header_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8.1 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle )
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            table_item.header_font = font 
            self.assertEqual(table_item.header_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(table_item.header_font, font)
            table_item.header_font = font 
            self.assertEqual(table_item.header_font, font)

    def test_body_font(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            font = table_item.body_font
            self.assertEqual(font['family'],'MS Shell Dlg 2' )
            self.assertEqual(font['point_size'], 8.1 )
            self.assertEqual(font['pixel_size'], -1 )
            self.assertEqual(font['style_hint'], bjason.Font.FontStyleHint.AnyStyle ) 
            self.assertEqual(font['weight'], bjason.Font.FontWeight.Normal )
            self.assertEqual(font['style'], bjason.Font.FontStyle.Normal )
            self.assertFalse(font['underline'])
            self.assertFalse(font['strike_out'])
            self.assertFalse(font['fixed_pitch'])
            self.assertFalse(font['dummy1'])

            table_item.body_font = font 
            self.assertEqual(table_item.body_font, font)

            font['family'] = 'Times New Roman'
            self.assertNotEqual(table_item.body_font, font)
            table_item.body_font = font 
            self.assertEqual(table_item.body_font, font)

    def test_visual_column_ids(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            ColID = bjason.NMRParamTableGraphicsItem.ColumnID
            self.assertEqual(table_item.visual_column_ids, (ColID.NAME, ColID.VALUE))
            table_item.visual_column_ids = (ColID.VALUE,)
            self.assertEqual(table_item.visual_column_ids, (ColID.VALUE,))
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            ColID = bjason.NMRPeakTableGraphicsItem.ColumnID
            self.assertEqual(table_item.visual_column_ids, (ColID.TYPE, ColID.POS0, ColID.WIDTH0, ColID.HEIGHT, ColID.VOLUME))
            table_item.visual_column_ids = table_item.visual_column_ids
            self.assertEqual(table_item.visual_column_ids, (ColID.TYPE, ColID.POS0, ColID.WIDTH0, ColID.HEIGHT, ColID.VOLUME))
            table_item.visual_column_ids = (ColID.POS0, ColID.WIDTH0, ColID.HEIGHT, ColID.VOLUME, ColID.TYPE)
            self.assertEqual(table_item.visual_column_ids, (ColID.POS0, ColID.WIDTH0, ColID.HEIGHT, ColID.VOLUME, ColID.TYPE))
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            ColID = bjason.NMRMultipletTableGraphicsItem.ColumnID
            self.assertEqual(table_item.visual_column_ids, (ColID.POS0, ColID.START0, ColID.END0, ColID.OFFSET, ColID.SLOPE, ColID.NORMALIZED, ColID.TYPE, ColID.J, ColID.SUM_INTEGRAL, ColID.PEAKS_VOLUME))
            table_item.visual_column_ids = table_item.visual_column_ids
            self.assertEqual(table_item.visual_column_ids, (ColID.POS0, ColID.START0, ColID.END0, ColID.OFFSET, ColID.SLOPE, ColID.NORMALIZED, ColID.TYPE, ColID.J, ColID.SUM_INTEGRAL, ColID.PEAKS_VOLUME))
            table_item.visual_column_ids = (ColID.POS0, ColID.START0, ColID.END0, ColID.TYPE, ColID.J, ColID.SUM_INTEGRAL, ColID.PEAKS_VOLUME, ColID.NORMALIZED)
            self.assertEqual(table_item.visual_column_ids, (ColID.POS0, ColID.START0, ColID.END0, ColID.TYPE, ColID.J, ColID.SUM_INTEGRAL, ColID.PEAKS_VOLUME, ColID.NORMALIZED))

    def test_custom_columns(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(len(table_item.customized_columns), 0)
            table_item.customized_columns.append([
                {'CustomTitle': 'My Column', 'Digits': 3, 'TextAlignment': bjason.Alignment.Right | bjason.Alignment.VCenter},
                {'Type': bjason.NMRPeakTableGraphicsItem.ColumnID.POS0, 'Digits': 5, 'TextAlignment': bjason.Alignment.HCenter | bjason.Alignment.VCenter}
            ])
            self.assertEqual(len(table_item.customized_columns), 2)
            col_info = table_item.customized_columns[0]
            self.assertEqual(col_info.digits, 3)
            self.assertEqual(col_info.text_alignment, bjason.Alignment.Right | bjason.Alignment.VCenter)
            self.assertIsNone(col_info.col_id)
            self.assertIsNone(col_info.custom_id)
            self.assertEqual(col_info.custom_title, 'My Column')
            col_info = table_item.customized_columns[1]
            self.assertEqual(col_info.digits, 5)
            self.assertEqual(col_info.text_alignment, bjason.Alignment.HCenter | bjason.Alignment.VCenter)
            self.assertEqual(col_info.col_id, bjason.NMRPeakTableGraphicsItem.ColumnID.POS0)
            self.assertIsNone(col_info.custom_id)
            self.assertIsNone(col_info.custom_title)

    def test_get_custom_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(table_item.get_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -1), 34.75)
            self.assertEqual(table_item.get_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -1), 35.56)
            self.assertEqual(table_item.get_custom_value(b'{01dce07b-a457-42ce-995e-be786113792f}', -1), 34.75)
            self.assertEqual(table_item.get_custom_value(b'{6e829454-0451-4ad3-90a5-5054002a5176}', -1), 35.56)
            self.assertIsNone(table_item.get_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -2))
            with self.assertRaises(bjason.utils.InvalidUUIDError):
                table_item.get_custom_value('test', -1)

    def test_set_custom_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.TableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(len(table_item.custom_rows), 2)
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}'])
            # Test replacing existing values
            table_item.set_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -1, 11.11)
            self.assertEqual(table_item.get_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -1), 11.11)
            self.assertIsNone(table_item.get_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -2))
            table_item.set_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -1, 22.22)
            self.assertEqual(table_item.get_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -1), 22.22)
            self.assertIsNone(table_item.get_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -3))
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}'])
            self.assertEqual(len(table_item.custom_rows), 2)
            # Test adding rows
            table_item.set_custom_value('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1, 33.33)
            self.assertEqual(table_item.get_custom_value('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1), 33.33)
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}', '{966aec7a-92bc-4de7-8727-8ed87fbb9910}'])
            self.assertEqual(len(table_item.custom_rows), 3)
            table_item.set_custom_value('{715ea92e-c8de-4382-90af-00564d2db33d}', -1, 44.44)
            self.assertEqual(table_item.get_custom_value('{715ea92e-c8de-4382-90af-00564d2db33d}', -1), 44.44)
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}', '{966aec7a-92bc-4de7-8727-8ed87fbb9910}', '{715ea92e-c8de-4382-90af-00564d2db33d}'])
            self.assertEqual(len(table_item.custom_rows), 4)
            # Test adding columns to the exiting rows
            table_item.set_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -2, 55.55)
            self.assertEqual(table_item.get_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -2), 55.55)
            self.assertEqual(table_item.get_custom_value('{01dce07b-a457-42ce-995e-be786113792f}', -1), 11.11)
            table_item.set_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -3, 66.66)
            self.assertEqual(table_item.get_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -3), 66.66)
            self.assertEqual(table_item.get_custom_value('{6e829454-0451-4ad3-90a5-5054002a5176}', -1), 22.22)
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}', '{966aec7a-92bc-4de7-8727-8ed87fbb9910}', '{715ea92e-c8de-4382-90af-00564d2db33d}'])
            self.assertEqual(len(table_item.custom_rows), 4)
            # Test adding both rows and columns
            table_item.set_custom_value('{4d11b87b-01b3-4f9b-91c3-5c57691d2141}', -4, 77.77)
            self.assertEqual(table_item.get_custom_value('{4d11b87b-01b3-4f9b-91c3-5c57691d2141}', -4), 77.77)
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}', '{966aec7a-92bc-4de7-8727-8ed87fbb9910}', '{715ea92e-c8de-4382-90af-00564d2db33d}', '{4d11b87b-01b3-4f9b-91c3-5c57691d2141}'])
            self.assertEqual(len(table_item.custom_rows), 5)
            # Test non-UUID-like row_id
            with self.assertRaises(bjason.utils.InvalidUUIDError):
                table_item.set_custom_value('test', -1, 88.88)
            self.assertEqual(len(table_item.custom_rows), 5)

    def test_append_custom_row(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}'])
            self.assertEqual(len(table_item.custom_rows), 2)
            # Test appending a row
            table_item.append_custom_row('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', [11.11])
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}', '{966aec7a-92bc-4de7-8727-8ed87fbb9910}'])
            self.assertEqual(len(table_item.custom_rows), 3)
            self.assertEqual(table_item.get_custom_value('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1), 11.11)
            # Test appending a row with a non-UUID-like row_id
            with self.assertRaises(bjason.utils.InvalidUUIDError):
                table_item.append_custom_row('test', [22.22])
            self.assertEqual(len(table_item.custom_rows), 3)

            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertEqual(len(table_item.custom_row_keys), 0)
            self.assertEqual(len(table_item.custom_rows), 0)
            table_item.customized_columns.append((
                {'Type': -1, 'Digits': 2, 'CustomTitle': 'Test Column 1'},
                {'Type': -2, 'Digits': 2, 'CustomTitle': 'Test Column 2'},
                ))
            self.assertEqual(len(table_item.customized_columns), 2)
            self.assertEqual(len(table_item.custom_rows), 0)
            table_item.append_custom_row('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', [11.11, 22.22])
            table_item.append_custom_row('{5638220f-4622-4c6c-a5ca-6ef9c98b6ec2}', [33.33, 44.44])
            self.assertEqual(len(table_item.custom_row_keys), 2)
            self.assertEqual(len(table_item.custom_rows), 2)
            self.assertEqual(table_item.get_custom_value('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1), 11.11)
            self.assertEqual(table_item.get_custom_value('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -2), 22.22)
            self.assertEqual(table_item.get_custom_value('{5638220f-4622-4c6c-a5ca-6ef9c98b6ec2}', -1), 33.33)
            self.assertEqual(table_item.get_custom_value('{5638220f-4622-4c6c-a5ca-6ef9c98b6ec2}', -2), 44.44)

            table_item.customized_columns.append({'Type': -3, 'Digits': -1, 'CustomTitle': 'Test String Column'})
            self.assertEqual(len(table_item.customized_columns), 3)
            self.assertEqual(len(table_item.custom_rows), 2)
            table_item.append_custom_row('{5df8c99a-d8b0-4476-bfa8-669720113a23}', [11.11, 22.22, 'Test String 1'])
            self.assertEqual(len(table_item.custom_row_keys), 3)
            self.assertEqual(len(table_item.custom_rows), 3)
            self.assertEqual(table_item.get_custom_row('{5df8c99a-d8b0-4476-bfa8-669720113a23}'), [11.11, 22.22, 'Test String 1'])
            self.assertEqual(table_item.get_custom_value('{5df8c99a-d8b0-4476-bfa8-669720113a23}', -1), 11.11)
            self.assertEqual(table_item.get_custom_value('{5df8c99a-d8b0-4476-bfa8-669720113a23}', -2), 22.22)
            self.assertEqual(table_item.get_custom_value('{5df8c99a-d8b0-4476-bfa8-669720113a23}', -3), 'Test String 1')

    def test_get_custom_row(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(list(table_item.custom_row_keys), ['{01dce07b-a457-42ce-995e-be786113792f}', '{6e829454-0451-4ad3-90a5-5054002a5176}'])
            self.assertEqual(len(table_item.custom_rows), 2)
            self.assertEqual(table_item.get_custom_row('{01dce07b-a457-42ce-995e-be786113792f}'), [34.75])
            self.assertEqual(table_item.get_custom_row('{6e829454-0451-4ad3-90a5-5054002a5176}'), [35.56])
            self.assertEqual(table_item.get_custom_row('{966aec7a-92bc-4de7-8727-8ed87fbb9910}'), [None])

    def test_custom_font(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            # Test for existinf row
            self.assertIsNone(table_item.get_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -1))
            font1 = table_item.body_font
            font2 = table_item.body_font
            font2['weight'] = bjason.Font.FontWeight.Bold
            table_item.set_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -1, font1)
            self.assertEqual(table_item.get_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -1), font1)
            self.assertIsNone(table_item.get_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -2))
            table_item.set_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -2, font2)
            self.assertEqual(table_item.get_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -2), font2)
            self.assertEqual(table_item.get_custom_font('{01dce07b-a457-42ce-995e-be786113792f}', -1), font1)
            # Test for non-existing row
            self.assertIsNone(table_item.get_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1))
            table_item.set_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1, font1)
            self.assertEqual(table_item.get_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1), font1)
            self.assertIsNone(table_item.get_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -2))
            table_item.set_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -2, font2)
            self.assertEqual(table_item.get_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -2), font2)
            self.assertEqual(table_item.get_custom_font('{966aec7a-92bc-4de7-8727-8ed87fbb9910}', -1), font1)
            
    def test_show_title(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertFalse(table_item.show_title)
            table_item.show_title = True
            self.assertTrue(table_item.show_title)
            table_item.show_title = False
            self.assertFalse(table_item.show_title)
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables(parameters+multiplets).jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRMultipletTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertTrue(table_item.show_title)
            table_item.show_title = False
            self.assertFalse(table_item.show_title)
            table_item.show_title = True
            self.assertTrue(table_item.show_title)
            table_item = bjason.NMRParamTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertFalse(table_item.show_title)
            table_item.show_title = True
            self.assertTrue(table_item.show_title)
            table_item.show_title = False
            self.assertFalse(table_item.show_title)

    def test_title(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(table_item.title, '')
            table_item.title = 'Test Peak Table'
            self.assertEqual(table_item.title, 'Test Peak Table')
            table_item.title = 'Peak Table'
            self.assertEqual(table_item.title, 'Peak Table')
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables(parameters+multiplets).jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRMultipletTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            html_string = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\\2610"; }
li.checked::marker { content: "\\2612"; }
</style></head><body style=" font-family:'Segoe UI'; font-size:10.8pt; font-weight:700; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial'; font-size:14pt;">Integral/Multiplet Table from #1</span></p></body></html>"""
            self.assertEqual(table_item.title, html_string)
            table_item.title = 'Test Multiplet Table'
            self.assertEqual(table_item.title, 'Test Multiplet Table')
            self.assertIsNone(table_item.title_plain_text)
            table_item.title = 'Multiplet Table'
            self.assertEqual(table_item.title, 'Multiplet Table')
            table_item = bjason.NMRParamTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            html_string = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
li.unchecked::marker { content: "\\2610"; }
li.checked::marker { content: "\\2612"; }
</style></head><body style=" font-family:'Segoe UI'; font-size:10.8pt; font-weight:700; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Parameters Report from #1</p></body></html>"""
            self.assertEqual(table_item.title, html_string)
            table_item.title = 'Test Param Table'
            self.assertEqual(table_item.title, 'Test Param Table')
            table_item.title = 'Param Table'
            self.assertEqual(table_item.title, 'Param Table')

    def test_title_plain_text(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertIsNone(table_item.title_plain_text)
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables(parameters+multiplets).jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRMultipletTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(table_item.title_plain_text, 'Integral/Multiplet Table from #1')
            table_item.title = 'Test Multiplet Table'
            self.assertIsNone(table_item.title_plain_text)
            table_item = bjason.NMRParamTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(table_item.title_plain_text, 'Parameters Report from #1')
            table_item.title = 'Test Param Table'
            self.assertIsNone(table_item.title_plain_text)

    def test_show_grid(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertTrue(table_item.show_grid)
            table_item.show_grid = False
            self.assertFalse(table_item.show_grid)
            table_item.show_grid = True
            self.assertTrue(table_item.show_grid)
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables(parameters+multiplets).jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRMultipletTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertTrue(table_item.show_grid)
            table_item.show_grid = False
            self.assertFalse(table_item.show_grid)
            table_item.show_grid = True
            self.assertTrue(table_item.show_grid)
            table_item = bjason.NMRParamTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertFalse(table_item.show_grid)
            table_item.show_grid = True
            self.assertTrue(table_item.show_grid)
            table_item.show_grid = False
            self.assertFalse(table_item.show_grid)

class NMRPeakTableGraphicsItemTestCase(unittest.TestCase):
    """NMRPeakTableGraphicsItem class test cases"""

    def test_data_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRPeakTableGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(table_item.data_id, '{ca3908a5-0246-4ec9-ac55-f863eb380478}')

class NMRMultipletTableGraphicsItemTestCase(unittest.TestCase):
    """NMRMultipletTableGraphicsItem class test cases"""

    def test_data_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRMultipletTableGraphicsItem(h5_file['/JasonDocument/Items/3'])
            self.assertEqual(table_item.data_id, '{ca3908a5-0246-4ec9-ac55-f863eb380478}')           

class AssignmentTableGraphicsItemTestCase(unittest.TestCase):
    """AssignmentTableGraphicsItem class test cases"""

    def test_data_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            table_item = bjason.AssignmentTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(table_item.data_id, '{9659aa0a-b0c8-493b-aa83-fe491191817a}')           

class NMRParamTableGraphicsItemTestCase(unittest.TestCase):
    """NMRParamTableGraphicsItem class test cases"""

    def test_data_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(table_item.data_id, '{ca3908a5-0246-4ec9-ac55-f863eb380478}')
    
    def test_param_list(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(len(table_item.param_list), 32)
            count = 0
            for param in table_item.param_list:
                self.assertIsInstance(param, bjason.NMRParamTableGraphicsItem.Parameter)
                count += 1
            self.assertEqual(count, 32)
            uuid = '{a3ec3407-7a50-4dc9-8c89-e504370849b8}'
            table_item.param_list.append({"name": "test param 1", "value": 111, "id": uuid})
            self.assertEqual(len(table_item.param_list), 33)
            count = 0
            for param in table_item.param_list:
                self.assertIsInstance(param, bjason.NMRParamTableGraphicsItem.Parameter)
                count += 1
            self.assertEqual(count, 33)
            param = table_item.param_list[32]
            self.assertEqual(param.name, 'test param 1')
            self.assertEqual(param.value, 111)
            self.assertEqual(param.id, uuid)
            self.assertIsNone(param.value_template)
            self.assertIsNone(param.condition)

            table_item.param_list.append([
                {"name": "test param 2", "value": '222', "id": '{51cf2041-aa24-420e-b75b-314d75cf50bc}'},
                {"name": "test param 3", "value": 33.3, "id": '{e6101390-62be-497d-97e9-e2837c86f3a3}'},
            ])
            self.assertEqual(len(table_item.param_list), 35)
            count = 0
            for param in table_item.param_list:
                self.assertIsInstance(param, bjason.NMRParamTableGraphicsItem.Parameter)
                count += 1
            self.assertEqual(count, 35)
            param = table_item.param_list[33]
            self.assertEqual(param.name, 'test param 2')
            self.assertEqual(param.value, '222')
            param = table_item.param_list[34]
            self.assertEqual(param.name, 'test param 3')
            self.assertEqual(param.value, 33.3)

class NMRParamTableGraphicsItem_ParameterTestCase(unittest.TestCase):
    """NMRParamTableGraphicsItem_Parameter class test cases"""

    def test_condition(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/0'])
            self.assertIsNone(table_item.condition)
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/20'])
            self.assertEqual(table_item.condition, 'jason_parameters/is2D')

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/0'])
            self.assertEqual(table_item.id, '{fdfab289-af4a-457d-8f15-a23305c43dc7}')

    def test_name(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/0'])
            self.assertEqual(table_item.name, 'Filename')

    def test_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/0'])
            self.assertEqual(table_item.value, 'Ethylindanone_Proton-13-1.jdf')
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/8'])
            self.assertEqual(table_item.value, 8)
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/19'])
            self.assertEqual(table_item.value, '45 °')

    def test_value_template(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.NMRParamTableGraphicsItem.Parameter(h5_file['/JasonDocument/Items/1/ParamsTable/list/0'])
            self.assertEqual(table_item.value_template, 'jason_parameters/OrigFilename.filename.str')

class TableGraphicsItem_ColumnInfoTestCase(unittest.TestCase):

    def test_digits(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/1/ModelInfo/ColInfo/0'])
            self.assertEqual(table_item.digits, -1)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/0'])
            self.assertEqual(table_item.digits, 3)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/3/ModelInfo/ColInfo/4'])
            self.assertEqual(table_item.digits, 4)

    def test_col_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/1/ModelInfo/ColInfo/1'])
            self.assertEqual(table_item.col_id, 1)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/0'])
            self.assertEqual(table_item.col_id, 0)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/3/ModelInfo/ColInfo/4'])
            self.assertEqual(table_item.col_id, 10)

        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/7'])
            self.assertEqual(table_item.col_id, -1)

    def test_units(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/1/ModelInfo/ColInfo/0'])
            self.assertEqual(table_item.units, bjason.Units.NONE)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/2'])
            self.assertEqual(table_item.units, bjason.Units.HZ)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/3/ModelInfo/ColInfo/2'])
            self.assertEqual(table_item.units, bjason.Units.PPM)

    def test_text_alignment(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/1/ModelInfo/ColInfo/0'])
            self.assertEqual(table_item.text_alignment, bjason.Alignment.Left | bjason.Alignment.VCenter)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/0'])
            self.assertEqual(table_item.text_alignment, bjason.Alignment.Left | bjason.Alignment.VCenter)
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/3/ModelInfo/ColInfo/4'])
            self.assertEqual(table_item.text_alignment, bjason.Alignment.Left | bjason.Alignment.VCenter)

    def test_custom_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/7'])
            self.assertEqual(table_item.custom_id, '{94d881bf-e240-42a0-bcc8-d8bdb3ba6af5}')
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/6'])
            self.assertIsNone(table_item.custom_id)

    def test_custom_title(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/7'])
            self.assertEqual(table_item.custom_title, 'Custom Column')
            table_item = bjason.TableGraphicsItem.ColumnInfo(h5_file['/JasonDocument/Items/2/ModelInfo/ColInfo/6'])
            self.assertIsNone(table_item.custom_title)

class MoleculeGraphicsItemTestCase(unittest.TestCase):
    """MoleculeGraphicsItem class test cases"""
    
    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(mol_item.id, '{c962da5e-188d-41b5-8cc3-ca3900792817}')

    def test_active_atom_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(mol_item.active_atom_type, bjason.Molecule.Atom.Type.C)

    def test_active_bond_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(mol_item.active_bond_type, 1)

    def test_browse_edit_mode(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(mol_item.browse_edit_mode, bjason.MoleculeGraphicsItem.EditMode.Shift)  

    def test_user_edit_mode(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(mol_item.user_edit_mode, bjason.MoleculeGraphicsItem.EditMode.Auto)

    def test_draw_style(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r+') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertIsInstance(mol_item.draw_style, bjason.MoleculeGraphicsItem.DrawStyle)
            draw_style = mol_item.draw_style

            # Test atoms_in_color
            self.assertTrue(draw_style.atoms_in_color)
            draw_style.atoms_in_color = False
            self.assertFalse(draw_style.atoms_in_color)

            # Test dra_internal_c
            self.assertFalse(draw_style.draw_internal_c)
            draw_style.draw_internal_c = True
            self.assertTrue(draw_style.draw_internal_c)

            # Test draw_terminal_c
            self.assertTrue(draw_style.draw_terminal_c)
            draw_style.draw_terminal_c = False
            self.assertFalse(draw_style.draw_terminal_c)
            draw_style.draw_terminal_c = 1
            self.assertTrue(draw_style.draw_terminal_c)
            draw_style.draw_terminal_c = []
            self.assertFalse(draw_style.draw_terminal_c)

            # Test draw_labels
            self.assertTrue(draw_style.draw_labels)
            draw_style.draw_labels = False
            self.assertFalse(draw_style.draw_labels)

            # Test labels
            LabelType = bjason.MoleculeGraphicsItem.DrawStyle.LabelType
            self.assertEqual(draw_style.labels, LabelType.C13Calc)
            draw_style.labels = LabelType.None_
            self.assertEqual(draw_style.labels, LabelType.None_)
            draw_style.labels = LabelType.H1Calc
            self.assertEqual(draw_style.labels, LabelType.H1Calc)

    def test_editor(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertIsInstance(mol_item.editor, bjason.MoleculeGraphicsItem.Editor)
            editor = mol_item.editor
            self.assertFalse(editor.allow_edit)
            self.assertFalse(editor.allow_modify_atoms)
            self.assertFalse(editor.allow_modify_bonds)
            
    def test_geometry(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertIsInstance(mol_item.draw_style, bjason.MoleculeGraphicsItem.DrawStyle)
            geometry = mol_item.geometry
            self.assertEqual(geometry.auto_scale, 1.0)
            self.assertEqual(geometry.user_scale, 1.0)
            transform = geometry.transform
            self.assertEqual(transform.angle, 0.0)
            self.assertEqual(transform.scale_x, 1.0)
            self.assertEqual(transform.scale_y, 1.0)
            self.assertEqual(transform.shift_x, 0.0)
            self.assertEqual(transform.shift_y, 0.0)

    def test_items(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(len(mol_item.items), 1)
            item = mol_item.items[0]
            self.assertEqual(item.user_scale, 1.0)
            self.assertEqual(item.auto_scale, 1.0)
            self.assertEqual(item.bond_len_scale, np.float32(13.019073))
            self.assertEqual(item.id, '{9659aa0a-b0c8-493b-aa83-fe491191817a}')
            transform = item.transform
            self.assertEqual(transform.angle, 0.0)
            self.assertEqual(transform.scale_x, np.float32(13.019073))
            self.assertEqual(transform.scale_y, np.float32(-13.019073))
            self.assertEqual(transform.shift_x, np.float32(64.88093))
            self.assertEqual(transform.shift_y, np.float32(1324.5134))

    def test_mol_data_list(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(len(mol_item.mol_data_list), 1)
            mol_data = mol_item.mol_data_list[0]
            self.assertIsInstance(mol_data, bjason.Molecule)
            self.assertEqual(mol_data.id, '{9659aa0a-b0c8-493b-aa83-fe491191817a}')

        with h5py.File(datafile_copy_path('Ethylindanone_molecule.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(len(mol_item.mol_data_list), 1)
            mol_data = mol_item.mol_data_list[0]
            self.assertIsInstance(mol_data, bjason.Molecule)
            self.assertEqual(mol_data.id, '{97e9f53f-815b-4d52-8295-b23e9bf6192a}')

    def test_mol_data(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol_item = bjason.MoleculeGraphicsItem(h5_file['/JasonDocument/Items/0'])
            mol = mol_item.mol_data()
            self.assertIsInstance(mol, bjason.Molecule)
            self.assertEqual(mol.id, '{9659aa0a-b0c8-493b-aa83-fe491191817a}')

            mol = mol_item.mol_data(0)
            self.assertIsInstance(mol, bjason.Molecule)
            self.assertEqual(mol.id, '{9659aa0a-b0c8-493b-aa83-fe491191817a}')

            mol = mol_item.mol_data('{9659aa0a-b0c8-493b-aa83-fe491191817a}')
            self.assertIsInstance(mol, bjason.Molecule)
            self.assertEqual(mol.id, '{9659aa0a-b0c8-493b-aa83-fe491191817a}')

            mol = mol_item.mol_data(1)
            self.assertIsNone(mol)

            mol = mol_item.mol_data('{97e9f53f-815b-4d52-8295-b23e9bf6192a}')
            self.assertIsNone(mol)

class ImageGraphicsItemTestCase(unittest.TestCase):
    """ImageGraphicsItem class test cases"""

    def test_image_id(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image_item = bjason.ImageGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(image_item.image_id, '{c67e0726-702e-4ec2-a179-6eb9e6b8c91c}')
    
    def test_image(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image_item = bjason.ImageGraphicsItem(h5_file['/JasonDocument/Items/0'])
            image = image_item.image
            self.assertEqual(image.id, image_item.image_id)

class TextGraphicsItemTestCase(unittest.TestCase):
    """TextGraphicsItem class test cases"""

    def test_text_id(self):
        with h5py.File(datafile_copy_path('lorem_ipsum.jjh5'), 'r') as h5_file:
            text_item = bjason.TextGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(text_item.text_id, '{10944f23-fb9a-4cc2-989f-871d51ffb17b}')

    def test_text(self):
        with h5py.File(datafile_copy_path('lorem_ipsum.jjh5'), 'r') as h5_file:
            text_item = bjason.TextGraphicsItem(h5_file['/JasonDocument/Items/0'])
            self.assertEqual(text_item.text_id, text_item.text.id)

class NMRMultipletReportGraphicsItemTestCase(unittest.TestCase):
    """NMRMultipletReportGraphicsItem class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_multiplet_reports.jjh5'), 'r') as h5_file:
            item = bjason.NMRMultipletReportGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(item.id, '{45ba918a-5b82-427a-90b0-75d1016c2958}')

    def test_spectrum_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_multiplet_reports.jjh5'), 'r') as h5_file:
            item = bjason.NMRMultipletReportGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.spectrum_id, '{46b8cb0d-c7cc-490f-84ed-1b3ea6809425}')

    def test_journal_format(self):
        formats = ["JACS", "Angew. Chem.", "Wiley"]
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_multiplet_reports.jjh5'), 'r') as h5_file:
            for i in range(3):
                item = bjason.NMRMultipletReportGraphicsItem(h5_file['/JasonDocument/Items/{}'.format(i+1)])
                self.assertEqual(item.journal_format, formats[i])

    def test_report_text(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_multiplet_reports.jjh5'), 'r') as h5_file:
            item = bjason.NMRMultipletReportGraphicsItem(h5_file['/JasonDocument/Items/1'])
            self.assertEqual(item.report_text, '1H NMR (400 MHz, CHLOROFORM-D) δ 7.71 - 7.76 (m, 20H), 7.54 - 7.60 (m, 26H), 7.42 - 7.47 (m, 24H), 7.32 - 7.38 (m, 26H), 7.25 (s, 1H), 3.30 (dddd, J = 0.7, 1.4, 7.9, 17.2 Hz, 32H), 2.77 - 2.85 (m, 32H), 2.60 (dddd, J = 3.9, 4.5, 8.0, 9.1 Hz, 27H), 1.96 (dqd, J = 4.5, 7.5, 13.7 Hz, 32H), 1.53 (ddq, J = 7.3, 9.1, 13.7 Hz, 32H), 1.27 (s, 0H), 1.11 - 1.14 (m, 1H), 1.00 (t, J = 7.4 Hz, 95H), 0.88 - 0.93 (m, 1H).')

    def test_journal_template(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_multiplet_reports.jjh5'), 'r') as h5_file:
            item = bjason.NMRMultipletReportGraphicsItem(h5_file['/JasonDocument/Items/1'])
            journal_template = item.journal_template
            self.assertEqual(journal_template.js, ', J = %J Hz')
            self.assertEqual(journal_template.js_separator, ', ')
            self.assertEqual(journal_template.multiplet, '%RANGE (%TYPE%JS, %COUNT%ELEMENT)')
            self.assertEqual(journal_template.multiplet_separator, ', ')
            self.assertEqual(journal_template.report, '%NUC NMR (%FREQ MHz, %SOLVENT) δ %MULTIPLETS.')

class ChartGraphicsItemTestCase(unittest.TestCase):
    """ChartGraphicsItem class test cases"""

    def test_gridlines_color(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.gridlines_color, '#E2E2E2FF')

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.gridlines_color = '#FF0000FF'
            self.assertEqual(item.gridlines_color, '#FF0000FF')

    def test_show_gridlines(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertTrue(item.show_gridlines)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.show_gridlines = False
            self.assertFalse(item.show_gridlines)

    def test_title(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.title, 'Chart Title')

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.title = 'Sum Integral vs Peak Area'
            self.assertEqual(item.title, 'Sum Integral vs Peak Area')

    # test_title_font
    def test_title_font(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.title_font, {
                'family': 'Segoe UI',
                'point_size': 9,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Normal,
                'style': bjason.Font.FontStyle.Normal,
                'underline': 0,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0
            })

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            font = item.title_font
            # modify the original font
            font['family'] = 'Times New Roman'
            font['point_size'] = 14
            font['weight'] = bjason.Font.FontWeight.Bold
            font['style'] = bjason.Font.FontStyle.Italic
            font['underline'] = 1
            item.title_font = font # set the modified font
            font = item.title_font
            self.assertEqual(font, {
                'family': 'Times New Roman',
                'point_size': 14,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Bold,
                'style': bjason.Font.FontStyle.Italic,
                'underline': 1,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0
            })

    def test_legend_alignment(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.legend_alignment, 32)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.legend_alignment = 24
            self.assertEqual(item.legend_alignment, 24)

    def test_horizontal_axis_ticks(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.horizontal_axis_ticks, 5)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.horizontal_axis_ticks = 10
            self.assertEqual(item.horizontal_axis_ticks, 10)

    def test_vertical_axis_ticks(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.vertical_axis_ticks, 5)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.vertical_axis_ticks = 10
            self.assertEqual(item.vertical_axis_ticks, 10)

    def test_horizontal_axis_minor_ticks(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.horizontal_axis_minor_ticks, 0)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.horizontal_axis_minor_ticks = 2
            self.assertEqual(item.horizontal_axis_minor_ticks, 2)

    def test_vertical_axis_minor_ticks(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.vertical_axis_minor_ticks, 0)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.vertical_axis_minor_ticks = 2
            self.assertEqual(item.vertical_axis_minor_ticks, 2)

    def test_horizontal_axis_color(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.horizontal_axis_color, '#000000FF')

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.horizontal_axis_color = '#FF0000FF'
            self.assertEqual(item.horizontal_axis_color, '#FF0000FF')

    def test_vertical_axis_color(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.vertical_axis_color, '#000000FF')

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.vertical_axis_color = '#FF0000FF'
            self.assertEqual(item.vertical_axis_color, '#FF0000FF')

    def test_horizontal_axis_title(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.horizontal_axis_title, 'Axis Title')

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.horizontal_axis_title = 'Pos (ppm)'
            self.assertEqual(item.horizontal_axis_title, 'Pos (ppm)')

    def test_vertical_axis_title(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.vertical_axis_title, 'Axis Title')

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.vertical_axis_title = 'Integral'
            self.assertEqual(item.vertical_axis_title, 'Integral')

    def test_horizontal_axis_title_font(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.horizontal_axis_title_font, {
                'family': 'MS Shell Dlg 2',
                'point_size': 9,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Bold,
                'style': bjason.Font.FontStyle.Normal,
                'underline': 0,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0})
            
        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            font = item.horizontal_axis_title_font
            # modify the original font
            font['family'] = 'Times New Roman'
            font['point_size'] = 14
            font['weight'] = bjason.Font.FontWeight.Normal
            font['style'] = bjason.Font.FontStyle.Italic
            font['underline'] = 1
            item.horizontal_axis_title_font = font

    def test_vertical_axis_title_font(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.vertical_axis_title_font, {
                'family': 'MS Shell Dlg 2',
                'point_size': 9,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Bold,
                'style': bjason.Font.FontStyle.Normal,
                'underline': 0,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0})
            
        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            font = item.vertical_axis_title_font
            # modify the original font
            font['family'] = 'Times New Roman'
            font['point_size'] = 14
            font['weight'] = bjason.Font.FontWeight.Normal
            font['style'] = bjason.Font.FontStyle.Italic
            font['underline'] = 1
            item.vertical_axis_title_font = font

    def test_horizontal_axis_font(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.horizontal_axis_font, {
                'family': 'MS Shell Dlg 2',
                'point_size': 9,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Normal,
                'style': bjason.Font.FontStyle.Normal,
                'underline': 0,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0})
            
        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            font = item.horizontal_axis_font
            # modify the original font
            font['family'] = 'Times New Roman'
            font['point_size'] = 14
            font['weight'] = bjason.Font.FontWeight.Bold
            font['style'] = bjason.Font.FontStyle.Italic
            font['underline'] = 1
            item.horizontal_axis_font = font

    def test_vertical_axis_font(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(item.vertical_axis_font, {
                'family': 'MS Shell Dlg 2',
                'point_size': 9,
                'pixel_size': -1,
                'style_hint': bjason.Font.FontStyleHint.AnyStyle,
                'weight': bjason.Font.FontWeight.Normal,
                'style': bjason.Font.FontStyle.Normal,
                'underline': 0,
                'strike_out': 0,
                'fixed_pitch': 0,
                'dummy1': 0})
            
        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            font = item.vertical_axis_font
            # modify the original font
            font['family'] = 'Times New Roman'
            font['point_size'] = 14
            font['weight'] = bjason.Font.FontWeight.Bold
            font['style'] = bjason.Font.FontStyle.Italic
            font['underline'] = 1
            item.vertical_axis_font = font

    def test_show_legend(self):
        # test getter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertTrue(item.show_legend)

        # test setter
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            item.show_legend = False
            self.assertFalse(item.show_legend)

    def test_series(self):
        # test getters
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            self.assertEqual(len(item.series), 4)
            series = item.series[0]
            self.assertEqual(series.id, '{c031e359-88e7-4b3f-9630-3a53179bb53f}')
            self.assertEqual(series.data_id, '{9e9a649f-2516-4198-82fa-91a2e5d259e4}')
            self.assertEqual(series.error_series_id, '{c05ed675-0317-4837-bfc4-337513f5495e}')
            self.assertEqual(series.name, 'Sum Integral')
            self.assertEqual(series.color, '#FF50D985')
            self.assertTrue(series.is_visible)
            self.assertFalse(series.is_error_series)
            self.assertFalse(series.show_error_bars_x)
            self.assertFalse(series.show_error_bars_y)
            self.assertEqual(series.source, bjason.ChartGraphicsItem.Series.Source.TABLE)
            self.assertEqual(series.type, bjason.ChartGraphicsItem.Series.Type.SCATTER)
            self.assertEqual(series.marker_shape, bjason.ChartGraphicsItem.Series.MarkerShape.CIRCLE)
            self.assertEqual(series.marker_size, 15)
            self.assertIsNone(series.parent_series_id)
            self.assertIsNone(series.parent_series_x_column_id)
            self.assertIsNone(series.parent_series_y_column_id)
            self.assertTrue((series.y == np.array(
                [26786.886900235757,
                 34294.21405132428,
                 32255.74547368148,
                 35028.51931039212,
                 42396.78670101551,
                 42301.67161864693,
                 36689.372013090826,
                 42555.39803316322,
                 4591.508448122837,
                 42545.087300142135,
                 475.7042452711641,
                 910.2675633166511,
                 126959.97089429486,
                 780.3491080941554],np.float64)).all())
            self.assertTrue((series.x == np.array(
                [7.733486189160735,
                 7.563311111051674,
                 7.447292882391571,
                 7.34650668969232,
                 3.303840042601149,
                 2.809046462956531,
                 2.6029619303555074,
                 1.9603950632803198,
                 1.8403508067261058,
                 1.5254291096796173,
                 1.265452137778759,
                 1.1326579543230357,
                 0.9958706387332069,
                 0.8971713371765205],np.float64)).all())
            
            series = item.series[1]
            self.assertEqual(series.id, '{c05ed675-0317-4837-bfc4-337513f5495e}')
            self.assertEqual(series.data_id, '{9e9a649f-2516-4198-82fa-91a2e5d259e4}')
            self.assertIsNone(series.error_series_id)
            self.assertEqual(series.name, 'ErrorSeries')
            self.assertEqual(series.color, '#FFA903F7')
            self.assertFalse(series.is_visible)
            self.assertTrue(series.is_error_series)
            self.assertFalse(series.show_error_bars_x)
            self.assertFalse(series.show_error_bars_y)
            self.assertEqual(series.source, bjason.ChartGraphicsItem.Series.Source.TABLE)
            self.assertEqual(series.type, bjason.ChartGraphicsItem.Series.Type.SCATTER)
            self.assertEqual(series.marker_shape, bjason.ChartGraphicsItem.Series.MarkerShape.CIRCLE)
            self.assertEqual(series.marker_size, 15)
            self.assertEqual(series.parent_series_id, '{c031e359-88e7-4b3f-9630-3a53179bb53f}')
            self.assertEqual(series.parent_series_x_column_id, 1)
            self.assertEqual(series.parent_series_y_column_id, 10)
            self.assertTrue((series.x == np.array([0.0]*14,np.float64)).all())
            self.assertTrue((series.y == np.array(
                [2.0748803624288894,
                2.535226808615356,
                2.146696667689361,
                2.425212249413643,
                3.0358875417474227,
                2.8716621248286507,
                2.9239735675705014,
                3.5256631506282923,
                3.1341616575231637,
                3.734459930843555,
                1.2063393844365347,
                1.2795161387212188,
                2.4500868720468283,
                1.6518482321569667],np.float64)).all())
            
            series = item.series[2]
            self.assertEqual(series.id, '{25d9438b-883c-4308-b531-274785a1a3cd}')
            self.assertEqual(series.data_id, '{9e9a649f-2516-4198-82fa-91a2e5d259e4}')
            self.assertEqual(series.error_series_id, '{e65b987f-f45f-4888-b8dc-ee13b2c6f875}')
            self.assertEqual(series.name, 'Peaks Area')
            self.assertEqual(series.color, '#FF41FFF9')
            self.assertTrue(series.is_visible)
            self.assertFalse(series.is_error_series)
            self.assertFalse(series.show_error_bars_x)
            self.assertFalse(series.show_error_bars_y)
            self.assertEqual(series.source, bjason.ChartGraphicsItem.Series.Source.TABLE)
            self.assertEqual(series.type, bjason.ChartGraphicsItem.Series.Type.SCATTER)
            self.assertEqual(series.marker_shape, bjason.ChartGraphicsItem.Series.MarkerShape.PENTAGON)
            self.assertEqual(series.marker_size, 15)
            self.assertIsNone(series.parent_series_id)
            self.assertIsNone(series.parent_series_x_column_id)
            self.assertIsNone(series.parent_series_y_column_id)
            self.assertTrue((series.y == np.array(
                [25213.501503562093,
                 34858.20629074832,
                 31967.211740921673,
                 33829.38587262333,
                 45860.132310998844,
                 44431.36957603144,
                 32703.993211768357,
                 39015.07610680448,
                 1339.475553579976,
                 39126.12351626353,
                 490.3676126593857,
                 770.3505451835895,
                 119683.76949835557,
                 811.3587763543799],np.float64)).all())
            self.assertTrue((series.x == np.array(
                [7.733486189160735,
                 7.563311111051674,
                 7.447292882391571,
                 7.34650668969232,
                 3.303840042601149,
                 2.809046462956531,
                 2.6029619303555074,
                 1.9603950632803198,
                 1.8403508067261058,
                 1.5254291096796173,
                 1.265452137778759,
                 1.1326579543230357,
                 0.9958706387332069,
                 0.8971713371765205],np.float64)).all())
            
            series = item.series[3]
            self.assertEqual(series.id, '{e65b987f-f45f-4888-b8dc-ee13b2c6f875}')
            self.assertEqual(series.data_id, '{9e9a649f-2516-4198-82fa-91a2e5d259e4}')
            self.assertIsNone(series.error_series_id)
            self.assertEqual(series.name, 'ErrorSeries')
            self.assertEqual(series.color, '#FFEBA3BF')
            self.assertFalse(series.is_visible)
            self.assertTrue(series.is_error_series)
            self.assertFalse(series.show_error_bars_x)
            self.assertFalse(series.show_error_bars_y)
            self.assertEqual(series.source, bjason.ChartGraphicsItem.Series.Source.TABLE)
            self.assertEqual(series.type, bjason.ChartGraphicsItem.Series.Type.SCATTER)
            self.assertEqual(series.marker_shape, bjason.ChartGraphicsItem.Series.MarkerShape.CIRCLE)
            self.assertEqual(series.marker_size, 15)
            self.assertEqual(series.parent_series_id, '{25d9438b-883c-4308-b531-274785a1a3cd}')
            self.assertEqual(series.parent_series_x_column_id, 1)
            self.assertEqual(series.parent_series_y_column_id, 12)
            self.assertTrue((series.x == np.array([0.0]*14,np.float64)).all())
            self.assertTrue((series.y == np.array([0.0]*14,np.float64)).all())

        # test setters 
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            
            series = item.series[0]
            series.name = 'Integrals'
            self.assertEqual(series.name, "Integrals")
            series.color = '#FF0000FF'
            self.assertEqual(series.color, '#FF0000FF')
            series.is_visible = False
            self.assertFalse(series.is_visible)
            series.type = bjason.ChartGraphicsItem.Series.Type.LINE
            self.assertEqual(series.type, bjason.ChartGraphicsItem.Series.Type.LINE)
            series.marker_shape = bjason.ChartGraphicsItem.Series.MarkerShape.STAR
            self.assertEqual(series.marker_shape, bjason.ChartGraphicsItem.Series.MarkerShape.STAR)
            series.marker_size = 10
            self.assertEqual(series.marker_size, 10)
            series.show_error_bars_x = True
            self.assertTrue(series.show_error_bars_x)
            series.show_error_bars_y = True
            self.assertTrue(series.show_error_bars_y)

    def test_add_series(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1 (chart sum integral vs peak area).jjh5'), 'r+') as h5_file:
            item = bjason.ChartGraphicsItem(h5_file['/JasonDocument/Items/2'])
            series = item.add_series('{9e9a649f-2516-4198-82fa-91a2e5d259e4}',
                                     bjason.NMRMultipletTableGraphicsItem.ColumnID.POS0,
                                     bjason.NMRMultipletTableGraphicsItem.ColumnID.NORMALIZED)
            self.assertIsInstance(series, bjason.ChartGraphicsItem.Series)
            self.assertIsNotNone(series.id)
            self.assertEqual(series.data_id, '{9e9a649f-2516-4198-82fa-91a2e5d259e4}')
            self.assertIsNone(series.parent_series_id)
            self.assertIsNone(series.parent_series_x_column_id)
            self.assertIsNone(series.parent_series_y_column_id)
            self.assertEqual(series.name, '')
            self.assertEqual(series.color, '')
            self.assertTrue(series.is_visible)
            self.assertFalse(series.is_error_series)
            self.assertFalse(series.show_error_bars_x)
            self.assertFalse(series.show_error_bars_y)
            self.assertEqual(series.source, bjason.ChartGraphicsItem.Series.Source.TABLE)
            self.assertEqual(series.type, bjason.ChartGraphicsItem.Series.Type.SCATTER)
            self.assertEqual(series.marker_shape, bjason.ChartGraphicsItem.Series.MarkerShape.CIRCLE)
            self.assertEqual(series.marker_size, 15)
            self.assertEqual(series.x.size, 0)
            self.assertEqual(series.y.size, 0)

if __name__ == '__main__':
    unittest.main()
