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

class NMRSpecInfoTestCase(unittest.TestCase):
    """NMRSpecInfo class test cases"""
    def test_get_param(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/SpecInfo'], 1)
            self.assertEqual(spec_info.get_param('OrigFileFormat'), bjason.OriginalFileFormat.JEOL_Delta)
            self.assertEqual(spec_info.get_param('Spinrate'), 15.0)
            self.assertEqual(spec_info.get_param('Title'), b'Ethylindanone')
            self.assertEqual(spec_info.get_param('OrigFilename'), b'')
            self.assertEqual(spec_info.get_param('PulseProgram'), b'proton.jxp')
            self.assertTrue((spec_info.get_param('SpectrumType') == np.array([1,0,0,0,0,0,0,0], np.int8)).all())
            self.assertTrue((spec_info.get_param('SW') == np.array([5995.569755133393,10.0,10.0,10.0,10.0,10.0,10.0,10.0],np.float64)).all())
            self.assertIsNone(spec_info.get_param('TestDummyName'))

            raw_spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/RawData/SpecInfo'], 1)
            self.assertEqual(raw_spec_info.get_param('OrigFileFormat'), bjason.OriginalFileFormat.JEOL_Delta)
            self.assertEqual(raw_spec_info.get_param('OrigFilename'), b'C:/Users/larin/source/repos/jason/bjason/trunk/beautifuljason-base/tests/data/Ethylindanone_Proton-13-1.jdf')
            self.assertTrue((raw_spec_info.get_param('SW') == np.array([7494.00479616307,10.0,10.0,10.0,10.0,10.0,10.0,10.0],np.float64)).all())
            self.assertTrue((raw_spec_info.get_param('SpectrumType') == np.array([0,0,0,0,0,0,0,0], np.int8)).all())

        with h5py.File(datafile_copy_path('cahe_cpmg-1-1.jjh5'), 'r') as h5_file:
            raw_spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/SpecInfo'], 1)    
            self.assertTrue((raw_spec_info.get_param('lists').attrs['list[1]'] == np.array([0.1,0.256,0.484,0.784,1.156,1.6,2.116,2.704,3.364,4.096,4.9,5.776,6.724,7.744,8.836,10.0],np.float64)).all())

    def test_get_orig_param(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            raw_spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/RawData/SpecInfo'], 1)
            self.assertEqual(raw_spec_info.get_orig_param('parameters', 'AF_VERSION'), 4)
            self.assertIsNone(raw_spec_info.get_orig_param('Parameters', 'AF_VERSION'))
            self.assertEqual(raw_spec_info.get_orig_param('header', 'Annotation_Ok'), -128)
            self.assertEqual(raw_spec_info.get_orig_param('header', 'Author'), b'delta')
            self.assertTrue((raw_spec_info.get_orig_param('header', 'Base_Freq') == np.array([399.78219837825003,0.0,0.0,0.0,0.0,0.0,0.0,0.0],np.float64)).all())
            self.assertTrue((raw_spec_info.get_orig_param('header', 'Data_Points') == np.array([16384,1,1,1,1,1,1,1],np.int32)).all())
            self.assertTrue((raw_spec_info.get_orig_param('header', 'Data_Axis_Titles') == np.array(['Proton','','','','','','',''],np.str_)).all()) 
            self.assertEqual(raw_spec_info.get_orig_param('header', 'Node_Name'), b'XJSQKPBVHR')
            self.assertIsNone(raw_spec_info.get_orig_param('Parameters', 'AF'))
 
            self.assertEqual(raw_spec_info.get_orig_param('parameters', 'ACQ_DELAY'), 8.34E-6)
            self.assertEqual(raw_spec_info.get_orig_param('parameters', 'AF_VERSION'), 4)
            self.assertEqual(raw_spec_info.get_orig_param('parameters', 'EXPERIMENT'), b'proton.jxp')
            self.assertIsNone(raw_spec_info.get_orig_param('parameters', 'EXP'))

            self.assertEqual(raw_spec_info.get_orig_param('context', 'Other'), b'0')

            self.assertEqual(raw_spec_info.get_orig_param('ext_parameters', 'COMMENT_7.type'), 10013)
            self.assertTrue((raw_spec_info.get_orig_param('ext_parameters', 'PHASE') == np.array([0,90,270,180,180,270,90,0],np.int32)).all()) 
           
            phase_unts = raw_spec_info.get_orig_param ('ext_parameters','PHASE.unts')
            self.assertIsInstance(phase_unts, h5py.Group)
            self.assertTrue((phase_unts.attrs['0'] == np.array([0,0,0,0,0],np.int16)).all()) 
            self.assertTrue((phase_unts.attrs['7'] == np.array([0,0,0,0,0],np.int16)).all())

    def test_nuclides(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/SpecInfo'], 1)
            self.assertTupleEqual(spec_info.nuclides, ("1H",))
        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/SpecInfo'], 2)
            self.assertTupleEqual(spec_info.nuclides, ("1H","13C"))
        with h5py.File(datafile_copy_path('cahe_cpmg-1-1.jjh5'), 'r') as h5_file:
            spec_info = bjason.NMRSpecInfo(h5_file['/JasonDocument/NMR/NMRData/0/SpecInfo'], 2)
            self.assertTupleEqual(spec_info.nuclides, ("1H",""))

class NMREntryTestCase(unittest.TestCase):
    """NMREntry class test cases"""
    def test_ndim(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMREntry(h5_file['/JasonDocument/NMR/NMRData/0'])
            self.assertEqual(spec_data.ndim, 1)
            raw_spec_data = bjason.NMREntry(h5_file['/JasonDocument/NMR/NMRData/0/RawData'])
            self.assertEqual(raw_spec_data.ndim, 1)
        with h5py.File(datafile_copy_path('cahe_cpmg-1-1.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMREntry(h5_file['/JasonDocument/NMR/NMRData/0'])
            self.assertEqual(spec_data.ndim, 2) 
            raw_spec_data = bjason.NMREntry(h5_file['/JasonDocument/NMR/NMRData/0/RawData'])
            self.assertEqual(raw_spec_data.ndim, 2)  
        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMREntry(h5_file['/JasonDocument/NMR/NMRData/0'])
            self.assertEqual(spec_data.ndim, 2)
            raw_spec_data = bjason.NMREntry(h5_file['/JasonDocument/NMR/NMRData/0/RawData'])
            self.assertEqual(raw_spec_data.ndim, 2)

class NMRMultipletTestCase(unittest.TestCase):
    """NMRMultiplet class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.id, '{3ffe5ec4-1374-441a-a142-7b36f1b7b7fa}') 

    def test_show_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.show_type, bjason.NMRMultiplet.ShowType.Multiplet)

    def test_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.value, 3771.0250256384797)

    def test_value_hz_factor(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.value_hz_factor, 1.0)

        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.value_hz_factor, 0.22869887683603118)

    def test_value_hz(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.value_hz, 3771.0250256384797)

        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.value_hz, 3771.0250256384797 * 0.22869887683603118)

    def test_integral_scope(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.integral_scope, 0)

    def test_multiplets(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(len(multiplet.multiplets), 14)
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/13'])
            self.assertEqual(len(multiplet.multiplets), 14)

    def test_normalized_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.normalized_value, 1.0)

    def test_flags(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertEqual(multiplet.flags, 0)  


    def test_range(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            self.assertTrue((multiplet.range[0] == np.array([0.8811775014017011, 0.9074922006983013],np.float64)).all())
            self.assertTrue((multiplet.range[1] == np.array([0.0, 0.0],np.float64)).all())
            self.assertTrue((multiplet.range[2] == np.array([0.0, 0.0],np.float64)).all())

    def test_jtree(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0'])
            self.assertTrue((multiplet.jtree[0]['groups'] == np.array([1, 1],np.int32)).all())  
            self.assertTrue((multiplet.jtree[0]['positions'] == np.array([0.8981841188336421, 0.8906289389431479],np.float64)).all()) 
            self.assertTrue((multiplet.jtree[1]['groups'] == np.array([1],np.int32)).all())
            self.assertTrue((multiplet.jtree[1]['positions'] == np.array([0.894406528888395],np.float64)).all()) 
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10'])
            self.assertEqual(multiplet.jtree, [])

    def test_peaks(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            peaks = multiplet.peaks
            self.assertEqual(len(peaks), 2)
            self.assertEqual(peaks[0].h5_group.name, '/JasonDocument/NMR/NMRData/0/Peaks/PeakList/270' )
            self.assertEqual(peaks[1].h5_group.name, '/JasonDocument/NMR/NMRData/0/Peaks/PeakList/271' )
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10'])      
            peaks = multiplet.peaks
            self.assertEqual(len(peaks), 13)

    def test_all_peaks(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            peaks = multiplet.all_peaks
            self.assertEqual(len(peaks), 2)
            self.assertEqual(peaks[0].h5_group.name, '/JasonDocument/NMR/NMRData/0/Peaks/PeakList/270' )
            self.assertEqual(peaks[1].h5_group.name, '/JasonDocument/NMR/NMRData/0/Peaks/PeakList/271' )
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10'])      
            peaks = multiplet.all_peaks
            self.assertEqual(len(peaks), 20)

    def test_moments(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            self.assertTrue((multiplet.moments == np.array([0.8970667422371588, 1.1496990624096572, -1.9837083768425283, 4.935098924355247],np.float64)).all())

    def test_curve(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            self.assertEqual(multiplet.curve[0], 24.32395454376305)
            self.assertEqual(multiplet.curve[19], 2898.9320334784534)
            self.assertEqual(multiplet.curve[32], 3553.713632949247)
            self.assertEqual(multiplet.curve[46], 3771.0250256384797)
            self.assertEqual(len(multiplet.curve), 47)

    def test_pos(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10']) 
            self.assertTrue((multiplet.pos == np.array([7.346366802907818, 0.0, 0.0],np.float64)).all())

    def test_js(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/13']) 
            self.assertTrue((multiplet.js == np.array([0.6694162075499214, 1.597234238841186, 7.701234751932071],np.float64)).all())
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            self.assertTrue((multiplet.js == np.array([3.0204264257649402],np.float64)).all())
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10']) 
            self.assertEqual(multiplet.js.size, 0)
            self.assertEqual(multiplet.js.dtype.type, np.float64)

    def test_multiplicities(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/13']) 
            self.assertTrue((multiplet.multiplicities == np.array([2, 1, 1], np.int32)).all())
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            self.assertTrue((multiplet.multiplicities == np.array([1], np.int32)).all())
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10']) 
            self.assertEqual(multiplet.multiplicities.size, 0)
            self.assertEqual(multiplet.multiplicities.dtype.type, np.int32)

    def test_multiplicities_str(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/13']) 
            self.assertEqual(multiplet.multiplicities_str, 'ddt')
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/0']) 
            self.assertEqual(multiplet.multiplicities_str, 'd')
            multiplet = bjason.NMRMultiplet(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals/MultipletList/10']) 
            self.assertEqual(multiplet.multiplicities_str, 'm')

class NMRMultiplet_ListTestCase(unittest.TestCase):
    """NMRMultiplet.List class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.id, '{bc8ba87e-2f0d-43be-91fe-fc7c733b85b7}') 

    def test_pos_units(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertTupleEqual(multiplets.pos_units, (bjason.Units.PPM, bjason.Units.HZ, bjason.Units.HZ))

    def test_integral_lvl(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.integral_lvl, 0.0) 

    def test_integral_scale(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.integral_scale, 0.0011595154872406802)

    def test_integral_tlt(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.integral_tlt, 0.0) 

    def test_integral_total(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.integral_total, 540.5953233077786)  

    def test_integral_vscale(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.integral_vscale, 0.02) 

    def test_integral_scale_scoped(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables_v2.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertTrue((multiplets.integral_scale_scoped == np.array([0.0011595154872406802, 1.0, 1.0], np.float64)).all())

    def test_integral_vshift(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(multiplets.integral_vshift, 3.0) 

    def test_getitem(self):       
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            multiplet = multiplets[0]
            self.assertEqual(multiplet.id, '{3ffe5ec4-1374-441a-a142-7b36f1b7b7fa}') 
            multiplet = multiplets[10]
            self.assertEqual(multiplet.id, '{5765521c-927a-483b-8b2c-a3fdf55a4294}')
            multiplet = multiplets[6]
            self.assertEqual(multiplet.id, '{1fd264aa-fdd0-4e1a-a080-cae826bc6733}')
            with self.assertRaises(IndexError):
                multiplet = multiplets[14]
            multiplet = multiplets[-1]
            self.assertEqual(multiplet.id, '{02c86440-ca8e-4241-bac3-eb002464645a}')
            self.assertEqual(len(multiplets[0:10]), 10)
            self.assertEqual(len(multiplets[:10]), 10)
            self.assertEqual(len(multiplets[:]), 14)
            self.assertEqual(len(multiplets[:-1]), 13)
            multiplets2 = multiplets[-3:-1]
            self.assertEqual(len(multiplets2), 2)
            self.assertEqual(multiplets2[0].id, '{4fc0fff5-ba3e-4a02-b0ba-c616f7409772}')
            self.assertEqual(multiplets2[1].id, '{c1eddf22-1769-40e2-90b7-8dff191eae9a}')
            multiplets2 = multiplets[-1:-3:-1]
            self.assertEqual(len(multiplets2), 2)
            self.assertEqual(multiplets2[0].id, '{02c86440-ca8e-4241-bac3-eb002464645a}')
            self.assertEqual(multiplets2[1].id, '{c1eddf22-1769-40e2-90b7-8dff191eae9a}')

        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            with self.assertRaises(IndexError):
                multiplet = multiplets[0]

    def test_iter(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            count = 0
            for multiplet in multiplets:
                self.assertIsInstance(multiplet, bjason.NMRMultiplet)
                count += 1
            self.assertEqual(count, 14)

        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            count = 0
            for multiplet in multiplets:
                count += 1
            self.assertEqual(count, 0)

    def test_reversed(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            count = 0
            i = len(multiplets)- 1
            for multiplet in reversed(multiplets):
                self.assertIsInstance(multiplet, bjason.NMRMultiplet)
                self.assertEqual(multiplet.id, multiplets[i].id )
                i -= 1
                count += 1
            self.assertEqual(count, 14)
            
        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            count = 0
            for multiplet in reversed(multiplets):
                count += 1
            self.assertEqual(count, 0) 

    def test_len(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(len(multiplets), 14)

        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertEqual(len(multiplets), 0)

    def test_bool(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertTrue(multiplets)

        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertFalse(multiplets)

    def test_auto_baseline(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            multiplets = bjason.NMRMultiplet.List(h5_file['/JasonDocument/NMR/NMRData/0/Multiplets_Integrals'])
            self.assertFalse(multiplets.auto_baseline)

class NMRPeakTestCase(unittest.TestCase):
    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.id, '{6e829454-0451-4ad3-90a5-5054002a5176}') 

    def test_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.type, bjason.NMRPeak.PeakType.GenLorentz)

    def test_classification(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.classification, bjason.NMRPeak.PeakClassification.Contaminant)            
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/11'])
            self.assertEqual(peak.classification, bjason.NMRPeak.PeakClassification.Compound)
            peak.classification = bjason.NMRPeak.PeakClassification.C13Satellite
            self.assertEqual(peak.classification, bjason.NMRPeak.PeakClassification.C13Satellite)
            peak.classification = 3
            self.assertEqual(peak.classification, bjason.NMRPeak.PeakClassification.ReactionSolvent)
            peak.classification = '1'
            self.assertEqual(peak.classification, bjason.NMRPeak.PeakClassification.Contaminant)
            with self.assertRaises(ValueError):
                peak.classification = 127
            with self.assertRaises(ValueError):
                peak.classification = 'test'
            
    def test_height(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.height, 27.524930877389707)  

    def test_offset(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.offset, 0.0)

    def test_label(self):
         with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r+') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.label, '')
            peak.label = 'test'
            self.assertEqual(peak.label, 'test')
            peak.label = ''
            self.assertEqual(peak.label, '')

    def test_pos(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertTrue((peak.pos == np.array([8.248149187089048, 0.0, 0.0],np.float64)).all())
    
    def test_shape_par(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertTrue((peak.shape_par == np.array([0.0, 0.0, 0.0],np.float64)).all())

    def test_width(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertTrue((peak.width == np.array([0.002056943856753252, 0.0, 0.0],np.float64)).all())

    def test_area(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertIsNone(peak.area)

        with h5py.File(datafile_copy_path('cahe_Proton-14-1_with_peak_table.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.area, 5.044061571576702e10)

    def test_area_sigma(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertIsNone(peak.area_sigma)
            
        with h5py.File(datafile_copy_path('cahe_Proton-14-1_with_peak_table.jjh5'), 'r') as h5_file:
            peak = bjason.NMRPeak(h5_file['/JasonDocument/NMR/NMRData/0/Peaks/PeakList/0'])
            self.assertEqual(peak.area_sigma, 2.7084265141544642e9)

class NMRPeak_ListTestCase(unittest.TestCase):
    """NMRPeak.List class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            self.assertEqual(peaks.id, '{5b820c0e-152d-4236-9631-768f1748e097}') 
    
    def test_pos_units(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            self.assertTupleEqual(peaks.pos_units, (bjason.Units.PPM, bjason.Units.HZ, bjason.Units.HZ))

    def test_getitem(self):       
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            peak = peaks[0]
            self.assertEqual(peak.id, '{6e829454-0451-4ad3-90a5-5054002a5176}') 
            peak = peaks[276]
            self.assertEqual(peak.id, '{61a14173-9ce5-440a-a5c5-f542a13252c6}')
            peak = peaks[36]
            self.assertEqual(peak.id, '{4c04bc8a-cd11-4634-9fbe-b66cb33c89c6}')
            with self.assertRaises(IndexError):
                peak = peaks[277]
            peak = peaks[-1]
            self.assertEqual(peak.id, '{61a14173-9ce5-440a-a5c5-f542a13252c6}')
            self.assertEqual(len(peaks[0:10]), 10)
            self.assertEqual(len(peaks[:10]), 10)
            self.assertEqual(len(peaks[:]), 277)
            self.assertEqual(len(peaks[:-1]), 276)
            peaks2 = peaks[-3:-1]
            self.assertEqual(len(peaks2), 2)
            self.assertEqual(peaks2[0].id, '{702f1f2e-f3b5-4d50-8be2-945da267fcca}')
            self.assertEqual(peaks2[1].id, '{403f697f-9e8e-4fe9-93d6-44807f6653fa}')
            peaks2 = peaks[-1:-3:-1]
            self.assertEqual(len(peaks2), 2)
            self.assertEqual(peaks2[0].id, '{61a14173-9ce5-440a-a5c5-f542a13252c6}')
            self.assertEqual(peaks2[1].id, '{403f697f-9e8e-4fe9-93d6-44807f6653fa}')

        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            with self.assertRaises(IndexError):
                peak = peaks[0]

    def test_iter(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            count = 0
            for peak in peaks:
                self.assertIsInstance(peak, bjason.NMRPeak)
                count += 1
            self.assertEqual(count, 277)

        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            count = 0
            for peak in peaks:
                count += 1
            self.assertEqual(count, 0)

    def test_reversed(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            count = 0
            i = len(peaks)- 1
            for peak in reversed(peaks):
                self.assertIsInstance(peak, bjason.NMRPeak)
                self.assertEqual(peak.id, peaks[i].id )
                i -= 1
                count += 1
            self.assertEqual(count, 277)
            
        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            count = 0
            for peak in reversed(peaks):
                count += 1
            self.assertEqual(count, 0)

    def test_len(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            self.assertEqual(len(peaks), 277)

        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            self.assertEqual(len(peaks), 0)

    def test_bool(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            self.assertTrue(peaks)

        with h5py.File(datafile_copy_path('Ethylindanone_hsqc-2-1.jjh5'), 'r') as h5_file:
            peaks = bjason.NMRPeak.List(h5_file['/JasonDocument/NMR/NMRData/0/Peaks'])
            self.assertFalse(peaks)

class NMRProcessingTestCase(unittest.TestCase):
    """NMRProcessing class test cases"""

    def test_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0'])
            self.assertEqual(proc.type, bjason.NMRProcessing.Type.Apodize)
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/1'])
            self.assertEqual(proc.type, bjason.NMRProcessing.Type.ZF)
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2'])
            self.assertEqual(proc.type, bjason.NMRProcessing.Type.FT)
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/3'])
            self.assertEqual(proc.type, bjason.NMRProcessing.Type.Phase)
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/4'])
            self.assertEqual(proc.type, bjason.NMRProcessing.Type.PolyBC)

    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0'])
            self.assertEqual(proc.id, '{607ed261-0c32-45d1-abf1-5547a389dc2a}')

    def test_name(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/1'])
            self.assertEqual(proc.name, 'Zero Filling')
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/4'])
            self.assertEqual(proc.name, 'Polynomial Baseline Correction')

    def test_active(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            proc = bjason.NMRProcessing(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/1'])
            self.assertTrue(proc.active)

class NMRProcessing_ListTestCase(unittest.TestCase):
    """NMRProcessing.List class test cases"""

    def test_iter(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            procs = bjason.NMRProcessing.List(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate'])
            count = 0
            for proc in procs:
                self.assertIsInstance(proc, bjason.NMRProcessing)
                count += 1
            self.assertEqual(count, 5)

    def test_len(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            procs = bjason.NMRProcessing.List(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate'])
            self.assertEqual(len(procs), 5)

    def test_end_point_dim(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            procs = bjason.NMRProcessing.List(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate'])
            self.assertEqual(procs.end_point_dim, 0)

    def test_end_point_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            procs = bjason.NMRProcessing.List(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate'])
            self.assertEqual(procs.end_point_type, bjason.NMRProcessing.List.EndType.Full)

class NMRProcessing_ParameterTestCase(unittest.TestCase):
    """NMRProcessing.Parameter class test cases"""  

    def test_name(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.name, 'Interface')
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/4/Parameters/0'])
            self.assertEqual(param.name, 'Order') 
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/10'])
            self.assertEqual(param.name, '') 

    def test_value_type(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.value_type, bjason.base.QMetaType_Type.QStringList)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/4/Parameters/0'])
            self.assertEqual(param.value_type, bjason.base.QMetaType_Type.Int) 
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/10'])
            self.assertEqual(param.value_type, bjason.base.QMetaType_Type.Double) 

    def test_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.value, ['Basic mode', 'Expert mode'])
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/4/Parameters/0'])
            self.assertEqual(param.value, 4) 
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/10'])
            self.assertEqual(param.value, 0.0)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/0'])
            self.assertTrue(param.value)             

    def test_tip(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.tip, 'Edit parameters in basic (assisted) or expert (manual) mode')
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2/Parameters/6'])
            self.assertEqual(param.tip, 'First Point Multiplier') 
        
    def test_decimals(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.decimals, None)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2/Parameters/6'])
            self.assertEqual(param.decimals, 3) 

    def test_step(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.step, None)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2/Parameters/6'])
            self.assertEqual(param.step, 0.1) 

    def test_max_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.max_value, None)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2/Parameters/6'])
            self.assertEqual(param.max_value, 100.0) 

    def test_min_value(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.min_value, None)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2/Parameters/6'])
            self.assertEqual(param.min_value, 0.0)
    
    def test_current_index(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.current_index, 0)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/2/Parameters/6'])
            self.assertEqual(param.current_index, None)

    def test_units(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/13'])
            self.assertEqual(param.units, bjason.Units.NONE)
            param = bjason.NMRProcessing.Parameter(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0/Parameters/1'])
            self.assertEqual(param.units, bjason.Units.HZ)

class NMRProcessing_Parameter_ListTestCase(unittest.TestCase):
    """NMRProcessing.ParameterList class test cases"""  

    def test_len(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            params = bjason.NMRProcessing.Parameter.List(h5_file['/JasonDocument/NMR/NMRData/0/ProcessingTemplate/ProcessingSteps/0'])
            self.assertEqual(len(params), 15)

class NMRSpectrumTestCase(unittest.TestCase):
    """NMREntry class test cases"""
    def test_id(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMRSpectrum(h5_file['/JasonDocument/NMR/NMRData/0'])
            self.assertEqual(spec_data.id, '{46b8cb0d-c7cc-490f-84ed-1b3ea6809425}')

    def test_peaks(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMRSpectrum(h5_file['/JasonDocument/NMR/NMRData/0'])     
            self.assertEqual(len(spec_data.peaks), 277)
            count = 0
            for peak in spec_data.peaks:
                self.assertIsInstance(peak, bjason.NMRPeak)
                count += 1
            self.assertEqual(count, 277)

    def test_multiplets(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMRSpectrum(h5_file['/JasonDocument/NMR/NMRData/0'])     
            self.assertEqual(len(spec_data.multiplets), 14)
            count = 0
            for multiplet in spec_data.multiplets:
                self.assertIsInstance(multiplet, bjason.NMRMultiplet)
                count += 1
            self.assertEqual(count, 14)   

    def test_proc_list(self):
        with h5py.File(datafile_copy_path('Ethylindanone_Proton-13-1_with_tables.jjh5'), 'r') as h5_file:
            spec_data = bjason.NMRSpectrum(h5_file['/JasonDocument/NMR/NMRData/0'])     
            self.assertEqual(len(spec_data.proc_list), 5)
            count = 0
            for proc in spec_data.proc_list:
                self.assertIsInstance(proc, bjason.NMRProcessing)
                count += 1
            self.assertEqual(count, 5)

class MoleculeTestCase(unittest.TestCase):
    """Molecule class test cases"""
    
    def test_atoms(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol = bjason.Molecule(h5_file['/JasonDocument/Molecules/Molecules/0'])
            atoms = mol.atoms
            self.assertEqual(len(atoms), 12)
            atom = mol.atoms[0]
            self.assertIsInstance(atom, bjason.Molecule.Atom)
            self.assertEqual(atom.type, bjason.Molecule.Atom.Type.C)
            self.assertTrue((atom.bonded_atom_numbers == np.array([1, 5],np.int32)).all())
            self.assertTrue((atom.bonds == np.array([770, 769],np.int32)).all())
            self.assertEqual(atom.x, np.float32(3.0632))
            self.assertEqual(atom.y, np.float32(95.1319))
            self.assertIsNone(atom.z)
            self.assertIsNone(atom.valence)
            self.assertIsNone(atom.charge)
            self.assertIsNone(atom.isotope)
            self.assertEqual(atom.nh, 1)

            bonded_atoms = atom.bonded_atoms
            self.assertEqual(len(bonded_atoms), 2)
            atom = bonded_atoms[1]
            self.assertIsInstance(atom, bjason.Molecule.Atom)
            self.assertEqual(atom.type, bjason.Molecule.Atom.Type.C)
            self.assertTrue((atom.bonded_atom_numbers == np.array([0, 4],np.int32)).all())
            self.assertTrue((atom.bonds == np.array([769, 770],np.int32)).all())
            self.assertEqual(atom.x, np.float32(-2.1804))
            self.assertEqual(atom.y, np.float32(91.9292))
            self.assertIsNone(atom.z)
            self.assertIsNone(atom.valence)
            self.assertIsNone(atom.charge)
            self.assertIsNone(atom.isotope)
            self.assertEqual(atom.nh, 1)

    def test_rings(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol = bjason.Molecule(h5_file['/JasonDocument/Molecules/Molecules/0'])
            rings = mol.rings
            self.assertEqual(len(rings), 2)
            ring = rings[0]
            self.assertIsInstance(ring, bjason.Molecule.Ring)
            self.assertTrue(ring.is_aromatic)
            self.assertTrue((ring.atoms == np.array([5, 4, 3, 2, 1, 0],np.int32)).all())
            ring = rings[1]
            self.assertIsInstance(ring, bjason.Molecule.Ring)
            self.assertFalse(ring.is_aromatic)
            self.assertTrue((ring.atoms == np.array([2, 8, 7, 6, 1],np.int32)).all())

    def test_couplings(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol = bjason.Molecule(h5_file['/JasonDocument/Molecules/Molecules/0/'])
            couplings = mol.couplings
            self.assertEqual(len(couplings), 18)
            coupling = couplings[0]
            self.assertIsInstance(coupling, bjason.Molecule.Coupling)
            self.assertEqual(coupling.acount1, 1)
            self.assertEqual(coupling.acount2, 1)
            self.assertEqual(coupling.error_spheres, 1)
            self.assertFalse(coupling.ignored_auto)
            self.assertFalse(coupling.ignored_user)
            self.assertFalse(coupling.is_exchangeable1)
            self.assertFalse(coupling.is_exchangeable2)
            self.assertEqual(coupling.jvalue, 4)
            self.assertEqual(coupling.n1, 0)
            self.assertEqual(coupling.n2, 4)
            self.assertEqual(coupling.nucl1, bjason.Molecule.Atom.NuclType.H1)
            self.assertEqual(coupling.nucl2, bjason.Molecule.Atom.NuclType.H1)
            self.assertTrue((coupling.value == np.array([1.418558, 1.373256, 1.373256],np.float32)).all())
            self.assertTrue((coupling.value_error == np.array([-1.0, 0.800001, 0.800001],np.float32)).all())
            self.assertTrue((coupling.value_method == np.array([2, 4, 5],np.int32)).all())
            self.assertEqual(coupling.value_spheres, 1)
            coupling = couplings[12]
            self.assertEqual(coupling.mark1, 'dn')
            self.assertEqual(coupling.mark2, 'dn')

    def test_spectra(self):
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol = bjason.Molecule(h5_file['/JasonDocument/Molecules/Molecules/0/'])
            spectra = mol.spectra
            self.assertEqual(len(spectra), 2)
            spectrum = spectra[0]
            self.assertIsInstance(spectrum, bjason.Molecule.Spectrum)
            self.assertEqual(spectrum.origin, 1)
            self.assertEqual(spectrum.spec_type, bjason.Molecule.Spectrum.Type.STD)
            self.assertEqual(spectrum.nucleus, bjason.Molecule.Atom.NuclType.C13)
            shifts = spectrum.shifts
            self.assertEqual(len(shifts), 11)
            shift = shifts[0]
            self.assertIsInstance(shift, bjason.Molecule.Spectrum.Shift)
            self.assertEqual(shift.acount, 1)
            
            self.assertEqual(shift.error_spheres, 2)
            self.assertFalse(shift.ignored_auto)
            self.assertFalse(shift.ignored_user)
            self.assertFalse(shift.is_exchangeable)
            self.assertTrue((shift.nums == np.array([0],np.int32)).all())
            self.assertTrue((shift.value == np.array([124.77037, 123.8, 123.8],np.float32)).all())
            self.assertTrue((shift.value_error == np.array([-1.0, 2.9147792, 2.9147792],np.float32)).all())
            self.assertTrue((shift.value_method == np.array([2, 4, 5],np.int32)).all())
            self.assertEqual(shift.value_spheres, 5)
            self.assertEqual(shift.nh, 1)
            spectrum = spectra[1]
            self.assertEqual(spectrum.nucleus, bjason.Molecule.Atom.NuclType.H1)
            shifts = spectrum.shifts
            self.assertEqual(len(shifts), 10)
            shift = shifts[6]
            self.assertIsInstance(shift, bjason.Molecule.Spectrum.Shift)
            self.assertEqual(shift.mark, 'dn')

    def test_symmetry(self):
        expected_items = [np.array([10, 10], np.int32), np.array([8, 8], np.int32)]
        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r') as h5_file:
            mol = bjason.Molecule(h5_file['/JasonDocument/Molecules/Molecules/0/'])
            symmetry = mol.symmetry
            self.assertIsInstance(symmetry, bjason.Molecule.Symmetry)
            items = symmetry.items
            self.assertEqual(len(items), 2)
            self.assertTrue(bool(items))
            i = 0
            for item in items:
                self.assertTrue((item == expected_items[i] ).all())
                i += 1
            self.assertEqual(i, 2)

            i = len(items) - 1
            for item in reversed(items):
                self.assertTrue((item == expected_items[i] ).all())             
                i -= 1
            self.assertEqual(i, -1)
            self.assertTrue((items[0] == expected_items[0]).all())
            self.assertTrue((items[1] == expected_items[1]).all())
            with self.assertRaises(IndexError):
                item = items[2]

        with h5py.File(datafile_copy_path('Ethylindanone_molecule_with_assignment_table.jjh5'), 'r+') as h5_file:
            mol = bjason.Molecule(h5_file['/JasonDocument/Molecules/Molecules/0/'])
            symmetry = mol.symmetry
            self.assertIsInstance(symmetry, bjason.Molecule.Symmetry)
            items = symmetry.items
            appended_items = [np.array([1, 1], np.int32), np.array([5, 5], np.int32),]
            items.append(appended_items)
            self.assertEqual(len(items), 4)
            i = 0
            for item in items:  
                i += 1
            self.assertEqual(i, 4)
            self.assertTrue((items[0] == expected_items[0]).all())
            self.assertTrue((items[1] == expected_items[1]).all())
            self.assertTrue((items[2] == appended_items[0]).all())
            self.assertTrue((items[3] == appended_items[1]).all())

class ImageTestCase(unittest.TestCase):
    """Image class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/0'])
            self.assertEqual(image.id, '{c67e0726-702e-4ec2-a179-6eb9e6b8c91c}')
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/1'])
            self.assertEqual(image.id, '{59f1d82b-f5b8-4d1b-9919-e228e2e6229f}')

    def test_width(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/0'])
            self.assertEqual(image.width, 1280)
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/1'])
            self.assertEqual(image.width, 256)

    def test_depth(self):
       with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            for i in range(2):
                image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/{}'.format(i)])
                self.assertEqual(image.depth, 32)

    def test_height(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/0'])
            self.assertEqual(image.height, 508)
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/1'])
            self.assertEqual(image.height, 256)

    def test_class_(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            for i in range(2):
                image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/{}'.format(i)])
                self.assertEqual(image.class_, b'IMAGE')

    def test_subclass(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            for i in range(2):
                image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/{}'.format(i)])
                self.assertEqual(image.subclass, b'IMAGE_TRUECOLOR')

    def test_version(self):
       with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            for i in range(2):
                image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/{}'.format(i)])
                self.assertEqual(image.version, b'1.2')

    def test_interlace_mode(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            for i in range(2):
                image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/{}'.format(i)])
                self.assertEqual(image.interlace_mode, b'INTERLACE_PIXEL')

    def test_min_max_range(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            for i in range(2):
                image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/{}'.format(i)])
                self.assertTrue((image.min_max_range == np.array([0, 255], np.uint8)).all())

    def test_pixmap(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/0'])
            pixmap = image.pixmap
            self.assertEqual(pixmap.shape, (508, 1280, 4))
            self.assertEqual(pixmap.dtype, np.uint8)
            image = bjason.Image(h5_file['/JasonDocument/General/Pixmaps/1'])
            pixmap = image.pixmap
            self.assertEqual(pixmap.shape, (256, 256, 4))
            self.assertEqual(pixmap.dtype, np.uint8)

    def test_List(self):
        with h5py.File(datafile_copy_path('JEOL_company_logo.jjh5'), 'r') as h5_file:
            image_list = bjason.Image.List(h5_file['/JasonDocument/General'])
            self.assertEqual(len(image_list), 2)
            count = 0
            for image in image_list:
                self.assertIsInstance(image, bjason.Image)
                self.assertEqual(image.class_, b'IMAGE')
                count += 1
            self.assertEqual(count, 2)

class TextTestCase(unittest.TestCase):
    """Text class test cases"""

    def test_id(self):
        with h5py.File(datafile_copy_path('lorem_ipsum.jjh5'), 'r') as h5_file:
            text = bjason.Text(h5_file['/JasonDocument/General/TextDocuments/0'])
            self.assertEqual(text.id, '{10944f23-fb9a-4cc2-989f-871d51ffb17b}')

    def test_html(self):
        with h5py.File(datafile_copy_path('lorem_ipsum.jjh5'), 'r') as h5_file:
            text = bjason.Text(h5_file['/JasonDocument/General/TextDocuments/0'])
            html = text.html
            self.assertEqual(len(html), 586)
            self.assertEqual(html[-54:], 'Lorem ipsum dolor sit amet...</span></p></body></html>')

if __name__ == '__main__':
    unittest.main()

