# coding=utf-8

import unittest

from hfcommon.template import render


class TestRender(unittest.TestCase):
    def test_render(self):

        self.assertEqual(render('', {}), '')
        self.assertEqual(render(u'Привет, {{ world }}!', {'world': u'мир'}), u'Привет, мир!')
        self.assertEqual(render(u'Привет, {{ world }}!', {'World': u'мир'}), u'Привет, мир!')
        self.assertEqual(render(u'Привет, мир!', {'world': u'world'}), u'Привет, мир!')
        self.assertEqual(render(u'Привет, мир!', {'hello': u'world'}), u'Привет, мир!')
        self.assertEqual(render(u'Привет, {{ unknown_var }}!', {'hello': u'world'}), u'Привет, {{ unknown_var }}!')
        self.assertEqual(render(u'Привет, мир!', {}), u'Привет, мир!')
