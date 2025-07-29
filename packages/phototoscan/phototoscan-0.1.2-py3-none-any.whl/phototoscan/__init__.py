import argparse
from pathlib import Path

from phototoscan.scanner import Scanner, OutputFormat, ScanningMode

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--images", help="Directory of images to be scanned")
    group.add_argument("--image", help="Path to single image to be scanned")
    parser.add_argument("--scanning-mode", type=str, choices=["color", "grayscale"], default="grayscale", help="Scanning mode")
    parser.add_argument("--output-dir", type=str, help="Output directory for the scanned images")

    args = vars(parser.parse_args())
    im_dir = args["images"]
    im_file_path = args["image"]
    scanning_mode = ScanningMode.COLOR if args["scanning_mode"] == "color" else ScanningMode.GRAYSCALE
    output_dir = args["output_dir"]

    scanner = Scanner()

    valid_formats = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"]

    get_ext = lambda f: Path(f).suffix.lower()

    # Scan single image specified by command line argument --image <IMAGE_PATH>
    if im_file_path:
        f = Path(im_file_path)
        scanner.scan(f, output_format=OutputFormat.FILE_PATH, scanning_mode=scanning_mode, output_filename=f.name, output_dir=output_dir)
    # Scan all valid images in directory specified by command line argument --images <IMAGE_DIR>
    else:
        im_dir = Path(im_dir)
        if output_dir is not None:
            output_dir = Path(output_dir)
        for f in im_dir.iterdir():
            if f.is_file() and get_ext(f) in valid_formats:
                scanner.scan(
                    f,
                    output_format=OutputFormat.FILE_PATH,
                    scanning_mode=scanning_mode,
                    output_filename=f.name,
                    output_dir=output_dir
                )
                print("Processed " + f.name)

if __name__ == "__main__":
    main()