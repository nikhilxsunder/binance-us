# binance-us 
## A simple package for connecting to the Binance US API.
## This package is still in beta please try it out and please report any comments, concerns, and issues.

[![Build and test GitHub](https://github.com/nikhilxsunder/binance_us/actions/workflows/main.yml/badge.svg)](https://github.com/nikhilxsunder/binance_us/actions)
[![PyPI version](https://img.shields.io/pypi/v/binance_us.svg)](https://pypi.org/project/binance_us/)
[![Downloads](https://img.shields.io/pypi/dm/binance_us.svg)](https://pypi.org/project/binance_us/)

### Latest Update

- Added Custodial class and methods.
- Updated README.md example

### Installation

You can install the package using pip:

```sh
pip install binance-us
```

### Rest API Usage

I recommend consulting the offical Binance US API documentation at: 
https://docs.binance.us/

Here is a simple example of how to use the package:

```python
# Imports
from binance_us import BinanceRestAPI
from binance_us import BinanceCustodialRestAPI

api_key = 'your_api_key'
api_secret = 'your_api_secret'

# REST API
client = BinanceRestAPI(api_key, api_secret)

# Custodial API
custodial = BinanceCustodialRestAPI(api_key, secret_key)

# Get exchange information
exchange_info = client.get_exchange_information()
print(exchange_info)

# Get recent trades
recent_trades = client.get_recent_trades(symbol='BTCUSD')
print(recent_trades)

# Get custodial account information
account_balance = custodial.get_account_balance(rail='CUSTODIAL_PARTNER')
print(custodial_info)
```

### Important Notes

- Currently all all responses are either JSON or f-strings.
- Store your API keys and secrets in environment variables or secure storage solutions.
- Do not hardcode your API keys and secrets in your scripts.
- Ambiguous method names will be subclassed into their respective categories in a coming update.

### Features

- Get exchange information
- Get market data
- Interact with most Binance US API endpoints (More endpoints coming soon)
- Post trades and orders
- etc.

## Next Update 

- Binance Rest API Custodial subclass

### Planned Updates

- Binance Websocket API class
- Binance Websocket Streams class
- Output data to pandas or polars

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
