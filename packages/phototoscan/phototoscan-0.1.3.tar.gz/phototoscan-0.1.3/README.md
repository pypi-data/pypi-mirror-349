# PhotoToScan

A Python library that converts casual document snapshots into professional-quality scanned documents.

This project makes use of the [OpenCV-Document-Scanner](https://github.com/andrewdcampbell/OpenCV-Document-Scanner) from [@andrewdcampbell](https://github.com/andrewdcampbell) and [@joaofauvel](https://github.com/joaofauvel), and the transform and imutils modules from [@PyImageSearch](https://github.com/PyImageSearch) (which can be accessed [here](http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/)).

## Environment

### [uv](https://github.com/astral-sh/uv) - An extremely fast Python package and project manager, written in Rust.

## Installation

```
pip install phototoscan
```

## How To Use It

### As a library

#### Examples

```python
from phototoscan import Scanner, OutputFormat, ScanMode
scanner = Scanner()

# Basic usage with file path
result = scanner.scan(
    img_input="path/to/image.jpg",
    output_format=OutputFormat.PATH_STR,
    output_dir="path/to/output",  # optional
    scan_mode=ScanMode.GRAYSCALE  # optional, defaults to GRAYSCALE
)

# Advanced usage with various input and output types
# 1. From file path to file path string
path_str = scanner.scan(
    img_input="path/to/image.jpg",
    output_format=OutputFormat.PATH_STR,
    scan_mode=ScanMode.COLOR  # Use color mode instead of default grayscale
)

# 2. From file path to Path object
path_obj = scanner.scan(
    img_input="path/to/image.jpg",
    output_format=OutputFormat.FILE_PATH
)

# 3. From numpy array to bytes
bytes_data = scanner.scan(
    img_input=numpy_array,
    output_format=OutputFormat.BYTES,
    ext=".jpg"  # required when input is numpy array and output is bytes
)

# 4. From bytes to numpy array
np_array = scanner.scan(
    img_input=image_bytes,
    output_format=OutputFormat.NP_ARRAY
)
```

#### Parameters:

- `img_input`: Can be a file path (str/Path), bytes/bytearray, or numpy array
- `output_format`: Determines the return type (OutputFormat.PATH_STR, OutputFormat.FILE_PATH, OutputFormat.BYTES, or OutputFormat.NP_ARRAY)
- `scan_mode`: Optional. Determines the output style (ScanMode.COLOR or ScanMode.GRAYSCALE). Defaults to GRAYSCALE
- `output_dir`: Optional. Directory to save the output (required for file outputs when input is numpy array)
- `output_filename`: Optional. Name for the output file (required for file outputs when input isn't a file path)
- `ext`: Optional. File extension for output (required for bytes output when input is numpy array)

#### Notes:

- When providing a file path as input and not specifying an output directory, a folder named "output" will be created at the same level as the input image.
- Any specified output directory that doesn't exist will be created automatically.

### As a command-line tool

#### To scan a single image:

```bash
uvx phototoscan --image <IMG_PATH> --output-dir <OUTPUT_DIR> --scan-mode <MODE>
```

- `--output-dir` is optional.

  - If not provided, a directory named output will be created next to the image file.
  - If the specified directory does not exist, it will be created automatically.

- `--scan-mode` is optional. Can be either `color` or `grayscale` (default is `grayscale`).

#### Scan all images in a directory

```bash
uvx phototoscan --images <IMG_DIR> --output-dir <OUTPUT_DIR> --scan-mode <MODE>
```

- The same rules apply for `--output-dir` and `--scan-mode` as above.
