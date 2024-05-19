import pytest

from furniture_plan_analyzer import is_valid_position, count_chairs_in_room, map_rooms_and_count_chairs

# Sample data for tests
floor_plan = ['+-----+', '|(a) W|', '+-----+']
already_visited = set()


def test_is_valid_position():
    """
    Test the is_valid_position() function with different arguments.

    Checks if the function correctly identifies valid and invalid positions in the plan.
    """
    # Test valid position
    assert is_valid_position((1, 4), floor_plan, already_visited, 'W') == True
    assert is_valid_position((0, 0), floor_plan, already_visited, '+') == False
    assert is_valid_position((1, 1), floor_plan, already_visited, '(') == False


def test_count_chairs_in_room():
    """
    Test the count_chairs_in_room() function.

    Checks if the function returns a dictionary and verifies that the counts for different chair types are correct.
    """
    chair_counts = count_chairs_in_room((1, 4), floor_plan, already_visited)
    # Test count_chairs_in_room returns a dict
    assert isinstance(chair_counts, dict)
    # Test dict returned has correct counts
    assert chair_counts == {'W': 1, 'P': 0, 'S': 0, 'C': 0}


def test_map_rooms_and_count_chairs(tmpdir):
    """
    Test the map_rooms_and_count_chairs() function.

    Creates a temporary .txt file with a defined floor plan, then checks if the function correctly maps the rooms and
    counts the chairs by room.
    """
    # Create a temporary txt file
    p = tmpdir.mkdir("sub").join("rooms.txt")
    p.write('+--------+\n|(a) W C S |\n|     P    |\n+--------+\n')
    # Test map_rooms_and_count_chairs returns a dict
    room_chair_counts = map_rooms_and_count_chairs(p)
    assert isinstance(room_chair_counts, dict)
    # Test dict returned has correct counts
    assert room_chair_counts == {'a': {'W': 1, 'P': 1, 'S': 1, 'C': 1}}


if __name__ == "__main__":
    pytest.main()