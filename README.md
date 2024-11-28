# Country-Capitals
Get the name of a country's capital city. That's it.

## Installation
```
pip install country_capitals
```

## Usage
```python
from country_capitals import get_capital

get_capital("Germany")
get_capital("Germ", fuzzy=True)
get_capital("DEU")
get_capital("DE")
get_capital("276")
```

The following identifiers are supported:
- Country name (common, official, etc.)
- ISO 3166-1 numeric-3 codes
- ISO 3166-1 alpha-2 codes
- ISO 3166-1 alpha-3 codes
- `pycountry` country objects

Including `fuzzy=True` will try to use use a fuzzy matching algorithm to find the country name.

## Development
Run the tests:
```
python -m unittest
```

Build the package:
```
python -m build
```
