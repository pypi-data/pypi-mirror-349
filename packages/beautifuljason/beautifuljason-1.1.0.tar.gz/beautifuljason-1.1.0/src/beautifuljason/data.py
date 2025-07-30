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

import beautifuljason.base as base
import beautifuljason.utils as utils
from enum import IntEnum, auto
import numpy as np
from typing import Iterable, Any

class NMRSpecInfo(base.H5Group):
    """
    Represents spectral information for an NMR dataset encapsulated within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    :param ndim: The number of dimensions for the NMR data.
    :type ndim: :obj:`int`
    """

    def __init__(self, h5_group, ndim):
        super().__init__(h5_group)
        self.ndim = ndim

    def get_param(self, param_name):
        """
        Retrieve a parameter value from the HDF5 group.

        Unlike original parameters (see :meth:`get_orig_param`), these parameters are part of a predefined set 
        that is populated using vendor data.

        :param param_name: Name of the parameter to retrieve.
        :type param_name: str

        :return: Value of the specified parameter if found; None otherwise.
        :rtype: Any or None

        Example Usage
        =============

        .. code-block:: python

            import beautifuljason as bjason

            def extract_metadata(jdf_file: str) -> dict:
                jason = bjason.JASON()
                with jason.create_document(jdf_file) as doc:
                    raw_spec_info = doc.nmr_data[0].raw_data.spec_info

                    # Extract example metadata
                    metadata = {
                        "Title": bjason.utils.ensure_str(raw_spec_info.get_param("Title")),
                        "Solvent": bjason.utils.ensure_str(raw_spec_info.get_param("Solvent")),
                        "Temperature": raw_spec_info.get_param("Temperature")
                    }

                return metadata
        """
        if param_name in self.h5_group.attrs:
            return self.h5_group.attrs[param_name]
        elif param_name in self.h5_group:
            return self.h5_group[param_name]

    def get_orig_param(self, group_name, param_name):
        """
        Retrieve an original parameter value from a specified group within the `OriginalParameters` section of the HDF5 group.
        Original parameters are values imported directly from the original dataset without modification.
        For some vendors, parameters may include attributes written using the syntax `param_name.attr_name`.
        For example, the JEOL Delta `X_FREQ` parameter also includes `X_FREQ.unts` and `X_FREQ.unts.str` attributes.

        :param group_name: Name of the group under 'OriginalParameters' to search in.
        :type group_name: str
        :param param_name: Name of the parameter to retrieve.
        :type param_name: str
        :return: Value of the specified parameter if found; None otherwise.
        :rtype: Any or None

        Example Usage
        =============

        .. code-block:: python
            
            import beautifuljason as bjason

            def extract_metadata(jdf_file: str) -> dict:
                jason = bjason.JASON()
                with jason.create_document(jdf_file) as doc:
                    raw_spec_info = doc.nmr_data[0].raw_data.spec_info

                    # Extract example metadata
                    metadata = {
                        "X_SWEEP": raw_spec_info.get_orig_param("parameters", "X_SWEEP"),
                        "X_FREQ": raw_spec_info.get_orig_param("parameters", "X_FREQ")
                    }

                return metadata
        """
        if group_name in self.h5_group['OriginalParameters']:
            if param_name in self.h5_group['OriginalParameters'][group_name].attrs:
                return self.h5_group['OriginalParameters'][group_name].attrs[param_name]
            elif param_name in self.h5_group['OriginalParameters'][group_name]:
                return self.h5_group['OriginalParameters'][group_name][param_name]

    @property
    def nuclides(self):
        """
        Retrieve the nuclide information for each dimension of the NMR data.
        Provided for convenience, as the value is not readily accessible in the HDF5 group.

        :return: A tuple of nuclide strings for each dimension.
        :rtype: tuple
        """
        return tuple(utils.nuclide_str(self.h5_group['Nucleides/{}'.format(d)].attrs['Isotope'], self.h5_group['Nucleides/{}'.format(d)].attrs['Name'].decode('utf-8'))  for d in range(self.ndim))

class NMREntry(base.H5Group):
    """
    Represents an NMR entry encapsulated within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    """

    def __init__(self, h5_group):
        super().__init__(h5_group)
        self.spec_info = NMRSpecInfo(h5_group['SpecInfo'], self.ndim)

    @property
    def ndim(self):
        """
        Retrieve the number of dimensions for the NMR data.
        Provided for convenience, as the value is not directly available in the HDF5 group.

        :return: Number of dimensions for the NMR data.
        :rtype: int
        """
        res = 0
        for l in self.h5_group.attrs['Length']:
            if l > 1:
                res += 1
        return res

