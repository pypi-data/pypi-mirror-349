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
import beautifuljason.data as data
import beautifuljason.utils as utils
from enum import IntEnum, auto
from functools import cached_property
from typing import Iterable, Sequence, Any
import numpy as np
import h5py
import struct
import io

class GraphicsItem(base.IDedObject):
    """
    Represents a graphics item stored within an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    """
    class Type(IntEnum):
        """
        Enumeration representing the types of graphics items.
        """
        NMRSpectrum = 65538
        NMRPeakTable = auto()
        Molecule = auto()
        NMRMultipletTable = auto()
        NMRMultipletReport = auto()
        Text = auto()
        NMRParamTable = auto()
        Image = auto()
        AssignmentTable = auto() 
        ArrayedTable = auto()
        Chart = auto()
        MS = auto()
        DOSYTable = auto()
        FitResultsTable = auto()
        MergedDataTable = auto()
        BinTable = auto()
        EMS = auto()
        MeasurementsTable = auto()
        MolImage = auto()
        Custom = 66536

    class Annotation(base.H5Group):
        """
        Represents an annotation stored within a graphics item.
        """
        class Type(IntEnum):
            """
            Enumeration representing the types of annotations.
            """
            NONE = 0
            RECT = 1
            LINE = 2
            TEXT = 3

        class List(base.GroupList):
            """
            Represents a list of annotations.

            :param h5_group: The actual HDF5 group object.
            :type h5_group: h5py.Group
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'Annotations', GraphicsItem.Annotation)

        @property
        def type(self) -> Type:
            """
            :return: The type of the annotation.
            :rtype: :obj:`Type`
            """
            return GraphicsItem.Annotation.Type(self.h5_group.attrs['Type'])

        @property
        def pos(self):
            """
            :return: The position of the annotation.
            :rtype: :obj:`numpy.ndarray` of shape (2,) with dtype :obj:`numpy.float64`
            """
            return self.h5_group.attrs['Pos']

        @property
        def local_coords(self) -> np.ndarray[np.float64]:
            """
            :return: The local coordinates of the annotation.
            :rtype: :obj:`numpy.ndarray` of shape (4,) with dtype :obj:`numpy.float64`
            """
            return self.h5_group.attrs['LocalCoords']

        @property
        def visible(self) -> bool:
            """
            :return: True if the annotation is visible, otherwise False.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['Visible'])

        @property
        def pinned(self) -> bool | None:
            """
            :return: True if the annotation is pinned, otherwise False. If not present, returns None.
            :rtype: :obj:`bool` or None
            """
            if 'Pinned' in self.h5_group.attrs:
                return bool(self.h5_group.attrs['Pinned'])
            return None

        @property
        def start_pinned(self)-> bool | None:
            """
            :return: True if the start of the annotation is pinned, otherwise False. If not present, returns None.
            :rtype: :obj:`bool` or None
            """
            if 'StartPinned' in self.h5_group.attrs:
                return bool(self.h5_group.attrs['StartPinned'])
            return None

        @property
        def end_pinned(self) -> bool | None:
            """
            :return: True if the end of the annotation is pinned, otherwise False. If not present, returns None.
            :rtype: :obj:`bool` or None
            """
            if 'EndPinned' in self.h5_group.attrs:
                return bool(self.h5_group.attrs['EndPinned'])
            return None

        @property
        def arrow(self) -> bool | None:
            """
            :return: True if the annotation has an arrow head, otherwise False. If not present, returns None.
            :rtype: :obj:`bool` or None
            """
            if 'Arrow' in self.h5_group.attrs:
                return bool(self.h5_group.attrs['Arrow'])
            return None

        @property
        def pen_color(self) -> np.ndarray[np.int32] | None:
            """
            :return: The pen color of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.ndarray` of shape (5,) with dtype :obj:`numpy.int32` or None
            """
            if 'PenColour' in self.h5_group.attrs:
                return self.h5_group.attrs['PenColour']
            return None

        @property
        def pen_style(self) -> np.int32 | None:
            """
            :return: The pen style of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.int32` or None
            """
            if 'PenStyle' in self.h5_group.attrs:
                return self.h5_group.attrs['PenStyle']
            return None

        @property
        def pen_width(self) -> np.float64 | None:
            """
            :return: The pen width of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.float64` or None
            """
            if 'PenWidth' in self.h5_group.attrs:
                return self.h5_group.attrs['PenWidth']
            return None

        @property
        def rect(self) -> np.ndarray[np.float64] | None:
            """
            :return: The rectangle of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.ndarray` of shape (4,) with dtype :obj:`numpy.float64` or None
            """
            if 'Rect' in self.h5_group.attrs:
                return self.h5_group.attrs['Rect']
            return None

        @property
        def line(self) -> np.ndarray[np.float64] | None:
            """
            :return: The line of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.ndarray` of shape (4,) with dtype :obj:`numpy.float64` or None
            """
            if 'Line' in self.h5_group.attrs:
                return self.h5_group.attrs['Line']
            return None

        @property
        def brush_color(self) -> np.ndarray[np.int32] | None:
            """
            :return: The brush color of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.ndarray` of shape (5,) with dtype :obj:`numpy.int32` or None
            """
            if 'BrushColour' in self.h5_group.attrs:
                return self.h5_group.attrs['BrushColour']
            return None 

        @property
        def rotation(self) -> np.float64 | None:
            """
            :return: The rotation of the annotation. If not present, returns None.
            :rtype: :obj:`numpy.float64` or None
            """
            if 'Rotation' in self.h5_group.attrs:
                return self.h5_group.attrs['Rotation']
            return None  
        
        @property
        def text(self) -> str | None:
            """
            :return: The text of the annotation. If not present, returns None.
            :rtype: :obj:`str` or None
            """
            if 'Text' in self.h5_group.attrs:
                return utils.ensure_str(self.h5_group.attrs['Text'])
            return None
        
        @property
        def html(self) -> str | None:
            """
            :return: The HTML of the annotation. If not present, returns None.
            :rtype: :obj:`str` or None
            """
            if 'Html' in self.h5_group.attrs:
                return utils.ensure_str(self.h5_group.attrs['Html'])
            return None
        
        @property
        def font(self) -> base.Font | None:
            """
            :return: The font of the annotation. If not present, returns None.
            :rtype: :obj:`base.Font` or None
            """
            if 'Font' in self.h5_group.attrs:
                return base.Font(self.h5_group.attrs['Font'])
            return None

    def __init__(self, h5_group):
         super(GraphicsItem, self).__init__(h5_group)

    def __str__(self):
        return "id: {}, type: {}, pos: {}, size: {}".format(self.id, self.type, self.pos, self.size)

    @staticmethod
    def create(class_, h5_group) -> 'GraphicsItem':
        """
        Creates a new graphics item of the specified type.
        
        :param class_: The class of the graphics item to create.
        :type class_: GraphicsItem
        :param h5_group: The HDF5 group corresponding to the graphics item.
        :type h5_group: h5py.Group
        :return: The newly created graphics item.
        :rtype: GraphicsItem
        """
        return class_(h5_group)

    @property
    def type(self) -> Type:
        """
        :return: The type of the graphics item.
        :rtype: :obj:`Type`
        """
        return GraphicsItem.Type(self.h5_group.attrs['Type'])

    @property
    def linked_ids(self) -> list[str]:
        """
        The list of linked IDs.

        :getter: Returns the list of linked IDs.
        :rtype: :obj:`list` of :obj:`str`

        :setter: Sets the list of linked IDs.
        :param new_linked_ids: The new list of linked IDs.
        :type new_linked_ids: :obj:`list` of :obj:`str`
        """
        return list(self.h5_group.attrs['LinkedIDs']) if 'LinkedIDs' in self.h5_group.attrs else [] 

    @linked_ids.setter
    def linked_ids(self, new_linked_ids: Sequence):
        assert isinstance(new_linked_ids, Sequence)
        self.h5_group.attrs['LinkedIDs'] = [utils.check_uuid_str(x) for x in new_linked_ids]

    @property
    def parent_item_id(self) -> str | None:
        """
        The parent item ID.

        :getter: Returns the parent item ID.
        :rtype: :obj:`str` or None if not present.

        :setter: Sets the parent item ID.
        :param new_parent_item_id: The new parent item ID.
        :type new_parent_item_id: :obj:`str` or None
        """
        if 'ParentItemID' in self.h5_group.attrs:
            id_ = self.h5_group.attrs['ParentItemID']
            if not isinstance(id_, str):
                return id_.decode('ascii')
            return id_

    @parent_item_id.setter
    def parent_item_id(self, new_parent_item_id):
        if new_parent_item_id is None:
            del self.h5_group.attrs['ParentItemID']
        else:
            self.h5_group.attrs['ParentItemID'] = utils.check_uuid_str(new_parent_item_id)

    @property
    def rotation(self) -> np.float64:
        """
        The rotation of the graphics item in degrees.

        :getter: Returns the rotation of the graphics item.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the rotation of the graphics item.
        :param new_rotation: The new rotation of the graphics item.
        :type new_rotation: :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Rotation']

    @rotation.setter
    def rotation(self, new_rotation):
        self.h5_group.attrs['Rotation'] = new_rotation

    @property
    def z_value(self) -> np.float64:
        """
        The Z value of the graphics item.

        :getter: Returns the Z value of the graphics item.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the Z value of the graphics item.
        :param new_zvalue: The new Z value of the graphics item.
        :type new_zvalue: :obj:`numpy.float64`
        """
        return self.h5_group.attrs['ZValue']

    @z_value.setter
    def z_value(self, new_zvalue):
        self.h5_group.attrs['ZValue'] = new_zvalue

    @property
    def pos(self) -> np.ndarray[np.float64]:
        """
        The position of the graphics item. X is at index 0, Y is at index 1 of the array.

        :getter: Returns the position of the graphics item.
        :rtype: :obj:`numpy.ndarray` of shape (2,) with dtype :obj:`numpy.float64`

        :setter: Sets the position of the graphics item.
        :param new_pos: The new position of the graphics item.
        :type new_pos: :obj:`Iterable` of length 2 of :obj:`numpy.float64`
        """
        return self.h5_group.attrs['Pos']

    @pos.setter
    def pos(self, new_pos: Iterable[np.float64]):
        assert len(new_pos) == 2
        self.h5_group.attrs.modify('Pos', np.array(new_pos, dtype=np.float64))
        g = self.h5_group.attrs['Geometry']
        g[0] = new_pos[0]
        g[1] = new_pos[1]
        self.h5_group.attrs.modify('Geometry', g)

    @property
    def size(self) -> tuple[np.float64, np.float64]:
        """
        The size of the graphics item. Width is at index 0, height is at index 1 of the tuple.

        :getter: Returns the size of the graphics item.
        :rtype: :obj:`tuple` of length 2 of :obj:`numpy.float64`

        :setter: Sets the size of the graphics item.
        :param new_size: The new size of the graphics item.
        :type new_size: :obj:`Iterable` of length 2 of :obj:`numpy.float64`
        """
        g = self.h5_group.attrs['Geometry']
        return (g[2], g[3])

    @size.setter
    def size(self, new_size: Iterable[np.float64]):
        assert len(new_size) == 2
        g = self.h5_group.attrs['Geometry']
        g[2] = new_size[0]
        g[3] = new_size[1]
        self.h5_group.attrs.modify('Geometry', g)

    @property
    def annotations(self) -> Annotation.List:
        """
        :return: The list of annotations.
        :rtype: :obj:`Annotation.List`
        """
        return GraphicsItem.Annotation.List(self.h5_group)
    
    def _get_color(self, group_name, attr_name):
        """
        Gets the color attribute from the specified group.

        :param group_name: The name of the group.
        :type group_name: :obj:`str`
        :param attr_name: The name of the attribute.
        :type attr_name: :obj:`str`
        :return: The color attribute in the format '#RRGGBBAA'.
        :rtype: :obj:`str`
        """
        color = self.h5_group[group_name].attrs[attr_name]
        return '#{:02X}{:02X}{:02X}{:02X}'.format(color[0], color[1], color[2], color[3])  

    def _set_color(self, group_name, attr_name, new_color):
        color = self.h5_group[group_name].attrs[attr_name]
        color[0] = int(new_color[1:3], 16)
        color[1] = int(new_color[3:5], 16)
        color[2] = int(new_color[5:7], 16)
        if len(new_color) >= 9:
            color[3] = int(new_color[7:9], 16)
        else:
            color[3] = 255
        self.h5_group[group_name].attrs[attr_name] = color

class NMRSpectrumGraphicsItem(GraphicsItem):
    """
    Represents an NMR spectrum graphics item stored within an HDF5 group.
    """

    class PlotType2D(IntEnum):
        """
        Enumeration representing the types of 2D plots.
        """
        RASTER = 0
        CONTOURS = 1
        OVERLAPPED = 2
        VER_STACK = 3
        HOR_STACK = 4

    class Print1DMode(IntEnum):
        """
        An enumeration that represents the different modes for printing 1D data.

        - ALL: Prints the data as a single line, displaying all points.
        - SKIP: Reduces the resolution by skipping some data points to provide a simplified view.
        - SPLIT: Divides the data into segments.
        """
        ALL = 0 
        SKIP = 1
        SPLIT = 2

    @property
    def spec_data_list(self) -> list[data.NMRSpectrum]:
        """
        :return: The list of spectra.
        :rtype: :obj:`list` of :obj:`data.NMRSpectrum`
        """
        result = []
        for spec_id in self.h5_group['NMRPlot/DataStore'].attrs['Spectra']:
            for spec in data.NMRSpectrum.List(self.h5_group.parent.parent['NMR']):
                if spec_id == spec.id:
                    result.append(spec)
        return result

    def spec_data(self, id: int | str = 0) -> data.NMRSpectrum | None:
        """
        Gets spectrum data by 'id', where 'id' is either an index or UUID string.

        :param id: The index or UUID string of the spectrum data.
        :type id: :obj:`int` or :obj:`str`
        :return: The spectrum data.
        :rtype: :obj:`NMRSpectrum` or None if not found.
        """
        specs = self.spec_data_list
        if isinstance(id, int) or str(id).isnumeric():
            id = int(id)
            if 0 <= id and id < len(specs):
                return specs[id]
            return
        for spec in specs:
            if spec.id == id:
                return spec

    @property
    def header(self) -> str:
        """
        The header of the spectrum.

        :getter: Returns the header of the spectrum.
        :rtype: :obj:`str`

        :setter: Sets the header of the spectrum.
        :param new_header: The new header of the spectrum.
        :type new_header: :obj:`str`
        :raises TypeError: If the new_header argument is not str or bytes.
        """
        return utils.ensure_str(self.h5_group['NMRPlot'].attrs['Header'])

    @header.setter
    def header(self, new_header):
        if isinstance(new_header, bytes):
            new_header = new_header.decode('utf-8')
        if not isinstance(new_header, str):
            raise TypeError("The new_header argument is expected to be str or bytes")
        self.h5_group['NMRPlot'].attrs['Header'] = new_header

    def _get_bool(self, attr_name):   
        return bool(self.h5_group['NMRPlot'].attrs[attr_name])

    def _set_bool(self, attr_name, new_value):
         self.h5_group['NMRPlot'].attrs[attr_name] = np.uint8(1 if new_value else 0)
   
    @property
    def show_x_axis(self) -> bool:
        """
        Whether to show the X axis.

        :getter: Returns True if the X axis is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the X axis.
        :param new_show: True if the X axis is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('XAxis')

    @show_x_axis.setter
    def show_x_axis(self, new_value):
        self._set_bool('XAxis', new_value)

    @property
    def show_y_axis(self) -> bool:
        """
        Whether to show the Y axis.

        :getter: Returns True if the Y axis is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the Y axis.
        :param new_show: True if the Y axis is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('YAxis')

    @show_y_axis.setter
    def show_y_axis(self, new_value):
        self._set_bool('YAxis', new_value)

    @property
    def active_bold(self) -> bool:
        """
        Whether to show the active spectrum in bold.

        :getter: Returns True if the active spectrum is shown in bold, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the active spectrum in bold.
        :param new_show: True if the active spectrum is to be shown in bold, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ActiveBold')

    @active_bold.setter
    def active_bold(self, new_value):
        self._set_bool('ActiveBold', new_value)

    @property
    def antialiasing(self) -> bool:
        """
        Whether to use antialiasing.

        :getter: Returns True if antialiasing is used, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to use antialiasing.
        :param new_show: True if antialiasing is to be used, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('Antialiasing')

    @antialiasing.setter
    def antialiasing(self, new_value):
        self._set_bool('Antialiasing', new_value)

    @property
    def color_cont(self) -> bool:
        """
        Whether to use color contours.

        :getter: Returns True if color contours are used, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to use color contours.
        :param new_show: True if color contours are to be used, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ColourCont')

    @color_cont.setter
    def color_cont(self, new_value):
        self._set_bool('ColourCont', new_value)

    @property
    def mix_fid_spec(self) -> bool:
        """
        Whether to mix FID and spectra.

        :getter: Returns True if FID and spectra are mixed, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to mix FID and spectra.
        :param new_show: True if FID and spectra are to be mixed, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('MixFidSpec')

    @mix_fid_spec.setter
    def mix_fid_spec(self, new_value):
        self._set_bool('MixFidSpec', new_value)

    @property
    def plot_2d_color_gradient(self) -> bool:
        """
        Whether to plot 2D color gradient.

        :getter: Returns True if 2D color gradient is plotted, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to plot 2D color gradient.
        :param new_show: True if 2D color gradient is to be plotted, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('Plot2DColorGradient')

    @plot_2d_color_gradient.setter
    def plot_2d_color_gradient(self, new_value):
        self._set_bool('Plot2DColorGradient', new_value)

    @property
    def show_header(self) -> bool:
        """
        Whether to show the header.

        :getter: Returns True if the header is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the header.
        :param new_show: True if the header is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ShowHeader')

    @show_header.setter
    def show_header(self, new_value):
        self._set_bool('ShowHeader', new_value)

    @property
    def show_integrals_multiplets(self) -> bool:
        """
        Whether to show integrals/multiplets.

        :getter: Returns True if integrals/multiplets are shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show integrals/multiplets.
        :param new_show: True if integrals/multiplets are to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """ 
        return self._get_bool('ShowIntegralsMultiplets')

    @show_integrals_multiplets.setter
    def show_integrals_multiplets(self, new_value):
        self._set_bool('ShowIntegralsMultiplets', new_value)

    @property
    def show_peak_models(self) -> bool:
        """
        Whether to show peak models.

        :getter: Returns True if peak models are shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show peak models.
        :param new_show: True if peak models are to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ShowPeakModels')

    @show_peak_models.setter
    def show_peak_models(self, new_value):
        self._set_bool('ShowPeakModels', new_value)

    @property
    def show_peak_residuals(self) -> bool:
        """
        Whether to show peak residuals.

        :getter: Returns True if peak residuals are shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show peak residuals.
        :param new_show: True if peak residuals are to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ShowPeakResiduals')

    @show_peak_residuals.setter
    def show_peak_residuals(self, new_value):
        self._set_bool('ShowPeakResiduals', new_value)

    @property
    def show_peak_sum(self) -> bool:
        """
        Whether to show peak sum.

        :getter: Returns True if peak sum is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show peak sum.
        :param new_show: True if peak sum is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ShowPeakSum')

    @show_peak_sum.setter
    def show_peak_sum(self, new_value):
        self._set_bool('ShowPeakSum', new_value)

    @property
    def show_peaks(self) -> bool:
        """
        Whether to show peaks.

        :getter: Returns True if peaks are shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show peaks.
        :param new_show: True if peaks are to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('ShowPeaks')

    @show_peaks.setter
    def show_peaks(self, new_value):
        self._set_bool('ShowPeaks', new_value)

    @property
    def show_x_grid(self) -> bool:
        """
        Whether to show the X grid.

        :getter: Returns True if the X grid is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the X grid.
        :param new_show: True if the X grid is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('XGrid')

    @show_x_grid.setter
    def show_x_grid(self, new_value):
        self._set_bool('XGrid', new_value)
    
    @property
    def show_y_axis_2d(self) -> bool:
        """
        Whether to show the Y axis of 2D spectra.

        :getter: Returns True if the Y axis of 2D spectra is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the Y axis of 2D spectra.
        :param new_show: True if the Y axis of 2D spectra is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('YAxis2D')

    @show_y_axis_2d.setter
    def show_y_axis_2d(self, new_value):
        self._set_bool('YAxis2D', new_value)

    @property
    def y_axis_right(self) -> bool:
        """
        Whether to show the Y axis on the right.

        :getter: Returns True if the Y axis is shown on the right, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the Y axis on the right.
        :param new_show: True if the Y axis is to be shown on the right, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('YAxisRight')

    @y_axis_right.setter
    def y_axis_right(self, new_value):
        self._set_bool('YAxisRight', new_value)

    @property
    def show_y_grid(self) -> bool:
        """
        Whether to show the Y grid.

        :getter: Returns True if the Y grid is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the Y grid.
        :param new_show: True if the Y grid is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('YGrid')

    @show_y_grid.setter
    def show_y_grid(self, new_value):
        self._set_bool('YGrid', new_value)

    @property
    def y_outside_labels(self) -> bool:
        """
        Whether to draw labels on the left side of the Y axis.

        :getter: Returns True if labels are drawn on the left side of the Y axis, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to draw labels on the left side of the Y axis.
        :param new_show: True if labels are to be drawn on the left side of the Y axis, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('YOutsideLabels')

    @y_outside_labels.setter
    def y_outside_labels(self, new_value):
        self._set_bool('YOutsideLabels', new_value)

    @property
    def show_legend(self) -> bool:
        """
        Whether to show the legend.

        :getter: Returns True if the legend is shown, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show the legend.
        :param new_show: True if the legend is to be shown, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('hasLegend')

    @show_legend.setter
    def show_legend(self, new_value):
        self._set_bool('hasLegend', new_value)

    @property
    def has_x_extra_ticks(self) -> bool:
        """
        Whether to show extra ticks on the X axis.

        :getter: Returns True if extra ticks are shown on the X axis, otherwise False.
        :rtype: :obj:`bool`
        
        :setter: Sets whether to show extra ticks on the X axis.
        :param new_show: True if extra ticks are to be shown on the X axis, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('hasXExtraTicks')

    @has_x_extra_ticks.setter
    def has_x_extra_ticks(self, new_value):
        self._set_bool('hasXExtraTicks', new_value)

    @property
    def has_y_extra_ticks(self) -> bool:
        """
        Whether to show extra ticks on the Y axis.

        :getter: Returns True if extra ticks are shown on the Y axis, otherwise False.
        :rtype: :obj:`bool`

        :setter: Sets whether to show extra ticks on the Y axis.
        :param new_show: True if extra ticks are to be shown on the Y axis, otherwise False.
        :type new_show: :obj:`bool`
        """
        return self._get_bool('hasYExtraTicks')

    @has_y_extra_ticks.setter
    def has_y_extra_ticks(self, new_value):
        self._set_bool('hasYExtraTicks', new_value)

    @property
    def plot_1d_color(self) -> str:
        """
        The color of 1D plot.

        :getter: Returns the color of 1D plot.
        :rtype: :obj:`str`

        :setter: Sets the color of 1D plot.
        :param new_color: The new color of 1D plot.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'Plot1DColor')
    
    @plot_1d_color.setter
    def plot_1d_color(self, new_color):
        self._set_color('NMRPlot', 'Plot1DColor', new_color)

    @property
    def plot_2d_neg_color(self) -> str:
        """
        The color of negative 2D plot.

        :getter: Returns the color of negative 2D plot.
        :rtype: :obj:`str`

        :setter: Sets the color of negative 2D plot.
        :param new_color: The new color of negative 2D plot.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'Plot2DNegColor')
    
    @plot_2d_neg_color.setter
    def plot_2d_neg_color(self, new_color):
        self._set_color('NMRPlot', 'Plot2DNegColor', new_color)

    @property
    def plot_2d_pos_color(self) -> str:
        """
        The color of positive 2D plot.

        :getter: Returns the color of positive 2D plot.
        :rtype: :obj:`str`

        :setter: Sets the color of positive 2D plot.
        :param new_color: The new color of positive 2D plot.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'Plot2DPosColor')
    
    @plot_2d_pos_color.setter
    def plot_2d_pos_color(self, new_color):
        self._set_color('NMRPlot', 'Plot2DPosColor', new_color)

    @property
    def integral_curve_color(self) -> str:
        """
        The color of integral curve.

        :getter: Returns the color of integral curve.
        :rtype: :obj:`str`

        :setter: Sets the color of integral curve.
        :param new_color: The new color of integral curve.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'IntegralCurveColor')
    
    @integral_curve_color.setter
    def integral_curve_color(self, new_color):
        self._set_color('NMRPlot', 'IntegralCurveColor', new_color)

    @property
    def mult_intg_label_color(self) -> str:
        """
        The color of multiplet integral label.

        :getter: Returns the color of multiplet integral label.
        :rtype: :obj:`str`

        :setter: Sets the color of multiplet integral label.
        :param new_color: The new color of multiplet integral label.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'MultIntgLabelColor')
    
    @mult_intg_label_color.setter
    def mult_intg_label_color(self, new_color):
        self._set_color('NMRPlot', 'MultIntgLabelColor', new_color)
  
    @property
    def peak_shape_color(self) -> str:
        """
        The color of peak shape.

        :getter: Returns the color of peak shape.
        :rtype: :obj:`str`

        :setter: Sets the color of peak shape.
        :param new_color: The new color of peak shape.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'PeakShapeColor')
    
    @peak_shape_color.setter
    def peak_shape_color(self, new_color):
        self._set_color('NMRPlot', 'PeakShapeColor', new_color)

    @property
    def x_axis_color(self) -> str:
        """
        The color of X axis.
        
        :getter: Returns the color of X axis.
        :rtype: :obj:`str`

        :setter: Sets the color of X axis.
        :param new_color: The new color of X axis.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'XAxisColor')
    
    @x_axis_color.setter
    def x_axis_color(self, new_color):
        self._set_color('NMRPlot', 'XAxisColor', new_color)
    
    @property
    def y_axis_color(self) -> str:
        """
        The color of Y axis.

        :getter: Returns the color of Y axis.
        :rtype: :obj:`str`
        
        :setter: Sets the color of Y axis.
        :param new_color: The new color of Y axis.
        :type new_color: :obj:`str`
        """
        return self._get_color('NMRPlot', 'YAxisColor')
    
    @y_axis_color.setter
    def y_axis_color(self, new_color):
        self._set_color('NMRPlot', 'YAxisColor', new_color)

    def _get_number(self, attr_name):   
        return self.h5_group['NMRPlot'].attrs[attr_name]

    def _set_number(self, attr_name, new_value, value_type):
         self.h5_group['NMRPlot'].attrs[attr_name] = value_type(new_value)
   
    @property
    def floor(self) -> np.float64:
        """
        The 2D plot floor.

        :getter: Returns the 2D plot floor.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the 2D plot floor.
        :param new_value: The new 2D plot floor.
        :type new_value: :obj:`numpy.float64`
        """
        return self._get_number('Floor')

    @floor.setter
    def floor(self, new_value):
        self._set_number('Floor', new_value, np.float64)

    @property
    def integral_label_v_shift(self) -> np.float64:
        """
        The vertical shift of integral label.

        :getter: Returns the vertical shift of integral label.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the vertical shift of integral label.
        :param new_value: The new vertical shift of integral label.
        :type new_value: :obj:`numpy.float64`
        """
        return self._get_number('IntegralLabelVShift')

    @integral_label_v_shift.setter
    def integral_label_v_shift(self, new_value):
        self._set_number('IntegralLabelVShift', new_value, np.float64)

    @property
    def multiplet_label_v_shift(self) -> np.float64:
        """
        The vertical shift of multiplet label.

        :getter: Returns the vertical shift of multiplet label.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the vertical shift of multiplet label.
        :param new_value: The new vertical shift of multiplet label.
        :type new_value: :obj:`numpy.float64`
        """
        return self._get_number('MultipletLabelVShift')

    @multiplet_label_v_shift.setter
    def multiplet_label_v_shift(self, new_value):
        self._set_number('MultipletLabelVShift', new_value, np.float64)

    @property
    def separation_inc(self) -> np.float64:
        """
        Overlapped spectra separation increment.

        :getter: Returns the overlapped spectra separation increment.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the overlapped spectra separation increment.
        :param new_value: The new overlapped spectra separation increment.
        :type new_value: :obj:`numpy.float64`
        """
        return self._get_number('SeparationInc')

    @separation_inc.setter
    def separation_inc(self, new_value):
        self._set_number('SeparationInc', new_value, np.float64)

    @property
    def tilt_inc(self) -> np.float64:
        """
        Overlapped spectra tilt increment.

        :getter: Returns the overlapped spectra tilt increment.
        :rtype: :obj:`numpy.float64`

        :setter: Sets the overlapped spectra tilt increment.
        :param new_value: The new overlapped spectra tilt increment.
        :type new_value: :obj:`numpy.float64`
        """
        return self._get_number('TiltInc')

    @tilt_inc.setter
    def tilt_inc(self, new_value):
        self._set_number('TiltInc', new_value, np.float64)

    @property
    def mult_intg_label_digits(self) -> np.int32:
        """
        The number of digits of multiplet/integral label.

        :getter: Returns the number of digits of multiplet/integral label.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of digits of multiplet/integral label.
        :param new_value: The new number of digits of multiplet/integral label.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('MultIntgLabelDigits')

    @mult_intg_label_digits.setter
    def mult_intg_label_digits(self, new_value):
        self._set_number('MultIntgLabelDigits', new_value, np.int32)

    @property
    def mult_intg_pos_digits(self) -> np.int32:
        """
        The number of digits of multiplet/integral position.

        :getter: Returns the number of digits of multiplet/integral position.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of digits of multiplet/integral position.
        :param new_value: The new number of digits of multiplet/integral position.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('MultIntgPosDigits')

    @mult_intg_pos_digits.setter
    def mult_intg_pos_digits(self, new_value):
        self._set_number('MultIntgPosDigits', new_value, np.int32)

    @property
    def multi_plot_type_2d(self) -> PlotType2D:
        """
        The plot type of 2D spectra when multiple spectra are present.

        :getter: Returns the plot type of 2D spectra.
        :rtype: :obj:`PlotType2D`

        :setter: Sets the plot type of 2D spectra.
        :param new_value: The new plot type of 2D spectra.
        :type new_value: :obj:`PlotType2D`
        """
        return NMRSpectrumGraphicsItem.PlotType2D(self._get_number('MultiPlotType2D'))

    @multi_plot_type_2d.setter
    def multi_plot_type_2d(self, new_value):
        self._set_number('MultiPlotType2D', new_value, np.int8)

    @property
    def n_levels(self) -> np.int32:
        """
        The number of contour levels.

        :getter: Returns the number of contour levels.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of contour levels.
        :param new_value: The new number of contour levels.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('NLevels')

    @n_levels.setter
    def n_levels(self, new_value):
        self._set_number('NLevels', new_value, np.int32)

    @property
    def n_x_extra_ticks(self) -> np.int32:
        """
        The number of extra ticks on the X axis.

        :getter: Returns the number of extra ticks on the X axis.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of extra ticks on the X axis.
        :param new_value: The new number of extra ticks on the X axis.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('NXExtraTicks')

    @n_x_extra_ticks.setter
    def n_x_extra_ticks(self, new_value):
        self._set_number('NXExtraTicks', new_value, np.int32)

    @property
    def n_y_extra_ticks(self) -> np.int32:
        """
        The number of extra ticks on the Y axis.

        :getter: Returns the number of extra ticks on the Y axis.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of extra ticks on the Y axis.
        :param new_value: The new number of extra ticks on the Y axis.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('NYExtraTicks')

    @n_y_extra_ticks.setter
    def n_y_extra_ticks(self, new_value):
        self._set_number('NYExtraTicks', new_value, np.int32)

    @property
    def plot_1d_width(self) -> np.int32:
        """
        The pen width of 1D plot.

        :getter: Returns the width of 1D plot.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the width of 1D plot.
        :param new_value: The new width of 1D plot.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('Plot1DWidth')

    @plot_1d_width.setter
    def plot_1d_width(self, new_value):
        self._set_number('Plot1DWidth', new_value, np.int32)

    @property
    def plot_2d_width(self) -> np.int32:
        """
        The pen width of 2D plot.

        :getter: Returns the width of 2D plot.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the width of 2D plot.
        :param new_value: The new width of 2D plot.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('Plot2DWidth')

    @plot_2d_width.setter
    def plot_2d_width(self, new_value):
        self._set_number('Plot2DWidth', new_value, np.int32)

    @property
    def plot_type_2d(self) -> PlotType2D:
        """
        The plot type of 2D spectra.

        :getter: Returns the plot type of 2D spectra.
        :rtype: :obj:`PlotType2D`

        :setter: Sets the plot type of 2D spectra.
        :param new_value: The new plot type of 2D spectra.
        :type new_value: :obj:`PlotType2D`
        """
        return NMRSpectrumGraphicsItem.PlotType2D(self._get_number('PlotType2D'))

    @plot_type_2d.setter
    def plot_type_2d(self, new_value):
        self._set_number('PlotType2D', new_value, np.int8)

    @property
    def pos_neg(self) -> np.int32:
        """
        Indicates the nature of the contour lines plotted on the 2D spectrum - whether they represent 
        positive values, negative values, or both.

        - 0: Positive contour lines only
        - 1: Both positive and negative contour lines (bipolar)
        - 2: Negative contour lines only

        :getter: Returns the setting indicating which contour lines (positive/negative/both) are being plotted.
        :rtype: :obj:`numpy.int32`

        :setter: Updates the setting for which contour lines (positive/negative/both) to plot.
        :param new_value: Indicates whether to plot positive contours, negative contours, or both.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('PosNeg')

    @pos_neg.setter
    def pos_neg(self, new_value):
        self._set_number('PosNeg', new_value, np.int32)

    @property
    def print_line_width(self) -> np.int32:
        """
        The line width of printed spectra.

        :getter: Returns the line width of printed spectra.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the line width of printed spectra.
        :param new_value: The new line width of printed spectra.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('PrintLineWidth')

    @print_line_width.setter
    def print_line_width(self, new_value):
        self._set_number('PrintLineWidth', new_value, np.int32)

    @property
    def print_mode(self) -> Print1DMode:
        """
        The print mode of 1D spectra.

        :getter: Returns the print mode of 1D spectra.
        :rtype: :obj:`Print1DMode`

        :setter: Sets the print mode of 1D spectra.
        :param new_value: The new print mode of 1D spectra.
        :type new_value: :obj:`Print1DMode`
        """
        return NMRSpectrumGraphicsItem.Print1DMode(self._get_number('PrintMode'))

    @print_mode.setter
    def print_mode(self, new_value: Print1DMode):
        self._set_number('PrintMode', new_value, np.int32)

    @property
    def x_ticks(self) -> np.int32:
        """
        The number of ticks on the X axis.

        :getter: Returns the number of ticks on the X axis.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of ticks on the X axis.
        :param new_value: The new number of ticks on the X axis.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('XTicks')

    @x_ticks.setter
    def x_ticks(self, new_value):
        self._set_number('XTicks', new_value, np.int32)

    @property
    def y_ticks(self) -> np.int32:
        """
        The number of ticks on the Y axis.

        :getter: Returns the number of ticks on the Y axis.
        :rtype: :obj:`numpy.int32`

        :setter: Sets the number of ticks on the Y axis.
        :param new_value: The new number of ticks on the Y axis.
        :type new_value: :obj:`numpy.int32`
        """
        return self._get_number('YTicks')

    @y_ticks.setter
    def y_ticks(self, new_value):
        self._set_number('YTicks', new_value, np.int32)

    def _get_font(self, attr_name) -> base.Font:
        return base.Font(self.h5_group['NMRPlot'].attrs[attr_name])

    def _set_font(self, attr_name, new_font: base.Font):
        self.h5_group['NMRPlot'].attrs[attr_name] = str(new_font)

    @property
    def header_font(self) -> base.Font:
        """
        The font of header.

        :getter: Returns the font of header.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of header.
        :param new_font: The new font of header.
        :type new_font: :obj:`base.Font`
        """
        return self._get_font('HeaderFont')
    
    @header_font.setter
    def header_font(self, new_value):
        self._set_font('HeaderFont', new_value)

    @property
    def j_tree_label_font(self) -> base.Font:
        """
        The font of J tree label.

        :getter: Returns the font of J tree label.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of J tree label.
        :param new_font: The new font of J tree label.
        :type new_font: :obj:`base.Font`
        """
        return self._get_font('JTreeLabelFont')
    
    @j_tree_label_font.setter
    def j_tree_label_font(self, new_value):
        self._set_font('JTreeLabelFont', new_value)

    @property
    def mult_intg_label_font(self) -> base.Font:
        """
        The font of multiplet integral label.

        :getter: Returns the font of multiplet integral label.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of multiplet integral label.
        :param new_font: The new font of multiplet integral label.
        :type new_font: :obj:`base.Font`
        """
        return self._get_font('MultIntgLabelFont')
    
    @mult_intg_label_font.setter
    def mult_intg_label_font(self, new_value):
        self._set_font('MultIntgLabelFont', new_value)

    @property
    def peak_label_font(self) -> base.Font:
        """
        The font of peak label.

        :getter: Returns the font of peak label.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of peak label.
        :param new_font: The new font of peak label.
        :type new_font: :obj:`base.Font`
        """
        return self._get_font('PeakLabelFont')
    
    @peak_label_font.setter
    def peak_label_font(self, new_value):
        self._set_font('PeakLabelFont', new_value)

    @property
    def x_font(self) -> base.Font:
        """
        The font of X axis.

        :getter: Returns the font of X axis.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of X axis.
        :param new_font: The new font of X axis.
        :type new_font: :obj:`base.Font`
        """
        return self._get_font('XFont')
    
    @x_font.setter
    def x_font(self, new_value):
        self._set_font('XFont', new_value)

    @property
    def y_font(self) -> base.Font:
        """
        The font of Y axis.

        :getter: Returns the font of Y axis.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of Y axis.
        :param new_font: The new font of Y axis.
        :type new_font: :obj:`base.Font`
        """
        return self._get_font('YFont')
    
    @y_font.setter
    def y_font(self, new_value):
        self._set_font('YFont', new_value)

class TableGraphicsItem(GraphicsItem):
    """Base class for table graphics items"""
    
    class RowInfo(base.H5Group):
        """
        Represents a row information of a table graphics item.
        """

        class List(base.GroupList):
            """
            Represents a list of row information.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'RowInfo_values', TableGraphicsItem.RowInfo)

        @property
        def custom_column_ids(self) -> np.ndarray[np.int32]:
            """
            The custom column IDs of the row. Unlike the standard column IDs, the custom column IDs are negative integers.

            :getter: Returns the custom column IDs of the row.
            :rtype: :obj:`numpy.ndarray` of :obj:`numpy.int32`

            :setter: Sets the custom column IDs of the row.
            :param new_value: The new custom column IDs of the row.
            :type new_value: :obj:`numpy.ndarray` of :obj:`numpy.int32`
            """
            return self.h5_group.attrs['CellCustomData_keys']

        @custom_column_ids.setter
        def custom_column_ids(self, value):
            self.h5_group.attrs['CellCustomData_keys'] = value

        @property
        def column_ids(self) -> np.ndarray[np.int32]:
            """
            The column IDs of the row.
            
            :getter: Returns the column IDs of the row.
            :rtype: :obj:`numpy.ndarray` of :obj:`numpy.int32`

            :setter: Sets the column IDs of the row.
            :param new_value: The new column IDs of the row.
            :type new_value: :obj:`numpy.ndarray` of :obj:`numpy.int32`
            """
            if 'ColIds' in self.h5_group.attrs:
                return self.h5_group.attrs['ColIds']
            else:
                return np.array([], dtype=np.int32)
        
        @column_ids.setter
        def column_ids(self, value):
            self.h5_group.attrs['ColIds'] = value

        @property
        def fonts(self) -> np.ndarray[np.bytes_]:
            """
            The fonts of the row.

            :getter: Returns the fonts of the row.
            :rtype: :obj:`numpy.ndarray` of :obj:`numpy.bytes_`

            :setter: Sets the fonts of the row.
            :param new_value: The new fonts of the row.
            :type new_value: :obj:`numpy.ndarray` of :obj:`numpy.bytes_`
            """
            if 'Fonts' in self.h5_group.attrs:
                return self.h5_group.attrs['Fonts']
            else:
                return np.array([], dtype=np.bytes_)
        
        @fonts.setter
        def fonts(self, fonts: Iterable[str]):
            self.h5_group.attrs['Fonts'] = fonts

        @property
        def custom_values(self) -> Iterable[Any] | None:
            """
            The custom values of the row.

            :getter: Returns the custom values of the row.
            :rtype: :obj:`Iterable` of :obj:`Any` | None

            :setter: Sets the custom values of the row.
            :param new_value: The new custom values of the row.
            :type new_value: :obj:`Iterable` of :obj:`Any`
            """
            if 'CellCustomData_values' in self.h5_group.attrs:
                return self.h5_group.attrs['CellCustomData_values']
            elif 'CellCustomData_values' in self.h5_group:
                return base.AttrList(self.h5_group['CellCustomData_values'])
            
        @custom_values.setter
        def custom_values(self, values: Iterable):
            if 'CellCustomData_values' in self.h5_group.attrs:
                del self.h5_group.attrs['CellCustomData_values']
            custom_values = base.AttrList(self.h5_group.require_group('CellCustomData_values'))
            custom_values.clear()
            custom_values.append(values)

    class ColumnInfo(base.H5Group):
        """
        Represents a column information of a table graphics item.
        """

        class List(base.GroupList):
            """
            Represents a list of column information.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'ColInfo', TableGraphicsItem.ColumnInfo)

        @property
        def digits(self) -> np.int32 | None:
            """
            :return: The number of digits of the column.
            :rtype: :obj:`numpy.int32` | None
            """
            if 'Digits' in self.h5_group.attrs: 
                return self.h5_group.attrs['Digits']

        @property
        def col_id(self) -> np.int32 | None:
            """
            :return: The ID of the column.
            :rtype: :obj:`numpy.int32` | None
            """
            if 'Type' in self.h5_group.attrs: 
                return self.h5_group.attrs['Type']

        @property
        def units(self) -> base.Units | None:
            """
            :return: The units of the column.
            :rtype: :obj:`Units` | None
            """
            if 'Units' in self.h5_group.attrs: 
                return base.Units(self.h5_group.attrs['Units'])

        @property
        def text_alignment(self) -> np.int32 | None:
            """
            :return: The text alignment of the column, which is a combination of :obj:`Qt.AlignmentFlag` values.
            :rtype: :obj:`numpy.int32` | None
            """
            if 'TextAlignment' in self.h5_group.attrs: 
                return self.h5_group.attrs['TextAlignment']
        
        @property
        def custom_id(self) -> str | None:
            """
            :return: The custom UUID string of the column if it is a custom column.
            :rtype: :obj:`str` | None
            """
            if 'CustomID' in self.h5_group.attrs: 
                return utils.check_uuid_str(self.h5_group.attrs['CustomID'])
            
        @property
        def custom_title(self) -> str | None:
            """
            :return: The custom title of the column if it is a custom column.
            :rtype: :obj:`str` | None
            """ 
            if 'CustomTitle' in self.h5_group.attrs: 
                return utils.ensure_str(self.h5_group.attrs['CustomTitle'])

    @property
    def data_id(self) -> str:
        """
        The ID of the data that the table is associated with.
        
        :raises NotImplementedError: Must be overridden in subclass.
        """
        raise NotImplementedError("'data_id' must be overridden in subclass")

    def set_defaults(self):
        """Setting default values on creating a table item"""
        self.alternating_row_colors = False
        self.horizontal_header_visible = True
        self.vertical_header_visible = False
        self.page_split = True
        self.column_label = False

    @cached_property
    def horizontal_header(self) -> dict[str, Any]:
        """
        Decodes QByteArray bytes to dict.

        :return: The horizontal header information.
        :rtype: :obj:`dict` of :obj:`str` to :obj:`Any`
        """

        result = {}
        horizontalHeaderState = self.h5_group.attrs['HorizontalHeaderState']
        if horizontalHeaderState.startswith(b'{@bytes.hex:'):
            with io.BytesIO(bytes.fromhex(horizontalHeaderState[12:-1].decode('ascii'))) as buf:

                # Read version marker, version, orientation, sort indicator order, sort indicator section, and sort indicator shown
                result['versionMarker'], result['version'], result['orientation'], result['sortIndicatorOrder'], result['sortIndicatorSection'], result['sortIndicatorShown'] = struct.unpack('>iiiii?', buf.read(21))

                # Read visual indices
                l = struct.unpack('>i', buf.read(4))[0]
                result['visualIndices'] = struct.unpack('>' + 'i'*l, buf.read(4*l))

                # Read logical indices
                l = struct.unpack('>i', buf.read(4))[0]
                result['logicalIndices'] = struct.unpack('>' + 'i'*l, buf.read(4*l))

                # Read sections hidden
                l = (struct.unpack('>i', buf.read(4))[0] + 7) // 8
                result['sectionsHidden'] = buf.read(l)

                # Read hidden section size
                l = struct.unpack('>i', buf.read(4))[0]
                s = struct.unpack('>' + 'i'*2*l, buf.read(4*2*l))
                result['hiddenSectionSize'] = dict(zip(s[0::2], s[1::2]))

                # Read length, section count, movable sections, clickable sections, highlight selected, stretch last section,
                # cascading resizing, stretch sections, contents sections, default section size, minimum section size, default alignment,
                # and global resize mode
                result['length'], result['sectionCount'], result['movableSections'], result['clickableSections'], result['highlightSelected'], result['stretchLastSection'], result['cascadingResizing'], result['stretchSections'], result['contentsSections'], result['defaultSectionSize'], result['minimumSectionSize'], result['defaultAlignment'], result['globalResizeMode'] = struct.unpack('>ii?????iiiiii', buf.read(37))

                if result['sectionsHidden']:
                    result['sectionsHidden'] = tuple(0 != (result['sectionsHidden'][(i >> 3)] & (1 << (i & 7))) for i in range(0, result['sectionCount']))
                else:
                    result['sectionsHidden'] = tuple()

                s = []
                for _ in range(0, struct.unpack('>i', buf.read(4))[0]):
                    i_data = struct.unpack('>iii', buf.read(12))
                    s.append({'size': i_data[0], 'tmpDataStreamSectionCount': i_data[1], 'resizeMode': i_data[2]})
                result['sectionItems'] = s

                result['resizeContentsPrecision'], result['customDefaultSectionSize'], result['lastSectionSize'] = struct.unpack('>i?i', buf.read(9))

        return result

    @property
    def alternating_row_colors(self) -> bool:
        """
        Indicates whether the table displays alternating row colors.

        :getter: Returns whether the table displays alternating row colors.
        :rtype: :obj:`bool`

        :setter: Sets whether the table displays alternating row colors.
        :param new_value: Indicates whether the table displays alternating row colors.
        :type new_value: :obj:`bool`
        """
        return bool(self.h5_group.attrs.get('AlternatingRowColors', False))

    @alternating_row_colors.setter
    def alternating_row_colors(self, value: bool):
        self.h5_group.attrs['AlternatingRowColors'] = np.uint8(value)

    @property
    def horizontal_header_visible(self) -> bool:
        """
        Indicates whether the horizontal header is visible.

        :getter: Returns whether the horizontal header is visible.
        :rtype: :obj:`bool`

        :setter: Sets whether the horizontal header is visible.
        :param new_value: Indicates whether the horizontal header is visible.
        :type new_value: :obj:`bool`
        """
        return bool(self.h5_group.attrs.get('HorizontalHeaderVisible', False))

    @horizontal_header_visible.setter
    def horizontal_header_visible(self, value: bool):
        self.h5_group.attrs['HorizontalHeaderVisible'] = np.uint8(value)

    @property
    def page_split(self) -> bool:
        """
        Indicates whether the table is split into pages.

        :getter: Returns whether the table is split into pages.
        :rtype: :obj:`bool`

        :setter: Sets whether the table is split into pages.
        :param new_value: Indicates whether the table is split into pages.
        :type new_value: :obj:`bool`
        """
        return bool(self.h5_group.attrs.get('PageSplit', False))

    @page_split.setter
    def page_split(self, value: bool):
        self.h5_group.attrs['PageSplit'] = np.uint8(value)

    @property
    def vertical_header_visible(self) -> bool:
        """
        Indicates whether the vertical header is visible.

        :getter: Returns whether the vertical header is visible.
        :rtype: :obj:`bool`

        :setter: Sets whether the vertical header is visible.
        :param new_value: Indicates whether the vertical header is visible.
        :type new_value: :obj:`bool`
        """
        return bool(self.h5_group.attrs.get('VerticalHeaderVisible', False))

    @vertical_header_visible.setter
    def vertical_header_visible(self, value: bool):
        self.h5_group.attrs['VerticalHeaderVisible'] = np.uint8(value)

    @property
    def column_label(self) -> bool:
        """
        Indicates whether the table displays column labels.

        :getter: Returns whether the table displays column labels.
        :rtype: :obj:`bool`

        :setter: Sets whether the table displays column labels.
        :param new_value: Indicates whether the table displays column labels.
        :type new_value: :obj:`bool`
        """
        if "ModelInfo" not in self.h5_group:
            return False
        return bool(self.h5_group["ModelInfo"].attrs.get('ColumnLabel', False))

    @column_label.setter
    def column_label(self, value: bool):
        self.h5_group.require_group("ModelInfo")
        self.h5_group["ModelInfo"].attrs['ColumnLabel'] = np.uint8(value)

    @property
    def header_font(self) -> base.Font:
        """
        The font of header.

        :getter: Returns the font of header.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of header.
        :param new_font: The new font of header.
        :type new_font: :obj:`base.Font`
        """
        if 'HeaderFont' in self.h5_group['ModelInfo'].attrs:
            return base.Font(self.h5_group['ModelInfo'].attrs['HeaderFont'])
        return None
    
    @header_font.setter
    def header_font(self, new_font: base.Font):
        self.h5_group['ModelInfo'].attrs['HeaderFont'] = str(new_font)

    @property
    def body_font(self) -> base.Font:
        """
        The font of table body.

        :getter: Returns the font of table body.
        :rtype: :obj:`base.Font`

        :setter: Sets the font of table body.
        :param new_font: The new font of table body.
        :type new_font: :obj:`base.Font`
        """
        if 'BodyFont' in self.h5_group['ModelInfo'].attrs:
            return base.Font(self.h5_group['ModelInfo'].attrs['BodyFont'])
        return None
    
    @body_font.setter
    def body_font(self, new_font: base.Font):
        self.h5_group['ModelInfo'].attrs['BodyFont'] = str(new_font)

    @property
    def columns(self) -> ColumnInfo.List:
        """
        :return: The column information of the table.
        :rtype: :obj:`ColumnInfo.List`
        """
        return TableGraphicsItem.ColumnInfo.List(self.h5_group['ModelInfo'])
    
    def logical_index(self, col_id: int) -> int:
        """
        Converts a column ID to a logical index.

        :param col_id: The column ID.
        :type col_id: :obj:`int`
        :return: The logical index of the column.
        :rtype: :obj:`int`
        """
        return next((i for i, col in enumerate(self.columns) if col.col_id == col_id), -1)
    
    def bjason_adjustments(self, require_group: bool = False) -> h5py.Group | None:
        """
        :return: The 'bjason_adjustments' group.
        :rtype: :obj:`h5py.Group` | None
        """
        if require_group:
            return self.h5_group.require_group('bjason_adjustments')
        elif 'bjason_adjustments' in self.h5_group:
            return self.h5_group['bjason_adjustments']
        else:
            return None

    @property
    def visual_column_ids(self) -> tuple[int]:
        """
        Defines visible columns and their order.

        :getter: Returns visible columns and their order.
        :rtype: :obj:`tuple` of :obj:`int`

        :setter: Sets visible columns and their order.
        :param column_ids: The new visible columns and their order.
        :type column_ids: :obj:`tuple` of :obj:`int`
        """
        bjason_adjustments = self.bjason_adjustments()
        if bjason_adjustments and 'visual_column_ids' in bjason_adjustments.attrs:
            return tuple(bjason_adjustments.attrs['visual_column_ids'])
        else: 
            horizontal_header = self.horizontal_header
            logical_indices: tuple[int] = horizontal_header['logicalIndices']
            sections_hidden: tuple[bool] = horizontal_header['sectionsHidden']
            assert len(logical_indices)  == len(sections_hidden)
            if not logical_indices: # All columns are visible in the predefined order 
                return tuple(col.col_id for col in self.columns)
            else:
                return tuple(self.columns[logical_indices[i]].col_id for i in range(len(sections_hidden)) if not sections_hidden[i])

    @visual_column_ids.setter
    def visual_column_ids(self, column_ids: Iterable[int]) -> None:
        if len(column_ids) != len(set(column_ids)):
            raise ValueError('Column IDs must be unique')
        self.bjason_adjustments(True).attrs['visual_column_ids'] = np.array(column_ids, np.int32)

    @property
    def customized_columns(self) -> ColumnInfo.List:
        """
        :return: The customized column information of the table.
        :rtype: :obj:`ColumnInfo.List`
        """ 

        return TableGraphicsItem.ColumnInfo.List(self.bjason_adjustments(self.h5_group.file.mode == 'r+'))
    
    @property
    def custom_row_keys(self) -> Iterable[str]:
        """
        The custom row keys of the table.

        :getter: Returns the custom row keys of the table.
        :rtype: :obj:`Iterable` of :obj:`str`

        :setter: Sets the custom row keys of the table.
        :param new_value: The new custom row keys of the table.
        :type new_value: :obj:`Iterable` of :obj:`str`
        """
        model_info_group = self.h5_group['ModelInfo']
        if 'RowInfo_keys' in model_info_group.attrs:
            return model_info_group.attrs['RowInfo_keys']
        else:
            return np.array([], dtype=np.object_)
        
    @custom_row_keys.setter
    def custom_row_keys(self, row_keys):
        model_info_group = self.h5_group['ModelInfo']
        model_info_group.attrs['RowInfo_keys'] = row_keys

    @property
    def custom_rows(self) -> RowInfo.List:
        """
        :return: The custom rows of the table.
        :rtype: :obj:`RowInfo.List`
        """
        return TableGraphicsItem.RowInfo.List(self.h5_group['ModelInfo'])

    def get_custom_value(self, row_id: str, column_id: int) -> Any:
        """
        Gets the custom value of a cell.

        :param row_id: The row ID.
        :type row_id: :obj:`str`
        :param column_id: The column ID.
        :type column_id: :obj:`int`
        :return: The custom value of the cell.
        :rtype: :obj:`Any`
        """
        row_id = utils.check_uuid_str(row_id)
        is_present = np.isin(self.custom_row_keys, row_id)
        if np.any(is_present):
            row_index = np.where(is_present)[0][0]
            row = self.custom_rows[row_index]
            is_present = np.isin(row.custom_column_ids, column_id)
            if np.any(is_present):
                return row.custom_values[np.where(is_present)[0][0]]
            
    def set_custom_value(self, row_id: str, column_id: int, value: Any):
        """
        Sets the custom value of a cell.

        :param row_id: The row ID.
        :type row_id: :obj:`str`
        :param column_id: The column ID.
        :type column_id: :obj:`int`
        :param value: The new custom value of the cell.
        :type value: :obj:`Any`
        """
        row_id = utils.check_uuid_str(row_id)
        is_present = np.isin(self.custom_row_keys, row_id)
        if not np.any(is_present):
            self.custom_row_keys = np.append(self.custom_row_keys, row_id)
            is_present = np.isin(self.custom_row_keys, row_id)
            self.custom_rows.append({'CellCustomData_keys': [column_id], 'CellCustomData_values': [value]})
        row_index = np.where(is_present)[0][0]
        row: TableGraphicsItem.RowInfo = self.custom_rows[row_index]
        is_present = np.isin(row.custom_column_ids, column_id)
        row_custom_values = list(row.custom_values)
        if not np.any(is_present):
            row.custom_column_ids = np.append(row.custom_column_ids, column_id)
            row_custom_values.append(value)
        else:
            column_index = np.where(is_present)[0][0]
            row_custom_values[column_index] = value
        row.custom_values = row_custom_values

    def get_custom_font(self, row_id: str, column_id: int) -> base.Font | None:
        """
        Gets the custom font of a cell.

        :param row_id: The row ID.
        :type row_id: :obj:`str`
        :param column_id: The column ID.
        :type column_id: :obj:`int`
        :return: The custom font of the cell.
        :rtype: :obj:`base.Font` | None
        """
        row_id = utils.check_uuid_str(row_id)
        is_present = np.isin(self.custom_row_keys, row_id)
        if np.any(is_present):
            row_index = np.where(is_present)[0][0]
            row = self.custom_rows[row_index]
            is_present = np.isin(row.column_ids, column_id)
            if np.any(is_present):
                return base.Font(row.fonts[np.where(is_present)[0][0]])

    def set_custom_font(self, row_id: str, column_id: int, font: base.Font | str):
        """
        Sets the custom font of a cell.

        :param row_id: The row ID.
        :type row_id: :obj:`str`
        :param column_id: The column ID.
        :type column_id: :obj:`int`
        :param font: The new custom font of the cell.
        :type font: :obj:`base.Font` | :obj:`str`
        """
        if isinstance(font, base.Font):
            font = str(font)
        font = font.encode('utf-8')
        row_id = utils.check_uuid_str(row_id)
        is_present = np.isin(self.custom_row_keys, row_id)
        if not np.any(is_present):
            self.custom_row_keys = np.append(self.custom_row_keys, row_id)
            self.custom_rows.append({'ColIds': [column_id], 'Fonts': [font]})
        else:
            row_index = np.where(is_present)[0][0]
            row: TableGraphicsItem.RowInfo = self.custom_rows[row_index]
            is_present = np.isin(row.column_ids, column_id)
            if not np.any(is_present):
                row.column_ids = np.append(row.column_ids, column_id)
                row.fonts = np.append(row.fonts, font)
            else:
                column_index = np.where(is_present)[0][0]
                row.fonts[column_index] = font

    def append_custom_row(self, row_id: str, values: Iterable[Any]):
        """
        Appends a custom row to the table.

        :param row_id: The row ID.
        :type row_id: :obj:`str`
        :param values: The values of the custom row.
        :type values: :obj:`Iterable` of :obj:`Any`

        .. note:: The number of values must be equal to the number of custom columns.
        """
        # custom columns are previousely defined by the user
        # values are in the same order as custom_columns
        custom_columns = sorted([column.col_id for column in list(self.columns) + list(self.customized_columns) if column.col_id < 0], reverse=True)
        # the columns are sorted this way: -1, -2, -3, ...
        assert len(values) == len(custom_columns) 
        row_id = utils.check_uuid_str(row_id)
        self.custom_row_keys = np.append(self.custom_row_keys, row_id)
        self.custom_rows.append({'CellCustomData_keys': custom_columns, 'CellCustomData_values': values})
    
    def get_custom_row(self, row_id: str) -> list[Any]:
        """
        Gets the custom row of the table.

        :param row_id: The row ID.
        :type row_id: :obj:`str`
        :return: The custom row of the table.
        :rtype: :obj:`list` of :obj:`Any`
        """
        row_id = utils.check_uuid_str(row_id)
        is_present = np.isin(self.custom_row_keys, row_id)
        custom_columns = sorted([column.col_id for column in list(self.columns) + list(self.customized_columns) if column.col_id < 0], reverse=True)
        if np.any(is_present):
            result = []
            row_index = np.where(is_present)[0][0]
            row = self.custom_rows[row_index]
            for column_id in custom_columns:
                is_present = np.isin(row.custom_column_ids, column_id)
                if np.any(is_present):
                    column_index = np.where(is_present)[0][0] 
                    result.append(row.custom_values[column_index])
                else:
                    result.append(None)
            return result
        else:
            return [None] * len(custom_columns)
        
    @property
    def show_title(self) -> bool:
        """
        .. versionadded:: 1.1.0

        Indicates whether the table displays a title.

        :getter: Returns whether the table displays a title.
        :rtype: :obj:`bool`

        :setter: Sets whether the table displays a title.
        :param new_value: Indicates whether the table displays a title.
        :type new_value: :obj:`bool`

        """
        return bool(self.h5_group.attrs.get('ShowTableTitle', False))
    
    @show_title.setter
    def show_title(self, value: bool):
        self.h5_group.attrs['ShowTableTitle'] = np.uint8(value)

    @property
    def title(self) -> str:
        """
        .. versionadded:: 1.1.0

        The title of the table. Usually in HTML format, but can be plain text.

        :getter: Returns the title of the table.
        :rtype: :obj:`str`

        :setter: Sets the title of the table.
        :param new_value: The new title of the table.
        :type new_value: :obj:`str`

        """
        return utils.ensure_str(self.h5_group.attrs.get('TableTitle', ''))

    @title.setter
    def title(self, value: str):
        self.h5_group.attrs['TableTitle'] = str(value)
        if 'TableTitle.plain_text' in self.h5_group.attrs:
            del self.h5_group.attrs['TableTitle.plain_text']

    @property
    def title_plain_text(self) -> str | None:
        """
        .. versionadded:: 1.1.0

        The plain text version of the title of the table. The setter is not available. Use :attr:`title` instead.
        Returnns either the plain text version of the title or None if it is not available.

        :getter: Returns the plain text version of the title of the table.
        :rtype: :obj:`str`

        """
        if 'TableTitle.plain_text' in self.h5_group.attrs:
            return utils.ensure_str(self.h5_group.attrs['TableTitle.plain_text'])
        return None
    
    @property
    def show_grid(self) -> bool:
        """
        .. versionadded:: 1.1.0

        Indicates whether the table displays a grid.

        :getter: Returns whether the table displays a grid.
        :rtype: :obj:`bool`

        :setter: Sets whether the table displays a grid.
        :param new_value: Indicates whether the table displays a grid.
        :type new_value: :obj:`bool`

        """
        return bool(self.h5_group.attrs.get('ShowTableGrid', True))
    
    @show_grid.setter
    def show_grid(self, value: bool):
        self.h5_group.attrs['ShowTableGrid'] = np.uint8(value)

class NMRTableGraphicsItem(TableGraphicsItem):
    """Base class for NMR data tables"""

    @property 
    def spec_data(self) -> data.NMRSpectrum | None:
        """
        :return: The NMR spectrum data associated with the table.
        :rtype: :obj:`NMRSpectrum` | None
        """
        for spec in data.NMRSpectrum.List(self.h5_group.parent.parent['NMR']):
            if self.data_id == spec.id:
                return spec
        return None

class NMRParamTableGraphicsItem(NMRTableGraphicsItem):
    """NMR parameter table graphics item"""    

    class ColumnID(IntEnum):
        """Column IDs"""
        NAME  = 0
        VALUE = 1

    class Parameter(base.H5Group):
        """Represents a parameter"""

        class List(base.GroupList):
            """Represents a list of parameters"""
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'list', NMRParamTableGraphicsItem.Parameter)

        @property
        def id(self) -> str:
            """
            :return: The UUID string of the parameter.
            :rtype: :obj:`str`
            """
            return utils.check_uuid_str(self.h5_group.attrs['id'])

        @property
        def name(self) -> str:
            """
            :return: The name of the parameter.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['name'])

        @property
        def value(self) -> str:
            """
            :return: The value of the parameter.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['value'])  

        @property
        def value_template(self) -> str | None:
            """
            :return: The value template string of the parameter.
            :rtype: :obj:`str` | None
            """
            if 'value_template' in self.h5_group.attrs:
                return utils.ensure_str(self.h5_group.attrs['value_template'])
            return None

        @property
        def condition(self) -> str | None:
            """
            :return: The condition string of the parameter.
            :rtype: :obj:`str` | None
            """
            if 'condition' in self.h5_group.attrs:
                return utils.ensure_str(self.h5_group.attrs['condition'])
            return None

    def set_defaults(self):
        """
        Setting default values on creating a parameter table item.
        Specifically, the horizontal header is hidden.
        """
        super().set_defaults()
        self.horizontal_header_visible = False

    @property
    def param_list(self) -> Parameter.List:
        """
        :return: The parameter list of the table.
        :rtype: :obj:`Parameter.List`
        """
        return NMRParamTableGraphicsItem.Parameter.List(self.h5_group['ParamsTable'])
        
    @property
    def data_id(self) -> str:
        """
        :return: The UUID string of the data that the table is associated with.
        :rtype: :obj:`str`
        """
        return utils.ensure_str(self.h5_group['ParamsTable'].attrs['id'])

class NMRPeakTableGraphicsItem(NMRTableGraphicsItem):
    """
    Represents an NMR peak table graphics item.
    """
    class ColumnID(IntEnum):
        """Column IDs"""
        POS0 = 0
        POS1 = 1
        POS2 = 2
        HEIGHT = 3
        WIDTH0 = 4
        WIDTH1 = 5
        WIDTH2 = 6
        KURTOSIS0 = 7
        KURTOSIS1 = 8
        KURTOSIS2 = 9
        VOLUME = 10
        TYPE = 11
        LABEL = 12
        POS0ERR = 13
        HEIGHTERR = 14
        WIDTH0ERR = 15
        KURTOSIS0ERR = 16
        VOLUMEERR = 17

    @property
    def data_id(self) -> str:
        """
        :return: The data ID of the spectrum the peak table belongs to.
        :rtype: :obj:`str`
        """
        return utils.check_uuid_str(self.h5_group['PeaksTable'].attrs['SpectrumID'])   

class NMRMultipletTableGraphicsItem(NMRTableGraphicsItem):
    """
    Represents an NMR multiplet table graphics item.
    """
    class ColumnID(IntEnum):
        """Column IDs"""
        POS0 = 0
        POS1 = 1
        POS2 = 2
        START0 = 3
        START1 = 4
        START2 = 5
        END0 = 6
        END1 = 7
        END2 = 8
        OFFSET = 9
        SLOPE = 10
        SUM_INTEGRAL = 11
        TYPE = 12
        NORMALIZED = 13
        J = 14
        PEAKS_VOLUME = 15

    @property
    def data_id(self) -> str:
        """
        :return: The data ID of the spectrum the multiplet table belongs to.
        :rtype: :obj:`str`
        """
        return utils.check_uuid_str(self.h5_group['MultipletsTable'].attrs['SpectrumID'])

class AssignmentTableGraphicsItem(TableGraphicsItem):
    """
    Represents an assignment table graphics item.
    """
    class ColumnID(IntEnum):
        """Column IDs"""
        ATOMS = 0,
        EXPSH = 1,
        PREDSH = 2,
        PREDERR = 3,
        EXPCOUPLINGS = 4,
        PREDCOUPLINGS = 5,
        COMMENT = 6,
        ASSIGNMENT = 7

    @property
    def data_id(self) -> str:
        """
        :return: The data ID of the spectrum the assignment table belongs to.
        :rtype: :obj:`str`
        """
        return utils.ensure_str(self.h5_group['AssignmentTable'].attrs['MoleculeID'])

class NMRMultipletReportGraphicsItem(GraphicsItem):
    """
    Represents an NMR multiplet report graphics item.
    """
    builtin_formats = ["JACS", "Angew. Chem.", "Chem Nat Prod", "Nature", "RSC", "Scientific Reports", "Wiley"]

    class JournalTemplate(base.H5Group):
        """
        Represents a journal template.
        """
        @property
        def js(self) -> str:
            """
            :return: The j-values format string.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['Js'])

        @property
        def js_separator(self) -> str:
            """
            :return: The j-values separator.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['Js_separator'])

        @property
        def multiplet(self) -> str:
            """
            :return: The multiplet format string.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['mutiplet'])

        @property
        def multiplet_separator(self) -> str:
            """
            :return: The multiplet separator.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['mutiplet_separator'])

        @property
        def report(self):
            """
            :return: The report format string.
            :rtype: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs['report'])

    @property
    def journal_format(self) -> str | None:
        """
        The journal format name. 

        :getter: Returns the journal format name.
        :rtype: :obj:`str` | None

        :setter: Sets the journal format name.
        :param new_format: The new journal format name.
        :type new_format: :obj:`str`
        """
        if 'JournalFormatName' in self.h5_group['MultipletsReport'].attrs: 
            return utils.ensure_str(self.h5_group['MultipletsReport'].attrs['JournalFormatName'])
        if 'JournalFormat' in self.h5_group['MultipletsReport'].attrs: 
            return NMRMultipletReportGraphicsItem.builtin_formats[self.h5_group['MultipletsReport'].attrs['JournalFormat']]

    @journal_format.setter
    def journal_format(self, new_format):
        self.h5_group['MultipletsReport'].attrs['JournalFormatName'] = new_format

    @property
    def report_text(self) -> str:
        """
        :return: The report text.
        :rtype: :obj:`str`
        """
        return utils.ensure_str(self.h5_group['MultipletsReport'].attrs['ReportText'])

    @property
    def spectrum_id(self) -> str:
        """
        :return: The data ID of the spectrum the multiplet report correponds to.
        :rtype: :obj:`str`
        """
        return utils.check_uuid_str(self.h5_group['MultipletsReport'].attrs['SpectrumID'])

    @property
    def journal_template(self) -> JournalTemplate | None:
        """
        :return: The journal template.
        :rtype: :obj:`JournalTemplate` | None
        """
        if 'MultipletsReport/JournalTemplate' in self.h5_group:
            return NMRMultipletReportGraphicsItem.JournalTemplate(self.h5_group['MultipletsReport/JournalTemplate'])

