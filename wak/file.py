import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class File:
    file_offset: int
    file_length: int
    filename: str
    file_contents: bytes

    @classmethod
    def from_construct(cls, container, file_contents) -> 'File':
        return File(
            file_offset=container.file_offset,
            file_length=container.file_length,
            filename=container.filename,
            file_contents=file_contents,
        )

    def extract(self, output_root: str):
        target_path = os.path.join(output_root, self.filename)

        Path(target_path).parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "wb") as f:
            f.write(bytearray(self.file_contents))
