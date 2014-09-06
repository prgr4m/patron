# -*- coding: utf-8 -*-
import os


class CodeInspector:
    "Imports a given module and inspects for code generation collisions"
    @staticmethod
    def inspect(module, attribute):
        if not os.path.exists(module):
            raise OSError('FileNotFoundError')  # FileNotFoundError in python3.4

__all__ = [CodeInspector]
