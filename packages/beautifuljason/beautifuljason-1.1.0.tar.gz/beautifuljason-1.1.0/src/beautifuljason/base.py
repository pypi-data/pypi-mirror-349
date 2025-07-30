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

import beautifuljason.utils as utils 
from enum import IntEnum, IntFlag
from typing import Mapping, Sequence, Iterable
import numpy as np

class Font(dict):
    """
    Represents a font with various attributes. This class is designed to parse and represent fonts in a specific string format.

    :param font_str: The font string to parse. Accepts both str and bytes.
    :type font_str: :obj:`str` | :obj:`bytes`
    :raises TypeError: If the provided font_str is not of type str or bytes.
    """

    class FontWeight(IntEnum):
        """
        Represents the weight of the font using QFont::Weight values from Qt5.
        Qt6 values will be automatically converted to their Qt5 counterparts.
        """
        Thin = 0
        ExtraLight = 12
        Light = 25
        Normal = 50
        Medium = 57
        DemiBold = 63
        Bold = 75
        ExtraBold = 81
        Black = 87

        @classmethod
        def qt6_to_qt5_mapping(cls):
            return {
                100: 0,
                200: 12,
                300: 25,
                400: 50,
                500: 57,
                600: 63,
                700: 75,
                800: 81,
                900: 87
            }

        @classmethod
        def _convert_from_qt6(cls, value):
            return cls.qt6_to_qt5_mapping().get(value, value)

        @classmethod
        def _missing_(cls, value):
            if value in cls.qt6_to_qt5_mapping():
                return cls(cls.qt6_to_qt5_mapping()[value])
            raise ValueError(f"{value} is not a valid {cls.__name__}")
        
    class FontStyle(IntEnum):
        """Represents the style of the font, analogous to QFont::Style in Qt."""
        Normal = 0
        Italic = 1
        Oblique	= 2

    class FontStyleHint(IntEnum):
        """Represents the style hint of the font, analogous to QFont::StyleHint in Qt."""
        AnyStyle =	5
        Helvetica =	0
        SansSerif =	Helvetica
        Times	= 1
        Serif	= Times
        Courier	= 2
        TypeWriter	= Courier
        OldEnglish	= 3
        Decorative	= OldEnglish
        Monospace	= 7
        Fantasy	= 8
        Cursive	= 6
        System	= 4

    def __init__(self, font_str: str | bytes):
        super().__init__()

        f = utils.ensure_str(font_str)
        if not isinstance(f, str):
            raise TypeError("Expected str or bytes")
        if f.startswith('{@font.str:'):
            f = f[11:-1]
        f = f.split(',')

        self.update({
            'family': f[0],
            'point_size': float(f[1]),
            'pixel_size': int(f[2]),
            'style_hint': Font.FontStyleHint(int(f[3])),
            'weight': Font.FontWeight(int(f[4])),  # This handles Qt6 to Qt5 weight conversion
            'style': Font.FontStyle(int(f[5])),
            'underline': bool(int(f[6])),
            'strike_out': bool(int(f[7])),
            'fixed_pitch': bool(int(f[8])),
            'dummy1': bool(int(f[9]))
        })
        # Commented out because present in Qt6 and not in Qt5, to which the conversion is done 
        # if len(f) > 10:
        #     self['font_style'] = f[10]

    def __str__(self):
        family = self['family']
        point_size = self['point_size']
        pixel_size = self['pixel_size']
        style_hint = int(self['style_hint'])
        weight = int(self['weight'])
        style = int(self['style'])
        underline = int(self['underline'])
        strike_out = int(self['strike_out'])
        fixed_pitch = int(self['fixed_pitch'])
        dummy1 = int(self['dummy1'])

        return f"{family},{point_size},{pixel_size},{style_hint},{weight},{style},{underline},{strike_out},{fixed_pitch},{dummy1}"

    @staticmethod
    def default_font() -> 'Font':
        """
        Provides a default font representation. Currently implemented for Windows only.

        :return: A default font representation.
        :rtype: :obj:`Font`
        """
        return Font('MS Shell Dlg 2,8.1,-1,5,50,0,0,0,0,0')

    @staticmethod
    def qt6_default_font() -> 'Font':
        """
        .. versionadded:: 1.1.0
        
        Provides a default font representation for Qt6. Currently implemented for Windows only.

        :return: A default font representation.
        :rtype: :obj:`Font`

        """
        return Font('MS Shell Dlg 2,9,-1,5,75,0,0,0,0,0')

class Alignment(IntFlag):
    """
    Represents alignment options, analogous to Qt's Qt::AlignmentFlag.
    """
    Left = 0x01
    Right = 0x02
    HCenter = 0x04
    Justify = 0x08
    Top = 0x10
    Bottom = 0x20
    VCenter = 0x40
    Center = VCenter | HCenter
    Absolute = 0x80
    Leading = Left
    Trailing = Right

