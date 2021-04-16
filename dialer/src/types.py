import typing

import pjsua

Call = typing.NamedTuple(
    "Call",
    (
        ("call_id", str),
        ("call", pjsua.Call),
        ("msisdn", str),
        ("modem", str),
        ("account", str),
        ("call_endpoint", pjsua.Account),
        ("modem_endpoint", pjsua.Account),
    ),
)
