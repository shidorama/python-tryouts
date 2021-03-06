import os
import unittest

import pep8

ignore_patterns = ['.git', '.idea']


class TestPEP(unittest.TestCase):
    files = []

    def test_pep8(self):
        style = pep8.StyleGuide()
        style.options.max_line_length = 120
        python_files = []
        for root, _, files in os.walk('./'):
            if self.__ignore(root):
                continue
            python_files.extend([os.path.join(root, f) for f in files if f.endswith('.py')])
        result = style.check_files(python_files)
        self.assertEqual(result.total_errors, 0, 'PEP8 validation fails. Errors count: %s' % result.total_errors)

    def __ignore(self, dir):
        for pattern in ignore_patterns:
            if pattern in dir:
                return True
        return False
