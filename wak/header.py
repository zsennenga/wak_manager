from dataclasses import dataclass


@dataclass
class Header:
    unknown1: int
    file_count: int
    files_start_offset: int
    unknown2: int

    @classmethod
    def from_construct(cls, container) -> 'Header':
        return Header(
            unknown1=container.unknown1,
            file_count=container.file_count,
            files_start_offset=container.files_start_offset,
            unknown2=container.unknown2,
        )
