import json
from typing import Any
from functools import lru_cache
import importlib.resources

import pycountry


class CountryNotFoundError(ValueError):
    pass


class CapitalNotFoundError(ValueError):
    pass


def load_capitals():
    with importlib.resources.open_text(__package__, "capitals.json", encoding="utf-8") as f:
        return json.load(f)


capitals = load_capitals()


@lru_cache(maxsize=None)
def get_capital(query: Any, fuzzy: bool = False) -> str:
    FUNCTIONS = [get_capital_by_iso_code, get_capital_by_name, get_capital_by_pycountry_country]
    if fuzzy:
        FUNCTIONS.append(get_capital_by_fuzzy_name)

    for func in FUNCTIONS:
        try:
            return func(query)
        except ValueError:
            pass

    raise ValueError(f"Could not find a capital for {query}.")


def get_capital_by_pycountry_country(country: pycountry.db.Country) -> str:
    if country.alpha_3 not in capitals:
        raise ValueError(f"Could not find a capital for country with alpha_3 ISO code {country.alpha_3}.")

    return capitals[country.alpha_3]


def get_capital_by_iso_code(iso_code: str) -> str:
    if iso_code.isdigit():
        return get_capital_by_numeric(iso_code)
    elif len(iso_code) == 2:
        return get_capital_by_alpha2(iso_code)
    elif len(iso_code) == 3:
        return get_capital_by_alpha3(iso_code)
    else:
        raise ValueError(f"Invalid ISO code {iso_code}.")


def get_capital_by_alpha3(alpha3: str) -> str:
    if len(alpha3) != 3:
        raise ValueError(f"Invalid ISO code {alpha3}, must be 3 characters long.")

    country = pycountry.countries.get(alpha_3=alpha3)

    if country is None:
        raise CountryNotFoundError(f"Could not find country with alpha_3 ISO code {alpha3}.")

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with alpha_3 ISO code {alpha3}.")

    return capitals[country.alpha_3]


def get_capital_by_alpha2(alpha2: str) -> str:
    if len(alpha2) != 2:
        raise ValueError(f"Invalid ISO code {alpha2}, must be 2 characters long.")

    country = pycountry.countries.get(alpha_2=alpha2)

    if country is None:
        raise CountryNotFoundError(f"Could not find country with alpha_2 ISO code {alpha2}.")

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with alpha_2 ISO code {alpha2}.")

    return capitals[country.alpha_3]


def get_capital_by_numeric(numeric: str) -> str:
    if not numeric.isdigit():
        raise ValueError(f"Invalid numeric ISO code {numeric}, must contain only digits.")

    numeric = numeric.zfill(3)
    country = pycountry.countries.get(numeric=numeric)

    if country is None:
        raise CountryNotFoundError(f"Could not find country with numeric ISO code {numeric}.")

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with numeric ISO code {numeric}.")

    return capitals[country.alpha_3]


def get_capital_by_name(country_name: str) -> str:
    country_from_name = pycountry.countries.get(name=country_name)
    country_from_common_name = pycountry.countries.get(common_name=country_name)
    country_from_official_name = pycountry.countries.get(official_name=country_name)

    if not any([country_from_name, country_from_common_name, country_from_official_name]):
        raise CountryNotFoundError(f"Could not find a country with name {country_name}.")

    country = country_from_name or country_from_common_name or country_from_official_name

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with name {country_name}.")

    return capitals[country.alpha_3]


def get_capital_by_fuzzy_name(country_name: str) -> str:
    country = pycountry.countries.search_fuzzy(country_name)

    if len(country) == 0:
        raise CountryNotFoundError(f"Could not find a country with name {country_name}.")

    if country[0].alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with name {country_name}.")

    return capitals[country[0].alpha_3]
