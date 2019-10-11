# Wak Manager

Utility for manipulating wak files for Noita

Requires a recent python, probably 3.7

## Usage


### Extract

Takes all the files out of the wak

```
python3 wak_manager.py --mode=extract --target_wak=<path_to_wak> --target_directory=<output dir>
```

### Pack

Puts all the files in the wak

```
python3 wak_manager.py --mode=pack --target_wak=<path_to_output_wak> --target_directory=<input dir>
```

### Append

Adds files to the wak from the target directory

Overwriting files isn't really a thing yet. May never be.

```
python3 wak_manager.py --mode=append --target_wak=<path_to_wak> --target_directory=<input dir>
```
