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
import os
import beautifuljason as bjason
from beautifuljason.tests.config import datafile_path, datafile_copy_path, newfile_path

class DocumentTestCase(unittest.TestCase):
    """Document class test cases"""

    @classmethod
    def setUpClass(cls):
        cls.jason = bjason.JASON()

    def test___init__(self):
        """Testing Document.__init__()"""

        # Existing documents
        with bjason.Document(datafile_copy_path('empty.jjh5')) as doc:
            self.assertTrue('JasonDocument' in doc.h5_file)
            self.assertEqual(len(doc.items), 0)
            doc.h5_file.create_group('TestGroup')
            self.assertTrue('TestGroup' in doc.h5_file)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 0)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.items), 1)
            self.assertEqual(len(doc.nmr_items), 1)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 1)

        # Existing document in read-only mode
        with bjason.Document(datafile_copy_path('empty.jjh5'), mode='r') as doc:
            self.assertTrue('JasonDocument' in doc.h5_file)
            self.assertEqual(len(doc.items), 0)
            with self.assertRaises(ValueError):
                doc.h5_file.create_group('TestGroup')
            self.assertFalse('TestGroup' in doc.h5_file)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 0)

        # New document
        with bjason.Document(newfile_path('new_doc.jjh5')) as doc:
            self.assertTrue('JasonDocument' in doc.h5_file)
            self.assertEqual(len(doc.items), 0)
            doc.h5_file.create_group('TestGroup')
            self.assertTrue('TestGroup' in doc.h5_file)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 0)

        # New temporary document
        with bjason.Document(newfile_path('new_temp_doc.jjh5'), is_temporary=True) as doc:
            self.assertTrue('JasonDocument' in doc.h5_file)
            self.assertEqual(len(doc.items), 0)
            doc.h5_file.create_group('TestGroup')
            self.assertTrue('TestGroup' in doc.h5_file)
            self.assertTrue(os.path.isfile(doc.file_name))
            doc_copy_name = newfile_path('copy_doc.jjh5')
            doc.close()
            doc.copy(doc_copy_name)
        self.assertTrue(len(doc.file_name) > 0)
        self.assertFalse(os.path.isfile(doc.file_name))
        with self.jason.create_document(doc_copy_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 0)

    def test_close(self):
        """Testing Document.close()"""

        # New document
        doc = bjason.Document(newfile_path('new_doc.jjh5'))
        self.assertTrue('JasonDocument' in doc.h5_file)
        doc.close()
        self.assertFalse('JasonDocument' in doc.h5_file)

        # New temporary document
        doc = bjason.Document(newfile_path('new_doc.jjh5'), is_temporary=True)
        self.assertTrue('JasonDocument' in doc.h5_file)
        doc.close()
        self.assertFalse('JasonDocument' in doc.h5_file)

    def test_remove(self):
        """Testing Document.remove()"""

        # New document
        doc = bjason.Document(newfile_path('new_doc.jjh5'))
        self.assertTrue(os.path.isfile(doc.file_name))
        doc.remove()
        self.assertTrue(os.path.isfile(doc.file_name))

        # New temporary document
        doc = bjason.Document(newfile_path('new_doc.jjh5'), is_temporary=True)
        self.assertTrue(os.path.isfile(doc.file_name))
        doc.remove()
        self.assertFalse(os.path.isfile(doc.file_name))

    def test_copy(self):
        """Testing Document.copy()"""

        orig_path = datafile_copy_path('empty.jjh5')
        with bjason.Document(orig_path) as doc:
            doc.h5_file.create_group('TestGroup')
            copy_path = newfile_path('copy.jjh5')
            doc.close()
            doc.copy(copy_path)
        with open(orig_path, 'rb') as orig_f, open(copy_path, 'rb') as copy_f:
            orig_b = orig_f.read()
            copy_b = copy_f.read()
            self.assertGreater(orig_b.find(b'TestGroup'), -1)
            self.assertEqual(orig_b, copy_b)

    def test_create_nmrpeaks_table(self):
        """Testing Document.create_nmrpeaks_table()"""

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.items), 1)
            spec_item = doc.items[0]
            new_item1 = doc.create_nmrpeaks_table(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item1, bjason.NMRPeakTableGraphicsItem)
            self.assertEqual(len(doc.items), 2)
            self.assertEqual(len(new_item1.columns), 0)
            new_item2 = doc.create_nmrpeaks_table(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item2, bjason.NMRPeakTableGraphicsItem)
            self.assertEqual(len(doc.items), 3)
            self.assertEqual(len(new_item1.columns), 0)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 3)

    def test_create_nmrmultiplets_table(self):
        """Testing Document.create_nmrintegrals_table()"""

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.items), 1)
            spec_item = doc.items[0]
            new_item1 = doc.create_nmrmultiplets_table(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item1, bjason.NMRMultipletTableGraphicsItem)
            self.assertEqual(len(doc.items), 2)
            new_item2 = doc.create_nmrmultiplets_table(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item2, bjason.NMRMultipletTableGraphicsItem)
            self.assertEqual(len(doc.items), 3)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 3)

    def test_create_nmrparams_table(self):
        """Testing Document.create_nmrparams_table()"""

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.items), 1)
            spec_item = doc.items[0]
            new_item1 = doc.create_nmrparams_table(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item1, bjason.NMRParamTableGraphicsItem)
            self.assertEqual(len(doc.items), 2)
            new_item2 = doc.create_nmrparams_table(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item2, bjason.NMRParamTableGraphicsItem)
            self.assertEqual(len(doc.items), 3)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 3)

    def test_create_nmrassignments_table(self):
        """Testing Document.create_nmrassignments_table()"""

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5')) as doc:
            self.assertEqual(len(doc.items), 1)
            mol_item = doc.items[0]
            table_item1 = doc.create_nmrassignments_table(mol_item, mol_item.mol_data())
            self.assertIsInstance(table_item1, bjason.AssignmentTableGraphicsItem)
            self.assertEqual(len(doc.items), 2)
            self.assertEqual(len(table_item1.columns), 0)
            table_item2 = doc.create_nmrassignments_table(mol_item, mol_item.mol_data())
            self.assertIsInstance(table_item2, bjason.AssignmentTableGraphicsItem)
            self.assertEqual(len(doc.items), 3)
            self.assertEqual(len(table_item2.columns), 0)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 3)

    def test_create_nmrmultiplet_report(self):
        """Testing Document.create_nmrmultiplet_report()"""

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.items), 1)
            spec_item = doc.items[0]
            new_item1 = doc.create_nmrmultiplet_report(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item1, bjason.NMRMultipletReportGraphicsItem)
            self.assertEqual(len(doc.items), 2)
            new_item2 = doc.create_nmrmultiplet_report(spec_item, spec_item.spec_data(0))
            self.assertIsInstance(new_item2, bjason.NMRMultipletReportGraphicsItem)
            self.assertEqual(len(doc.items), 3)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 3)
            
    def test_create_text_item(self):
        """Testing Document.create_text()"""

        with bjason.Document(newfile_path('create_text.jjh5')) as doc:
            self.assertEqual(len(doc.items), 0)
            new_item1 = doc.create_text_item()
            self.assertEqual(doc.h5_file['/JasonDocument/Items'].attrs['.container_type'], 9)
            self.assertIsInstance(new_item1, bjason.TextGraphicsItem)
            self.assertEqual(len(doc.items), 1)
            new_item2 = doc.create_text_item('test text')
            self.assertEqual(new_item2.text.html, 'test text')
            self.assertIsInstance(new_item2, bjason.TextGraphicsItem)
            self.assertEqual(len(doc.items), 2)
        with self.jason.create_document(doc.file_name) as temp_doc:
            self.assertEqual(len(temp_doc.items), 2)

    def test_create_image_data(self):
        """Testing Document.create_image_data()"""

        with bjason.Document(newfile_path('create_image.jjh5')) as doc:
            self.assertEqual(len(doc.items), 0)
            try:
                new_image1 = doc.create_image_data(datafile_path('jason_logo.png'))
            except AssertionError:
                new_image1 = None
            else:
                self.assertIsInstance(new_image1, bjason.Image)
                self.assertEqual(new_image1.depth, 32)
                self.assertEqual(len(doc.image_data), 1)
                self.assertEqual(len(doc.items), 0)
                new_image2 = doc.create_image_data(datafile_path('jason_logo.png'))
                self.assertIsInstance(new_image2, bjason.Image)
                self.assertEqual(len(doc.image_data), 2)
                self.assertEqual(len(doc.items), 0)
        if new_image1:
            with self.jason.create_document(doc.file_name) as temp_doc:
                self.assertEqual(len(temp_doc.items), 0)
                self.assertEqual(len(temp_doc.image_data), 2)

    def test_create_image_item(self):
        """Testing Document.create_image_item()"""

        with bjason.Document(newfile_path('create_image_item.jjh5')) as doc:
            self.assertEqual(len(doc.items), 0)
            try:
                new_image = doc.create_image_data(datafile_path('jason_logo.png'))
            except AssertionError:
                new_image = None
            else:
                self.assertIsInstance(new_image, bjason.Image)
                self.assertEqual(len(doc.image_data), 1)
                for i in range(10):
                    new_item = doc.create_image_item(new_image.id)
                    self.assertIsInstance(new_item, bjason.ImageGraphicsItem)
                    self.assertEqual(len(doc.items), i + 1)
        if new_image:
            with self.jason.create_document(doc.file_name) as temp_doc:
                self.assertEqual(len(temp_doc.items), 10)
                self.assertEqual(len(temp_doc.image_data), 1)

    def test_nmr_items(self):
        """Testing Document.nmr_items"""

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.nmr_items), 1)
            self.assertIsInstance(doc.nmr_items[0], bjason.NMRSpectrumGraphicsItem)

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5')) as doc:
            self.assertEqual(len(doc.nmr_items), 0)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton+Carbon+HMQC.jjh5')) as doc:
            self.assertEqual(len(doc.nmr_items), 3)
            for nmr_item in doc.nmr_items:
                self.assertIsInstance(nmr_item, bjason.NMRSpectrumGraphicsItem)

    def test_mol_items(self):
        """Testing Document.mol_items"""

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5')) as doc:
            self.assertEqual(len(doc.mol_items), 1)
            self.assertIsInstance(doc.mol_items[0], bjason.MoleculeGraphicsItem)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5')) as doc:
            self.assertEqual(len(doc.mol_items), 0)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton+Carbon+HMQC.jjh5')) as doc:
            self.assertEqual(len(doc.mol_items), 0)

    def test_items_by_type(self):
        """Testing Document.items_by_type"""

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5')) as doc:
            items = doc.items_by_type(bjason.GraphicsItem.Type.Molecule)
            self.assertEqual(len(items), 1)
            self.assertIsInstance(items[0], bjason.MoleculeGraphicsItem)
            items = doc.items_by_type(bjason.MoleculeGraphicsItem)
            self.assertEqual(len(items), 1)
            self.assertIsInstance(items[0], bjason.MoleculeGraphicsItem)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton+Carbon+HMQC.jjh5')) as doc:
            items = doc.items_by_type(bjason.GraphicsItem.Type.NMRSpectrum)
            self.assertEqual(len(items), 3)
            for item in items:
                self.assertIsInstance(item, bjason.NMRSpectrumGraphicsItem)
            items = doc.items_by_type(bjason.NMRSpectrumGraphicsItem)
            self.assertEqual(len(items), 3)
            for item in items:
                self.assertIsInstance(item, bjason.NMRSpectrumGraphicsItem)

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5')) as doc:
            items = doc.items_by_type(bjason.GraphicsItem.Type.AssignmentTable)
            self.assertEqual(len(items), 1)
            self.assertIsInstance(items[0], bjason.AssignmentTableGraphicsItem)

    def test_nmr_data(self):
        """Testing Document.nmr_data"""

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.nmr_data), 1)
            self.assertIsInstance(doc.nmr_data[0], bjason.NMRSpectrum)

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.nmr_data), 0)
        
        with bjason.Document(datafile_copy_path('Ethylindanone_Proton+Carbon+HMQC.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.nmr_data), 3)
            for nmr_data in doc.nmr_data:
                self.assertIsInstance(nmr_data, bjason.NMRSpectrum)

    def test_mol_data(self):
        """Testing Document.mol_data"""

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.mol_data), 1)
            self.assertIsInstance(doc.mol_data[0], bjason.Molecule)

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.mol_data), 1)
            self.assertIsInstance(doc.mol_data[0], bjason.Molecule)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.mol_data), 0)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton+Carbon+HMQC.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.mol_data), 0)

    def test_image_data(self):
        """Testing Document.image_data"""

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.image_data), 0)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.image_data), 0)

        with bjason.Document(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.image_data), 2)
            for image in doc.image_data:
                self.assertIsInstance(image, bjason.Image)

    def test_text_data(self):
        """Testing Document.text_data"""

        with bjason.Document(datafile_copy_path('Ethylindanone_molecule.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.text_data), 0)

        with bjason.Document(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.text_data), 0)

        with bjason.Document(datafile_copy_path('lorem_ipsum.jjh5'), 'r') as doc:
            self.assertEqual(len(doc.text_data), 1)
            self.assertIsInstance(doc.text_data[0], bjason.Text)

    def test_create_chart_item(self):
        """Testing Document.create_chart_item()"""

        with bjason.Document(datafile_copy_path('cahe_Proton-14-1_with_peak_table.jjh5'), 'r+') as doc:
            chart_item = doc.create_chart_item()
            self.assertIsInstance(chart_item, bjason.ChartGraphicsItem)
            self.assertEqual(len(doc.items), 3)
            self.assertEqual(doc.items[2].id, chart_item.id)

            # add series
            series = chart_item.add_series(doc.items[1].id, bjason.NMRPeakTableGraphicsItem.ColumnID.POS0, bjason.NMRPeakTableGraphicsItem.ColumnID.VOLUME)
            self.assertEqual(len(chart_item.series), 1)
            self.assertEqual(chart_item.series[0].id, series.id)
            self.assertEqual(chart_item.series[0].x_column_id, bjason.NMRPeakTableGraphicsItem.ColumnID.POS0)
            self.assertEqual(chart_item.series[0].y_column_id, bjason.NMRPeakTableGraphicsItem.ColumnID.VOLUME)
            self.assertEqual(chart_item.series[0].data_id, doc.items[1].id)
            self.assertEqual(chart_item.series[0].source, bjason.ChartGraphicsItem.Series.Source.TABLE)

if __name__ == '__main__':
    unittest.main()
