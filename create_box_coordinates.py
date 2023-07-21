"""
creates box coordinates from input coordinates and 
stores a list of box coordinates of length 2*step_count+1 with center coordinates from the input
"""
import argparse


def create_box_coordinates(source: str, destination: str, step_count: int, step_size: float):
    """creates box coordinates from input coordinates and 
       stores a list of box coordinates of length 2*step_count+1 
       with center coordinates from the input
    Args:
        source (str): path of the source file, containing initial coordinates
        destination (str): path of the destination file, where final box coordinates are stored
        step_count (int): indicates how many steps left, right, down, up should we move from initial coordinates
        step_size (float): indicates size of the step described by the previous argument
    """
    with open(source, 'r',  encoding='UTF-8') as source_file:
        lines = source_file.readlines()

    with open(destination, 'w', encoding='UTF-8') as destination_file:

        for line in lines:
            width_coordinate, height_coordinate = line.split(',')
            width_coordinate = float(width_coordinate)
            height_coordinate = float(height_coordinate)

            width_left = width_coordinate - step_count * step_size
            width_right = width_coordinate + step_count * step_size
            height_down = height_coordinate - step_count * step_size
            height_up = height_coordinate + step_count * step_size

            destination_file.write(f"{[height_down, width_left, height_up, width_right]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--source", type=str, required=True, help="path of the source file, containing initial coordinates")
    parser.add_argument('-d', "--destination", type=str, required=True, help="path of the destination file, where final box coordinates are stored")
    parser.add_argument('-sc', "--step_count", type=int, default=5, help="indicates how many steps left, right, down, up should we move from initial coordinates")
    parser.add_argument('-ss', "--step_size", type=float, default=0.01, help="indicates size of the step described by the previous argument")
    args = parser.parse_args()
    create_box_coordinates(args.source, args.destination, args.step_count, args.step_size)


