#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, with_statement

import unittest
from unittest import TextTestRunner, TestSuite


TEST_MODULES = [
    'hfcommon_tests.pycodestyle_test',
    'hfcommon_tests.util_test',
    'hfcommon_tests.template_test',
    'hfcommon_tests.format_test',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


if __name__ == '__main__':
    suite = TestSuite((
        all()
    ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)
