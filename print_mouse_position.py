from pynput.mouse import Button, Controller
import time


def print_mouse_position():

    mouse = Controller()

    starttime = time.monotonic()
    while True:
        print(f'The current pointer position is {mouse.position}')
        time.sleep(3.0 - ((time.monotonic() - starttime) % 3.0))

    


if __name__ == "__main__":
    print_mouse_position()