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

import unittest
import uuid
from beautifuljason.utils import (create_uuid, group_to_list, ensure_str, InvalidUUIDError,
                   check_uuid_str, nuclide_str)

class TestUtils(unittest.TestCase):
    
    def test_create_uuid(self):
        result = create_uuid()
        self.assertTrue(result.startswith('{'))
        self.assertTrue(result.endswith('}'))
        uuid.UUID(result[1:-1])  # This will raise an error if not a valid UUID

    def test_group_to_list(self):
        class MockGroup:
            def __init__(self, items):
                self.items_dict = items

            def items(self):
                return self.items_dict.items()

            def __contains__(self, key):
                return key in self.items_dict

        group = MockGroup({'1': 'A', '2': 'B', 'not_a_number': 'C'})
        self.assertEqual(group_to_list(group, ''), ['A', 'B'])

    def test_ensure_str(self):
        self.assertEqual(ensure_str('hello'), 'hello')
        self.assertEqual(ensure_str(b'hello'), 'hello')

    def test_check_uuid_str(self):
        valid_uuid = '{' + str(uuid.uuid4()) + '}'
        self.assertEqual(check_uuid_str(valid_uuid), valid_uuid)
        with self.assertRaises(InvalidUUIDError):
            check_uuid_str("not_a_valid_uuid")

    def test_nuclide_str(self):
        self.assertEqual(nuclide_str(13, 'C'), '13C')
        self.assertEqual(nuclide_str(None, 'C'), '')
        self.assertEqual(nuclide_str(13, None), '')

if __name__ == '__main__':
    unittest.main()
