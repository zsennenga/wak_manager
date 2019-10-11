import numpy as np

from constants import SEED, HEADER_IV, KEY_IV, FILE_TABLE_IV


class PRNG(object):
    def __init__(self, seed: int) -> None:
        self.seed = np.double(np.double(np.uint32(seed)) + np.double(SEED))

        if self.seed >= 2147483647:
            self.seed = self.seed / 2

        self.next_int()

    def next_int(self) -> bytes:
        temp = np.int32(
            np.right_shift(
                np.int64(np.int32(self.seed)) * np.int64(-2092037281), 32
            )
        ) + np.int32(self.seed)

        self.seed = np.double(np.int32(self.seed) * 16807 - (np.right_shift(temp, 16)) * np.iinfo(np.int32).max)

        return np.ndarray.tobytes(
            np.array(
                [
                    np.int32((self.seed / np.double(2147483647.0)) * -2147483648.0)
                ]
            )
        )

    def get(self) -> bytes:
        return bytes([
            byte
            for _ in range(4)
            for byte in self.next_int()
        ])

    @classmethod
    def get_aes_key(cls) -> bytes:
        return PRNG(KEY_IV).get()

    @classmethod
    def get_header_iv(cls) -> bytes:
        return PRNG(HEADER_IV).get()

    @classmethod
    def get_file_table_iv(cls) -> bytes:
        return PRNG(FILE_TABLE_IV).get()

    @classmethod
    def get_file_index_iv(cls, index) -> bytes:
        return PRNG(index).get()