class TextGraphicsItem(GraphicsItem):
    """
    Represents a text graphics item.
    """
    @property
    def text_id(self) -> str:
        """
        :return: The text data object ID.
        :rtype: :obj:`str`
        """
        return utils.check_uuid_str(self.h5_group['TextItem'].attrs['TextID'])

    @property
    def text(self) -> data.Text:
        """
        :return: The text data object.
        :rtype: :obj:`data.Text`
        """
        text_id = self.text_id
        for txt in data.Text.List(self.h5_group.parent.parent['General']):
            if text_id == txt.id:
                return txt

class ImageGraphicsItem(GraphicsItem):
    """
    Represents an image graphics item.
    """
    @property
    def image_id(self) -> str:
        """
        :return: The image data object ID.
        :rtype: :obj:`str`
        """
        return utils.check_uuid_str(self.h5_group['ImageDraw'].attrs['ImageID'])

    @property
    def image(self) -> data.Image:
        """
        :return: The image data object.
        :rtype: :obj:`data.Image`
        """
        image_id = self.image_id
        for img in data.Image.List(self.h5_group.parent.parent['General']):
            if image_id == img.id:
                return img

class MoleculeGraphicsItem(GraphicsItem):
    """
    Represents a molecule graphics item.
    """
    
    class EditMode(IntEnum):
        """
        Edit modes enumeration.
        """
        NONE = 0
        Auto = 1
        Select = 2
        Move = 3
        Rotate2D = 4
        Rotate3D = 5
        Draw = 6
        Delete = 7
        Edit = 8
        Charge = 9
        Stereo = 10
        Shift = 11
        Modify = 20
        Create = 21 

    class DrawStyle(base.H5Group):
        """
        Represents a draw style.
        """
        class LabelType(IntEnum):
            """
            .. versionadded:: 1.1.0

            Label types enumeration.
            """
            None_       = 0
            AtomNum     = 1 << 0
            XCoord      = 1 << 1
            YCoord      = 1 << 2
            ZCoord      = 1 << 3
            Exp         = 1 << 4
            Calc        = 1 << 5
            Diff        = 1 << 6
            C13         = 1 << 7
            H1          = 1 << 8
            N15         = 1 << 9
            StereoSign  = 1 << 10

            # Derived masks
            FlatCoord   = XCoord | YCoord
            Coord3D     = XCoord | YCoord | ZCoord
            C13Exp      = C13 | Exp
            C13Calc     = C13 | Calc
            C13Diff     = C13 | Diff
            H1Exp       = H1 | Exp
            H1Calc      = H1 | Calc
            H1Diff      = H1 | Diff
            N15Exp      = N15 | Exp
            N15Calc     = N15 | Calc
            N15Diff     = N15 | Diff

        @property
        def atoms_in_color(self) -> bool:
            """
            :getter: Returns whether atoms are drawn in color.
            :rtype: :obj:`bool`

            :setter: Sets whether atoms are drawn in color.
            :param new_value: Indicates whether atoms are drawn in color.
            :type new_value: :obj:`bool`
            """
            return bool(self.h5_group.attrs['AtomsInColor'])
 
        @atoms_in_color.setter
        def atoms_in_color(self, new_value: bool):
            self.h5_group.attrs['AtomsInColor'] = np.uint8(1 if new_value else 0)

        @property
        def draw_internal_c(self) -> bool:
            """
            :getter: Returns whether internal carbon atoms are drawn.
            :rtype: :obj:`bool`

            :setter: Sets whether internal carbon atoms are drawn.
            :param new_value: Indicates whether internal carbon atoms are drawn.
            :type new_value: :obj:`bool`
            """
            return bool(self.h5_group.attrs['DrawInternalC'])

        @draw_internal_c.setter
        def draw_internal_c(self, new_value: bool):
            self.h5_group.attrs['DrawInternalC'] = np.uint8(1 if new_value else 0)

        # getter for draw_labels
        @property
        def draw_labels(self) -> bool:
            """
            :getter: Returns whether labels are drawn.
            :rtype: :obj:`bool`

            :setter: Sets whether labels are drawn.
            :param new_value: Indicates whether labels are drawn.
            :type new_value: :obj:`bool`
            """
            return bool(self.h5_group.attrs['DrawLabels'])

        @draw_labels.setter
        def draw_labels(self, new_value: bool):
            self.h5_group.attrs['DrawLabels'] = np.uint8(1 if new_value else 0)

        @property
        def draw_terminal_c(self) -> bool:
            """
            :getter: Returns whether terminal carbon atoms are drawn.
            :rtype: :obj:`bool`

            :setter: Sets whether terminal carbon atoms are drawn.
            :param new_value: Indicates whether terminal carbon atoms are drawn.
            :type new_value: :obj:`bool`
            """
            return bool(self.h5_group.attrs['DrawTerminalC'])
        
        @draw_terminal_c.setter
        def draw_terminal_c(self, new_value: bool):
            self.h5_group.attrs['DrawTerminalC'] = np.uint8(1 if new_value else 0)

        @property
        def labels(self) -> int:
            """
            :getter: Returns the label type.
            :rtype: :obj:`int`

            :setter: Sets the label type.
            :param value: The new label type.
            :type value: :obj:`int`

            .. note:: The label type is a combination of :class:`LabelType` flags.
            """
            return self.h5_group.attrs['Labels']
            
        @labels.setter
        def labels(self, value: int):
            self.h5_group.attrs['Labels'] = int(value)

    class Editor(base.H5Group):
        """
        Represents an editor.
        """
        @property
        def allow_edit(self) -> bool:
            """
            :return: Whether editing is allowed.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['AllowEdit'])

        @property
        def allow_modify_atoms(self) -> bool:
            """
            :return: Whether modifying atoms is allowed.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['AllowModifyAtoms'])

        @property
        def allow_modify_bonds(self) -> bool:
            """
            :return: Whether modifying bonds is allowed.
            :rtype: :obj:`bool`
            """
            return bool(self.h5_group.attrs['AllowModifyBonds'])

    class Geometry(base.H5Group):
        """
        Represents molecule geometry
        """
        @property
        def auto_scale(self) -> float:
            """
            :return: The auto scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['AutoScale']

        @property
        def user_scale(self) -> float:
            """
            :return: The user scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['UserScale']

        @property
        def transform(self) -> 'MoleculeGraphicsItem.Transform':
            """
            :return: The transform.
            :rtype: :obj:`MoleculeGraphicsItem.Transform`
            """
            return MoleculeGraphicsItem.Transform(self.h5_group['Transform'])

    class Transform(base.H5Group):
        """
        Represents a coordinate transform.
        """
        @property
        def angle(self) -> float:
            """
            :return: The angle.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['Angle']

        @property
        def scale_x(self) -> float:
            """
            :return: The X scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['ScaleX'] 

        @property
        def scale_y(self) -> float:
            """
            :return: The Y scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['ScaleY'] 

        @property
        def shift_x(self) -> float:
            """
            :return: The X shift.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['ShiftX'] 

        @property
        def shift_y(self) -> float:
            """
            :return: The Y shift.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['ShiftY'] 

    class DrawItem(base.IDedObject):
        """
        Represents mulecule draw item.
        """

        class List(base.GroupList):
            """
            Represents a list of draw items.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'Items', MoleculeGraphicsItem.DrawItem)

        @property
        def user_scale(self) -> float:
            """
            :return: The user scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['UserScale']

        @property
        def auto_scale(self) -> float:
            """
            :return: The auto scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['AutoScale']

        @property
        def bond_len_scale(self) -> float:
            """
            :return: The bond length scale.
            :rtype: :obj:`float`
            """
            return self.h5_group.attrs['BondLenScale']

        @property
        def id(self) -> str:
            """
            :return: The ID.
            :rtype: :obj:`str`
            """
            return utils.check_uuid_str(self.h5_group.attrs['ID'])

        @property
        def transform(self) -> 'MoleculeGraphicsItem.Transform':
            """
            :return: The transform.
            :rtype: :obj:`MoleculeGraphicsItem.Transform`
            """
            return  MoleculeGraphicsItem.Transform(self.h5_group['Transform'])

    @property
    def items(self) -> DrawItem.List:
        """
        :return: The molecule draw items.
        :rtype: :obj:`DrawItem.List`
        """
        return  MoleculeGraphicsItem.DrawItem.List(self.h5_group['MolPlot'])

    @property
    def draw_style(self) -> DrawStyle:
        """
        :return: The draw style.
        :rtype: :obj:`DrawStyle`
        """
        return MoleculeGraphicsItem.DrawStyle(self.h5_group['MolPlot/DrawMolStyle'])

    @property
    def editor(self) -> Editor:
        """
        :return: The editor.
        :rtype: :obj:`Editor`
        """
        return MoleculeGraphicsItem.Editor(self.h5_group['MolPlot/Editor'])

    @property
    def geometry(self) -> Geometry:
        """
        :return: The geometry.
        :rtype: :obj:`Geometry`
        """
        return MoleculeGraphicsItem.Geometry(self.h5_group['MolPlot/Geometry'])

    @property
    def active_atom_type(self) -> 'data.Molecule.Atom.Type':
        """
        :return: The active atom type.
        :rtype: :obj:`data.Molecule.Atom.Type`
        """
        return data.Molecule.Atom.Type(self.h5_group['MolPlot'].attrs['ActiveAtomType'])

    @property
    def active_bond_type(self) -> 'data.Molecule.Bond.Type':
        """
        :return: The active bond type.
        :rtype: :obj:`data.Molecule.Bond.Type`
        """
        return self.h5_group['MolPlot'].attrs['ActiveBondType']

    @property
    def browse_edit_mode(self) -> EditMode:
        """
        :return: The browse edit mode.
        :rtype: :obj:`EditMode`
        """
        return MoleculeGraphicsItem.EditMode(self.h5_group['MolPlot'].attrs['BrowseEditMode'])

    @property
    def user_edit_mode(self) -> EditMode:
        """
        :return: The user edit mode.
        :rtype: :obj:`EditMode`
        """
        return MoleculeGraphicsItem.EditMode(self.h5_group['MolPlot'].attrs['UserEditMode'])
    
    @property
    def mol_data_list(self) -> list[data.Molecule]:
        """
        .. versionadded:: 1.1.0

        :return: The list of molecules associated with the graphics item.
        :rtype: :obj:`list` of :obj:`data.Molecule`

        """
        result = []
        for mol_draw_item in self.items:
            for mol in data.Molecule.List(self.h5_group.parent.parent['Molecules']):
                if mol_draw_item.id == mol.id:
                    result.append(mol)
        return result

    def mol_data(self, id: int | str = 0) -> data.Molecule:
        """
        .. versionadded:: 1.1.0

        :param id: The index or ID of the molecule.
        :type index: :obj:`int` | :obj:`str`
        :return: The molecule associated with the graphics item.
        :rtype: :obj:`data.Molecule`

        """
        mols = self.mol_data_list
        if isinstance(id, int) or str(id).isnumeric():
            id = int(id)
            if 0 <= id and id < len(mols):
                return mols[id]
            return
        for mol in mols:
            if mol.id == id:
                return mol

