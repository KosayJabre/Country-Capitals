# Country-Capitals
[![PyPI Downloads](https://static.pepy.tech/badge/country-capitals)](https://pepy.tech/projects/country-capitals)
Get the name of a country's capital city. That's pretty much it.

## Installation
```
pip install country_capitals
```

## Usage
It's pretty simple. Including `fuzzy=True` will try to use use a fuzzy matching algorithm to find the country name.
```python
from country_capitals import get_capital

get_capital("Germany")
get_capital("Germ", fuzzy=True)
get_capital("DEU")
get_capital("DE")
get_capital("276")
```

For ISO 3166-1 codes specifically, you can use `get_capital_by_iso_code` or any of the more specific functions:
```python
from country_capitals import get_capital_by_iso_code, get_capital_by_numeric, get_capital_by_alpha2, get_capital_by_alpha3

get_capital_by_iso_code("DE")
get_capital_by_iso_code("DEU")
get_capital_by_iso_code("276")
# or
get_capital_by_alpha2("DE")
get_capital_by_alpha3("DEU")
get_capital_by_numeric("276")
```



## Development
Run the tests:
```
python -m unittest
```

Build the package:
```
python -m build
```
