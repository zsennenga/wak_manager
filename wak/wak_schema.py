from construct import *


class WakSchema:
    @classmethod
    def header_schema(cls) -> Struct:
        return Struct(
            "unknown1" / Int32ul,
            "file_count" / Int32ul,
            "files_start_offset" / Int32ul,
            "unknown2" / Int32ul,
        )

    @classmethod
    def file_table_schema(cls) -> Struct:
        return Struct(
            "file_offset" / Int32ul,
            "file_length" / Int32ul,
            "filename" / PascalString(Int32ul, "utf8"),
        )
    # TOO SLOWWWWWWW
    # @classmethod
    # def files_schema(cls) -> Struct:
    #    return cls.file_table_schema() + Struct(
    #        #"file" / Pointer(this.file_offset, Byte[this.file_length])
    #    )
