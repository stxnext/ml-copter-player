import itertools
import math
import random

from settings import config


def prepare_params(seed, length):
    try:
        seed = int(seed)
    except (ValueError, TypeError):
        seed = random.randint(1, 999999)

    try:
        length = int(length)
    except (ValueError, TypeError):
        length = random.randint(200, 2000)

    return seed, length


def generate_section_params():
    return (
        random.randint(config.STEEPNESS_MIN, config.STEEPNESS_MAX),
        random.randint(config.SECTION_LENGTH_MIN, config.SECTION_LENGTH_MAX),
        random.randint(config.SPACE_MIN, config.SPACE_MAX)
    )


def generate_map(seed, length, rows):
    seed, length = prepare_params(seed, length)
    random.seed(seed)

    path_center = rows // 2
    direction = 1
    data = [[config.WALL] for i in range(rows)]
    full_length = 0

    while full_length < length:
        steepness, section_length, space = generate_section_params()

        direction, path_center, section_data = generate_section(
            steepness, section_length, space, rows, direction, path_center
        )

        extend_map(data, section_data)
        full_length += section_length

    return data


def preetify_map(data):
    # PREETY SPRITES
    no_of_columns = len(data[0])
    no_of_rows = len(data)

    for column_idx in range(no_of_columns):
        painted = [False for row_idx in range(no_of_rows)]
        # Paint top section
        for row_idx in range(no_of_rows):
            if data[row_idx][column_idx]:
                data[row_idx][column_idx] = config.TOP_WALL
                painted[row_idx] = True
            else:
                if row_idx - 1 >= 0:
                    data[row_idx - 1][column_idx] = config.TOP_WALL_BOTTOM
                break
        # Paint bottom section
        for row_idx in reversed(range(no_of_rows)):
            if data[row_idx][column_idx]:
                data[row_idx][column_idx] = config.BOTTOM_WALL
                painted[row_idx] = True
            else:
                if row_idx + 1 < no_of_rows:
                    data[row_idx + 1][column_idx] = config.BOTTOM_WALL_TOP
                    # Put random small object
                    if random.randint(0, config.SMALL_OBJECT_CHANCE) == 0:
                        data[row_idx][column_idx] = random.choice(
                            config.SMALL_OBJECTS
                        )
                        painted[row_idx] = True
                break
        # Paint anything in the middle
        for row_idx in range(no_of_rows):
            if not data[row_idx][column_idx]:
                # empty cell
                continue
            if painted[row_idx]:
                # already marked as top or bottom
                continue
            data[row_idx][column_idx] = config.MIDDLE_WALL


FINISH_TUNNEL_LENGTH = 50


def add_finish_line(data):
    no_of_columns = len(data[0])
    last_col_idx = no_of_columns - 1
    no_of_rows = len(data)
    column = [config.EMPTY for _ in range(no_of_columns)]

    # Build how a straight tunnel should look like
    for row_idx in range(no_of_rows):
        if data[row_idx][last_col_idx] in config.WALLS:
            column[row_idx] = config.TOP_WALL
        else:
            column[row_idx - 1] = config.TOP_WALL_BOTTOM
            break
    for row_idx in reversed(range(no_of_rows)):
        if data[row_idx][last_col_idx] in config.WALLS:
            column[row_idx] = config.BOTTOM_WALL
        else:
            column[row_idx + 1] = config.BOTTOM_WALL_TOP
            break

    # Repeat the straight section column
    for _ in range(FINISH_TUNNEL_LENGTH):
        for row_idx in range(no_of_rows):
            data[row_idx].append(column[row_idx])

    # Insert exit column
    exit_column = [cell if cell else config.FINISH for cell in column]
    for row_idx in range(no_of_rows):
            data[row_idx].append(exit_column[row_idx])

    # Repeat straight tunnel a bit more
    for _ in range(2):
        for row_idx in range(no_of_rows):
            data[row_idx].append(column[row_idx])


