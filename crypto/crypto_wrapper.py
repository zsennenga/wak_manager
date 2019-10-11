from Crypto.Cipher import AES

from crypto.counter import Counter
from crypto.prng import PRNG


class CryptoWrapper(object):
    def __init__(
            self,
            iv: bytes,
    ):
        self.iv = iv
        self.counter = None
        self.aes = None

    def reset(self):
        self.counter = Counter(self.iv)
        self.aes = AES.new(
            PRNG.get_aes_key(),
            AES.MODE_CTR,
            counter=lambda: self.counter.get()
        )

    @classmethod
    def build_for_header(cls):
        return CryptoWrapper(PRNG.get_header_iv())

    @classmethod
    def build_for_file_table(cls):
        return CryptoWrapper(PRNG.get_file_table_iv())

    @classmethod
    def build_for_file(cls, index: int):
        return CryptoWrapper(PRNG.get_file_index_iv(index))

    def encrypt(self, input_bytes: bytes) -> bytes:
        self.reset()

        return self.aes.encrypt(input_bytes)

    def decrypt(self, input_bytes: bytes) -> bytes:
        self.reset()

        return self.aes.decrypt(input_bytes)
