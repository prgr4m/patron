#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path as path
import sys
import unittest

current_location = path.dirname(path.abspath(__file__))
lib_dir = path.join(path.abspath(path.join(current_location, os.pardir)), 'lib')
sys.path.insert(0, lib_dir)

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('generators')
    unittest.TextTestRunner(verbosity=2).run(tests)
