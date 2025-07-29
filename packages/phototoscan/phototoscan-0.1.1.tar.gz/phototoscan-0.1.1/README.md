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
from phototoscan import Scanner, OutputFormat
scanner = Scanner()

# Basic usage with file path
result = scanner.scan(
    image_input="path/to/image.jpg",
    output_format=OutputFormat.PATH_STR,
    output_dir="path/to/output"  # optional
)

# Advanced usage with various input and output types
# 1. From file path to file path string
path_str = scanner.scan(
    image_input="path/to/image.jpg",
    output_format=OutputFormat.PATH_STR
)

# 2. From file path to Path object
path_obj = scanner.scan(
    image_input="path/to/image.jpg",
    output_format=OutputFormat.FILE_PATH
)

# 3. From numpy array to bytes
bytes_data = scanner.scan(
    image_input=numpy_array,
    output_format=OutputFormat.BYTES,
    ext=".jpg"  # required when input is numpy array and output is bytes
)

# 4. From bytes to numpy array
np_array = scanner.scan(
    image_input=image_bytes,
    output_format=OutputFormat.NP_ARRAY
)
```

#### Parameters:

- `image_input`: Can be a file path (str/Path), bytes/bytearray, or numpy array
- `output_format`: Determines the return type (OutputFormat.PATH_STR, OutputFormat.FILE_PATH, OutputFormat.BYTES, or OutputFormat.NP_ARRAY)
- `output_dir`: Optional. Directory to save the output (required for file outputs when input is numpy array)
- `output_filename`: Optional. Name for the output file (required for file outputs when input isn't a file path)
- `ext`: Optional. File extension for output (required for bytes output when input is numpy array)

#### Notes:

- When providing a file path as input and not specifying an output directory, a folder named "output" will be created at the same level as the input image.
- Any specified output directory that doesn't exist will be created automatically.

### As a command-line tool

#### To scan a single image:

```bash
uvx phototoscan --image <IMG_PATH> --output-dir <OUTPUT_DIR>
```

- --output-dir is optional.

- If not provided, a directory named output will be created next to the image file.

- If the specified directory does not exist, it will be created automatically.

#### Scan all images in a directory

```bash
uvx phototoscan --images <IMG_DIR> --output-dir <OUTPUT_DIR>
```

- The same rules apply for --output-dir as above.
