# Binance US: A simple package for connecting to the Binance US API.
## Still in beta missing items will be added soon.

[![Build and test GitHub](https://github.com/nikhilxsunder/binance_us/actions/workflows/main.yml/badge.svg)](https://github.com/nikhilxsunder/binance_us/actions)
[![PyPI version](https://img.shields.io/pypi/v/binance_us.svg)](https://pypi.org/project/binance_us/)
[![Downloads](https://img.shields.io/pypi/dm/binance_us.svg)](https://pypi.org/project/binance_us/)

### Installation

You can install the package using pip:

```sh
pip install binance_us
```

### Usage

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

### Features

- Get exchange information
- Get recent trades
- Get historical trades
- Get aggregate trades
- Get order book depth
- Get candlestick data
- Get live ticker price
- Get average price
- Get best order book price
- Get 24h price change statistics
- Get rolling window price change statistics
- Get user account information
- Get user account status
- Get user API trading status
- Get asset distribution history
- Get trade fee
- Get past 30d trade volume
- Get sub-account information
- Get sub-account transfer history
- Execute sub-account transfer
- Get sub-account assets
- Get master accounts total USD value
- Get sub-account status
- Get order rate limits
- Create new order
- Test new order
- Get order
- Get all open orders
- Cancel order
- Cancel open orders for symbol
- Get trades
- Replace order
- Query prevented matches

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

### License

This project is licensed under the GNU Affero General Public License v3.0 - see the 

LICENSE

 file for details.
```
