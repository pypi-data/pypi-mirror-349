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

import argparse
import os.path
import datetime
import beautifuljason as bjason

# Custom column ID for the multiplet name column of the multiplet table.
# The value must be negative and unique.
ColID_NAME = -1

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Batch process and analyze spectral files. The script performs automatic analysis of spectra, creates tables, reports, and modifies visual properties. The results are saved in the specified output files.')
    parser.add_argument('input_files', nargs='+', help='List of spectral files to process.')
    parser.add_argument('-output_files', required=True, nargs='+', help='List of output files. Supported formats: .jjh5, .jjj, .jdx, and .pdf.')
    return parser.parse_args()

def customize_layout(doc: bjason.Document):
    """Customize the layout of spectral items."""
    for spec_item in doc.nmr_items:
        old_item_pos = spec_item.pos
        old_item_size = spec_item.size
        spec_item.pos = (old_item_pos[0] + old_item_size[0] * 0.3, old_item_pos[1])
        spec_item.size = (old_item_size[0] * 0.7, old_item_size[1] * 0.9)
    
def customize_appearance(doc: bjason.Document):
    """Customize the appearance of spectral items."""
    for spec_item in doc.nmr_items:
        spec_data = spec_item.spec_data(0)
        spec_item.show_y_axis = spec_data.ndim != 1
        spec_item.plot_1d_color = '#006400'

def add_parameter_tables(doc: bjason.Document):
    """Add parameter tables and adjust their layout."""
    for spec_item in doc.nmr_items:
        spec_data = spec_item.spec_data(0)
        params_item = doc.create_nmrparams_table(spec_item, spec_data)
        params_item.param_list.append([
            {'name': 'Filename', 'value': os.path.basename(spec_data.raw_data.spec_info.get_param('OrigFilename'))},
            {'name': 'Nuclide', 'value': spec_data.spec_info.nuclides[0] if len(spec_data.spec_info.nuclides) == 1 else ', '.join(spec_data.spec_info.nuclides)},
            {'name': 'Solvent', 'value': spec_data.raw_data.spec_info.get_param('Solvent')}
        ])
        spec_item_pos = spec_item.pos
        spec_item_size = spec_item.size
        new_x = spec_item_pos[0] - 3.0/7.0*spec_item_size[0]
        params_item.pos = (new_x, spec_item_pos[1])
        params_item.size = (spec_item_pos[0] - new_x, spec_item_size[1] * 0.3)

def add_peak_and_multiplet_tables(doc: bjason.Document):
    """Add peak and/or multiplet tables and adjust their layout. The multilet tables are created for 1H spectra only."""
    for spec_item in doc.nmr_items:
        spec_data = spec_item.spec_data(0)
        table_item: bjason.NMRPeakTableGraphicsItem | bjason.NMRMultipletTableGraphicsItem = None
        if spec_data.ndim == 1:
            if spec_data.spec_info.nuclides[0] == '1H':
                table_item = doc.create_nmrmultiplets_table(spec_item, spec_data)
                ColID = bjason.NMRMultipletTableGraphicsItem.ColumnID
                # Define visible columns and their order. Negative numbers correspond to custom columns. 
                table_item.visual_column_ids = (ColID_NAME, ColID.START0, ColID.END0, ColID.PEAKS_VOLUME, ColID.NORMALIZED)
                # Customize standard columns view  
                table_item.customized_columns.append((
                    {'Type': ColID.START0, 'Digits': 2},
                    {'Type': ColID.END0, 'Digits': 2},
                    {'Type': ColID.NORMALIZED, 'Digits': 1},
                    {'Type': ColID_NAME, 'Digits': -1, 'CustomTitle': 'Name'}
                ))
        if not table_item:
            table_item = doc.create_nmrpeaks_table(spec_item, spec_data)
            ColID = bjason.NMRPeakTableGraphicsItem.ColumnID
            if spec_data.ndim == 1:
                table_item.visual_column_ids = [ColID.POS0, ColID.WIDTH0, ColID.HEIGHT, ColID.VOLUME]
            elif spec_data.ndim == 2:
                table_item.visual_column_ids = [ColID.POS0, ColID.POS1, ColID.HEIGHT, ColID.VOLUME]
        table_item.show_title = True
        table_item.alternating_row_colors = True
        spec_item_pos = spec_item.pos
        spec_item_size = spec_item.size
        new_x = spec_item_pos[0] - 3.0/7.0*spec_item_size[0]
        table_item.pos = (new_x, spec_item_pos[1] + spec_item_size[1] * 0.3)
        table_item.size = (spec_item_pos[0] - new_x, spec_item_size[1] * 0.7)

