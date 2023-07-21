from PIL import ImageGrab
import matplotlib.pyplot as plt
import argparse


def take_screenshot(bbox):
    print(list(map(int, bbox)))
    image = ImageGrab.grab(bbox=list(map(int, bbox)))
    image.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', "--bbox", nargs='+', required=True, help="bbox coordinates")
    args = parser.parse_args()
    take_screenshot(args.bbox)