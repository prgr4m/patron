#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
from os import path
import sys
import unittest

current_location = path.dirname(path.abspath(__file__))
lib_dir = path.join(path.abspath(path.join(current_location, os.pardir)),
                    'patron')
sys.path.insert(0, lib_dir)

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('generators')
    unittest.TextTestRunner(verbosity=2).run(tests)
