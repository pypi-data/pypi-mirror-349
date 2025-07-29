import argparse
import os

from phototoscan.scanner import Scanner

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--images", help="Directory of images to be scanned")
    group.add_argument("--image", help="Path to single image to be scanned")
    parser.add_argument("--output-dir", type=str, help="Output directory for the scanned images")

    args = vars(parser.parse_args())
    im_dir = args["images"]
    im_file_path = args["image"]
    output_dir = args["output_dir"]

    scanner = Scanner()

    valid_formats = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif"]

    get_ext = lambda f: os.path.splitext(f)[1].lower()

    # Scan single image specified by command line argument --image <IMAGE_PATH>
    if im_file_path:
        scanner.scan(im_file_path, output_dir=output_dir)

    # Scan all valid images in directory specified by command line argument --images <IMAGE_DIR>
    else:
        im_files = [f for f in os.listdir(im_dir) if get_ext(f) in valid_formats]
        for im in im_files:
            scanner.scan(im_dir + '/' + im, output_dir=output_dir)

if __name__ == "__main__":
    main()