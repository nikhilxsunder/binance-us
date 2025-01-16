"""Binance US"""
#Imports
import urllib.parse
import hashlib
import hmac
import time
import requests

class BinanceRestAPI:
    """The BinanceRestAPI class contain methods for interacting with the Binance US REST API v3."""
    # Dunder Methods
    def __init__(self, api_key, secret_key):
        """
        Initialize the BinanceRestAPI class that provides functions which query 
        Binance US market data. an API key is not needed for market data requests but 
        is required for account related requests.

        Parameters
        ----------
        api_key : str
            API key. A free API key can be obtained on the Binance US website at 
            https://www.binance.us/.
        secret_key : str
            String containing API secret key.            
        """
        self.base_url = 'https://api.binance.us'
        self.api_key = api_key
        self.secret_key = secret_key
    # Private Methods
    def __get_binanceus_signature(self, data):
        postdata = urllib.parse.urlencode(data)
        message = postdata.encode()
        byte_key = bytes(self.secret_key, 'UTF-8')
        mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return mac
    def __binanceus_get_request(self, url_endpoint, data):
        if not self.api_key or not self.secret_key:
            raise ValueError("'api_key' and 'secret_key' are required for this function")
        headers = {}
        headers['X-MBX-APIKEY'] = self.api_key
        signature = self.__get_binanceus_signature(data)
        params={
            **data,
            "signature": signature,
            }
        req = requests.get((self.base_url + url_endpoint), params=params, headers=headers,
                           timeout=10)
        return req.text
    def __binanceus_post_request(self, url_endpoint, data):
        if not self.api_key or not self.secret_key:
            raise ValueError("'api_key' and 'secret_key' are required for this function")
        headers = {}
        headers['X-MBX-APIKEY'] = self.api_key
        signature = self.__get_binanceus_signature(data)
        payload={
            **data,
            "signature": signature,
            }
        req = requests.get((self.base_url + url_endpoint), params=payload, headers=headers,
                           timeout=10)
        return req.text
    def __binanceus_delete_request(self, url_endpoint, data):
        if not self.api_key or not self.secret_key:
            raise ValueError("'api_key' and 'secret_key' are required for this function")
        headers = {}
        headers['X-MBX-APIKEY'] = self.api_key
        signature = self.__get_binanceus_signature(data)
        params={
            **data,
            "signature": signature,
            }
        req = requests.delete((self.base_url + url_endpoint), params=params, headers=headers,
                            timeout=10)
        return req.text
    # Public Methods
    ## General Data Endpoints
    ### System Information
    def test_connectivity(self):
        """
        Use this endpoint to test connectivity to the exchange.
        """
        url_endpoint = '/api/v3/ping'
        resp = requests.get(self.base_url + url_endpoint, timeout=10)
        return resp
    def get_server_time(self):
        """
        Use this endpoint to get the exchange's server time.
        """
        url_endpoint = '/api/v3/time'
        resp = requests.get(self.base_url + url_endpoint, timeout=10)
        return resp.json()
    def get_system_status(self, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to fetch whether the system status is normal or under maintenance.

        Notes
        ----------
        For response, 0: normal, 1: system maintenance.

        Parameters
        ----------
        timestamp : long
            Timestamp for request.            
        """
        url_endpoint = "/sapi/v1/system/status"
        data = {
            "timestamp": timestamp,
        }
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ### Exchange Information
    def get_exchange_information(self, symbol=None, symbols=None, permissions=None):
        """
        Use this endpoint to get the current exchange trading rules and trading pair 
        information.

        Notes 
        ----------
        If the value provided to symbol or symbols do not exist, the endpoint will throw an error 
        saying the symbol is invalid.
        All parameters are optional.
        If permissions parameter not provided, the default values will be ["SPOT"].

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        symbols : str
            String containing multiple ticker IDs.
        permissions : str
            Level of access the API key has to your account.
        """
        if symbol and symbols:
            raise ValueError("Only one of 'symbol' or 'symbols' can be specified.")
        url_endpoint = '/api/v3/exchangeInfo'
        params = {}
        if symbol:
            params['symbol'] = symbol
        if symbols:
            params['symbols'] = symbols
        if permissions:
            params['permissions'] = permissions
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    ## Market Data Endpoints
    ### Trade Data
    def get_recent_trades(self, symbol, limit=None):
        """
        Use this endpoint to get the recent trades. Please note the maximum limit 
        is 1,000 trades.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        limit : int
            Default 500; max 1000.
        """
        url_endpoint = '/api/v3/trades'
        params = {'symbol': symbol}
        if limit:
            params['limit'] = limit
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_historical_trades(self, symbol, limit=None, from_id=None):
        """
        Use this endpoint to get older trades. Please note the maximum limit is 1,000 trades.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        limit : int
            Default 500; Max 1000.
        from_id : long
            Trade is to fetch from. default gets most recent trades.
        """
        url_endpoint = '/api/v3/historicalTrades'
        params = {'symbol': symbol}
        if limit:
            params['limit'] = limit
        if from_id:
            params['fromId'] = from_id
        headers = {'X-MBX-APIKEY': self.api_key}
        resp = requests.get(self.base_url + url_endpoint,
                            params=params,
                            headers=headers,
                            timeout=10)
        return resp.json()
    def get_aggregate_trades(self, symbol, from_id=None, start_time=None, end_time=None,limit=None):
        """
        Use this endpoint to get compressed, aggregate trades. Trades that fill at the same time, 
        from the same order, with the same price, will have the quantity aggregated. 
        Please note the maximum limit is 1,000 trades.

        Notes
        ----------
        If fromId, startTime, and endTime are not sent, the most recent aggregate trades will 
        be returned.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        from_id : long
            Trade is to fetch from. default gets most recent trades.
        start_time : long
            Timestamp in ms to get aggregate trades from INCLUSIVE.
        end_time : long
            Timestamp in ms to get aggregate trades until INCLUSIVE.
        limit : int
            Default 500; Max 1000.
        """
        url_endpoint = '/api/v3/aggTrades'
        params = {'symbol': symbol}
        if from_id:
            params['fromId'] = from_id
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        if limit:
            params['limit'] = limit
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_orderbook_depth(self, symbol, limit=None):
        """
        Use this endpoint to get order book depth (prices and quantities of bids and asks).

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        limit : int
            Default 500; Max 1000.
        """
        url_endpoint = '/api/v3/depth'
        params = {'symbol': symbol}
        if limit:
            params['limit'] = limit
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_candlestick_data(self, symbol, interval, start_time=None, end_time=None):
        """
        Use this endpoint to get Kline/candlestick bars for a token symbol. Klines are uniquely 
        identified by their open time. Please note the maximum limit is 1,000 bars.

        Notes
        ----------
        If startTime and endTime are not sent, the most recent klines are returned.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        interval : enum
            interval : str
                The interval for the candlestick data.
        start_time : long
            Timestamp in ms to get aggregate trades from INCLUSIVE.
        end_time : long
            Timestamp in ms to get aggregate trades until INCLUSIVE.
        limit : int
            Default 500; Max 1000.
        """
        url_endpoint = '/api/v3/klines'
        params = {'symbol': symbol, 'interval': interval}
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    ### Price Data
    def get_live_ticker_price(self, symbol=None, symbols=None):
        """
        Use this endpoint to get the live ticker price.

        Notes
        ----------
        Parameter symbol and symbols cannot be used in combination. If neither parameter is sent, 
        prices for all symbols will be returned in an array.
        Exaples of accepted format for the symbols parameter: ["BTCUSDT", "BNBUSDT"] or 
        %5B%22BTCUSDT%22, %22BNBUSDT%22%5D

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        symbols : str
            String containing multiple ticker IDs.
        """
        if symbol and symbols:
            raise ValueError("Only one of 'symbol' or 'symbols' can be specified.")
        url_endpoint = '/api/v3/ticker/price'
        params = {}
        if symbol:
            params['symbol'] = symbol
        if symbols:
            params['symbols'] = symbols
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_average_price(self, symbol):
        """
        Use this endpoint to get the current average price for a symbol.
        
        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        """
        url_endpoint = '/api/v3/avgPrice'
        params = {'symbol': symbol}
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_best_order_book_price(self, symbol=None, symbols=None):
        """
        Use this endpoint to get the best available order book price.
        
        Notes
        ----------
        Parameter symbol and symbols cannot be used in combination. If neither parameter is sent, 
        prices for all symbols will be returned in an array.
        Exaples of accepted format for the symbols parameter: ["BTCUSDT", "BNBUSDT"] or 
        %5B%22BTCUSDT%22, %22BNBUSDT%22%5D

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from
        symbols : str
            String containing multiple ticker IDs.
        """
        if symbol and symbols:
            raise ValueError("Only one of 'symbol' or 'symbols' can be specified.")
        url_endpoint = '/api/v3/ticker/bookTicker'
        params = {}
        if symbol:
            params['symbol'] = symbol
        if symbols:
            params['symbols'] = symbols
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_24h_price_change_statistics(self, symbol=None, symbols=None, stat_type=None):
        """
        Use this endpoint to get price change data for the past 24hrs.
        
        Notes
        ----------
        Parameter symbol and symbols cannot be used in combination. If neither parameter is sent, 
        prices for all symbols will be returned in an array.
        Exaples of accepted format for the symbols parameter: ["BTCUSDT", "BNBUSDT"] or 
        %5B%22BTCUSDT%22, %22BNBUSDT%22%5D.
        If none provided,the default is FULL.
        Parameter stat_type=FULL is the default value and the response that is currently being 
        returned from the endpoint.
        Parameter stat_type=MINI omits the following fields from the response: priceChangePercent, 
        weightedAvgPrice, bidPrice, bidQty, askPrice, askQty, and lastQty

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        symbols : str
            String containing multiple ticker IDs.
        stat_type: enum
            Supported values: FULL or MINI. If none provided, the default is FULL.
        """
        if symbol and symbols:
            raise ValueError("Only one of 'symbol' or 'symbols' can be specified.")
        url_endpoint = '/api/v3/ticker/24hr'
        params = {}
        if symbol:
            params['symbol'] = symbol
        if symbols:
            params['symbols'] = symbols
        if stat_type:
            params['type'] = stat_type
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    def get_rolling_window_price_change_statistics(self, symbol=None, symbols=None,
                                                    window_size=None, stat_type=None):
        """
        Use this endpoint to get the price change data within a requested window of time.
        
        Notes
        ----------
        openTime reverts to the start of the minute (e.g. 09:17:00 UTC, instead of 09:17:47:99). 
        closeTime is the current time of the request (including seconds and milliseconds). 
        Therefore, the effective window can be up to 59999ms (59 seconds) longer than the specified 
        windowSize.
        E.g. If the closeTime is 1641287867099 (January 04, 2022 09:17:47:099 UTC), and the 
        windowSize is 1d. the openTime will be: 1641201420000 (January 3, 2022, 09:17:00 UTC).

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        symbols : str
            String containing multiple ticker IDs.
        window_size : enum
            Defaults to 1d if no parameter provided.
        stat_type: enum
            Supported values: FULL or MINI. If none provided,the default is FULL.        
        """
        if symbol and symbols:
            raise ValueError("Only one of 'symbol' or 'symbols' can be specified.")
        if not symbol or symbols:
            raise ValueError("One of 'symbol' or 'symbols' must be specified.")
        url_endpoint = '/api/v3/ticker'
        params = {}
        if symbol:
            params['symbol'] = symbol
        if symbols:
            params['symbols'] = symbols
        if window_size:
            params['windowSize'] = window_size
        if stat_type:
            params['type'] = stat_type
        resp = requests.get(self.base_url + url_endpoint, params=params, timeout=10)
        return resp.json()
    ## User Data Endpoints
    ### User Account Data
    def get_user_account_information(self, recv_window=None,
                                     timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get current account information.

        Parameters
        ----------
        recvWindow : long
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/api/v3/account"
        data = {
            'timestamp': timestamp
        }
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_user_account_status(self, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to fetch account status details.

        Parameters
        ----------
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v3/accountStatus"
        data = {
            'timestamp': timestamp
        }
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_user_api_trading_status(self, recv_window=None,
                                    timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to fetch account API trading status details.

        Parameters
        ----------
        recvWindow : long
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v3/accountStatus"
        data = {
            'timestamp': timestamp
        }
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_asset_distribution_history(self, asset=None, category=None, start_time=None,
                                        end_time=None, limit=None,
                                        timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to query asset distribution records, including 
        Market Maker Rebate, MM Streaks Rebate, API Partner Rebate and airdrop, etc.

        Parameters
        ----------
        asset : str
            Distribution asset.
        category : str 
            Distribution category (e.g., Market Maker Rebate, MM Streaks Rebate,
            API Partner Rebate, airdrop).
        start_time : long
            Distribution start time.
        end_time : long
            Distribution end time.
        limit : int
            Limit rows (default: 20, max: 500).
        timestamp : long
            Current timestamp.
        """
        url_endpoint = "/sapi/v1/asset/assetDistributionHistory"
        data = {
            'timestamp': timestamp
        }
        if asset:
            data['asset'] = asset
        if category:
            data['category'] = category
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if limit:
            data['limit'] = limit
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_trade_fee(self, symbol=None):
        """
        Use this endpoint to get your current maker & taker fee rates for spot trading based on your 
        VIP level or manual fee adjustment. Discount for using BNB to pay fees (25% off) is not 
        factored in.

        Parameters
        ----------
        symbol : str
            Symbol name.
        """
        url_endpoint = "/sapi/v1/asset/query/trading-fee"
        data = {
            'timestamp': int(round(time.time() * 1000))
        }
        if symbol:
            data['symbol'] = symbol
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_past_30d_trade_volume(self):
        """
        Use this endpoint to get total trade volume for the past 30 days, calculated on a rolling 
        basis every day at 0:00 AM (UTC).
        """
        url_endpoint = "/sapi/v1/asset/query/trading-volume"
        data = {
            "timestamp": int(round(time.time() * 1000))
        }
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ### Sub Account Data
    def get_sub_account_information(self, email=None, status=None, page=None, limit=None,
                                    recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get your sub-account list.

        Parameters
        ----------
        email : str
            Sub-account Email.
        status : str
            Sub-account status: enabled or disabled.
        page : int
            Default value: 1.
        limit : int
            Default value: 500.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v3/sub-account/list"
        data = {
            "timestamp": timestamp
        }
        if email:
            data['email'] = email
        if status:
            data['status'] = status
        if page:
            data['page'] = page
        if limit:
            data['limit'] = limit
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_sub_account_transfer_history(self, email=None, start_time=None, end_time=None,
                                         page=None, limit=None,
                                         timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get your sub-account list.

        Parameters
        ----------
        email : str
            Sub-account Email.
        start_time : long
            Time to search history from.
        end_time : long
            Time to search history until.
        page : long
            The transfer history batch number (each batch contains at most 500 transfer history 
            records).
        limit : int
            Default value: 500.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v3/sub-account/transfer/history"
        data = {
            "timestamp": timestamp
        }
        if email:
            data['email'] = email
        if start_time:
            data['startTime'] = start_time
        if start_time:
            data['endTime'] = end_time
        if page:
            data['page'] = page
        if limit:
            data['limit'] = limit
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def execute_sub_account_transfer(self, from_email, to_email, asset, amount,
                                     timestamp = int(round(time.time() * 1000))):
        """
        Use this endpoint to execute an asset transfer between the master account and a sub-account.

        Parameters
        ----------
        from_email : str
            Sender Email.
        to_email : long
            Recipient Email.
        asset : long
            Transfer asset.
        amount : long
            Transfer amount.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v3/sub-account/transfer/history"
        data = {
            "fromEmail": from_email,
            "toEmail": to_email,
            "asset": asset,
            "amount": amount,
            "timestamp": timestamp
        }
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def get_sub_account_assets(self, email, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to fetch sub-account assets.

        Parameters
        ----------
        email : str
            Sub-account Email.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v3/sub-account/assets"
        data = {
            'email': email,
            'timestamp': timestamp
        }
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_master_accounts_total_usd_value(self, email=None, page=None, size=None,
                                            timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get the total value of assets in the master account in USD.

        Parameters
        ----------
        email : str
            Sub-account Email.
        page: int
            Default value: 1.
        size: int
            Return request size.
        timestamp: long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v1/sub-account/spotSummary"
        data = {
            'timestamp': timestamp
        }
        if email:
            data['email'] = email
        if page:
            data['page'] = page
        if size:
            data['size'] = size
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_sub_account_status(self, email, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get a status list of sub-accounts.

        Parameters
        ----------      
        email : str
            Sub-account Email.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = "/sapi/v1/sub-account/status"
        data = {
            'email': email,
            'timestamp': timestamp
        }
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ## Trade Order Endpoints
    ### General Orders
    def get_order_rate_limits(self, recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Get the current trade order count rate limits for all time intervals.

        Parameters
        ----------
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp: long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/rateLimit/order'
        data = {
            "timestamp": timestamp
        }
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def create_new_order(self, symbol, side, order_type, time_in_force=None, quantity=None,
                         quote_order_quantity=None, price=None, new_client_order_id=None,
                         stop_price=None, trailing_delta=None, iceberg_qty=None,
                         self_trade_prevention_mode=None, new_order_resp_type=None,
                         recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Notes 
        ----------
        Any LIMIT or LIMIT_MAKER type order can be made an iceberg order by sending an iceberg_qty.
        Any order with an iceberg_qty MUST have timeInForce set to GTC.
        MARKET orders using quote_order_qty will not break LOT_SIZE filter rules; the order will 
        execute a quantity with a notional value as close as possible to quote_order_qty.

        Trigger order price rules against market price for both MARKET and LIMIT versions:
        Price above market price: STOP_LOSS BUY, TAKE_PROFIT SELL
        Price below market price: STOP_LOSS SELL, TAKE_PROFIT BUY

        Parameters
        ----------
        symbol : str
            Order trading pair (e.g., BTCUSD, ETHUSD).
        side : enum
            Order side (e.g., BUY, SELL).
        order_type : enum
            Order type (e.g., LIMIT, MARKET, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER).
        time_in_force: enum
            Duration for which a trading order remains active.
        quantity : dec
            Order quantity.
        quote_order_quantity : dec
            Order quantity of the quote asset for market order.
        price : dec
            Order price.
        new_client_order_id : str
            A unique ID among open orders. Automatically generated if not sent.
            Orders with the same new_client_order_id can be accepted only when the previous one is 
            filled, otherwise the order will be rejected.
            For API Partner Program members: In order to receive rebates the new_client_order_id 
            parameter must begin with your Partner ID, followed by a dash symbol, when calling order 
            placement endpoints. For example: “ABCD1234-…”.
        stop_price : dec
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
        trailing_delta : long
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
            For more details on SPOT implementation on trailing stops, please refer to 
            Trailing Stop FAQ:
            https://github.com/binance-us/binance-us-api-docs/blob/master/faqs/trailing-stop-faq.md
        icebergQty : dec
            Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        self_trade_prevention_mode : enum
            The configured default mode is EXPIRE_MAKER. The supported values currently are 
            EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH.
        new_order_resp_type : enum
            Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to 
            FULL; all other orders default to ACK.       
        recvWindow : long
            The value cannot be greater than 60000.
        timestamp: long
            Timestamp for request.
        
        Order Type Mandatory Parameters
        ----------
        LIMIT : time_in_force, quantity, price
        MARKET : quantity or quote_order_qty
            MARKET orders using the quantity field specifies the amount of the base asset the user 
            wants to buy or sell at the market price.
            E.g., a MARKET order on BTCUSDT will specify how much BTC the user is buying or selling
            MARKET orders using quote_order_qty specify the amount the user wants to spend (when 
            buying) or receive (when selling) the quote asset; the correct quantity will be 
            determined based on the market liquidity and quote_order_qty.
            E.g., Using the symbol BTCUSDT:
            BUY side, the order will buy as many BTC as quote_order_qty USDT can.
            SELL side, the order will sell as much BTC needed to receive quote_order_qty USDT.
        STOP_LOSS_LIMIT : time_in_force, quantity, price, stop_price, trailing_delta
            This will execute a LIMIT order when the stop_price is reached.
        TAKE_PROFIT_LIMIT : time_in_force, quantity, price, stop_price, trailing_delta
            This will execute a LIMIT order when the stopPrice is reached.
        LIMIT_MAKER : qauntity, price
            This is a LIMIT order that will be rejected if the order immediately matches and trades 
            as a taker.
            This is also known as a POST-ONLY order.
        """
        url_endpoint = '/api/v3/order'
        data = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'timestamp': timestamp
        }
        if quantity and quote_order_quantity:
            raise ValueError("Both 'quantity' and 'quote_order_quantity' cannot be specified "
                             "together.")
        if order_type == 'LIMIT':
            if not time_in_force or not quantity or not price:
                raise ValueError("LIMIT orders require 'time_in_force', 'quantity', and 'price' "
                                 "parameters.")
        elif order_type == 'MARKET':
            if not quantity and not quote_order_quantity:
                raise ValueError("MARKET orders require either 'quantity' or 'quote_order_quantity'"
                                 " parameters.")
        elif order_type == 'STOP_LOSS_LIMIT' or type == 'TAKE_PROFIT_LIMIT':
            if not time_in_force or not quantity:
                raise ValueError("LIMIT and TAKE_PROFIT_LIMT orders require 'time_in_force', "
                                 "'quantity', 'price', 'stop_price', and 'trailing_delta' "
                                 "parameters.")                 
            if not price or not stop_price or not trailing_delta:
                raise ValueError("LIMIT and TAKE_PROFIT_LIMT orders require 'time_in_force', "
                                 "'quantity', 'price', 'stop_price', and 'trailing_delta' "
                                 "parameters.")
        elif order_type == 'LIMIT_MAKER':
            if not quantity or not price:
                raise ValueError("LIMIT_MAKER orders require 'quantity' and 'price' parameters")
        if time_in_force:
            data['timeInForce'] = time_in_force
        if quantity:
            data['quanity'] = quantity
        if quote_order_quantity:
            data['quoteOrderQty'] = quote_order_quantity
        if price:
            data['price'] = price
        if new_client_order_id:
            data['newClientOrderId'] = new_client_order_id
        if stop_price:
            data['stopPrice'] = stop_price
        if trailing_delta:
            data['trailingDelta'] = trailing_delta
        if iceberg_qty:
            data['icebergQty'] = iceberg_qty
            if time_in_force != 'GTC':
                raise ValueError("Iceberg orders must have 'time_in_force' set to 'GTC'.")
        if self_trade_prevention_mode:
            data['selfTradePreventionMode'] = self_trade_prevention_mode
        if new_order_resp_type:
            data['newOrderRespType'] = new_order_resp_type
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def test_new_order(self, symbol, side, order_type, time_in_force=None, quantity=None,
                         quote_order_quantity=None, price=None, new_client_order_id=None,
                         stop_price=None, trailing_delta=None, iceberg_qty=None,
                         self_trade_prevention_mode=None, new_order_resp_type=None,
                         recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Notes 
        ----------
        Any LIMIT or LIMIT_MAKER type order can be made an iceberg order by sending an iceberg_qty.
        Any order with an iceberg_qty MUST have timeInForce set to GTC.
        MARKET orders using quote_order_qty will not break LOT_SIZE filter rules; the order will 
        execute a quantity with a notional value as close as possible to quote_order_qty.

        Trigger order price rules against market price for both MARKET and LIMIT versions:
        Price above market price: STOP_LOSS BUY, TAKE_PROFIT SELL
        Price below market price: STOP_LOSS SELL, TAKE_PROFIT BUY

        Parameters
        ----------
        symbol : str
            Order trading pair (e.g., BTCUSD, ETHUSD).
        side : enum
            Order side (e.g., BUY, SELL).
        order_type : enum
            Order type (e.g., LIMIT, MARKET, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER).
        time_in_force: enum
            Duration for which a trading order remains active.
        quantity : dec
            Order quantity.
        quote_order_quantity : dec
            Order quantity of the quote asset for market order.
        price : dec
            Order price.
        new_client_order_id : str
            A unique ID among open orders. Automatically generated if not sent.
            Orders with the same new_client_order_id can be accepted only when the previous one is 
            filled, otherwise the order will be rejected.
            For API Partner Program members: In order to receive rebates the new_client_order_id 
            parameter must begin with your Partner ID, followed by a dash symbol, when calling order 
            placement endpoints. For example: “ABCD1234-…”.
        stop_price : dec
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
        trailing_delta : long
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
            For more details on SPOT implementation on trailing stops, please refer to 
            Trailing Stop FAQ:
            https://github.com/binance-us/binance-us-api-docs/blob/master/faqs/trailing-stop-faq.md
        icebergQty : dec
            Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        self_trade_prevention_maker : enum
            The configured default mode is EXPIRE_MAKER. The supported values currently are 
            EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH.
        new_order_resp_type : enum
            Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to 
            FULL; all other orders default to ACK.
        recvWindow : long
            The value cannot be greater than 60000.
        timestamp: long
            Timestamp for request.
        
        Order Type Mandatory Parameters
        ----------
        LIMIT : time_in_force, quantity, price
        MARKET : quantity or quote_order_qty
            MARKET orders using the quantity field specifies the amount of the base asset the user 
            wants to buy or sell at the market price.
            E.g., a MARKET order on BTCUSDT will specify how much BTC the user is buying or selling
            MARKET orders using quote_order_qty specify the amount the user wants to spend (when 
            buying) or receive (when selling) the quote asset; the correct quantity will be 
            determined based on the market liquidity and quote_order_qty.
            E.g., Using the symbol BTCUSDT:
            BUY side, the order will buy as many BTC as quote_order_qty USDT can.
            SELL side, the order will sell as much BTC needed to receive quote_order_qty USDT.
        STOP_LOSS_LIMIT : time_in_force, quantity, price, stop_price, trailing_delta
            This will execute a LIMIT order when the stop_price is reached.
        TAKE_PROFIT_LIMIT : time_in_force, quantity, price, stop_price, trailing_delta
            This will execute a LIMIT order when the stopPrice is reached.
        LIMIT_MAKER : qauntity, price
            This is a LIMIT order that will be rejected if the order immediately matches and trades 
            as a taker.
            This is also known as a POST-ONLY order.
        """
        url_endpoint = '/api/v3/order'
        data = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'timestamp': timestamp
        }
        if quantity and quote_order_quantity:
            raise ValueError("Both 'quantity' and 'quote_order_quantity' cannot be specified "
                             "together.")
        if order_type == 'LIMIT':
            if not time_in_force or not quantity or not price:
                raise ValueError("LIMIT orders require 'time_in_force', 'quantity', and 'price' "
                                 "parameters.")
        elif order_type == 'MARKET':
            if not quantity and not quote_order_quantity:
                raise ValueError("MARKET orders require either 'quantity' or 'quote_order_quantity'"
                                 " parameters.")
        elif order_type == 'STOP_LOSS_LIMIT' or type == 'TAKE_PROFIT_LIMIT':
            if not time_in_force or not quantity:
                raise ValueError("LIMIT and TAKE_PROFIT_LIMT orders require 'time_in_force', "
                                 "'quantity', 'price', 'stop_price', and 'trailing_delta' "
                                 "parameters.")                 
            if not price or not stop_price or not trailing_delta:
                raise ValueError("LIMIT and TAKE_PROFIT_LIMT orders require 'time_in_force', "
                                 "'quantity', 'price', 'stop_price', and 'trailing_delta' "
                                 "parameters.")
        elif order_type == 'LIMIT_MAKER':
            if not quantity or not price:
                raise ValueError("LIMIT_MAKER orders require 'quantity' and 'price' parameters")
        if time_in_force:
            data['timeInForce'] = time_in_force
        if quantity:
            data['quanity'] = quantity
        if quote_order_quantity:
            data['quoteOrderQty'] = quote_order_quantity
        if price:
            data['price'] = price
        if new_client_order_id:
            data['newClientOrderId'] = new_client_order_id
        if stop_price:
            data['stopPrice'] = stop_price
        if trailing_delta:
            data['trailingDelta'] = trailing_delta
        if iceberg_qty:
            data['icebergQty'] = iceberg_qty
            if time_in_force != 'GTC':
                raise ValueError("Iceberg orders must have 'time_in_force' set to 'GTC'.")
        if self_trade_prevention_mode:
            data['selfTradePreventionMode'] = self_trade_prevention_mode
        if new_order_resp_type:
            data['newOrderRespType'] = new_order_resp_type
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def get_order(self, symbol, order_id=None, orig_client_order_id=None, recv_window=None,
                  timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to check a trade order's status.

        Notes 
        ----------
        Either orderId or origClientOrderId must be sent.
        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not 
        available at this time.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        order_id : long
            Identifier of specific order.
        orig_client_order_id : str
            Original client order ID.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp: long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/order'
        data = {
            'symbol': symbol,
            'timestamp': timestamp
        }
        if not order_id and not orig_client_order_id:
            raise ValueError("either 'order_id' or 'orig_client_order_id' must be specified.")
        if order_id:
            data['orderId'] = order_id
        if orig_client_order_id:
            data['origClientOrderId'] = orig_client_order_id
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_all_open_orders(self, symbol=None, recv_window=None,
                            timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get all open trade orders for a token symbol. Do not access this 
        without a token symbol as this would return all pair data.

        Notes 
        ----------
        If the symbol is not sent, orders for all symbols will be returned in an array. 

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp: long
            Timestamp for request.
        """
        url_endpoint = "/api/v3/openOrders"
        data = {
            'timestamp': timestamp
        }
        if symbol:
            data['symbol'] = symbol
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def cancel_order(self, symbol, order_id=None, orig_client_order_id=None,
                     new_client_order_id=None, cancel_restrictions=None, recv_window=None,
                     timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to cancel an active trade order.

        Notes 
        ----------
        Either order_id or orig_client_id must be sent.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        order_id : long
            Identifier of specific order.
        orig_client_order_id : str
            Original client order ID.
        new_client_order_id : str
            Used to uniquely identify this cancel. Automatically generated by default.
            For API Partner Program members: In order to receive rebates the new_client_order_id 
            parameter must begin with your Partner ID, followed by a dash symbol, when calling 
            order placement endpoints. For example: “ABCD1234-…”.
        cancel_restrictions : enum
            Supported values:
            ONLY_NEW - Cancel will succeed if the order status is NEW.
            ONLY_PARTIALLY_FILLED - Cancel will succeed if order status is PARTIALLY_FILLED.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp: long
            Timestamp for request.
        """
        url_endpoint = "/api/v3/order"
        data = {
            'symbol': symbol,
            'timestamp': timestamp
        }
        if not order_id and not orig_client_order_id:
            raise ValueError("either 'order_id' or 'orig_client_order_id' must be specified.")
        if order_id:
            data['orderId'] = order_id
        if orig_client_order_id:
            data['origClientOrderId'] = orig_client_order_id
        if new_client_order_id:
            data['newClientOrderId'] = new_client_order_id
        if cancel_restrictions:
            data['cancelRestrictions'] = cancel_restrictions
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_delete_request(url_endpoint, data)
        return f"DELETE {url_endpoint}: {result}"
    def cancel_open_orders_for_symbol(self, symbol, side, order_type, cancel_replace_mode,
                                    time_in_force=None, quantity=None, quote_order_qty=None,
                                    price=None, cancel_new_client_order_id=None,
                                    cancel_orig_client_order_id=None, cancel_order_id=None,
                                    new_client_order_id=None, stop_price=None,
                                    trailing_delta=None, iceberg_gty=None, new_order_resp_type=None,
                                    self_trade_prevention_mode=None, cancel_restrictions=None,
                                    recv_window=None, timestamp = int(round(time.time() * 1000))):
        """
        Use this endpoint to cancels all active trade orders on a token symbol (this includes OCO 
        orders).

        Regarding cancel_restrictions
        ----------
        If the cancel_restrictions value is not any of the supported values, the error will be:
        { "code": -1145, "msg": "Invalid cancelRestrictions" }
        If the order did not pass the conditions for cancelRestrictions, the error will be:
        { "code": -2011, "msg": "Order was not canceled due to cancel restrictions." }

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        side : enum
            Order side (e.g., BUY, SELL).
        order_type : enum
            Order type (e.g., LIMIT, MARKET, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER).
        cancel_replace_mode : enum
            The allowed values are:
            STOP_ON_FAILURE - If the cancel request fails, the new order placement 
            will not be attempted.
            ALLOW_FAILURE - new order placement will be attempted even if cancel request 
            fails.
        time_in_force : enum
            Duration for which a trading order remains active.
        quantity : dec
            Order quantity.
        quote_order_quantity : decimal
            Order quantity of the quote asset for market order.
        price : dec
            Order price.
        cancel_new_client_order_id : str
            Used to uniquely identify this 
            Either the cancel_orig_client_order_id or cancel_order_id must be provided. If 
            both are provided, cancelOrderId takes precedence.
        cancel_order_id : long
            Either the cancel_orig_client_order_id or cancel_order_id must be provided. If both are 
            provided, cancel_order_id takes precedence.
        new_client_order_id : str
            Used to identify the new order.
            For API Partner Program members: In order to receive rebates the new_client_order_id 
            parameter must begin with your Partner ID, followed by a dash symbol, when calling 
            order placement endpoints. For example: “ABCD1234-…”.
        stop_price : dec
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
        trailing_delta : long
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
            For more details on SPOT implementation on trailing stops, please refer to 
            Trailing Stop FAQ:
            https://github.com/binance-us/binance-us-api-docs/blob/master/faqs/trailing-stop-faq.md
        icebergQty : dec
            Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        new_order_resp_type : enum
            Allowed values:
            ACK, RESULT, FULL
            MARKET and LIMIT orders types default to FULL; all other orders default to ACK
        self_trade_prevention_mode : enum
            The allowed enums is dependent on what is configured on the symbol. The possible 
            supported values are EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH, NONE.
        cancel_restrictions : enum
            Supported values:
            ONLY_NEW - Cancel will succeed if the order status is NEW.
            ONLY_PARTIALLY_FILLED - Cancel will succeed if order status is PARTIALLY_FILLED. 
            For more information please refer to Regarding cancelRestrictions
        """
        url_endpoint = '/api/v3/openOrders'
        data = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'cancelReplaceMode': cancel_replace_mode, 
            'timestamp': timestamp
        }
        if not cancel_orig_client_order_id and not cancel_order_id:
            raise ValueError("Either the cancelOrigClientOrderId or cancelOrderId must be provided")
        if time_in_force:
            data['timeInForce'] = time_in_force
        if quantity:
            data['quantity'] = quantity
        if quote_order_qty:
            data['quoteOrderQty'] = quote_order_qty
        if price:
            data['price'] = price
        if cancel_new_client_order_id:
            data['cancelNewClientOrderId'] = cancel_new_client_order_id
        if cancel_orig_client_order_id:
            data['cancelOrigClientOrderId'] = cancel_orig_client_order_id
        if cancel_order_id:
            data['cancelOrderId'] = cancel_order_id
        if new_client_order_id:
            data['newClientOrderId'] = new_client_order_id
        if stop_price:
            data['stopPrice'] = stop_price
        if trailing_delta:
            data['trailingDelta'] = trailing_delta
        if iceberg_gty:
            data['icebergQty'] = iceberg_gty
        if new_order_resp_type:
            data['newOrderRespType'] = new_order_resp_type
        if self_trade_prevention_mode:
            data['selfTradePreventionMode'] = self_trade_prevention_mode
        if cancel_restrictions:
            data['cancelRestrictions'] = cancel_restrictions
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_delete_request(url_endpoint, data)
        return f"DELETE {url_endpoint}: {result}"
    def get_trades(self, symbol, order_id=None, start_time=None, end_time=None, from_id=None,
                   limit=None, recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get trade data for a specific account and token symbol.

        Notes 
        ----------
        If fromId is set, it will get orders >= than fromId. Otherwise most recent orders are 
        returned.
        The time between startTime and endTime can't be longer than 24 hours.
        These are the supported combinations of optional parameters:
            symbol
            symbol + orderId
            symbol + fromId
            symbol + startTime
            symbol + endTime
            symbol + startTime + endTime
            symbol + orderId + fromId
            
        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        order_id : long
            This can only be used in combination with symbol
        start_time : long
            Timestamp in ms to get aggregate trades from INCLUSIVE.
        end_time : long
            Timestamp in ms to get aggregate trades until INCLUSIVE.
        from_id : long
            Trade is to fetch from. default gets most recent trades.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp: long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/myTrades'
        data = {
            'symbol': symbol,
            'timestamp': timestamp
        }
        if order_id:
            data['orderId'] = order_id
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if from_id:
            data['fromId'] = from_id
        if limit:
            data['limit'] = limit
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def replace_order(self, symbol, side, order_type, cancel_replace_mode, time_in_force=None,
                    quantity=None, quote_order_qty=None, price=None,
                    cancel_new_client_order_id=None, cancel_orig_client_order_id=None,
                    cancel_order_id=None, new_client_order_id=None, strategy_id=None,
                    strategy_type=None, stop_price=None, trailing_delta=None, iceberg_qty=None,
                    self_trade_prevention_mod=None, new_order_resp_type=None, recv_window=None,
                    timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to replace an existing order with a new order.

        Notes
        ----------
        Cancels an existing order and places a new order on the same symbol.
        Filters and Order Count are evaluated before the processing of the cancellation and
        order placement occurs.
        A new order that was not attempted (i.e. when newOrderResult: NOT_ATTEMPTED), will 
        still increase the order count by 1.

        Parameters
        ----------
        symbol : str
            Order trading pair (e.g., BTCUSD, ETHUSD).
        side : enum
            Order side (e.g., BUY, SELL).
        order_type : enum
            Order type (e.g., LIMIT, MARKET, STOP_LOSS_LIMIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER).
        cancel_replace_mode : enum
            The allowed values are:
            STOP_ON_FAILURE - If the cancel request fails, the new order placement will not be 
            attempted.
            ALLOW_FAILURE - New order placement will be attempted even if cancel request fails.
        time_in_force : enum, optional
            Duration for which a trading order remains active.
        quantity : decimal, optional
            Order quantity.
        quote_order_qty : decimal, optional
            Order quantity of the quote asset for market order.
        price : decimal, optional
            Order price.
        cancel_new_client_order_id : str, optional
            Used to uniquely identify this cancel. Automatically generated by default.
        cancel_orig_client_order_id : str, optional
            Either the cancelOrigClientOrderId or cancelOrderId must be provided. If both are 
            provided, cancelOrderId takes precedence.
        cancel_order_id : long, optional
            Identifier of specific order to cancel.
            Either the cancelOrigClientOrderId or cancelOrderId must be provided. If both are 
            provided, cancelOrderId takes precedence.
        new_client_order_id : str, optional
            Used to identify the new order.
            For API Partner Program members: In order to receive rebates the newClientOrderId 
            parameter must begin with your Partner ID, followed by a dash symbol, when calling 
            order placement endpoints. For example: “ABCD1234-…”.
        strategy_id : long, optional
            Strategy ID.
        strategy_type : long, optional
            The value cannot be less than 1000000.
        stop_price : decimal, optional
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
        trailing_delta : long, optional
            Used with STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT orders.
        iceberg_qty : decimal, optional
            Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        self_trade_prevention_mode : enum, optional
            The configured default mode is EXPIRE_MAKER. The supported values currently are 
            EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH.
        new_order_resp_type : enum, optional
            Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default 
            to FULL; all other orders default to ACK.
        recv_window : long, optional
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/order/cancelReplace'
        data = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'cancelReplaceMode': cancel_replace_mode,
            'timestamp': timestamp
        }
        if not cancel_orig_client_order_id and not cancel_order_id:
            raise ValueError("Either the cancelOrigClientOrderId or cancelOrderId must be provided")
        if time_in_force:
            data['timeInForce'] = time_in_force
        if quantity:
            data['quantity'] = quantity
        if quote_order_qty:
            data['quoteOrderQty'] = quote_order_qty
        if price:
            data['price'] = price
        if cancel_new_client_order_id:
            data['cancelNewClientOrderId'] = cancel_new_client_order_id
        if cancel_orig_client_order_id:
            data['cancelOrigClientOrderId'] = cancel_orig_client_order_id
        if cancel_order_id:
            data['cancelOrderId'] = cancel_order_id
        if new_client_order_id:
            data['newClientOrderId'] = new_client_order_id
        if strategy_id:
            data['strategyId'] = strategy_id
        if strategy_type:
            data['strategyType'] = strategy_type
        if stop_price:
            data['stopPrice'] = stop_price
        if trailing_delta:
            data['trailingDelta'] = trailing_delta
        if iceberg_qty:
            data['icebergQty'] = iceberg_qty
        if self_trade_prevention_mod:
            data['selfTradePreventionMode'] = self_trade_prevention_mod
        if new_order_resp_type:
            data['newOrderRespType'] = new_order_resp_type
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def query_prevented_matches(self, symbol, prevented_match_id=None, order_id=None,
                                from_prevented_match_id=None, limit=None, recv_window=None,
                                timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to query the list of prevented matches.

        Notes
        ----------
        If the symbol is not sent, all prevented matches will be returned in an array.
        If both order_id and prevented_match_id are sent, order_id takes precedence.

        Parameters
        ----------
        symbol : str, optional
            Ticker ID to get data from.
        prevented_match_id : long, optional
            Identifier of the specific prevented match.
        order_id : long, optional
            Identifier of the specific order.
        from_prevented_match_id : long, optional
            Start with the prevented match ID.
        limit : int, optional
            Default 500; max 1000.
        recv_window : long, optional
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/myPreventedMatches'
        data = {'timestamp': timestamp}
        if symbol:
            data['symbol'] = symbol
        if prevented_match_id:
            data['preventedMatchId'] = prevented_match_id
        if order_id:
            data['orderId'] = order_id
        if from_prevented_match_id:
            data['fromPreventedMatchId'] = from_prevented_match_id
        if limit:
            data['limit'] = limit
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def all_orders(self, symbol, order_id=None, start_time=None, end_time=None, limit=None,
                   recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Get all account orders: active, canceled, or filled.

        Notes
        ----------
        If order_id is set, it will get orders >= that order_id. Otherwise, most recent orders 
        are returned.
        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not 
        available at this time.
        If start_time and/or end_time provided, order_id is not required.

        Parameters
        ----------
        symbol : str
            Ticker ID to get data from.
        order_id : long, optional
            Identifier of specific order.
        start_time : long, optional
            Timestamp in ms to get orders from INCLUSIVE.
        end_time : long, optional
            Timestamp in ms to get orders until INCLUSIVE.
        limit : int, optional
            Default 500; max 1000.
        recv_window : long, optional
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/allOrders'
        data = {
            'symbol': symbol,
            'timestamp': timestamp
        }
        if order_id:
            data['orderId'] = order_id
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if limit:
            data['limit'] = limit
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ### OCO Orders
    def create_new_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price=None,
                             limit_client_order_id=None, stop_client_order_id=None,
                             list_client_order_id=None, limit_iceberg_qty=None,
                             stop_iceberg_qty=None, stop_limit_time_in_force=None,
                             new_order_resp_type=None, self_trade_prevention_mode=None,
                             recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to create a new OCO (One Cancels the Other) order.

        Parameters
        ----------
        symbol : str
            Order trading pair (e.g., BTCUSD, ETHUSD).
        side : enum
            Order side (e.g., BUY, SELL).
        quantity : decimal
            Order quantity.
        price : decimal
            Order price.
        stop_price : decimal
            Stop price.
        stop_limit_price : decimal
            Stop limit price.
        limit_client_order_id : str
            A unique ID for the limit order.
        stop_client_order_id : str
            A unique ID for the stop loss/stop loss limit leg.
        list_client_order_id : str
            A unique ID for the entire orderList.
        limit_iceberg_qty : decimal
            Iceberg quantity for the limit order.
        stop_iceberg_qty : decimal
            Iceberg quantity for the stop order.
        stop_limit_time_in_force : enum
            Valid values are GTC/FOK/IOC
        new_order_resp_type : enum
            Set the response JSON. ACK, RESULT, or FULL.
        self_trade_prevention_mode : enum
            The configured default mode is EXPIRE_MAKER. The supported values currently are 
            EXPIRE_TAKER, EXPIRE_MAKER, EXPIRE_BOTH.
        recv_window : long, optional
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/order/oco'
        data = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'stopPrice': stop_price,
            'timestamp': timestamp
        }
        if stop_limit_price:
            data['stopLimitPrice'] = stop_limit_price
        if limit_client_order_id:
            data['limitClientOrderId'] = limit_client_order_id
        if stop_client_order_id:
            data['stopClientOrderId'] = stop_client_order_id
        if list_client_order_id:
            data['listClientOrderId'] = list_client_order_id
        if limit_iceberg_qty:
            data['limitIcebergQty'] = limit_iceberg_qty
        if stop_iceberg_qty:
            data['stopIcebergQty'] = stop_iceberg_qty
        if stop_limit_time_in_force:
            data['stopLimitTimeInForce'] = stop_limit_time_in_force
        if new_order_resp_type:
            data['newOrderRespType'] = new_order_resp_type
        if self_trade_prevention_mode:
            data['selfTradePreventionMode'] = self_trade_prevention_mode
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def get_oco_order(self, order_list_id=None, list_client_order_id=None, recv_window=None,
                      timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get an OCO order's status.

        Parameters
        ----------
        symbol : str
            Order trading pair (e.g., BTCUSD, ETHUSD).
        order_list_id : long
            Either order_list_id or list_client_order_id must be provided
        list_client_order_id : str
            Either order_list_id or list_client_order_id must be provided
        recv_window : long
            The value cannot be greater than 60000
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/orderList'
        data = {
            'timestamp': timestamp
        }
        if not order_list_id and not list_client_order_id:
            raise ValueError("Either 'order_list_id' or 'list_client_order_id' must be provided.")
        if order_list_id:
            data['orderListId'] = order_list_id
        if list_client_order_id:
            data['origClientOrderId'] = list_client_order_id
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_all_oco_order(self, from_id=None, start_time=None, end_time=None, limit=None,
                          recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get all OCO orders.

        Parameters
        ----------
        from_id : long
            Start with the order list ID.
        start_time : long
            Timestamp in ms to get orders from INCLUSIVE.
        end_time : long
            Timestamp in ms to get orders until INCLUSIVE.
        limit : int
            Default 500; max 1000.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/allOrderList'
        data = {
            'timestamp': timestamp
        }
        if from_id:
            data['fromId'] = from_id
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if limit:
            data['limit'] = limit
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_open_oco_orders(self, recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get all open OCO orders.

        Parameters
        ----------
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/openOrderList'
        data = {
            'timestamp': timestamp
        }
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def cancel_oco_order(self, symbol, order_list_id=None, list_client_order_id=None,
                         new_client_order_id=None, recv_window=None,
                         timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to cancel an active OCO order.

        Parameters
        ----------
        symbol : str
            Order trading pair (e.g., BTCUSD, ETHUSD).
        order_list_id : long
            Either orderListId or listClientOrderId must be provided.
        list_client_order_id : str
            Either orderListId or listClientOrderId must be provided.
        new_client_order_id : str
            Used to uniquely identify this cancel. Automatically generated by default.
            For API Partner Program members: In order to receive rebates the newClientOrderId 
            parameter must begin with your Partner ID, followed by a dash symbol, when calling 
            order placement endpoints. For example: “ABCD1234-…”.
        recv_window : long
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/api/v3/orderList'
        data = {
            'symbol': symbol,
            'timestamp': timestamp
        }
        if order_list_id:
            data['orderListId'] = order_list_id
        if list_client_order_id:
            data['listClientOrderId'] = list_client_order_id
        if new_client_order_id:
            data['newClientOrderId'] = new_client_order_id
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_delete_request(url_endpoint, data)
        return f"DELETE {url_endpoint}: {result}"
    ## OTC Endpoints
    def get_supported_coin_pairs(self, from_coin=None, to_coin=None,
                                 timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get the list of supported coin pairs for OTC trading.

        Parameters
        ----------
        from_coin : str
            From coin name, e.g. BTC, SHIB.
        to_coin : str
            To coin name, e.g. USDT, KSHIB.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/sapi/v1/otc/coinPairs'
        data = {
            'timestamp': timestamp
        }
        if from_coin:
            data['fromCoin'] = from_coin
        if to_coin:
            data['toCoin'] = to_coin
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def request_for_quote(self, from_coin, to_coin, request_coin, request_amount,
                          timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to request a quote for an OTC trade.

        Parameters
        ----------
        from_coin : str
            From coin name, e.g. SHIB
        to_coin : str
            To coin name, e.g. KSHIB
        request_coin : decimal
            Request coin name, e.g. SHIB
        request_amount : str
            Amount of request coin, e.g. 50000
        timestamp : long
            Timestamp for request.

        """
        url_endpoint = '/sapi/v1/otc/quotes'
        data = {
            'fromCoin': from_coin,
            'toCoin': to_coin,
            'requestCoin': request_coin,
            'requestAmount': request_amount,
            'timestamp': timestamp
        }
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def place_otc_trade_order(self, quote_id, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to place an OTC trade order.

        Parameters
        ----------
        quote_id : str
            The quote ID for the trade.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/sapi/v1/otc/orders'
        data = {
            'quoteId': quote_id,
            'timestamp': timestamp
        }
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def get_otc_trade_order(self, order_id, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get the details of an OTC trade order.

        Parameters
        ----------
        order_id : str
            The order ID for the trade.
        timestamp : long
            Timestamp for request.

        """
        url_endpoint = f'/sapi/v1/otc/orders/{order_id}'
        data = {
            'orderId': order_id,
            'timestamp': timestamp
        }
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_all_otc_trade_orders(self, from_coin=None, to_coin=None, start_time=None, end_time=None,
                                 page=None, limit=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to query OTC trade orders by condition.

        Parameters
        ----------
        from_coin : str
            The coin to trade from.
        to_coin : str
            The coin to trade to.
        start_time : long
            Timestamp in ms to get orders from INCLUSIVE.
        end_time : long
            Timestamp in ms to get orders until INCLUSIVE.
        page : int
            Set the number of pages, depending on the number of records and the record limit 
            for each page. No maximum value of pages.
        limit : int
            Number of records per page. Default: 10, Max: 100.
        timestamp : int
            Timestamp in ms for the request. Defaults to current time in ms.
        """
        url_endpoint = '/sapi/v1/otc/allOrders'
        data = {
            'timestamp': timestamp
        }
        if from_coin:
            data['fromCoin'] = from_coin
        if to_coin:
            data['toCoin'] = to_coin
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if page:
            data['page'] = page
        if limit:
            data['limit'] = limit
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_all_ocbs_trade_orders(self, order_id=None, start_time=None, end_time=None, page=None,
                                  limit=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get all OCBS trade orders.

        Parameters
        ----------
        order_id : str
            Order ID
        start_time : long
            Timestamp in ms to get orders from INCLUSIVE.
        end_time : long
            Timestamp in ms to get orders until INCLUSIVE.
        page : int
            Set the number of pages, depending on the number of records and the record 
            limit for each page. No maximum value of pages.
        limit : int
            Number of records per page. Default: 10, Max: 100.
        timestamp : long
            Timestamp in ms for the request. Defaults to current time in ms.
        """
        url_endpoint = '/sapi/v1/ocbs/orders'
        data = {
            'timestamp': timestamp
        }
        if order_id:
            data['orderId'] = order_id
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if page:
            data['page'] = page
        if limit:
            data['limit'] = limit
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ## Wallet Endpoints
    ### Asset Fees & Wallet Status
    def get_asset_fees_and_wallet_status(self, recv_window=None,
                                         timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to fetch the details of all crypto assets including fees, withdrawal 
        limits, and network status.

        Parameters
        ----------
        recv_window : long
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp in ms for the request. Defaults to current time in ms.
        """
        url_endpoint = '/sapi/v1/capital/config/getall'
        data = {
            'timestamp': timestamp
        }
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ### Withdrawals
    def withdraw_fiat_via_bitgo(self, payment_method, payment_account, amount, fiat_currency=None,
                                recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to withdraw fiat currency via BitGo.

        Parameters
        ----------
        payment_method : str
            The payment method to use for the withdrawal (e.g., bank transfer).
        payment_account : str
            The account to withdraw to.
        amount : decimal
            The amount to withdraw.
        fiat_currency : str, optional
            The fiat currency to withdraw (e.g., USD). If not provided, the default currency 
            will be used.
        recv_window : long, optional
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/sapi/v1/fiatpayment/withdraw/apply'
        data = {
            'paymentMethod': payment_method,
            'paymentAccount': payment_account,
            'amount': amount,
            'timestamp': timestamp
        }
        if fiat_currency:
            data['fiatCurrency'] = fiat_currency
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def withdraw_crypto(self, coin, network, address, amount, withdraw_order_id=None,
                        address_tag=None, recv_window=None,
                        timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to withdraw cryptocurrency.

        Parameters
        ----------
        coin : str
            The cryptocurrency to withdraw (e.g., BTC, ETH).
        network : str
            Specify the withdrawal network (e.g. 'ERC20' or 'BEP20'). Please ensure the address 
            type is correct for the chosen network.
        withdraw_order_id : str
            Client ID for withdraw.
        address : str
            The address to withdraw to.
        address_tag : str
            Memo: Acts as a secondary address identifier for coins like XRP, XMR etc.
        amount : decimal
            The amount to withdraw.
        recv_window : long, optional
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/sapi/v1/capital/withdraw/apply'
        data = {
            'coin': coin,
            'network': network,
            'address': address,
            'addressTag': address_tag,
            'amount': amount,
            'timestamp': timestamp
        }
        if withdraw_order_id:
            data['withdrawOrderId'] = withdraw_order_id
        if address_tag:
            data['addressTag'] = address_tag
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_post_request(url_endpoint, data)
        return f"POST {url_endpoint}: {result}"
    def get_crypto_withdrawal_history(self, coin, withdraw_order_id=None, status=None,
                                      start_time=None, end_time=None, offset=None, limit=None,
                                      recv_window=None, timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get the history of cryptocurrency withdrawals.

        Parameters
        ----------
        coin : str
            The coin to get the history for.
        withdraw_order_id : str
            Client ID for withdraw
        status : int
            0: email sent, 1: canceled, 2: awaiting approval, 3: rejected, 4: processing,
            5: failure, 6: completed
        start_time : long
            Default: 90 days from current timestamp
        end_time : long
            Default: present timestamp
        offset : int
            Default: 0
        limit : int
            Default: 1000, max: 1000
        recv_window : long
            The value cannot be greater than 60000.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/sapi/v1/capital/withdraw/history'
        data = {
            'coin': coin,
            'timestamp': timestamp
        }
        if withdraw_order_id:
            data['withdrawOrderId'] = withdraw_order_id
        if status:
            data['status'] = status
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if offset:
            data['offset'] = offset
        if limit:
            data['limit'] = limit
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    def get_fiat_withdrawal_history(self, fiat_currency=None, order_id=None, offset=None,
                                    payment_channel=None, payment_method=None, start_time=None,
                                    end_time=None, recv_window=None,
                                    timestamp=int(round(time.time() * 1000))):
        """
        Use this endpoint to get the history of fiat withdrawals.

        Notes
        ----------
        Please pay attention to the default value of startTime and endTime.
        If both startTime and endTime are sent, the duration between startTime and endTime must 
        be greater than 0 day and less than 90 days.

        Parameters
        ----------
        fiat_currency : str, optional
            The fiat currency to filter the withdrawal history (e.g., USD).
        order_id : str, optional
            The order ID to filter the withdrawal history.
        offset : int, optional
            The offset for pagination.
        payment_channel : str, optional
            The payment channel used for the withdrawal.
        payment_method : str, optional
            The payment method used for the withdrawal.
        start_time : long, optional
            Default to 90 days from current timestamp.
        end_time : long, optional
            Default to current timestamp
        recv_window : long, optional
            Number of milliseconds after timestamp request is valid for.
        timestamp : long
            Timestamp for request.
        """
        url_endpoint = '/sapi/v1/fiatpayment/query/withdraw/history'
        data = {
            'timestamp': timestamp
        }
        if fiat_currency:
            data['fiatCurrency'] = fiat_currency
        if order_id:
            data['orderId'] = order_id
        if offset:
            data['offset'] = offset
        if payment_channel:
            data['paymentChannel'] = payment_channel
        if payment_method:
            data['paymentMethod'] = payment_method
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        if recv_window:
            data['recvWindow'] = recv_window
        result = self.__binanceus_get_request(url_endpoint, data)
        return f"GET {url_endpoint}: {result}"
    ### Deposits
    #def get_crypto_deposit_address():
    #def get_crypto_deposit_history():
    #def get_fiat_deposit_history():
    #def get_sub_account_depsoit_address(self):
    #def get_sub_account_deposit_history(self):
    ## Convert Dust
    #def convert_dust(self):
    #def get_convert_dust_history(self):
    #def get_assets_that_can_be_converted(self):
    ## Referral Endpoints
    #def get_referral_reward_history(self):
    ## Staking Endpoints
    #def get_staking_asset_information(self):
    #def stake_asset(self):
    #def unstake_asset(self):
    #def get_staking_balance(self):
    #def get_staking_history(self):
    #def get_staking_rewards_history(self):
    ## Credit Line Endpoints
    #def get_credt_line_account_information(self):
    #def get_alert_history(self):
    #def get_transfer_history(self):
    #def execute_transfer(self):
    ## API Partner Endpoints
    #def check_user_eligibility(self):
    #def get_rebate_history(self):
    #class Custodial:
        #Dunder Methods
        #def __init__(self):
        #Private Methods
        #Public Methods
        ## Custodial Solution Endpoints
        ### User Account Data (Custodial)
        #def get_account_balance(self):
        #def get_supported_asset_list(self):
        ### Transfer (Custodial)
        #def transfer_from_exchange_wallet(self):
        #def transfer_from_custodian(self):
        #def undo_transfer(self):
        #def get_exchange_wallet_transfer(self):
        #def custodian_transfer(self):
        ### Trade Order (Custodial)
        #def create_new_order(self):
        #def create_new_oco_order(self):
        #def get_all_open_orders(self):
        #def get_order(self):
        #def get_order_history(self):
        #def get_trade_history(self):
        #def cancel_order(self):
        #def cancel_open_orders_for_symbol(self):
        #def cancel_oco_order(self):
        ### Settlement (Custodial)
        #def get_settlement_settings(self):
        #def get_settlement_history(self):
        ## Credit Line Endpoints
        #def get_credt_line_account_information(self):
        #def get_alert_history(self):
        #def get_transfer_history(self):
        #def execute_transfer(self):
        ## API Partner Endpoints
        #def check_user_eligibility(self):
        #def get_rebate_history(self):
#class BinanceWebSocketAPI:
#class BinanceWebSocketStreams:
