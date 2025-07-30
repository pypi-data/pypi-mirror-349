import base64
import re


alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def _b64(b: bytes) -> str:
    return base64.b64encode(b).rstrip(b'=').decode('ascii')


def _tail(buf: bytes, shift: int) -> str:
    m = (len(buf) + shift) % 3
    if m == 0:
        return alphabet[buf[-1] & 0x3F]
    if m == 1:
        x = (buf[-1] & 0x03) << 4
        return f'[{"".join(alphabet[x | n] for n in range(0x10))}]?'
    x = (buf[-1] & 0x0F) << 2
    return f'[{"".join(alphabet[x | n] for n in range(0x04))}]'


def _shift0(buf: bytes) -> str:
    return f'{_b64(buf)[:-1]}{_tail(buf, 0)}'


def _shift1(buf: bytes) -> str:
    x = buf[0] >> 4
    first = ''.join(alphabet[p | x] for p in (0x00, 0x10, 0x20, 0x30))
    rest = _b64(bytes([0, *buf]))[2:-1]
    return f'[{first}]{rest}{_tail(buf, 1)}'


def _shift2(buf: bytes) -> str:
    x = buf[0] >> 6
    first = ''.join(alphabet[p | x] for p in (0x00, 0x04, 0x08, 0x0C, 0x10, 0x14, 0x18, 0x1C, 0x20, 0x24, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C))
    rest = _b64(bytes([0, 0, *buf]))[3:-1]
    return f'[{first}]{rest}{_tail(buf, 2)}'


def base64_re(buf: bytes, *, binary: bool = False, compile: bool = True) -> bytes | str | re.Pattern[bytes] | re.Pattern[str]:  # noqa: A002
    pat = f'{_shift0(buf)}|{_shift1(buf)}|{_shift2(buf)}'
    if binary:
        pat = pat.encode()
    if compile:
        pat = re.compile(pat)
    return pat
