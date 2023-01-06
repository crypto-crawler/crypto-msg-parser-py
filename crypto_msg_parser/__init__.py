import json
from enum import IntEnum
from typing import Any, Dict, List, Optional

from result import Err, Ok, Result

from crypto_msg_parser._lowlevel import ffi, lib


class MarketType(IntEnum):
    """Market type."""

    unknown = lib.Unknown
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


class MessageType(IntEnum):
    """Message type."""

    other = lib.Other
    trade = lib.Trade
    l2_event = lib.L2Event
    l2_snapshot = lib.L2Snapshot
    l2_topk = lib.L2TopK
    l3_event = lib.L3Event
    l3_snapshot = lib.L3Snapshot
    bbo = lib.BBO
    ticker = lib.Ticker
    candlestick = lib.Candlestick
    funding_rate = lib.FundingRate
    open_interest = lib.OpenInterest


def extract_symbol(exchange: str, market_type: MarketType, msg: str) -> Optional[str]:
    json_ptr = lib.extract_symbol(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return None
    try:
        # Copy the data to a python string, then parse the JSON
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)


def extract_timestamp(
    exchange: str, market_type: MarketType, msg: str
) -> Result[Optional[int], str]:
    timestamp: int = lib.extract_timestamp(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if timestamp == 0:
        return Ok(None)
    elif timestamp < 0:
        return Err(f"Failed to parse {msg}")
    else:
        return Ok(timestamp)


def get_msg_type(exchange: str, msg: str) -> MessageType:
    msg_type = lib.get_msg_type(
        ffi.new("char[]", exchange.encode("utf-8")),
        ffi.new("char[]", msg.encode("utf-8")),
    )
    return MessageType(msg_type)


def parse_trade(
    exchange: str, market_type: MarketType, msg: str
) -> List[Dict[str, Any]]:
    json_ptr = lib.parse_trade(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        # Copy the data to a python string, then parse the JSON
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)


def parse_l2(
    exchange: str,
    market_type: MarketType,
    msg: str,
    received_at: Optional[int] = None,
) -> List[Dict[str, Any]]:
    json_ptr = lib.parse_l2(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
        0 if received_at is None else received_at,
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)


def parse_l2_topk(
    exchange: str,
    market_type: MarketType,
    msg: str,
    received_at: Optional[int] = None,
) -> List[Dict[str, Any]]:
    json_ptr = lib.parse_l2_topk(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
        0 if received_at is None else received_at,
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)


def parse_bbo(
    exchange: str,
    market_type: MarketType,
    msg: str,
    received_at: Optional[int] = None,
) -> List[Dict[str, Any]]:
    json_ptr = lib.parse_bbo(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
        0 if received_at is None else received_at,
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)


def parse_candlestick(
    exchange: str,
    market_type: MarketType,
    msg: str,
    received_at: Optional[int] = None,
) -> List[Dict[str, Any]]:
    json_ptr = lib.parse_candlestick(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
        0 if received_at is None else received_at,
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)


def parse_funding_rate(
    exchange: str,
    market_type: MarketType,
    msg: str,
    received_at: Optional[int] = None,
) -> List[Dict[str, Any]]:
    json_ptr = lib.parse_funding_rate(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char[]", msg.encode("utf-8")),
        0 if received_at is None else received_at,
    )
    if json_ptr == ffi.NULL:
        return []
    try:
        return json.loads(ffi.string(json_ptr).decode("UTF-8"))
    finally:
        lib.deallocate_string(json_ptr)
