import hashlib, time

def sha256_int(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest(), byteorder='big')

def timestamp() -> int:
    return int(time.time())

def bigint_to_bytes(n: int) -> bytes:
    return n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')