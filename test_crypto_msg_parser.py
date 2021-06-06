#!/usr/bin/env python3

from crypto_msg_parser import (MarketType, parse_funding_rate, parse_l2,
                               parse_trade)


def test_parse_trade():
    json_arr = parse_trade("binance", MarketType.InverseSwap, '{"stream":"btcusd_perp@aggTrade","data":{"e":"aggTrade","E":1616201883458,"a":41045788,"s":"BTCUSD_PERP","p":"58570.1","q":"58","f":91864326,"l":91864327,"T":1616201883304,"m":true}}')
    assert len(json_arr) == 1
    trade = json_arr[0]
    assert trade['exchange'] == 'binance'
    assert trade['market_type'] == str(MarketType.InverseSwap)
    assert trade['msg_type'] == 'trade'
    assert trade['price'] == 58570.1
    assert trade['quantity_base'] == 5800.0 / 58570.1
    assert trade['quantity_quote'] == 5800.0
    assert trade['quantity_contract'] == 58.0
    assert trade['side'] == 'sell'

def test_parse_l2():
    json_arr = parse_l2("binance", MarketType.InverseSwap, '{"stream":"btcusd_perp@depth@100ms","data":{"e":"depthUpdate","E":1622370862564,"T":1622370862553,"s":"BTCUSD_PERP","ps":"BTCUSD","U":127559587191,"u":127559588177,"pu":127559587113,"b":[["35365.9","1400"],["35425.8","561"]],"a":[["35817.8","7885"],["35818.7","307"]]}}')
    assert len(json_arr) == 1
    orderbook = json_arr[0]
    assert orderbook['exchange'] == 'binance'
    assert orderbook['market_type'] == str(MarketType.InverseSwap)
    assert orderbook['msg_type'] == 'l2_event'
    assert len(orderbook['asks']) == 2
    assert len(orderbook['bids']) == 2
    assert orderbook['snapshot'] == False
    assert orderbook['timestamp'] == 1622370862553
    assert orderbook['bids'][0][0] == 35365.9
    assert orderbook['bids'][0][3] == 1400.0
    assert orderbook['asks'][0][0] == 35817.8
    assert orderbook['asks'][0][3] == 7885.0

def test_parse_funding_rate():
    json_arr = parse_funding_rate("binance", MarketType.InverseSwap, '{"stream":"btcusd_perp@markPrice","data":{"e":"markPriceUpdate","E":1617309477000,"s":"BTCUSD_PERP","p":"59012.56007222","P":"58896.00503145","r":"0.00073689","T":1617321600000}}')
    assert len(json_arr) == 1
    rate = json_arr[0]
    assert rate['exchange'] == 'binance'
    assert rate['market_type'] == str(MarketType.InverseSwap)
    assert rate['msg_type'] == 'funding_rate'
    assert rate['pair'] == "BTC/USD"
    assert rate['funding_rate'] == 0.00073689
    assert rate['funding_time'] == 1617321600000
