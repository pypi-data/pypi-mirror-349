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

```python
from phototoscan import Scanner
scanner = Scanner()
scanner.scan(<IMAGE_PATH>, output_dir=<OUTPUT_DIR>)
```

- output_dir is optional.
- If not specified, a folder named output will be automatically created at the same level as the input image.
- If the specified output directory does not exist, it will be created automatically.

### As a command-line tool

#### To scan a single image:

```bash
uvx phototoscan --image <IMAGE_PATH> --output-dir <OUTPUT_DIR>
```

- --output-dir is optional.

- If not provided, a directory named output will be created next to the image file.

- If the specified directory does not exist, it will be created automatically.

#### Scan all images in a directory

```bash
uvx phototoscan --images <IMAGES_DIR> --output-dir <OUTPUT_DIR>
```

- The same rules apply for --output-dir as above.
