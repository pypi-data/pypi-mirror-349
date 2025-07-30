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

import tempfile
import shutil
import os
import configparser
import beautifuljason.jason as jason

class Config:
    def __init__(self):
        self._load_config()

    def _load_config(self):
        config_parser = configparser.ConfigParser()
        config_path = os.path.join(jason.config.work_path, 'config.ini')
        config_parser.read(config_path)

        # Path to the directory containing test data
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

        # Path to the temporary directory. JASON's temp_path is used as a base.
        self.temp_dir = os.path.join(jason.config.temp_path, 'beautifuljason_unittests')
        if not os.path.isdir(self.temp_dir):
            os.mkdir(self.temp_dir, 0o755)

        # Ensure the temporary directory is clean before tests run
        if os.path.isdir(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                raise RuntimeError(f"Failed to remove the temporary directory: {e}")

        # Ensure the temporary directory doesn't exist
        assert not os.path.exists(self.temp_dir)

        # Create the temporary directory
        try:
            os.makedirs(self.temp_dir, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create the temporary directory: {e}")

        # Ensure the temporary directory exists
        assert os.path.exists(self.temp_dir)

# Create an instance of the TestConfig class
config = Config()

def newfile_path(file_name: str) -> str:
    """
    Generates a unique file path within the temp_dir using the provided file_name as a template.
    
    The base name of the provided file_name is used as a prefix, and its extension is preserved.
    The generated file path ensures no collision with existing files in the temp_dir.
    
    Args:
    - file_name (str): The template file name to base the unique file path on.

    Returns:
    - str: A unique file path within temp_dir.
    """
    
    splitext = os.path.splitext(file_name)
    with tempfile.NamedTemporaryFile(prefix=splitext[0] + '-', suffix=splitext[1], dir=config.temp_dir) as tmp_f:
        saved_file_name = tmp_f.name
    assert(not os.path.exists(saved_file_name))
    return saved_file_name

def datafile_copy_path(file_name: str) -> str:
    """
    Copies a specified data file to a temporary location with a unique name and returns its full path.
    
    The function ensures that the data file exists in the data directory before copying. 
    The copied file in the temporary location retains the original file's content but has a unique name.
    
    Args:
    - file_name (str): The name of the data file to be copied.

    Returns:
    - str: The full path to the copied file in the temporary location.
    """
    
    saved_file_name = newfile_path(file_name)
    assert(os.path.exists(os.path.join(config.data_dir, file_name)))
    shutil.copy(os.path.join(config.data_dir, file_name), saved_file_name)
    return saved_file_name

def datafile_path(file_name: str) -> str:
    """
    Returns the full path to a specified data file located in the data directory.
    
    The function checks if the specified file exists in the data directory before returning its path.
    
    Args:
    - file_name (str): The name of the data file whose path is to be retrieved.

    Returns:
    - str: The full path to the specified data file in the data directory.
    
    Raises:
    - AssertionError: If the specified file does not exist in the data directory.
    """    
    assert(os.path.isfile(os.path.join(config.data_dir, file_name)))
    return os.path.join(config.data_dir, file_name)