class NMRMultiplet(base.IDedObject):
    """
    Represents an NMR multiplet stored within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    """
    class List(base.IDedObject, base.GroupList):
        """
        Represents a list of NMR multiplets.

        :param h5_group: The actual HDF5 group object.
        :type h5_group: h5py.Group        
        """
        def __init__(self, h5_group):
            base.IDedObject.__init__(self, h5_group)
            base.GroupList.__init__(self, h5_group, 'MultipletList', NMRMultiplet)

        @property
        def pos_units(self):
            """
            :return: A tuple of position units.
            :rtype: :obj:`tuple` of :obj:`Units`
            """
            units = self.h5_group.attrs['PosUnits']
            return tuple(base.Units(u) for u in units)
        
        @property
        def auto_baseline(self):
            """
            :return: True if the baseline is automatically calculated, otherwise False.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['AutoBaseline'])

        @property
        def integral_lvl(self):
            """
            :return: integral level of the multiplets.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['IntegralLvl']

        @property
        def integral_scale(self):
            """
            :return: integral scale of the multiplets.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['IntegralScale']

        @property
        def integral_scale_scoped(self):
            """
            :return: array of scoped integral scales of the multiplets.
            :rtype: :obj:`numpy.ndarray` of :obj:`numpy.float64` or None
            """
            if 'IntegralScaleScoped' in self.h5_group.attrs:
                return self.h5_group.attrs['IntegralScaleScoped']

        @property
        def integral_tlt(self):
            """
            :return: integral tilt of the multiplets.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['IntegralTlt']

        @property
        def integral_total(self):
            """
            :return: total integral of the multiplets.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['IntegralTotal']

        @property
        def integral_vscale(self):
            """
            :return: integral vertical scale of the multiplets.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['IntegralVScale']

        @property
        def integral_vshift(self):
            """
            :return: integral vertical shift of the multiplets.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['IntegralVShift']

    def __init__(self, h5_group):
        super(NMRMultiplet, self).__init__(h5_group)

    class ShowType(IntEnum):
        """
        Enumeration representing the types of display for the multiplet.
        """
        Multiplet = 0
        Integral = 1

    @property
    def show_type(self)-> ShowType:
        """
        :return: The display type of the multiplet.
        :rtype: :obj:`ShowType`
        """
        return NMRMultiplet.ShowType(self.h5_group.attrs['ShowType'])

    @property
    def value(self):
        """
        :return: The value of the multiplet.
        :rtype: :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Value']

    @property
    def value_hz(self):
        """
        :return: The value in Hertz (Hz) of the multiplet.
        :rtype: :obj:`numpy.float64`
        """
        return self.value * self.value_hz_factor

    @property
    def value_hz_factor(self):
        """
        :return: The factor to convert the value to Hertz (Hz). Defaults to 1.0 if not specified in the HDF5 group.
        :rtype: :obj:`numpy.float64`
        """
        if 'Value.HzFactor' in self.h5_group.attrs:
            return self.h5_group.attrs['Value.HzFactor']
        return 1.0    

    @property
    def multiplets(self):
        """
        :return: The associated list of multiplets.
        :rtype: :obj:`NMRMultiplet.List` or None if not present.
        """
        if self.h5_group.parent and self.h5_group.parent.parent:
            return self.List(self.h5_group.parent.parent)

    @property
    def normalized_value(self):
        """
        :return: The normalized value of the multiplet. 
        :rtype: :obj:`numpy.float64`
        """
        if not self.multiplets is None and not self.multiplets.integral_scale_scoped is None:
            return self.value_hz * self.multiplets.integral_scale_scoped[self.integral_scope]
        return self.value_hz * self.multiplets.integral_scale

    @property
    def integral_scope(self) -> np.int32:
        """
        :return: The scope for the integral. Defaults to 0 if not specified in the HDF5 group.
        :rtype: :obj:`numpy.int32`
        """
        if 'IntegralScope' in self.h5_group.attrs:
            return self.h5_group.attrs['IntegralScope']
        return 0

    @property
    def flags(self) -> np.int32:
        """
        :return: The flags associated with the multiplet.
        :rtype: :obj:`int`
        """
        return self.h5_group.attrs['MultipletFlags']

    @property
    def range(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        :return: The multiplet range as a tuple of np.array objects.
        :rtype: :obj:`tuple` of shape (3,) of :obj:`numpy.ndarray` with dtype :obj:`numpy.float64` 
        """
        return (self.h5_group.attrs['SpectrumRange[0]'], self.h5_group.attrs['SpectrumRange[1]'], self.h5_group.attrs['SpectrumRange[2]'])

    @property
    def jtree(self):
        """
        :return: The J coupling tree data, represented as a list of dictionaries with 'groups' and 'positions' as keys.
        :rtype: :obj:`list` of :obj:`dict` with keys 'groups' and 'positions'
        """
        i = 0
        result = []
        while 'JTree[{}].Groups'.format(i) in self.h5_group.attrs:
            result.append({'groups': self.h5_group.attrs['JTree[{}].Groups'.format(i)], 'positions': self.h5_group.attrs['JTree[{}].Positions'.format(i)]})
            i += 1
        return result 

    def _get_peaks(self, attr_name) -> list['NMRPeak']:
        """
        :param attr_name: The name of the attribute to retrieve the peaks from.
        :type attr_name: :obj:`str`
        :return: The peaks associated with the attribute.
        :rtype: :obj:`list` of :obj:`NMRPeak`
        """
        result = []
        if 'Peaks' not in self.h5_group.parent.parent.parent:
            return result
        peak_list = NMRPeak.List(self.h5_group.parent.parent.parent['Peaks'])
        peak_ids = self.h5_group.attrs[attr_name]
        for id in peak_ids:
            for peak in peak_list:
                if id == peak.id:
                    result.append(peak) 
                    break
        return result   

    @property
    def peaks(self) -> list['NMRPeak']:
        """
        :return: The peaks associated with the multiplet.
        :rtype: :obj:`list` of :obj:`NMRPeak`

        **Example Usage**:

        .. code-block:: python

            import beautifuljason as bjason

            # It is assumed that the 'example.jjh5' document contains a spectrum with multiplets.
            with bjason.Document('example.jjh5', mode='r') as doc:
                for multiplet in doc.nmr_data[0].multiplets:
                    print(f'Pos: {multiplet.pos[0]}, Sum Integral: {multiplet.value_hz}')
                    for peak in multiplet.peaks:
                        print(f'  Peak Pos: {peak.pos[0]}, Area: {peak.area}')
        """
        return self._get_peaks('Peaks')

    @property
    def all_peaks(self) -> list['NMRPeak']:
        """
        :return: All peaks found within the multiplet region, including those not associated with the multiplet.
        :rtype: :obj:`list` of :obj:`NMRPeak`
        """
        return self._get_peaks('AllPeaks')

    @property
    def moments(self) -> np.ndarray[np.float64]:
        """
        :return: The moments associated with the multiplet.
        :rtype: :obj:`numpy.ndarray` with dtype :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Moments']

    @property
    def curve(self) -> np.ndarray[np.float64]:
        """
        :return: The curve data for the multiplet.
        :rtype: :obj:`numpy.ndarray` with dtype :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Curve']

    @property
    def pos(self) -> np.ndarray[np.float64]:
        """
        :return: The position of the multiplet.
        :rtype: :obj:`numpy.ndarray` of shape (3,) with dtype :obj:`numpy.float64`
        """
        return self.h5_group.attrs['MultipletPos']

    @property
    def js(self) -> np.ndarray[np.float64]:
        """
        :return: The J values for the multiplet. If not present, returns an empty array.
        :rtype: :obj:`numpy.ndarray` with dtype :obj:`numpy.float64`
        """
        if 'Js' in self.h5_group.attrs:
            return self.h5_group.attrs['Js']
        else:
            return np.array([],np.float64)

    @property
    def multiplicities(self) -> np.ndarray[np.int32]:
        """
        :return: The multiplicities for the multiplet. If not present, returns an empty array.
        :rtype: :obj:`numpy.ndarray` with dtype :obj:`numpy.int32`
        """
        if 'Multiplicities' in self.h5_group.attrs:
            return self.h5_group.attrs['Multiplicities']
        else:
            return np.array([],np.int32)

    @property
    def multiplicities_str(self) -> str | None:
        """
        :return: The multiplicities for the multiplet as a string.
        :rtype: :obj:`str` or None if not present.
        """
        if 'Multiplicities.str' in self.h5_group.attrs:
            return utils.ensure_str(self.h5_group.attrs['Multiplicities.str'])

class NMRPeak(base.IDedObject):
    """
    Represents an NMR peak stored within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    """
    class List(base.IDedObject, base.GroupList):
        """
        Represents a list of NMR peaks.

        :param h5_group: The actual HDF5 group object.
        :type h5_group: h5py.Group
        """
        def __init__(self, h5_group):
            base.IDedObject.__init__(self, h5_group)
            base.GroupList.__init__(self, h5_group, 'PeakList', NMRPeak)

        @property
        def pos_units(self) -> tuple[base.Units, base.Units, base.Units]:
            """
            Returns the position units of the peaks.

            :return: A tuple of position units.
            :rtype: :obj:`tuple` of :obj:`base.Units`
            """
            units = self.h5_group.attrs['PosUnits']
            return tuple(base.Units(u) for u in units)

    def __init__(self, h5_group):
        super(NMRPeak, self).__init__(h5_group)

    class PeakType(IntEnum):
        """Enumeration representing the types of peaks."""
        PseudoVoigt = 0
        GenLorentz = 1
 
    class PeakClassification(IntEnum):
        """
        Enumeration representing the classifications of peaks.
        """
        Compound = 0
        Contaminant = 1
        NMRSolvent = 2
        ReactionSolvent = 3
        C13Satellite = 4
        SSSideband = 5

    @property
    def type(self):
        """
        :return: The type of the peak.
        :rtype: :obj:`PeakType`
        """
        return NMRPeak.PeakType(self.h5_group.attrs['PeakType'])

    @property
    def classification(self) -> PeakClassification:
        """
        The classification of the peak.

        :getter: Returns the classification of the peak.
        :rtype: :obj:`PeakClassification`
        
        :setter: Sets the classification of the peak.
        :param new_classification: The new classification of the peak.
        :type new_classification: :obj:`PeakClassification`
        """
        return NMRPeak.PeakClassification(self.h5_group.attrs['PeakClassification'])
    
    @classification.setter
    def classification(self, new_classification: PeakClassification):
        self.h5_group.attrs['PeakClassification'] = np.int8(NMRPeak.PeakClassification(int(new_classification)))

    @property
    def height(self) -> np.float64:
        """
        :return: The height of the peak.
        :rtype: :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Height']

    @property
    def offset(self) -> np.float64:
        """
        :return: The offset of the peak.
        :rtype: :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Offset']

    @property
    def label(self):
        """
        The label of the peak.

        :getter: Returns the label of the peak.
        :rtype: :obj:`str`

        :setter: Sets the label of the peak.
        :param new_label: The new label of the peak.
        :type new_label: :obj:`str`
        """
        return utils.ensure_str(self.h5_group.attrs['PeakLabel'])
    
    @label.setter
    def label(self, new_label):
        self.h5_group.attrs['PeakLabel'] = new_label

    @property
    def pos(self) -> np.ndarray[np.float64]:
        """
        :return: The position of the peak.
        :rtype: :obj:`numpy.ndarray` of shape (3,) with dtype :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Pos']

    @property
    def shape_par(self) -> np.ndarray[np.float64]:
        """
        :return: The shape parameter of the peak.
        :rtype: :obj:`numpy.ndarray` of shape (3,) with dtype :obj:`numpy.float64`
        """
        return self.h5_group.attrs['ShapePar']

    @property
    def width(self) -> np.ndarray[np.float64]:
        """
        :return: The width of the peak.
        :rtype: :obj:`numpy.ndarray` of shape (3,) with dtype :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Width']
    
    @property
    def area(self) -> np.float64:
        """
        .. versionadded:: 1.0.4

        :return: The area of the peak.
        :rtype: :obj:`numpy.float64`

        .. note:: Requires JASON 4.1 or later.
        """
        return self.h5_group.attrs['Area'] if 'Area' in self.h5_group.attrs else None
    
    @property
    def area_sigma(self) -> np.float64:
        """
        .. versionadded:: 1.0.4

        :return: The area sigma of the peak.
        :rtype: :obj:`numpy.float64`

        .. note:: Requires JASON 4.1 or later.
        """
        return self.h5_group.attrs['Area.sigma'] if 'Area.sigma' in self.h5_group.attrs else None
    
class NMRProcessing(base.IDedObject):
    """
    Represents an NMR processing step stored within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    """

    class List(base.GroupList):
        """
        Represents a list of NMR processing steps.

        :param h5_group: The actual HDF5 group object.
        """
        def __init__(self, h5_group):
            base.GroupList.__init__(self, h5_group, 'ProcessingSteps', NMRProcessing)        

        class EndType(IntEnum):
            """
            Enumeration representing the types of endpoints.
            """
            Full = 0
            Orig = 1
            preFT = 2
            postFT = 3
    
        @property
        def end_point_dim(self) -> np.int32:
            """
            :return: The dimension of the endpoint.
            :rtype: :obj:`numpy.int32`
            """
            return self.h5_group['EndPoint'].attrs['Dim']

        @property
        def end_point_type(self) -> EndType:
            """
            :return: The type of endpoint.
            :rtype: :obj:`EndType`
            """
            return NMRProcessing.List.EndType(self.h5_group['EndPoint'].attrs['EndPtType'])

    def __init__(self, h5_group):
        super(NMRProcessing, self).__init__(h5_group)

    class Type(IntEnum):
        """
        Enumeration representing the types of processing steps.
        """
        Unknown = 0
        ZF = 1
        Apodize = 2
        Lp = 3
        FT = 4
        PrepIndir = 5
        Phase = 6
        Reverse = 7
        Abs = 8
        NextDim = 9
        SGSmooth = 10
        PolyBC = 11
        Flatten = 12
        Real = 13
        External = 14
        NUS = 15
        Sym = 16
        Sub = 17
        SGFilter2D = 18
        CSSF = 19
        Sim = 20
        Rot = 21
        iFT = 22
        PhaseFID = 23
        DOSY = 24
        DTA = 25
        DC = 26
        Scale = 27
        Sum = 28
        PeakRef = 29
        T1Sup = 30
        fLP = 31
        Filter = 32
        ATD = 33
        NoiseGen = 34
        ReSample = 35
        ROSY = 36
        Compress = 37
        Fiddle = 38
        Custom = 39
        DcFID = 40
        Cov = 41
        Normalize = 42
        bLP = 43
        Round = 44
        DownSample = 45
        Shear = 46
        Tilt = 47
    
    class Parameter(base.H5Group):
        """
        Represents a parameter for an NMR processing step.
        """
        class List(base.GroupList):
            """
            Represents a list of parameters for an NMR processing step.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'Parameters', NMRProcessing.Parameter)

        @property
        def name(self) -> str:
            """
            :return: The name of the parameter.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['Name'])

        @property
        def value_type(self) -> base.QMetaType_Type:
            """
            :return: The type of the parameter.
            :rtype: :obj:`base.QMetaType_Type`
            """
            return base.QMetaType_Type(self.h5_group.attrs['Value.type']) if 'Value.type' in self.h5_group.attrs else base.QMetaType_Type.UnknownType

        @property
        def tip(self) -> str:
            """
            :return: The tip for the parameter.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['Tip'])

        @property
        def value(self) -> Any:
            """
            :return: The value of the parameter.
            :rtype: :obj:`Any`
            """
            if 'Value' not in self.h5_group.attrs:
                return None
            t = self.value_type
            v = self.h5_group.attrs['Value']
            if t == base.QMetaType_Type.Bool:
                return bool(v)
            elif t == base.QMetaType_Type.QStringList:
                return [utils.ensure_str(s) for s in v]
            elif t == base.QMetaType_Type.QString:
                return utils.ensure_str(v)
            else:
                return v

        @property
        def decimals(self) -> np.int32 | None:
            """
            :return: The number of decimals for the parameter.
            :rtype: :obj:`numpy.int32` or None if not present.
            """
            if 'Decimals' in self.h5_group.attrs:
                return self.h5_group.attrs['Decimals']
            else:
                return None

        @property
        def step(self) -> np.float64 | None:
            """
            :return: The step size for the parameter.
            :rtype: :obj:`numpy.float64` or None if not present.
            """
            if 'Step' in self.h5_group.attrs:
                return self.h5_group.attrs['Step']
            else:
                return None
        
        @property
        def max_value(self) -> Any | None:
            """
            :return: The maximum value for the parameter.
            :rtype: :obj:`Any` or None if not present.
            """
            if 'MaxValue' in self.h5_group.attrs:
                return self.h5_group.attrs['MaxValue']
            else:
                return None
        
        @property
        def min_value(self) -> Any | None:
            """
            :return: The minimum value for the parameter.
            :rtype: :obj:`Any` or None if not present.
            """
            if 'MinValue' in self.h5_group.attrs:
                return self.h5_group.attrs['MinValue']
            else:
                return None

        @property
        def current_index(self) -> np.int32 | None:
            """
            :return: The current index for the parameter.
            :rtype: :obj:`numpy.int32` or None if not present.
            """
            if 'CurrentIndex' in self.h5_group.attrs:
                return self.h5_group.attrs['CurrentIndex']
            else:
                return None

        @property
        def units(self) -> base.Units:
            """
            :return: The units for the parameter.
            :rtype: :obj:`base.Units`
            """
            if 'Units' in self.h5_group.attrs:
                return base.Units(self.h5_group.attrs['Units'])
            else:
                return base.Units.NONE

    @property
    def type(self) -> Type:
        """
        :return: The type of the processing step.
        :rtype: :obj:`Type`
        """
        return NMRProcessing.Type(self.h5_group.attrs['ProcessingType'])

    @property
    def name(self) -> str:
        """
        :return: The name of the processing step.
        :rtype: :obj:`str`
        """
        return utils.ensure_str(self.h5_group.attrs['Name'])

    @property
    def active(self) -> bool:
        """
        :return: True if the processing step is active, otherwise False.
        :rtype: :obj:`bool`
        """
        return bool(self.h5_group.attrs['Active'])
    
    @property
    def parameters(self) -> Parameter.List:
        """
        .. versionadded:: 1.1.0

        :return: The list of parameters for the processing step.
        :rtype: :obj:`Parameter.List`
        """
        return NMRProcessing.Parameter.List(self.h5_group)