def add_headers_and_logos(doc: bjason.Document):
    """Add headers and logos to the document."""
    logo_width = 200.0
    logo_image_data = None
    for spec_item in doc.nmr_items:
        spec_item.show_header = False
        text_item = doc.create_text_item()
        text_item.pos = spec_item.pos
        text_item.size = (spec_item.size[0], 60.0)
        text_item.text.html = '<b>{}</b><br/>Copyright (C) My Company. All rights reserved'.format(datetime.datetime.now().isoformat(timespec='seconds'))
        spec_item.pos = (spec_item.pos[0], text_item.pos[1] + text_item.size[1])
        if logo_image_data is None:
            logo_image_data = doc.create_image_data(os.path.abspath(os.path.join(os.path.dirname(__file__), 'JEOL_company_logo.png')))
        image_item = doc.create_image_item(logo_image_data.id)
        image_item.pos = (text_item.pos[0] + text_item.size[0] - logo_width, text_item.pos[1])
        image = image_item.image
        image_item.size = (logo_width, logo_width * image.height / image.width)

def add_multiplet_reports(doc):
    """Add multiplet reports to the document. The multiplet reports are created for 1H spectra only."""
    for spec_item in doc.nmr_items:
        spec_data = spec_item.spec_data(0)
        if spec_data.ndim == 1 and spec_data.spec_info.nuclides[0] == '1H':
            report_item = doc.create_nmrmultiplet_report(spec_item, spec_data)
            report_item.journal_format = 'Wiley'
            report_item.pos = spec_item.pos
            report_item.size = (0.5 * spec_item.size[0], 0.25 * spec_item.size[1])

def apply_analysis(jason, doc):
    """
    Apply specific analysis techniques based on the type of spectrum.
    Specifically, the script performs multiplet analysis for 1H spectra and peak picking for 13C and 2D spectra.
    """
    items_1H = []
    items_13C = []
    items_2D = []
    for spec_item in doc.nmr_items:
        spec_data = spec_item.spec_data(0)
        if spec_data.ndim == 2:
            items_2D.append(spec_item.id)
        elif spec_data.ndim == 1:
            if spec_data.spec_info.nuclides[0] == '1H':
                items_1H.append(spec_item.id)
            elif spec_data.spec_info.nuclides[0] == '13C':
                items_13C.append(spec_item.id)

    # Apply analysis actions to the document
    jason.apply_actions(doc, [{'name': 'multiplet_analysis', 'items': items_1H}, {'name': 'peak_picking', 'items': items_13C + items_2D}])
    for item in doc.items:
        if item.type == bjason.GraphicsItem.Type.NMRMultipletTable:
            # Add custom multiplet names to the Name column of the multiplet table
            table_item: bjason.NMRMultipletTableGraphicsItem = item
            for i, multiplet in enumerate(item.spec_data.multiplets):
                table_item.set_custom_value(multiplet.id, ColID_NAME, f'M{i+1}')

def main():
    """Main entry point of the script."""
    jason = bjason.JASON() # Create a JASON object 
    args = parse_arguments() # Parse command line arguments

    # Convert input and output file paths to absolute paths
    absolute_input_files = [os.path.abspath(file) for file in args.input_files]
    absolute_output_files = [os.path.abspath(file) for file in args.output_files]

    with jason.create_document(absolute_input_files) as doc:  # Open and process the spectral files in JASON
        customize_layout(doc) # Customize the layout of spectral items
        customize_appearance(doc) # Customize the appearance of spectral items
        add_parameter_tables(doc)  # Add parameter tables and adjust their layout
        add_peak_and_multiplet_tables(doc) # Add peak and/or multiplet tables and adjust their layout
        add_headers_and_logos(doc) # Add headers and logos to the document
        add_multiplet_reports(doc) # Add multiplet reports to the document
        apply_analysis(jason, doc) # Apply specific analysis techniques based on the type of spectrum
        jason.save(doc, absolute_output_files)  # Save the document to the specified output files

    # Optionally, open the resulting .jjh5 file in JASON for visual inspection
    jjh5_files = [output_file for output_file in absolute_output_files if output_file.endswith('.jjh5')]
    if jjh5_files:
        jason.launch(jjh5_files)

if __name__ == "__main__":
    main()