class Units(IntEnum):
    """
    Represents various unit types used in JASON.
    """
    NONE = 0
    HZ = 1
    KHZ = 2
    PPM = 3
    US = 4
    MS = 5 
    S = 6
    FPTS = 7
    TPTS = 8
    DEG = 9
    PERCENTS = 10
    TVIRT = 11
    FVIRT = 12
    CM2perS = 13
    M2perS = 14
    DPTS = 15
    CM2perS_LIN = 16
    M2perS_LIN = 17
    DPTS_LIN = 18
    GperCM = 19
    mTperM = 20
    TperM = 21
    GPTS = 22

class QMetaType_Type(IntEnum):
    """
    Represents data types analogous to Qt's QMetaType::Type.
    """
    UnknownType = 0
    Bool = 1
    Int = 2
    UInt = 3
    LongLong = 4
    ULongLong = 5
    Double = 6
    QChar = 7
    QVariantList = 9
    QString = 10
    QStringList = 11
    QByteArray = 12
    Long = 32
    Short = 33
    Char = 34
    Char16 = 56
    Char32 = 57
    ULong = 35
    UShort = 36
    SChar = 40
    UChar = 37
    Float = 38
    QSize = 21

class OriginalFileFormat(IntEnum):
    """
    Represents various file formats supported by JASON.
    """
    Unknown = 0
    JJH5 = 1
    JJD = 2
    JJJ = 3
    Spinsight = 4
    Vnmr = 5
    TopSpin = 6
    TopSpinProc = 7
    Spinevolution = 8
    Castep = 9
    JEOL_Delta = 10
    Molfile = 11
    Image = 12
    SVG = 13
    PDF = 14
    EMF = 15
    SIMPSON = 16
    Custom = 17
    JCAMPDX = 18
    WinNMR = 19
    WinNMRProc = 20 
    SPINit = 21
    Magritek = 22
    JEOL_Alice2 = 23

class PenStyle(IntEnum):
    """
    Represents various pen styles used in JASON. Corresponds to Qt's Qt::PenStyle.
    """
    NoPen = 0
    SolidLine = 1
    DashLine = 2
    DotLine = 3
    DashDotLine = 4
    DashDotDotLine = 5
    CustomDashLine = 6

class DummyH5Group:
    """
    A dummy representation of an :obj:`H5Group`.
    
    This class is used as a workaround for cases where the actual h5_group is None.
    It provides a mock interface to mimic the behavior of an :obj:`H5Group` without any actual data.
    """
    def __init__(self):
        self.attrs = {}
        self.create_group = lambda name: DummyH5Group()

    def __iter__(self):
        return iter(())

class H5Group:
    """
    Represents a group within an HDF5 file.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    """
    def __init__(self, h5_group):
        self.h5_group = h5_group

class IDedObject(H5Group):
    """
    Represents a group within an HDF5 file that has an ID.
    """
    @property
    def id(self)-> str:
        """
        Returns the ID of the object after validating its format.

        :return: The ID of the object.
        :rtype: :obj:`str`
        """
        return utils.check_uuid_str(self.h5_group.attrs.get('ID', ''))

