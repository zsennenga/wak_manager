import os
from dataclasses import dataclass
from typing import List

from crypto.crypto_wrapper import CryptoWrapper
from wak.file import File
from wak.header import Header
from wak.wak_schema import WakSchema


@dataclass
class WakFile:
    header: Header
    files: List[File]
    size: int

    @classmethod
    def get_relative_paths_for_files_in_folder(cls, target_directory):
        file_set = set()

        for dir_, _, files in os.walk(target_directory):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, target_directory)
                rel_file = os.path.join(rel_dir, file_name)
                file_set.add(rel_file)

        return file_set

    @classmethod
    def _decrypt_bytes(cls, encrypted_bytes) -> bytes:
        decrypted_header = CryptoWrapper.build_for_header().decrypt(encrypted_bytes[:16])

        parsed_header = WakSchema.header_schema().parse(decrypted_header)

        file_count = parsed_header.file_count
        files_start_offset = parsed_header.files_start_offset

        decrypted_file_table = CryptoWrapper.build_for_file_table().decrypt(encrypted_bytes[16:files_start_offset])

        file_table = WakSchema.file_table_schema()[file_count].parse(decrypted_file_table)

        decrypted_files = bytearray()

        progress_counter = 1

        for (i, file) in enumerate(file_table):
            percent_completion = (i + 1) / file_count
            target_progress = .25 * progress_counter
            if percent_completion >= target_progress:
                progress_counter += 1
                print(f"{100 * target_progress}% decryption complete!")

            encrypted_file_bytes = encrypted_bytes[file.file_offset: file.file_offset + file.file_length]

            decrypted_files += CryptoWrapper.build_for_file(i).decrypt(encrypted_file_bytes)

        return decrypted_header + decrypted_file_table + decrypted_files

    @classmethod
    def from_encrypted_bytes(cls, encrypted_bytes: bytes) -> 'WakFile':
        print("Decrypting data...")
        as_bytes = memoryview(cls._decrypt_bytes(encrypted_bytes))

        header = WakSchema.header_schema().parse(as_bytes[:16])
        file_table = WakSchema.file_table_schema()[header.file_count].parse(as_bytes[16:header.files_start_offset])

        return WakFile(
            header=Header.from_construct(header),
            files=[
                File.from_construct(
                    file,
                    as_bytes[file.file_offset:file.file_offset + file.file_length]
                )
                for file in file_table
            ],
            size=len(as_bytes)
        )

    @classmethod
    def from_encrypted_file(cls, filename: str) -> 'WakFile':
        print("Loading file...")
        with open(filename, 'rb') as f:
            encrypted_bytes = f.read()

        return cls.from_encrypted_bytes(encrypted_bytes)

    def extract(self, output_root: str):
        file_count = self.header.file_count
        progress_counter = 1
        for (i, file) in enumerate(self.files):
            percent_completion = (i + 1) / file_count
            target_progress = .25 * progress_counter
            if percent_completion >= target_progress:
                progress_counter += 1
                print(f"{100 * target_progress}% extraction complete!")

            file.extract(output_root)

    def add_file(self, relative_path):
        with open(relative_path, "rb") as f:
            new_bytes = f.read()

        filesize = len(new_bytes)

        self.header.file_count += 1
        self.files.append(
            File(
                file_offset=self.size,
                file_length=filesize,
                filename=relative_path,
                file_contents=new_bytes,
            )
        )

        self.size += filesize

    @classmethod
    def create_wak_from_directory(cls, root: str) -> 'WakFile':
        files_in_directory = cls.get_relative_paths_for_files_in_folder(root)  # TODO
        file_count = len(files_in_directory)

        temp_filetable = WakSchema.file_table_schema()[file_count].build(
            [
                {
                    'file_offset': 0,
                    'file_length': 0,
                    'filename': file,
                }
                for file in files_in_directory
            ]
        )

        header_size = 16
        filetable_size = len(temp_filetable)

        files_start_offset = header_size + filetable_size

        header = Header(
            file_count=file_count,
            files_start_offset=files_start_offset,
            unknown1=0,
            unknown2=0,
        )

        files = []

        current_file_end = files_start_offset

        for filename in files_in_directory:
            with open(filename, 'rb') as f:
                file_contents = f.read()
            filesize = len(file_contents)
            files.append(
                File(
                    file_offset=current_file_end,
                    file_length=filesize,
                    filename=filename,
                    file_contents=file_contents,
                )
            )
            current_file_end += filesize

        return WakFile(
            header=header,
            files=files,
            size=current_file_end
        )

    def save(self, target):
        with open(target, "wb") as f:
            bytes_header = WakSchema.header_schema().build(
                {
                    'unknown1': self.header.unknown1,
                    'file_count': self.header.file_count,
                    'files_start_offset': self.header.files_start_offset,
                    'unknown2': self.header.unknown2
                }
            )
            encrypted_header = CryptoWrapper.build_for_header().encrypt(bytes_header)

            bytes_file_table = WakSchema.file_table_schema()[self.header.file_count].build(
                [
                    {
                        'file_offset': file.file_offset,
                        'file_length': file.file_length,
                        'filename': file.filename,
                    }
                    for file in self.files
                ]
            )

            encrypted_file_table = CryptoWrapper.build_for_file_table().encrypt(bytes_file_table)

            encrypted_bytes = bytearray(encrypted_header) + bytearray(encrypted_file_table)

            for (i, file) in enumerate(self.files):
                encrypted_bytes += CryptoWrapper.build_for_file(i).encrypt(file.file_contents)

            f.write(encrypted_bytes)

    def append_files_in_path(self, target_directory):
        files_in_directory = self.get_relative_paths_for_files_in_folder(target_directory)

        for file in files_in_directory:
            self.add_file(file)
