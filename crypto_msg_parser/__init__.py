import json
import re
from enum import IntEnum
from typing import Dict

from crypto_msg_parser._lowlevel import ffi, lib

# snake case
_pattern = re.compile(r'(?<!^)(?=[A-Z])')

def _snake_case(s: str) -> str:
    return _pattern.sub('_', s).lower()

class MarketType(IntEnum):
    '''Market type.'''
    Spot = lib.Spot
    LinearFuture = lib.LinearFuture
    InverseFuture = lib.InverseFuture
    LinearSwap = lib.LinearSwap
    InverseSwap = lib.InverseSwap

    AmericanOption = lib.AmericanOption
    EuropeanOption = lib.EuropeanOption

    QuantoFuture = lib.QuantoFuture
    QuantoSwap = lib.QuantoSwap

    Move = lib.Move
    BVOL = lib.BVOL

    def __str__(self):
        return _snake_case(self.name)

def parse_trade(
    exchange: str,
    market_type: MarketType,
    msg: str
)-> Dict:
    json_ptr = lib.parse_trade(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        # Copy the data to a python string, then parse the JSON
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)

def parse_l2(
    exchange: str,
    market_type: MarketType,
    msg: str
)-> Dict:
    json_ptr = lib.parse_l2(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)

def parse_funding_rate(
    exchange: str,
    market_type: MarketType,
    msg: str
)-> Dict:
    json_ptr = lib.parse_funding_rate(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        return json.loads(ffi.string(json_ptr).decode('UTF-8'))
    finally:
        lib.deallocate_string(json_ptr)