def extend_map(current_map, new_section):
    for i, row in enumerate(current_map):
        row.extend(new_section[i])


def generate_section(steepness, length, space, rows, direction, path_center):
    data = [[] for i in range(rows)]
    switched = None
    direction *= -1
    min_row = 1
    max_row = rows - 1

    for col in range(length):
        half_space = space // 2
        top_block = path_center - half_space
        bottom_block = path_center + half_space

        for row in range(rows):
            if row in (0, max_row):
                data[row].append(config.WALL)
            elif row < top_block or row > bottom_block:
                data[row].append(config.WALL)
            else:
                data[row].append(config.EMPTY)

        current_center = math.floor(rows / steepness * col)
        next_center = math.floor(rows / steepness * (col + 1))
        path_center += (current_center - next_center) * direction

        if bottom_block >= max_row and switched != 'up':
            direction, switched = 1, 'up'

        if top_block <= min_row and switched != 'down':
            direction, switched = -1, 'down'

    data = add_obstacles(data, length, space, rows)

    return direction, path_center, data


def add_obstacles(data, length, space, rows):
    if space < 9:
        return data
    elif space < 15:
        obstacle = random.choice(config.NARROW_OBSTACLES_TYPES)
    else:
        obstacle = random.choice(
            config.OBSTACLES_TYPES
        )

    if obstacle == 'point':
        return add_point_obstacle(data, length, space, rows)
    elif obstacle == 'stalactite':
        return add_stalactite_obstacle(data, length, space, rows)
    elif obstacle == 'junction':
        return add_junction_obstacle(data, length, space, rows)
    elif obstacle == 'deadend':
        return add_deadend_obstacle(data, length, space, rows)


def add_point_obstacle(data, length, space, rows):
    distance = random.randint(8, 14)

    for col in range(distance, length, distance):
        clear_path = get_clear_path_indices(data, rows, col)

        possible_space = clear_path[3:-3]
        if not possible_space:
            continue

        row = random.choice(possible_space)

        if space <= 12:
            data[row][col] = config.WALL
        else:
            for i, j in itertools.product([0, 1], [0, 1]):
                try:
                    data[row + i][col + j] = config.WALL
                except IndexError:
                    pass

    return data


def add_stalactite_obstacle(data, length, space, rows):
    distance = random.randint(12, 18)

    for col in range(distance, length, distance):
        clear_path = get_clear_path_indices(data, rows, col)

        possible_space = clear_path[7:-7]
        if not possible_space:
            continue

        row = random.choice(possible_space)
        direction = random.randint(0, 1)

        for k in clear_path:
            if direction and k <= row:
                data[k][col] = config.WALL
            elif not direction and k >= row:
                data[k][col] = config.WALL

    return data


def add_junction_obstacle(data, length, space, rows):
    distance = 4

    for col in range(distance, length - distance):
        clear_path = get_clear_path_indices(data, rows, col)

        middle = clear_path[len(clear_path) // 2]

        for x in clear_path:
            if x == middle:
                data[x][col] = config.WALL
    return data


def add_deadend_obstacle(data, length, space, rows):
    distance = 8
    depth = random.randint(6, 9)
    direction = random.randint(0, 1)
    start = 0

    if length - (distance + depth) <= distance:
        start_distance = distance
    else:
        start_distance = random.randint(distance, length - (distance + depth))

    for col in range(start_distance, length - distance):
        clear_path = get_clear_path_indices(data, rows, col)
        middle = clear_path[len(clear_path) // 2]

        for x in clear_path:
            if x == middle:
                data[x][col] = config.WALL

        if start == depth:
            for k in clear_path:
                if direction and k <= middle:
                    data[k][col] = config.WALL
                elif not direction and k >= middle:
                    data[k][col] = config.WALL
            break

        start += 1

    return data


def get_clear_path_indices(data, rows, col):
    return [i for i in range(rows) if data[i][col] is config.EMPTY]