class NMRSpectrum(NMREntry, base.IDedObject):
    """
    Represents an NMR spectrum stored within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    """
    class List(base.GroupList):
        """
        Represents a list of NMR spectra.

        :param h5_group: The actual HDF5 group object.
        """
        def __init__(self, h5_group):
            base.GroupList.__init__(self, h5_group, 'NMRData', NMRSpectrum)

    def __init__(self, h5_group):
        super(NMRSpectrum, self).__init__(h5_group)
        self.raw_data = NMREntry(h5_group['RawData'])

    @property
    def peaks(self) -> NMRPeak.List:
        """
        :return: The associated list of peaks.
        :rtype: :obj:`NMRPeak.List` of :obj:`NMRPeak`.

        **Example Usage**:

        .. code-block:: python

            import beautifuljason as bjason

            # It is assumed that the 'example.jjh5' document contains a spectrum with peaks.
            with bjason.Document('example.jjh5', mode='r') as doc:
                for peak in doc.nmr_data[0].peaks:
                    print(f'Pos: {peak.pos[0]}, Area: {peak.area}')
        """
        return NMRPeak.List(self.h5_group['Peaks'])

    @property
    def multiplets(self) -> NMRMultiplet.List:
        """
        :return: The associated list of multiplets.
        :rtype: :obj:`NMRMultiplet.List` of :obj:`NMRMultiplet`.

        **Example Usage**:

        .. code-block:: python

            import beautifuljason as bjason
                        
            # It is assumed that the 'example.jjh5' document contains a spectrum with multiplets.
            with bjason.Document('example.jjh5', mode='r') as doc:
                for multiplet in doc.nmr_data[0].multiplets:
                    print(f'Pos: {multiplet.pos[0]}, Sum Integral: {multiplet.value_hz}')
        """
        return NMRMultiplet.List(self.h5_group['Multiplets_Integrals'])

    @property
    def proc_list(self) -> NMRProcessing.List:
        """
        :return: The associated list of processing steps.
        :rtype: :obj:`NMRProcessing.List` of :obj:`NMRProcessing`.

        **Example Usage**:

        .. code-block:: python

            import beautifuljason as bjason

            # It is assumed that the 'example.jjh5' document contains a spectrum.
            with bjason.Document('example.jjh5', mode='r') as doc:
                for proc in doc.nmr_data[0].proc_list:
                    print(f'Name: {proc.name}')
                    for param in proc.parameters:
                        print(f'  {param.name}({param.tip}): {param.value}')
        """
        return NMRProcessing.List(self.h5_group['ProcessingTemplate'])

