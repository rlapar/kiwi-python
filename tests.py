#!/usr/bin/python3

import unittest
from click.testing import CliRunner
from book_flight import main

DEFAULT_DATE = '2018-04-13'
DEFAULT_IATA = 'DUB'
INVALID_IATA = 'QQQ'

class Test(unittest.TestCase):
    def setUp(self):
        self._runner = CliRunner()

    def testInvalidDate(self):
        result = self._runner.invoke(main, ['--no-warn', '--date', '0', '--from', DEFAULT_IATA, '--to', DEFAULT_IATA])
        self.assertEqual(result.output.strip(), '0', 'Ivalid date should return 0 code.')

    def testInvalidIATAFormat(self):
        result = self._runner.invoke(main, ['--no-warn', '--date', DEFAULT_DATE, '--from', 'x23', '--to', DEFAULT_IATA])
        self.assertEqual(result.output.strip(), '0', 'Ivalid IATA format should return 0 code.')

    def testNonExistantIATACode(self):
        result = self._runner.invoke(main, ['--no-warn', '--date', DEFAULT_DATE, '--from', INVALID_IATA, '--to', DEFAULT_IATA])
        self.assertEqual(result.output.strip(), '0', 'Non Existant IATA format should return 0 code.')
    
    def testAmbiguousOnewayReturn(self):
        result = self._runner.invoke(main, ['--no-warn', '--date', DEFAULT_DATE, '--from', DEFAULT_IATA, '--to', DEFAULT_IATA, '--cheapest', '--fastest'])
        self.assertEqual(result.output.strip(), '0', 'Ambiguous options --cheapest/--fastest should return 0 code.')

    def testAmbiguousCheapestFastest(self):
        result = self._runner.invoke(main, ['--no-warn', '--date', DEFAULT_DATE, '--from', DEFAULT_IATA, '--to', DEFAULT_IATA, '--one-way', '--return', '3'])
        self.assertEqual(result.output.strip(), '0', 'Ambiguous options --one-way/--return should return 0 code.')

    def testSuccessfulBooking(self):
        result = self._runner.invoke(main, ['--no-warn', '--date', DEFAULT_DATE, '--from', 'BCN', '--to', 'DUB', '--one-way'])
        self.assertNotEqual(result.output.strip(), '0', 'Successful booking should not return 0 code.')

if __name__ == '__main__':
    unittest.main()