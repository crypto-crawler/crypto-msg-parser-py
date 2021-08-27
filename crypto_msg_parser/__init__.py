import json
from enum import IntEnum
from typing import Any, Dict, List, Optional

from crypto_msg_parser._lowlevel import ffi, lib


class MarketType(IntEnum):
    '''Market type.'''
    spot = lib.Spot
    linear_future = lib.LinearFuture
    inverse_future = lib.InverseFuture
    linear_swap = lib.LinearSwap
    inverse_swap = lib.InverseSwap

    american_option = lib.AmericanOption
    european_option = lib.EuropeanOption

    quanto_future = lib.QuantoFuture
    quanto_swap = lib.QuantoSwap

    move = lib.Move
    bvol = lib.BVOL


def parse_trade(
    exchange: str,
    market_type: MarketType,
    msg: str
)-> List[Dict[str, Any]]:
    json_ptr = lib.parse_trade(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        # Copy the data to a python string, then parse the JSON
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)

def parse_l2(
    exchange: str,
    market_type: MarketType,
    msg: str,
    timestamp: Optional[int] = None,
)-> List[Dict[str, Any]]:
    json_ptr = lib.parse_l2(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
        0 if timestamp is None else timestamp,
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)

def parse_funding_rate(
    exchange: str,
    market_type: MarketType,
    msg: str
)-> List[Dict[str, Any]]:
    json_ptr = lib.parse_funding_rate(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)
