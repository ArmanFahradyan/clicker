"""Generates pairs of google map images: one in the past, one in the present.
    Run this file with "google-earth-pro & python3 get_set_of_changed_images.py" command
"""
import os
import argparse
import time
import json
from pynput.mouse import Button
import pynput
from pynput.keyboard import Key
import numpy as np
from PIL import ImageGrab


MOUSE_AWAY_POSITION = (1036, 0)  # (40, 550)

HISTORY_BUTTON_POSITION = (423, 94)  # (498, 93)

LEFT_ARROW_POSITION = (245, 153)  # (315, 153)
RIGHT_ARROW_POSITION = (513, 153)  # (587, 153)

UPPER_LEFT_CORNER_POSITION = (225, 186)  # (300, 187) 1502x920, 1500x780
LOWER_RIGHT_CORNER_POSITION = (1725, 966) # (1802, 1107)

ZOOM_IN_POSITION = (1811, 322)  # (1876, 323)
# ZOOM_OUT_POSITION = (1876, 443)

SEARCH_BAR_POSITION = (78, 125)  # (162, 126)
QUIT_SEARCH_BAR_POSITION = (189, 348)  # (263, 346)

METADATA_JSON = "metadata.json"

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()


def check_destination(destination: str):
    """checks if there are all required paths and creates if needed

    Args:
        destination (str): path of the destination directory
    """
    if not os.path.exists(destination):
        os.mkdir(destination)

    for sub_dir in ('A', 'B'):
        if not os.path.exists(os.path.join(destination, sub_dir)):
            os.mkdir(os.path.join(destination, sub_dir))


def parse_coordinates(box_coordinates: list, step_height: float, step_width: float) -> tuple:
    """generates arrays of coordinates from the input information

    Args:
        box_coordinates (list): four coordinates, indicating lower left and 
                                upper right corners of the interesting region of the map
        step_height (float): step between two consequtive images in height
        step_width (float): step between two consequtive images in width

    Returns:
        tuple: two arrays of width and height coordinates
    """

    count_x = int((box_coordinates[3]-box_coordinates[1]) / step_width)
    count_y = int((box_coordinates[2]-box_coordinates[0]) / step_height)

    x_coordinates = np.linspace(box_coordinates[1], box_coordinates[3], count_x, endpoint=True)
    y_coordinates = np.linspace(box_coordinates[0], box_coordinates[2], count_y, endpoint=True)

    return x_coordinates, y_coordinates


def search_coordinate(x: float, y: float, first_search: bool):
    """moves screen to the given coordinates and zooms in

    Args:
        x (float): width coordinate
        y (float): height coordinate
        first_search (bool): flag, indicating whether it is the first search, 
                            because the first one lasts long
    """
    mouse.position = SEARCH_BAR_POSITION
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(0.1)

    coordinate = f"{y}°, {x}°"
    keyboard.type(coordinate)
    time.sleep(0.1)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    if first_search:
        time.sleep(10.0)
    time.sleep(9.0)

    mouse.position = ZOOM_IN_POSITION
    mouse.press(Button.left)
    time.sleep(1.0)
    mouse.release(Button.left)
    time.sleep(2.0)

    mouse.position = QUIT_SEARCH_BAR_POSITION
    time.sleep(1.0)
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1.0)


def screenshot_the_area() -> dict:
    """generates pair of images, one in the past and one in present

    Returns:
        dict: dictionary, containing the pair of images
    """

    images = {}

    images['B'] = ImageGrab.grab(bbox=UPPER_LEFT_CORNER_POSITION + LOWER_RIGHT_CORNER_POSITION)

    mouse.position = HISTORY_BUTTON_POSITION
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1.0)

    mouse.position = LEFT_ARROW_POSITION
    time.sleep(1.0)
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1.0)
    mouse.press(Button.left)
    mouse.release(Button.left)
    mouse.position = MOUSE_AWAY_POSITION
    time.sleep(2.0)

    images['A'] = ImageGrab.grab(bbox=UPPER_LEFT_CORNER_POSITION + LOWER_RIGHT_CORNER_POSITION)

    time.sleep(1.0)

    mouse.position = HISTORY_BUTTON_POSITION
    mouse.press(Button.left)
    mouse.release(Button.left)

    return images


def save_images(images: dict, x: float, y: float, destination: str):
    """saves the image pair in the destination in the appropriate directory

    Args:
        images (dict): dictionary, containing the pair of images
        x (float): width coordinate of the image, needed for the name of the image
        y (float): height coordinate of the image, needed for the name of the image
        destination (str): path of the destination directory
    """

    for sub_dir in ('A', 'B'):
        images[sub_dir].save(os.path.join(destination, sub_dir, f"{y}°, {x}°.png"))


def get_screenshots(destination: str, box_coordinates: list, step_height: float, step_width: float):
    """main function that generates pairs of images of the required coordinates and saves them

    Args:
        destination (str): path of the destination directory
        box_coordinates (list): four coordinates, indicating lower left and 
                                upper right corners of the interesting region of the map
        step_height (float): step between two consequtive images in height
        step_width (float): step between two consequtive images in width
    """

    time.sleep(5.0)

    check_destination(destination)

    box_coordinates = list(map(float, box_coordinates))

    x_coordinates, y_coordinates = parse_coordinates(box_coordinates, step_height, step_width)

    mouse.position = MOUSE_AWAY_POSITION
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1.0)

    first_search = True

    for x in x_coordinates:
        for y in y_coordinates:
            search_coordinate(x, y, first_search)
            first_search = False
            images = screenshot_the_area()
            save_images(images, x, y, destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    with open(METADATA_JSON, 'r', encoding='UTF-8') as fin:
        metadata = json.load(fin)
        parser.set_defaults(**metadata)
    args = parser.parse_args()
    get_screenshots(args.destination, args.box_coordinates, args.step_height, args.step_width)
