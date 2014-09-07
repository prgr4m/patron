# -*- coding: utf-8 -*-
import unittest
from tempfile import NamedTemporaryFile
import textwrap
import os.path as path
from stencil.generators import CodeInspector as Ci


#class TestCodeInspector(unittest.TestCase):
#    def setUp(self):
#        self.temp_file = NamedTemporaryFile(mode='w+t', suffix='.py')
#        self.temp_file.file.write(textwrap.dedent("""\\
#        # -*- coding: utf-8 -*-
#        from __future__ import print
#
#        def add(a, b):
#            return a + b
#
#        def sub(a, b):
#            return a - b
#
#        def mult(a, b):
#            return a * b
#
#        if __name__ == '__main__':
#            print(add(1,2))
#            print(sub(2,3))
#            print(mult(3,4))
#        """))
#
#    def tearDown(self):
#        self.temp_file.close()
#
#    def test_source_code_has_collision(self):
#        self.assertEqual(Ci.has_collision(self.temp_file.name, 'sub'), True,
#                         "sub exists... there's something wrong with python")
#
#    def test_source_code_no_collision(self):
#        self.assertFalse(Ci.has_collision(self.temp_file.name, 'div'))
