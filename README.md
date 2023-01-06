# crypto-msg-parser

Python bindings for the [crypto-msg-parser](https://github.com/crypto-crawler/crypto-crawler-rs/tree/main/crypto-msg-parser) library.

## Install

```bash
pip3 install crypto-msg-parser
```

## Quickstart

```python
from crypto_msg_parser import MarketType, parse_trade

json_arr = parse_trade("binance", MarketType['inverse_swap'], '{"stream":"btcusd_perp@aggTrade","data":{"e":"aggTrade","E":1616201883458,"a":41045788,"s":"BTCUSD_PERP","p":"58570.1","q":"58","f":91864326,"l":91864327,"T":1616201883304,"m":true}}')

assert len(json_arr) == 1
trade = json_arr[0]
assert trade["exchange"] == "binance"
assert trade["market_type"] == "inverse_swap"
assert trade["msg_type"] == "trade"
assert trade["price"] == 58570.1
assert trade["quantity_base"] == 5800.0 / 58570.1
assert trade["quantity_quote"] == 5800.0
assert trade["quantity_contract"] == 58.0
assert trade["side"] == "sell"
```

Another example, parsing the output of `crypto-crawler`:

```python
from crypto_crawler import MarketType, crawl_trade
from crypto_msg_parser import MarketType, parse_trade

crawl_trade(
    "binance",
    MarketType.Spot,
    ["BTCUSDT", "ETHUSDT"],
    lambda msg: print(parse_trade(msg.exchange, msg.market_type, msg.json))
)
```
