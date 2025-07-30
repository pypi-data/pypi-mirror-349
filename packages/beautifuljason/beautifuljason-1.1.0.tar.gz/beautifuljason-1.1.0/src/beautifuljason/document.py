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

import beautifuljason.graphics as graphics
import beautifuljason.data as data
import beautifuljason.utils as utils
import numpy as np
from typing import Iterable
import os
import shutil
import h5py
from PIL import Image as PILImage

class Document:
    """
    This class is used to create, read, and modify JASON documents.
    It provides methods to create various types of graphics items, including text items, image items,
    NMR peaks tables, multiplet tables, assignment tables, and multiplet reports.
    
    It consists of two logical parts: data and graphics items.
    Data are the actual data objects (e.g., NMR spectra, molecules, images, texts, etc) that are stored in the document.
    Graphics items are the visual representations of these data objects in the document.
    The graphics items are linked to the data objects, allowing for easy access and manipulation of the data.

    **Key Features**:

    1. Access NMR spectra, molecules, images, and text data stored in the document.
        - :attr:`nmr_data`: Iterable of NMR spectra.
        - :attr:`mol_data`: Iterable of molecule data.
        - :attr:`image_data`: Iterable of image data.
        - :attr:`text_data`: Iterable of text data.  

    2. Access graphics items representing data visually.
        - :attr:`items`: List of all graphics items.
        - :attr:`nmr_items`: List of NMR spectrum graphics items.
        - :attr:`mol_items`: List of molecule graphics items.
        - :meth:`items_by_type`: Returns a list of graphics items of the specified type.

    3. New graphics items creation.
        - :meth:`create_text_item`: Creates a text graphics item.
        - :meth:`create_image_item`: Creates an image graphics item.
        - :meth:`create_chart_item`: Creates a chart graphics item.
        - :meth:`create_nmrpeaks_table`: Creates an NMR peaks table.
        - :meth:`create_nmrmultiplets_table`: Creates an NMR multiplets table.
        - :meth:`create_nmrassignments_table`: Creates an NMR assignments table.
        - :meth:`create_nmrmultiplet_report`: Creates an NMR multiplet report.
        - :meth:`create_nmrparams_table`: Creates an NMR parameters table.  

    :param file_name: The file name of the JASON document. The absolute path is recommended.
    :type file_name: str
    :param is_temporary: Whether the document is temporary. If True, the document will be deleted when the Document object is destroyed.
    :type is_temporary: bool
    :param mode: The mode in which the file should be opened. Defaults to 'a' (append mode). Use 'r' for read-only mode.
    :type mode: str
    """

    def __init__(self, file_name: str, is_temporary=False, mode='a'):
        self.page_margin = 10
        self.is_temporary = is_temporary
        self.file_name = file_name
        self.load(mode)

    def load(self, mode='a'):
        """
        Loads the JASON document file.

        :param mode: The mode in which the file should be opened. Defaults to 'a' (append mode). Use 'r' for read-only mode.
        :type mode: str
        """
        is_new_file = not os.path.isfile(self.file_name)
        self.h5_file = h5py.File(self.file_name, mode)

        if mode != 'r':
            # Create the document structure if it doesn't exist
            doc_group = self.h5_file.require_group('JasonDocument') 
            doc_group.require_group('NMR')
            doc_group.require_group('General')
            doc_group.require_group('Molecules')
            if is_new_file:
                self.h5_file.attrs['Version.Major'] = np.uint8(2)
                self.h5_file.attrs['Version.Minor'] = np.uint32(1994)
                doc_group.attrs['DPI'] = np.double(120.0)
                doc_group.attrs['HPages'] = np.int32(2)
                doc_group.attrs['VPages'] = np.int32(2)
                doc_group.attrs['Orientation'] = np.int32(1)
                doc_group.attrs['Units'] = np.int32(1)
                doc_group.attrs['Margins'] = np.array([0.0, 0.0, 0.0, 0.0], np.double)
                doc_group.attrs['PageSize'] = np.array([595, 842], np.int32)

    @property
    def items(self) -> list[graphics.GraphicsItem]:
        """
        :return: A list of all graphics items in the document.
        :rtype: :obj:`list` of :obj:`graphics.GraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5', mode='r') as doc:
                for item in doc.items:
                    print(item.type.name, item.pos, item.size)
        """
        return [graphics.GraphicsItemFactory.create(elem) for elem in utils.group_to_list(self.h5_file, '/JasonDocument/Items')]

    @property
    def nmr_data(self) -> Iterable[data.NMRSpectrum]:
        """
        :return: A list of all NMR data objects (spectra) in the document.
        :rtype: :obj:`Iterable` of :obj:`NMRSpectrum`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5', mode='r') as doc:
                for spec in doc.nmr_data:
                    print(bjason.utils.ensure_str(spec.spec_info.get_param("Title")))
        """
        return data.NMRSpectrum.List(self.h5_file['/JasonDocument/NMR'])

    @property
    def text_data(self) -> Iterable[data.Text]:
        """
        :return: A list of all text data objects in the document.
        :rtype: :obj:`Iterable` of :obj:`data.Text`

        **Example Usage:**

        .. code-block:: python
            
                import beautifuljason as bjason
    
                with bjason.Document('example.jjh5', mode='r') as doc:
                    for text in doc.text_data:
                        print(bjason.utils.ensure_str(text.html))
        """
        return data.Text.List(self.h5_file['/JasonDocument/General']) if '/JasonDocument/General' in self.h5_file else []

    @property
    def image_data(self) -> Iterable[data.Image]:
        """
        :return: A list of all image data objects in the document.
        :rtype: :obj:`Iterable` of :obj:`data.Image`

        **Example Usage:**
        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5', mode='r') as doc:
                for image in doc.image_data:
                    print(bjason.utils.ensure_str(image.id))
        """
        return data.Image.List(self.h5_file['/JasonDocument/General']) if '/JasonDocument/General' in self.h5_file else []

    @property
    def mol_data(self) -> Iterable[data.Molecule]:
        """
        .. versionadded:: 1.1.0

        :return: A list of all molecule data objects in the document.
        :rtype: :obj:`Iterable` of :obj:`data.Molecule`


        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5', mode='r') as doc:
                for mol in doc.mol_data:
                    for atom in mol.atoms:
                        print(atom.type.name, atom.x, atom.y, atom.z if atom.z else '')
        """
        return data.Molecule.List(self.h5_file['/JasonDocument/Molecules']) if '/JasonDocument/Molecules' in self.h5_file else []

    @property
    def nmr_items(self) -> list[graphics.NMRSpectrumGraphicsItem]:
        """
        A convenience property to get all NMR spectrum graphics items in the document.

        :return: A list of all NMR spectrum graphics items in the document.
        :rtype: :obj:`list` of :obj:`graphics.NMRSpectrumGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5', mode='r') as doc:
                for nmr_item in doc.nmr_items:
                    print(nmr_item.header)
                    for spec in nmr_item.spec_data_list:
                        print("  ", spec.spec_info.nuclides[0], bjason.utils.ensure_str(spec.spec_info.get_param("Title")))
        """
        return self.items_by_type(graphics.GraphicsItem.Type.NMRSpectrum)
    
    @property
    def mol_items(self) -> list[graphics.MoleculeGraphicsItem]:
        """
        .. versionadded:: 1.1.0

        A convenience property to get all molecule graphics items in the document.

        :return: A list of all molecule graphics items in the document.
        :rtype: :obj:`list` of :obj:`graphics.MoleculeGraphicsItem`


        **Example Usage:**

        .. code-block:: python
            
                import beautifuljason as bjason
    
                with bjason.Document('example.jjh5', mode='r') as doc:
                    for mol_item in doc.mol_items:
                        for atom in mol_item.mol_data().atoms:
                            print(atom.type.name, atom.x, atom.y, atom.z if atom.z else '')
        """
        return self.items_by_type(graphics.GraphicsItem.Type.Molecule)
    
    def items_by_type(self, item_type: graphics.GraphicsItem.Type | graphics.GraphicsItem) -> list:
        """
        .. versionadded:: 1.1.0

        Returns a list of graphics items of the specified type.

        :param item_type: The type of graphics item to filter by.
        :type item_type: :obj:`GraphicsItem.Type`

        :return: A list of graphics items of the specified type.
        :rtype: :obj:`list`

        """
        return list(filter(lambda item: (item.type == item_type) if isinstance(item_type, graphics.GraphicsItem.Type) else isinstance(item, item_type), self.items))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove()

    def __del__(self):
        self.remove()

    def close(self):
        """
        Closes the document file.
        """
        if os.path.isfile(self.file_name):
            self.h5_file.close()

    def remove(self):
        """
        Closes and removes the document file if it's marked as temporary.
        """
        self.close()
        if self.is_temporary and os.path.isfile(self.file_name):
            os.remove(self.file_name)

    def copy(self, file_name: str | bytes):
        """
        Copies the JASON document to a new file.

        .. note:: 
            Starting from h5py v3.4, it's essential to close the h5py.File object before using the 'copy' method. 
            This constraint diminishes the utility of the 'copy' method. Intentionally, the `self.close()` line 
            is omitted in this method, delegating the responsibility of calling 'close' to the programmer.

        :param file_name: The destination file name.
        :type file_name: str | bytes
        """
        shutil.copyfile(self.file_name, file_name)

    def _create_item_elem(self, item_type):
        items_group = self.h5_file.require_group('/JasonDocument/Items')
        items_group.attrs['.container_type'] = 9
        items_len = len(self.items)
        item_elem = items_group.create_group(str(items_len))
        item_elem.attrs['Geometry'] = (0.0, 0.0, 0.0, 0.0)
        item_elem.attrs['Pos'] = (0.0, 0.0)
        item_elem.attrs['TransformOrigPoint'] = (0.0, 0.0)
        item_elem.attrs['Rotation'] = 0.0
        item_elem.attrs['ZValue'] = 0.0
        item_elem.attrs['ID'] = utils.create_uuid()
        item_elem.attrs['Type'] = int(item_type)

        return item_elem

    def create_nmrpeaks_table(self, spec_item: graphics.NMRSpectrumGraphicsItem, spec_data: data.NMRSpectrum) -> graphics.NMRPeakTableGraphicsItem:
        """
        Creates a new NMR peaks table in the document.
        Requires the document to be opened in append mode ('a').

        :param spec_item: The spectrum graphics item to which the table is linked.
        :type spec_item: :obj:`NMRSpectrumGraphicsItem`
        :param spec_data: The NMR spectrum data for the table.
        :type spec_data: :obj:`data.NMRSpectrum`

        :return: The created NMR peaks table graphics item.
        :rtype: :obj:`graphics.NMRPeakTableGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                nmr_item = doc.nmr_items[0]
                peaks_table = doc.create_nmrpeaks_table(nmr_item, nmr_item.spec_data_list[0])
                peaks_table.pos = (nmr_item.pos[0], nmr_item.pos[1] + nmr_item.size[1] + 2*doc.page_margin)
                peaks_table.size = nmr_item.size
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.NMRPeakTable)
        item: graphics.NMRPeakTableGraphicsItem = self.items[-1]
        item.set_defaults()

        item.linked_ids += [spec_item.id]
        spec_item.linked_ids += [item.id]

        peaks_table = item_elem.create_group('PeaksTable')
        peaks_table.attrs['SpectrumID'] = spec_data.id

        return item

    def create_nmrmultiplets_table(self, spec_item: graphics.NMRSpectrumGraphicsItem, spec_data: data.NMRSpectrum) -> graphics.NMRMultipletTableGraphicsItem:
        """
        Creates a new NMR multiplets table in the document.
        Requires the document to be opened in append mode ('a').

        :param spec_item: The spectrum graphics item to which the table is linked.
        :type spec_item: :obj:`NMRSpectrumGraphicsItem`
        :param spec_data: The NMR spectrum data for the table.
        :type spec_data: :obj:`data.NMRSpectrum`

        :return: The created NMR multiplets table graphics item.
        :rtype: :obj:`graphics.NMRMultipletTableGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                mol_item = doc.mol_items[0]
                assignments_table = doc.create_nmrassignments_table(mol_item, mol_item.mol_data())
                assignments_table.pos = (mol_item.pos[0], mol_item.pos[1] + mol_item.size[1] + 2*doc.page_margin)
                assignments_table.size = mol_item.size
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.NMRMultipletTable)
        item: graphics.NMRMultipletTableGraphicsItem = self.items[-1]
        item.set_defaults()

        item.linked_ids += [spec_item.id]
        spec_item.linked_ids += [item.id]

        multiplets_table = item_elem.create_group('MultipletsTable')
        multiplets_table.attrs['SpectrumID'] = spec_data.id

        return item

    def create_nmrassignments_table(self, mol_item: graphics.MoleculeGraphicsItem, mol_data: data.Molecule) -> graphics.AssignmentTableGraphicsItem:
        """
        .. versionadded:: 1.1.0
        
        Creates a new NMR assignments table in the document.
        Requires the document to be opened in append mode ('a').

        :param mol_item: The molecule graphics item to which the table is linked.
        :type mol_item: :obj:`MoleculeGraphicsItem`
        :param mol_data: The molecule data for the table.
        :type mol_data: :obj:`data.Molecule`

        :return: The created NMR assignments table graphics item.
        :rtype: :obj:`graphics.AssignmentTableGraphicsItem`


        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                mol_item = doc.mol_items[0]
                assignments_table = doc.create_nmrassignments_table(mol_item, mol_item.mol_data())
                assignments_table.pos = (mol_item.pos[0] + 2*doc.page_margin, mol_item.pos[1] + 5*doc.page_margin)
                assignments_table.size = tuple(dim / 3 for dim in mol_item.size)
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.AssignmentTable)
        item: graphics.AssignmentTableGraphicsItem = self.items[-1]
        item.set_defaults()

        item.linked_ids += [mol_item.id]
        mol_item.linked_ids += [item.id]

        assignments_table = item_elem.create_group('AssignmentTable')
        assignments_table.attrs['MoleculeID'] = mol_data.id

        return item

    def create_nmrmultiplet_report(self, spec_item: graphics.NMRSpectrumGraphicsItem, spec_data: data.NMRSpectrum) -> graphics.NMRMultipletReportGraphicsItem:
        """
        Creates a new NMR multiplet report in the document.
        Requires the document to be opened in append mode ('a').

        :param spec_item: The spectrum graphics item to which the report is linked.
        :type spec_item: :obj:`graphics.NMRSpectrumGraphicsItem`
        :param spec_data: The NMR spectrum data for the report.
        :type spec_data: :obj:`data.NMRSpectrum`

        :return: The created NMR multiplet report graphics item.
        :rtype: :obj:`graphics.NMRMultipletReportGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                nmr_item = doc.nmr_items[0]
                multiplet_report = doc.create_nmrmultiplet_report(nmr_item, nmr_item.spec_data_list[0])
                multiplet_report.pos = (nmr_item.pos[0] + 2*doc.page_margin, nmr_item.pos[1] + 5*doc.page_margin)
                multiplet_report.size = tuple(dim / 3 for dim in nmr_item.size)
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.NMRMultipletReport)
        item: graphics.NMRMultipletReportGraphicsItem = self.items[-1]

        item.linked_ids += [spec_item.id]
        spec_item.linked_ids += [item.id]

        multiplets_report = item_elem.create_group('MultipletsReport')
        multiplets_report.attrs['SpectrumID'] = spec_data.id

        return item

    def create_nmrparams_table(self, spec_item: graphics.NMRSpectrumGraphicsItem, spec_data: data.NMRSpectrum) -> graphics.NMRParamTableGraphicsItem:
        """
        Creates a new NMR parameters table in the document.
        Requires the document to be opened in append mode ('a').

        :param spec_item: The spectrum graphics item to which the table is linked.
        :type spec_item: :obj:`graphics.NMRSpectrumGraphicsItem`
        :param spec_data: The NMR spectrum data for the table.
        :type spec_data: :obj:`data.NMRSpectrum`

        :return: The created NMR parameters table graphics item.
        :rtype: :obj:`graphics.NMRParamTableGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                nmr_item = doc.nmr_items[0]
                params_table = doc.create_nmrparams_table(nmr_item, nmr_item.spec_data_list[0])
                params_table.pos = (nmr_item.pos[0], nmr_item.pos[1] + nmr_item.size[1] + 2*doc.page_margin)
                params_table.size = nmr_item.size
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.NMRParamTable)
        item: graphics.NMRParamTableGraphicsItem = self.items[-1]
        item.set_defaults()

        item.linked_ids += [spec_item.id]
        spec_item.linked_ids += [item.id]
        
        params_table = item_elem.create_group('ParamsTable')
        params_table.create_group('list').attrs['.container_type'] = 9
        params_table.attrs['id'] = spec_data.id

        return item

    def create_text_item(self, html_str: str='') -> graphics.TextGraphicsItem:
        """
        Creates a new text item in the document.
        Requires the document to be opened in append mode ('a').

        :param html_str: The HTML text to be added.
        :type html_str: :obj:`str`

        :return: The created text graphics item.
        :rtype: :obj:`graphics.TextGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                new_text_item = doc.create_text_item("<h1>Hello, World!</h1>")
                print(new_text_item.text.html)
                # Make sure the text item is available in the list of text items
                for text_item in doc.items_by_type(bjason.graphics.GraphicsItem.Type.Text):
                    if text_item.id == new_text_item.id:
                        print(bjason.utils.ensure_str(text_item.text.html))
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.Text)

        data_id = utils.create_uuid()
        item_elem.create_group('TextItem').attrs['TextID'] = data_id
        data_group = self.h5_file.require_group('/JasonDocument/General/TextDocuments')
        data_group.attrs['.container_type'] = 9
        data_elem = data_group.create_group(str(len(utils.group_to_list(data_group, ''))))
        data_elem.attrs['ID'] = data_id

        item: graphics.TextGraphicsItem = self.items[-1]
        item.text.html = html_str

        return item

    def create_image_item(self, data_id: str) -> graphics.ImageGraphicsItem:
        """
        Creates a new image item in the document.
        Requires the document to be opened in append mode ('a').

        .. seealso::
            - :meth:`create_image_data` for creating image data from an image file.

        :param data_id: The ID of the image data object.
        :type data_id: :obj:`str`

        :return: The created image graphics item.
        :rtype: :obj:`graphics.ImageGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                image_data = doc.create_image_data('example.png')
                new_image_item = doc.create_image_item(image_data.id)
                new_image_item.pos = (0, 0)
                new_image_item.size = (100, 100)
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.Image)

        image_draw = item_elem.create_group('ImageDraw')
        image_draw.attrs['ImageID'] = data_id
        image_draw.attrs['MaskColor'] = (0, 0, 0, 255, 0)

        return self.items[-1]

    def create_image_data(self, image_file: str) -> data.Image:
        """
        Creates a new image data in the document.
        Requires the document to be opened in append mode ('a').
        The image data is created from the specified image file.
        It's necessary to create `ImageGraphicsItem` items in the document to display the image data.
        Multiple image items can be linked to the same image data.

        .. seealso:: 
            - :meth:`create_image_item` for creating an image item linked to the image data.

        :param image_file: The path to the image file.
        :type image_file: :obj:`str`

        :return: The created image data object.
        :rtype: :obj:`Image`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                image_data = doc.create_image_data('example.png')
                new_image_item = doc.create_image_item(image_data.id)
                new_image_item.pos = (0, 0)
                new_image_item.size = (100, 100)
        """

        data_id = utils.create_uuid()

        data_group = self.h5_file.require_group('/JasonDocument/General/Pixmaps')
        data_group.attrs['.container_type'] = 9
        data_elem = data_group.create_group(str(len(utils.group_to_list(data_group, ''))))
        data_elem.attrs['ID'] = data_id

        with PILImage.open(image_file) as image:
            rgba_image = image.convert('RGBA')
            data_array = np.asarray(rgba_image)
            image_ds = data_elem.create_dataset('Pixmap', data=data_array)
            image_ds.attrs['CLASS'] = np.bytes_(b'IMAGE')
            image_ds.attrs['IMAGE_MINMAXRANGE'] = np.array([0, 255], np.uint8)
            image_ds.attrs['IMAGE_SUBCLASS'] = np.bytes_(b'IMAGE_TRUECOLOR')
            image_ds.attrs['IMAGE_VERSION'] = np.bytes_(b'1.2')
            image_ds.attrs['INTERLACE_MODE'] = np.bytes_(b'INTERLACE_PIXEL')

        return data.Image(data_elem)
    
    def create_chart_item(self) -> graphics.ChartGraphicsItem:
        """
        .. versionadded:: 1.1.0

        Creates a new chart item in the document.
        Requires the document to be opened in append mode ('a').

        :return: The created chart graphics item.
        :rtype: :obj:`graphics.ChartGraphicsItem`

        **Example Usage:**

        .. code-block:: python

            import beautifuljason as bjason

            with bjason.Document('example.jjh5') as doc:
                new_chart_item = doc.create_chart_item()
                # In the code below we assume that doc.items[1] is a NMRPeakTableGraphicsItem
                series = new_chart_item.add_series(doc.items[1].id, bjason.NMRPeakTableGraphicsItem.ColumnID.POS0, bjason.NMRPeakTableGraphicsItem.ColumnID.VOLUME)
                series.name = "My Series"
                new_chart_item.pos = (doc.page_margin, doc.page_margin)
                new_chart_item.size = (400, 300)
        """
        item_elem = self._create_item_elem(graphics.GraphicsItem.Type.Chart)

        chart_elem = item_elem.create_group('Chart')
        series_elem = chart_elem.create_group('Series')
        series_elem.attrs['.container_type'] = 9

        return self.items[-1]