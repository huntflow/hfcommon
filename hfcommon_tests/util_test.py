# coding=utf-8

import unittest

from hfcommon.util import try_int, host_included


class TestUtil(unittest.TestCase):
    def test_try_int(self):

        self.assertEqual(try_int('1'), 1)
        self.assertEqual(try_int('123'), 123)
        self.assertEqual(try_int(' '), None)
        self.assertEqual(try_int(''), None)
        self.assertEqual(try_int(u'цифра'), None)
        self.assertEqual(try_int('number'), None)
        self.assertEqual(try_int(123), 123)

    def test_host_included(self):
        self.assertEqual(host_included('https://ya.ru', ['ya.ru']), True)
        self.assertEqual(host_included('http://127.0.0.1:8400/docs', ['127.0.0.1']), True)
        self.assertEqual(host_included('https://yandex.ru', ['ya.ru']), False)
        self.assertEqual(host_included('https://ya.ru:80', ['127.0.0.1', 'ya.ru']), True)
        self.assertEqual(host_included('https://', ['ya.ru']), False)
