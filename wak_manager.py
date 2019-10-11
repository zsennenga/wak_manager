import click

from wak.wak_file import WakFile


@click.command()
@click.option(
    "--mode",
    type=click.Choice(['extract', 'pack', 'append'], case_sensitive=False),
    help="Extract: Read target_wak, output contents to target_directory\n"
         "Pack: load all files in target_directory, write to target_wak\n"
         "Append: load all files in target_directory, add them to the wak, then resave it as target_wak"
)
@click.option("--target_wak", help="Wak file to read or write to")
@click.option("--target_directory", help="Directory to write to or read from, depending on mode")
def main(mode, target_wak, target_directory):
    mode = mode.lower()
    if mode == "extract":
        wak_file = WakFile.from_encrypted_file(target_wak)

        wak_file.extract(target_directory)
    elif mode == "pack":
        wak_file = WakFile.create_wak_from_directory(target_directory)

        wak_file.save(target_wak)
    elif mode == "append":
        wak_file = WakFile.from_encrypted_file(target_wak)

        wak_file.append_files_in_path(target_directory)

        wak_file.save(target_wak)
    else:
        print(f"Bad mode {mode}")
        exit(1)


if __name__ == "__main__":
    main()
