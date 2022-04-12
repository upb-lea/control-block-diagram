from ..points import Point


def generate_connection(p1, p2, space_x, space_y, start_direction=None, end_direction=None):
    """Function that generates a list of points for a connection between two points"""

    start_direction = get_start_direction(p1, p2) if start_direction is None else start_direction
    end_direction = get_end_direction(p1, p2) if end_direction is None else end_direction
    directions = start_direction + '_' + end_direction
    return connection_reader[directions](p1, p2, space_x, space_y)


def get_start_direction(p1: Point, p2: Point) -> str:
    """Calculate the starting direction of a connection"""
    if p1.direction:
        return p1.direction
    elif p1.x == p2.x:
        if p1.y < p2.y:
            return 'north'
        else:
            return 'south'
    elif p1.x < p2.x:
        return 'east'
    else:
        return 'west'


def get_end_direction(p1: Point, p2: Point) -> str:
    """Calculate the ending direction of a connection"""
    if p2.direction:
        return p2.direction
    elif p1.x == p2.x:
        if p1.y < p2.y:
            return 'south'
        else:
            return 'north'
    elif p1.x < p2.x:
        return 'west'
    else:
        return 'east'


def get_mid_x(p1: Point, p2: Point) -> float:
    """Calculate the middle of the x-direction of to points"""
    return (p1.x + p2.x) / 2


def get_mid_y(p1: Point, p2: Point) -> float:
    """Calculate the middle of the y-direction of to points"""
    return (p1.y + p2.y) / 2


