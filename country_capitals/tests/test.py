import unittest
from country_capitals import (
    get_capital,
    get_capital_by_iso_code,
    get_capital_by_name,
    get_capital_by_pycountry_country,
    get_capital_by_fuzzy_name,
    get_capital_by_numeric,
    get_capital_by_alpha2,
    get_capital_by_alpha3,
    CountryNotFoundError,
)
import pycountry

class TestCountryCapitals(unittest.TestCase):

    def test_get_capital_by_iso_code(self):
        self.assertEqual(get_capital_by_iso_code('US'), 'Washington, D.C.')
        self.assertEqual(get_capital_by_iso_code('USA'), 'Washington, D.C.')
        self.assertEqual(get_capital_by_iso_code('840'), 'Washington, D.C.')
        with self.assertRaises(ValueError):
            get_capital_by_iso_code('INVALID')

    def test_get_capital_by_name(self):
        self.assertEqual(get_capital_by_name('United States'), 'Washington, D.C.')
        with self.assertRaises(CountryNotFoundError):
            get_capital_by_name('Invalid Country')

    def test_get_capital_by_pycountry_country(self):
        country = pycountry.countries.get(alpha_3='USA')
        self.assertEqual(get_capital_by_pycountry_country(country), 'Washington, D.C.')

    def test_get_capital_by_fuzzy_name(self):
        self.assertEqual(get_capital_by_fuzzy_name('United States'), 'Washington, D.C.')
        with self.assertRaises(CountryNotFoundError):
            get_capital_by_fuzzy_name('Invalid Country')

    def test_get_capital_by_numeric(self):
        self.assertEqual(get_capital_by_numeric('840'), 'Washington, D.C.')
        with self.assertRaises(CountryNotFoundError):
            get_capital_by_numeric('999')

    def test_get_capital_by_alpha2(self):
        self.assertEqual(get_capital_by_alpha2('US'), 'Washington, D.C.')
        with self.assertRaises(CountryNotFoundError):
            get_capital_by_alpha2('ZZ')

    def test_get_capital_by_alpha3(self):
        self.assertEqual(get_capital_by_alpha3('USA'), 'Washington, D.C.')
        with self.assertRaises(CountryNotFoundError):
            get_capital_by_alpha3('ZZZ')

    def test_get_capital(self):
        self.assertEqual(get_capital('US'), 'Washington, D.C.')
        self.assertEqual(get_capital('United States'), 'Washington, D.C.')
        self.assertEqual(get_capital(pycountry.countries.get(alpha_3='USA')), 'Washington, D.C.')
        with self.assertRaises(ValueError):
            get_capital('Invalid Country')

if __name__ == '__main__':
    unittest.main()