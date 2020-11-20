

import codecs
from typing import Tuple


def decode_addr(addr: Tuple[bytes]) -> Tuple[str]:
    return tuple([val.decode() for val in addr])


def encode_im920(data: bytes) -> bytes:
    return codecs.encode(data, "hex_codec")
