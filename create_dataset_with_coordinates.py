"""
creates a dataset of image pairs using given coordinates and their neighbors.
Run this file with "google-earth-pro & python3 create_dataset_with_coordinates.py" command
"""
import json
import argparse

from get_set_of_changed_images import get_screenshots, METADATA_JSON


def generate_dataset(coordinate_path: str, destination: str, step_height: float, step_width: float):
    """generates a dataset of image pairs using given coordinates and their neighbors

    Args:
        coordinate_path (str): path of the file with box coordinates
        destination (str): path of the destination directory
        step_height (float): step between two consequtive images in height
        step_width (float): step between two consequtive images in width
    """
    with open(coordinate_path, 'r',  encoding='UTF-8') as file:
        lines = file.readlines()

    for line in lines:
        box_coordinate = eval(line)
        get_screenshots(destination, box_coordinate, step_height, step_width)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    with open(METADATA_JSON, 'r', encoding='UTF-8') as fin:
        metadata = json.load(fin)
        parser.set_defaults(**metadata)
    args = parser.parse_args()
    generate_dataset(args.coordinate_path, args.destination, args.step_height, args.step_width)