class ChartGraphicsItem(GraphicsItem):
    """
    .. versionadded:: 1.1.0
    
    Represents a chart graphics item.
    """

    class Series(base.IDedObject):

        class Type(IntEnum):
            """
            Series type enumeration. Corresponds to QAbstractSeries::SeriesType, 
            but only the types that are currently supported in JASON are included.
            """
            LINE = 0
            SCATTER = 6

        class MarkerShape(IntEnum):
            """
            Marker shape enumeration. Corresponds to QScatterSeries::MarkerShape,
            but only the shapes that are currently supported in JASON are included.
            """
            CIRCLE = 0
            RECTANGLE = 1
            DIAMOND = 2
            TRIANGLE = 3
            STAR = 4
            PENTAGON = 5

        class Source(IntEnum):
            """
            Source enumeration.
            """
            TABLE = 0
            FIT = 1
            FIT_RESIDUALS = 2

        """
        Represents a series in a chart.
        """
        class List(base.GroupList):
            """
            Represents a list of series.
            """
            def __init__(self, h5_group):
                base.GroupList.__init__(self, h5_group, 'Series', ChartGraphicsItem.Series)

        @property
        def data_id(self) -> str:
            """
            :return: The table or fit ID.
            :rtype: :obj:`str`
            """
            if self.source == ChartGraphicsItem.Series.Source.TABLE:
                return utils.check_uuid_str(self.h5_group.attrs.get('TableID', ''))
            return utils.ensure_str(self.h5_group.attrs.get('FitID', ''))
        
        @property
        def error_series_id(self) -> str | None:
            """
            :return: The error series ID.
            :rtype: :obj:`str`
            """
            _id = utils.ensure_str(self.h5_group.attrs.get('ErrorSeriesID', '{undefined}'))
            if _id == '{undefined}':
                return None
            return _id
        
        @property
        def type(self) -> Type:
            """
            :return: The series type.
            :rtype: :obj:`Type`

            :setter: Sets the series type.
            :param value: The new series type.
            :type value: :obj:`Type`
            """
            return ChartGraphicsItem.Series.Type(self.h5_group.attrs['Type'])
        
        @type.setter
        def type(self, value: Type):
            self.h5_group.attrs['Type'] = int(value)

        @property
        def name(self) -> str:
            """
            :return: The name of the series.
            :rtype: :obj:`str`

            :setter: Sets the name of the series.
            :param value: The new name of the series.
            :type value: :obj:`str`

            """
            return utils.ensure_str(self.h5_group.attrs.get('Name', ''))
        
        @name.setter
        def name(self, value: str):
            self.h5_group.attrs['Name'] = str(value)
        
        @property
        def color(self) -> str:
            """
            :return: The color of the series in the format '#RRGGBBAA'.
            :rtype: :obj:`str`

            :setter: Sets the color of the series.
            :param value: The new color of the series.
            :type value: :obj:`str`
            """
            return utils.ensure_str(self.h5_group.attrs.get('Colour', '')).upper()
        
        @color.setter
        def color(self, value: str):
            self.h5_group.attrs['Colour'] = value

        @property
        def is_visible(self) -> bool:
            """
            :return: Whether the series is visible.
            :rtype: :obj:`bool`

            :setter: Sets whether the series is visible.
            :param value: Indicates whether the series is visible.
            :type value: :obj:`bool`
            """
            return bool(self.h5_group.attrs['Visibility'])
        
        @is_visible.setter
        def is_visible(self, value: bool):
            self.h5_group.attrs['Visibility'] = np.uint8(value)

        @property
        def is_error_series(self) -> bool:
            """
            :return: Whether the series is an error series.
            :rtype: :obj:`bool`
            """
            # Can be a numeric value, representing a boolean or a string '{undefined}' which is also interpreted as False
            _is_error_series = self.h5_group.attrs.get('IsErrorSeries', False)
            if utils.ensure_str(_is_error_series) == '{undefined}':
                return False
            return bool(_is_error_series)
        
        @property
        def x_column_id(self) -> int | None:
            """
            :return: The X column ID.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs.get('XColumn', None)
        
        @property
        def y_column_id(self) -> int | None:
            """
            :return: The Y column ID.
            :rtype: :obj:`int`
            """
            return self.h5_group.attrs.get('YColumn', None)

        @property
        def source(self) -> Source:
            """
            :return: The source.
            :rtype: :obj:`Source`
            """
            return ChartGraphicsItem.Series.Source(self.h5_group.attrs['Source'])
        
        @property
        def show_error_bars_x(self) -> bool:
            """
            :return: Whether error bars are shown on the X axis.
            :rtype: :obj:`bool`

            :setter: Sets whether error bars are shown on the X axis.
            """
            _show_error_bars_x = self.h5_group.attrs.get('ShowErrorBarsX', False)
            if utils.ensure_str(_show_error_bars_x) == '{undefined}':
                return False
            return bool(_show_error_bars_x)
        
        @show_error_bars_x.setter
        def show_error_bars_x(self, value: bool):
            self.h5_group.attrs['ShowErrorBarsX'] = np.uint8(value)

        @property
        def show_error_bars_y(self) -> bool:
            """
            :return: Whether error bars are shown on the Y axis.
            :rtype: :obj:`bool`

            :setter: Sets whether error bars are shown on the Y axis.
            """
            _show_error_bars_y = self.h5_group.attrs.get('ShowErrorBarsY', False)
            if utils.ensure_str(_show_error_bars_y) == '{undefined}':
                return False
            return bool(_show_error_bars_y)
        
        @show_error_bars_y.setter
        def show_error_bars_y(self, value: bool):
            self.h5_group.attrs['ShowErrorBarsY'] = np.uint8(value)

        @property
        def marker_shape(self) -> MarkerShape | base.PenStyle:
            """
            :return: The marker shape.
            :rtype: :obj:`MarkerShape`

            :setter: Sets the marker shape.
            :param value: The new marker shape.
            :type value: :obj:`MarkerShape`
            """
            if self.type == ChartGraphicsItem.Series.Type.LINE:
                return base.PenStyle(self.h5_group.attrs['MarkerShape'])
            return ChartGraphicsItem.Series.MarkerShape(self.h5_group.attrs['MarkerShape'])
        
        @marker_shape.setter
        def marker_shape(self, value: MarkerShape | base.PenStyle):
            self.h5_group.attrs['MarkerShape'] = int(value)

        @property
        def marker_size(self) -> int:
            """
            :return: The marker size.
            :rtype: :obj:`int`

            :setter: Sets the marker size.
            :param value: The new marker size.
            :type value: :obj:`int`
            """
            return self.h5_group.attrs['MarkerSize']
        
        @marker_size.setter
        def marker_size(self, value: int):
            self.h5_group.attrs['MarkerSize'] = value

        @property
        def parent_series_id(self) -> str | None:
            """
            :return: The parent series ID for the error series.
            :rtype: :obj:`str` | None
            """
            _id = utils.ensure_str(self.h5_group.attrs.get('ParentSeriesId', '{undefined}'))
            if _id == '{undefined}':
                return None
            return _id
        
        @property
        def parent_series_x_column_id(self) -> int | None:
            """
            :return: The parent series X column ID for the error series.
            :rtype: :obj:`int` | None
            """
            _id = self.h5_group.attrs.get('ParentSeriesXCol', '{undefined}')
            if utils.ensure_str(_id) == '{undefined}':
                return None
            return _id

        @property
        def parent_series_y_column_id(self) -> int | None:
            """
            :return: The parent series Y column ID for the error series.
            :rtype: :obj:`int` | None
            """
            _id = self.h5_group.attrs.get('ParentSeresYCol', '{undefined}')
            if utils.ensure_str(_id) == '{undefined}':
                return None
            return _id
        
        @property
        def x(self) -> np.ndarray[np.float64]:
            """
            :return: The X values.
            :rtype: :obj:`np.ndarray`
            """
            return self.h5_group.attrs.get('x', np.array([]))

        @property
        def y(self) -> np.ndarray[np.float64]:
            """
            :return: The Y values.
            :rtype: :obj:`np.ndarray[np.float64]`
            """
            return self.h5_group.attrs.get('y', np.array([]))

    @property
    def gridlines_color(self) -> str:
        """
        The color of the gridlines.

        :getter: Returns the color of the gridlines in the format '#RRGGBBAA'.
        :rtype: :obj:`str`

        :setter: Sets the color of the gridlines.
        :param new_value: The new color of the gridlines.
        :type new_value: :obj:`str`
        """
        return self._get_color('Chart', 'ChartGridlinesColor')
    
    @gridlines_color.setter
    def gridlines_color(self, new_value: str):
        self._set_color('Chart', 'ChartGridlinesColor', new_value)

    @property
    def show_gridlines(self) -> bool:
        """
        Indicates whether gridlines are shown.

        :getter: Returns whether gridlines are shown.
        :rtype: :obj:`bool`

        :setter: Sets whether gridlines are shown.
        :param new_value: Indicates whether gridlines are shown.
        :type new_value: :obj:`bool`
        """
        return bool(self.h5_group['Chart'].attrs.get('ShowChartGridlines', False))
    
    @show_gridlines.setter
    def show_gridlines(self, value: bool):
        self.h5_group['Chart'].attrs['ShowChartGridlines'] = np.uint8(value)

    @property
    def title(self) -> str:
        """
        The title of the chart.

        :getter: Returns the title of the chart.
        :rtype: :obj:`str`

        :setter: Sets the title of the chart.
        :param new_value: The new title of the chart.
        :type new_value: :obj:`str`
        """
        return utils.ensure_str(self.h5_group['Chart'].attrs.get('ChartTitle', ''))
    
    @title.setter
    def title(self, value: str):
        self.h5_group['Chart'].attrs['ChartTitle'] = str(value)

    @property
    def title_font(self) -> base.Font | None:
        """
        The font of the title.

        :getter: Returns the font of the title.
        :rtype: :obj:`base.Font` | None

        :setter: Sets the font of the title.
        :param new_value: The new font of the title.
        :type new_value: :obj:`base.Font`
        """
        return base.Font(self.h5_group['Chart'].attrs.get('ChartTitleFont', ''))
    
    @title_font.setter
    def title_font(self, value: base.Font):
        self.h5_group['Chart'].attrs['ChartTitleFont'] = str(value)

    @property
    def legend_alignment(self) -> int:
        """
        The alignment of the legend.

        :getter: Returns the alignment of the legend.
        :rtype: :obj:`int`

        :setter: Sets the alignment of the legend.
        :param new_value: The new alignment of the legend.
        :type new_value: :obj:`int`
        """
        return self.h5_group['Chart'].attrs.get('ChartLegendAlignment', 0)
    
    @legend_alignment.setter
    def legend_alignment(self, value: int):
        self.h5_group['Chart'].attrs['ChartLegendAlignment'] = value

    @property
    def horizontal_axis_ticks(self) -> int:
        """
        The number of horizontal axis ticks.

        :getter: Returns the number of horizontal axis ticks.
        :rtype: :obj:`int`

        :setter: Sets the number of horizontal axis ticks.
        :param new_value: The new number of horizontal axis ticks.
        :type new_value: :obj:`int`
        """
        return self.h5_group['Chart'].attrs.get('DefaultHorizontalAxisTicks', 0)
    
    @horizontal_axis_ticks.setter
    def horizontal_axis_ticks(self, value: int):
        self.h5_group['Chart'].attrs['DefaultHorizontalAxisTicks'] = value

    @property
    def vertical_axis_ticks(self) -> int:
        """
        The number of vertical axis ticks.

        :getter: Returns the number of vertical axis ticks.
        :rtype: :obj:`int`

        :setter: Sets the number of vertical axis ticks.
        :param new_value: The new number of vertical axis ticks.
        :type new_value: :obj:`int`
        """
        return self.h5_group['Chart'].attrs.get('DefaultVerticalAxisTicks', 0)
    
    @vertical_axis_ticks.setter
    def vertical_axis_ticks(self, value: int):
        self.h5_group['Chart'].attrs['DefaultVerticalAxisTicks'] = value

    @property
    def horizontal_axis_minor_ticks(self) -> int:
        """
        The number of horizontal axis minor ticks.

        :getter: Returns the number of horizontal axis minor ticks.
        :rtype: :obj:`int`

        :setter: Sets the number of horizontal axis minor ticks.
        :param new_value: The new number of horizontal axis minor ticks.
        :type new_value: :obj:`int`
        """
        return self.h5_group['Chart'].attrs.get('DefaultHorizontalAxisMinorTicks', 0)
    
    @horizontal_axis_minor_ticks.setter
    def horizontal_axis_minor_ticks(self, value: int):
        self.h5_group['Chart'].attrs['DefaultHorizontalAxisMinorTicks'] = value

    @property
    def vertical_axis_minor_ticks(self) -> int:
        """
        The number of vertical axis minor ticks.

        :getter: Returns the number of vertical axis minor ticks.
        :rtype: :obj:`int`

        :setter: Sets the number of vertical axis minor ticks.
        :param new_value: The new number of vertical axis minor ticks.
        :type new_value: :obj:`int`
        """
        return self.h5_group['Chart'].attrs.get('DefaultVerticalAxisMinorTicks', 0)
    
    @vertical_axis_minor_ticks.setter
    def vertical_axis_minor_ticks(self, value: int):
        self.h5_group['Chart'].attrs['DefaultVerticalAxisMinorTicks'] = value

    @property
    def horizontal_axis_color(self) -> str:
        """
        The color of the horizontal axis.

        :getter: Returns the color of the horizontal axis in the format '#RRGGBBAA'.
        :rtype: :obj:`str`

        :setter: Sets the color of the horizontal axis.
        :param new_value: The new color of the horizontal axis.
        :type new_value: :obj:`str`
        """
        return self._get_color('Chart', 'HorizontalAxisColor')
    
    @horizontal_axis_color.setter
    def horizontal_axis_color(self, new_value: str):
        self._set_color('Chart', 'HorizontalAxisColor', new_value)

    @property
    def vertical_axis_color(self) -> str:
        """
        The color of the vertical axis.

        :getter: Returns the color of the vertical axis in the format '#RRGGBBAA'.
        :rtype: :obj:`str`

        :setter: Sets the color of the vertical axis.
        :param new_value: The new color of the vertical axis.
        :type new_value: :obj:`str`
        """
        return self._get_color('Chart', 'VerticalAxisColor')
    
    @vertical_axis_color.setter
    def vertical_axis_color(self, new_value: str):
        self._set_color('Chart', 'VerticalAxisColor', new_value)

    @property
    def horizontal_axis_title(self) -> str:
        """
        The title of the horizontal axis.

        :getter: Returns the title of the horizontal axis.
        :rtype: :obj:`str`

        :setter: Sets the title of the horizontal axis.
        :param new_value: The new title of the horizontal axis.
        :type new_value: :obj:`str`
        """
        return utils.ensure_str(self.h5_group['Chart'].attrs.get('HorizontalAxisTitle', ''))
    
    @horizontal_axis_title.setter
    def horizontal_axis_title(self, value: str):
        self.h5_group['Chart'].attrs['HorizontalAxisTitle'] = str(value)

    @property
    def vertical_axis_title(self) -> str:
        """
        The title of the vertical axis.

        :getter: Returns the title of the vertical axis.
        :rtype: :obj:`str`

        :setter: Sets the title of the vertical axis.
        :param new_value: The new title of the vertical axis.
        :type new_value: :obj:`str`
        """
        return utils.ensure_str(self.h5_group['Chart'].attrs.get('VerticalAxisTitle', ''))
    
    @vertical_axis_title.setter
    def vertical_axis_title(self, value: str):
        self.h5_group['Chart'].attrs['VerticalAxisTitle'] = str(value)

    @property
    def horizontal_axis_title_font(self) -> base.Font | None:
        """
        The font of the horizontal axis title.

        :getter: Returns the font of the horizontal axis title.
        :rtype: :obj:`base.Font` | None

        :setter: Sets the font of the horizontal axis title.
        :param new_value: The new font of the horizontal axis title.
        :type new_value: :obj:`base.Font`
        """
        return base.Font(self.h5_group['Chart'].attrs.get('HorizontalAxisTitleFont', ''))
    
    @horizontal_axis_title_font.setter
    def horizontal_axis_title_font(self, value: base.Font):
        self.h5_group['Chart'].attrs['HorizontalAxisTitleFont'] = str(value)

    @property
    def vertical_axis_title_font(self) -> base.Font | None:
        """
        The font of the vertical axis title.

        :getter: Returns the font of the vertical axis title.
        :rtype: :obj:`base.Font` | None

        :setter: Sets the font of the vertical axis title.
        :param new_value: The new font of the vertical axis title.
        :type new_value: :obj:`base.Font`
        """
        return base.Font(self.h5_group['Chart'].attrs.get('VerticalAxisTitleFont', ''))
    
    @vertical_axis_title_font.setter
    def vertical_axis_title_font(self, value: base.Font):
        self.h5_group['Chart'].attrs['VerticalAxisTitleFont'] = str(value)

    @property
    def horizontal_axis_font(self) -> base.Font | None:
        """
        The font of the horizontal axis.

        :getter: Returns the font of the horizontal axis.
        :rtype: :obj:`base.Font` | None

        :setter: Sets the font of the horizontal axis.
        :param new_value: The new font of the horizontal axis.
        :type new_value: :obj:`base.Font`
        """
        return base.Font(self.h5_group['Chart'].attrs.get('HorizontalAxisFont', ''))
    
    @horizontal_axis_font.setter
    def horizontal_axis_font(self, value: base.Font):
        self.h5_group['Chart'].attrs['HorizontalAxisFont'] = str(value)

    @property
    def vertical_axis_font(self) -> base.Font | None:
        """
        The font of the vertical axis.

        :getter: Returns the font of the vertical axis.
        :rtype: :obj:`base.Font` | None

        :setter: Sets the font of the vertical axis.
        :param new_value: The new font of the vertical axis.
        :type new_value: :obj:`base.Font`
        """
        return base.Font(self.h5_group['Chart'].attrs.get('VerticalAxisFont', ''))
    
    @vertical_axis_font.setter
    def vertical_axis_font(self, value: base.Font):
        self.h5_group['Chart'].attrs['VerticalAxisFont'] = str(value)

    @property
    def show_legend(self) -> base.Font | None:
        """
        Indicates whether the legend is shown.

        :getter: Returns whether the legend is shown.
        :rtype: :obj:`bool`

        :setter: Sets whether the legend is shown.
        :param new_value: Indicates whether the legend is shown.
        :type new_value: :obj:`bool`
        """
        return bool(self.h5_group['Chart'].attrs.get('ShowChartLegend', False))
    
    @show_legend.setter
    def show_legend(self, value: bool):
        self.h5_group['Chart'].attrs['ShowChartLegend'] = np.uint8(value)

    @property
    def series(self) -> Series.List:
        """
        :return: The series in the chart.
        :rtype: :obj:`Series.List`
        """
        return ChartGraphicsItem.Series.List(self.h5_group['Chart'])
    
    def add_series(self, table_id: str, x_column_id: int, y_column_id: int,
                   type: Series.Type = Series.Type.SCATTER, source: Series.Source = Series.Source.TABLE,
                   is_visibile: bool = True, marker_shape: Series.MarkerShape = Series.MarkerShape.CIRCLE,
                   marker_size: int = 15) -> Series:
        """
        Adds a new series to the chart.

        :param table_id: The ID of the table.
        :type table_id: :obj:`str`
        :param x_column_id: The ID of the X column.
        :type x_column_id: :obj:`int`
        :param y_column_id: The ID of the Y column.
        :type y_column_id: :obj:`int`
        :return: The new series.
        :rtype: :obj:`Series`
        """
        self.series.append({"ID": utils.create_uuid(),
                            "TableID": table_id, 
                            "XColumn": x_column_id, 
                            "YColumn": y_column_id,
                            "Type": type,
                            'Source': source,
                            'Visibility': int(is_visibile),
                            'MarkerShape': marker_shape,
                            'MarkerSize': marker_size})
        return self.series[-1]

class GraphicsItemFactory:
    """
    Factory class responsible for creating instances of GraphicsItem subclasses based on their type.
    """

    all_classes = {
        GraphicsItem.Type.NMRSpectrum: NMRSpectrumGraphicsItem,
        GraphicsItem.Type.Molecule: MoleculeGraphicsItem,
        GraphicsItem.Type.NMRPeakTable: NMRPeakTableGraphicsItem,
        GraphicsItem.Type.NMRMultipletTable: NMRMultipletTableGraphicsItem,
        GraphicsItem.Type.NMRMultipletReport: NMRMultipletReportGraphicsItem,
        GraphicsItem.Type.NMRParamTable: NMRParamTableGraphicsItem,
        GraphicsItem.Type.Text: TextGraphicsItem,
        GraphicsItem.Type.Image: ImageGraphicsItem,
        GraphicsItem.Type.AssignmentTable: AssignmentTableGraphicsItem,
        GraphicsItem.Type.Chart: ChartGraphicsItem
    }
    """A mapping of :obj:`GraphicsItem.Type` to their respective class implementations."""

    @staticmethod
    def create(h5_group) -> GraphicsItem:
        """
        Creates an instance of a :obj:`GraphicsItem.Type` subclass based on the type attribute of the provided h5 group.

        :param h5_group: The h5 group containing the attributes and data for the graphics item.
        :type h5_group: h5py.Group
        :return: An instance of the appropriate :obj:`GraphicsItem.Type` subclass.
        :rtype: :obj:`GraphicsItem.Type`
        """
        type = GraphicsItem.Type(h5_group.attrs['Type'])
        if type in GraphicsItemFactory.all_classes:
            return GraphicsItem.create(GraphicsItemFactory.all_classes[type], h5_group)
        return GraphicsItem.create(GraphicsItem, h5_group)
