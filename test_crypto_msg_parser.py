#!/usr/bin/env python3

from crypto_msg_parser import (
    MarketType,
    MessageType,
    extract_symbol,
    extract_timestamp,
    get_msg_type,
    parse_bbo,
    parse_candlestick,
    parse_funding_rate,
    parse_l2,
    parse_l2_topk,
    parse_trade,
)


def test_extract_symbol():
    symbol = extract_symbol(
        "binance",
        MarketType["inverse_swap"],
        '{"stream":"btcusd_perp@aggTrade","data":{"e":"aggTrade","E":1616201883458,"a":41045788,"s":"BTCUSD_PERP","p":"58570.1","q":"58","f":91864326,"l":91864327,"T":1616201883304,"m":true}}',
    )
    assert "BTCUSD_PERP" == symbol


def test_extract_timestamp():
    timestamp = extract_timestamp(
        "binance",
        MarketType["inverse_swap"],
        '{"stream":"btcusd_perp@markPrice","data":{"e":"markPriceUpdate","E":1617309477000,"s":"BTCUSD_PERP","p":"59012.56007222","P":"58896.00503145","r":"0.00073689","T":1617321600000}}',
    )
    assert timestamp.is_ok()
    assert timestamp.unwrap() == 1617309477000


def test_get_msg_type():
    msg_type = get_msg_type(
        "binance",
        '{"stream":"btcusd_perp@aggTrade","data":{"e":"aggTrade","E":1616201883458,"a":41045788,"s":"BTCUSD_PERP","p":"58570.1","q":"58","f":91864326,"l":91864327,"T":1616201883304,"m":true}}',
    )
    assert MessageType.trade == msg_type


def test_parse_trade():
    json_arr = parse_trade(
        "binance",
        MarketType["inverse_swap"],
        '{"stream":"btcusd_perp@aggTrade","data":{"e":"aggTrade","E":1616201883458,"a":41045788,"s":"BTCUSD_PERP","p":"58570.1","q":"58","f":91864326,"l":91864327,"T":1616201883304,"m":true}}',
    )
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


def test_parse_l2():
    json_arr = parse_l2(
        "binance",
        MarketType["inverse_swap"],
        '{"stream":"btcusd_perp@depth@100ms","data":{"e":"depthUpdate","E":1622370862564,"T":1622370862553,"s":"BTCUSD_PERP","ps":"BTCUSD","U":127559587191,"u":127559588177,"pu":127559587113,"b":[["35365.9","1400"],["35425.8","561"]],"a":[["35817.8","7885"],["35818.7","307"]]}}',
    )
    assert len(json_arr) == 1
    orderbook = json_arr[0]
    assert orderbook["exchange"] == "binance"
    assert orderbook["market_type"] == "inverse_swap"
    assert orderbook["msg_type"] == "l2_event"
    assert len(orderbook["asks"]) == 2
    assert len(orderbook["bids"]) == 2
    assert orderbook["snapshot"] == False
    assert orderbook["timestamp"] == 1622370862564
    assert orderbook["seq_id"] == 127559588177
    assert orderbook["prev_seq_id"] == 127559587113
    assert orderbook["bids"][0][0] == 35365.9
    assert orderbook["bids"][0][3] == 1400.0
    assert orderbook["asks"][0][0] == 35817.8
    assert orderbook["asks"][0][3] == 7885.0


def test_parse_l2_topk():
    json_arr = parse_l2_topk(
        "binance",
        MarketType["linear_swap"],
        '{"stream":"ethusdt@depth20","data":{"e":"depthUpdate","E":1651122265861,"T":1651122265854,"s":"ETHUSDT","U":1437010873371,"u":1437010882721,"pu":1437010873329,"b":[["2886.71","0.454"],["2886.70","2.755"],["2886.67","1.000"]],"a":[["2886.72","77.215"],["2886.73","1.734"],["2886.74","0.181"]]}}',
    )
    assert len(json_arr) == 1
    orderbook = json_arr[0]
    assert orderbook["exchange"] == "binance"
    assert orderbook["market_type"] == "linear_swap"
    assert orderbook["msg_type"] == "l2_topk"
    assert len(orderbook["asks"]) == 3
    assert len(orderbook["bids"]) == 3
    assert orderbook["snapshot"] == True
    assert orderbook["timestamp"] == 1651122265861
    assert orderbook["seq_id"] == 1437010882721
    assert orderbook["prev_seq_id"] == 1437010873329
    assert orderbook["bids"][0][0] == 2886.71
    assert orderbook["bids"][0][3] == 0.454
    assert orderbook["asks"][0][0] == 2886.72
    assert orderbook["asks"][0][3] == 77.215


