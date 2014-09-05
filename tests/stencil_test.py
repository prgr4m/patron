#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('generators')
    unittest.TextTestRunner(verbosity=2).run(tests)