def west_west(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y == p2.y:
        if p1.x < p2.x:
            return p1 + south_west(p1.add_x(-space_x), p2, space_x, space_y)
        else:
            return p1 + south_west(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)
    elif p1.y >= p2.y:
        if p1.x <= p2.x:
            return p1 + south_west(p1.add_x(-space_x), p2, space_x, space_y)
        else:
            return p1 + south_west(Point(p2.x - space_x, p1.y), p2, space_x, space_y)
    else:
        return list(reversed(west_west(p2, p1, space_x, space_y)))


def west_south(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y < p2.y:
        if p1.x <= p2.x:
            return p1 + north_south(p1.add_x(-space_x), p2, space_x, space_y)
        else:
            return p1 + north_south(Point(p2.x, p1.y), p2, space_x, space_y)
    else:
        if p1.x <= p2.x:
            return p1 + south_south(p1.add_x(-space_x), p2, space_x, space_y)
        else:
            return p1 + south_south(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)


def west_east(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    return list(reversed(east_west(p2, p1, space_x, space_y)))


def west_north(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y <= p2.y:
        if p1.x <= p2.x:
            return p1 + north_north(p1.add_x(-space_x), p2, space_x, space_y)
        else:
            return p1 + north_north(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)
    else:
        if p1.x <= p2.x:
            return p1 + south_north(p1.add_x(-space_x), p2, space_x, space_y)
        else:
            return p1 + south_north(Point(p2.x, p1.y), p2, space_x, space_y)


def south_west(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    return list(reversed(west_south(p2, p1, space_x, space_y)))


def south_south(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y <= p2.y:
        if p1.x < p2.x:
            return p1 + east_south(p1.add_y(-space_y), p2, space_x, space_y)
        else:
            return p1 + west_south(p1.add_y(-space_y), p2, space_x, space_y)
    else:
        return list(reversed(south_south(p2, p1, space_x, space_y)))


def south_east(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y <= p2.y:
        if p1.x <= p2.x:
            return p1 + east_east(p1.add_y(-space_y), p2, space_x, space_y)
        else:
            return p1 + west_east(p1.add_y(-space_y), p2, space_x, space_y)
    else:
        if p1.x <= p2.x:
            return p1 + east_east(Point(p1.x, get_mid_y(p1, p2)), p2, space_x, space_y)
        else:
            return p1 + west_east(Point(p1.x, p2.y), p2, space_x, space_y)


def south_north(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.x == p2.x and p1.y > p2.y:
        return [p1, p2]
    elif p1.y <= p2.y:
        if p1.x < p2.x:
            return p1 + east_north(p1.add_y(-space_y), p2, space_x, space_y)
        else:
            return p1 + west_north(p1.add_y(-space_y), p2, space_x, space_y)
    else:
        if p1.x <= p2.x:
            return p1 + east_north(Point(p1.x, get_mid_y(p1, p2)), p2, space_x, space_y)
        else:
            return p1 + west_north(Point(p1.x, get_mid_y(p1, p2)), p2, space_x, space_y)


def east_west(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y == p2.y and p1.x < p2.x:
        return [p1, p2]
    elif p1.y < p2.y:
        if p1.x < p2.x:
            return p1 + north_west(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)
        else:
            return p1 + north_west(p1.add_x(space_x), p2, space_x, space_y)
    else:
        if p1.x < p2.x:
            return p1 + south_west(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)
        else:
            return p1 + south_west(p1.add_x(space_x), p2, space_x, space_y)


def east_south(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    return list(reversed(south_east(p2, p1, space_x, space_y)))


def east_east(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y == p2.y and p1.x < p2.x:
        return p1 + south_east(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)
    elif p1.y <= p2.y:
        if p1.x <= p2.x:
            return p1 + north_east(Point(p2.x + space_x, p1.y), p2, space_x, space_y)
        else:
            return p1 + north_east(p1.add_x(space_x), p2, space_x, space_y)
    else:
        return list(reversed(east_east(p2, p1, space_x, space_y)))


def east_north(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.y <= p2.y:
        if p1.x < p2.x:
            return p1 + north_north(Point(get_mid_x(p1, p2), p1.y), p2, space_x, space_y)
        else:
            return p1 + north_north(p1.add_x(space_x), p2, space_x, space_y)
    else:
        if p1.x < p2.x:
            return p1 + south_north(Point(p2.x, p1.y), p2, space_x, space_y)
        else:
            return p1 + south_north(p1.add_x(space_x), p2, space_x, space_y)


def north_west(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    return list(reversed(west_north(p2, p1, space_x, space_y)))


def north_south(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    return list(reversed(south_north(p2, p1, space_x, space_y)))


def north_east(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    return list(reversed(east_north(p2, p1, space_x, space_y)))


def north_north(p1: Point, p2: Point, space_x: float, space_y: float) -> list:
    if p1.x == p2.x:
        if p1.y <= p2.y:
            return p1 + east_north(Point(p1.x, get_mid_y(p1, p2)), p2, space_x, space_y)
        else:
            return p1 + east_north(p1.add_y(space_y), p2, space_x, space_y)
    if p1.y <= p2.y:
        if p1.x < p2.x:
            return p1 + east_north(Point(p1.x, p2.y + space_y), p2, space_x, space_y)
        else:
            return p1 + west_north(Point(p1.x, p2.y + space_y), p2, space_x, space_y)
    else:
        return list(reversed(north_north(p2, p1, space_x, space_y)))


connection_reader = {
        'west_west': lambda p1, p2, space_x, space_y: west_west(p1, p2, space_x, space_y),
        'west_south': lambda p1, p2, space_x, space_y: west_south(p1, p2, space_x, space_y),
        'west_east': lambda p1, p2, space_x, space_y: west_east(p1, p2, space_x, space_y),
        'west_north': lambda p1, p2, space_x, space_y: west_north(p1, p2, space_x, space_y),
        'south_west': lambda p1, p2, space_x, space_y: south_west(p1, p2, space_x, space_y),
        'south_south': lambda p1, p2, space_x, space_y: south_south(p1, p2, space_x, space_y),
        'south_east': lambda p1, p2, space_x, space_y: south_east(p1, p2, space_x, space_y),
        'south_north': lambda p1, p2, space_x, space_y: south_north(p1, p2, space_x, space_y),
        'east_west': lambda p1, p2, space_x, space_y: east_west(p1, p2, space_x, space_y),
        'east_south': lambda p1, p2, space_x, space_y: east_south(p1, p2, space_x, space_y),
        'east_east': lambda p1, p2, space_x, space_y: east_east(p1, p2, space_x, space_y),
        'east_north': lambda p1, p2, space_x, space_y: east_north(p1, p2, space_x, space_y),
        'north_west': lambda p1, p2, space_x, space_y: north_west(p1, p2, space_x, space_y),
        'north_south': lambda p1, p2, space_x, space_y: north_south(p1, p2, space_x, space_y),
        'north_east': lambda p1, p2, space_x, space_y: north_east(p1, p2, space_x, space_y),
        'north_north': lambda p1, p2, space_x, space_y: north_north(p1, p2, space_x, space_y),
    }