class Text(base.IDedObject):
    """
    Represents a text data object located at /JasonDocument/General/TextDocuments/<N>.

    The text is stored as an HTML string.
    """

    class List(base.GroupList):
        """
        Represents a list of text data objects
        """

        def __init__(self, h5_group):
            super().__init__(h5_group, 'TextDocuments', Text)

    @property
    def html(self) -> str:
        """
        The HTML text.

        :getter: Returns the HTML text.
        :rtype: :obj:`str`

        :setter: Sets the HTML text.
        :param new_html: The new HTML text.
        :type new_html: :obj:`str`
        """
        return utils.ensure_str(self.h5_group.attrs['Html'])

    @html.setter
    def html(self, new_html):
        self.h5_group.attrs['Html'] = new_html

class Image(base.IDedObject):
    """
    Represents an image data object /JasonDocument/General/Pixmaps/<N>

    The image is stored in HDF5 format and can be accessed as a numpy array.
    """

    class List(base.GroupList):
        """
        Represents a list of image data objects
        """

        def __init__(self, h5_group):
            super().__init__(h5_group, 'Pixmaps', Image)

    @property
    def class_(self) -> bytes:
        """
        :return: The image class attribute.
        :rtype: :obj:`bytes`
        """
        return self.h5_group['Pixmap'].attrs['CLASS']

    @property
    def min_max_range(self) -> np.ndarray[np.uint8]:
        """
        :return: The image min max range attribute.
        :rtype: :obj:`np.ndarray` of :obj:`np.uint8`
        """
        return self.h5_group['Pixmap'].attrs['IMAGE_MINMAXRANGE']

    @property
    def subclass(self) -> bytes:
        """
        :return: The image subclass attribute.
        :rtype: :obj:`bytes`
        """
        return self.h5_group['Pixmap'].attrs['IMAGE_SUBCLASS']

    @property
    def version(self) -> bytes:
        """
        :return: The image version attribute.
        :rtype: :obj:`bytes`
        """
        return self.h5_group['Pixmap'].attrs['IMAGE_VERSION']

    @property
    def interlace_mode(self) -> bytes:
        """
        :return: The image interlace mode attribute.
        :rtype: :obj:`bytes`
        """
        return self.h5_group['Pixmap'].attrs['INTERLACE_MODE']

    @property
    def width(self) -> int:
        """
        :return: The image width.
        :rtype: :obj:`int`
        """
        return  self.h5_group['Pixmap'].shape[1]

    @property
    def height(self) -> int:
        """
        :return: The image height.
        :rtype: :obj:`int`
        """
        return  self.h5_group['Pixmap'].shape[0]

    @property
    def depth(self) -> int:
        """
        :return: The image depth. 24 for RGB and 32 for RGBA
        :rtype: :obj:`int`
        """
        return  self.h5_group['Pixmap'].shape[2] * 8
    
    @property
    def pixmap(self) -> np.ndarray[np.uint8]:
        """
        .. versionadded:: 1.1.0

        The image data.

        :return: The image data as a numpy array.
        :rtype: :obj:`np.ndarray` of :obj:`np.uint8`
        """
        return self.h5_group['Pixmap'][:]

