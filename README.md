# crypto-msg-parser

Python bindings for the [crypto-msg-parser](https://github.com/soulmachine/crypto-crawler-rs/tree/main/crypto-msg-parser) library.

## Quickstart

Install,

```bash
pip3 install crypto-msg-parser
```

```python
from crypto_msg_parser import MarketType, parse_trade

json_arr = parse_trade("binance", MarketType['inverse_swap'], '{"stream":"btcusd_perp@aggTrade","data":{"e":"aggTrade","E":1616201883458,"a":41045788,"s":"BTCUSD_PERP","p":"58570.1","q":"58","f":91864326,"l":91864327,"T":1616201883304,"m":true}}')

assert len(json_arr) == 1
trade = json_arr[0]
assert trade['exchange'] == 'binance'
assert trade['market_type'] == 'inverse_swap'
assert trade['msg_type'] == 'trade'
assert trade['price'] == 58570.1
assert trade['quantity_base'] == 5800.0 / 58570.1
assert trade['quantity_quote'] == 5800.0
assert trade['quantity_contract'] == 58.0
assert trade['side'] == 'sell'
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

## How to build

On Mac OS X,

```bash
conda install --file requirements-dev.txt

rm -rf build crypto-msg-parser-ffi/target
python3 setup.py bdist_wheel

# Need to create a ~/.pypirc file first
twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps crypto-msg-parser

twine upload dist/*
```

For Linux,

```bash
docker run -it --rm -v $(pwd):/project soulmachine/rust:manylinux2014 bash

/opt/python/cp36-cp36m/bin/pip3 install -r requirements-dev.txt
rm -rf build crypto-msg-parser-ffi/target
/opt/python/cp36-cp36m/bin/python3 setup.py bdist_wheel
auditwheel repair dist/*linux*.whl --plat manylinux2014_x86_64
/opt/python/cp36-cp36m/bin/twine upload --repository testpypi wheelhouse/*
```

## Test

```bash
python3 setup.py develop
pytest -s
```
