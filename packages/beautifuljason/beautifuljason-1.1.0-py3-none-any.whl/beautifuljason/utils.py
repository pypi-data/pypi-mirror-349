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

# """
# .. module:: utils
   # :synopsis: Utility functions and classes for various tasks.

# This module offers utilities for:

# - UUID management.
# - Group-to-list conversions.
# - String type assurances and decoding.
# - Nuclide string construction.
# """

import uuid

def create_uuid() -> str:
    """
    Generates a UUID string in a specific format.

    :return: A UUID string enclosed in curly braces.
    :rtype: :obj:`str`
    """
    return '{{{}}}'.format(uuid.uuid4())

def group_to_list(group, path):
    """
    Converts a group to a sorted list based on numeric keys.

    :param group: The group object to be converted.
    :type group: :obj:`h5py.Group`
    :param path: The path within the group to be converted.
    :type path: :obj:`str`
    :return: A list of values sorted by their numeric keys.
    :rtype: :obj:`list`
    """
    if path:
        if path in group:
            group = group[path]
        else:
            return []
    
    list_dict = {int(key): value for key, value in group.items() if key.isnumeric()}
    return [value for _, value in sorted(list_dict.items())]

def ensure_str(str_: str | bytes) -> str:
    """
    Ensures the input is a string, decoding if it's bytes.

    :param str_: The input string or bytes.
    :type str_: :obj:`str` | :obj:`bytes`
    :return: The decoded string if input was bytes, or the original string.
    :rtype: :obj:`str`
    """
    if isinstance(str_, bytes):
        return str_.decode('utf8')
    return str_

class InvalidUUIDError(ValueError):
    """
    Exception raised for invalid UUID strings.
    """
    pass

def check_uuid_str(uuid_str) -> str:
    """
    Validates a UUID string.

    :param uuid_str: The UUID string to validate.
    :type uuid_str: :obj:`str`
    :return: The validated UUID string.
    :rtype: :obj:`str`
    :raises InvalidUUIDError: If the provided string is not a valid UUID.
    """
    if isinstance(uuid_str, bytes):
        uuid_str = uuid_str.decode('ascii')
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        raise InvalidUUIDError(f"{uuid_str} is not a valid UUID")
    return uuid_str

def nuclide_str(isotope, name) -> str:
    """
    Constructs a nuclide string from isotope and  name.

    :param isotope: The isotope number.
    :param name: The name of the nuclide.
    :type name: :obj:`str`
    :return: A string representation of the nuclide, or an empty string if either argument is missing.
    :rtype: :obj:`str`
    """
    if isotope and name:
        return f'{isotope}{name}'
    return ''