class Molecule(base.IDedObject):
    """
    Represents a molecule data object from /JasonDocument/Molecules/Molecules/<N> groups.
    """

    class Atom(base.H5Group):
        """
        Represents an atom.
        """

        class Type(base.IntEnum):
            """
            Atom elements enumeration. 
            """
            NONE = 0
            H = auto()
            He = auto()
            Li = auto(); Be = auto(); B = auto(); C = auto(); N = auto(); O = auto(); F = auto(); Ne = auto()
            Na = auto(); Mg = auto(); Al = auto(); Si = auto(); P = auto(); S = auto(); Cl = auto(); Ar = auto()
            K = auto(); Ca = auto(); Sc = auto(); Ti = auto(); V = auto(); Cr = auto(); Mn = auto(); Fe = auto(); Co = auto(); Ni = auto()
            Cu = auto(); Zn = auto(); Ga = auto(); Ge = auto(); As = auto(); Se = auto(); Br = auto(); Kr = auto()
            Rb = auto(); Sr = auto(); Y = auto(); Zr = auto(); Nb = auto(); Mo = auto(); Tc = auto(); Ru = auto(); Rh = auto(); Pd = auto()
            Ag = auto(); Cd = auto(); In = auto(); Sn = auto(); Sb = auto(); Te = auto(); I = auto(); Xe = auto()
            Cs = auto(); Ba = auto()
            La = auto(); Ce = auto(); Pr = auto(); Nd = auto(); Pm = auto(); Sm = auto(); Eu = auto(); Gd = auto(); Tb = auto(); Dy = auto(); Ho = auto(); Er = auto(); Tm = auto(); Yb = auto(); Lu = auto()
            Hf = auto(); Ta = auto(); W = auto(); Re = auto(); Os = auto(); Ir = auto(); Pt = auto()
            Au = auto(); Hg = auto(); Tl = auto(); Pb = auto(); Bi = auto(); Po = auto(); At = auto(); Rn = auto()
            Fr = auto(); Ra = auto()
            Ac = auto(); Th = auto(); Pa = auto(); U = auto(); Np = auto(); Pu = auto(); Am = auto(); Cm = auto(); Bk = auto(); Cf = auto(); Es = auto(); Fm = auto(); Md = auto(); No = auto(); Lr = auto()
            Rf = auto(); Db = auto(); Sg = auto(); Bh = auto(); Hs = auto(); Mt = auto(); Ds = auto()
            Rg = auto(); Cn = auto(); Nh = auto(); Fl = auto(); Mc = auto(); Lv = auto(); Ts = auto(); Og = auto()
            El119 = auto(); El120 = auto()
            El121 = auto(); El122 = auto(); El123 = auto(); El124 = auto(); El125 = auto(); El126 = auto(); El127 = auto(); El128 = auto(); El129 = auto(); El130 = auto()
            El131 = auto(); El132 = auto(); El133 = auto(); El134 = auto(); El135 = auto(); El136 = auto(); El137 = auto(); El138 = auto(); El139 = auto(); El140 = auto()
            El141 = auto(); El142 = auto(); El143 = auto(); El144 = auto(); El145 = auto(); El146 = auto(); El147 = auto(); El148 = auto(); El149 = auto(); El150 = auto()
            # Specific non-existing element(s)
            FV = auto(); A = auto(); Q = auto(); L = auto(); NL = auto()

        class NuclType(IntEnum):
            """
            Nuclide types enumeration. 
            """
            Undef = 0
            H1 = auto()
            H2 = auto()
            H3 = auto()
            He3 = auto()
            Li6 = auto()
            Li7 = auto()
            Be9 = auto()
            B10 = auto()
            B11 = auto()
            C13 = auto()
            N14 = auto()
            N15 = auto()
            O17 = auto()
            F19 = auto()
            Ne21 = auto()
            Na23 = auto()
            Mg25 = auto()
            Al27 = auto()
            Si29 = auto()
            P31 = auto()
            S33 = auto()
            Cl35 = auto()
            Cl37 = auto()
            K39 = auto()
            K41 = auto()
            Ca43 = auto()
            Sc45 = auto()
            Ti47 = auto()
            Ti49 = auto()
            V50 = auto()
            V51 = auto()
            Cr53 = auto()
            Mn55 = auto()
            Fe57 = auto()
            Co59 = auto()
            Ni61 = auto()
            Cu63 = auto()
            Cu65 = auto()
            Zn67 = auto()
            Ga69 = auto()
            Ga71 = auto()
            Ge73 = auto()
            As75 = auto()
            Se77 = auto()
            Br79 = auto()
            Br81 = auto()
            Kr83 = auto()
            Rb85 = auto()
            Rb87 = auto()
            Sr87 = auto()
            Y89 = auto()
            Zr91 = auto()
            Nb93 = auto()
            Mo95 = auto()
            Mo97 = auto()
            Ru99 = auto()
            Ru101 = auto()
            Rh103 = auto()
            Pd105 = auto()
            Ag107 = auto()
            Ag109 = auto()
            Cd111 = auto()
            Cd113 = auto()
            In113 = auto()
            In115 = auto()
            Sn115 = auto()
            Sn117 = auto()
            Sn119 = auto()
            Sb121 = auto()
            Sb123 = auto()
            Te123 = auto()
            Te125 = auto()
            I127 = auto()
            Xe129 = auto()
            Xe131 = auto()
            Cs133 = auto()
            Ba135 = auto()
            Ba137 = auto()
            La138 = auto()
            La139 = auto()
            Pr141 = auto()
            Nd143 = auto()
            Nd145 = auto()
            Sm147 = auto()
            Sm149 = auto()
            Eu151 = auto()
            Eu153 = auto()
            Gd155 = auto()
            Gd157 = auto()
            Tb159 = auto()
            Dy161 = auto()
            Dy163 = auto()
            Ho165 = auto()
            Er167 = auto()
            Tm169 = auto()
            Yb171 = auto()
            Yb173 = auto()
            Lu175 = auto()
            Lu176 = auto()
            Hf177 = auto()
            Hf179 = auto()
            Ta181 = auto()
            W183 = auto()
            Re185 = auto()
            Re187 = auto()
            Os187 = auto()
            Os189 = auto()
            Ir191 = auto()
            Ir193 = auto()
            Pt195 = auto()
            Au197 = auto()
            Hg199 = auto()
            Hg201 = auto()
            Tl203 = auto()
            Tl205 = auto()
            Pb207 = auto()
            Bi209 = auto()
            U235 = auto()

        class List(base.GroupList):
            """
            Represents a list of atoms.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'Atoms', Molecule.Atom)

        @property
        def type(self) -> Type:
            """
            :return: The type of the atom.
            :rtype: :obj:`Type`
            """
            return Molecule.Atom.Type(self.h5_group.attrs['El'])

        @property
        def valence(self) -> int | None:
            """
            :return: The valence of the atom.
            :rtype: :obj:`int` | None
            """
            if 'Val' in self.h5_group.attrs: 
                return self.h5_group.attrs['Val']   

        @property
        def charge(self) -> int | None:
            """
            :return: The charge of the atom.
            :rtype: :obj:`int` | None
            """
            if 'Ch' in self.h5_group.attrs: 
                return self.h5_group.attrs['Ch']

        @property
        def isotope(self) -> int | None:
            """
            :return: The isotope of the atom.
            :rtype: :obj:`int` | None
            """
            if 'Iso' in self.h5_group.attrs: 
                return self.h5_group.attrs['Iso']

        @property
        def bonds(self) -> np.ndarray[np.uint32]:
            """
            :return: The bonds of the atom.
            :rtype: :obj:`np.ndarray` of :obj:`np.uint32`
            """
            return self.h5_group.attrs['NB.Conn']

        @property
        def bonded_atom_numbers(self) -> np.ndarray[np.uint32]:
            """
            :return: The bonded atom numbers of the atom.
            :rtype: :obj:`np.ndarray` of :obj:`np.uint32`
            """
            return self.h5_group.attrs['NB.Num']

        @property
        def bonded_atoms(self) -> list['Molecule.Atom']:
            """
            :return: The bonded atoms of the atom.
            :rtype: :obj:`list` of :obj:`Molecule.Atom`
            """
            mol = Molecule(self.h5_group.parent.parent)
            mol_atoms = mol.atoms
            atoms = []
            for atom_num in self.h5_group.attrs['NB.Num']:
                atoms.append(mol_atoms[atom_num])
            return atoms

        @property
        def x(self) -> float:
            """
            :return: The X coordinate of the atom.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['X']

        @property
        def y(self) -> float:
            """
            :return: The Y coordinate of the atom.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['Y']

        @property
        def z(self) -> float | None:
            """
            :return: The Z coordinate of the atom if present.
            :rtype: :obj:`float` | None
            """
            if 'Z' in self.h5_group.attrs: 
                return self.h5_group.attrs['Z']

        @property
        def nh(self) -> int:
            """
            :return: The number of hydrogen atoms attached to the atom.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['nH']
 
    class Ring(base.H5Group):
        """
        Represents a ring.
        """
        
        class List(base.GroupList):
            """
            Represents a list of rings.

            :param h5_group: The H5 group.
            :type h5_group: :obj:`h5py.Group`
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'Rings', Molecule.Ring)

        @property
        def atoms(self) -> np.ndarray[np.uint32]:
            """
            :return: The atoms of the ring.
            :rtype: :obj:`np.ndarray` of :obj:`np.uint32`
            """
            return self.h5_group.attrs['Atoms']

        @property
        def is_aromatic(self) -> bool:
            """
            :return: Whether the ring is aromatic.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['IsAromatic'])

    class Coupling(base.H5Group):
        """
        Represents a j-coupling.
        """

        class List(base.GroupList):
            """
            Represents a list of j-couplings.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'CouplingsList', Molecule.Coupling)

        @property
        def acount1(self) -> int:
            """
            :return: The number of identical atoms of the first coupling partner.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['ACount1']

        @property
        def acount2(self) -> int:
            """
            :return: The number of identical atoms of the second coupling partner.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['ACount2']

        @property
        def error_spheres(self) -> int:
            """
            :return: The error spheres of the coupling.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['ErrorSpheres']

        @property
        def ignored_auto(self) -> bool:
            """
            :return: Whether the coupling is ignored automatically.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['IgnoredAuto'])

        @property
        def ignored_user(self) -> bool:
            """
            :return: Whether the coupling is ignored by the user.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['IgnoredUser'])

        @property
        def is_exchangeable1(self) -> bool:
            """
            :return: Whether the first coupling partner is exchangeable.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['IsExchangeable1'])

        @property
        def is_exchangeable2(self) -> bool:
            """
            :return: Whether the second coupling partner is exchangeable.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['IsExchangeable2'])

        @property
        def jvalue(self) -> int:
            """
            :return: Number of bonds between the coupling partners.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['JValue']

        @property
        def n1(self) -> np.uint32:
            """
            :return: The first atom number of the coupling.
            :rtype: :obj:`np.uint32`
            """ 
            return self.h5_group.attrs['N1']

        @property
        def n2(self) -> np.uint32:
            """
            :return: The second atom number of the coupling.
            :rtype: :obj:`np.uint32`
            """
            return self.h5_group.attrs['N2']

        @property
        def nucl1(self) -> 'Molecule.Atom.NuclType':
            """
            :return: The nuclide type of the first coupling partner.
            :rtype: :obj:`Molecule.Atom.NuclType`
            """
            return Molecule.Atom.NuclType(self.h5_group.attrs['Nucl1'])

        @property
        def nucl2(self) -> 'Molecule.Atom.NuclType':
            """
            :return: The nuclide type of the second coupling partner.
            :rtype: :obj:`Molecule.Atom.NuclType`
            """
            return Molecule.Atom.NuclType(self.h5_group.attrs['Nucl2'])

        @property
        def mark1(self) -> str | None:
            """
            :return: The mark of the first coupling partner if present.
            :rtype: :obj:`str` | None
            """
            if 'Mark1' in self.h5_group.attrs: 
                return utils.ensure_str(self.h5_group.attrs['Mark1'])

        @property
        def mark2(self) -> str | None:
            """
            :return: The mark of the second coupling partner if present.
            :rtype: :obj:`str` | None
            """
            if 'Mark2' in self.h5_group.attrs: 
                return utils.ensure_str(self.h5_group.attrs['Mark2'])

        @property
        def value(self) -> np.ndarray[np.float64]:
            """
            :return: array of experimental and calculated J values of the coupling. The value at index 0 is the experimental J value.
            :rtype: :obj:`np.ndarray` of :obj:`np.float64`
            """
            return self.h5_group.attrs['Value']

        @property
        def value_error(self) -> np.ndarray[np.float64]:
            """
            :return: array of calculated J value errors of the coupling. The value at index 0, corresponding to the experimental J value, is -1.
            :rtype: :obj:`np.ndarray` of :obj:`np.float64`
            """
            return self.h5_group.attrs['Value.Error']

        @property
        def value_method(self) -> np.ndarray[np.int32]:
            """
            :return: array of value calculation methods of the coupling.
            :rtype: :obj:`np.ndarray` of :obj:`np.int32`
            """
            return self.h5_group.attrs['Value.Method']

        @property
        def value_spheres(self) -> int:
            """
            :return: The value spheres of the coupling.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['ValueSpheres']

    class Spectrum(base.H5Group):
        """
        Represents a prediction spectrum.
        """
        
        class Type(IntEnum):
            """
            Spectrum types enumeration.
            """
            Undef = 0
            STD = auto()
            DEPT90 = auto()
            DEPT135 = auto()
            APT = auto()
            COSY = auto()
            TOCSY = auto()
            NOESY = auto()
            ROESY = auto()
            HSQC = auto()
            HMQC = auto()
            HSQC_TOCSY = auto()
            HETCOR = auto()
            HMBC = auto()
            COLOC = auto()
            H2BC = auto()
            ADEQUATE = auto()
            INADEQUATE = auto()
            Near_2D = auto()
            Long_2D = auto()
            Mass = auto()
            IR = auto()
            UV = auto()
            Chrom = auto()
            DEPT45 = auto()
            HSQC_DEPT135 = auto()

            # for more convenience 
            H1 = auto()
            C13 = auto()
            All = auto()

        class List(base.GroupList):
            """
            Represents a list of prediction spectra.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'SpectraList', Molecule.Spectrum)

        class Shift(base.H5Group):
            """
            Represents a chemical shift.
            """

            class List(base.GroupList):
                """
                Represents a list of chemical shifts.
                """
                def __init__(self, h5_group):
                    base.GroupList.__init__(self, h5_group, 'Shifts', Molecule.Spectrum.Shift)

            @property
            def acount(self) -> int:
                """
                :return: The number of identical atoms of the chemical shift.
                :rtype: :obj:`int`
                """
                return self.h5_group.attrs['ACount']

            @property
            def error_spheres(self) -> int:
                """
                :return: The error spheres of the chemical shift.
                :rtype: :obj:`int`
                """
                return self.h5_group.attrs['ErrorSpheres']

            @property
            def ignored_auto(self) -> bool:
                """
                :return: Whether the chemical shift is ignored automatically.
                :rtype: :obj:`bool`
                """
                return bool(self.h5_group.attrs['IgnoredAuto'])

            @property
            def ignored_user(self) -> bool:
                """
                :return: Whether the chemical shift is ignored by the user.
                :rtype: :obj:`bool`
                """
                return bool(self.h5_group.attrs['IgnoredUser'])

            @property
            def is_exchangeable(self) -> bool:
                """
                :return: Whether the chemical shift is exchangeable.
                :rtype: :obj:`bool`
                """
                return bool(self.h5_group.attrs['IsExchangeable'])

            @property
            def nums(self) -> np.ndarray[np.uint32]:
                """
                :return: The atom numbers of the chemical shift.
                :rtype: :obj:`np.ndarray` of :obj:`np.uint32`
                """
                return self.h5_group.attrs['Nums']

            @property
            def value(self) -> np.ndarray[np.float64]:
                """
                :return: The experimental and calculated chemical shift values. The value at index 0 is the experimental chemical shift.
                :rtype: :obj:`np.ndarray` of :obj:`np.float64`
                """
                return self.h5_group.attrs['Value']

            @property
            def value_error(self) -> np.ndarray[np.float64]:
                """
                :return: The calculated chemical shift errors. The value at index 0, corresponding to the experimental chemical shift, is -1.
                :rtype: :obj:`np.ndarray` of :obj:`np.float64`
                """
                return self.h5_group.attrs['Value.Error']

            @property
            def value_method(self) -> np.ndarray[np.int32]:
                """
                :return: The value calculation methods of the chemical shift.
                :rtype: :obj:`np.ndarray` of :obj:`np.int32`
                """
                return self.h5_group.attrs['Value.Method']

            @property
            def value_spheres(self) -> int:
                """
                :return: The value spheres of the chemical shift.
                :rtype: :obj:`int`
                """
                return self.h5_group.attrs['ValueSpheres'] 

            @property
            def nh(self) -> int:
                """
                :return: The number of hydrogen atoms attached to the atom.
                :rtype: :obj:`int`
                """
                return self.h5_group.attrs['nH']

            @property
            def mark(self) -> str | None:
                """
                :return: The mark of the chemical shift if present.
                :rtype: :obj:`str` | None
                """
                if 'Mark' in self.h5_group.attrs: 
                    return utils.ensure_str(self.h5_group.attrs['Mark'])

        @property
        def nucleus(self) -> 'Molecule.Atom.NuclType':
            """
            :return: The nucleus of the spectrum.
            :rtype: :obj:`Molecule.Atom.NuclType`
            """
            return Molecule.Atom.NuclType(self.h5_group.attrs['Nucleus'])

        @property
        def origin(self) -> int:
            """
            :return: The origin of the spectrum.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs['Origin']

        @property
        def spec_type(self) -> Type:
            """
            :return: The type of the spectrum.
            :rtype: :obj:`Type`
            """
            return Molecule.Spectrum.Type(self.h5_group.attrs['SpecType'])

        @property
        def shifts(self) -> Shift.List:
            """
            :return: The chemical shifts of the spectrum.
            :rtype: :obj:`Shift.List` of :obj:`Molecule.Spectrum.Shift`

            **Example Usage**:

            .. code-block:: python

                import beautifuljason as bjason

                # It is assumed that the 'example.jjh5' document contains a molecule.
                with bjason.Document('example.jjh5', mode='r') as doc:
                    for pred_spec in doc.mol_data[0].spectra:
                        print(f'Nucleus: {pred_spec.nucleus.name}')
                        for shift in pred_spec.shifts:
                            print(f'  Atoms: {shift.nums}, Shift: {shift.value[0]} ppm')
            """
            return Molecule.Spectrum.Shift.List(self.h5_group)

    class Symmetry(base.H5Group):
        """
        Represents atom symmetry.
        """
        def __init__(self, h5_group):
            super().__init__(h5_group)

        @property
        def items(self) -> Iterable[int]:
            """
            :return: The symmetry items.
            :rtype: :obj:`Iterable` of :obj:`int`
            """
            return base.AttrList(self.h5_group['Items'])
        
    class List(base.GroupList):
        """
        .. versionadded:: 1.1.0

        Represents a list of molecules.
        """
        def __init__(self, h5_group):
            base.GroupList.__init__(self, h5_group, 'Molecules', Molecule)

    # Molecule properties start here
    @property
    def atoms(self) -> Atom.List:
        """
        :return: The atoms of the molecule.
        :rtype: :obj:`Atom.List` of :obj:`Molecule.Atom`
        """
        return Molecule.Atom.List(self.h5_group)

    @property
    def rings(self) -> Ring.List:
        """
        :return: The rings of the molecule.
        :rtype: :obj:`Ring.List` of :obj:`Molecule.Ring`
        """
        return Molecule.Ring.List(self.h5_group)

    @property
    def couplings(self) -> Coupling.List:
        """
        :return: The j-couplings of the molecule.
        :rtype: :obj:`Coupling.List` of :obj:`Molecule.Coupling`
        """
        return Molecule.Coupling.List(self.h5_group['NMRData/Couplings'])

    @property
    def spectra(self) -> Spectrum.List:
        """
        :return: The prediction spectra of the molecule.
        :rtype: :obj:`Spectrum.List` of :obj:`Molecule.Spectrum`

        **Example Usage**:

            .. code-block:: python

                import beautifuljason as bjason

                # It is assumed that the 'example.jjh5' document contains a molecule.
                with bjason.Document('example.jjh5', mode='r') as doc:
                    for pred_spec in doc.mol_data[0].spectra:
                        print(f'Nucleus: {pred_spec.nucleus.name}')
                        for shift in pred_spec.shifts:
                            print(f'  Atoms: {shift.nums}, Shift: {shift.value[0]} ppm')
        """
        return Molecule.Spectrum.List(self.h5_group['NMRData/Spectra'])

    @property
    def symmetry(self) -> Symmetry:
        """
        :return: The symmetry of the molecule.
        :rtype: :obj:`Symmetry`
        """
        return Molecule.Symmetry(self.h5_group['Symmetry'])
