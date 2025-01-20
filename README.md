# binance_us 
## A simple package for connecting to the Binance US API.
## This package is still in beta please try it out and please report any comments, concerns, and issues.

[![Build and test GitHub](https://github.com/nikhilxsunder/binance_us/actions/workflows/main.yml/badge.svg)](https://github.com/nikhilxsunder/binance_us/actions)
[![PyPI version](https://img.shields.io/pypi/v/binance_us.svg)](https://pypi.org/project/binance_us/)
[![Downloads](https://img.shields.io/pypi/dm/binance_us.svg)](https://pypi.org/project/binance_us/)

### Installation

You can install the package using pip:

```sh
pip install binance_us
```

### Rest API Usage

I recommend consulting the offical Binance US API documentation at: 
https://docs.binance.us/

Here is a simple example of how to use the package:

```python
from binance_us import BinanceRestAPI

api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = BinanceRestAPI(api_key, api_secret)

# Get exchange information
exchange_info = client.get_exchange_information()
print(exchange_info)

# Get recent trades
recent_trades = client.get_recent_trades(symbol='BTCUSD')
print(recent_trades)
```

### Important Notes

- Currently all all responses are eitther JSON or f-strings.
- Store your API keys and secrets in environment variables or secure storage solutions.
- Do not hardcode your API keys and secrets in your scripts.
- Some functions currently do not have docstrings, they will be added soon.

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
