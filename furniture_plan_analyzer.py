# Import necessary libraries
import argparse
import os
from collections import deque
from typing import List, Tuple, Dict, Set

# Directions are represented as tuples: Up, Right, Down, Left
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Chair types are represented as a List of characters
CHAIR_TYPES = ['W', 'P', 'S', 'C']

# Aggregate Chair types
CHAIR_TYPES_STRING = ''.join(CHAIR_TYPES)


def get_parsed_arguments():
    """
    Parses command-line arguments for a tool to count chairs by room type from a given floor plan.

    This function uses Python's argparse module to parse command-line arguments. It expects one argument:
    '-f' or '--floor_plan_file_path', which should be the path to the floor plan file as a string.

    Returns
    -------
    argparse.Namespace
        The parsed command-line arguments, accessible as properties on an object.
    """
    # Define an ArgumentParser object for command line arguments
    argument_parser = argparse.ArgumentParser(description='Tool to count chairs by room type from a given floor plan.')
    # Add the path to the floor plan file as a command-line argument
    argument_parser.add_argument('-f', '--floor_plan_file_path', type=str, help='Path to the floor plan file')
    # Parse the provided command-line arguments
    args = argument_parser.parse_args()
    return args


def is_valid_position(new_position: Tuple[int, int], floor_plan: List[str],
                      already_visited: Set[Tuple[int, int]], chair_type: str) -> bool:
    """
    Validates if a position is valid in the given floor plan and has not yet been visited.

    Parameters
    ----------
    new_position : tuple
        A tuple (x, y) representing the position to be validated.
    floor_plan : list of string
        A 2D list representing the floor plan.
    already_visited : set of tuples
        A set of tuples representing the positions that have been visited.
    chair_type : str
        A string representing the type of chair.

    Returns
    -------
    bool
        True if the position is valid; False otherwise.
    """
    return 0 <= new_position[0] < len(floor_plan) and 0 <= new_position[1] < len(
        floor_plan[0]) and new_position not in already_visited and chair_type in CHAIR_TYPES_STRING + ' '


def count_chairs_in_room(starting_coordinate: Tuple[int, int], floor_plan: List[str],
                         already_visited: Set[Tuple[int, int]]) -> Dict[str, int]:
    """
    Performs a Breadth-first search (BFS) from a given start coordinate in the floor plan to count chair occurrences
    by type and returns a dictionary with chair types as keys and occurrences as values.

    Parameters
    ----------
    starting_coordinate : Tuple[int, int]
        A tuple (x, y) representing the starting coordinate for the BFS.
    floor_plan : List[str]
        A list of strings where each string represents a row in the floor plan.
    already_visited : Set[Tuple[int, int]]
        A set of tuples representing the coordinates that have already been visited.

    Returns
    -------
    Dict[str, int]
        A dictionary where keys are chair types and values are the counts of the chair types.
    """
    # Create a deque for BFS and initialize with the starting coordinate
    search_queue = deque([starting_coordinate])
    # Initialize the chair_counts dictionary to count each type of chair
    chair_counts = {chair: 0 for chair in CHAIR_TYPES}
    while search_queue:
        # Take a position from the front of the queue
        current_position = search_queue.popleft()
        for direction in DIRECTIONS:
            # Calculate the new position based on the current one and the direction
            new_position = current_position[0] + direction[0], current_position[1] + direction[1]
            chair_type = floor_plan[new_position[0]][new_position[1]]
            # If the new position is valid, add it to the queue and add it to visited nodes
            if is_valid_position(new_position, floor_plan, already_visited, chair_type):
                already_visited.add(new_position)
                # If the new position has a chair, increase the count for that chair type
                if chair_type in CHAIR_TYPES:
                    chair_counts[chair_type] += 1
                search_queue.append(new_position)
    # return the count of each type of chair
    return chair_counts


def map_rooms_and_count_chairs(floor_plan_file_path: str) -> Dict[str, Dict[str, int]]:
    """
    Opens a floor plan file and iterates over the characters.
    Identifies rooms by room names surrounded by parentheses and performs BFS to count chairs by room.
    Returns a dictionary with room names as keys and a dictionary of chair counts as values.

    Parameters
    ----------
    floor_plan_file_path : str
        A string representing the path to the floor plan file.

    Returns
    -------
    Dict[str, Dict[str, int]]
        A dictionary where keys are room names and values are dictionaries.
        The inner dictionaries have chair types as keys and their counts as values.
    """
    # Check if the floor_plan_file exists in the system
    if not os.path.isfile(floor_plan_file_path):
        print(f'The file {floor_plan_file_path} does not exist.')
        return {}
    # Open the floor plan file
    with open(floor_plan_file_path, 'r') as file:
        floor_plan_data = file.readlines()
    # Storage for the counts of chairs in each room
    room_chair_counts = {}
    # Keep tracks of the already visited coordinates
    already_visited = set()
    # Iterate over each row, and each character in those rows
    for row_index, row in enumerate(floor_plan_data):
        for column_index, symbol in enumerate(row):
            # For each room represented by '(room_name)', find the chair counts in the room
            if symbol == '(':
                room_name = row[column_index + 1:column_index + row[column_index:].find(')')]
                starting_coordinate = (row_index, column_index + row[column_index:].find(')') + 1)
                room_chair_counts[room_name] = count_chairs_in_room(starting_coordinate, floor_plan_data,
                                                                    already_visited)
    # return the dictionary with room names as keys and a dictionary of chair counts as values
    return room_chair_counts


def print_results(survey_results: Dict[str, Dict[str, int]], chair_counts: Dict[str, int]):
    """
    Prints the room-wise and total chair counts. The print order is first sorted by room name, then by chair type.

    Parameters
    ----------
    survey_results : Dict[str, Dict[str, int]]
        A dictionary where keys are room names and values are dictionaries. The inner dictionaries have chair types
        as keys and counts as values.
    chair_counts : Dict[str, int]
        A dictionary with chair types as keys and the total counts as values.

    Returns
    -------
    None
    """
    print('*' * 50)
    print(f'\n{"Results".center(50, "-")}')
    for room_name, room_survey in sorted(survey_results.items()):
        print(f'\nRoom: {room_name}')
        for chair_type, chair_count in room_survey.items():
            print(f'{chair_type}: {chair_count}', end=', ')
            chair_counts[chair_type] += chair_count
    print(f'\n\n{"Overall Counts".center(50, "-")}\n')
    for chair_type, count in chair_counts.items():
        print(f'{chair_type}: {count}', end=', ')
    print('\n')
    print('*' * 50)


# Python main check to ensure script execution as a script, not as an imported module
if __name__ == '__main__':
    parsed_args = get_parsed_arguments()
    # Count chairs in floor plan for each room
    results = map_rooms_and_count_chairs(parsed_args.floor_plan_file_path)
    # Initialize overall chair counts for summary
    overall_chair_counts = {chair: 0 for chair in CHAIR_TYPES}
    # Print the results
    print_results(results, overall_chair_counts)
