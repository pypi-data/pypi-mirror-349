import argparse
import base64
from collections.abc import Iterator
import logging

from base64_regex import base64_re


logger = logging.getLogger(__name__)


def permutations(buf: bytes) -> Iterator[bytes]:
    yield buf
    for prefix_len in range(1, 4):
        for prefix_char in range(0x100):
            yield bytes([prefix_char] * prefix_len) + buf
            for postfix_len in range(1, 4):
                for postfix_char in range(0x100):
                    yield (bytes([prefix_char] * prefix_len) + buf + bytes([postfix_char] * postfix_len))


def test(buf: bytes, *, fail_fast: bool = False) -> bool:
    pat = base64_re(buf)
    logger.info('Test pattern: %r', pat)

    misses = 0
    for n, b in enumerate(permutations(buf), 1):
        if not pat.search(s := base64.b64encode(b).decode()):
            misses += 1
            logger.debug('#%06d %r => %s: MISS #%d', n, b, s, misses)
            if fail_fast:
                break
            continue
        logger.debug('#%06d %r => %s: OK', n, b, s)

    if misses:
        logger.warning('Missed %d out of %d (%.2f%)', misses, n, misses / n * 100)
    else:
        logger.warning('All OK (%d total)', n)

    return not misses


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--fail-fast', '--ff', action='store_true')
    p.add_argument('-v', '--verbose', action='count', default=0)
    p.add_argument('-q', '--quiet', action='store_true')
    p.add_argument('text', type=str.encode, nargs='*', default=[b'asdf'])
    args = p.parse_args()

    if args.quiet:
        log_level = logging.ERROR
    elif not args.verbose:
        log_level = logging.WARNING
    elif args.verbose >= 2:  # noqa: PLR2004
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, format='%(message)s')

    failed = False
    for buf in args.text:
        failed = not test(buf, fail_fast=args.fail_fast)
        if failed and args.fail_fast:
            break

    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
