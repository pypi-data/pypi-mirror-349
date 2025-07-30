import re
from typing import Literal, assert_type, overload

alphabet: Literal['ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/']

@overload
def base64_re(buf: bytes) -> re.Pattern[str]: ...
@overload
def base64_re(buf: bytes, *, binary: Literal[False] = ...) -> re.Pattern[str]: ...
@overload
def base64_re(buf: bytes, *, binary: Literal[True] = ...) -> re.Pattern[bytes]: ...
@overload
def base64_re(buf: bytes, *, compile: Literal[False] = ...) -> str: ...
@overload
def base64_re(buf: bytes, *, compile: Literal[True] = ...) -> re.Pattern[str]: ...
@overload
def base64_re(buf: bytes, *, binary: Literal[False] = ..., compile: Literal[False] = ...) -> str: ...
@overload
def base64_re(buf: bytes, *, binary: Literal[True] = ..., compile: Literal[False] = ...) -> bytes: ...
@overload
def base64_re(buf: bytes, *, binary: Literal[False] = ..., compile: Literal[True] = ...) -> re.Pattern[str]: ...
@overload
def base64_re(buf: bytes, *, binary: Literal[True] = ..., compile: Literal[True] = ...) -> re.Pattern[bytes]: ...

assert_type(base64_re(b'asdf'), re.Pattern[str])
assert_type(base64_re(b'asdf', binary=False), re.Pattern[str])
assert_type(base64_re(b'asdf', binary=True), re.Pattern[bytes])
assert_type(base64_re(b'asdf', compile=False), str)
assert_type(base64_re(b'asdf', compile=True), re.Pattern[str])
assert_type(base64_re(b'asdf', binary=False, compile=False), str)
assert_type(base64_re(b'asdf', binary=True, compile=False), bytes)
assert_type(base64_re(b'asdf', binary=False, compile=True), re.Pattern[str])
assert_type(base64_re(b'asdf', binary=True, compile=True), re.Pattern[bytes])
