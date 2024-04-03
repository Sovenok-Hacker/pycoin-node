import hashlib
from dataclasses import dataclass
from utils import bigint_to_bytes

@dataclass
class Address:
    ir: int

    @classmethod
    def from_hex(cls, hex_string: str):
        return cls.from_int(ir=int(hex_string, 16))

    @classmethod
    def from_int(cls, ir: int):
        assert ir < 2**512
        return cls(ir=ir)

    @classmethod
    def from_bytes(cls, br: bytes):
        return cls.from_int(ir=int.from_bytes(br, byteorder='big'))

    def to_bytes(self):
        return self.ir.to_bytes(32, byteorder='big')

@dataclass
class Transaction:
    sender: Address
    receiver: Address
    amount: float
    data: bytes
    nonce: int
    signature: bytes

class Block:
    def __init__(self, index: int, timestamp: int, phash: bytes, txs: list[Transaction], miner: Address, pow: int, diff: int, hash: bytes = None):
        self.index = index
        self.timestamp = timestamp
        self.phash = phash
        self.txs = txs
        self.miner = miner
        self.pow = pow
        self.diff = diff
        self.hash = hash
        if self.hash:
            self.hash = self.hash()
    def hash(self) -> bytes:
        self.hash = hashlib.sha256(
            bigint_to_bytes(self.index) +
            bigint_to_bytes(self.timestamp) +
            self.phash +
            self.miner.to_bytes() +
            bigint_to_bytes(self.pow) +
            bigint_to_bytes(self.diff)
        ).digest()
        return self.hash