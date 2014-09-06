# -*- coding: utf-8 -*-
import os
import os.path as path
import unittest
from stencil.generators import is_name_valid, get_templates_dir


class TestUtilityFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_name_valid(self):
        self.assertEqual(is_name_valid('N*/G0*'), False,
                         "N*/G0* should not pass!")

    def test_get_templates_dir(self):
        expected_loc = path.dirname(path.join(path.abspath(__file__),
                                              os.pardir))
        self.assertEqual(expected_loc, get_templates_dir(),
                          "They should be the same location but are not")
