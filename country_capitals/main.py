"""
Retrieve the capital city of a country identified through various identifiers such as ISO codes or names.
"""

import json
from typing import Union
import importlib.resources

import pycountry


with importlib.resources.open_text(__package__, "capitals.json", encoding="utf-8") as f:
    capitals = json.load(f)


class CountryNotFoundError(ValueError):
    """Exception raised when a country cannot be found."""

    pass


class CapitalNotFoundError(ValueError):
    """Exception raised when a capital city cannot be found for a country."""

    pass


def get_capital(query: Union[str, pycountry.db.Country], fuzzy: bool = False) -> str:
    """Get the capital city of a country given a multi-type query.

    Args:
        query (Union[str, pycountry.db.Country]): Can be a name, ISO code, or pycountry Country object.
        fuzzy (bool, optional): If True, perform a fuzzy search for the country name. Defaults to False.

    Returns:
        str: The capital city of the country.

    Raises:
        CapitalNotFoundError: If the capital cannot be found.
    """
    FUNCTIONS = [get_capital_by_iso_code, get_capital_by_name, get_capital_by_pycountry_country]
    if fuzzy:
        FUNCTIONS.append(get_capital_by_fuzzy_name)

    for func in FUNCTIONS:
        try:
            return func(query)
        except:
            pass

    raise CapitalNotFoundError(f"Could not find a capital for {query}.")


def get_capital_by_iso_code(iso_code: str) -> str:
    """Get the capital city of a country given its ISO code.

    Args:
        iso_code (str): The ISO code of the country (numeric, alpha-2, or alpha-3).

    Returns:
        str: The capital city of the country.

    Raises:
        ValueError: If the ISO code is invalid.
    """
    if iso_code.isdigit():
        return get_capital_by_numeric(iso_code)
    elif len(iso_code) == 2:
        return get_capital_by_alpha2(iso_code)
    elif len(iso_code) == 3:
        return get_capital_by_alpha3(iso_code)
    else:
        raise ValueError(f"Invalid ISO code {iso_code}.")


def get_capital_by_name(country_name: str) -> str:
    """Get the capital city of a country given its name.

    Args:
        country_name (str): The official, common, or official name of the country.

    Returns:
        str: The capital city of the country.

    Raises:
        CountryNotFoundError: If the country cannot be found.
        CapitalNotFoundError: If the capital cannot be found for the country.
    """
    country_from_name = pycountry.countries.get(name=country_name)
    country_from_common_name = pycountry.countries.get(common_name=country_name)
    country_from_official_name = pycountry.countries.get(official_name=country_name)

    if not any([country_from_name, country_from_common_name, country_from_official_name]):
        raise CountryNotFoundError(f"Could not find a country with name {country_name}.")

    country = country_from_name or country_from_common_name or country_from_official_name

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with name {country_name}.")

    return capitals[country.alpha_3]


def get_capital_by_pycountry_country(country: pycountry.db.Country) -> str:
    """Get the capital city of a country given a pycountry Country object.

    Args:
        country (pycountry.db.Country): The pycountry Country object.

    Returns:
        str: The capital city of the country.

    Raises:
        ValueError: If the capital cannot be found for the country.
    """
    if country.alpha_3 not in capitals:
        raise ValueError(f"Could not find a capital for country with alpha_3 ISO code {country.alpha_3}.")

    return capitals[country.alpha_3]


def get_capital_by_fuzzy_name(country_name: str) -> str:
    """Get the capital city of a country given a country name using fuzzy search.

    Args:
        country_name (str): The approximate name of the country.

    Returns:
        str: The capital city of the country.

    Raises:
        CountryNotFoundError: If the country cannot be found.
        CapitalNotFoundError: If the capital cannot be found for the country.
    """
    try:
        country = pycountry.countries.search_fuzzy(country_name)
    except LookupError:
        raise CountryNotFoundError(f"Could not find a country with name {country_name}.")

    if len(country) == 0:
        raise CountryNotFoundError(f"Could not find a country with name {country_name}.")

    if country[0].alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with name {country_name}.")

    return capitals[country[0].alpha_3]


def get_capital_by_numeric(numeric: str) -> str:
    """Get the capital city of a country given its numeric ISO code.

    Args:
        numeric (str): The numeric ISO code of the country.

    Returns:
        str: The capital city of the country.

    Raises:
        ValueError: If the numeric code is invalid.
        CountryNotFoundError: If the country cannot be found.
        CapitalNotFoundError: If the capital cannot be found for the country.
    """
    if not numeric.isdigit():
        raise ValueError(f"Invalid numeric ISO code {numeric}, must contain only digits.")

    numeric = numeric.zfill(3)
    country = pycountry.countries.get(numeric=numeric)

    if country is None:
        raise CountryNotFoundError(f"Could not find country with numeric ISO code {numeric}.")

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with numeric ISO code {numeric}.")

    return capitals[country.alpha_3]


def get_capital_by_alpha2(alpha2: str) -> str:
    """Get the capital city of a country given its alpha-2 ISO code.

    Args:
        alpha2 (str): The alpha-2 ISO code of the country.

    Returns:
        str: The capital city of the country.

    Raises:
        ValueError: If the alpha-2 code is invalid.
        CountryNotFoundError: If the country cannot be found.
        CapitalNotFoundError: If the capital cannot be found for the country.
    """
    if len(alpha2) != 2:
        raise ValueError(f"Invalid ISO code {alpha2}, must be 2 characters long.")

    country = pycountry.countries.get(alpha_2=alpha2)

    if country is None:
        raise CountryNotFoundError(f"Could not find country with alpha_2 ISO code {alpha2}.")

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with alpha_2 ISO code {alpha2}.")

    return capitals[country.alpha_3]


def get_capital_by_alpha3(alpha3: str) -> str:
    """Get the capital city of a country given its alpha-3 ISO code.

    Args:
        alpha3 (str): The alpha-3 ISO code of the country.

    Returns:
        str: The capital city of the country.

    Raises:
        ValueError: If the alpha-3 code is invalid.
        CountryNotFoundError: If the country cannot be found.
        CapitalNotFoundError: If the capital cannot be found for the country.
    """
    if len(alpha3) != 3:
        raise ValueError(f"Invalid ISO code {alpha3}, must be 3 characters long.")

    country = pycountry.countries.get(alpha_3=alpha3)

    if country is None:
        raise CountryNotFoundError(f"Could not find country with alpha_3 ISO code {alpha3}.")

    if country.alpha_3 not in capitals:
        raise CapitalNotFoundError(f"Could not find a capital for country with alpha_3 ISO code {alpha3}.")

    return capitals[country.alpha_3]
