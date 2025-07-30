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

def main():
    import os
    import tempfile
    import beautifuljason as bjason
    from PIL import Image as PILImage

    # Determine the path to the data directory inside the beautifuljason's tests subpackage
    test_data_dir = os.path.join(os.path.dirname(bjason.__file__), 'tests', 'data')

    # Specify input spectral file and define the path for the output PNG file
    input_1H_file = os.path.join(test_data_dir, "Ethylindanone_Proton-13-1.jdf")
    output_file = os.path.join(tempfile.gettempdir(), "Ethylindanone_Proton-13-1.png")

    # Create an instance of the JASON application interface
    jason = bjason.JASON()

    # Define and customize the default font settings
    font = bjason.base.Font.default_font()
    font['family'] = 'Arial'
    font['point_size'] = 12
    
    # Load the 1H spectral file, apply multiplet analysis, and customize its visual appearance
    with jason.create_document(input_1H_file, actions=[{'name': 'multiplet_analysis'}]) as doc:
        # Access the first spectral item and adjust its properties
        spec_item = doc.nmr_items[0]
        spec_item.header = 'Ethylindanone'
        spec_item.header_font = font
        spec_item.x_font = font
        spec_item.mult_intg_label_font = font
        spec_item.peak_label_font = font
        spec_item.plot_1d_color = '#3556d8'
        spec_item.show_y_axis = False

        # Save the customized document to an image file
        jason.save(doc, output_file)

    # Display the generated image using the default image viewer
    image = PILImage.open(output_file)
    image.show()

if __name__ == '__main__':
    main()