def test_parse_bbo():
    json_arr = parse_bbo(
        "binance",
        MarketType["linear_swap"],
        '{"stream":"ethusdt@bookTicker","data":{"e":"bookTicker","u":1553413152520,"s":"ETHUSDT","b":"1778.54","B":"15.164","a":"1778.55","A":"7.289","T":1653817855284,"E":1653817855289}}',
    )
    assert len(json_arr) == 1
    bbo_msg = json_arr[0]
    assert bbo_msg["exchange"] == "binance"
    assert bbo_msg["market_type"] == "linear_swap"
    assert bbo_msg["msg_type"] == "bbo"
    assert bbo_msg["symbol"] == "ETHUSDT"
    assert bbo_msg["timestamp"] == 1653817855289
    assert bbo_msg["id"] == 1553413152520

    assert bbo_msg["ask_price"] == 1778.55
    assert bbo_msg["ask_quantity_base"] == 7.289
    assert bbo_msg["ask_quantity_quote"] == 1778.55 * 7.289
    assert bbo_msg["ask_quantity_contract"] == 7.289

    assert bbo_msg["bid_price"] == 1778.54
    assert bbo_msg["bid_quantity_base"] == 15.164
    assert bbo_msg["bid_quantity_quote"] == 1778.54 * 15.164
    assert bbo_msg["bid_quantity_contract"] == 15.164


def test_parse_funding_rate():
    json_arr = parse_funding_rate(
        "binance",
        MarketType["inverse_swap"],
        '{"stream":"btcusd_perp@markPrice","data":{"e":"markPriceUpdate","E":1617309477000,"s":"BTCUSD_PERP","p":"59012.56007222","P":"58896.00503145","r":"0.00073689","T":1617321600000}}',
    )
    assert len(json_arr) == 1
    rate = json_arr[0]
    assert rate["exchange"] == "binance"
    assert rate["market_type"] == "inverse_swap"
    assert rate["msg_type"] == "funding_rate"
    assert rate["pair"] == "BTC/USD"
    assert rate["funding_rate"] == 0.00073689
    assert rate["funding_time"] == 1617321600000


def test_parse_candlestick():
    json_arr = parse_candlestick(
        "binance",
        MarketType["linear_swap"],
        '{"stream":"btcusdt@kline_1M","data":{"e":"kline","E":1653819041520,"s":"BTCUSDT","k":{"t":1651363200000,"T":1654041599999,"s":"BTCUSDT","i":"1M","f":2172726276,"L":2301806561,"o":"37614.40","c":"29075.50","h":"40071.70","l":"26631.00","v":"13431981.671","n":129025447,"x":false,"q":"423075730671.12853","V":"6700065.176","Q":"211000435586.65000","B":"0"}}}',
    )
    assert len(json_arr) == 1
    candlestick_msg = json_arr[0]
    assert candlestick_msg["exchange"] == "binance"
    assert candlestick_msg["market_type"] == "linear_swap"
    assert candlestick_msg["msg_type"] == "candlestick"
    assert candlestick_msg["symbol"] == "BTCUSDT"
    assert candlestick_msg["timestamp"] == 1653819041520
    assert candlestick_msg["period"] == "1M"
    assert candlestick_msg["begin_time"] == 1651363200

    assert candlestick_msg["open"] == 37614.40
    assert candlestick_msg["high"] == 40071.70
    assert candlestick_msg["low"] == 26631.0
    assert candlestick_msg["close"] == 29075.5
    assert candlestick_msg["volume"] == 13431981.671
    assert candlestick_msg["quote_volume"] == 423075730671.12853
