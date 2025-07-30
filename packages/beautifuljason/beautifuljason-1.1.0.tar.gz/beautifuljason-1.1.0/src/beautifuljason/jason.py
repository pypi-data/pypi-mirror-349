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

import beautifuljason.document as document
import configparser
import platform
import subprocess
import os.path
import tempfile
import pathlib
import json
import platform
from functools import cached_property
from copy import copy
from collections.abc import Sequence

class JASONException(Exception):
    """Exception raised for errors specific to the JASON application."""
    pass

class Config:
    """
    Represents the configuration settings for the JASON application.
    This class handles loading, saving, and managing the paths to the JASON application instances.
    It also provides methods to add, delete, and set preferred paths for JASON instances.

    The configuration is stored in a file named `config.ini` located in the user's home directory under `.beautifuljason`.
    The configuration file contains paths to different JASON instances and a preferred path key.

    The configuration file is created with default values if it does not exist.
    The default paths are set based on the operating system (Windows or macOS).

    .. note::

        Don't use the `Config` class directly. Use the :ref:`jason_config` tool for configuring the JASON application path.

    """

    if platform.system() == "Windows":
        DEFAULT_CONFIG_CONTENTS = """[JASON]
path_1 = C:\Program Files\JEOL\JASON\JASON.exe
path_2 = C:\Program Files\JEOL\JASON-dev\JASON-dev.exe"""
    elif platform.system() == "Darwin":  # Darwin indicates macOS
        DEFAULT_CONFIG_CONTENTS = """[JASON]
path_1 = /Applications/JASON.app/Contents/MacOS/JASON
path_2 = /Applications/JASON-dev.app/Contents/MacOS/JASON-dev"""
    else:
        # Default to a generic configuration or raise an exception
        DEFAULT_CONFIG_CONTENTS = """[JASON]
path_1 =
path_2 ="""

    def __init__(self):
        self.app_path = None
        self.error = ''

        # Define a work directory
        self.work_path = os.path.join(str(pathlib.Path.home()), '.beautifuljason')
        if not os.path.isdir(self.work_path):
            os.mkdir(self.work_path, 0o755)

        # Define a temporary directory. It can be overridden in the config.ini. See _load_config().
        self.temp_path = tempfile.gettempdir()

        self._load_config()

    @property
    def config_path(self) -> str:
        """
        :return: The path to the config.ini file.
        :rtype: str
        """
        return os.path.join(self.work_path, 'config.ini')

    def _load_config(self):
        """Load the JASON application path from the config.ini."""

        self.app_path = None
        self.error = ''

        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)
        
        # Read the temp_path from the config if it exists
        if config_parser.has_option('JASON', 'temp_path'):
            self.temp_path = config_parser.get('JASON', 'temp_path')

        # Check if the config is empty and populate it from the default if necessary
        if not config_parser.sections():
            with open(self.config_path, 'w') as configfile:
                configfile.write(self.DEFAULT_CONFIG_CONTENTS)
                
            config_parser.read(self.config_path)  # Reload the config after populating

        # If a preferred path key is specified, use that first
        preferred_key = config_parser.get('JASON', 'preferred_path_key', fallback=None)
        if preferred_key and config_parser.has_option('JASON', preferred_key):
            preferred_path = config_parser.get('JASON', preferred_key)
            if os.path.exists(preferred_path):
                self.app_path = preferred_path
            else:
                self.error = f"Preferred path '{preferred_path}' specified in config.ini not found."
                return
            
        if self.app_path is None:
            # If the preferred path is not found or not specified, fall back to the default paths
            path_keys = [f"path_{i}" for i in range(1, 11)]  # Check paths from path_1 to path_10
            for key in path_keys:
                if config_parser.has_option('JASON', key):
                    path = config_parser.get('JASON', key)
                    if os.path.exists(path):
                        self.app_path = path
                        break

        if self.app_path is None:
            self.error = "No valid JASON application path found in config.ini."

    def find_path(self, path: str) -> int | None:
        """Find the index of a JASON instance path in the config.

        :param path: The path to find in the JASON instance config.
        :type path: str

        :return: The index of the path if found, otherwise None.
        :rtype: int | None
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)

        for key in config_parser['JASON']:
            if config_parser['JASON'][key] == path:
                return int(key.split('_')[1])
        return None

    def add_path(self, new_path: str) -> int:
        """Add a new JASON instance path to the config.

        :param new_path: The new path to add for the JASON instance.
        :type new_path: str

        :return: The index of the new path or the existing index if the path already exists.
        :rtype: int
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)
        
        # Check if the path already exists
        path_index = self.find_path(new_path)
        if path_index is not None:
            return path_index
        
        highest_index = 0

        # Iterate over all items in the 'JASON' section and find the highest path index
        for key in config_parser['JASON']:
            if key.startswith('path_'):
                index = int(key.split('_')[1])
                highest_index = max(highest_index, index)

        # Create a new slot for the new path
        new_key = f"path_{highest_index + 1}"
        config_parser.set('JASON', new_key, new_path)
        
        with open(self.config_path, 'w') as configfile:
            config_parser.write(configfile)
            
        return highest_index + 1

    def set_preferred_path_index(self, path_index: int):
        """Set a new preferred JASON instance path index.

        :param path_index: The new path to set as preferred for the JASON instance.
        :type path_index: int
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)
        path_key = f"path_{path_index}"
        if not config_parser.has_option('JASON', path_key):
            raise JASONException(f"No path found at index {path_index}.")
        config_parser.set('JASON', 'preferred_path_key', path_key)
        with open(self.config_path, 'w') as configfile:
            config_parser.write(configfile)
        self._load_config()  # Reload the configuration after setting the preferred path

    # Return the preferred path index or None if the preferred path is not set
    @property
    def preferred_path_index(self) -> int | None:
        """
        :return: The index of the preferred JASON instance path.
        :rtype: int | None
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)
        preferred_key = config_parser.get('JASON', 'preferred_path_key', fallback=None)
        if preferred_key:
            return int(preferred_key.split('_')[1])
        else:
            return None

    def delete_path_by_index(self, index):
        """Delete a JASON instance path by its index.

        :param index: The index of the path to delete.
        :type index: int
        """

        if index == 1 or index == 2:
            raise JASONException("The default paths at index 1 and 2 cannot be deleted.")

        config_parser = configparser.ConfigParser()
        config_parser.read(self.config_path)

        # Find the key for the path at the specified index
        path_key = f"path_{index}"
        if not config_parser.has_option('JASON', path_key):
            raise JASONException(f"No path found at index {index}.")

        # Remove the path from the config
        config_parser.remove_option('JASON', path_key)
        with open(self.config_path, 'w') as configfile:
            config_parser.write(configfile)

        # If the path was the preferred path, remove the preferred path key
        if index == self.preferred_path_index:
            config_parser.remove_option('JASON', 'preferred_path_key')

        self._load_config()

    def reset(self):
        """Reset the configuration to the default settings."""
        with open(self.config_path, 'w') as configfile:
            configfile.write(self.DEFAULT_CONFIG_CONTENTS)
        
        self._load_config()  # Reload the configuration after resetting

    @property
    def all_paths(self) -> list[tuple[int, str]]:
        """
        :return: A list of all JASON application paths from the config.
        :rtype: :obj:`list[tuple[int, str]]`
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(config.config_path)

        paths = []
        for key in config_parser['JASON']:
            if key.startswith('path_'):
                index = int(key.split('_')[1])
                path = config_parser['JASON'][key]
                paths.append((index, path))
        return paths

# Instantiate the Config class
config = Config()

class JASON:
    """
    This class provides methods to interact with the JASON application.
    It allows users to create documents, apply actions, and save results in various formats.

    :param app_path: The path to the JASON application. If not provided, it will be fetched from the configuration, which is the recommended way.
    :type app_path: str | None

    :param plugins: Defines the plugins to load. ['off'] skips loading, while 'None' or [] loads all.
    :type plugins: list[str] | None

    :raises JASONException: If the JASON app path is not specified or does not exist.

    .. _example_jason_usage:

    JASON Class Example Usage
    =========================

    .. code-block:: python

        from beautifuljason import JASON

        # Initialize the JASON interface
        jason = JASON()

        # Create a document for the specified file using the rules
        with jason.create_document(
                file_names=["example.jdf"],
                rules="example_rules.jjr"  # Use the rules file for processing, analysis and layout
            ) as doc:

            # Save the document
            jason.save(doc, file_names="output.pdf")
    """

    def __init__(self, app_path: str | None = None, plugins: list[str] = ['off']):
        if app_path is None:
            app_path = config.app_path
            if not app_path:
                raise JASONException('JASON path not specified in config and not provided during initialization.')

        if not os.path.isfile(app_path):
            raise JASONException(f'JASON path does not exist: {app_path}')

        self.app_dir = os.path.dirname(app_path)
        self.app_name = os.path.join('.', os.path.basename(app_path))
        if plugins:
            self.plugin_args = [item for plugin in plugins for item in ['--plugins', f'"{plugin}"' if ' ' in plugin else plugin]]
        else:
            self.plugin_args = []

        if len(self.version) != 3:
            raise JASONException(f'Unexpected version: {self.version}')

        minVersion = (0, 1, 1924)
        if self.version < minVersion:
            raise JASONException(f'Old JASON version: {".".join(map(str, self.version))}. The minimal supported version is {".".join(map(str, minVersion))}')
        
        if self.version < (3, 2, 6555):
            self.plugin_args = []

    def _run(self, args: list[str]) -> subprocess.CompletedProcess:
        """
        Run the JASON application with the specified arguments.
        This method is used internally. However, it can be used to run JASON in headless mode in complex scenarios.
        It is recommended to use the :meth:`create_document` method instead.

        :param args: The arguments to pass to the JASON application.
        :type args: :obj:`list[str]`

        :return: The result of the subprocess run.
        :rtype: :obj:`subprocess.CompletedProcess`
        """
        old_wd = os.getcwd()    
        os.chdir(self.app_dir)
        try:
            runres = subprocess.run([self.app_name, '--headless'] + args + self.plugin_args, capture_output=True)
        finally:
            os.chdir(old_wd)
        if runres.returncode != 0:
            raise JASONException("JASON finished with an error code {}".format(runres.returncode))
        return runres

    @cached_property
    def version(self) -> tuple[int, int, int] | None:
        """
        :return: The JASON version as a tuple of integers. Empty tuple if the version cannot be determined.
        :rtype: :obj:`tuple` of :obj:`int` | :obj:`tuple`
        """
        runres = self._run(['-v'])
        if runres.returncode == 0:
            return tuple(int(i) for i in runres.stdout.split(b' ')[-1].split(b'.'))
        else:
            return None

    def create_document(self, file_names: list[str] | str, actions: list[dict] = [], rules: str = "off") -> 'document.Document':
        """
        Creates a JASON document based on provided files and actions.

        :param file_names: List of file names or a single file name to be processed.
        :type file_names: list[str] | str

        :param actions: Actions to apply to the files. Defaults to an empty list.
            Each action is a dictionary with the action name and parameters.
            Actions include:

            - `'peak_picking'`
            - `'integration'`
            - `'multiplet_analysis'`
            - `'processing'`

            **Simple examples**:

            .. code-block:: python

                [{'name': 'peak_picking'}]

            or
                
            .. code-block:: python

                [{'name': 'integration'}]

            or

            .. code-block:: python

                [{'name': 'multiplet_analysis'}]

            These imply that the default JASON parameters are used.

            **More complex example**:

            .. code-block:: python

                [
                    {
                        "name": "processing",
                        "params": "proton.jjp"
                    },
                    {
                        "name": "multiplet_analysis",
                        "params": {
                            "normalize": {
                                "units": [3],
                                "position": [1.009],
                                "value": 3.0
                            }
                        }
                    }
                ]

            The actions are applied in the order they are provided.

            .. note::
                It is recommended to use the `rules` argument to pass the corresponding processing
                and analysis instead of specifying actions manually.

        :type actions: list[dict], optional

        :param rules: "on", "off", library name, or rule library file path. Defaults to "off".
            If you want to apply specific processing and analysis, use the rules feature instead of actions.
        :type rules: str, optional

        :return: The created JASON document.
        :rtype: document.Document

        **Example usage**:
        See :ref:`example_jason_usage`.
        """
        if isinstance(file_names, str):
            file_names = [file_names]

        # Safely create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jjh5", dir=config.temp_path, delete=False) as temp_file:
            saved_file_name = temp_file.name  # Get the secure temp file path

        actions_file_name = self._create_actions_file(actions)
        if actions_file_name:
            new_file_names = []
            for fname in file_names:
                new_file_names.append(fname)
                new_file_names.append(actions_file_name)
            file_names = new_file_names
        self._run(file_names + ['-s', saved_file_name] + ['--rules', rules])
        if actions_file_name:
            os.remove(actions_file_name)
        return document.Document(saved_file_name, is_temporary=True)

    def launch(self, args):
        """
        Launches the JASON GUI application with the provided arguments. For headless mode, use the :meth:`_run` method, or preferably, the :meth:`create_document` method.

        :param args: The arguments to pass to the JASON application.
        :type args: :obj:`list[str]`
        """
        if platform.system() == 'Windows':
            start = 'start "JASON"'
        else:
            start = 'open'
        os.system(start + ' ' + '"{}"'.format(os.path.join(self.app_dir, self.app_name)) + ' ' + ' '.join(['"{}"'.format(arg) if ' ' in arg else arg for arg in args]))

    def apply_actions(self, doc: document.Document, actions: list[dict]):
        """
        Applies the specified actions to a JASON document. This is useful for automating the processing and analysis of existing JASON `.jjh5` documents.

        :param doc: The JASON document to which the actions should be applied.
        :type doc: Document

        :param actions: The actions to apply. This argument is similar to the `actions` parameter in the :meth:`create_document` method.
            Refer to the :meth:`create_document` documentation for details on the structure and examples of actions.
        :type actions: :obj:`list[dict]`

        **Example usage**:

        .. code-block:: python

            from beautifuljason import JASON, Document

            # Initialize the JASON interface
            jason = JASON()

            # Open an existing JASON document
            with Document("example.jjh5") as doc:
                # Categorize NMR items by their dimensionality and nucleus type
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
                jason.apply_actions(doc, [
                    {'name': 'multiplet_analysis', 'items': items_1H},
                    {'name': 'peak_picking', 'items': items_13C + items_2D}
                ])
        """
        actions_file_name = self._create_actions_file(actions)        
        doc.close()
        self._run([doc.file_name, actions_file_name, '-s', doc.file_name])
        doc.load()
        if actions_file_name:
            os.remove(actions_file_name)

    def _create_actions_file(self, actions):
        """
        Creates a temporary actions file based on the provided actions.
        """
        actions_file_name = ''
        if actions:
            actions_file_name = tempfile.mktemp(suffix='.jja', dir=config.temp_path)
            with open(actions_file_name, 'w') as f:
                f.write(json.dumps(actions))
        return actions_file_name

    def save(self, doc: document.Document, file_names: list[str] | str, actions: list[dict]=[]):
        """
        Saves the JASON document to the specified file names after applying the given actions. The file format is determined by the file extension.
        
        The extensions supported are:

        - `.jjh5` (JASON HDF5 format) - recommended for JASON documents
        - `.jjj` (JASON JSON format)
        - `.jdx` (JCAMP-DX format)
        - `.pdf` (PDF format) - recommended for reports
        - `.jdf` (JEOL Delta Format)
        - `.png`, `.jpg`, `.jpeg`, `.tiff` (Raster image formats)
        - `.svg` (Scalable Vector Graphics)
        - `.mol` (Molfiles)
        - Check the "Save As" dialog in JASON for additional supported formats.

        :param doc: The JASON document to save.
        :type doc: Document

        :param file_names: List of file names or a single file name to save the document to. JASON will determine the format based on the file extension.
        :type file_names: :obj:`list[str]` | :obj:`str`

        :param actions: Actions to apply to the document before saving. Defaults to an empty list.
        :type actions: :obj:`list[dict]`, optional

        **Example usage**:
        See :ref:`example_jason_usage`.
        """
        if isinstance(file_names, str):
            file_names = [file_names]

        actions_file_name = self._create_actions_file(actions)

        save_args = []
        for file_name in file_names:
            save_args += ['-s', file_name]
        if isinstance(doc, document.Document):
            doc.close()
            args = [doc.file_name]
            if actions_file_name:
                args.append(actions_file_name)
            self._run(args + save_args)
            doc.load()
        else:
            if isinstance(doc, str):
                open_file_names = [doc]
            elif isinstance(doc, Sequence):
                open_file_names = list(doc)
            self._run(open_file_names + save_args)

        if actions_file_name:
            os.remove(actions_file_name)
