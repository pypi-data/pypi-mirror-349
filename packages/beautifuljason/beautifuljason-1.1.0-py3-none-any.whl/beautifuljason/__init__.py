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

from . import base
from . import data
from . import document
from . import jason
from . import graphics
from . import utils

from .jason import JASON
from .jason import JASONException
from .document import Document
from .graphics import GraphicsItem
from .graphics import NMRSpectrumGraphicsItem
from .graphics import TableGraphicsItem
from .graphics import NMRPeakTableGraphicsItem
from .graphics import NMRMultipletTableGraphicsItem
from .graphics import NMRParamTableGraphicsItem
from .graphics import NMRMultipletReportGraphicsItem
from .graphics import TextGraphicsItem
from .graphics import ImageGraphicsItem
from .graphics import AssignmentTableGraphicsItem
from .graphics import MoleculeGraphicsItem
from .graphics import ChartGraphicsItem
from .data import Text
from .data import Image
from .data import NMRSpecInfo
from .data import NMREntry
from .data import NMRSpectrum
from .data import NMRPeak
from .data import NMRMultiplet
from .data import NMRProcessing
from .data import Molecule
from .base import Font
from .base import OriginalFileFormat
from .base import Units
from .base import Alignment

from importlib.metadata import version

try:
    __version__ = version("beautifuljason")
except Exception:
    __version__ = "unknown"