#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

import phonenumbers

from hfcommon.format import phone


expected = u'+7 981 704-10-02'


class PhoneTest(unittest.TestCase):
    def test_hh_dict(self):
        result = phone({
            'country': '7',
            'city': '981',
            'number': '7041002'
        })
        self.assertEqual(result, expected)

    def test_no_country_code_phone(self):
        result = phone('9817041002')
        self.assertEqual(result, expected)

    def test_hh_formatted(self):
        result = phone({
            'formatted': '+79817041002'
        })
        self.assertEqual(result, expected)

    def test_string(self):
        result = phone('89817041002')
        self.assertEqual(result, expected)

    def test_plus_string(self):
        result = phone('+79817041002')
        self.assertEqual(result, expected)

    def test_hyphen_string(self):
        result = phone('8981704-10-02')
        self.assertEqual(result, expected)

    def test_plus_hyphen_string(self):
        result = phone('+7981704-10-02')
        self.assertEqual(result, expected)

    def test_bracket_string(self):
        result = phone('8(981)7041002')
        self.assertEqual(result, expected)

    def test_plus_bracket_string(self):
        result = phone('+7(981)7041002')
        self.assertEqual(result, expected)

    def test_bracket_hyphen_string(self):
        result = phone('8(981)704-10-02')
        self.assertEqual(result, expected)

    def test_plus_bracket_hyphen_string(self):
        result = phone('8(981)704-10-02')
        self.assertEqual(result, expected)

    def test_broken_string(self):
        broken_string = '8AAA7041002'
        result = phone(broken_string)
        self.assertEqual(result, broken_string)


if __name__ == '__main__':
    unittest.main()