class GroupList(H5Group):
    """
    Represents a list-like structure within an HDF5 file.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    :param list_group_name: The name of the group that contains the list.
    :type list_group_name: :obj:`str`
    :param value_class: The class that represents the values within the list.
    :type value_class: :obj:`type`
    """
    class Iterator(H5Group):
        """
        Iterator for the GroupList class.

        :param h5_group: The actual HDF5 group object.
        :type h5_group: h5py.Group
        :param obj_class: The class that represents the values within the list.
        :type obj_class: :obj:`type`
        :param iter_start: The starting index for the iterator.
        :type iter_start: :obj:`int`
        :param iter_step: The step size for the iterator.
        :type iter_step: :obj:`int`
        """
        def __init__(self, h5_group, obj_class, iter_start: int, iter_step: int):
            super().__init__(h5_group)
            self.obj_class = obj_class
            self.iter_index = iter_start
            self.iter_step = iter_step

        def __iter__(self):
            return self

        def __next__(self):
            try:
                result = self.obj_class(self.h5_group[str(self.iter_index)])
            except KeyError:
                raise StopIteration
            self.iter_index += self.iter_step
            return result

    def __init__(self, h5_group, list_group_name: str, value_class):
        if h5_group is None:
            h5_group = DummyH5Group()
        super().__init__(h5_group)
        self.list_group_name: str = list_group_name
        self.value_class = value_class
        self._len = 0
        for _ in self:
            self._len += 1

    def __iter__(self):
        if self.list_group_name in self.h5_group:
            return GroupList.Iterator(self.h5_group[self.list_group_name], self.value_class, 0, 1)
        else:
            return iter(())

    def __reversed__(self):
        if self.list_group_name in self.h5_group:
            return GroupList.Iterator(self.h5_group[self.list_group_name], self.value_class, self._len - 1, -1)
        else:
            return iter(())

    def __getitem__(self, index):
        try:
            if isinstance(index, slice):
                ifnone = lambda a, b: b if a is None else a
                start = ifnone(index.start, 0)
                stop = ifnone(index.stop, self._len)
                step = ifnone(index.step, 1)
                if  stop < 0:
                    stop = self._len + stop
                if start < 0:
                    start = self._len + start
                return [self.value_class(self.h5_group[self.list_group_name][str(self._len + i if i < 0 else i)]) for i in range(start, stop, step)]
            else:
                return self.value_class(self.h5_group[self.list_group_name][str(self._len + index if index < 0 else index)])
        except KeyError:
            raise IndexError(f"{self.__class__.__name__} index out of range")

    def __len__(self):
        return self._len

    def __bool__(self):
        return bool(self._len)

    def append(self, attrs: Sequence[Mapping] | Mapping) -> None:
        """
        Appends one or multiple items to the list.

        :param attrs: The item(s) to append to the list.
        :type attrs: :obj:`Sequence` | :obj:`Mapping`
        :raises TypeError: If the provided attrs is not of type Sequence or Mapping.        
        """
        if isinstance(attrs, Sequence):
            for attrs_dict in attrs:
                self.append(attrs_dict)
        elif isinstance(attrs, dict):
             # Create a new group if it doesn't exist
            if self.list_group_name not in self.h5_group:
                list_group = self.h5_group.create_group(self.list_group_name)
                # Set the container_type attribute on the group
                list_group.attrs['.container_type'] = 9
            else:
                list_group = self.h5_group[self.list_group_name]
    
            i_group = list_group.require_group(str(self._len))
            self._len += 1
            for key in attrs:
                value = attrs[key]
                if isinstance(value, Iterable) and not isinstance(value, str) and not isinstance(value, bytes):
                    try:
                        i_group.attrs[key] = np.array(value)
                    except TypeError:
                        key_group = i_group.require_group(key)
                        key_group.attrs['.container_type'] = 9
                        for i, v in enumerate(value):
                            key_group.attrs[str(i)] = v
                else:
                    i_group.attrs[key] = value
        else:
            raise TypeError("Expected dict")

class AttrList(H5Group):
    """
    Represents a list-like interface for attributes in an HDF5 group.

    :param h5_group: The actual HDF5 group object.
    :type h5_group: h5py.Group
    """

    class Iterator(H5Group):
        """
        Iterator for the :obj:`AttrList` class.

        :param h5_group: The actual HDF5 group object.
        :type h5_group: h5py.Group
        :param iter_start: The starting index for the iterator.
        :type iter_start: :obj:`int`
        :param iter_step: The step size for the iterator.
        :type iter_step: :obj:`int`
        """
        def __init__(self, h5_group, iter_start, iter_step):
            super().__init__(h5_group)
            self.iter_index = iter_start
            self.iter_step = iter_step
            
        def __iter__(self):
            return self

        def __next__(self):
            try:
                result = self.h5_group.attrs[str(self.iter_index)]
            except KeyError:
                raise StopIteration
            self.iter_index += self.iter_step
            return result

    def __init__(self, h5_group):
        super().__init__(h5_group)
        self._len = 0
        for _ in self:
            self._len += 1

    def __iter__(self):
        return AttrList.Iterator(self.h5_group, 0, 1)

    def __reversed__(self):
        return AttrList.Iterator(self.h5_group, self._len - 1, -1)

    def __getitem__(self, index):
        try:
            if isinstance(index, slice):
                ifnone = lambda a, b: b if a is None else a
                start = ifnone(index.start, 0)
                stop = ifnone(index.stop, self._len)
                step = ifnone(index.step, 1)
                if  stop < 0:
                    stop = self._len + stop
                if start < 0:
                    start = self._len + start
                return [self.h5_group.attrs[str(self._len + i if i < 0 else i)] for i in range(start, stop, step)]
            else:
                return self.h5_group.attrs[str(self._len + index if index < 0 else index)]
        except KeyError:
            raise IndexError(f"{self.__class__.__name__} index out of range")

    def __len__(self):
        return self._len

    def __bool__(self):
        return bool(self._len)

    def append(self, values):
        """
        Appends the given values as attributes.

        :param values: The values to append.
        :type values: :obj:`Sequence`
        """
        for value in values:
            self.h5_group.attrs.create(str(self._len), value)
            self._len += 1

    def clear(self):
        """
        Removes all attributes used by the :obj:`AttrList`.
        """
        for i in range(self._len):
            del self.h5_group.attrs[str(i)]
        self._len = 0
